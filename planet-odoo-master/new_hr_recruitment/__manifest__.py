# -*- coding: utf-8 -*-
{
    'name': "Employees Resume",

    'summary': """""",


    'description': """ """,



    'author': "Teckzilla Software Solutions pvt. ltd.",
    'website': "http://www.teckzilla.net",
    'category': '',
    'version': '0.1',
    'depends': ['base', 'account', 'sale','hr','hr_payroll','hr_recruitment','hr_payroll_account'],
    'images': ['static/description/icon.png'],

    'data': [
        # 'security/recruitment_security.xml',
        # 'security/emp_recruitment.csv',
        'data/ir_sequence_data.xml',
        # 'views/attachment_view.xml',
        'views/employee_view.xml',
        'views/salary_category.xml',
        'views/resignation_view.xml',
        'views/pension_view.xml',
        'views/bank_details_view.xml',
        'views/resource_request_view.xml',
        'views/salary_contract_view.xml',
        # 'views/hr_view.xml',
        'views/resource_view.xml',
        'views/resource_category_view.xml',
        'views/hr_payslip_view.xml',
        'views/emp_compensation_view.xml',
        'report/sick_report_view.xml',
        'report/sick_report_temp_view.xml'


        # 'views/result_view.xml',
        # 'views/step_view.xml',
        # 'views/process_view.xml'

        # 'wizard/wizard_process_view.xml'
        # 'views/prospect_menu_main.xml',
        # 'views/details_form_view.xml',
        # 'views/application_no_sequence.xml',

    ]
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
