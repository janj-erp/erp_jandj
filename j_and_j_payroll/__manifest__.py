{
    'name' : 'J & J Payroll',
    'version' : '15.0.0.2',
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
        'views/hr_emp_form.xml',
        "reports/jj_payslip.xml",
        "reports/jj_payslip_template.xml",
    ],
    'installable': True,
    'application': True,
}
