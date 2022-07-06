from odoo.addons.portal.controllers import portal

from odoo import fields, http, _
from odoo.http import request
from datetime import datetime



class TimeoffPortal(portal.CustomerPortal):

    # Time off count------------------
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        current_user = request.session.uid
        employee_id = request.env['hr.employee'].with_user(2).search([('related_user', '=', current_user)])
        if not employee_id:
            employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', current_user)])
        if 'timeoff_count' in counters:
            values['timeoff_count'] = request.env['hr.leave'].with_user(2).search_count([
                ('employee_id', '=', employee_id.id)
            ])
        return values


class Timeoff(http.Controller):

    # List view of the timeoffs
    @http.route(['/my/timeoffs'], type='http', auth="user", website=True)
    def my_timeoffs(self):
        current_user = request.session.uid
        employee_id = request.env['hr.employee'].with_user(2).search([('related_user','=',current_user)])
        if not employee_id:
            employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', current_user)])
        timeoff_obj = request.env['hr.leave'].with_user(2).search([('employee_id', '=', employee_id.id)])
        values = {}
        values.update({
            'time_offs': timeoff_obj,
        })
        return http.request.render('timeoff_custom.portal_my_timeoffs', values)

    # Timeoffs creation form - Data
    @http.route(['/timeoffs'], type='http', auth="user", website=True)
    def timeoff(self):
        holiday_status = request.env['hr.leave.type'].sudo().search([])
        current_user = request.session.uid

        employee = request.env['hr.employee'].sudo().search([('related_user', '=', current_user)])
        if not employee:
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', current_user)])
        user_id = request.env['res.users'].sudo().search([('id', '=', current_user)])
        values = {}
        values.update({
            'holiday_status_id': holiday_status,
            'user_id': user_id,
            'employee_id': employee,
        })
        return http.request.render('timeoff_custom.timeoff_creation_form', values)

    # Timeoff has been created on submit button
    @http.route('/timeoff/created', type="http", auth="user", website=True)
    def timeoff_creation(self, **kw):
        # print("Data Received.....", kw)
        if kw.get('holiday_status_id'):
            holiday_status_id = request.env['hr.leave.type'].sudo().search([('id', '=', kw['holiday_status_id'])])
            # if holiday_status_id.requires_allocation == 'yes' and not holiday_status_id.has_valid_allocation:
            #     return http.request.render('timeoff_custom.timeoff_invalid', {
            #         'error_message': f"You have not been allocated any leaves of {holiday_status_id.name} type."})
            kw['holiday_status_id'] = holiday_status_id.id
        else:
            kw['holiday_status_id'] = False

        user = request.env['res.users'].sudo().search([('id', '=', 2)])
        kw['user_id'] = user.id

        if kw.get('employee_id'):
            employee_id = request.env['hr.employee'].with_user(2).search([('id', '=', kw['employee_id'])])
            kw['employee_id'] = employee_id.id
        else:
            kw['employee_id'] = False

        kw_add = {"request_date_from": kw.get('date_from'),
                  "request_date_to": kw.get('date_to'),
                  }

        kw.update(kw_add)

        # date_format = "%Y-%m-%d"
        # a = datetime.strptime(kw_add.get('request_date_from'), date_format)
        # b = datetime.strptime(kw_add.get('request_date_to'), date_format)
        # delta = b - a
        #
        #
        #
        # print(kw_add, type(kw_add['request_date_to']), delta, delta.days)
        #
        # found_allocations = request.env['hr.leave.allocation'].search([
        #     ('holiday_status_id', '=', kw.get('holiday_status_id')),
        #     ('employee_id', '=', kw.get('employee_id')),
        #     ('state', '=', 'validate')
        # ])
        # if not found_allocations:
        #     return http.request.render('timeoff_custom.timeoff_invalid', {
        #         'error_message': f"You have not been allocated any leaves of {holiday_status_id.name} type.",
        #     })
        # else:
        #     valid_allocations = found_allocations.filtered(lambda allocation:
        #                                                    allocation.date_from <= kw['request_date_from'] and
        #                                                    allocation.date_to >= kw['request_date_to'])
        #     start_date = min(valid_allocations.mapped('date_from'))
        #     end_date = min(valid_allocations.mapped('date_to'))
        #     total_leaves = sum(valid_allocations.mapped('number_of_days_display'))
        #     if not valid_allocations:
        #         return http.request.render('timeoff_custom.timeoff_invalid', {
        #             'error_message': f"You do not have any leaves allocated between {kw['request_date_from']} and "
        #                              f"{kw['request_date_to']}",
        #         })
        # leaves = request.env['hr.leave'].search([
        #     ('employee_id', '=', kw.get('employee_id')),
        #     ('state', '=', 'validate'),
        #     ('date_from', '>=', start_date),
        #     ('date_to', '<=', end_date),
        # ])
        # leaves_left = total_leaves - sum(leaves.mapped('number_of_days'))
        # if leaves_left < delta.days + 1:
        #     return http.request.render('timeoff_custom.timeoff_invalid', {
        #             'error_message': f"You have only {leaves_left} leaves left. Requested {delta.days + 1} days."
        #         })

        leave = request.env['hr.leave'].with_user(user.id).create(kw)
        leave.number_of_days += 1
        # print(leave)

        return http.request.render('timeoff_custom.timeoff_created')
