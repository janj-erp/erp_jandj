from odoo import api,fields,models,_
from datetime import date, datetime ,timedelta
from num2words import num2words

class Employee(models.Model):
    _inherit = "hr.employee"

    salary = fields.Float("Salary")
    structure = fields.Many2one('hr.payroll.structure')
    trn_number = fields.Char('TRN Number')
    nis_number = fields.Char('NIS Number')


class Payslip(models.Model):
    _inherit = "hr.payslip"

    #other deductions & allowances
    allowances = fields.Float(" Food Allowances")
    paye_deduction = fields.Float("Paye Deduction")
    travel_allowance =  fields.Float("Travel")
    loan_repayment = fields.Float("Loan Repayments")

    working_week = fields.Float(string="Total Working Hours In Week",
                                compute="calculate_employee_working_hours_in_current_week")
    # amount_calc = fields.Float(compute="calculcate_amount")
    total_hours = fields.Float('Total Hours (per week)')
    spl_ot_amount = fields.Float("Holiday OT amount")
    holiday_ot = fields.Float('Holiday OT')
    public_leave_days = fields.Float('Public Holidays')
    ot_amount = fields.Float("Normal OT amount")

    # food_alw = fields.Float("Food Allowance")
    entertainment = fields.Float("Entertainment")
    accommodation = fields.Float("Accommodation")

    # working & leave days
    total_days = fields.Float("Total Days", compute="get_total_number_of_days")
    leave_type = fields.Many2one('hr.leave.type')
    unpaid_days = fields.Float('Loss Of Pay (Days)',compute="get_total_unpaid_of_days")
    total_sundays = fields.Integer('Total Sundays')

    # year_to_date
    ytd_basic = fields.Float("YTD Basic")
    ytd_nis = fields.Float("YTD NIS")
    ytd_nht = fields.Float("YTD NHT")
    ytd_edt = fields.Float("YTD EDT")
    ytd_paye = fields.Float("YTD PAYE")

    start_date = fields.Date(string='Start Date',default=None)
    end_date = fields.Date(string='End Date',default=None)

    vacation_type = fields.Selection([('week','Week'),
                                      ('day','Day')])
    vacation_period = fields.Float('No.of Days/Week')
    bonus = fields.Float('Bonus')
    maternity_leave_type = fields.Selection([('week','Week'),
                                      ('month','Month')])
    maternity_period = fields.Float('No.of Days/Week')



    @api.depends('date_from')
    @api.onchange('date_from')
    def get_start_date(self):
        for payslip in self:
            date_from = payslip.date_from
            payslip.write({'start_date':date_from,
                        })

    @api.depends('date_to')
    @api.onchange('date_to')
    def get_end_date(self):
        for payslip in self:
            date_to = payslip.date_to
            payslip.write({'end_date': date_to})


    # For computation of the employee's total working hours of current week:-
    @api.depends('date_from', 'date_to')
    @api.onchange('date_from', 'date_to')
    def calculate_employee_working_hours_in_current_week(self):
        for payslip in self:
            date_from = payslip.date_from
            date_to = payslip.date_to
            emp_id = payslip.employee_id
            ytd_basic = 0
            ytd_nis = 0
            ytd_nht = 0
            ytd_edt = 0
            ytd_paye = 0
            payslip.working_week = 0
            if emp_id:
                attendance_hrs = self.env['hr.attendance']
                recs = attendance_hrs.search([('employee_id', '=', emp_id.id)])

                for rec in recs :
                    check_in  = rec.check_in.date()
                    check_out = rec.check_out.date()
                    if check_in >= date_from and check_out <= date_to:
                        attendance_hrs |= rec

                holiday_obj = self.env['resource.calendar.leaves']
                public_holidays = holiday_obj.search([])
                for val in public_holidays:
                    if val.work_entry_type_id.code == 'PUBLIC':
                        start_date = val.date_from.date()
                        end_date = val.date_to.date()
                        if start_date >= date_from and end_date <= date_to:
                            holiday_obj |= val
                hours = 0
                ot_hours = 0
                normal_ot = 0
                ot_amt = 0
                payslip.public_leave_days = len(holiday_obj.ids)
                if holiday_obj:
                    for hrs in attendance_hrs:
                        for hol in holiday_obj:
                            date_from = hol.date_from.date()
                            date_to = hol.date_to.date()
                            check_in = hrs.check_in.date()
                            check_out = hrs.check_out.date()
                            if date_from == check_in and date_to == check_out:
                                ot_hours += hrs.worked_hours
                                payslip.holiday_ot = ot_hours

                for hrs in attendance_hrs :
                    hours += hrs.worked_hours
                payslip.working_week = hours
                payslip.total_hours = hours
            recs = payslip.search([('state', '=', 'paid'), ('employee_id', '=', emp_id.id)])
            if recs :
                for rec in recs :
                    ytd_basic += rec.ytd_basic
                    ytd_nis += rec.ytd_nis
                    ytd_nht += rec.ytd_nht
                    ytd_edt += rec.ytd_edt
                    ytd_paye += rec.ytd_paye
            payslip.ytd_basic = ytd_basic
            payslip.ytd_nis = ytd_nis
            payslip.ytd_nht = ytd_nht
            payslip.ytd_edt = ytd_edt
            payslip.ytd_paye = ytd_paye


    @api.depends('date_from', 'date_to')
    def get_total_number_of_days(self):
        for payslip in self:
            date_from = str(payslip.date_from)
            date_to = str(payslip.date_to)
            start_date = datetime.strptime(date_from, "%Y-%m-%d")
            end_date = datetime.strptime(date_to, "%Y-%m-%d")
            days = (end_date - start_date).days + 1
            from_date = payslip.date_from
            to_date = payslip.date_to
            days_count = (from_date - to_date)
            payslip.total_days = days
            sun = 0
            dates_btwn = start_date
            while dates_btwn <= end_date:
                dates_btwn = dates_btwn + timedelta(days=1)
                if (dates_btwn.strftime("%A") == 'Sunday'):
                    sun += 1
                else:
                    sun += 0
            payslip.total_sundays = sun
            date_from = payslip.date_from
            date_to = payslip.date_to
            holiday_obj = self.env['resource.calendar.leaves']
            public_holidays = holiday_obj.search([])
            for val in public_holidays:
                if val.work_entry_type_id.code == 'PUBLIC':
                    from_date = val.date_from.date()
                    to_date = val.date_to.date()
                    if from_date >= date_from and to_date <= date_to:
                        holiday_obj |= val
            payslip.public_leave_days = len(holiday_obj.ids)

    @api.depends('leave_type')
    def get_total_unpaid_of_days(self):
        for payslip in self:
            date_from = payslip.date_from
            date_to = payslip.date_to
            days = 0
            ytd_basic = 0
            ytd_nis = 0
            ytd_nht = 0
            ytd_edt = 0
            ytd_paye = 0
            emp_id = payslip.employee_id
            recs = payslip.search([('state', '=', 'paid'), ('employee_id', '=', emp_id.id)])
            if recs:
                for rec in recs:
                    ytd_basic += rec.ytd_basic
                    ytd_nis += rec.ytd_nis
                    ytd_nht += rec.ytd_nht
                    ytd_edt += rec.ytd_edt
                    ytd_paye += rec.ytd_paye
            payslip.ytd_basic = ytd_basic
            payslip.ytd_nis = ytd_nis
            payslip.ytd_nht = ytd_nht
            payslip.ytd_edt = ytd_edt
            payslip.ytd_paye = ytd_paye
            if payslip.leave_type:
                type_id = payslip.leave_type.id
                recs = self.env['hr.leave'].search([('employee_id', '=', emp_id.id), ('state', '=', 'validate'),
                                                    ('holiday_status_id', '=', type_id),
                                                    ('request_date_from', '>=', date_from),
                                                    ('request_date_to', '<=', date_to)])
                for rec in recs:
                    days += rec.number_of_days
                payslip.unpaid_days = days
            else:
                payslip.unpaid_days = 0


    @api.onchange('employee_id')
    def get_pay_structure(self):
        emp_id = self.employee_id
        if emp_id.structure:
            self.write({'struct_id': emp_id.structure.id})

    def net_amount_to_text(self):
        for val in self.line_ids:
            if val.code == "NET":
                net_amount = round(val.total)
                words = num2words(net_amount).title() + ' only'
        return words

    def get_branch_name(self):
        datas = self.env['pos.config'].search([('salesperson_ids','in',self.employee_id.id)])
        for data in datas:
            branch_name = data.picking_type_id.warehouse_id.name
        return branch_name
