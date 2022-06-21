odoo.define('pos_product_customization.new_order', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const NumberBuffer = require('point_of_sale.NumberBuffer');

    const NewOrderCustom = ProductScreen =>
    class extends ProductScreen {

        constructor() {
            super(...arguments);
            if (!this.currentOrder.order_type) {
                this.set_order_type();
            }
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

        async _clickProduct(event) {
            if (!this.currentOrder) {
                this.env.pos.add_new_order();
            }
            const product = event.detail;
            const options = await this._getAddProductOptions(product);
            // Do not add product if options is undefined.
            if (!options) return;
            //Custom Code: Check if the quantity of chosen product is more than zero or is an advance sale type of order
            var quant = await this.rpc({
                    model: 'product.product',
                    method: 'get_warehouse_quant',
                    args: [[product.id],
                    this.env.pos.config_id],
                });
            if (quant <= 0) {
                var current_type = this.currentOrder.order_type
                if (!current_type) {
                    let order = await this.rpc({
                                    model: 'pos.advance.sale',
                                    method: 'search_read',
                                    domain: [['name', '=', this.currentOrder.export_as_JSON().name],],
                                    fields: ['id']
                                });
                    if (!order.length) {
                        this.env.pos.add_new_order();
                        await this.rpc({
                            model: 'pos.advance.sale',
                            method: 'create_new',
                            args: [[], this.currentOrder.export_as_JSON().name, this.env.pos.config_id,],
                            fields: ['name', 'state']
                        });
                    } else {
                        current_type = 'advance';
                    }
                    this.currentOrder.order_type = 'advance';
                }
                this.currentOrder.add_product(product, options);
                NumberBuffer.reset();
                if (!current_type) {
                    return this.showPopup('ConfirmPopup', {
                        title: _("Zero Quantity!"),
                        body: _("This product's quantity is zero. A New Order of type Advance Sale has been started."),
                        cancelText: "",
                    });
                }
                return
            }

            // Add the product after having the extra information.
            this.currentOrder.add_product(product, options);
            NumberBuffer.reset();
        }

    }

    Registries.Component.extend(ProductScreen, NewOrderCustom);

    return NewOrderCustom;

});