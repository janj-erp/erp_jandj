# -*- coding: utf-8 -*-
{
    'name': 'Timeoff Enhancements',
    'summary': """This module customizes for allowing portal user to manage their timeoffs """,
    'version': '15.3 06JUN2021-2',
    'description': """""",
    'author': 'PMCS',
    'sequence':1000,
    'company': 'prime minds consulting pvt ltd',
    'website': 'http://www.primeminds.com',
    'category': 'Sale',
    'depends': ['base','hr','website','mail','portal','hr_holidays'],
    'data': [
        'views/timeoff_list.xml',
        'views/timeoff_create.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
