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

    @api.constrains('default_code')
    def sync_default_code(self):
        for rec in self.product_variant_ids:
            if not rec.default_code:
                rec.default_code = self.default_code

    def update_all_variant_codes(self):
        for product in self:
            code = product.default_code
            product.product_variant_ids.default_code = code
            product.default_code = code


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char('Item Code', index=False, required=True)



