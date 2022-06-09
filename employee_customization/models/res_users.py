from odoo import api, fields, models, _
from datetime import date, datetime
from odoo.exceptions import UserError
from werkzeug.urls import url_encode


class ReportActivity(models.Model):
    _inherit = 'res.users'

    hr_work_location_id = fields.Many2one('hr.work.location', string="Work Location")
