odoo.define('pos_product_customization.validate_popup', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');

    const ValidatePopup = PaymentScreen =>
    class extends PaymentScreen {

        constructor() {
            super(...arguments);
            if (!this.currentOrder.order_type) {
                this.setOrderType();
            } else {
                if (!this.currentOrder.is_to_invoice()) {
                    this.toggleIsToInvoice();
                }
            }
        }

        async setOrderType() {
            let order = await this.rpc({
                            model: 'pos.advance.sale',
                            method: 'search_read',
                            domain: [['name', '=', this.currentOrder.export_as_JSON().name],],
                            fields: ['id']
                        });
            if (order.length) {
                this.currentOrder.order_type = 'advance';
                if (!this.currentOrder.is_to_invoice()) {
                    this.toggleIsToInvoice();
                }
            }
        }

        async validateOrder(isForceValidate) {
            let order_id = false;
            if (this.currentOrder.order_type) {
                let order = await this.rpc({
                                model: 'pos.advance.sale',
                                method: 'search_read',
                                domain: [
                                    ['name', '=', this.currentOrder.export_as_JSON().name],
                                    ['state', '!=', 'new'],
                                ],
                                fields: ['name', 'state']
                            });
                console.log(order)
                if (!order.length) {
                    return this.showPopup('ConfirmPopup', {
                        title: _("Selection Pending!"),
                        body: _("Please select the locations for each product and confirm its availability."),
                    });
                } else {
                    order_id = order[0].id;
                    let availability = await this.rpc({
                                            model: 'pos.advance.sale',
                                            method: 'confirm_availability',
                                            args: [[order_id], ]
                                       });
                    console.log(availability);
                    if (!availability[0]) {
                        return this.showPopup('ErrorPopup', {
                            title: _("Oops! It seems some products have been consumed.."),
                            body: _(availability[1]),
                            cancelText: "Close",
                        });
                    }
                }
            } else {
                let lines = this.currentOrder.export_as_JSON().lines
                for(let i = 0; i < lines.length; i++) {
                    if (lines[i][2].full_product_name.includes('Discount') || lines[i][2].full_product_name.includes('Expense')){
                        continue;
                    }
                    let available_qty = await this.rpc({
                        model: 'product.product',
                        method: 'get_warehouse_quant',
                        args: [[lines[i][2].product_id],
                        this.env.pos.config_id],
                    });
                    let selling_qty = lines[i][2].qty;
                    if (selling_qty > available_qty) {
                        return this.showPopup('ErrorPopup', {
                            title: _("Quantity Unavailable!"),
                            body: _("Product " + lines[i][2].full_product_name + " has only {" + available_qty.toString()
                                    + "}Nos available, but you are trying to sell {" + selling_qty.toString() +
                                    "}Nos. Please edit this order before selling or update the quantity of the " +
                                    "product. If you are trying to make an advance sale, start an advance order."),
                        });
                    }
                }
            }

            if(this.env.pos.config.cash_rounding) {
                if(!this.env.pos.get_order().check_paymentlines_rounding()) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Rounding error in payment lines'),
                        body: this.env._t("The amount of your payment lines must be rounded to validate the transaction."),
                    });
                    return;
                }
            }
            if (await this._isOrderValid(isForceValidate)) {
                // remove pending payments before finalizing the validation
                for (let line of this.paymentLines) {
                    if (!line.is_done()) this.currentOrder.remove_paymentline(line);
                }
                if (order_id) {
                    await this.rpc({
                            model: 'pos.advance.sale',
                            method: 'complete_stock_pickings',
                            args: [[order_id], ]
                       });
                    if (this.currentOrder.is_paid()) {
                        await this.rpc({
                                model: 'pos.advance.sale',
                                method: 'mark_fully_paid',
                                args: [[order_id], ],
                           });
                    }
                }
                await this._finalizeValidation();
            }
        }

        async advanceMapping() {
            return this.showPopup('ProductSelectPopup', {
                        title: _("Select Location"),
                        body: _("Please select the locations you want to sell from"),
                        confirmText: "Confirm",
                        products: this.currentOrder.export_as_JSON().lines,
                        order_name: this.currentOrder.export_as_JSON().name,
                    });
        }

    }

    Registries.Component.extend(PaymentScreen, ValidatePopup);

    return ValidatePopup;

});