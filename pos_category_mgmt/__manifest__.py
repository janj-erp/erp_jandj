{
    "name": """POS Category Management""",
    "summary": """Shows the product for only selected category""",
    "category": "Point of Sale",
    "version": "15.0.0.0",
    "application": False,
    "author": "Prime Minds Consulting Services",
    "website": "http://primeminds.co",
    "license": "LGPL-3",  # MIT
    "depends": ["point_of_sale"],
    "data": [],
    "qweb": [],
    "auto_install": False,
    "installable": True,
    'assets': {
        'point_of_sale.assets': [
            'pos_category_mgmt/static/src/js/*.js',
        ],
    },
}
