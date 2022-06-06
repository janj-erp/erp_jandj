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

    @api.constrains('list_price')
    def list_price_validation(self):
        if self.list_price < 10:
            raise ValidationError('Please enter a valid sales price')


class Product(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char('Item Code', index=False, required=True)

    _sql_constraints = [
        ('barcode_uniq', 'CHECK(1=1)', 'A barcode can only be assigned to one product !'),
    ]

    @api.onchange('default_code')
    def _onchange_default_code(self):
        return
    
    
    
    
    
 ##Move to new module later

class ResBankIn(models.Model):
    _inherit = 'res.bank'

    branch_name = fields.Char('Branch Name')
    

class BankAccountIn(models.Model):
    _inherit = 'res.partner.bank'

    branch_name = fields.Char('Branch Name', related='bank_id.branch_name')




