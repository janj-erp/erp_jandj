from odoo import models, fields, api


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HrPayslip, self).create(vals_list)
        for record in res:
            commission_conf = self.env['commission.conf'].search([('employee_id', '=', record.employee_id.id)],limit=1)
            if commission_conf:
                self.env['commission.computation.wizard'].create({
                    'config_ids': [(6, 0, commission_conf.ids)],
                    'date_from': record.date_from,
                    'date_to': record.date_to
                }).calculate_commission_for_employee()
        return res

