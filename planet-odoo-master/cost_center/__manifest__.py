# -*- coding: utf-8 -*-
{
    'name': "Cost Center",

    'summary': """
        Cost Center 
        """,
    
    'description': """
        Adding fields in product and donation line
        Adding section in the donation.
        Adding donation report and customizing it.
    """,

    'author': "Teckzilla Software Solutions pvt. ltd.",
    'website': "http://www.teckzilla.net",
    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'images': ['static/description/icon.png'],
    'depends': ['base','sale','account_journal_task','donation','report','document'],

    # always loaded
    'data': [
        'views/inherit_product_template_view.xml',
        'views/donation_access.xml',
        'views/inherit_donation.xml',
        # 'views/inherit_partner.xml',
        # 'views/donation_form_inherit.xml',
        'report/report_tax_rec_donation.xml',
        'report/donation_report.xml',
        'report/donation_report_analysis_new.xml',
        # 'security/security_groups.xml',

        # 'report/report_header_footer.xml',
        ],
    # only loaded in demonstration mode
    'demo': [
#        'demo/demo.xml',
    ],
}