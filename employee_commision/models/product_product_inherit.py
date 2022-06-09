from odoo import models, api, fields


class Product(models.Model):
    _inherit = 'product.product'

    include_in_commission = fields.Boolean('Included in Commission', default=True)
