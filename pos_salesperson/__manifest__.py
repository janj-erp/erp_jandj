{
    "name": """POS Salesperson Select""",
    "summary": """Select Salesperson on the Payment Screen""",
    "category": "Point of Sale",
    "version": "15.0.0.0.0",
    "application": False,
    "author": "Prime Minds Consulting Services",
    "website": "http://primeminds.co",
    "license": "LGPL-3",  # MIT
    "depends": ["point_of_sale","pos_hr","hr"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        # "views/views.xml",
        "views/pos_config_inherit.xml",
        "views/pos_order_inherit.xml",
    ],
    "qweb": [

    ],
    "auto_install": False,
    "installable": True,
    'assets': {
        'point_of_sale.assets': [
            'pos_salesperson/static/src/js/main.js',
            'pos_salesperson/static/src/js/PaymentScreenInherit.js',
            # 'pos_salesperson/static/src/js/SelectionPopupSalesperson.js',
            'pos_salesperson/static/src/js/PosModel.js',
            'pos_salesperson/static/src/css/*.*',

        ],
        'web.assets_qweb': [
            'pos_salesperson/static/src/xml/*',
            # 'pos_salesperson/static/src/xml/PaymentScreenSalesperson.xml',


        ],
    },
}
