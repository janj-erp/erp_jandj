import base64
import io
from odoo import models
from datetime import date, datetime ,timedelta


class BankTransferSummaryXlsx(models.AbstractModel):
    _name = 'report.payroll_summary.report_bank_transfer_summary_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, payslips):
        domain = []
        start_date = data.get('start_date')
        end_date =  data.get('end_date')
        domain += [('date_from','>=',start_date)]
        domain += [('date_to','<=',end_date)]
        sheet = workbook.add_worksheet('Payslips')
        bold = workbook.add_format({'bold': True})
        row = 0
        col = 1
        sheet.write(row, col, 'J & J UNITED LIMITED', bold)
        format_str = '%Y-%m-%d'
        datetime_obj  = datetime.strptime(start_date, format_str)
        date_from = datetime.strptime(start_date, format_str)
        date_to  = datetime.strptime(end_date, format_str)
        if 'monthly' in data.get('payslip_type'):
            sheet.write(row+1, col,datetime_obj.strftime("%B - %Y")+'- Bank Transfer Summary' , bold)
        else :
            sheet.write(row + 1, col, 'Weekly Payroll Summary : Period from  '  + date_from.strftime("%d-%b-%Y") + ' - to - '  + date_to.strftime("%d-%b-%Y") , bold)
        row = 3
        col = 0
        title = [ 'S.No','Employee Name',
                  'Bank Account Number',
                  'Net Salary',
                 ]
        for i in range(len(title)):
            sheet.set_column('T:T', 13)
            sheet.write(row, col + i , title[i] , bold)
        payslips = self.env['hr.payslip'].search(domain)
        total_net = 0
        s_no = 0
        for payslip in payslips:
            if data.get('payslip_type') in payslip.struct_id.name.casefold():
                row += 1
                col = 0
                s_no = s_no + 1
                sheet.write(row, col,s_no)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.name)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.bank_account_id.acc_number if payslip.employee_id.bank_account_id.acc_number else ' ')
                col = col + 1
                rec = {}
                for line in payslip.line_ids :
                    if line.code == 'NET':
                        rec.update({"NET": round(line.total)})
                        total_net += round(line.total)
                num = len(title)
                for i in range(num):
                    col = 3
                    sheet.write(row, col, rec.get('NET'))
                    col = col + 1
        row += 1
        col = 1
        sheet.write(row, col, 'Grand Total', bold)
        num = len(title)
        for i in range(num):
            col = 3
            sheet.write(row, col, total_net, bold)
            col = col + 1






























