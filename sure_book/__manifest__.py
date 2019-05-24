# -*- coding: utf-8 -*-
{
    'name': "SureBook",

    'summary': """
        Booking & Property Management System""",

    'description': """
        TODO Write desrciption
    """,

    'author': "Teckzilla ",
    'website': "http://www.teckzilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'SureBook',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock_account','account','stock','account_accountant','l10n_uk','point_of_sale','website_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/authorized_view.xml',
        'views/account_invoice.xml',
        'views/account_journal.xml',
        'views/voucher_payment_receipt_view.xml',
        'views/account_move.xml',
        'views/product.xml',
        'views/myallocator_config_view.xml',
        'views/my_allocator_dashboard_view.xml',
        'views/myallocator_property_view.xml',
        'views/myallocator_room_view.xml',
        'views/myallocator_channel_view.xml',
        'views/sale_start_end_date.xml',
        'views/myallocator_booking_view.xml',
        'views/booking.xml',
        'views/scheduler.xml',
        'views/sale_order.xml',
        'views/merge/sale_order.xml',
        'views/merge/sale_order_merge.xml',
        'views/quick/sale_view.xml',
        'views/pos_config_demo.xml',
        'views/pos_config_view.xml',
        'views/pos_order_view.xml',
        'views/template.xml',
        'views/templates.xml',
        'views/check_in_room.xml',
        'wizard/create_booking_view.xml',
        'wizard/update_room_view.xml',
        'data/operations.xml',
	'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': ['demo/*.xml',],
    'qweb': ['static/src/xml/*.xml'],
}
