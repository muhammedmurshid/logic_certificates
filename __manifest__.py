{
    'name': "Certificates",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/experience.xml',
        'views/experience_template.xml',
        'views/salary_slip.xml',
        'views/salary_template.xml',
        'views/bonafide_certificates.xml',
        'views/bonafide_template.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'logic_certificates/static/src/js/location.js',
        ],
    },
    'demo': [],
    'summary': "cip/excel_module",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}
