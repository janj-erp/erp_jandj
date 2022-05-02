odoo.define('pos_product_creation.product_create_popup', function(require) {
    'use strict';

    const {
        useState,
        useRef
    } = owl.hooks;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');
    const { useListener } = require('web.custom_hooks');

    class ProductCreatePopup extends AbstractAwaitablePopup {

        async load_products(){
            var x =  await this.props.products;
            this.state.products = x;
        }

        async load_warehouses(){
            var x =  await this.props.warehouses;
            this.state.warehouses = x;
        }

        constructor() {
            super(...arguments);
//            console.log(this.props.product)
            this.state = useState({
                products: [],
                warehouse: this.env.pos.config,
                warehouses: [],
                typeValue: this.props.startingValue,
                productValue: this.props.startingValue,
                priceValue: this.props.priceValue,
                productRef: this.props.startingValue,
                title: "Request stock for a Product",
            });
            this.load_products()
            this.load_warehouses()
        }

        confirm(data, reserve){
//            console.log(this.state.wareValue)
            if (!this.state.wareValue) {
                this.showPopup('ErrorPopup', {
                            title: this.env._t('User Error'),
                            body: this.env._t('Please select the source location'),
                        });
            } else {
                var rpc = require('web.rpc');
                rpc.query({
                    model: 'stock.picking',
                    method: 'create_from_pos',
                    args: [[], [{'warehouse_name': this.env.pos.config}, this.props.product.id, this.state.priceValue, this.state.wareValue, this.state.note], reserve]
                }).then(function (data) {
                });
                this.cancel()
            }

//            useListener('close-screen', this.close);
//            this.cancel()
//            this.trigger('close-screen');
        }

//        getPayload() {
//            var selected_vals = [];
//            var category = this.state.typeValue;
//            var product = this.state.productValue;
//            var product_reference = this.state.productRef;
//            var price = this.state.priceValue;
//            var unit = this.state.unitValue;
//            var product_category = this.state.categoryValue;
//            selected_vals.push(category);
//            selected_vals.push(product);
//            selected_vals.push(product_reference);
//            selected_vals.push(price);
//            selected_vals.push(unit);
//            selected_vals.push(product_category);
//            return selected_vals
//        }
    }
    ProductCreatePopup.template = 'ProductCreatePopup';
    ProductCreatePopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        array: [],
        title: 'Create ?',
        body: '',
        startingValue: '',
        priceValue: 0,
        list: [],
        products: rpc.query({
                                model: 'stock.picking',
                                method: 'get_products',
                                args: [[]]
                            }).then(function (data) {
                                return data;
                            }),
        warehouses: rpc.query({
                                model: 'stock.picking',
                                method: 'get_warehouses',
                                args: [[]]
                            }).then(function (data) {
                                return data;
                            }),
    };

    Registries.Component.add(ProductCreatePopup);

    return ProductCreatePopup;
});
