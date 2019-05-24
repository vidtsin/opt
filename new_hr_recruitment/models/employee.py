from odoo import models, fields, api

AVAILABLE_PRIORITIES = [
    ('0', 'Normal'),
    ('1', 'Bad'),
    ('2', 'Average'),
    ('3', 'good'),
]


class hr_employee(models.Model):
    _inherit = "hr.employee"

    visa_no = fields.Char('Visa')
    permit_no = fields.Char('Permit')
    issue_date = fields.Date('Issue Date')
    expiry_date = fields.Date('Expiry Date')
    joining_date = fields.Date('Joining Date')
    employment_date = fields.Date('Employment Date')
    gap = fields.Char('Gap(Months)')
    experience = fields.Char('Countable Experience(Months)')
    previous_expr = fields.Char('Prev. Expr.(Months)')
    current_expr = fields.Char('Curr. Expr.(Months)')
    total_expr = fields.Char('Total. Expr.(Months)')
    description = fields.Text('Skills')
    phone = fields.Char('Phone')
    mobile_no = fields.Char('Mobile Number')
    alternative_mob_no = fields.Char('Alternative Mobile No.')

    emp_education_data = fields.One2many('emp.education', 'edu_id', String="Education Data")
    emp_details = fields.One2many('emp.education', 'emp_id', String="Employee Data")
    family_details = fields.One2many('emp.education', 'family_id', String="Family Data")
    medical_data = fields.One2many('emp.education', 'medical_id', String="Medical Data")
    emp_skills_details = fields.One2many('emp.education', 'skill_id', String="Skills Data")

    identification_no = fields.Char('Identification No.')
    state_id = fields.Many2one('res.country.state', 'state_id')
    country_id = fields.Many2one('res.country', 'country_id')
    city = fields.Char('City')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip')

    review_date = fields.Date('Date of Review')
    last_raise = fields.Date('Date of Last Raise')
    last_promotion = fields.Date('Last Promotion Date')
    last_class_change = fields.Date('Date of Last Class Change')
    last_paycheck = fields.Date('Date of Paycheck')
    hire_date = fields.Date('Hire Date')
    termination_date = fields.Date('Termination Date')
    name_of_bank = fields.Char('Bank Name')
    account_holder = fields.Char('Account Holder')
    bank_account_no = fields.Char('Bank Account No.')
    bank_identifier_code = fields.Char('Bank Identifier Code')
    phone_number = fields.Char('Phone')
    email = fields.Char('Email')
    policy = fields.Char('Policy')
    amount = fields.Float('Amount')
    start_date = fields.Date('Date Started')
    close_date = fields.Date('Date Closed')
    dependent = fields.Selection([('spouse', 'Spouse'),
                                  ('children', 'Children'),
                                  ('mother', 'Mother'),
                                  ('father', 'Father')],
                                 string='Dependent')
    dependent_name = fields.Char('Full Name of Dependent')
    job_description = fields.Text('Job Description')
    shift = fields.Selection([('first_shift', 'First shift'),
                              ('second_shift', 'Second shift'),
                              ('third_shift', 'Third shift')],
                             string='Shift')
    employee_category = fields.Selection([('exempt', 'Exempt'),
                                          ('non_exempt', 'Non-exempt')],
                                         string='Category')

    technical = fields.Selection(AVAILABLE_PRIORITIES, string='Technical', index=True, default=AVAILABLE_PRIORITIES[0][0])


    functional = fields.Selection(AVAILABLE_PRIORITIES, string='Functional', index=True, default=AVAILABLE_PRIORITIES[0][0])

    analytical = fields.Selection(AVAILABLE_PRIORITIES, string='Analytical', index=True, default=AVAILABLE_PRIORITIES[0][0])

    communication = fields.Selection(AVAILABLE_PRIORITIES, string='Communication', index=True, default=AVAILABLE_PRIORITIES[0][0])

    remarks = fields.Text('Remarks')




