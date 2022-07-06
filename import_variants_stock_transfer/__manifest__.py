# -*- coding: utf-8 -*-
{
	'name': 'Import Products from Excel / Product packages',
	'version': '15.2',
	'category': 'Inventory',
	'summary': 'This apps helps to import products, variants and stock using CSV or Excel file',
	'description': '''Using this module, stock transfers are imported using excel sheets
	''',
	'author': 'CJ Rohan, Prime Minds Consulting Private Limited',
	'website': 'https://www.primeminds.co',
	'depends': ['base', 'account', 'stock', 'pos_product_customization'],
	'data': [
		'security/ir.model.access.csv',
		'wizard/view_import_chart.xml',
		'views/pack_view.xml',
		'views/create_pack_action.xml',
		'views/product_views.xml',
		],
	'auto_install': False,
	'installable': True,
	'application': True,
	'images': ['static/description/Banner.png'],
}

