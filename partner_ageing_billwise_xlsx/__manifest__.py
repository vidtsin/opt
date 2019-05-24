# -*- coding: utf-8 -*-
###################################################################################

###################################################################################
{
    'name': 'Aged Partner Balance In Excel',
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Bill-Wise Aged Partner Balance in Excel Format',
    'description': """
    This module provides features to take an excel report of bill-wise aged partner balance.
    """,
    "author"               :  "Planet Odoo",
     "website"              :  "https://www.odoo.com/page/crm",
    'depends': ['report_xlsx', 'account_accountant'],
    'data': [
             'views/report_aged_partner_billwise.xml',
            ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
