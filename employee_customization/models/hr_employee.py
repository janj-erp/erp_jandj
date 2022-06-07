from odoo import api, fields, models, _
from datetime import date, datetime
from odoo.exceptions import UserError
from werkzeug.urls import url_encode


class ReportActivity(models.Model):
    _inherit = 'hr.employee'

    read_id = fields.Boolean("Title True", compute="compute_job_title")

    def compute_job_title(self):
        self.read_id = self.env.user.has_group('base.group_system')


class ResBankIn(models.Model):
    _inherit = 'res.bank'

    branch_name = fields.Char('Branch Name')

    def name_get(self):
        return [(rec.id, f"{rec.name}{rec.branch_name and '/' + rec.branch_name or ''}") for rec in self]


class BankAccountIn(models.Model):
    _inherit = 'res.partner.bank'

    account_type = fields.Selection([
        ('savings', 'Savings Account'),
        ('current', 'Current Account')
    ], 'Account Type')

