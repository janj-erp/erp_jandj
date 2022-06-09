from odoo import models, fields, api, _


class ResUsersInherit(models.Model):
    _inherit = 'hr.employee'

    related_user = fields.Many2one('res.users', string='Related User')