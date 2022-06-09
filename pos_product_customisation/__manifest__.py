# -*- coding: utf-8 -*-

{
    'name': 'Product Stock Moves from POS',
    'version': '1.3',
    'category': 'Point of Sale',
    'summary': '''1. Request Products from POS Interface \n
                  2. Update Product's quantity from POS Interface''',
    'website': 'https://www.primeminds.co',
    'author': 'CJ Rohan, Prime Minds Consulting Private Limited',
    'depends': ['base', 'point_of_sale', 'stock', 'product'],
    'sequence': 50,
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/product_view.xml',
        'data/server_actions.xml',
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
