# -*- coding: utf-8 -*-
{
    'name': "booking",

    'summary': """
        Hotel Room Booking""",

    'description': """
        Booking Module
    """,

    'author': "Techversant",
    'website': "http://www.techversaninfotech.com",

    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','backing_the_packers'],
    'qweb': ['static/src/xml/*.xml'],
    'application': True,

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/booking.xml',
        'views/scheduler.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
