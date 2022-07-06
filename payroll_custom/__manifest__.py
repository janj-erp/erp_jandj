# -*- coding: utf-8 -*-
{
    'name': 'Portal Payroll',
    'summary': """This module customizes for allowing portal user to manage their payslips """,
    'version': '15.0.0.1 7-jan',
    'description': """""",
    'author': 'PMCS',
    'sequence':1000,
    'company': 'prime minds consulting pvt ltd',
    'website': 'http://www.primeminds.com',
    'category': 'Sale',
    'depends': ['base','hr','website','mail','portal','hr_payroll'],
    'data': [
        'views/payroll.xml',
        # 'views/timeoff_create.xml',

    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
