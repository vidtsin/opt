# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'PFS CRM leads',
    'version': '1.1',
    'category': 'CRM',
    'description': """
Add additional date information to the sales order.
===================================================

You can add the additional fields to a sales order:
------------------------------------------------------------
""",
    'website': 'https://www.odoo.com/page/crm',
    'depends': ['sale','crm','mail'],
    'data': [
        # 'data/activity_data.xml',
        # 'data/mail_data.xml',
        # 'data/filing_demo_data.xml',
        'views/crm_lead_new.xml',
        'views/crm_activities_new.xml',
        'views/hst_email_template.xml',
        'views/payroll_email_template.xml',
        'views/hst_payroll_settings.xml',
        'views/pfs_wizard.xml',

             ],
    'installable': True,
    'auto-install' : True,
}