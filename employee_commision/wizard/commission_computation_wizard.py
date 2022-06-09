from odoo import models, fields, api
import datetime as dt

class CommissionComputaionWizard(models.TransientModel):
    _name = 'commission.computation.wizard'

    config_ids = fields.Many2many('commission.conf', string='Configuration Id')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    # Filter to see on which level the calculation will happen for the employee selected
    def filter_employee_commission_level(self, employee):
        level = ''
        if employee.employee_type in ['warehouse_clerk', 'warehouse_manager']:
            level = 'company'
        elif employee.employee_type in ['sales_clerk']:
            level = 'personal_sale'
        else:
            level = 'store'
        return level

    # calculation of commission for employee who has commission in the sales done
    def compute_commission_order_wise(self, employee):
        commission_mod = self.env['hr.employee.commission']
        orders = self.env['pos.order.line'].search(
            [('order_id.salesperson_id', '=', employee.employee_id.id),
             ('order_id.date_order', '>=', self.date_from),
             ('order_id.date_order', '<=', self.date_to),
             ('product_id.include_in_commission', '=', True)])
        total = sum(orders.mapped('price_subtotal'))
        commission_amount = total * employee.commission_percentage * 0.01
        commission_report = commission_mod.search(
            [('employee_id', '=', employee.employee_id.id), ('conf_id', '=', employee.id)])
        if not commission_report:
            commission_report = commission_mod.create({
                'employee_id': employee.employee_id.id,
                'conf_id': employee.id,
                'line_ids': [(0, 0, {
                    'date': fields.Date.today(),
                    'state': 'pending',
                    'amount': commission_amount,
                    'total_sales_amount': total,
                    'month': str(dt.datetime.today().month),
                    'commission': employee.commission_percentage
                })],
            })
        else:
            commission_report.write({
                'line_ids': [(0, 0, {
                    'date': fields.Date.today(),
                    'state': 'pending',
                    'amount': commission_amount,
                    'total_sales_amount': total,
                    'month': str(dt.datetime.today().month),
                    'commission': employee.commission_percentage
                })]
            })
        # return commission_report

    # calculation of commission for employee who has commission on companies total sale for the period
    def compute_commission_company_wise(self, employee):
        commission_mod = self.env['hr.employee.commission']
        orders = self.env['pos.order.line'].search(
            [('order_id.company_id', '=', employee.employee_id.company_id.id),
             ('order_id.date_order', '>=', self.date_from),
             ('order_id.date_order', '<=', self.date_to),
             ('product_id.include_in_commission', '=', True)])
        leaves = self.env['hr.leave'].search(
            [('employee_id', '=', employee.employee_id.id), ('request_date_from', '>=', self.date_from),
             ('request_date_from', '<=', self.date_to), ('state', '=', 'validate')])
        orders_leave = False
        for leave in leaves:
            orders_leave = orders.filtered(lambda x: leave.request_date_from <= x.order_id.date_order.date() <= leave.request_date_to)
        if orders_leave:
            orders -= orders_leave
        total = sum(orders.mapped('price_subtotal'))
        commission_amount = total * employee.commission_percentage * 0.01
        commission_report = commission_mod.search(
            [('employee_id', '=', employee.employee_id.id), ('conf_id', '=', employee.id)])
        if not commission_report:
            commission_report = commission_mod.create({
                'employee_id': employee.employee_id.id,
                'conf_id': employee.id,
                'line_ids': [(0, 0, {
                    'date': fields.Date.today(),
                    'state': 'pending',
                    'amount': commission_amount,
                    'total_sales_amount': total,
                    'month': str(dt.datetime.today().month),
                    'commission': employee.commission_percentage
                })],
            })
        else:
            commission_report.write({
                'line_ids': [(0, 0, {
                    'date': fields.Date.today(),
                    'state': 'pending',
                    'amount': commission_amount,
                    'total_sales_amount': total,
                    'month': str(dt.datetime.today().month),
                    'commission': employee.commission_percentage
                })]
            })

    # calculation of commission for employee who has commission on stores total sale for the period
    def compute_commission_store_wise(self, employee):
        commission_mod = self.env['hr.employee.commission']
        orders = self.env['pos.order.line'].search(
            [('order_id.session_id.config_id', 'in', employee.store.ids),
             ('order_id.date_order', '>=', self.date_from),
             ('order_id.date_order', '<=', self.date_to),
             ('product_id.include_in_commission', '=', True)])
        leaves = self.env['hr.leave'].search([('employee_id', '=', employee.employee_id.id),
                                              ('request_date_from', '>=', self.date_from),
                                              ('request_date_from', '<=', self.date_to), ('state', '=', 'validate')])
        orders_leave = False
        for leave in leaves:
            orders_leave = orders.filtered(lambda x: leave.request_date_from <= x.order_id.date_order.date() <= leave.request_date_to)
        if orders_leave:
            orders -= orders_leave
        total = sum(orders.mapped('price_subtotal'))
        commission_amount = total * employee.commission_percentage * 0.01
        commission_report = commission_mod.search(
            [('employee_id', '=', employee.employee_id.id), ('conf_id', '=', employee.id)])
        if not commission_report:
            commission_report = commission_mod.create({
                'employee_id': employee.employee_id.id,
                'conf_id': employee.id,
                'line_ids': [(0, 0, {
                    'date': fields.Date.today(),
                    'state': 'pending',
                    'amount': commission_amount,
                    'total_sales_amount': total,
                    'month': str(dt.datetime.today().month),
                    'commission': employee.commission_percentage
                })],
            })
        else:
            commission_report.write({
                'line_ids': [(0, 0, {
                    'date': fields.Date.today(),
                    'state': 'pending',
                    'amount': commission_amount,
                    'total_sales_amount': total,
                    'month': str(dt.datetime.today().month),
                    'commission': employee.commission_percentage
                })]
            })

    def calculate_commission_for_employee(self):
        for employee in self.config_ids:
            commission_level = self.filter_employee_commission_level(employee)
            if commission_level and commission_level == 'personal_sale':
                self.compute_commission_order_wise(employee)
            if commission_level and commission_level == 'company':
                self.compute_commission_company_wise(employee)
            if commission_level and commission_level == 'store':
                self.compute_commission_store_wise(employee)
