{
    'name': 'BTC Export',
    'version': '1.0',
    'category': '',
    'description': """

    """,
    "website" : "www.teckzilla.net",
    'author': 'Teckzilla Software Solutions',
    'depends': ['sale','product','website','base','auth_signup','crm','base_geolocalize'],
    'css': [

        ],
    "demo" : [],
    "data": [
        'security/ir.model.access.csv',

       	'views/btc_lead_view.xml',
        'views/btc_contacts_view.xml',
        'views/btc_product_view.xml',
        'views/btc_stage_view.xml',
        'views/prospect_view.xml',
        # 'wizard/wizard_export_view.xml',
        'wizard/wizard_import_lead_view.xml',
        'wizard/wizard_lead_view.xml',
        'wizard/wizard_prospect_view.xml',
        'wizard/wizard_prospect_new_view.xml',
        'wizard/wizard_user_view.xml',
        # 'wizard/wizard_res_partner_view.xml'
        'wizard/wizard_pipeline_view.xml',
        'wizard/btc_ir_attch_view.xml',
        'wizard/btc_mail_messages_view.xml',



    ],
    'installable': True,
}
