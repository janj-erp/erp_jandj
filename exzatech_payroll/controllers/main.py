import io
import re
from PyPDF2 import PdfFileReader, PdfFileWriter
from odoo.http import request, route, Controller
from odoo.tools.safe_eval import safe_eval


class HrPayroll(Controller):

    @route(["/print/payslips"], type='http', auth='user')
    def get_payroll_report_print(self, list_ids='', **post):
        # print('EXZA get_payroll_report_print++++++++++')
        if not request.env.user.has_group('hr_payroll.group_hr_payroll_user') or not list_ids or re.search("[^0-9|,]", list_ids):
            return request.not_found()

        ids = [int(s) for s in list_ids.split(',')]
        payslips = request.env['hr.payslip'].browse(ids)

        pdf_writer = PdfFileWriter()

        for payslip in payslips:
            # if not payslip.struct_id or not payslip.struct_id.report_id:
            #     report = request.env.ref('exzatech_payroll.report_payslip_menu', False)
            # else:
            #     report = payslip.struct_id.report_id
            report = request.env.ref('exzatech_payroll.report_payslip_menu', False)
            # print("@@@@@@@@@@@@@@@", report)
            report = report.with_context(lang=payslip.employee_id.sudo().address_home_id.lang)
            pdf_content, _ = report.sudo()._render_qweb_pdf(payslip.id, data={'company_id': payslip.company_id})
            reader = PdfFileReader(io.BytesIO(pdf_content), strict=False, overwriteWarnings=False)

            for page in range(reader.getNumPages()):
                pdf_writer.addPage(reader.getPage(page))

        _buffer = io.BytesIO()
        pdf_writer.write(_buffer)
        merged_pdf = _buffer.getvalue()
        _buffer.close()

        if len(payslips) == 1 and payslips.struct_id.report_id.print_report_name:
            report_name = safe_eval(payslips.struct_id.report_id.print_report_name, {'object': payslips})
        else:
            report_name = "Payslips"

        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(merged_pdf)),
            ('Content-Disposition', 'attachment; filename=' + report_name + '.pdf;')
        ]

        return request.make_response(merged_pdf, headers=pdfhttpheaders)