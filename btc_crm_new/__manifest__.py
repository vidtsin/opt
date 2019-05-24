{
    'name': 'BTC CRM NEW',
    'version': '1.0',
    'category': 'CRM Details',
    'sequence': 15,
    'summary': '',
    'description': """ 
    """,
    'author':'Planet Odoo',
    'website': 'https://www.odoo.com/page/crm',
    'depends': ['crm','base','sale','sale_crm','website_crm_partner_assign'],
    'data': [
        'views/crm_lead.xml',
        # 'wizard/crm_report_wizard_view.xml',
        # 'wizard/send_email_view.xml',
        # 'wizard/convert_stage_to_view.xml',
        # # 'wizard/filter_view_leads.xml',
        # 'wizard/filter_program_wizard_view.xml',
        # 'wizard/crm_city_report_wizard_view.xml',
        # 'wizard/crm_country_report_wizard_view.xml',
        # # 'wizard/crm_merge_opportunities_view.xml',
        # 'wizard/leads_by_creation_date_view.xml',
        # 'wizard/comparative_reports_view.xml',

        ],
# 'qweb': [
#         "static/src/xml/sales_team_dashboard.xml",
#     ],
    'installable': True,
    'auto_install': False,
    'application': True,
}