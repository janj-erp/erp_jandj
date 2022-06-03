import base64
import io
from odoo import models
from datetime import date, datetime ,timedelta


class PayrollSummary (models.AbstractModel):
    _name = 'report.exzatech_payroll.report_payroll_summary_xls'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, payslips):
        domain = []
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        structure_id = data.get('structure_id')
        rec = self.env['hr.payroll.structure'].search([('id','=',structure_id)])
        #"Intership Stipend"
        domain += [('date_from', '>=', start_date)]
        domain += [('date_to', '<=', end_date)]
        domain += [('struct_id', '=', structure_id)]
        domain += [('state', 'in', ['verify', 'done', 'paid'])]
        sheet = workbook.add_worksheet('Payslips')
        bold = workbook.add_format({'bold': True})
        row = 0
        col = 2
        sheet.write(row, col, 'Exzatech Consulting and Services Private Limited', bold)
        format_str = '%Y-%m-%d'
        datetime_obj = datetime.strptime(start_date, format_str)

        sheet.write(row + 1, col, datetime_obj.strftime("%B - %Y") + '- Payroll Summary', bold)
        row = 3
        col = 0
        if rec.name == "Intership Stipend":
            title = ['S.No', 'Employee No', 'Employee Name',
                     'Bank Account Number',
                     'PAN', 'Stipend', 'Income Tax', 'Net Pay']
            # 'Gross','Total Deductions',
            for i in range(len(title)):
                sheet.set_column('T:T', 13)
                sheet.write(row, col + i, title[i], bold)
            payslips = self.env['hr.payslip'].search(domain).sorted(
                key=lambda r: r.employee_id.identification_id if r.employee_id.identification_id else 'zzzzz')
            total_stipend = total_net = total_it = 0
            s_no = 0
            for payslip in payslips:
                row += 1
                col = 0
                s_no = s_no + 1
                sheet.write(row, col, s_no)
                col = col + 1
                sheet.write(row, col,payslip.employee_id.identification_id if payslip.employee_id.identification_id else ' ')
                col = col + 1
                sheet.write(row, col, payslip.employee_id.name)
                col = col + 1
                sheet.write(row, col,payslip.employee_id.bank_account_id.acc_number if payslip.employee_id.bank_account_id.acc_number else ' ')
                col = col + 1
                sheet.write(row, col, payslip.employee_id.pan_card_number if payslip.employee_id.pan_card_number else ' ')
                col = col + 1
                rec = {}
                for line in payslip.line_ids:
                    if line.code == 'STIPEND':
                        rec.update({"STIPEND": line.total})
                        total_stipend += line.total
                    # if line.code == 'GROSS':
                    #     rec.update({"GROSS": line.total})
                    #     total_gross += line.total
                    if line.code == 'IT':
                        rec.update({"IT": line.total})
                        total_it += line.total
                    # if line.code == 'TD':
                    #     rec.update({"TD": line.total})
                    #     total_td += line.total
                    if line.code == 'NET':
                        rec.update({"NET": round(line.total)})
                        total_net += round(line.total)
                num = len(title)
                for i in range(num):
                    col = 5
                    sheet.set_column('T:T', 13)
                    sheet.write(row, col, rec.get('STIPEND'))
                    col = col + 1
                    # sheet.write(row, col, rec.get('GROSS'))
                    # col = col + 1
                    sheet.write(row, col, rec.get('IT'))
                    col = col + 1
                    # sheet.write(row, col, rec.get('TD'))
                    # col = col + 1
                    sheet.write(row, col, rec.get('NET'))
                    col = col + 1
            row += 1
            col = 2
            sheet.write(row, col, 'Grand Total', bold)
            num = len(title)
            for i in range(num):
                col = 5
                sheet.write(row, col, total_stipend, bold)
                col = col + 1
                # sheet.write(row, col, total_gross, bold)
                # col = col + 1
                sheet.write(row, col, total_it, bold)
                col = col + 1
                # sheet.write(row, col, total_td, bold)
                # col = col + 1
                sheet.write(row, col, total_net, bold)
                col = col + 1
        else:
            title = ['S.No', 'Employee No','Employee Name',
                     'Bank Account Number', 'PAN',
                     'Basic Pay', 'HRA',
                     'Leave Travel Alloance', 'Standard Deduction',
                     'Food Coupon (Allowance)', 'Onsite Allowance', 'Shift Allowance',
                     'Spl Allowance','Gross',
                     'Employee PF Contribution', 'Food Coupon (Deduction)',
                     'Income Tax', 'HR Deductions', 'Other Deductions',
                     'Professional Tax', 'Total Deductions', 'Net Pay',
                     ]
            for i in range(len(title)):
                sheet.set_column('T:T', 13)
                sheet.write(row, col + i, title[i], bold)
            payslips = self.env['hr.payslip'].search(domain).sorted(key=lambda r: r.employee_id.identification_id if r.employee_id.identification_id else 'zzzzz')
            total_basic = total_stipend =total_hra = total_lta = total_sd = 0
            total_fca = total_onsite = total_shift = 0
            total_spl = total_gross = 0
            total_epf = total_fcd = total_it = 0
            total_hrd = total_other = total_pt = 0
            total_td = total_net = 0
            s_no = 0
            for payslip in payslips:
                row += 1
                col = 0
                s_no = s_no + 1
                sheet.write(row, col, s_no)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.identification_id if payslip.employee_id.identification_id else ' ')
                col = col + 1
                sheet.write(row, col, payslip.employee_id.name)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.bank_account_id.acc_number if payslip.employee_id.bank_account_id.acc_number else ' ')
                col = col + 1
                sheet.write(row, col, payslip.employee_id.pan_card_number if payslip.employee_id.pan_card_number else ' ')
                col = col + 1
                rec = {}
                for line in payslip.line_ids:
                    if line.code == 'BASIC':
                        rec.update({"BASIC": line.total})
                        total_basic += line.total
                    if line.code == 'HRA':
                        rec.update({"HRA": line.total})
                        total_hra += line.total
                    if line.code == 'LTA':
                        rec.update({"LTA": line.total})
                        total_lta += line.total
                    if line.code == 'SD':
                        rec.update({"SD": line.total})
                        total_sd += line.total
                    if line.code == 'FCA':
                        rec.update({"FCA": line.total})
                        total_fca += line.total
                    if line.code == 'ONSITE':
                        rec.update({"ONSITE": line.total})
                        total_onsite += line.total
                    if line.code == 'SHIFT':
                        rec.update({"SHIFT": line.total})
                        total_shift += line.total
                    if line.code == 'SPL':
                        rec.update({"SPL": line.total})
                        total_spl += line.total
                    if line.code == 'GROSS':
                        rec.update({"GROSS": line.total})
                        total_gross += line.total
                    if line.code == 'EPF':
                        rec.update({"EPF": line.total})
                        total_epf += line.total
                    if line.code == 'FCD':
                        rec.update({"FCD": line.total})
                        total_fcd += line.total
                    if line.code == 'IT':
                        rec.update({"IT": line.total})
                        total_it += line.total
                    if line.code == 'HRD':
                        rec.update({"HRD": line.total})
                        total_hrd += line.total
                    if line.code == 'OTHER':
                        rec.update({"OTHER": line.total})
                        total_other += line.total
                    if line.code == 'PT':
                        rec.update({"PT": line.total})
                        total_pt += line.total
                    if line.code == 'TD':
                        rec.update({"TD": line.total})
                        total_td += line.total
                    if line.code == 'NET':
                        rec.update({"NET": round(line.total)})
                        total_net += round(line.total)
                num = len(title)
                for i in range(num):
                    col = 5
                    sheet.set_column('T:T', 13)
                    sheet.write(row, col, rec.get('BASIC'))
                    col = col + 1
                    sheet.write(row, col, rec.get('HRA'))
                    col = col + 1
                    sheet.write(row, col, rec.get('LTA'))
                    col = col + 1
                    sheet.write(row, col, rec.get('SD'))
                    col = col + 1
                    sheet.write(row, col, rec.get('FCA'))
                    col = col + 1
                    sheet.write(row, col, rec.get('ONSITE'))
                    col = col + 1
                    sheet.write(row, col, rec.get('SHIFT'))
                    col = col + 1
                    sheet.write(row, col, rec.get('SPL'))
                    col = col + 1
                    sheet.write(row, col, rec.get('GROSS'))
                    col = col + 1
                    sheet.write(row, col, rec.get('EPF'))
                    col = col + 1
                    sheet.write(row, col, rec.get('FCD'))
                    col = col + 1
                    sheet.write(row, col, rec.get('IT'))
                    col = col + 1
                    sheet.write(row, col, rec.get('HRD'))
                    col = col + 1
                    sheet.write(row, col, rec.get('OTHER'))
                    col = col + 1
                    sheet.write(row, col, rec.get('PT'))
                    col = col + 1
                    sheet.write(row, col, rec.get('TD'))
                    col = col + 1
                    sheet.write(row, col, rec.get('NET'))
                    col = col + 1
            row += 1
            col = 2
            sheet.write(row, col, 'Grand Total', bold)
            num = len(title)
            for i in range(num):
                col = 5
                sheet.write(row, col, total_basic, bold)
                col = col + 1
                sheet.write(row, col, total_hra, bold)
                col = col + 1
                sheet.write(row, col, total_lta, bold)
                col = col + 1
                sheet.write(row, col, total_sd, bold)
                col = col + 1
                sheet.write(row, col, total_fca, bold)
                col = col + 1
                sheet.write(row, col, total_onsite, bold)
                col = col + 1
                sheet.write(row, col, total_shift, bold)
                col = col + 1
                sheet.write(row, col, total_spl, bold)
                col = col + 1
                sheet.write(row, col, total_gross, bold)
                col = col + 1
                sheet.write(row, col, total_epf, bold)
                col = col + 1
                sheet.write(row, col, total_fcd, bold)
                col = col + 1
                sheet.write(row, col, total_it, bold)
                col = col + 1
                sheet.write(row, col, total_hrd, bold)
                col = col + 1
                sheet.write(row, col, total_other, bold)
                col = col + 1
                sheet.write(row, col, total_pt, bold)
                col = col + 1
                sheet.write(row, col, total_td, bold)
                col = col + 1
                sheet.write(row, col, total_net, bold)
                col = col + 1
