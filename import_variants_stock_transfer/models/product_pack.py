from odoo import models, fields


class ProductPack(models.Model):
    _name = 'product.pack'
    _description = 'Model to group products into a pack and use them for internal transfer'

    name = fields.Char('Pack Name')
    image_variant_1920 = fields.Image("Variant Image", max_width=256, max_height=256)
    pack_lines = fields.One2many('product.pack.line', 'pack_id', string='Pack Lines')


class ProductPackLine(models.Model):
    _name = 'product.pack.line'
    _description = 'List of product and their quantities in a pack'

    name = fields.Many2one('product.product', 'Product', required=True)
    product_image = fields.Image('Line Image', related='name.image_128')
    quantity = fields.Integer('Nos')
    # product_template_id = fields.Many2one('product.template', 'Product Template')
    pack_id = fields.Many2one('product.pack', string='Pack ID')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def create_pack(self):
        new_pack = self.env['product.pack'].create({'name': f'New Pack {fields.Datetime.now()}'})
        for rec in self:
            new_pack.pack_lines += self.env['product.pack.line'].create({
                'name': rec.id,
            })
        compose_form = self.env.ref('import_variants_stock_transfer.product_pack_form_view', False)
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'product.pack',
            'view_mode': 'form',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'res_id': new_pack.id,
            'target': 'new',
        }
        return action

