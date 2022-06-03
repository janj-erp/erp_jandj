from odoo.addons.portal.controllers import portal

from odoo import fields, http, _
from odoo.http import request


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
            kw['holiday_status_id'] = holiday_status_id.id
        else:
            kw['holiday_status_id'] = False

        # if kw['user_id']:
        #     user_id = request.env['res.users'].sudo().search([('id', '=', kw['user_id'])])
        #     kw['user_id'] = user_id.id
        # else:
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
        leave = request.env['hr.leave'].with_user(user.id).create(kw)
        leave._compute_number_of_days()
        return http.request.render('timeoff_custom.timeoff_created')
