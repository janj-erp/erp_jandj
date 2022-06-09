odoo.define("pos_salesperson.pos_model", function (require) {
    "use strict";

    var models = require('point_of_sale.models')

   var posmodel_super = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        get_salesperson: function() {
            var order = this.get_order();
            if (order) {
                return order.get_salesperson();
            }
            return null;
        },

        set_salesperson: function(salesperson) {
            var order = this.get_order();
            if (order) {
                return order.set_salesperson(salesperson);
            }
            return null;
        },

    });
});