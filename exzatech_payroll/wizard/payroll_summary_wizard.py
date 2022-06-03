from odoo import api, fields, models,_
from datetime import date, datetime ,timedelta
from dateutil.relativedelta import relativedelta

class PayrollSummary(models.TransientModel):
    _name = 'payroll.summary.wizard'
    _description = 'Payroll Summary Wizard'

    date_from = fields.Date("Date From", default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    date_to = fields.Date("Date To", default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    structure_id = fields.Many2one('hr.payroll.structure', "Structure")

    def generate_payroll_summary(self):
        data = {
            'start_date': self.date_from,
             'end_date': self.date_to,
             'structure_id': self.structure_id.id,
        }
        return self.env.ref('exzatech_payroll.report_payroll_summary_xls').report_action(self, data=data)
