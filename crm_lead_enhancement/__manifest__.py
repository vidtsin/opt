# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'CRM Lead enhancement',
    'version' : '1.0',
    'description': """
    
""",
    'depends' : ['crm','sale_crm','crm_lead_website_integration'],
    'data': [
        'views/crm_lead_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
