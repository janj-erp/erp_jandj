from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class ProductTags(models.Model):
    _name = 'product.tags'

    name = fields.Char('Tag Desc')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tag_ids = fields.Many2many('product.tags', string='Tags')
