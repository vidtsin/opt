# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Biztech Crm Lead',
    'version': '1.1',
    'category': 'Crm',
    'sequence': 35,
    'summary': 'Crm and Sales Management',
    'description': """
Accounting Access Rights
========================
It gives the Administrator user access to all accounting features such as journal items and the chart of accounts.

It assigns manager and user access rights to the Administrator for the accounting application and only user rights to the Demo user.
""",
    # 'website': 'https://www.odoo.com/page/accounting',
    'depends': ['sale', 'sales_team','crm','base_geolocalize','website_crm_partner_assign','mail','btc_export'],
    'data': [
        #'security/crm_lead.xml',
        'data/crm_lead_stage.xml',
      	# 'views/crm_lead.xml',
        'views/res_users_view.xml',
        'security/crm_lead_manager_security.xml',
    ],
    # 'demo': ['data/account_accountant_demo.xml'],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
