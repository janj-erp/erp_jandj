from odoo import models, fields


class TerminationReason(models.Model):
    _name = 'employee.termination'

    emp_terminate = fields.Many2one('hr.employee')
    reason_termination = fields.Char('Termination Reason')