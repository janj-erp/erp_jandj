from odoo import api, fields, models,_
from datetime import date, datetime ,timedelta
from odoo.tools.misc import format_date


class BankTransfer(models.TransientModel):
    _name = 'bank.transfer.wizard'
    _description = 'Bank Transfer Wizard'

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    payslip_type = fields.Selection([('monthly','Monthly'),
                                     ('weekly','Weekly') ])

    def generate_bank_transfer_summary(self):
        report = self.env['ir.actions.report']._get_report_from_name('payroll_summary.report_bank_transfer_summary_xls')
        date_from = self.date_from
        date_to = self.date_to
        if self.payslip_type == 'weekly':
            report.name = 'Bank Transfer Summary - %(payslip_type)s -  %(date_start)s  To  %(date_end)s' % {
                                              'payslip_type': self.payslip_type,
                                              'date_start': format_date(self.env, date_from, date_format="d MMM y"),
                                              'date_end': format_date(self.env, date_to, date_format="d MMM y"),
                                          }
        else:
            report.name = 'Bank Transfer Summary -  %(date_start)s' % {
                'date_start': format_date(self.env, date_from, date_format="MMM y"),
            }
        data = {
            'start_date': self.date_from,
             'end_date' : self.date_to,
             'payslip_type': self.payslip_type,
        }
        return self.env.ref('payroll_summary.report_bank_transfer_summary_xls').report_action(self,data=data)