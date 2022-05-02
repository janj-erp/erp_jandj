# -*- coding: utf-8 -*-
{
    'name': "J & J Reports",
    'version': '15.0.0.6',
    'summary': """This module creates employee related report in employee module""",
    'sequence': 4,
    'description': """This module creates employee related report in employee module""",
    'author': "PMCS, @soyeb",
    'website': "http://int.primeminds.co/",
    'depends': ['base', 'hr', 'point_of_sale'],
    'data': ["security/ir.model.access.csv", 'wizard/layoff.xml', 'views/hr_employee_inherit.xml', 'views/employee_experience_details.xml', 'views/employee_qualification.xml', 'views/termination_reason.xml', 'reports/Application_employement.xml', 'reports/Application_employement_template.xml', 'reports/Employee_verification.xml', 'reports/Employee_verification_template.xml', 'reports/Lay_off.xml', 'reports/Lay_off_template.xml', 'reports/suspension_letter.xml', 'reports/suspension_letter_template.xml', 'reports/termination_report.xml', 'reports/termination_report_template.xml', 'reports/warning_letter.xml', 'reports/warning_letter_template.xml'],
    'demo': [],
    'auto_install': False,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}