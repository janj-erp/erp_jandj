from odoo import models, fields
from datetime import datetime


class Employee(models.Model):
    _inherit = 'hr.employee'

    father_name = fields.Char(string="Father Name", required=False)
    father_address = fields.Char(string="Father Address")
    dob_father = fields.Date(string="Father Date Of Birth")
    father_occupation = fields.Char(string="Father Occupation")
    father_phone = fields.Char(string="Father Phone No")
    mother_name = fields.Char(string="Mother Name")
    dob_mother = fields.Date(string="Mother Date Of Birth")
    mother_address = fields.Char(string="Mother Address")
    mother_occupation = fields.Char(string="Mother Occupation")
    mother_phone = fields.Char(string="Mother Phone No")
    spouse_name = fields.Char(string="Spouse Name")
    dob_spouse = fields.Date(string="Spouse Date Of Birth")
    spouse_address = fields.Char(string="Spouse Address")
    spouse_occupation = fields.Char(string="Spouse Occupation")
    spouse_phone = fields.Char(string="Spouse Phone No")
    mobile_1 = fields.Char(string='Mobile 1')
    mobile_2 = fields.Char(string='Mobile 2')
    id_type = fields.Char(string='ID Type')
    employee_joining_date = fields.Date('Date of Joining', compute='_hired_date')
    layoff_start_date = fields.Date(string="Lay Off Start Date")
    layoff_end_date = fields.Date(string="Lay Off End Date")
    layoff_reason = fields.Char(string="Reason for Layoff")
    suspension_start_date = fields.Date(string="Suspension Start Date")
    suspension_end_date = fields.Date(string="Suspension End Date")
    suspension_reason = fields.Char(string="Reason for Suspension")
    suspension_period = fields.Char('Period of Suspension')
    notice_week_pay_duration = fields.Char('Notice Payment Duration')
    employement_duration = fields.Char('Employment Duration')
    emp_history = fields.One2many('employee.experience', 'emp_history')
    employee_qualification = fields.One2many('employee.qualification', 'employee_qualification')
    emp_terminate = fields.One2many('employee.termination', 'emp_terminate')
    store = fields.Char('Store Name', compute='_store_name')
    ref_name_1 = fields.Char()
    ref_address_1 = fields.Char()
    relationship_ref_1 = fields.Char()
    ref_occupation_1 = fields.Char()
    ref_phone_1 = fields.Char()
    ref_name_2 = fields.Char()
    ref_address_2 = fields.Char()
    relationship_ref_2 = fields.Char()
    ref_occupation_2 = fields.Char()
    ref_phone_2 = fields.Char()
    ref_name_3 = fields.Char()
    ref_address_3 = fields.Char()
    relationship_ref_3 = fields.Char()
    ref_occupation_3 = fields.Char()
    ref_phone_3 = fields.Char()
    trn_no = fields.Char()
    nis_no = fields.Char()
    employee_salary = fields.Float()

    def _store_name(self):
        res = self.env['pos.config'].search([('salesperson_ids', '=', self.id)])
        vals = res.picking_type_id.warehouse_id.name
        self.store = vals

    def _hired_date(self):
        res = self.env['hr.contract.history'].search([('employee_id', '=', self.id)])
        vals = res.date_hired
        self.employee_joining_date = vals









