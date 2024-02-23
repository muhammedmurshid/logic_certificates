{
    'name': "CIP",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/experience.xml',
        'views/experience_template.xml',
        'views/salary_slip.xml',
        'views/salary_template.xml',
    ],

    'demo': [],
    'summary': "cip/excel_module",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}
