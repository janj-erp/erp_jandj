{
    'name': 'TimeOffice Attendance Integration',
    'version': '13.0.0.3 04 Mar',
    'category': 'Account',
    'license': 'AGPL-3',
    'description': """""",
    'Last Updated': '',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'author': 'PMCS Er. Biswajeet',
    'website': 'http://www.primeminds.co',
    'depends': ['hr_attendance', 'hr', 'base'],
    'data': [
        'data/cron.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_inherit.xml',
        'views/res_company_inherit.xml',
        'wizard/attendance_sync_wizard.xml'
    ],
    'installable': True,
}
