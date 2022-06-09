from odoo import models, fields
from odoo.exceptions import ValidationError


class PickingPackLine(models.Model):
    _name = 'picking.pack.line'
    _description = 'Packages lines in stock pickings'

    name = fields.Many2one('product.pack', 'Package Name')
    pack_image = fields.Image('Pack Image', related='name.image_variant_1920')
    quantity = fields.Integer('Quantity')
    picking_id = fields.Many2one('stock.picking', 'Picking ID')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    pack_ids = fields.One2many('picking.pack.line', 'picking_id', 'Select Packages')

    def update_moves(self):
        # print('update_moves')
        # products = list()
        for pack in self.pack_ids:
            if not pack.name:
                raise ValidationError('Please remove the empty pack lines before updating products')
        for move in self.move_ids_without_package:
            if move.from_package:
                move.unlink()
        for pack in self.pack_ids:
            for line in pack.name.pack_lines:
                product = line.name
                qty = line.quantity * pack.quantity
                self.move_ids_without_package += self.env['stock.move'].create({
                    'name': 'Package Moves',
                    'from_package': True,
                    'product_uom': product.uom_id.id,
                    'product_id': product.id,
                    'product_uom_qty': qty,
                    'company_id': self.company_id.id,
                    'location_id': self.location_id.id,
                    'location_dest_id': self.location_dest_id.id,
                    'date': fields.Date.today()
                })


class StockMove(models.Model):
    _inherit = 'stock.move'

    from_package = fields.Boolean('From Packages')


