from odoo import models, fields, api, _


class ResUsersInherit(models.Model):
    _inherit = 'hr.employee'

    is_created = fields.Boolean(compute="get_user_id")
    related_user = fields.Many2one('res.users', string='Related User')

    def create_user(self):
        self.related_user = self.env['res.users'].create({'name': self.name,
                                                'login': self.work_email,
                                                'password': '1234',
                                                'sel_groups_1_9_10': 9,
                                                }).id
        self.is_created = True

    def get_user_id(self):
        if self.related_user:
            self.is_created = True
        else:
            self.is_created = False