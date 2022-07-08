from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class ProductTags(models.Model):
    _name = 'product.tags'

    name = fields.Char('Tag Desc')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tag_ids = fields.Many2many('product.tags', string='Tags')
    default_code = fields.Char(
        'Item Code', compute='_compute_default_code',
        inverse='_set_default_code', store=True, required=True)
    available_in_pos = fields.Boolean(string='Available in POS',
                                      help='Check if you want this product to appear in the Point of Sale.',
                                      default=True)

    def _set_barcode(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.barcode = self.barcode
        if len(self.product_variant_ids) > 1:
            for variant in self.product_variant_ids:
                variant.barcode = self.barcode

    @api.depends('product_variant_ids.barcode')
    def _compute_barcode(self):
        self.barcode = False
        for template in self:
            if len(template.product_variant_ids) >= 1:
                template.barcode = template.product_variant_ids[0].barcode

    @api.constrains('default_code')
    def sync_default_code(self):
        if not self.default_code:
            self.default_code = self.product_variant_ids[0].default_code 
        for rec in self.product_variant_ids:
            if not rec.default_code:
                rec.default_code = self.default_code
        # if self._name == 'product.template':
        #     if self.default_code:
        #         count = len(self.search([('default_code', '=', self.default_code)]))
        #         if count > 1:
        #             raise ValidationError(_('Cannot Set Duplicate Item Code'))

    def update_all_variant_codes(self):
        for product in self:
            code = product.default_code
            product.product_variant_ids.default_code = code
            product.default_code = code

    # @api.constrains('list_price')
    def list_price_validation(self):
        if self.list_price < 10:
            raise ValidationError('Please enter a valid sales price')

    def add_template_category(self):
        for rec in self:
            if rec.name != rec.pos_categ_id.name:
                template_categ = self.env['pos.category'].create({
                    'name': rec.name,
                    'parent_id': rec.pos_categ_id.id,
                    'image_128': rec.image_128
                })
                for variant in rec.product_variant_ids:
                    variant.pos_categ_id = template_categ

    def remove_template_category(self):
        for rec in self:
            if rec.name == rec.pos_categ_id.name:
                parent_categ = rec.product_variant_ids.pos_categ_id.parent_id
                rec.product_variant_ids.pos_categ_id.unlink()
                for variant in rec.product_variant_ids:
                    variant.pos_categ_id = parent_categ


class Product(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char('Item Code', index=False, required=True)

    _sql_constraints = [
        ('barcode_uniq', 'CHECK(1=1)', 'A barcode can only be assigned to one product !'),
    ]

    @api.onchange('default_code')
    def _onchange_default_code(self):
        return

    def get_warehouse_quant(self, pos_config_id):
        warehouse = self.env['pos.config'].browse(pos_config_id).picking_type_id.warehouse_id
        return self.with_context({'warehouse': warehouse.id}).qty_available

    def confirm_selections(self, products, quants, warehouses, order_name, pos_config):
        order = self.env['pos.advance.sale'].search([('name', '=', order_name)]) or \
                self.env['pos.advance.sale'].sudo().create({'name': order_name, 'pos_config': pos_config})
        order.pos_lines.sudo().unlink()
        for i in range(len(products)):
            product = self.env['product.product'].browse(products[i])
            if product.detailed_type != 'product':
                continue
            pos_warehouse = self.env['pos.config'].browse(pos_config).picking_type_id.warehouse_id
            order.pos_lines += self.env['pos.advance.sale.line'].sudo().create({
                'product_id': products[i],
                'quantity': quants[i],
                'warehouse_id': int(warehouses[i]),
                'store_pos_id': pos_warehouse.id,
            })
        for i in range(len(products)):
            w = int(warehouses[i])
            product = self.env['product.product'].browse(products[i])
            if product.detailed_type != 'product':
                continue
            available_qty = product.with_context({'warehouse': w}).qty_available
            if available_qty < quants[i]:
                order.state = 'new'
                return [
                    False,
                    f"{self.env['stock.warehouse'].browse(w).name} has only '{available_qty}' available for product "
                    f"'{self.env['product.product'].browse(products[i]).display_name}'. But requested is '{quants[i]}'."
                ]
        order.state = 'valid'
        return [True, 'All products available', order.id]


class POSAdvanceSale(models.Model):
    _name = 'pos.advance.sale'
    _description = 'pos.advance.sale'

    name = fields.Char('Order Ref', required=True, readonly=True)
    pos_lines = fields.One2many('pos.advance.sale.line', 'pos_id', string='POS Sale Lines')
    pos_config = fields.Many2one('pos.config', 'POS Store', readonly=True)
    state = fields.Selection([
        ('new', 'New'),
        ('valid', 'Valid'),
        # ('part_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('delivered', 'Goods Delivered')
    ], string='Status', default='new')
    is_transferred = fields.Boolean('Inventory Transfer Done', default=False)
    is_moved_physically = fields.Boolean('Delivered to Store', compute='compute_goods_moved')
    order_id = fields.Many2one('pos.order', compute='compute_order')

    def compute_goods_moved(self):
        for rec in self:
            rec.is_moved_physically = False
            for line in rec.pos_lines:
                if line.state == 'new':
                    return
            rec.is_moved_physically = True

    def compute_order(self):
        for rec in self:
            rec.order_id = self.env['pos.order'].search([('pos_reference', '=', rec.name)], limit=1)

    def create_new(self, order_name, pos_config):
        if not self.env['pos.advance.sale'].search([('name', '=', order_name)]):
            self.env['pos.advance.sale'].sudo().create({'name': order_name, 'pos_config': pos_config})

    def confirm_availability(self):
        for line in self.pos_lines:
            print(line.product_id.detailed_type)
            if line.product_id.detailed_type != 'product':
                continue
            available_qty = line.product_id.with_context({
                'warehouse': line.warehouse_id.id,
            }).qty_available
            if available_qty < line.quantity:
                return [
                    False,
                    f"{line.warehouse_id.name} has only '{available_qty}' available for product "
                    f"'{line.product_id.display_name}'. But requested is '{line.quantity}'."
                ]
        return [True, 'All products available']

    def complete_stock_pickings(self):
        if not self.is_transferred:
            warehouse_dest = self.pos_config.picking_type_id.warehouse_id
            picking_type = self.env['stock.picking.type'].sudo().search([
                ('warehouse_id', '=', warehouse_dest.id),
                ('sequence_code', '=', 'INT')
            ])
            locations = self.env['stock.location'].sudo().search([('name', '=', 'Stock'),])
            for loc in locations:
                if loc.warehouse_id.id == warehouse_dest.id:
                    location_dest = loc
                    break
            for line in self.pos_lines:
                for loc in locations:
                    if loc.warehouse_id.id == line.warehouse_id.id:
                        location = loc
                        break
                picking = self.env['stock.picking'].sudo().create({
                    'partner_id': 1,
                    'picking_type_id': picking_type.id,
                    'location_id': location.id,
                    'location_dest_id': location_dest.id,
                    'scheduled_date': fields.Datetime.now(),
                    'note': "Advance Sale"
                })
                picking.move_ids_without_package += self.env['stock.move'].sudo().create({
                    'name': 'POS Advance Sale Transfer',
                    'product_uom': line.product_id.uom_id.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'company_id': picking.company_id.id,
                    'location_id': location.id,
                    'location_dest_id': location_dest.id,
                    'date': fields.Date.today(),
                })
                picking.action_confirm()
                picking.action_set_quantities_to_reservation()
                picking.button_validate()
            self.is_transferred = True

    def get_active_warehouses(self):
        return [line.warehouse_id.id for line in self.pos_lines]

    def mark_transferred(self):
        for rec in self:
            for line in rec.pos_lines:
                line.state = 'moved'

    def mark_delivered(self):
        for rec in self:
            rec.state = 'delivered'
            for line in rec.pos_lines:
                line.state = 'delivered'

    def mark_fully_paid(self):
        for rec in self:
            rec.state = 'paid'

    def mark_part_paid(self):
        for rec in self:
            rec.state = 'part_paid'


class POSAdvanceSaleLine(models.Model):
    _name = 'pos.advance.sale.line'

    _description = 'pos.advance.sale.line'

    name = fields.Char('Order Name', related='pos_id.name')
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    quantity = fields.Float('Required Quantity', readonly=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'From Location', readonly=True)
    pos_id = fields.Many2one('pos.advance.sale', 'POS Order', readonly=True, ondelete='cascade')
    state = fields.Selection([
        ('new', 'Transfer Pending'),
        ('sent', 'Goods Sent'),
        ('moved', 'Goods Received'),
        ('delivered', 'Goods Delivered'),
    ], string='Status', default='new')
    store_pos_id = fields.Many2one('stock.warehouse', 'To Location', readonly=True,)
    user_warehouse_from_id = fields.Integer('user_warehouse_id', compute='compute_current_user_warehouse_id',
                                            search='search_cur_ware')
    user_warehouse_to_id = fields.Integer('user_warehouse_id', compute='compute_current_user_warehouse_to_id',
                                          search='search_cur_to_ware')

    def compute_current_user_warehouse_id(self):
        self.user_warehouse_from_id = self.env.user.property_warehouse_id and self.env.user.property_warehouse_id.id or 0

    def search_cur_ware(self, operator, value):
        id = self.env.user.property_warehouse_id and self.env.user.property_warehouse_id.id or 0
        if not id:
            lines = self.env['pos.advance.sale.line'].search([])
        else:
            lines = self.env['pos.advance.sale.line'].search([('warehouse_id', '=', id)])
        return [('id', 'in', lines.mapped('id'))]

    def compute_current_user_warehouse_to_id(self):
        self.user_warehouse_to_id = self.env.user.property_warehouse_id and self.env.user.property_warehouse_id.id or 0

    def search_cur_to_ware(self, operator, value):
        id = self.env.user.property_warehouse_id and self.env.user.property_warehouse_id.id or 0
        if not id:
            lines = self.env['pos.advance.sale.line'].search([])
        else:
            lines = self.env['pos.advance.sale.line'].search([('store_pos_id', '=', id)])
        return [('id', 'in', lines.mapped('id'))]

    def mark_as_sent(self):
        for rec in self:
            rec.state = 'sent'

    def mark_as_receive(self):
        for rec in self:
            rec.state = 'moved'
