from odoo import models, fields

class Company(models.Model):
    _inherit = 'res.company'

    url = fields.Char('URL')
    corporate_id = fields.Char('Corporate Id')
    username = fields.Char('Username')
    password = fields.Char('Password')
