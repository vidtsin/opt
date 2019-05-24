{
    'name': 'Crm Lead Website Integration',
    'version': '1.0',
    'category': 'CRM Details',
    'sequence': 15,
    'summary': '',
    'description': """ 
    """,
    'author':'Planet Odoo',
    'website': 'https://www.odoo.com/page/crm',
    'depends': ['crm','base','sale_crm','website_crm_partner_assign'],
    'data': [
        'view/crm_lead_student.xml',
        'view/product_view.xml',
        'view/biztec_program.xml',
        # 'view/my_report_crm.xml',
        'security/crm_lead_website_integration_security.xml',
        'security/ir.model.access.csv',
        'report/crm_opportunity_report_views.xml',
        'wizard/crm_report_wizard_view.xml',
        'wizard/crm_city_report_wizard_view.xml',
        'wizard/crm_country_report_wizard_view.xml',
        'wizard/leads_by_creation_date_view.xml',
        'wizard/comparative_reports_view.xml'
        ],
# 'qweb': [
#         "static/src/xml/sales_team_dashboard.xml",
#     ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
