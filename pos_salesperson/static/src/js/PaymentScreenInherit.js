odoo.define('pos_salesperson.PaymentScreenInherit', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen')


//    class SalespersonButton extends PosComponent{
//        selectSalesperson() {
//        }
//    }
//    Registries.Component.add(SalespersonButton);
//
//    return SalespersonButton;
const PaymentScreenPopup = (PaymentScreen) =>
        class extends PaymentScreen {
            async selectSalespersonView(selectionList) {
            const {confirmed, payload: salesperson} = await this.showPopup(
                "SelectionPopup",
                {
                    title: this.env._t("Change Salesperson"),
                    list: selectionList
                }
            );

            if (!confirmed) return false;
            if (salesperson) {
                return salesperson;
            }
        }

        async selectSalesperson() {
                const list = this.env.pos.salespeople.map((sp) => {
                    return {
                        id: sp.id,
                        item: sp,
                        label: sp.name,
                        isSelected: false,
                    };
                });
                const sales_person = await this.selectSalespersonView(list);
                if (sales_person) {
                    this.env.pos.set_salesperson(sales_person);
                    this.showScreen("PaymentScreen");
                }
            }
        }
        Registries.Component.extend(PaymentScreen, PaymentScreenPopup)
        return PaymentScreenPopup
    });