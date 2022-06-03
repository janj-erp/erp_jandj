{
    'name': 'Exzatech Payroll Configuration',
    'version': '15.0.1.7 24-mar',
    'summary': 'Exzatech Payroll Configuration',
    'sequence': 15,
    'description': """
    Payroll Calculation
    """,
    'author': 'Hema',
    'category': 'HR Payroll',
    'website': 'https://www.odoo.com/',
    'depends': ['base','hr_payroll','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'data/cron_func.xml',
        'views/hr_emp_form.xml',
        'views/accrual_plan_view.xml',
        "wizard/payroll_summary_view.xml",
        'views/summary_menu.xml',
        'data/server_action.xml',
        "reports/payslip.xml",
        "reports/payslip_template.xml",
        "reports/summary_report.xml",
    ],
    'installable': True,
    'application': True,
}
