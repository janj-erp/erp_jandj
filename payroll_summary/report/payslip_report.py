import base64
import io
from odoo import models
from datetime import date, datetime ,timedelta


class PayrollSummaryXlsx(models.AbstractModel):
    _name = 'report.payroll_summary.report_payroll_summary_xls'
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
            sheet.write(row+1, col,datetime_obj.strftime("%B - %Y")+'- Payroll Summary' , bold)
        else :
            sheet.write(row + 1, col, 'Weekly Payroll Summary : Period from  '  + date_from.strftime("%d-%b-%Y") + ' - to - '  + date_to.strftime("%d-%b-%Y") , bold)
        row = 3
        col = 0
        title = [ 'S.No','Name',
                 'TRN','NIS Number','Bank Account Number',
                 'Days not worked',
                 'Total Hours', 'Worked Hours',
                 'Basic Pay',
                 'Travel Allowance','Food Coupon',
                 'Entertainment','Accommodation',
                 'Normal OT', 'Holiday OT',
                 'Bonus','Vacation','Maternity',
                 'Gross', 'Taxable Gross Pay' , 'Non-taxable Pay',
                 '3% NIS Employee', '2% NHT Employee', '2.25% ED.TAX Employee',
                 'Loam Repayments', '25% P.A.Y.E', 'Total Deductions',
                 'Net Pay',
                 '3% NIS Employer' ,'3% NHT Employer',
                 '3.5% ED.TAX Employer' , '3% HEART'
                 ]
        for i in range(len(title)):
            sheet.set_column('T:T', 13)
            sheet.write(row, col + i , title[i] , bold)
        payslips = self.env['hr.payslip'].search(domain)
        total_basic = total_dnw = total_ta = total_ea = total_acc = total_not = total_hot = 0
        total_fc = total_tg = total_loan = total_ntg = total_nis = total_nise = 0
        total_paye = total_nht = total_nhte = total_edt = total_edte = total_heart = 0
        total_td = total_net = total_gross = total_bonus = total_vac = total_mat = 0
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
                sheet.write(row, col, payslip.employee_id.trn_number if payslip.employee_id.trn_number else ' ')
                col = col + 1
                sheet.write(row, col, payslip.employee_id.nis_number if payslip.employee_id.nis_number else ' ')
                col = col + 1
                sheet.write(row, col, payslip.employee_id.bank_account_id.acc_number if payslip.employee_id.bank_account_id.acc_number else ' ')
                col = col + 1
                rec = {}
                for line in payslip.line_ids :
                    if line.code == 'DNW':
                        rec.update({"DNW": line.total})
                        total_dnw += 0
                    if line.code == 'THRS':
                        rec.update({"THRS": line.total})
                        total_dnw += 0
                    if line.code == 'WHRS':
                        rec.update({"WHRS": line.total})
                        total_dnw += 0
                    if line.code == 'BASIC':
                        rec.update({"basic":line.total })
                        total_basic += line.total
                    if line.code == 'TA':
                        rec.update({"TA": line.total})
                        total_ta += line.total
                    if line.code == 'FC':
                        rec.update({"FC": line.total})
                        total_fc += line.total
                    if line.code == 'EA':
                        rec.update({"EA": line.total})
                        total_ea += line.total
                    if line.code == 'ACC':
                        rec.update({"ACC": line.total})
                        total_acc += line.total
                    if line.code == 'NOT':
                        rec.update({"NOT": line.total})
                        total_not += line.total
                    if line.code == 'HOT':
                        rec.update({"HOT": line.total})
                        total_hot += line.total
                    if line.code == 'GROSS':
                        rec.update({"GROSS": line.total})
                        total_gross += line.total
                    if line.code == 'TG':
                        rec.update({"TG": line.total})
                        total_tg += line.total
                    if line.code == 'LOAN':
                        rec.update({"LOAN": line.total})
                        total_loan += line.total
                    if line.code == 'NTG':
                        rec.update({"NTG": line.total})
                        total_ntg += line.total
                    if line.code == 'NIS':
                        rec.update({"NIS": line.total})
                        total_nis += line.total
                    if line.code == 'NHT':
                        rec.update({"NHT": line.total})
                        total_nht += line.total
                    if line.code == 'EDT':
                        rec.update({"EDT": line.total})
                        total_edt += line.total
                    if line.code == 'TD':
                        rec.update({"TD": line.total})
                        total_td += line.total
                    if line.code == 'NET':
                        rec.update({"NET": round(line.total)})
                        total_net += round(line.total)
                    if line.code == 'NISE':
                        rec.update({"NISE": line.total})
                        total_nise += line.total
                    if line.code == 'NHTE':
                        rec.update({"NHTE": line.total})
                        total_nhte += line.total
                    if line.code == 'EDTE':
                        rec.update({"EDTE": line.total})
                        total_edte += line.total
                    if line.code == 'PAYE':
                        rec.update({"PAYE": line.total})
                        total_paye += line.total
                    if line.code == 'HEART':
                        rec.update({"HEART": line.total})
                        total_heart += line.total
                    if line.code == 'BONUS':
                        rec.update({"BONUS": line.total})
                        total_bonus += line.total
                    if line.code == 'VAC':
                        rec.update({"VAC": line.total})
                        total_vac += line.total
                    if line.code == 'MAT':
                        rec.update({"MAT": line.total})
                        total_mat += line.total
                num = len(title)
                for i in range(num):
                    col = 5
                    sheet.set_column('T:T', 13)
                    sheet.write(row, col, rec.get('DNW'))
                    col = col + 1
                    sheet.write(row, col, rec.get('THRS'))
                    col = col + 1
                    sheet.write(row, col, rec.get('WHRS'))
                    col = col + 1
                    sheet.write(row, col, rec.get('basic'))
                    col = col + 1
                    sheet.write(row, col , rec.get('TA'))
                    col = col + 1
                    sheet.write(row, col, rec.get('FC'))
                    col = col + 1
                    sheet.write(row, col, rec.get('EA'))
                    col = col + 1
                    sheet.write(row, col, rec.get('ACC'))
                    col = col + 1
                    sheet.write(row, col, rec.get('NOT'))
                    col = col + 1
                    sheet.write(row, col, rec.get('HOT'))
                    col = col + 1
                    sheet.write(row, col, rec.get('BONUS'))
                    col = col + 1
                    sheet.write(row, col, rec.get('VAC'))
                    col = col + 1
                    sheet.write(row, col, rec.get('MAT'))
                    col = col + 1
                    sheet.write(row, col, rec.get('GROSS'))
                    col = col + 1
                    sheet.write(row, col , rec.get('TG'))
                    col = col + 1
                    sheet.write(row, col, rec.get('NTG'))
                    col = col + 1
                    sheet.write(row, col,rec.get('NIS'))
                    col = col + 1
                    sheet.write(row, col, rec.get('NHT'))
                    col = col + 1
                    sheet.write(row, col, rec.get('EDT'))
                    col = col + 1
                    sheet.write(row, col, rec.get('LOAN'))
                    col = col + 1
                    sheet.write(row, col, rec.get('PAYE'))
                    col = col + 1
                    sheet.write(row, col, rec.get('TD'))
                    col = col + 1
                    sheet.write(row, col, rec.get('NET'))
                    col = col + 1
                    sheet.write(row, col, rec.get('NISE'))
                    col = col + 1
                    sheet.write(row, col, rec.get('NHTE'))
                    col = col + 1
                    sheet.write(row, col, rec.get('EDTE'))
                    col = col + 1
                    sheet.write(row, col, rec.get('HEART'))
                    col = col + 1
        row += 1
        col = 1
        sheet.write(row, col, 'Grand Total', bold)
        num = len(title)
        for i in range(num):
            # row += 1
            col = 5
            sheet.write(row, col, total_dnw, bold)
            col = col + 1
            sheet.write(row, col, total_dnw, bold)
            col = col + 1
            sheet.write(row, col, total_dnw, bold)
            col = col + 1
            sheet.write(row, col, total_basic, bold)
            col = col + 1
            sheet.write(row, col, total_ta, bold)
            col = col + 1
            sheet.write(row, col, total_fc, bold)
            col = col + 1
            sheet.write(row, col, total_ea, bold)
            col = col + 1
            sheet.write(row, col, total_acc, bold)
            col = col + 1
            sheet.write(row, col, total_not, bold)
            col = col + 1
            sheet.write(row, col, total_hot, bold)
            col = col + 1
            sheet.write(row, col, total_bonus, bold)
            col = col + 1
            sheet.write(row, col, total_vac, bold)
            col = col + 1
            sheet.write(row, col, total_mat, bold)
            col = col + 1
            sheet.write(row, col, total_gross, bold)
            col = col + 1
            sheet.write(row, col, total_tg, bold)
            col = col + 1
            sheet.write(row, col, total_ntg, bold)
            col = col + 1
            sheet.write(row, col, total_nis, bold)
            col = col + 1
            sheet.write(row, col, total_nht, bold)
            col = col + 1
            sheet.write(row, col, total_edt, bold)
            col = col + 1
            sheet.write(row, col, total_loan, bold)
            col = col + 1
            sheet.write(row, col, total_paye, bold)
            col = col + 1
            sheet.write(row, col, total_td, bold)
            col = col + 1
            sheet.write(row, col, total_net, bold)
            col = col + 1
            sheet.write(row, col, total_nise, bold)
            col = col + 1
            sheet.write(row, col, total_nhte, bold)
            col = col + 1
            sheet.write(row, col, total_edte, bold)
            col = col + 1
            sheet.write(row, col, total_heart, bold)
            col = col + 1





























