{
    'name': 'Ethnic Classification',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
Define ehhtnic group for employee
========================================
  
    """,
    'author': 'Teckzilla Software Solutions pvt. ltd.',
    'website': 'http://www.teckzilla.net',
    'depends': [
        'hr',

    ],
    # 'init_xml': [
    # ],
    'data': [
        'views/ethnic_cat_view.xml',
        'data/ethnic_group_data.xml',
    ],
    'test': [
    ],

    'installable': True,
    'active': False,
}
