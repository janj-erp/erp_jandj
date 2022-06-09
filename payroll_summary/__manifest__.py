{
    'name' : 'J & J Payroll Summary',
    'version' : '15.0.0.4 june-8',
    'summary': 'J & J Payroll Summary',
    'sequence': 10,
    'description': """
    Payroll Summary Report for monthly/weekly 
    """,
    'author':'Hema',
    'category': 'HR Payroll',
    'website': 'https://www.odoo.com/',
    'depends' : ['base','hr_payroll','report_xlsx','j_and_j_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/payroll_summary.xml',
        'wizard/bank_transfer_summary.xml',
        'views/payslip.xml',
        'report/report.xml',
    ],
    'installable': True,
    'application': True,
}
