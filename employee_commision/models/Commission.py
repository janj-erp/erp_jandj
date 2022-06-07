# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields
import datetime


class Commission(models.Model):
    _name = 'hr.employee.commission'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    conf_id = fields.Many2one('commission.conf', string='Configuration Id')
    line_ids = fields.One2many('commission.lines', 'employee_commission_id', string='Lines')

    def get_pending_commission_total_sale_sum(self, wizard_id):
        wizard = self.env['commission.slip.print'].browse(wizard_id)
        lines = self.line_ids.filtered(lambda l: wizard.date_from <= l.date <= wizard.date_to and l.state == 'pending')
        return sum(lines.mapped('total_sales_amount'))

    def get_pending_commission_amount_sum(self, wizard_id):
        wizard = self.env['commission.slip.print'].browse(wizard_id)
        lines = self.line_ids.filtered(lambda l: wizard.date_from <= l.date <= wizard.date_to and l.state == 'pending')
        return sum(lines.mapped('amount'))

