odoo.define('pos_product_customization.info_as', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const ProductInfoButton = require('point_of_sale.ProductInfoButton');
//    const NumberBuffer = require('point_of_sale.NumberBuffer');

    const InfoAS = ProductInfoButton =>
    class extends ProductInfoButton {

        constructor() {
            super(...arguments);
//            if (!this.currentOrder.order_type) {
//                this.set_order_type();
//            }
        }

        async set_order_type() {
            let order = await this.rpc({
                                model: 'pos.advance.sale',
                                method: 'search_read',
                                domain: [['name', '=', this.currentOrder.export_as_JSON().name],],
                                fields: ['id']
                            });
            if (order.length) {
                this.currentOrder.order_type = 'advance';
            }
        }
    }

    Registries.Component.extend(ProductInfoButton, InfoAS);

    return InfoAS;

});