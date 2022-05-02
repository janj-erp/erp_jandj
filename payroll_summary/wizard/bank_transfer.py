from odoo import api, fields, models,_
from datetime import date, datetime ,timedelta


class BankTransfer(models.TransientModel):
    _name = 'bank.transfer.wizard'
    _description = 'Bank Transfer Wizard'

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    payslip_type = fields.Selection([('monthly','Monthly'),
                                     ('weekly','Weekly') ])

    def generate_bank_transfer_summary(self):
        data = {
            'start_date': self.date_from,
             'end_date' : self.date_to,
             'payslip_type': self.payslip_type,
        }
        return self.env.ref('payroll_summary.report_bank_transfer_summary_xls').report_action(self,data=data)