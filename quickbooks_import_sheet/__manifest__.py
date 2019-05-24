{
    'name': 'QuickBooks - Import using sheet',
    'version': '10.1.0',
    "category" : "account",
    'summary': 'Importing data for xls file.',
    "description": """
        Importing data from QuickBooks to Odoo using sheet(For Desktop).
    """,
    "author" : "Planet-odoo",
    'website': 'http://www.planet-odoo.com/',
    'depends': ['base', 'account', 'account_accountant', 'quickbooks_teckzilla_v10'],
    'data': [
             # 'security/ir.model.access.csv',

             'views/account_account_view.xml',
             'wizard/chart_of_accounts_import_view.xml',
             'wizard/customers_import_view.xml',
             'wizard/products_import_view.xml',
             'wizard/invoice_import_view.xml',
             # 'wizard/journal_entry_import_view.xml',
         ],

    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
