from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Applicant(models.Model):
    _inherit = 'hr.applicant'

    probationary_period = fields.Integer("Probationary Period")
    probationary_period_salary = fields.Float("Probationary Period Salary")
    probationary_period_basis = fields.Char("Based On")
    permanent_salary = fields.Float("Permanent Salary")
    permanent_basis = fields.Char("Based On")
    allowance = fields.Float("Allowance")

    def generate_appointment_letter(self):
        template = self.env.ref('appointment_letter.report_appointment_letter_menu',
                                raise_if_not_found=False)
        if not template:
            raise ValueError(_("The mail template is missing..!!!"))
        if not self.probationary_period_salary or not self.probationary_period_basis or not self.permanent_salary or not self.permanent_basis or not self.allowance or not self.probationary_period:
            raise UserError(_("Some salary structure information is missing..!!!"
                              "Please add those to continue"))
        print("&&&**&*&&&*&**&&&&", template, self)
        return self.env.ref('appointment_letter.report_appointment_letter_menu').report_action(self)