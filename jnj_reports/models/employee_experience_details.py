from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class EmployeeHistory(models.Model):
    _name = 'employee.experience'


    emp_history = fields.Many2one('hr.employee')
    join_date_1 = fields.Date(string='Joining Date of Job')
    resign_date_1 = fields.Date(string='Resign Date of Job')
    employer_name_1 = fields.Char(string='Employer Name')
    salary_1 = fields.Float(string='Salary of Job')
    job_position_1 = fields.Char(string='Job Position')
    reason_for_resign_1 = fields.Char(string='Reason for Resign')
