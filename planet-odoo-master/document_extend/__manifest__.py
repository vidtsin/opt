
# -*- coding: utf-8 -*-
{
    'name': "Document Extended",

    'summary': """
        Customization of Document module 
        """,
    
    'description': """
        This module is developed for customizing
        default document module to support DMS
                
    """,

    'author': "Teckzilla Software Solutions pvt. ltd.",
    'website': "http://www.teckzilla.net",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Document',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'images': ['static/description/icon.png'],
    'depends': ['base','document'],

    # always loaded
    'data': [
        'views/document_menu.xml',
        'data/document_dir_data.xml',
        'views/attachment.xml',

        ],
    # only loaded in demonstration mode
    'demo': [
#        'demo/demo.xml',
    ],
}