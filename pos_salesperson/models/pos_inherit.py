from odoo import models,fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    salesperson_ids = fields.Many2many('hr.employee', 'hr_employee_pos_config_salesperson_rel', string='Sales People')
