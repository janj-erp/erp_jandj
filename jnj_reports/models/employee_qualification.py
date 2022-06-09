from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class EmployeeQualification(models.Model):
    _name = 'employee.qualification'


    employee_qualification = fields.Many2one('hr.employee')
    institute_type = fields.Char(string='Institute Type')
    institute_name = fields.Char(string='Institute Name')
    degree_received = fields.Char('Certificate Received or Expected')
    years_completed_of_course = fields.Integer(string='Years Completed')
    ref_name_1 = fields.Char(string="First Reference Name")
    ref_address_1 = fields.Char(string=" First Reference Address")
    relationship_ref_1 = fields.Char(string="First Reference Relationship")
    ref_occupation_1 = fields.Char(string="First Reference Occupation")
    ref_phone_1 = fields.Char(string="First Reference Phone No")
    ref_name_2 = fields.Char(string="Second Reference Name")
    ref_address_2 = fields.Char(string="Second Reference Address")
    relationship_ref_2 = fields.Char(string="Second Reference Relationship")
    ref_occupation_2 = fields.Char(string="Second Reference Occupation")
    ref_phone_2 = fields.Char(string="Second Reference Phone No")
    ref_name_3 = fields.Char(string="Third Reference Name")
    ref_address_3 = fields.Char(string="Third Reference Address")
    relationship_ref_3 = fields.Char(string="Third Reference Relationship")
    ref_occupation_3 = fields.Char(string="Third Reference Occupation")
    ref_phone_3 = fields.Char(string="Third Reference Phone No")
