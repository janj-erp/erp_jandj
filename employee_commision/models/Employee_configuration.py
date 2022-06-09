# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class EmployeeConfiguration(models.Model):
    _name = 'commission.conf'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee ID')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse ID')
    store = fields.Many2many('pos.config', string='Store')
    commission_percentage = fields.Float('Commission %')
    manager_id = fields.Many2one('hr.employee', string='Manager')
    pos_order_count = fields.Integer(compute='compute_pos_count')
    employee_type = fields.Selection([('stores_manager', 'Stores Manager'),
                                      ('warehouse_manager', 'Warehouse Manager'),
                                      ('sales_clerk', 'Sales Clerk'),
                                      ('store_room_clerk', 'Store Room Clerk'),
                                      ('baggage_collector', 'Baggage Collector'),
                                      ('warehouse_clerk', 'Warehouse Clerk'),
                                      ], string='Employee Type')

    _sql_constraints = [('commission_employee_id_uniq', 'unique (employee_id)', 'Cannot create multiple configurations for an employee.')]

    def action_pos_orders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Point of Sale Order',
            'view_mode': 'tree,form',
            'res_model': 'pos.order',
            'domain': [('salesperson_id', '=', self.employee_id.id)],
        }

    def compute_pos_count(self):
        for rec in self:
            pos_order_count = self.env['pos.order'].search_count([('salesperson_id', '=', self.employee_id.id)])
            rec.pos_order_count = pos_order_count

