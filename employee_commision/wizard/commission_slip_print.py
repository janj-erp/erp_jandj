from odoo import models, fields, api


class CommissionComputaionWizard(models.TransientModel):
    _name = 'commission.slip.print'

    config_ids = fields.Many2many('commission.conf', string='Configuration Id')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    update_payment_status = fields.Selection(selection=[('pending','Pending'),('paid', 'Paid'), ('cancel', 'Cancelled')],
                                             string='Update Payment Status', default='paid')

    def print_commission_report(self):
        commission_ids = self.env['hr.employee.commission'].search([('conf_id', 'in', self.config_ids.ids)])
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'commission_ids': commission_ids.ids,
            'wizard_id': self.id
        }
        return self.env.ref('employee_commision.action_report_commission_payslip').report_action(self.id, data=data)

    def update_commission_lines(self):
        lines = self.env['commission.lines'].search(
            [('employee_commission_id.conf_id', 'in', self.config_ids.ids), ('date', '>=', self.date_from),
             ('date', '<=', self.date_to)])
        for line in lines:
            line.write({'state': self.update_payment_status})


class CommissionPayslipReport(models.AbstractModel):
    _name = 'report.employee_commision.commission_payslip_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'commission_ids': self.env['hr.employee.commission'].browse(data['commission_ids']),
            'date_from': data['date_from'],
            'date_to': data['date_to'],
            'wizard_id': data['wizard_id'],
            'company': self.env.company
        }
