from odoo import fields, models, _


class HrPaylsip(models.Model):
    _name = "hr.payslip"
    _inherit = ['hr.payslip', 'portal.mixin']
