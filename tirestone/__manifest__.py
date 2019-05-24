{
    'name': 'TireStone',
    'version': '1.0',

    'sequence': 15,
    'summary': '',
    'description': """ 
    """,
    'author':'Planet Odoo',
    'website': 'https://www.odoo.com/page/crm',
    'depends': ['sale'],
    'data': [
        'views/sale_order_view.xml',
        'views/report_invoice_view.xml',

        ],
# 'qweb': [
#
#     ],
    'installable': True,
    'auto_install': False,
    'application': True,
}