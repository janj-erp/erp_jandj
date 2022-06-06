{
    'name' : 'J & J Payroll',
    'version' : '15.0.0.5 june-6',
    'summary': 'J & J Payroll Configuration',
    'sequence': 10,
    'description': """
    Payroll Calculation monthly/weekly basis
    """,
    'author':'Hema',
    'category': 'HR Payroll',
    'website': 'https://www.odoo.com/',
    'depends' : ['base','hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_emp_form.xml',
        'wizards/bulk_payslips_wizard_view.xml',
        'views/bulk_payslip_menu.xml',
        "reports/jj_payslip.xml",
        "reports/jj_payslip_template.xml",
    ],
    'installable': True,
    'application': True,
}
