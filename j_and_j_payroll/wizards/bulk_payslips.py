from odoo import api, fields, models,_
from datetime import date, datetime ,timedelta
from odoo.tools.misc import format_date


class BulkPayslips(models.TransientModel):
    _name = 'bulk.payslip.wizard'
    _description = 'Wizard to generate bulk payslips'

    structure_id = fields.Many2one('hr.payroll.structure', "Structure")
    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")



    def create_bulk_payslips(self):
        payslip = self.env['hr.payslip']
        structure_id = self.structure_id.id
        employee = self.env['hr.employee'].search([('structure','=',structure_id)])
        date_from = self.date_from
        date_to = self.date_to
        batch_obj = self.env['hr.payslip.run']
        batch = batch_obj.create({'name': format_date(self.env, date_from, date_format="MMMM y"),
                                  'date_start': date_from,
                                  'date_end': date_to,
                                  })
        for emp in employee:
            if emp.contract_id :
                vals = {'employee_id': emp.id,
                        'struct_id': emp.structure.id,
                        'date_from': date_from,
                        'date_to': date_to,
                        'contract_id':emp.contract_id.id,
                        'name': '%(payslip_name)s - %(employee_name)s - %(dates)s' % {
                            'payslip_name': 'Salary Slip',
                            'employee_name': emp.name,
                            'dates': format_date(self.env, date_from, date_format="MMMM y")},
                        'payslip_run_id': batch.id,
                        }
                new_rec = payslip.create(vals)
                new_rec.calculate_employee_working_hours_in_current_week()
                new_rec.get_total_number_of_days()
                new_rec.get_total_unpaid_of_days()
                new_rec.compute_sheet()


