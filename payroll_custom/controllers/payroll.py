from odoo.addons.portal.controllers import portal

from odoo import fields, http, _
from odoo.http import request, content_disposition
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from collections import OrderedDict


class PayslipPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        current_user = request.session.uid
        employee_id = request.env['hr.employee'].with_user(2).search([('related_user', '=', current_user)])
        if not employee_id:
            employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', current_user)])
        if 'payslip_count' in counters:
            values['payslip_count'] = request.env['hr.payslip'].with_user(2).search_count([
                ('employee_id', '=', employee_id.id)
            ])
        return values

class Payslips(http.Controller):
    @http.route(['/my/payslips', '/my/payslips/page/<int:page>'], type='http', auth="user", website=True)
    def my_payslips(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        current_user = request.session.uid
        employee_id = request.env['hr.employee'].with_user(2).search([('related_user', '=', current_user)])
        if not employee_id:
            employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', current_user)])

        # values = self._prepare_portal_layout_values()
        values = {}
        domain = [('employee_id', '=', employee_id.id), ('state', 'in', ['done', 'paid'])]
        payslip = request.env['hr.payslip']

        # domain = self._get_invoices_domain()
        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'date_from desc'},
        }
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        # default filter by value
        # if not filterby:
        #     filterby = 'all'
        # domain += searchbar_filters[filterby]['domain']

        # count for pager
        payslip_count = payslip.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/payslips",
            total=payslip_count,
            page=page,
            step=80
        )
        # content according to pager and archive selected
        slips = payslip.sudo().search(domain)
        request.session['my_payslip_history'] = slips.ids

        values.update({
            'date': date_begin,
            'slips': slips,
            'page_name': 'Payslips',
            'pager': pager,
            'default_url': '/my/payslips',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return http.request.render('payroll_custom.portal_my_payslips', values)

    @http.route(['/download_slip'], type='http', auth="user", website=True, csrf=False)
    def download_payslips(self, **kw):
        # current_user = request.session.uid
        # employee_id = request.env['hr.employee'].with_user(2).search([('related_user', '=', current_user)])
        # print("@#@#@@#@", kw)
        if kw.get('slip_id'):
            payslip = request.env['hr.payslip'].sudo().search([('id', '=', int(kw.get('slip_id')))])
            ps = payslip.action_print_payslip()

            pdf, _ = request.env.ref('hr_payroll.action_report_payslip').with_user(2)._render_qweb_pdf([payslip.id])
            pdf_http_headers = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
                                ('Content-Disposition', content_disposition('%s - payslip.pdf' % (payslip.name)))]
            return request.make_response(pdf, headers=pdf_http_headers)
            # return ps.get('url')
