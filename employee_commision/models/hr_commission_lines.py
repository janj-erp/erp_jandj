from odoo import models, fields, api

MONTH_SELECTION = [
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
]


class CommissionLines(models.Model):
    _name = 'commission.lines'

    date = fields.Date('Evaluation Date')
    payment_date = fields.Date('Payment Date')
    state = fields.Selection(selection=[('pending', 'Pending'), ('paid', 'Paid'), ('cancel', 'Cancelled')],
                             string='Status')
    amount = fields.Float('Amount')
    month = fields.Selection(MONTH_SELECTION, string='Month')
    total_sales_amount = fields.Float('Total Sale Amount')
    commission = fields.Float('Commission(%)')
    employee_commission_id = fields.Many2one('hr.employee.commission', string='Employee Commission')
