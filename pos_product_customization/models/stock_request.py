from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class StockRequest(models.Model):
    _inherit = 'stock.picking'

    is_request = fields.Boolean('Request from POS', default=False)
    is_pos_reserve = fields.Boolean('Reserve sold quant', default=False)

    def create_from_pos(self, data, reserve=False):
        pos_id = self.env['stock.picking.type'].search([('id', '=', data[0].get('warehouse_name')['picking_type_id'][0])])
        w_id = int(pos_id.warehouse_id.id)

        if reserve:
            operation_type = self.env['stock.picking.type'].search(
                [('warehouse_id', '=', w_id), ('name', 'ilike', 'Receipt')], limit=1)
            location = self.env['stock.location'].search([('name', 'ilike', 'Vendor')], limit=1)
        else:
            operation_type = self.env['stock.picking.type'].search(
                [('warehouse_id', '=', int(data[3])), ('name', 'ilike', 'Internal')], limit=1)
            location = self.env['stock.location'].search([('name', '=', 'Stock')])
            for l in location:
                if l.warehouse_id.id == int(data[3]):
                    location = l
                    break
        location_dest = self.env['stock.location'].search([('name', '=', 'Stock')])
        for l in location_dest:
            if l.warehouse_id.id == w_id:
                location_dest = l
                break
        # location_dest = self.env['stock.location'].search([('warehouse_id', '=', pos_id.warehouse_id.id)], limit=1)
        res = self.env['stock.picking'].create({'partner_id': 1, 'picking_type_id': operation_type.id,
                                                'location_id': location.id, 'location_dest_id': location_dest.id,
                                                'scheduled_date': fields.Datetime.now(), 'note': data[4]})
        if reserve:
            res.write({'is_pos_reserve': True})
        else:
            res.write({'is_request': True})
        product = self.env['product.product'].browse(int(data[1]))
        res.move_ids_without_package += self.env['stock.move'].create({'name': 'POS stock request',
                                                                       'product_uom': product.uom_id.id,
                                                                       'product_id': int(data[1]),
                                                                       'product_uom_qty': int(data[2]),
                                                                       'company_id': res.company_id.id,
                                                                       'location_id': location.id,
                                                                       'location_dest_id': location_dest.id,
                                                                       'date': fields.Date.today()})
        if reserve:
            res.action_confirm()
            res.action_set_quantities_to_reservation()
            res.button_validate()

    # def get_products(self):
    #     x = self.env['product.product'].search([])
    #     partners = list()
    #     for partner in x:
    #         name = ""
    #         for attrs in partner.product_template_variant_value_ids:
    #             name += " " + attrs.name
    #         # print(name)
    #         partners.append({'id': partner.id, 'name': partner.name + name})
    #     # return [{'id': 1, 'name': 'Administrator'}, {'id': 2, 'name': 'Admin'}, {'id': 3, 'name': 'Admini'}]
    #     print(partners)
    #     return partners

    def get_products(self):
        rec = self.env['product.product'].search([])
        products = [{'id': product.id, 'name': product.name + ''.join([" " + attrs.name for attrs in product.product_template_variant_value_ids])} for product in rec]
        return products

    def get_warehouses(self):
        rec = self.env['stock.warehouse'].search([])
        warehouses = [{'id': warehouse.id, 'name': warehouse.name} for warehouse in rec]
        return warehouses

    def get_warehouses_with_qty(self, product_id):
        rec = self.env['stock.warehouse'].search([])
        warehouses = [{
            'id': warehouse.id,
            'name': f"["
                    f"{self.env['product.product'].browse(product_id).with_context({'warehouse': warehouse.id,}).qty_available}"
                    f"]NOS - {warehouse.name} ",
        } for warehouse in rec]
        return warehouses

    def get_pos_warehouse_id(self, pos_config_id):
        return self.env['pos.config'].browse(pos_config_id).picking_type_id.warehouse_id.id





