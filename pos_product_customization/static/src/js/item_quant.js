odoo.define('pos_product_customization.item_quant', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const ProductItem = require('point_of_sale.ProductItem');
//    const NumberBuffer = require('point_of_sale.NumberBuffer');

    const ItemQuant = ProductItem =>
    class extends ProductItem {

        constructor() {
            super(...arguments);
            this.set_product_quant();
        }

        async set_product_quant() {
            this.props.product.quant = await this.rpc({
                    model: 'product.product',
                    method: 'get_warehouse_quant',
                    args: [[this.props.product.id],
                    this.env.pos.config_id],
                });
        }
    }

    Registries.Component.extend(ProductItem, ItemQuant);

    return ItemQuant;

});