from odoo import models, fields, api


class AttendanceSyncWizard(models.Model):
    _name = 'attendance.sync.wizard'

    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')

    def synchronise_attendance_records(self):
        # self.env['hr.employee'].fetch_employee_attendance(start_date=self.date_start, end_date=self.date_end)
        return self.env['hr.employee'].fetch_employee_attendance(start_date=self.date_start, end_date=self.date_end)

