{
    'name': 'Employee Customization',
    'version': '15.1',
    'summary': 'Enhancement has been done in various models, created new models, fields and edited the flow of models',
    'author': 'Murali GM',
    'created_on': '18 May',
    'last_updated_on': '18 May',
    'sequence': 1,
    'description': """Enhancement has been done in various models, created new models, fields and edited the flow of models""",
    'category': 'Tools',
    'depends': ['hr', 'base'],
    'data': [
        'views/res_users.xml',
        'views/hr_employee.xml',
        'security/group_employee.xml'

    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
