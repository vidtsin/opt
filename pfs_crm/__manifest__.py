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
        'data/newsletter_campaign_data.xml',
        'data/sin_data.xml',
        'data/next_activity_data.xml',
        'data/business_end_year_data.xml',
        'data/send_birthday_data.xml',
        'data/activity_data.xml',
        'data/mail_data.xml',
        'data/filing_demo_data.xml',
        'report/crm_lead_pipeline.xml',
        'report/crm_partnership_report.xml',
        'report/crm_oppor_report.xml',
        'report/crm_lead_report.xml',
        'wizard/crm_lead_market.xml',
        'wizard/pfs_wizard.xml',
        'wizard/pfs_convert_stage.xml',
        'views/crm_lead_new.xml',
        'views/crm_lead_Campaign_mail.xml',
        'views/crm_activities_new.xml',
        'views/hst_email_template.xml',
        'views/payroll_email_template.xml',
        'views/hst_payroll_settings.xml',
        'views/sin_schedular_settings.xml',
        'views/product_display.xml'

             ],
    'installable': True,
    'auto-install' : True,
}