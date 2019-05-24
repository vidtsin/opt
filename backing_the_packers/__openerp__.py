# -*- coding: utf-8 -*-
{
    'name': "Backing The Packers",

    'summary': """
        Booking & Property Management System""",

    'description': """
        TODO Write desrciption
    """,

    'author': "Backing The Packers",
    'website': "http://www.backingthepackers.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock_account','account','stock','account_accountant','l10n_uk','point_of_sale', 'sale_start_end_dates'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/quick/sale_view.xml',
        'views/merge/sale_order.xml',
        'views/merge/sale_order_merge.xml',
        'views/views.xml',
        'views/templates.xml',
	'views/sale_order.xml',
	'data/operations.xml',
	'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
