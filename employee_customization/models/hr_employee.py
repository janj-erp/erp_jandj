from odoo import api, fields, models, _
from datetime import date, datetime
from odoo.exceptions import UserError
from werkzeug.urls import url_encode


class ReportActivity(models.Model):
    _inherit = 'hr.employee'

    read_id = fields.Boolean("Title True", compute="compute_job_title")

    def compute_job_title(self):
        self.read_id = self.env.user.has_group('base.group_system')
