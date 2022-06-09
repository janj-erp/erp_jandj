# -*- coding: utf-8 -*-
from odoo import models, fields


class AddLayOff(models.TransientModel):
    _name = "add.layoff"
    _description = "adding new layoff "

    layoff_start_date = fields.Date(string="Lay Off Start Date")
    layoff_end_date = fields.Date(string="Lay Off End Date")
    layoff_reason = fields.Char(string="Reason for Layoff")


    def set_open(self):
        vals = {
            'layoff_start_date': self.layoff_start_date,
            'layoff_end_date': self.layoff_end_date,
            'layoff_reason': self.layoff_reason,
        }
        rec = self.env.context.get('active_id')
        recr = self.env['hr.employee'].browse(rec)
        recr.write(vals)


