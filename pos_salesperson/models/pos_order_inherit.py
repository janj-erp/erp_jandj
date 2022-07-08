from odoo import models,fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    salesperson_id = fields.Many2one('hr.employee', string='Salesperson')
    active = fields.Boolean('Active', default=True, groups='base.group_system')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res['salesperson_id'] = ui_order['salesperson']
        return res