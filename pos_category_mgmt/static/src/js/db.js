odoo.define('pos_category_mgmt.db', function (require) {
"use strict";

    var utils = require('web.utils');
    const PosDB = require('point_of_sale.DB');

    PosDB.include({
        add_products: function(products){
            var stored_categories = this.product_by_category_id;

            if(!products instanceof Array){
                products = [products];
            }
            for(var i = 0, len = products.length; i < len; i++){
                var product = products[i];
                if (product.id in this.product_by_id) continue;
                if (product.available_in_pos){
                    var search_string = utils.unaccent(this._product_search_string(product));
                    var categ_id = product.pos_categ_id ? product.pos_categ_id[0] : this.root_category_id;
                    product.product_tmpl_id = product.product_tmpl_id[0];
                    if(!stored_categories[categ_id]){
                        stored_categories[categ_id] = [];
                    }
                    stored_categories[categ_id].push(product.id);

                    if(this.category_search_string[categ_id] === undefined){
                        this.category_search_string[categ_id] = '';
                    }
                    this.category_search_string[categ_id] += search_string;

                    var ancestors = this.get_category_ancestors_ids(categ_id) || [];

                    for(var j = 0, jlen = ancestors.length; j < jlen; j++){
                        var ancestor = ancestors[j];
//                        if(! stored_categories[ancestor]){
//                            stored_categories[ancestor] = [];
//                        }
//                        stored_categories[ancestor].push(product.id);

                        if( this.category_search_string[ancestor] === undefined){
                            this.category_search_string[ancestor] = '';
                        }
                        this.category_search_string[ancestor] += search_string;
                    }
                }
                this.product_by_id[product.id] = product;
                if(product.barcode){
                    this.product_by_barcode[product.barcode] = product;
                }
            }
        },
    });
});