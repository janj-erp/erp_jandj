from odoo import api,fields,models,_
from datetime import date, datetime,timedelta
from num2words import num2words
from odoo.tools.misc import formatLang
from dateutil.relativedelta import relativedelta
from odoo.tools.misc import format_date



class Employee(models.Model):
    _inherit = "hr.employee"

    total_ctc = fields.Float("Total CTC")
    mbo = fields.Float("MBO (in %)")
    structure = fields.Many2one('hr.payroll.structure')
    relieving_date = fields.Date('Date Of Relieving')

class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    #other deductions & allowances
    food_coupon_ded = fields.Float("Food Coupon (Deduction)")
    income_tax = fields.Float("Income Tax")
    hr_deduction = fields.Float("HR Deductions")
    other_deductions = fields.Float("Other Deductions")
    food_coupon_alw = fields.Float("Food Coupon (Allowance)")
    onsite_allowance = fields.Float("Onsite Allowance")
    shift_allowance = fields.Float("Shift Allowance")
    other_allowance = fields.Float("Other Allowance")

    #working & leave days
    present_days = fields.Float("Present Days")
    leave_days = fields.Float("Leave Days", compute="get_total_leave_days")
    total_days = fields.Float("Total Days", compute="get_total_number_of_days")
    salary_days = fields.Float("Salary Days")
    paid_days = fields.Float("Paid Days")

    #master salry details
    basic_salary = fields.Float("Basic Salary")
    hra = fields.Float("HRA")
    standard_deduction = fields.Float("Standard Deduction")
    lta = fields.Float("LTA")
    special_allowance = fields.Float("Special Allowance")
    variable_allowance = fields.Float("Variable Allowance")
    pf_amount = fields.Float("PF (Employer's Contribution)")

    unpaid_days = fields.Float('Loss Of Pay (Days)')
    weekend_days = fields.Float("Weekend / Holiday Days")
    public_leave_days = fields.Float('Public Holidays')

    #arrears
    arrears_basic = fields.Float('Basic (Arrears)')
    arrears_hra = fields.Float('HRA (Arrears)')
    arrears_lta = fields.Float('LTA (Arrears)')
    arrears_spl_alw = fields.Float('Special Allowance (Arrears)')
    arrears_std_ded = fields.Float('Standard Deduction (Arrears)')

    # @api.depends('employee_id', 'date_from', 'date_to')
    # def _compute_contract_id(self):
    #     super(HrPayslip, self)._compute_contract_id
    #     self.contract_id = self.env['hr.contract'].search([], limit=1).id
    #     return

    def _cron_generate_payslips(self):
        payslip = self.env['hr.payslip']
        employee = self.env['hr.employee'].search([])
        date_from = fields.Date.to_string(date.today().replace(day=1))
        date_to = fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date())
        for emp in employee:
            vals = {'employee_id': emp.id,
                    'struct_id': emp.structure.id,
                    'date_from': date_from,
                    'date_to': date_to,
                    'name': '%(payslip_name)s - %(employee_name)s - %(dates)s' % {
                        'payslip_name': 'Salary Slip',
                        'employee_name': emp.name,
                        'dates': format_date(self.env, date_from, date_format="MMMM y")}
                    }
            new_rec = payslip.create(vals)
            new_rec.compute_sheet()
            new_rec.calculate_salary_details()

    # def compute_sheet(self):
    #     self.calculate_salary_details()
    #     return super(Payslip, self).compute_sheet()

    def compute_sheet(self):
        for rec in self:
            rec.calculate_salary_details()
            rec.get_total_leave_days()
            super(HrPayslip, rec).compute_sheet()
        return

    @api.onchange('employee_id')
    @api.depends('employee_id')
    def calculate_salary_details(self):
        # employee = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        if self.struct_id.name == 'Intership Stipend':
            basic = self.employee_id.total_ctc
            self.write({'basic_salary': round(basic),
                        'hra': 0.00,
                        'standard_deduction': 0.00,
                        'lta': 0.00,
                        'special_allowance': 0.00,
                        'variable_allowance': 0.00,
                        'pf_amount': 0.0
                        })
        else:
            total_ctc = self.employee_id.total_ctc
            mbo = self.employee_id.mbo
            mbo = mbo / 100
            base_salary = round(total_ctc - (total_ctc*mbo))
            lta = 0
            var_alw = 0
            if base_salary <= 400000.00:
                basic = 180000.00
                lta = 0
            elif base_salary > 400000.00 and base_salary <= 700000.00:
                basic = base_salary * 0.5
                lta = 18000
            elif base_salary > 700000 and base_salary <= 1200000:
                basic = base_salary * 0.45
                lta = 24000
            elif base_salary > 1200000:
                basic = base_salary * 0.45
                lta = 42000
            if basic:
                if base_salary <= 300000:
                    hra = 0
                elif base_salary > 300000:
                    hra = basic * 0.4
            if base_salary > 400000.00:
                std_ded = 50000
            else:
                std_ded = 0
            if basic/12 > 15000:
                pf = 1800*12
            else:
                pf = (basic/12 * 0.12)*12
            fca = self.food_coupon_alw
            spl_alw = base_salary - (basic + hra + std_ded + lta + pf + fca)
            var_alw = total_ctc * mbo
            self.write({'basic_salary': round(basic),
                        'hra': round(hra),
                        'standard_deduction': round(std_ded),
                        'lta': round(lta),
                        'special_allowance': round(spl_alw),
                        'variable_allowance': round(var_alw),
                        'pf_amount': round(pf)})

    @api.depends('leave_type')
    def get_total_unpaid_of_days(self):
        date_from = self.date_from
        date_to = self.date_to
        days = 0
        if self.leave_type:
            emp_id = self.employee_id.id
            type_ids = self.leave_type.id
            recs = self.env['hr.leave'].search([('employee_id', '=', emp_id), ('state', '=', 'validate'),
                                                ('holiday_status_id', 'in', type_ids),
                                                ('request_date_from', '>=', date_from),
                                                ('request_date_to', '<=', date_to)])
            for rec in recs:
                days += rec.number_of_days
            self.unpaid_days = days
        else:
            self.unpaid_days = 0

    @api.onchange('employee_id')
    def get_pay_structure(self):
        emp_id = self.employee_id
        if emp_id.structure:
            self.write({'struct_id': emp_id.structure.id})

    def net_amount_to_text(self):
        words = " "
        for val in self.line_ids:
            if val.code == "NET":
                net_amount = round(val.total)
                words = 'Rupees ' + num2words(net_amount, lang='en_IN').title() + ' only'
        return words

    @api.onchange('employee_id')
    @api.depends('date_from', 'date_to')
    def get_total_leave_days(self):
        date_from = self.date_from
        date_to = self.date_to
        days = lop_days = leave_days = sal_days = new_days = 0
        emp = self.employee_id
        start_date = datetime.strptime(str(date_from), "%Y-%m-%d")
        end_date = datetime.strptime(str(date_to), "%Y-%m-%d")
        days = (end_date - start_date).days + 1
        new_days = days
        if emp.first_contract_date:
            if self.date_to > emp.first_contract_date > self.date_from:
                join_date = str(emp.first_contract_date)
                join_date = datetime.strptime(join_date, "%Y-%m-%d")
                start_date = datetime.strptime(str(date_from), "%Y-%m-%d")
                end_date = datetime.strptime(str(date_to), "%Y-%m-%d")
                days = (end_date - start_date).days + 1
                new_days = (end_date - join_date).days + 1
                sal_days = days - new_days
        if emp.relieving_date:
            if self.date_from < emp.relieving_date < self.date_to:
                relieve_date = str(emp.relieving_date)
                relieve_date = datetime.strptime(relieve_date, "%Y-%m-%d")
                start_date = datetime.strptime(str(date_from), "%Y-%m-%d")
                end_date = datetime.strptime(str(date_to), "%Y-%m-%d")
                days = (end_date - start_date).days + 1
                new_days = (relieve_date - start_date).days + 1
                sal_days = days - new_days
        self.with_user(2).write({
            'paid_days': new_days,
            'salary_days': sal_days,
        })
        emp_id = self.employee_id.id
        holiday_obj = self.env['resource.calendar.leaves']
        public_holidays = holiday_obj.search([])
        for val in public_holidays:
            if val.work_entry_type_id.code == 'PUBLIC':
                start_date = val.date_from.date()
                end_date = val.date_to.date()
                if start_date >= date_from and end_date <= date_to:
                    holiday_obj |= val
        self.with_user(2).write({
            'public_leave_days': len(holiday_obj.ids),
        })
        type_ids = self.env['hr.leave.type'].search([]).ids
        recs = self.env['hr.leave'].search([('employee_id', '=', emp_id), ('state', '=', 'validate'),
                                            ('holiday_status_id', 'in', type_ids),
                                            ('request_date_from', '>=', date_from),
                                            ('request_date_to', '<=', date_to)])
        for rec in recs:
            leave_days += rec.number_of_days
        self.with_user(2).write({
            'leave_days': leave_days
            ,
        })
        type_id = self.env['hr.leave.type'].search([('name', '=', 'Unpaid')])
        recs = self.env['hr.leave'].search([('employee_id', '=', emp_id), ('state', '=', 'validate'),
                                            ('holiday_status_id', '=', type_id.id),
                                            ('request_date_from', '>=', date_from),
                                            ('request_date_to', '<=', date_to)])
        for rec in recs:
            lop_days += rec.number_of_days
        self.with_user(2).write({
            'unpaid_days': lop_days,
        })

    @api.depends('date_from', 'date_to')
    def get_total_number_of_days(self):
        date_from = str(self.date_from)
        date_to = str(self.date_to)
        start_date = datetime.strptime(date_from, "%Y-%m-%d")
        end_date = datetime.strptime(date_to, "%Y-%m-%d")
        days = (end_date - start_date).days + 1
        self.with_user(2).write({
            'total_days': days,
        })
        sun = 0
        sat = 0
        dates_btwn = start_date
        while dates_btwn <= end_date:
            if (dates_btwn.strftime("%A") == 'Sunday'):
                sun += 1
            else:
                sun += 0
            if (dates_btwn.strftime("%A") == 'Saturday'):
                sat += 1
            else:
                sat += 0
            dates_btwn = dates_btwn + timedelta(days=1)
        self.with_user(2).write({
            'weekend_days': sun + sat,
            'present_days': self.total_days - (self.weekend_days + self.leave_days + self.public_leave_days),
        })

    def order_formatLang(self, value, currency_obj=False):
        res = value
        if currency_obj and value:
            res = formatLang(self.env, value, currency_obj=False)
        return res


    def send_payslips_by_mail(self):
        template_id = self.env.ref('exzatech_payroll.payslip_mail', raise_if_not_found=False).id
        for rec in self:
            self.env['mail.template'].browse(template_id).send_mail(rec.id, force_send=True, email_values={
                'email_from': rec.env.user.company_id.email,
                'email_to': rec.employee_id.work_email,
            })

class HrpayslipLines(models.Model):
    _inherit = "hr.payslip.line"

    contract_id = fields.Many2one('hr.contract', string='Contract', index=True , required=False)