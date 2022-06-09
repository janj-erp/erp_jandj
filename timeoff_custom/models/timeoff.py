from odoo import models, fields, api, _


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def get_state(self, val):
        if val:
            if val == "draft":
                return "To Submit"
            elif val == "confirm":
                return "To Approve"
            elif val == "refuse":
                return "Refused"
            elif val == "validate1":
                return "Second Approval"
            elif val == "validate":
                return "Approved"
        return False

#     @api.model
#     def write(self, vals):
#         rec = super(HrLeave, self).write(vals)
#         # create Sale Order template and update on the vals
#         print(vals, "VVVVVVVVVVVVVVVVVVvvvv")
#         return rec
