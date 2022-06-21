odoo.define('pos_product_customization.ProductSelectPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { _lt } = require('@web/core/l10n/translation');
    const rpc = require('web.rpc');
    const {
        useState,
        useRef
    } = owl.hooks;

    // formerly ConfirmPopupWidget
    class ProductSelectPopup extends AbstractAwaitablePopup {

        constructor() {
            super(...arguments);
            this.state = useState({
                warehouses: [],
                selected_warehouses: [],
            });
            this.setinfo();
        }

        async setinfo() {
            let len = this.props.products.length;
            this.state.selected_warehouses = new Array(len);
            this.state.warehouses = new Array(len);
            for(let i = 0; i < len; i++) {
                this.props.products[i][0] = `/web/image?model=product.product&field=image_128&id=${this.props.products[i][2].product_id}&unique=1`;
                this.state.warehouses[i] = await this.rpc({
                    model: 'stock.picking',
                    method: 'get_warehouses_with_qty',
                    args: [[], this.props.products[i][2].product_id]
                })
            }
//            let warehouse_id = await this.rpc({
//                model: "stock.picking",
//                method: "get_pos_warehouse_id",
//                args: [[], this.env.pos.config_id],
//            })
//            for(let i = 0; i < len; i++) this.state.selected_warehouses[i] = 1;//warehouse_id;
            let order = await this.rpc({
                                model: 'pos.advance.sale',
                                method: 'search_read',
                                domain: [['name', '=', this.props.order_name],],
                                fields: ['id']
                            });
            let active_warehouse_ids = await this.rpc({
                                        model: 'pos.advance.sale',
                                        method: 'get_active_warehouses',
                                        args: [[order[0].id],]
                                    });
            if (!active_warehouse_ids.length) {
                let warehouse_id = await this.rpc({
                    model: "stock.picking",
                    method: "get_pos_warehouse_id",
                    args: [[], this.env.pos.config_id],
                })
                for(let i = 0; i < len; i++) this.state.selected_warehouses[i] = warehouse_id;
            } else {
                for(let i = 0; i < len; i++) this.state.selected_warehouses[i] = active_warehouse_ids[i] ;
            }
        }

        async confirm_post() {
            let len = this.props.products.length
            let product = new Array(len);
            let quants = new Array(len);
            let warehouses = new Array(len);
            for(let i = 0; i < len; i++) {
                product[i] = this.props.products[i][2].product_id;
                quants[i] = this.props.products[i][2].qty;
                warehouses[i] = this.state.selected_warehouses[i];
                if (!warehouses[i]) {
                    return this.showPopup('ErrorPopup', {
                            title: _("Invalid Data"),
                            body: _("Please select warehouses for all products."),
                            });
                }
            }
            let data = await this.rpc({
                            model: 'product.product',
                            method: 'confirm_selections',
                            args: [[],
                                product,
                                quants,
                                warehouses,
                                this.props.order_name,
                                this.env.pos.config_id,
                            ]
                        });
            if (!data[0]) {
                return this.showPopup('ErrorPopup', {
                            title: _("Quantity Unavailable!"),
                            body: data[1],
                            });
            } else {
                return this.showPopup('ConfirmPopup', {
                            title: _("Quantities Validated!"),
                            body: data[1],
                            });
            }
        }
    }
    ProductSelectPopup.template = 'ProductSelectPopup';
    ProductSelectPopup.defaultProps = {
        confirmText: _lt('Ok'),
        title: _lt('Confirm ?'),
        body: '',
        products: false,
        order_name: '',
    };

    Registries.Component.add(ProductSelectPopup);

    return ProductSelectPopup;
});
