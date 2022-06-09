odoo.define("pos_salesperson.pos_salesperson", function (require) {
    "use strict";

var models = require('point_of_sale.models')
var PosDB = require('point_of_sale.DB')

var _super_order = models.Order.prototype;

models.Order = models.Order.extend({
     initialize: function (attributes, options) {
        _super_order.initialize.apply(this, arguments);
//        this.salesperson = null;
        this.set({
            'salesperson': null
        })
    },
    export_as_JSON: function () {
        const json = _super_order.export_as_JSON.apply(this, arguments);
        json.salesperson = this.salesperson ? this.salesperson.id : false;
        return json;
    },
    init_from_JSON: function (json) {
        _super_order.init_from_JSON.apply(this, arguments);
        this.salesperson = this.pos.salesperson_by_id[json.salesperson];
    },
    set_salesperson: function(salesperson){
        self = this;
        self.salesperson = salesperson;
    },

    get_salesperson: function(){
        return this.get('salesperson') || this.salesperson;
    },

    get_salesperson_name: function(){
        var salesperson = this.get('salesperson');
        return salesperson ? salesperson.name : "";
    },
});

models.load_models([{
    model:  'hr.employee',
    fields: ['name', 'id', 'user_id'],
    domain: function(self){
        return self.config.salesperson_ids.length > 0
            ? [
                  '&',
                  ['company_id', '=', self.config.company_id[0]],
                  '|',
                  ['user_id', '=', self.user.id],
                  ['id', 'in', self.config.salesperson_ids],
              ]
            : [['company_id', '=', self.config.company_id[0]]];
    },
    loaded: function(self, employees) {
        if (self.config.module_pos_hr) {
            self.salespeople = employees;
            self.salesperson_by_id = {};
            self.salespeople.forEach(function(sp) {
                self.salesperson_by_id[sp.id] = sp;
            });
        }
    }
}]);
});
