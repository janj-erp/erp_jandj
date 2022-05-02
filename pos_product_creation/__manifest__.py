# -*- coding: utf-8 -*-
{
    'name': 'Create Stock Requests From POS',
    'version': '14.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Create Products From POS Interface',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
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
            "pos_product_creation/static/src/js/product_create_popup.js",
            # "pos_product_creation/static/src/js/product_create_button.js",
            "pos_product_creation/static/src/js/create_request.js",
        ],
        'web.assets_qweb': [
            'pos_product_creation/static/src/xml/*',
        ],
    },
}
