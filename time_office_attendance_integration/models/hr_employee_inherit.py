from odoo import models, fields
import requests
from datetime import datetime
from logging import getLogger
import json
import pytz
import datetime as dt

_logger = getLogger(__name__)


class Employee(models.Model):
    _inherit = 'hr.employee'

    device_emp_code = fields.Char('Biometric Device Employee Code')

    def get_search_date_filter_date(self, start_date, end_date):
        # Creates a search start and end dates if not defined by the user.
        user_tz = pytz.timezone(self.env.user.tz or 'UTC')

        def convert_to_utc(time, _date):
            date_obj = datetime.combine(_date, time)
            date_utc = user_tz.localize(date_obj).astimezone(pytz.utc).replace(tzinfo=None)
            return date_utc

        search_start = convert_to_utc(dt.time(hour=0, minute=int(0)), start_date)
        search_end = convert_to_utc(dt.time(hour=23, minute=int(55)), end_date)
        return search_start, search_end

    def fetch_employee_attendance(self, start_date=None, end_date=None):
        # Gets the employee Attendance from cloud and updates it on the Attendance Module
        user_tz = pytz.timezone(self.env.user.tz or 'UTC')

        def convert_date_string_to_date(time_str=None, date_str=None):
            user_tz = pytz.timezone(self.env.user.tz or 'UTC')
            date = datetime.strptime(date_str + ' ' + time_str, '%d-%m-%Y %H:%M')
            return user_tz.localize(date).astimezone(pytz.utc).replace(tzinfo=None)

        attendance_mod = self.env['hr.attendance']
        start_date = start_date if start_date else datetime.today().date()
        end_date = end_date if end_date else datetime.today().date()
        records = self.get_employee_attendance(employee_id=self, start_date=start_date, end_date=end_date)
        search_start, search_end = self.get_search_date_filter_date(start_date, end_date)
        for rec in records['InOutPunchData']:
            employee_att = attendance_mod.search(
                [('employee_id.device_emp_code', '=', rec['Empcode']), ('check_out', '=', False),('check_in', '<=', search_start)])
            if employee_att:
                employee_att.write({'check_out': convert_date_string_to_date('19:00', datetime.strftime(employee_att.check_in.date(), '%d-%m-%Y'))})
                # employee_att.write({'check_out': employee_att.check_in + dt.timedelta(minutes=1)})

            employee_login = attendance_mod.search(
                [('employee_id.device_emp_code', '=', rec['Empcode']), ('check_out', '=', False),('check_in', '>=', search_start), ('check_in', '<=', search_end)])
            for line in employee_login:
                if line.check_in.date() == datetime.strptime(rec['DateString'], '%d-%m-%Y').date():
                    line.write({
                        'check_out': convert_date_string_to_date(rec['OUTTime'], rec['DateString']) if rec['OUTTime'] != '--:--' else False
                    })
                elif line.check_in.date() < datetime.strptime(rec['DateString'], '%d-%m-%Y').date():
                    employee_login.write({'check_out': convert_date_string_to_date('19:00', datetime.strftime(employee_login.check_in.date(), '%d-%m-%Y'))})
                    # employee_login.write({'check_out': employee_login.check_in + dt.timedelta(minutes=1)})

            if rec['INTime'] != '--:--':
                employee_id = self.env['hr.employee'].search([('device_emp_code', '=', rec['Empcode'])])

                if employee_id and not attendance_mod.search([('employee_id.device_emp_code', '=', rec['Empcode'])]).filtered(lambda x: x.check_in.date() == convert_date_string_to_date(rec['INTime'], rec['DateString']).date()):
                    attendance_mod.create({
                        'employee_id': employee_id.id,
                        'check_in': convert_date_string_to_date(rec['INTime'], rec['DateString']),
                        'check_out': convert_date_string_to_date(rec['OUTTime'], rec['DateString']) if rec[
                                                                                                           'OUTTime'] != '--:--' else False,
                    })

    def get_employee_attendance(self, employee_id=None, start_date=None, end_date=None):
        # url = "http://api.etimeoffice.com/api/DownloadInOutPunchData?Empcode={emp}&FromDate={start}&ToDate={end}"
        # Connects to the cloud server and fetches the attendance data based on the date filter
        company_id = self.env.company if self.env.company else self.env.user.company_id
        url = company_id.url
        auth = company_id.corporate_id + ':' + company_id.username + ':' + company_id.password + ':' + 'true'
        if employee_id:
            emp = employee_id.device_emp_code
        else:
            emp = "ALL"

        try:
            # request the data from the Time Office portal using API Call.
            # Auth: it is combination of Corporate id:Username:Password:true.
            r = requests.request('GET', url.format(emp=emp, start=start_date.strftime('%d/%m/%Y'),
                                                   end=end_date.strftime('%d/%m/%Y')),
                                 auth=(auth, ''))
        except Exception as e:
            # Any Error During the calling of API will be Shown in the Logs.
            _logger.error(e)
            raise

        # The Response Will be stored in 'r' and it is converted to utf-8
        result = r.content.decode('utf-8')
        json_obj = json.loads(result)
        return json_obj

class EmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    device_emp_code = fields.Char('Biometric Device Employee Code')