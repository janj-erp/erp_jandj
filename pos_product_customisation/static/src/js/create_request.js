odoo.define('pos_stock_request.CreateRequest', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const ProductInfoPopup = require('point_of_sale.ProductInfoPopup');

    const CreateRequest = ProductInfoPopup =>
    class extends ProductInfoPopup {
        open_req(reserve) {
//            console.log("sssssssss", this.props.product, reserve)
            if (reserve) {
                this.showPopup('ProductCreatePopup',  {product: this.props.product, reserve: 1})
            } else {
                this.showPopup('ProductCreatePopup',  {product: this.props.product})
            }
        }

    }
//    CreateRequest.template = 'CreateRequest';

    Registries.Component.extend(ProductInfoPopup, CreateRequest);

    return CreateRequest;
});