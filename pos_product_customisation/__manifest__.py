# -*- coding: utf-8 -*-

{
    'name': 'Product Stock Moves from POS',
    'version': '1.0.2',
    'category': 'Point of Sale',
    'summary': '''1. Request Products from POS Interface \n
                  2. Update Product's quantity from POS Interface''',
    'website': 'https://www.odoo.com',
    'depends': ['base', 'point_of_sale', 'stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/product_view.xml',
    ],
    # 'qweb': [
    #     'static/src/xml/product_create_button.xml',
    #     'static/src/xml/product_create_popup.xml',
    # ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'assets': {
        'point_of_sale.assets': [
            "pos_product_customisation/static/src/js/product_create_popup.js",
            # "pos_product_creation/static/src/js/product_create_button.js",
            "pos_product_customisation/static/src/js/create_request.js",
        ],
        'web.assets_qweb': [
            'pos_product_customisation/static/src/xml/*',
        ],
    },
}
