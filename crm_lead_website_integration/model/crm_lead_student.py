from odoo import api, fields, models,tools, _
from datetime import datetime
import json
import logging
logger = logging.getLogger(__name__)
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError
import collections
# from pyquery import PyQuery as jQ

global ids


CRM_LEAD_FIELDS_TO_MERGE = [
    'name',
    'partner_id',
    'campaign_id',
    'company_id',
    'country_id',
    'team_id',
    'state_id',
    'stage_id',
    'medium_id',
    'source_id',
    'user_id',
    'title',
    'city',
    'contact_name',
    'description',
    'mobile',
    'partner_name',
    'phone',
    'probability',
    'planned_revenue',
    'street',
    'street2',
    'zip',
    'create_date',
    'date_action_last',
    'email_from',
    'email_cc',
    'website',
    'partner_name']






















class crm_lead_iddocs(models.Model):
    _name = 'crm.lead.iddocs'

    crm_lead_id = fields.Many2one('crm.lead')
    identification_doc_id = fields.Char('SCAN Passport pages ')


class res_partner_businessdocs(models.Model):
    _name = 'res.partner.businessdocs'

    res_partner_id = fields.Many2one('res.partner')
    business_doc_id = fields.Char('Records of Excellence and Good Standing')

class merged_crm_leads(models.Model):
    _name='merged.crm.leads'

    crm_lead=fields.Many2one('crm.lead','Lead')
    crm_lead_id = fields.Many2one('crm.lead', 'Lead')
    # team_id_name = fields.Char(related='crm_lead.name', readonly=True, store=True)
    mode_of_contact=fields.Selection([('asked_question','Request Information'),('requested_catalog','Requested Catalog'),('book_a_tour','Book A Tour'),('apply_now','Apply Now'),('call','Call'),('walk_in','Walk In')],string='Mode Of Contact')

    @api.model
    def create(self, vals):
        print vals
        result = super(merged_crm_leads, self).create(vals)
        print result
        return result

class crm_issue(models.Model):
    _name = 'crm.issue'

    issue_id = fields.Many2one('crm.lead', 'Issue ID')

    title = fields.Char(string="Title")
    note = fields.Text(string="Note")
    Report_date = fields.Date(string="Date")

class crm_note(models.Model):
    _name = 'crm.note'

    note_id = fields.Many2one('crm.lead', 'Note Id')
    user_id = fields.Many2one('res.users','Sales Staff')
    note = fields.Text(string="Note")
    name = fields.Text()



    @api.model
    def create(self, vals):
        view_id = self.env['res.users'].search([('id', '=', self.env.uid)])
        vals['name']=view_id.name
        result = super(crm_note, self).create(vals)
        return result


class OtherRequirement(models.Model):
    _name = 'other.requirement'

    # name = fields.Char(string='Name')


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    # upload_attachment_id = fields.Many2one('crm.lead','Upload Document')
    # document_type = fields.Char('Document type')
    # category = fields.Char('Category')
    # verification = fields.Char('Verification')
    # submitted_to = fields.Char('Submitted To')
    # attachments = fields.Binary("Attachments")


class Faculty(models.Model):
    _name = 'faculty.details'

    name = fields.Char("Name")
    faculty_ids= fields.One2many('program.details','faculty_id','Faculty')


class MultiProgramDetails(models.Model):
    _name = 'multi.program.details'

    program_id = fields.Many2one('crm.lead',string="program")
    program_ids=fields.Many2one('program.details',string="program")
    checkbox=fields.Boolean(' ')
    start_date = fields.Char('Start Date')
    start_date_2 = fields.Char('Start Date 2')
    start_date_3 = fields.Char('Start Date 3')

class crm(models.Model):
    _inherit = 'crm.lead'


    asked_question = fields.Boolean('Asked A Question')
    requested_catalog = fields.Boolean('Requested Catalog')
    inquiry_follow_up_date=fields.Date('Inquiry Follow-up Date')
    admission_app_req=fields.Boolean('Admission Application Request')
    date_received=fields.Date('Date Received')
    agent=fields.Char('Agent')
    app_fee_paid=fields.Date('Application Fee Paid')
    pre_requisite_material_submitted=fields.Boolean('Pre-requisite Material Submitted')
    esl_message_submitted=fields.Boolean('ESL Testing Submitted')
    offer_of_admission_date=fields.Date('Offer of Admission Date')
    net_amount_due=fields.Float('Net Amount Due')
    due_date=fields.Date('Due Date')
    net_payment_recieved=fields.Date('Net Payment Received')
    payment_type=fields.Char('Payment Type')
    offer_signed_and_returned=fields.Boolean('Offer Signed And Returned')
    bank_transaction_charges=fields.Float('Bank Transaction Charges')
    in_file=fields.Char('In File')
    international_student_letter_of_acceptance=fields.Char('International Student Letter Of Acceptance')
    date_of_issue=fields.Date('Date Of Issue')
    letter_expiry_date=fields.Date('Letter Expiry Date')
    copy_in_file=fields.Boolean('Copy In File')
    study_permit_issued=fields.Boolean('Study Permit Issued')
    copy_of_permit_in_file=fields.Boolean('Copy Of Permit In File')
    enrollment_date=fields.Date('Enrollment Date')
    expected_arrival_date=fields.Date('Expected Arrival Date')
    expected_return_date=fields.Date('Expected Return Date')
    team_id_name=fields.Char(related='team_id.name', readonly=True, store=True)
    preferred_date = fields.Date('Preferred Date')
    preferred_time = fields.Selection([('9am_to_930am', '9 am to 9:30 am'),
                                       ('930am_to_10am', '9:30 am to 10 am'),
                                       ('10am_to_1030am', '10 am to 10:30 am'),
                                       ('1030am_to_11am', '10:30 am to 11 am'),
                                       ('1am_to_1130am', '11 am to 11:30 am'),
                                       ('1130am_to_12am', '11:30 am to 12 pm'),
                                       ('12pm_to_1230pm', '12 pm to 12:30 pm'),
                                       ('1230pm_to_1pm', '12:30 pm to 1 pm'),
                                       ('1pm_to_130pm', '1 pm to 1:30 pm'),
                                       ('130pm_to_2pm', '1:30 pm to 2 pm'),
                                       ('2pm_to_230pm', '2 pm to 2:30 pm'),
                                       ('230pm_to_3pm', '2:30 pm to 3 pm'),
                                       ('3pm_to_330pm', '3 pm to 3:30 pm'),
                                       ('330pm_to_4pm', '3:30 pm to 4 pm')], 'Preferred Time')
    comments = fields.Text('Comments')
    academic_requirements=fields.Boolean('Mark As Informed')
    academic_requirements_text=fields.Text('Academic Requirements')
    academic_requirements_date = fields.Date('Date')
    academic_requirements_user = fields.Char('Informed By')
    other_requirements = fields.Boolean('Mark As Informed')
    other_requirements_text = fields.Text('Other Requirements')
    other_requirements_date = fields.Date('Date')
    other_requirements_user = fields.Char('Informed By')
    seat_deposit_amt=fields.Float('Amount')
    seat_deposit = fields.Boolean('Mark As Informed')
    seat_deposit_date = fields.Date('Date')
    seat_deposit_user = fields.Char('Informed By')
    duration_in_weeks = fields.Integer('Duration/Weeks')
    duration_in_hours = fields.Integer('Duration/Hours')
    class_schedule = fields.Char('Schedule')
    tuition_fee = fields.Float('Tuition Fee')
    texts_book_fee = fields.Float('Text Book Fee')
    seat_deposit_fee = fields.Float('Seat Deposit Fee')
    lab_fee = fields.Float('Lab/Clinical Fee')
    lab_supply_fee = fields.Float('Lab Supply Fee')
    major_equipment_fee = fields.Float('Major Equipment Fee')
    professional_exam_fee = fields.Float('Professional Exam Fee')
    program_start_date=fields.Char('Program Start Date')
    deadline_to_apply=fields.Char('Deadline To Apply')
    scholarship=fields.Char('Scholarship')
    supporting_academic_docs = fields.Boolean('Mark As Received')
    supporting_academic_docs_date = fields.Date('Date')
    supporting_academic_docs_user = fields.Char('Received By')
    other_consideration=fields.Char('Notes')
    assessment_test_date=fields.Date('Assessment Test Date')
    seat_deposit_amount=fields.Float('Seat Deposit Amount')
    deposit_payment_date=fields.Date('Date Of Deposit Payment')
    method_of_payment=fields.Char('Method Of Payment')
    pending_docs=fields.Text('Pending Documents')
    financial_aid_provided=fields.Boolean('Financial Aid Approved')
    financial_aid_provided_reason=fields.Char('Why?')
    payment_plan=fields.Boolean('Payment Plan')
    payment_plan_reason = fields.Char('Why?')
    police_clearance=fields.Boolean('Police Clearance')
    police_clearance_reason = fields.Char('Why?')
    health_immunization_record=fields.Boolean('Health Immunization Record')
    health_immunization_record_reason = fields.Char('Why?')
    date_of_enrollment=fields.Date('Date Of Enrollment')
    reason_of_delay=fields.Text('The Reason Of The Delay')
    delay_date=fields.Date('Delay Date')
    new_start_date=fields.Date('New Start Date')
    lost_reason=fields.Text('Reason')
    lost_date=fields.Date('Date')
    app_id = fields.Char('Application ID')
    form_no = fields.Char('Inquiry Form Number')
    x_funding = fields.Selection([('3', 'Family'),
                                  ('1', 'OSAP'),
                                  ('2', 'Self Funded'),
                                  ('5', 'Second Career'),
                                  ('6', 'WSIB'),
                                  ('7', 'Registered Retiremnet Saving Paln RRSP'),
                                  ('8', 'Registered Education Saving Paln RRSP'),
                                  ('9', 'Out of Province Funding'),
                                  ('4', 'Bank Loan'),
                                  ('10', 'Other')], string='Funding Source')

    form_page_url=fields.Char()
    select_button = fields.Selection([('domestic_student', 'Domestic Student'),
                                      ('international_student', 'International Student'),
                                      ('registered_agent', 'Registered Agent')], 'Student Type')
    stage_id_name = fields.Char(related='stage_id.name', readonly=True, store=True)
    marital_status=fields.Char('Marital Status')
    dependent_children=fields.Char('Do You Have Any Dependent Children?')
    mode_of_contact=fields.Selection([('asked_question','Request Information'),('requested_catalog','Requested Catalog'),('book_a_tour','Book A Tour'),('apply_now','Apply Now'),('call','Call'),('walk_in','Walk In')],'Mode Of Contact')
    new_lead=fields.Boolean('New Lead',default=True)
    unit_apt = fields.Char()

    occupation = fields.Char('Occupation')

    residency_status = fields.Selection([('canadian_citizen', 'Canadian Citizen'),
                                         ('permanent_resident', 'Permanent Resident'),
                                         ('refugee', 'Refugee'),
                                         ('visitor', 'Visitor'),
                                         ('other', 'Other')], 'Residency Status')

    residency_status_specify = fields.Char()

    highest_qualification = fields.Selection([('high_school', 'High School'),
                                              ('college', 'College'),
                                              ('university', 'University')], 'Highest Qualification')

    field_of_study = fields.Char()
    lead_rating = fields.Char('Lead Rating',readonly=True)
    closing_date = fields.Date('Joining Date')
    knowledge_of_computers = fields.Selection([('none', 'None'),
                                               ('fair', 'Fair'),
                                            ('average', 'Average'),
                                            ('good', 'Good'),
                                            ('excellent', 'Excellent')], 'Knowledge of Computers')

    knowledge_of_english = fields.Selection([('fair', 'Fair'),
                                          ('average', 'Average'),
                                          ('good', 'Good'),
                                          ('excellent', 'Excellent')], 'Knowledge of English')

    course_time_preference_first = fields.Selection([
                                                     ('full_time_am', 'Full Time(AM)'),
                                                     ('full_time_pm', 'Full Time(PM)'),
                                                     ('part_time_am', 'Part Time(AM)'),
                                                     ('part_time_pm', 'Part Time(PM)'),
                                                     ('weekends', 'Weekends')], ' First Priority ')

    course_time_preference_second = fields.Selection([
                                                      ('full_time_am', 'Full Time(AM)'),
                                                      ('full_time_pm', 'Full Time(PM)'),
                                                      ('part_time_am', 'Part Time(AM)'),
                                                      ('part_time_pm', 'Part Time(PM)'),
                                                      ('weekends', 'Weekends')], ' Second Priority')

    program_id = fields.Many2one('product.product', 'Which Program/Course are you applying ')

    referral_name = fields.Char()
    referral_phone = fields.Char()

    google = fields.Boolean('Google')
    facebook = fields.Boolean('Facebook')
    radio = fields.Boolean('Radio')
    tv = fields.Boolean('TV')
    jobfair = fields.Boolean('Job Fair')
    newspaper = fields.Boolean('Newspaper')
    iddocids = fields.One2many('crm.lead.iddocs', 'crm_lead_id', 'Identification Documents')

    hear_about_newspaper = fields.Char()

    other_hear = fields.Boolean('Other')

    hear_about_other = fields.Char()

    name_as_passport = fields.Char('Passport Name')

    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')], 'Gender')

    dob = fields.Date('Date of Birth')

    nationality = fields.Char()

    apply_check = fields.Selection([('yes', 'Yes'),
                                    ('no', 'No')], 'Apply before or Not ')
    student_id = fields.Char()

    same_as_above = fields.Boolean('Same as Above')
    curr_street_name = fields.Char('Address')
    curr_unit_apt = fields.Char()
    curr_city_id = fields.Char('City')
    curr_state_id = fields.Many2one("res.country.state", string='')
    curr_country_id = fields.Many2one('res.country', string='Country')
    curr_home_telephone_number = fields.Char('Phone No')
    curr_postal_code = fields.Char()
    curr_cell_number = fields.Char('Mobile No')

    program_id_1 = fields.Many2one('product.product', string='1st Choice')
    start_date_1 = fields.Char('Start Date 1')

    program_id_2 = fields.Many2one('product.product', string='2nd Choice')
    start_date_2 = fields.Char('Start Date 2')

    program_id_3 = fields.Many2one('product.product', string='3rd Choice')
    start_date_3 = fields.Char('Start Date 3')

    ref_education = fields.One2many('crm.lead.educational.background', 'education_back', 'Educational Background')
    merged_lead_ids=fields.One2many('merged.crm.leads','crm_lead_id','Merged Leads')
    from_year = fields.Char()
    to_year = fields.Char()
    institution_name = fields.Char('Name of Institution')
    qualifications = fields.Char('Qualification')
    file = fields.Char('File To Upload')

    eng_lang_test_name = fields.Selection([('ielts', 'IELTS'),
                                           ('tofel', 'TOFEL')], 'Select Test Name')

    eng_lang_date_taken = fields.Date()
    eng_lang_total_score = fields.Float('Total Score')
    eng_lang_city = fields.Char()
    eng_lang_country = fields.Char('Country')
    eng_score_doc_id = fields.Char('Score Report')



    photograph_id = fields.Char('Color Scan Photo')

    declaration = fields.Boolean()

    declaration_name = fields.Char()

    agency_name = fields.Char('Agency Name')
    agent_name = fields.Many2one('res.partner','Agent Name')
    agent_email = fields.Char('Agent Email')
    agent_home_number = fields.Char('Phone Number')
    agent_id = fields.Char('Agent ID')

    student_message =fields.Text('Message')
    country_residence = fields.Many2one('res.country', string='Country')
    # street_name=fields.Char()
    # unit_apt=fields.Char()
    # country_id=fields.Char()
    # state_id=fields.Char()
    # city_id=fields.Char()
    # postal_code=fields.Char()
    # home_telephone_number=fields.Char()
    # cell_number=fields.Char()


    # add new fields by hasan
    source_url = fields.Selection([('website', 'Website'),
                                   ('call', 'Call'),
                                   ('walk_in', 'Walk In')],
                                  string='source')
    form_filled = fields.Selection([('asked_question', 'Request Information'),
                                    ('requested_catalog', 'Requested Catelog'),
                                    ('book_a_tour', 'Book A Tour'),
                                    ('apply_now', 'Apply Now')],
                                   string='Form Filled')

    program_line_ids = fields.One2many('multi.program.details','program_id', string="Program")
    academic_requirements = fields.Boolean(string="academic requirements")

    assessment_test = fields.Boolean(string="assessment test")
    # seat_deposit = fields.Boolean(string="seat deposit")
    support_academic_document = fields.Boolean(string="Support Academic Required")
    assessment_test_completed = fields.Boolean(string="Assessment Test Completed")
    seat_deposit_completed = fields.Boolean(string="Seat Deposit Completed")
    agreement_signed = fields.Boolean(string="Agreement Signed")
    other_requirements = fields.Many2one('other.requirement', 'Other Requirement')
    checkbox = fields.Boolean('Checkbox')
    # upload_attachment_ids = fields.One2many('ir.attachment','upload_attachment_id', string='Upload Documents')
    disqualified = fields.Boolean('Disqualified')
    rating = fields.Selection([('hot','Hot'),
                               ('warm', 'Warm'),
                               ('cold', 'Cold')],
                              string="Rating")
    checked =fields.Boolean(string="Checked")
    note_ids = fields.One2many('crm.note', 'note_id', 'Note ')
    issue_ids = fields.One2many('crm.issue', 'issue_id', 'Issue')
    # ends here


    # pass value in program:many2one field on crm_lead
    @api.multi
    def oppor_inter_program(self):
        team_id = self.env['crm.team'].search([('name','=','International Sales')])
        lead_ids = self.env['crm.lead'].search([('type','=','opportunity'),('team_id','=',team_id.id)])
        logger.info("-----------lead_ids---length---------%s" % len(lead_ids))
        count = 1
        for lead_id in lead_ids:
            logger.info("-----------count------------%s" % count)
            count += 1
            if lead_id.program_1.id and lead_id.program_2.id and lead_id.program_3.id:
                lead_id.write({'program':lead_id.program_1.id})

            elif lead_id.program_1.id and lead_id.program_2.id and not lead_id.program_3.id:
                lead_id.write({'program': lead_id.program_1.id})
            elif lead_id.program_1.id and not lead_id.program_2.id and not lead_id.program_3.id:
                lead_id.write({'program': lead_id.program_1.id})

            elif not lead_id.program_1.id and lead_id.program_2.id and not lead_id.program_3.id:
                lead_id.write({'program': lead_id.program_2.id})
            elif not lead_id.program_1.id and lead_id.program_2.id and lead_id.program_3.id:
                lead_id.write({'program': lead_id.program_2.id})

            elif not lead_id.program_1.id and not lead_id.program_2.id and lead_id.program_3.id:
                lead_id.write({'program': lead_id.program_3.id})

        return True


    # pass value in program:one2many field on crm_lead
    @api.multi
    def oppor_inter_program_multi(self):
        multi_pro_obj = self.env['multi.program.details']
        team_id = self.env['crm.team'].search([('name', '=', 'International Sales')])
        lead_ids = self.env['crm.lead'].search([('type', '=', 'opportunity'), ('team_id', '=', team_id.id)])
        logger.info("-----------lead_ids---length---------%s" % len(lead_ids))
        count = 1
        for lead_id in lead_ids:
            logger.info("-----------count------------%s" % count)
            count += 1
            program_1, program_2, program_3 = False, False, False

            if lead_id.program_1.id and lead_id.program_2.id and lead_id.program_3.id:
                program_1 = True

            elif lead_id.program_1.id and lead_id.program_2.id and not lead_id.program_3.id:
                program_1 = True
            elif lead_id.program_1.id and not lead_id.program_2.id and not lead_id.program_3.id:
                program_1 = True

            elif not lead_id.program_1.id and lead_id.program_2.id and not lead_id.program_3.id:
                program_2 = True
            elif not lead_id.program_1.id and lead_id.program_2.id and lead_id.program_3.id:
                program_2 = True

            elif not lead_id.program_1.id and not lead_id.program_2.id and lead_id.program_3.id:
                program_3 = True


            if lead_id.program_1:
                check = False
                if program_1:
                    check = True
                multi_pro_id_1 = multi_pro_obj.create({
                    'program_ids': lead_id.program_1.id,
                    'start_date': lead_id.start_date_1,
                    'program_id': lead_id.id,
                    'checkbox': check,
                })
            if lead_id.program_2:
                check = False
                if program_2:
                    check = True
                multi_pro_id_2 = multi_pro_obj.create({
                    'program_ids': lead_id.program_2.id,
                    'start_date': lead_id.start_date_2,
                    'program_id': lead_id.id,
                    'checkbox': check,
                })
            if lead_id.program_3:
                check = False
                if program_3:
                    check = True
                multi_pro_id_3 = multi_pro_obj.create({
                    'program_ids': lead_id.program_3.id,
                    'start_date': lead_id.start_date_3,
                    'program_id': lead_id.id,
                    'checkbox': check,
                })

        return True


    # update_selection_field on crm_lead
    @api.multi
    def update_selection_field(self):
        lead_ids = self.env['crm.lead'].search([])
        logger.info("-----------lead_ids---length---------%s" % len(lead_ids))
        count = 1
        for lead_id in lead_ids:
            logger.info("-----------count------------%s" % count)
            count += 1
            if lead_id.mode_of_contact == 'call':
                lead_id.write({'source_url':lead_id.mode_of_contact})
            elif lead_id.mode_of_contact == 'walk_in':
                lead_id.write({'source_url': lead_id.mode_of_contact})

            elif lead_id.mode_of_contact == 'asked_question':
                lead_id.write({
                    'source_url': 'website',
                    'form_filled': lead_id.mode_of_contact,
                })
            elif lead_id.mode_of_contact == 'requested_catalog':
                lead_id.write({
                    'source_url': 'website',
                    'form_filled': lead_id.mode_of_contact,
                })
            elif lead_id.mode_of_contact == 'book_a_tour':
                lead_id.write({
                    'source_url': 'website',
                    'form_filled': lead_id.mode_of_contact,
                })
            elif lead_id.mode_of_contact == 'apply_now':
                lead_id.write({
                    'source_url': 'website',
                    'form_filled': lead_id.mode_of_contact,
                })

        return True




    def mark_as_read(self):
        self.write({'new_lead':False})





    @api.onchange('same_as_above')
    def change_address(self):
        if self.same_as_above:
            self.curr_street_name=self.street
            self.curr_city_id=self.city
            self.curr_state_id=self.state_id
            self.curr_unit_apt=self.unit_apt
            self.curr_postal_code=self.zip
            self.curr_country_id=self.country_id
            self.curr_cell_number=self.mobile
            self.curr_home_telephone_number=self.phone
        else:
            self.curr_street_name=''
            self.curr_city_id = ''
            self.curr_state_id = ''
            self.curr_unit_apt = ''
            self.curr_postal_code = ''
            self.curr_country_id = ''
            self.curr_cell_number = ''
            self.curr_home_telephone_number = ''

    # @api.model
    # def create_agent_catalog(self, args):
    #     try:
    #         logger.info("=====7====----------------------------------------------------------------%s" % args)
    #         vals = {
    #             'name': args['first_name'] + " " + args['last_name'],
    #             'contact_name': args['first_name'] + " " + args['last_name'],
    #             'email_from': args['email'],
    #             'new_lead':True,
    #             'mode_of_contact':'requested_catalog',
    #         }
    #
    #         if args.get('program_id', False):
    #             if args['program_id']['program_id']:
    #                 args['program_id']['program_name'] = jQ(args['program_id']['program_name']).text()
    #                 program_obj = self.env['program.details'].search(
    #                     [('name', '=', args['program_id']['program_name'])])
    #                 if not program_obj:
    #                     program_obj = self.env['program.details'].create({'name': args['program_id']['program_name'],
    #                                                                       'internal_ref': args['program_id']['program_short_name']})
    #                 vals.update({'program':program_obj.id})
    #
    #         if args.get('form_page_url',False):
    #             vals.update({'form_page_url': args['form_page_url']})
    #
    #         if args.get('phone_number', False):
    #             vals.update({'phone': args['phone_number']})
    #
    #         # if args.get('student_type_int', False):
    #         #     if args['student_type_int'] == '1':
    #         #         vals.update({'select_button': 'international_student'})
    #         #     else:
    #         #         vals.update({'select_button': 'domestic_student'})
    #
    #         if args.get('student_type_int', False):
    #             if args['student_type_int'] == '1':
    #                 team_id = self.env['crm.team'].search([('name', 'ilike', 'international')])
    #                 if team_id:
    #                     vals.update({'team_id': team_id.id})
    #                 user_id = self.env['res.users'].search([('name', '=', 'Elaine Gate')])
    #                 if user_id:
    #                     vals.update({'user_id': user_id.id})
    #                 vals.update({'select_button': 'international_student'})
    #             else:
    #                 team_id = self.env['crm.team'].search([('name', 'ilike', 'local')])
    #                 if team_id:
    #                     vals.update({'team_id': team_id.id})
    #                 user_id = self.env['res.users'].search([('name', '=', 'Sana Hasni')])
    #                 if user_id:
    #                     vals.update({'user_id': user_id.id})
    #                 vals.update({'select_button': 'domestic_student'})
    #
    #         catalog_obj = self.env['crm.lead'].create(vals)
    #         result = {'status': 'success', 'id': catalog_obj.id}
    #         return json.dumps(result)
    #     except Exception as e:
    #         result = {'status': 'failure', 'error': str(e)}
    #         return json.dumps(result)

    @api.model
    def create_agent_catalog(self, args):
        list=[]
        try:
            logger.info("=====7====----------------------------------------------------------------%s" % args)
            vals = {
                'name': args['first_name'] + " " + args['last_name'],
                'contact_name': args['first_name'] + " " + args['last_name'],
                'email_from': args['email'],
                'new_lead': True,
                'form_filled': 'requested_catalog',
            }

            # if args.get('program_id', False):
            #     if args['program_id']['program_id']:
            #         args['program_id']['program_name'] = jQ(args['program_id']['program_name']).text()
            #         program_obj = self.env['program.details'].search(
            #             [('name', '=', args['program_id']['program_name'])])
            #         if not program_obj:
            #             program_obj = self.env['program.details'].create({'name': args['program_id']['program_name'],
            #                                                               'internal_ref': args['program_id'][
            #                                                                   'program_short_name']})

            if args.get('program_id', False):
                if args['program_id']['program_id']:
                    args['program_id']['program_name'] = jQ(args['program_id']['program_name']).text()
                    program_obj1 = self.env['program.details'].search(
                        [('name', '=', args['program_id']['program_name'])])
                    if not program_obj1:
                        program_obj1 = self.env['program.details'].create(
                            {'name': args['program_id']['program_name'],
                             'internal_ref': args['program_id'][
                                 'program_short_name']})
                    list.append(
                        {'program_ids': program_obj1.id,'checkbox': True})





            if args.get('form_page_url', False):
                vals.update({'form_page_url': args['form_page_url']})

            if args.get('phone_number', False):
                vals.update({'phone': args['phone_number']})

            # if args.get('student_type_int', False):
            #     if args['student_type_int'] == '1':
            #         vals.update({'select_button': 'international_student'})
            #     else:
            #         vals.update({'select_button': 'domestic_student'})

            if args.get('student_type_int', False):
                if args['student_type_int'] == '1':
                    team_id = self.env['crm.team'].search([('name', 'ilike', 'international')])
                    if team_id:
                        vals.update({'team_id': team_id.id})
                    user_id = self.env['res.users'].search([('name', '=', 'Elaine Gate')])
                    if user_id:
                        vals.update({'user_id': user_id.id})
                    vals.update({'select_button': 'international_student'})
                else:
                    team_id = self.env['crm.team'].search([('name', 'ilike', 'local')])
                    if team_id:
                        vals.update({'team_id': team_id.id})
                    user_id = self.env['res.users'].search([('name', '=', 'Sana Hasni')])
                    if user_id:
                        vals.update({'user_id': user_id.id})
                    vals.update({'select_button': 'domestic_student'})

            catalog_obj = self.env['crm.lead'].create(vals)
            for rec in list:
                catalog_obj.write({'program_line_ids': [(0, 0, rec)]})
            catalog_obj.write({'program': program_obj1.id})
            result = {'status': 'success', 'id': catalog_obj.id}
            return json.dumps(result)
        except Exception as e:
            result = {'status': 'failure', 'error': str(e)}
            return json.dumps(result)

    # @api.model
    # def create_domestic_stu(self, args):
    #     try:
    #         vals = {'name': args['first_name'] + " " + args['last_name'],
    #                 'contact_name': args['first_name'] + " " + args['last_name'],
    #                 'zip': args['postal_code'],
    #                 'email_from': args['email'],
    #                 'phone': args['phone_number'],
    #                 'occupation': args['occupation'],
    #                 'street': args['street_name'],
    #                 'field_of_study': args['field_of_study'],
    #                 'knowledge_of_computers': args['knowledge_of_computers'].lower(),
    #                 'knowledge_of_english': args['knowledge_of_english'].lower(),
    #                 'select_button': 'domestic_student',
    #                 'city': args['city_id']['city_name'],
    #                 'new_lead':True,
    #                 'mode_of_contact':'apply_now',
    #         }
    #
    #         if args.get('form_page_url',False):
    #             vals.update({'form_page_url': args['form_page_url']})
    #
    #         if args.get('unit_apt',False):
    #             vals.update({'unit_apt': args['unit_apt']})
    #
    #         if args.get('residency_status',False):
    #             if args['residency_status']=='Permanent Resident':
    #                 vals.update({'residency_status': 'permanent_resident'})
    #             elif args['residency_status']=='Canadian Citizen':
    #                 vals.update({'residency_status': 'canadian_citizen'})
    #             elif args['residency_status']=='Refugee':
    #                 vals.update({'residency_status': 'refugee'})
    #             elif args['residency_status']=='Visitor':
    #                 vals.update({'residency_status': 'visitor'})
    #             else:
    #                 if args['residency_status_specify']:
    #                     vals.update({'residency_status_specify':args['residency_status_specify']})
    #                 vals.update({'residency_status': 'other'})
    #
    #         team_id = self.env['crm.team'].search([('name', 'ilike', 'domestic')])
    #         if team_id:
    #             vals.update({'team_id': team_id.id})
    #         user_id = self.env['res.users'].search([('name', '=', 'Sana Hasni')])
    #         if user_id:
    #             vals.update({'user_id': user_id.id})
    #
    #         if args.get('highest_qualification',False):
    #             if args['highest_qualification']=='High School':
    #                 vals.update({'highest_qualification': 'high_school'})
    #             elif args['highest_qualification']=='College':
    #                 vals.update({'highest_qualification': 'college'})
    #             elif args['highest_qualification']=='University':
    #                 vals.update({'highest_qualification': 'university'})
    #             else:
    #                 pass
    #
    #
    #         if args.get('referral_name',False):
    #             vals.update({'referral_name': args['referral_name']})
    #
    #         if args.get('referral_phone',False):
    #             vals.update({'referral_phone': args['referral_phone']})
    #
    #         if args.get('course_time_preference_first',False):
    #             if 'Full Time (AM)' in args['course_time_preference_first']:
    #                 vals.update({'course_time_preference_first': 'full_time_am'})
    #             elif 'Full Time (PM)' in args['course_time_preference_first']:
    #                 vals.update({'course_time_preference_first': 'full_time_pm'})
    #             elif 'Part Time(AM)' in args['course_time_preference_first']:
    #                 vals.update({'course_time_preference_first': 'part_time_am'})
    #             elif 'Part Time(PM)' in args['course_time_preference_first']:
    #                 vals.update({'course_time_preference_first': 'part_time_pm'})
    #             elif 'Weekends' in args['course_time_preference_first']:
    #                 vals.update({'course_time_preference_first': 'weekends'})
    #             else:
    #                 pass
    #
    #         if args.get('course_time_preference_second',False):
    #             if 'Full Time (AM)' in args['course_time_preference_second']:
    #                 vals.update({'course_time_preference_second': 'full_time_am'})
    #             elif 'Full Time (PM)' in args['course_time_preference_second']:
    #                 vals.update({'course_time_preference_second': 'full_time_pm'})
    #             elif 'Part Time(AM)' in args['course_time_preference_second']:
    #                 vals.update({'course_time_preference_second': 'part_time_am'})
    #             elif 'Part Time(PM)' in args['course_time_preference_second']:
    #                 vals.update({'course_time_preference_second ': 'part_time_pm'})
    #             elif 'Weekends' in args['course_time_preference_second']:
    #                 vals.update({'course_time_preference_second ': 'weekends'})
    #             else:
    #                 pass
    #
    #         if args.get('hear_about_us',False):
    #             for rec in args['hear_about_us'].split(','):
    #                 hear_about_us = rec.lower()
    #                 if hear_about_us == 'google':
    #                     vals.update({'google': True})
    #                 if hear_about_us == 'facebook':
    #                     vals.update({'facebook': True})
    #                 if hear_about_us == 'radio':
    #                     vals.update({'radio': True})
    #                 if hear_about_us == 'Television Commercial':
    #                     vals.update({'tv': True})
    #                 if hear_about_us == 'job fair':
    #                     vals.update({'jobfair': True})
    #                 if hear_about_us == 'newspaper':
    #                     vals.update({'newspaper': True})
    #                     if args.get('hear_about_newspaper',False):
    #                         vals.update({'hear_about_newspaper': args['hear_about_newspaper']})
    #                 if hear_about_us == 'other':
    #                     vals.update({'other_hear': True})
    #                     if args.get('hear_about_other',False):
    #                         vals.update({'hear_about_other': args['hear_about_other']})
    #
    #         if args.get('province',False):
    #             if args['province']['province_name']:
    #                 state_obj = self.env['res.country.state'].search([('name', '=', args['province']['province_name'])])
    #                 country_id = self.env['res.country'].search([('name', '=', 'Canada')]).id
    #                 if not state_obj:
    #                     state_obj = self.env['res.country.state'].create({'name': args['province']['province_name'],
    #                                                                        'code':args['province']['province_id']
    #                                                                        ,'country_id': country_id})
    #                 vals.update({'state_id': state_obj.id, 'country_id': country_id})
    #
    #         if args.get('program_id',False):
    #             if args['program_id']['program_id']:
    #
    #                 args['program_id']['program_name']= jQ( args['program_id']['program_name']).text()
    #
    #                 program_obj = self.env['program.details'].search(
    #                     [('name', '=', args['program_id']['program_name'])])
    #                 if not program_obj:
    #                     program_obj = self.env['program.details'].create({'name': args['program_id']['program_name'],
    #                                                                       'internal_ref': args['program_id']['program_short_name']})
    #                 vals.update({'program':program_obj.id})
    #
    #         crm_lead_obj = self.env['crm.lead'].create(vals)
    #
    #         # lead2oppurtunity_obj = self.env['crm.lead2opportunity.partner'].create({'name': 'convert', 'opportunity_ids': [(6, 0, [crm_lead_obj.id])], 'user_id': user_id.id, 'team_id': team_id.id})
    #         # context={'from_website':True,'active_ids':crm_lead_obj.id}
    #         # res=lead2oppurtunity_obj.with_context(context).action_apply()
    #         result = {'status': 'success', 'id': crm_lead_obj.id}
    #         return json.dumps(result)
    #
    #     except Exception as e:
    #         result = {'status': 'failure', 'error': str(e)}
    #         return json.dumps(result)

    @api.model
    def create_domestic_stu(self, args):
        print("valsss")
        list=[]
        try:
            vals = {'name': args['first_name'] + " " + args['last_name'],
                    'contact_name': args['first_name'] + " " + args['last_name'],
                    'zip': args['postal_code'],
                    'email_from': args['email'],
                    'phone': args['phone_number'],
                    'occupation': args['occupation'],
                    'street': args['street_name'],
                    'field_of_study': args['field_of_study'],
                    'knowledge_of_computers': args['knowledge_of_computers'].lower(),
                    'knowledge_of_english': args['knowledge_of_english'].lower(),
                    'select_button': 'domestic_student',
                    'city': args['city_id']['city_name'],
                    'new_lead': True,
                    'form_filled': 'apply_now',
                    }

            if args.get('form_page_url', False):
                vals.update({'form_page_url': args['form_page_url']})

            if args.get('unit_apt', False):
                vals.update({'unit_apt': args['unit_apt']})

            if args.get('residency_status', False):
                if args['residency_status'] == 'Permanent Resident':
                    vals.update({'residency_status': 'permanent_resident'})
                elif args['residency_status'] == 'Canadian Citizen':
                    vals.update({'residency_status': 'canadian_citizen'})
                elif args['residency_status'] == 'Refugee':
                    vals.update({'residency_status': 'refugee'})
                elif args['residency_status'] == 'Visitor':
                    vals.update({'residency_status': 'visitor'})
                else:
                    if args['residency_status_specify']:
                        vals.update({'residency_status_specify': args['residency_status_specify']})
                    vals.update({'residency_status': 'other'})

            team_id = self.env['crm.team'].search([('name', 'ilike', 'domestic')])
            if team_id:
                vals.update({'team_id': team_id.id})
            user_id = self.env['res.users'].search([('name', '=', 'Sana Hasni')])
            if user_id:
                vals.update({'user_id': user_id.id})

            if args.get('highest_qualification', False):
                if args['highest_qualification'] == 'High School':
                    vals.update({'highest_qualification': 'high_school'})
                elif args['highest_qualification'] == 'College':
                    vals.update({'highest_qualification': 'college'})
                elif args['highest_qualification'] == 'University':
                    vals.update({'highest_qualification': 'university'})
                else:
                    pass

            if args.get('referral_name', False):
                vals.update({'referral_name': args['referral_name']})

            if args.get('referral_phone', False):
                vals.update({'referral_phone': args['referral_phone']})

            if args.get('course_time_preference_first', False):
                if 'Full Time (AM)' in args['course_time_preference_first']:
                    vals.update({'course_time_preference_first': 'full_time_am'})
                elif 'Full Time (PM)' in args['course_time_preference_first']:
                    vals.update({'course_time_preference_first': 'full_time_pm'})
                elif 'Part Time(AM)' in args['course_time_preference_first']:
                    vals.update({'course_time_preference_first': 'part_time_am'})
                elif 'Part Time(PM)' in args['course_time_preference_first']:
                    vals.update({'course_time_preference_first': 'part_time_pm'})
                elif 'Weekends' in args['course_time_preference_first']:
                    vals.update({'course_time_preference_first': 'weekends'})
                else:
                    pass

            if args.get('course_time_preference_second', False):
                if 'Full Time (AM)' in args['course_time_preference_second']:
                    vals.update({'course_time_preference_second': 'full_time_am'})
                elif 'Full Time (PM)' in args['course_time_preference_second']:
                    vals.update({'course_time_preference_second': 'full_time_pm'})
                elif 'Part Time(AM)' in args['course_time_preference_second']:
                    vals.update({'course_time_preference_second': 'part_time_am'})
                elif 'Part Time(PM)' in args['course_time_preference_second']:
                    vals.update({'course_time_preference_second ': 'part_time_pm'})
                elif 'Weekends' in args['course_time_preference_second']:
                    vals.update({'course_time_preference_second ': 'weekends'})
                else:
                    pass

            if args.get('hear_about_us', False):
                for rec in args['hear_about_us'].split(','):
                    hear_about_us = rec.lower()
                    if hear_about_us == 'google':
                        vals.update({'google': True})
                    if hear_about_us == 'facebook':
                        vals.update({'facebook': True})
                    if hear_about_us == 'radio':
                        vals.update({'radio': True})
                    if hear_about_us == 'Television Commercial':
                        vals.update({'tv': True})
                    if hear_about_us == 'job fair':
                        vals.update({'jobfair': True})
                    if hear_about_us == 'newspaper':
                        vals.update({'newspaper': True})
                        if args.get('hear_about_newspaper', False):
                            vals.update({'hear_about_newspaper': args['hear_about_newspaper']})
                    if hear_about_us == 'other':
                        vals.update({'other_hear': True})
                        if args.get('hear_about_other', False):
                            vals.update({'hear_about_other': args['hear_about_other']})

            if args.get('province', False):
                if args['province']['province_name']:
                    state_obj = self.env['res.country.state'].search([('name', '=', args['province']['province_name'])])
                    country_id = self.env['res.country'].search([('name', '=', 'Canada')]).id
                    if not state_obj:
                        state_obj = self.env['res.country.state'].create({'name': args['province']['province_name'],
                                                                          'code': args['province']['province_id']
                                                                             , 'country_id': country_id})
                    vals.update({'state_id': state_obj.id, 'country_id': country_id})

            # if args.get('program_id', False):
            #     if args['program_id']['program_id']:
            #         program_obj = self.env['program.details'].search(
            #             [('internal_ref', '=', args['program_id']['program_short_name'])])
            # if args.get('program_id', False):
            #     if args['program_id']['program_id']:
            #         args['program_id']['program_name']= jQ( args['program_id']['program_name']).text()
            #         program_obj = self.env['program.details'].search(
            #             [('name', '=', args['program_id']['program_name'])])
            #         if not program_obj:
            #             program_obj = self.env['program.details'].create({'name': args['program_id']['program_name'],
            #                                                               'internal_ref': args['program_id'][
            #                                                                   'program_short_name']})

            if args.get('program_id', False):
                if args['program_id']['program_id']:
                    args['program_id']['program_name'] = jQ(args['program_id']['program_name']).text()
                    program_obj1 = self.env['program.details'].search(
                        [('name', '=', args['program_id']['program_name'])])
                    if not program_obj1:
                        program_obj1 = self.env['program.details'].create(
                            {'name': args['program_id']['program_name'],
                             'internal_ref': args['program_id'][
                                 'program_short_name']})
                    list.append(
                        {'program_ids': program_obj1.id,'checkbox': True})


            crm_lead_obj = self.env['crm.lead'].create(vals)
            for rec in list:
                crm_lead_obj.write({'program_line_ids': [(0, 0, rec)]})
            crm_lead_obj.write({'program': program_obj1.id})

            # lead2oppurtunity_obj = self.env['crm.lead2opportunity.partner'].create({'name': 'convert', 'opportunity_ids': [(6, 0, [crm_lead_obj.id])], 'user_id': user_id.id, 'team_id': team_id.id})
            # context={'from_website':True,'active_ids':crm_lead_obj.id}
            # res=lead2oppurtunity_obj.with_context(context).action_apply()
            result = {'status': 'success', 'id': crm_lead_obj.id}
            return json.dumps(result)

        except Exception as e:
            result = {'status': 'failure', 'error': str(e)}
            return json.dumps(result)

    # @api.model
    # def create_int_stu(self, args):
    #     try:
    #         vals = {
    #             'name': args['first_name'] + " " + args['last_name'],
    #             'contact_name': args['first_name'] + " " + args['last_name'],
    #             'name_as_passport': args['name_as_passport'],
    #             'gender': args['gender'].lower(),
    #             'email_from': args['email'],
    #             'nationality': args['nationality'],
    #             'street': args['street_name'],
    #             'zip': args['postal_code'],
    #             'phone': args['home_telephone_number'],
    #             'mobile': args['cell_number'],
    #             'curr_street_name': args['curr_street_name'],
    #             'curr_postal_code': args['curr_postal_code'],
    #             'curr_home_telephone_number': args['curr_home_telephone_number'],
    #             'curr_cell_number': args['curr_cell_number'],
    #             'start_date_1': args['start_date_1'],
    #             'start_date_2': args['start_date_2'],
    #             'start_date_3': args['start_date_3'],
    #             'knowledge_of_computers': args['knowledge_of_computers'].lower(),
    #             'knowledge_of_english': args['knowledge_of_english'].lower(),
    #             'select_button': 'international_student',
    #             'new_lead':True,
    #             'mode_of_contact':'apply_now',
    #         }
    #
    #         if args.get('applied_before',False):
    #             if args['applied_before']=='1':
    #                 vals.update({'apply_check':'yes'})
    #             else:
    #                 vals.update({'apply_check': 'no'})
    #
    #         if args.get('form_page_url',False):
    #             vals.update({'form_page_url': args['form_page_url']})
    #
    #         if args.get('student_id',False):
    #             vals.update({'student_id': args['student_id']})
    #
    #         if args.get('unit_apt', False):
    #             vals.update({'unit_apt': args['unit_apt']})
    #
    #         if args.get('curr_unit_apt', False):
    #             vals.update({'curr_unit_apt': args['curr_unit_apt']})
    #
    #         if args.get('dob',False):
    #             dob=datetime.strptime(args['dob'],'%Y-%m-%d')
    #             vals.update({'dob':dob})
    #
    #         if args.get('eng_lang_total_score',False):
    #             vals.update({'eng_lang_total_score': args['eng_lang_total_score']})
    #
    #         if args.get('eng_lang_city',False):
    #             vals.update({'eng_lang_city': args['eng_lang_city']})
    #
    #         if args.get('eng_lang_country',False):
    #             vals.update({'eng_lang_country': args['eng_lang_country']})
    #
    #
    #         team_id = self.env['crm.team'].search([('name', 'ilike', 'international')])
    #         if team_id:
    #             vals.update({'team_id': team_id.id})
    #         user_id = self.env['res.users'].search([('name', '=', 'Elaine Gate')])
    #         if user_id:
    #             vals.update({'user_id': user_id.id})
    #
    #         if args.get('agent_name',False):
    #             agent_obj=self.env['res.partner'].search([('name','=',args['agent_name'])],limit=1)
    #             if not agent_obj:
    #                 agent_obj=self.env['res.partner'].create({'name':args['agent_name'],'select_button':True})
    #             vals.update({'agent_name':agent_obj.id})
    #
    #         if args.get('agent_id',False):
    #             vals.update({'agent_id': args['agent_id']})
    #
    #         if args.get('eng_lang_date_taken',False):
    #             if args['eng_lang_date_taken']:
    #                 date_taken=datetime.strptime(args['eng_lang_date_taken'],'%Y-%m-%d')
    #                 vals.update({'eng_lang_date_taken': date_taken})
    #
    #         if args.get('same_as_above',False):
    #             if args['same_as_above'] == '1':
    #                 vals.update({'same_as_above':True})
    # # country Residence
    #         if args.get('country_residence',False):
    #             if args['country_residence']['country_name']:
    #                 country_resid = self.env['res.country'].search([('name', '=', args['country_residence']['country_name'])])
    #                 if not country_resid:
    #                     country_resid = self.env['res.country'].create({'name': args['country_residence']['country_name'],
    #                                                                    'code':args['country_residence']['country_id']})
    #                 vals.update({'country_residence': country_resid.id})
    #
    # # Main Country and State, City
    #
    #         if args.get('country_id',False):
    #             if args['country_id']['country_name']:
    #                 country_obj = self.env['res.country'].search([('name', '=', args['country_id']['country_name'])])
    #                 if not country_obj:
    #                     country_obj = self.env['res.country'].create({'name':args['country_id']['country_name'],
    #                                                                    'code': args['country_id']['country_id']})
    #                 vals.update({'country_id': country_obj.id,})
    #                 if args.get('state_id',False):
    #                     if args['state_id']['state_name']:
    #                         state_obj = self.env['res.country.state'].search([('name', '=', args['state_id']['state_name'])])
    #                         if not state_obj:
    #                             state_obj = self.env['res.country.state'].create({'name':args['state_id']['state_name'],
    #                                                                                'code':args['state_id']['state_id'],
    #                                                                                'country_id':country_obj.id})
    #                         vals.update({'state_id': state_obj.id})
    #
    #         if args.get('city_id',False):
    #             if args['city_id']['city_name']:
    #                 vals.update({'city': args['city_id']['city_name']})
    #
    # # Curren# Current Country And State
    #         if args.get('curr_country_id',False):
    #             if args['curr_country_id']['country_name']:
    #                 country_obj1 = self.env['res.country'].search(
    #                     [('name', '=', args['curr_country_id']['country_name'])])
    #                 if not country_obj1:
    #                     country_obj1 = self.env['res.country'].create(
    #                         {'name':args['curr_country_id']['country_name'],
    #                           'code':args['curr_country_id']['country_id']})
    #                 vals.update({'curr_country_id': country_obj1.id, })
    #                 if args.get('curr_state_id',False):
    #                     if args['curr_state_id']['state_name']:
    #                         state_obj1 = self.env['res.country.state'].search(
    #                             [('name', '=', args['curr_state_id']['state_name'])])
    #                         if not state_obj1:
    #                             state_obj1 = self.env['res.country.state'].create(
    #                                 {'name':args['curr_state_id']['state_name'],
    #                                   'code':args['curr_state_id']['state_id'],
    #                                   'country_id':country_obj1.id})
    #                         vals.update({'curr_state_id': state_obj1.id})
    #
    #         if args.get('curr_city_id',False):
    #             if args['curr_city_id']['city_name']:
    #                 vals.update({'curr_city_id': args['curr_city_id']['city_name']})
    #
    # # Program Id 1
    #         if args.get('program_id_1',False):
    #             if args['program_id_1']['program_name']:
    #                 args['program_id_1']['program_name'] = jQ(args['program_id_1']['program_name']).text()
    #                 program_obj1 = self.env['program.details'].search([('name', '=', args['program_id_1']['program_name'])])
    #                 if not program_obj1:
    #                     program_obj1 = self.env['program.details'].create({'name': args['program_id_1']['program_name'],
    #                                                                                    'internal_ref': args['program_id_1']['program_short_name']})
    #                 vals.update({'program_1':program_obj1.id})
    # # Program Id 2
    #         if args.get('program_id_2',False):
    #             if args['program_id_2']['program_name']:
    #                 args['program_id_2']['program_name'] = jQ(args['program_id_2']['program_name']).text()
    #                 program_obj2 = self.env['program.details'].search([('name', '=', args['program_id_2']['program_name'])])
    #                 if not program_obj2:
    #                     program_obj2 = self.env['program.details'].create({'name': args['program_id_2']['program_name'],
    #                                                                                    'internal_ref': args['program_id_2']['program_short_name']})
    #                 vals.update({'program_2':program_obj2.id})
    #
    # # Program Id 3
    #         if args.get('program_id_3',False):
    #             if args['program_id_3']['program_name']:
    #                 args['program_id_3']['program_name'] = jQ(args['program_id_3']['program_name']).text()
    #                 program_obj3 = self.env['program.details'].search([('name', '=', args['program_id_3']['program_name'])])
    #                 if not program_obj3:
    #                     program_obj3 = self.env['program.details'].create({'name': args['program_id_3']['program_name'],
    #                                                                                    'internal_ref': args['program_id_3']['program_short_name']})
    #                 vals.update({'program_3':program_obj3.id})
    #
    #
    #         if args.get('eng_lang_test_name',False):
    #             if args['eng_lang_test_name']=='IELTS':
    #                 vals.update({'eng_lang_test_name': 'ielts'})
    #             elif args['eng_lang_test_name']=='TOFEL':
    #                 vals.update({'eng_lang_test_name': 'tofel'})
    #             else:
    #                 pass
    #
    #
    #         if args.get('hear_about_us',False):
    #             for rec in args['hear_about_us'].split(','):
    #                 hear_about_us = rec.lower()
    #                 if hear_about_us == 'google':
    #                     vals.update({'google': True})
    #                 if hear_about_us == 'facebook':
    #                     vals.update({'facebook': True})
    #                 if hear_about_us == 'radio':
    #                     vals.update({'radio': True})
    #                 if hear_about_us == 'Television Commercial':
    #                     vals.update({'tv': True})
    #                 if hear_about_us == 'job fair':
    #                     vals.update({'jobfair': True})
    #                 if hear_about_us == 'newspaper':
    #                     vals.update({'newspaper': True})
    #                 if args.get('hear_about_newspaper',False):
    #                     vals.update({'hear_about_newspaper': args['hear_about_newspaper']})
    #                 if hear_about_us == 'other':
    #                     vals.update({'other_hear': True})
    #                     if args.get('hear_about_other',False):
    #                         vals.update({'hear_about_other': args['hear_about_other']})
    #
    #
    #         if args.get('eng_score_doc_id',False):
    #             if args['eng_score_doc_id']:
    #                 if args['eng_score_doc_id']['file_url']:
    #                     vals.update({'eng_score_doc_id': args['eng_score_doc_id']['file_url']})
    #
    #
    #
    #
    #         if args.get('photograph_id',False):
    #             if args['photograph_id']:
    #                 if args['photograph_id']['file_url']:
    #                     vals.update({'photograph_id': args['photograph_id']['file_url']})
    #
    #         international_stud = self.env['crm.lead'].create(vals)
    #
    #         if args.get('identification_doc_id',False):
    #             for rec in args['identification_doc_id']:
    #                 doc_vals={
    #                     'identification_doc_id':rec['file_url'],
    #                     'crm_lead_id':international_stud.id
    #                 }
    #                 self.env['crm.lead.iddocs'].create(doc_vals)
    #
    #         if args.get('educational_background',False):
    #             for line in args['educational_background']:
    #                 vals1 = {
    #
    #                         'education_back': international_stud.id,
    #                         'from_year': line['from_year'],
    #                         'to_year': line['to_year'],
    #                         'institution_name': line['institution_name'],
    #                         'qualifications': line['qualifications'],
    #                     }
    #                 educational_background = self.env['crm.lead.educational.background'].create(vals1)
    #                 for rec in line['edu_image_id']:
    #                     file_vals={
    #                         'file':rec['file_url'],
    #                         'crm_lead_edu_back_id':educational_background.id
    #                     }
    #                     self.env['crm.lead.edu.files'].create(file_vals)
    #
    #         # lead2oppurtunity_obj = self.env['crm.lead2opportunity.partner'].create(
    #         #     {'name': 'convert', 'opportunity_ids': [(6, 0, [international_stud.id])], 'user_id': user_id.id,
    #         #      'team_id': team_id.id})
    #         # context = {'from_website': True, 'active_ids': international_stud.id}
    #         # res = lead2oppurtunity_obj.with_context(context).action_apply()
    #         result = {'status': 'success', 'id': international_stud.id}
    #         return json.dumps(result)
    #     except Exception as e:
    #         result = {'status': 'failure', 'error': str(e)}
    #         return json.dumps(result)

    @api.model
    def create_int_stu(self, args):
        list = []
        try:

            vals = {
                'name': args['first_name'] + " " + args['last_name'],
                'contact_name': args['first_name'] + " " + args['last_name'],
                'name_as_passport': args['name_as_passport'],
                'gender': args['gender'].lower(),
                'email_from': args['email'],
                'nationality': args['nationality'],
                'street': args['street_name'],
                'zip': args['postal_code'],
                'phone': args['home_telephone_number'],
                'mobile': args['cell_number'],
                'curr_street_name': args['curr_street_name'],
                'curr_postal_code': args['curr_postal_code'],
                'curr_home_telephone_number': args['curr_home_telephone_number'],
                'curr_cell_number': args['curr_cell_number'],
                # 'start_date': args['start_date_1'],
                # 'start_date': args['start_date_2'],
                # 'start_date': args['start_date_3'],
                'knowledge_of_computers': args['knowledge_of_computers'].lower(),
                'knowledge_of_english': args['knowledge_of_english'].lower(),
                'select_button': 'international_student',
                'new_lead': True,
                'form_filled': 'apply_now',
            }

            if args.get('applied_before', False):
                if args['applied_before'] == '1':
                    vals.update({'apply_check': 'yes'})
                else:
                    vals.update({'apply_check': 'no'})

            if args.get('form_page_url', False):
                vals.update({'form_page_url': args['form_page_url']})

            if args.get('student_id', False):
                vals.update({'student_id': args['student_id']})

            if args.get('unit_apt', False):
                vals.update({'unit_apt': args['unit_apt']})

            if args.get('curr_unit_apt', False):
                vals.update({'curr_unit_apt': args['curr_unit_apt']})

            if args.get('dob', False):
                dob = datetime.strptime(args['dob'], '%Y-%m-%d')
                vals.update({'dob': dob})

            if args.get('eng_lang_total_score', False):
                vals.update({'eng_lang_total_score': args['eng_lang_total_score']})

            if args.get('eng_lang_city', False):
                vals.update({'eng_lang_city': args['eng_lang_city']})

            if args.get('eng_lang_country', False):
                vals.update({'eng_lang_country': args['eng_lang_country']})

            team_id = self.env['crm.team'].search([('name', 'ilike', 'international')])
            if team_id:
                vals.update({'team_id': team_id.id})
            user_id = self.env['res.users'].search([('name', '=', 'Elaine Gate')])
            if user_id:
                vals.update({'user_id': user_id.id})

            if args.get('agent_name', False):
                agent_obj = self.env['res.partner'].search([('name', '=', args['agent_name'])], limit=1)
                if not agent_obj:
                    agent_obj = self.env['res.partner'].create({'name': args['agent_name'], 'select_button': True})
                vals.update({'agent_name': agent_obj.id})

            if args.get('agent_id', False):
                vals.update({'agent_id': args['agent_id']})

            if args.get('eng_lang_date_taken', False):
                if args['eng_lang_date_taken']:
                    date_taken = datetime.strptime(args['eng_lang_date_taken'], '%Y-%m-%d')
                    vals.update({'eng_lang_date_taken': date_taken})

            if args.get('same_as_above', False):
                if args['same_as_above'] == '1':
                    vals.update({'same_as_above': True})
            # country Residence
            if args.get('country_residence', False):
                if args['country_residence']['country_name']:
                    country_resid = self.env['res.country'].search(
                        [('name', '=', args['country_residence']['country_name'])])
                    if not country_resid:
                        country_resid = self.env['res.country'].create(
                            {'name': args['country_residence']['country_name'],
                             'code': args['country_residence']['country_id']})
                    vals.update({'country_residence': country_resid.id})

            # Main Country and State, City

            if args.get('country_id', False):
                if args['country_id']['country_name']:
                    country_obj = self.env['res.country'].search([('name', '=', args['country_id']['country_name'])])
                    if not country_obj:
                        country_obj = self.env['res.country'].create({'name': args['country_id']['country_name'],
                                                                      'code': args['country_id']['country_id']})
                    vals.update({'country_id': country_obj.id, })
                    if args.get('state_id', False):
                        if args['state_id']['state_name']:
                            state_obj = self.env['res.country.state'].search(
                                [('name', '=', args['state_id']['state_name'])])
                            if not state_obj:
                                state_obj = self.env['res.country.state'].create(
                                    {'name': args['state_id']['state_name'],
                                     'code': args['state_id']['state_id'],
                                     'country_id': country_obj.id})
                            vals.update({'state_id': state_obj.id})

            if args.get('city_id', False):
                if args['city_id']['city_name']:
                    vals.update({'city': args['city_id']['city_name']})

            # Curren# Current Country And State
            if args.get('curr_country_id', False):
                if args['curr_country_id']['country_name']:
                    country_obj1 = self.env['res.country'].search(
                        [('name', '=', args['curr_country_id']['country_name'])])
                    if not country_obj1:
                        country_obj1 = self.env['res.country'].create(
                            {'name': args['curr_country_id']['country_name'],
                             'code': args['curr_country_id']['country_id']})
                    vals.update({'curr_country_id': country_obj1.id, })
                    if args.get('curr_state_id', False):
                        if args['curr_state_id']['state_name']:
                            state_obj1 = self.env['res.country.state'].search(
                                [('name', '=', args['curr_state_id']['state_name'])])
                            if not state_obj1:
                                state_obj1 = self.env['res.country.state'].create(
                                    {'name': args['curr_state_id']['state_name'],
                                     'code': args['curr_state_id']['state_id'],
                                     'country_id': country_obj1.id})
                            vals.update({'curr_state_id': state_obj1.id})

            if args.get('curr_city_id', False):
                if args['curr_city_id']['city_name']:
                    vals.update({'curr_city_id': args['curr_city_id']['city_name']})

            # Program Id 1
            # if args.get('program_id_1', False):
            #     if args['program_id_1']['program_name']:
            #         program_obj1 = self.env['program.details'].search(
            #             [('internal_ref', '=', args['program_id_1']['program_short_name'])])
            if args.get('program_id_1', False):
                if args['program_id_1']['program_name']:
                    args['program_id_1']['program_name'] = jQ(args['program_id_1']['program_name']).text()
                    program_obj1 = self.env['program.details'].search([('name', '=', args['program_id_1']['program_name'])])
                    if not program_obj1:
                        program_obj1 = self.env['program.details'].create({'name': args['program_id_1']['program_name'],
                                                                           'internal_ref': args['program_id_1'][
                                                                               'program_short_name']})
                    list.append(
                        {'program_ids': program_obj1.id, 'start_date': args['start_date_1'], 'checkbox': True})
            # Program Id 2
            if args.get('program_id_2', False):
                if args['program_id_2']['program_name']:
                    args['program_id_2']['program_name'] = jQ(args['program_id_2']['program_name']).text()
                    program_obj2 = self.env['program.details'].search([('name', '=', args['program_id_2']['program_name'])])
                    if not program_obj2:
                        program_obj2 = self.env['program.details'].create({'name': args['program_id_2']['program_name'],
                                                                           'internal_ref': args['program_id_2'][
                                                                               'program_short_name']})
                    list.append({'program_ids': program_obj2.id, 'start_date': args['start_date_2']})

            # Program Id 3
            if args.get('program_id_3', False):
                if args['program_id_3']['program_name']:
                    args['program_id_3']['program_name'] = jQ(args['program_id_3']['program_name']).text()
                    program_obj3 = self.env['program.details'].search([('name', '=', args['program_id_3']['program_name'])])
                    if not program_obj3:
                        program_obj3 = self.env['program.details'].create({'name': args['program_id_3']['program_name'],
                                                                           'internal_ref': args['program_id_3'][
                                                                               'program_short_name']})
                    list.append({'program_ids': program_obj3.id, 'start_date': args['start_date_3']})

            if args.get('eng_lang_test_name', False):
                if args['eng_lang_test_name'] == 'IELTS':
                    vals.update({'eng_lang_test_name': 'ielts'})
                elif args['eng_lang_test_name'] == 'TOFEL':
                    vals.update({'eng_lang_test_name': 'tofel'})
                else:
                    pass

            if args.get('hear_about_us', False):
                for rec in args['hear_about_us'].split(','):
                    hear_about_us = rec.lower()
                    if hear_about_us == 'google':
                        vals.update({'google': True})
                    if hear_about_us == 'facebook':
                        vals.update({'facebook': True})
                    if hear_about_us == 'radio':
                        vals.update({'radio': True})
                    if hear_about_us == 'Television Commercial':
                        vals.update({'tv': True})
                    if hear_about_us == 'job fair':
                        vals.update({'jobfair': True})
                    if hear_about_us == 'newspaper':
                        vals.update({'newspaper': True})
                    if args.get('hear_about_newspaper', False):
                        vals.update({'hear_about_newspaper': args['hear_about_newspaper']})
                    if hear_about_us == 'other':
                        vals.update({'other_hear': True})
                        if args.get('hear_about_other', False):
                            vals.update({'hear_about_other': args['hear_about_other']})

            if args.get('eng_score_doc_id', False):
                if args['eng_score_doc_id']:
                    if args['eng_score_doc_id']['file_url']:
                        vals.update({'eng_score_doc_id': args['eng_score_doc_id']['file_url']})

            if args.get('photograph_id', False):
                if args['photograph_id']:
                    if args['photograph_id']['file_url']:
                        vals.update({'photograph_id': args['photograph_id']['file_url']})

            international_stud = self.env['crm.lead'].create(vals)

            if args.get('identification_doc_id', False):
                for rec in args['identification_doc_id']:
                    doc_vals = {
                        'identification_doc_id': rec['file_url'],
                        'crm_lead_id': international_stud.id
                    }
                    self.env['crm.lead.iddocs'].create(doc_vals)

            if args.get('educational_background', False):
                for line in args['educational_background']:
                    vals1 = {

                        'education_back': international_stud.id,
                        'from_year': line['from_year'],
                        'to_year': line['to_year'],
                        'institution_name': line['institution_name'],
                        'qualifications': line['qualifications'],
                    }
                    educational_background = self.env['crm.lead.educational.background'].create(vals1)
                    for rec in line['edu_image_id']:
                        file_vals = {
                            'file': rec['file_url'],
                            'crm_lead_edu_back_id': educational_background.id
                        }
                        self.env['crm.lead.edu.files'].create(file_vals)

            # lead2oppurtunity_obj = self.env['crm.lead2opportunity.partner'].create(
            #     {'name': 'convert', 'opportunity_ids': [(6, 0, [international_stud.id])], 'user_id': user_id.id,
            #      'team_id': team_id.id})
            # context = {'from_website': True, 'active_ids': international_stud.id}
            # res = lead2oppurtunity_obj.with_context(context).action_apply()
            for rec in list:
                international_stud.write({'program_line_ids': [(0, 0, rec)]})
            international_stud.write({'program': program_obj1.id})
            result = {'status': 'success', 'id': international_stud.id}
            return json.dumps(result)
        except Exception as e:
            result = {'status': 'failure', 'error': str(e)}
            return json.dumps(result)

    # @api.model
    # def create_register_agent(self, args):
    #     try:
    #         vals = {
    #             'name':  args['first_name'] +' '+ args['last_name'],
    #             'contact_name': args['first_name'] +' '+ args['last_name'],
    #             'name_as_passport': args['name_as_passport'],
    #             'gender': args['gender'].lower(),
    #             'email_from': args['email'],
    #             'nationality': args['nationality'],
    #             'street': args['street_name'],
    #             'zip': args['postal_code'],
    #             'phone': args['home_telephone_number'],
    #             'mobile': args['cell_number'],
    #             'curr_street_name': args['curr_street_name'],
    #             'curr_postal_code': args['curr_postal_code'],
    #             'curr_home_telephone_number': args['curr_home_telephone_number'],
    #             'curr_cell_number': args['curr_cell_number'],
    #             'start_date_1': args['start_date_1'],
    #             'start_date_2': args['start_date_2'],
    #             'start_date_3': args['start_date_3'],
    #             'knowledge_of_computers': args['knowledge_of_computers'].lower(),
    #             'knowledge_of_english': args['knowledge_of_english'].lower(),
    #             'select_button': 'registered_agent',
    #             'new_lead':True,
    #             'mode_of_contact':'apply_now'
    #         }
    #
    #         if args.get('applied_before',False):
    #             if args['applied_before']=='1':
    #                 vals.update({'apply_check':'yes'})
    #             else:
    #                 vals.update({'apply_check': 'no'})
    #
    #         if args.get('student_id', False):
    #             vals.update({'student_id': args['student_id']})
    #
    #         if args.get('contact_name',False):
    #             agent_obj=self.env['res.partner'].search([('name','=',args['contact_name'])],limit=1)
    #             if not agent_obj:
    #                 agent_obj=self.env['res.partner'].create({'name':args['contact_name'],'select_button':True,'agency_name':args['agency_name'],'email':args['contact_email'],'phone':args['contact_home_number']})
    #             vals.update({'agent_name':agent_obj.id})
    #
    #         if args.get('eng_lang_total_score',False):
    #             vals.update({'eng_lang_total_score': args['eng_lang_total_score']})
    #
    #         if args.get('eng_lang_city',False):
    #             vals.update({'eng_lang_city': args['eng_lang_city']})
    #
    #         if args.get('eng_lang_country',False):
    #             vals.update({'eng_lang_country': args['eng_lang_country']})
    #
    #         if args['dob']:
    #             dob=datetime.strptime(args['dob'],'%Y-%m-%d')
    #             vals.update({'dob':dob})
    #
    #
    #         if args.get('unit_apt', False):
    #             vals.update({'unit_apt': args['unit_apt']})
    #
    #         if args.get('curr_unit_apt', False):
    #             vals.update({'curr_unit_apt': args['curr_unit_apt']})
    #
    #         team_id = self.env['crm.team'].search([('name', 'ilike', 'international')])
    #         if team_id:
    #             vals.update({'team_id': team_id.id})
    #         user_id = self.env['res.users'].search([('name', '=', 'Elaine Gate')])
    #         if user_id:
    #             vals.update({'user_id': user_id.id})
    #
    #         if args.get('eng_lang_date_taken',False):
    #             if args['eng_lang_date_taken']:
    #                 date_taken=datetime.strptime(args['eng_lang_date_taken'],'%Y-%m-%d')
    #                 vals.update({'eng_lang_date_taken': date_taken})
    #
    #         if args.get('same_as_above',False):
    #             if args['same_as_above'] == '1':
    #                 vals.update({'same_as_above':True})
    # # country Residence
    #         if args.get('country_residence',False):
    #             if args['country_residence']['country_name']:
    #                 country_resid = self.env['res.country'].search([('name', '=', args['country_residence']['country_name'])])
    #                 if not country_resid:
    #                     country_resid = self.env['res.country'].create({'name':args['country_residence']['country_name'],
    #                                                                    'code':args['country_residence']['country_id']})
    #                 vals.update({'country_residence': country_resid.id,})
    #
    # # Main Country and State, City
    #
    #         if args.get('country_id',False):
    #             if args['country_id']['country_name']:
    #                 country_obj = self.env['res.country'].search([('name', '=', args['country_id']['country_name']),],limit=1)
    #                 if not country_obj:
    #                     country_obj = self.env['res.country'].create({'name': args['country_id']['country_name'],
    #                                                                    'code':args['country_id']['country_id']})
    #                 vals.update({'country_id': country_obj.id,})
    #                 if args.get('state_id',False):
    #                     if args['state_id']['state_name']:
    #                         state_obj = self.env['res.country.state'].search([('name', '=', args['state_id']['state_name'])])
    #                         if not state_obj:
    #                             state_obj = self.env['res.country.state'].create({'name':args['state_id']['state_name'],
    #                                                                                'code':args['state_id']['state_id'],
    #                                                                                'country_id':country_obj.id})
    #                         vals.update({'state_id': state_obj.id})
    #         if args.get('city_id',False):
    #             if args['city_id']['city_name']:
    #                 vals.update({'city': args['city_id']['city_name']})
    #
    # # Curren# Current Country And State
    #         if args.get('curr_country_id',False):
    #             if args['curr_country_id']['country_name']:
    #                 country_obj1 = self.env['res.country'].search(
    #                     [('name', '=', args['curr_country_id']['country_name'])])
    #                 if not country_obj1:
    #                     country_obj1 = self.env['res.country'].create(
    #                         {'name':args['curr_country_id']['country_name'],
    #                           'code':args['curr_country_id']['country_id']})
    #                 vals.update({'curr_country_id': country_obj1.id, })
    #                 if args.get('curr_state_id',False):
    #                     if args['curr_state_id']['state_name']:
    #                         state_obj1 = self.env['res.country.state'].search(
    #                             [('name', '=', args['curr_state_id']['state_name'])])
    #                         if not state_obj1:
    #                             state_obj1 = self.env['res.country.state'].create(
    #                                 {'name':args['curr_state_id']['state_name'],
    #                                   'code':args['curr_state_id']['state_id'],
    #                                   'country_id':country_obj1.id})
    #                         vals.update({'curr_state_id': state_obj1.id})
    #
    #         if args.get('curr_city_id',False):
    #             if args['curr_city_id']['city_name']:
    #                 vals.update({'curr_city_id': args['curr_city_id']['city_name']})
    #
    # # Program Id 1
    #         if args.get('program_id_1',False):
    #             if args['program_id_1']['program_name']:
    #                 args['program_id_1']['program_name'] = jQ(args['program_id_1']['program_name']).text()
    #                 program_obj1 = self.env['program.details'].search([('name', '=', args['program_id_1']['program_name'])])
    #                 if not program_obj1:
    #                     program_obj1 = self.env['program.details'].create({'name': args['program_id_1']['program_name'],
    #                                                                                    'internal_ref': args['program_id_1']['program_short_name']})
    #                 vals.update({'program_1':program_obj1.id})
    # # Program Id 2
    #         if args.get('program_id_2',False):
    #             if args['program_id_2']['program_name']:
    #                 args['program_id_2']['program_name'] = jQ(args['program_id_2']['program_name']).text()
    #                 program_obj2 = self.env['program.details'].search([('name', '=', args['program_id_2']['program_name'])])
    #                 if not program_obj2:
    #                     program_obj2 = self.env['program.details'].create({'name': args['program_id_2']['program_name'],
    #                                                                                    'internal_ref': args['program_id_2']['program_short_name']})
    #                 vals.update({'program_2':program_obj2.id})
    #
    # # Program Id 3
    #         if args.get('program_id_3',False):
    #             if args['program_id_3']['program_name']:
    #                 args['program_id_3']['program_name'] = jQ(args['program_id_3']['program_name']).text()
    #                 program_obj3 = self.env['program.details'].search([('name', '=', args['program_id_3']['program_name'])])
    #                 if not program_obj3:
    #                     program_obj3 = self.env['program.details'].create({'name': args['program_id_3']['program_name'],
    #                                                                                    'internal_ref': args['program_id_3']['program_short_name']})
    #                 vals.update({'program_3':program_obj3.id})
    #
    #
    #         if args.get('eng_lang_test_name',False):
    #             if args['eng_lang_test_name']=='IELTS':
    #                 vals.update({'eng_lang_test_name': 'ielts'})
    #             elif args['eng_lang_test_name']=='TOFEL':
    #                 vals.update({'eng_lang_test_name': 'tofel'})
    #             else:
    #                 pass
    #
    #         if args.get('hear_about_us',False):
    #             for rec in args['hear_about_us'].split(','):
    #                 hear_about_us = rec.lower()
    #                 if hear_about_us == 'google':
    #                     vals.update({'google': True})
    #                 if hear_about_us == 'facebook':
    #                     vals.update({'facebook': True})
    #                 if hear_about_us == 'radio':
    #                     vals.update({'radio': True})
    #                 if hear_about_us == 'Television Commercial':
    #                     vals.update({'tv': True})
    #                 if hear_about_us == 'job fair':
    #                     vals.update({'jobfair': True})
    #                 if hear_about_us == 'newspaper':
    #                     vals.update({'newspaper': True})
    #                 if args.get('hear_about_newspaper',False):
    #                     vals.update({'hear_about_newspaper': args['hear_about_newspaper']})
    #                 if hear_about_us == 'other':
    #                     vals.update({'other_hear': True})
    #                     if args.get('hear_about_other',False):
    #                         vals.update({'hear_about_other': args['hear_about_other']})
    #
    #
    #         if args.get('eng_score_doc_id',False):
    #             if args['eng_score_doc_id']:
    #                 if args['eng_score_doc_id']['file_url']:
    #                     vals.update({'eng_score_doc_id': args['eng_score_doc_id']['file_url']})
    #
    #         logger.info("=====8====----------------------------------------------------------------")
    #
    #         if args.get('form_page_url',False):
    #             vals.update({'form_page_url': args['form_page_url']})
    #
    #         if args.get('photograph_id',False):
    #             if args['photograph_id']:
    #                 if args['photograph_id']['file_url']:
    #                     vals.update({'photograph_id': args['photograph_id']['file_url']})
    #
    #         international_stud = self.env['crm.lead'].create(vals)
    #
    #         if args.get('identification_doc_id',False):
    #             for rec in args['identification_doc_id']:
    #                 doc_vals={
    #                     'identification_doc_id':rec['file_url'],
    #                     'crm_lead_id':international_stud.id
    #                 }
    #                 self.env['crm.lead.iddocs'].create(doc_vals)
    #         logger.info("=====9====----------------------------------------------------------------")
    #         if args.get('educational_background',False):
    #             for line in args['educational_background']:
    #                 vals1 = {
    #
    #                         'education_back': international_stud.id,
    #                         'from_year': line['from_year'],
    #                         'to_year': line['to_year'],
    #                         'institution_name': line['institution_name'],
    #                         'qualifications': line['qualifications'],
    #                     }
    #                 educational_background = self.env['crm.lead.educational.background'].create(vals1)
    #                 for rec in line['edu_image_id']:
    #                     file_vals={
    #                         'file':rec['file_url'],
    #                         'crm_lead_edu_back_id':educational_background.id
    #                     }
    #                     self.env['crm.lead.edu.files'].create(file_vals)
    #         logger.info("=====10====----------------------------------------------------------------")
    #         # lead2oppurtunity_obj = self.env['crm.lead2opportunity.partner'].create(
    #         #     {'name': 'convert', 'opportunity_ids': [(6, 0, [international_stud.id])], 'user_id': user_id.id,
    #         #      'team_id': team_id.id})
    #         # context = {'from_website': True, 'active_ids': international_stud.id}
    #         # res = lead2oppurtunity_obj.with_context(context).action_apply()
    #         result = {'status': 'success', 'id': international_stud.id}
    #         return json.dumps(result)
    #     except Exception as e:
    #         result = {'status': 'failure', 'error': str(e)}
    #         return json.dumps(result)

    @api.model
    def create_register_agent(self, args):
        list = []
        try:
            vals = {
                'name': args['first_name'] + ' ' + args['last_name'],
                'contact_name': args['first_name'] + ' ' + args['last_name'],
                'name_as_passport': args['name_as_passport'],
                'gender': args['gender'].lower(),
                'email_from': args['email'],
                'nationality': args['nationality'],
                'street': args['street_name'],
                'zip': args['postal_code'],
                'phone': args['home_telephone_number'],
                'mobile': args['cell_number'],
                'curr_street_name': args['curr_street_name'],
                'curr_postal_code': args['curr_postal_code'],
                'curr_home_telephone_number': args['curr_home_telephone_number'],
                'curr_cell_number': args['curr_cell_number'],
                # 'start_date_1': args['start_date_1'],
                # 'start_date_2': args['start_date_2'],
                # 'start_date_3': args['start_date_3'],
                'knowledge_of_computers': args['knowledge_of_computers'].lower(),
                'knowledge_of_english': args['knowledge_of_english'].lower(),
                'select_button': 'registered_agent',
                'new_lead': True,
                'form_filled': 'apply_now'
            }

            if args.get('applied_before', False):
                if args['applied_before'] == '1':
                    vals.update({'apply_check': 'yes'})
                else:
                    vals.update({'apply_check': 'no'})

            if args.get('student_id', False):
                vals.update({'student_id': args['student_id']})

            if args.get('contact_name', False):
                agent_obj = self.env['res.partner'].search([('name', '=', args['contact_name'])], limit=1)
                if not agent_obj:
                    agent_obj = self.env['res.partner'].create(
                        {'name': args['contact_name'], 'select_button': True, 'agency_name': args['agency_name'],
                         'email': args['contact_email'], 'phone': args['contact_home_number']})
                vals.update({'agent_name': agent_obj.id})

            if args.get('eng_lang_total_score', False):
                vals.update({'eng_lang_total_score': args['eng_lang_total_score']})

            if args.get('eng_lang_city', False):
                vals.update({'eng_lang_city': args['eng_lang_city']})

            if args.get('eng_lang_country', False):
                vals.update({'eng_lang_country': args['eng_lang_country']})

            if args['dob']:
                dob = datetime.strptime(args['dob'], '%Y-%m-%d')
                vals.update({'dob': dob})

            if args.get('unit_apt', False):
                vals.update({'unit_apt': args['unit_apt']})

            if args.get('curr_unit_apt', False):
                vals.update({'curr_unit_apt': args['curr_unit_apt']})

            team_id = self.env['crm.team'].search([('name', 'ilike', 'international')])
            if team_id:
                vals.update({'team_id': team_id.id})
            user_id = self.env['res.users'].search([('name', '=', 'Elaine Gate')])
            if user_id:
                vals.update({'user_id': user_id.id})

            if args.get('eng_lang_date_taken', False):
                if args['eng_lang_date_taken']:
                    date_taken = datetime.strptime(args['eng_lang_date_taken'], '%Y-%m-%d')
                    vals.update({'eng_lang_date_taken': date_taken})

            if args.get('same_as_above', False):
                if args['same_as_above'] == '1':
                    vals.update({'same_as_above': True})
            # country Residence
            if args.get('country_residence', False):
                if args['country_residence']['country_name']:
                    country_resid = self.env['res.country'].search(
                        [('name', '=', args['country_residence']['country_name'])])
                    if not country_resid:
                        country_resid = self.env['res.country'].create(
                            {'name': args['country_residence']['country_name'],
                             'code': args['country_residence']['country_id']})
                    vals.update({'country_residence': country_resid.id, })

            # Main Country and State, City

            if args.get('country_id', False):
                if args['country_id']['country_name']:
                    country_obj = self.env['res.country'].search([('name', '=', args['country_id']['country_name']), ],
                                                                 limit=1)
                    if not country_obj:
                        country_obj = self.env['res.country'].create({'name': args['country_id']['country_name'],
                                                                      'code': args['country_id']['country_id']})
                    vals.update({'country_id': country_obj.id, })
                    if args.get('state_id', False):
                        if args['state_id']['state_name']:
                            state_obj = self.env['res.country.state'].search(
                                [('name', '=', args['state_id']['state_name'])])
                            if not state_obj:
                                state_obj = self.env['res.country.state'].create(
                                    {'name': args['state_id']['state_name'],
                                     'code': args['state_id']['state_id'],
                                     'country_id': country_obj.id})
                            vals.update({'state_id': state_obj.id})
            if args.get('city_id', False):
                if args['city_id']['city_name']:
                    vals.update({'city': args['city_id']['city_name']})

            # Curren# Current Country And State
            if args.get('curr_country_id', False):
                if args['curr_country_id']['country_name']:
                    country_obj1 = self.env['res.country'].search(
                        [('name', '=', args['curr_country_id']['country_name'])])
                    if not country_obj1:
                        country_obj1 = self.env['res.country'].create(
                            {'name': args['curr_country_id']['country_name'],
                             'code': args['curr_country_id']['country_id']})
                    vals.update({'curr_country_id': country_obj1.id, })
                    if args.get('curr_state_id', False):
                        if args['curr_state_id']['state_name']:
                            state_obj1 = self.env['res.country.state'].search(
                                [('name', '=', args['curr_state_id']['state_name'])])
                            if not state_obj1:
                                state_obj1 = self.env['res.country.state'].create(
                                    {'name': args['curr_state_id']['state_name'],
                                     'code': args['curr_state_id']['state_id'],
                                     'country_id': country_obj1.id})
                            vals.update({'curr_state_id': state_obj1.id})

            if args.get('curr_city_id', False):
                if args['curr_city_id']['city_name']:
                    vals.update({'curr_city_id': args['curr_city_id']['city_name']})

            # Program Id 1
            # if args.get('program_id_1', False):
            #     if args['program_id_1']['program_name']:
            #         program_obj1 = self.env['program.details'].search(
            #             [('internal_ref', '=', args['program_id_1']['program_short_name'])])
            if args.get('program_id_1', False):
                if args['program_id_1']['program_name']:
                    args['program_id_1']['program_name'] = jQ(args['program_id_1']['program_name']).text()
                    program_obj1 = self.env['program.details'].search([('name', '=', args['program_id_1']['program_name'])])
                    if not program_obj1:
                        program_obj1 = self.env['program.details'].create({'name': args['program_id_1']['program_name'],
                                                                           'internal_ref': args['program_id_1'][
                                                                               'program_short_name']})
                    list.append(
                        {'program_ids': program_obj1.id, 'start_date': args['start_date_1'], 'checkbox': True})
            # Program Id 2
            if args.get('program_id_2', False):
                if args['program_id_2']['program_name']:
                    args['program_id_2']['program_name'] = jQ(args['program_id_2']['program_name']).text()
                    program_obj2 = self.env['program.details'].search(
                        [('name', '=', args['program_id_2']['program_name'])])
                    if not program_obj2:
                        program_obj2 = self.env['program.details'].create({'name': args['program_id_2']['program_name'],
                                                                           'internal_ref': args['program_id_2'][
                                                                               'program_short_name']})
                    list.append({'program_ids': program_obj2.id, 'start_date': args['start_date_2']})

            # Program Id 3
            if args.get('program_id_3', False):
                if args['program_id_3']['program_name']:
                    args['program_id_3']['program_name'] = jQ(args['program_id_3']['program_name']).text()
                    program_obj3 = self.env['program.details'].search(
                        [('name', '=', args['program_id_3']['program_name'])])
                    if not program_obj3:
                        program_obj3 = self.env['program.details'].create({'name': args['program_id_3']['program_name'],
                                                                           'internal_ref': args['program_id_3'][
                                                                               'program_short_name']})
                    list.append({'program_ids': program_obj3.id, 'start_date': args['start_date_3']})

            if args.get('eng_lang_test_name', False):
                if args['eng_lang_test_name'] == 'IELTS':
                    vals.update({'eng_lang_test_name': 'ielts'})
                elif args['eng_lang_test_name'] == 'TOFEL':
                    vals.update({'eng_lang_test_name': 'tofel'})
                else:
                    pass

            if args.get('hear_about_us', False):
                for rec in args['hear_about_us'].split(','):
                    hear_about_us = rec.lower()
                    if hear_about_us == 'google':
                        vals.update({'google': True})
                    if hear_about_us == 'facebook':
                        vals.update({'facebook': True})
                    if hear_about_us == 'radio':
                        vals.update({'radio': True})
                    if hear_about_us == 'Television Commercial':
                        vals.update({'tv': True})
                    if hear_about_us == 'job fair':
                        vals.update({'jobfair': True})
                    if hear_about_us == 'newspaper':
                        vals.update({'newspaper': True})
                    if args.get('hear_about_newspaper', False):
                        vals.update({'hear_about_newspaper': args['hear_about_newspaper']})
                    if hear_about_us == 'other':
                        vals.update({'other_hear': True})
                        if args.get('hear_about_other', False):
                            vals.update({'hear_about_other': args['hear_about_other']})

            if args.get('eng_score_doc_id', False):
                if args['eng_score_doc_id']:
                    if args['eng_score_doc_id']['file_url']:
                        vals.update({'eng_score_doc_id': args['eng_score_doc_id']['file_url']})

            logger.info("=====8====----------------------------------------------------------------")

            if args.get('form_page_url', False):
                vals.update({'form_page_url': args['form_page_url']})

            if args.get('photograph_id', False):
                if args['photograph_id']:
                    if args['photograph_id']['file_url']:
                        vals.update({'photograph_id': args['photograph_id']['file_url']})

            international_stud = self.env['crm.lead'].create(vals)

            if args.get('identification_doc_id', False):
                for rec in args['identification_doc_id']:
                    doc_vals = {
                        'identification_doc_id': rec['file_url'],
                        'crm_lead_id': international_stud.id
                    }
                    self.env['crm.lead.iddocs'].create(doc_vals)
            logger.info("=====9====----------------------------------------------------------------")
            if args.get('educational_background', False):
                for line in args['educational_background']:
                    vals1 = {

                        'education_back': international_stud.id,
                        'from_year': line['from_year'],
                        'to_year': line['to_year'],
                        'institution_name': line['institution_name'],
                        'qualifications': line['qualifications'],
                    }
                    educational_background = self.env['crm.lead.educational.background'].create(vals1)
                    for rec in line['edu_image_id']:
                        file_vals = {
                            'file': rec['file_url'],
                            'crm_lead_edu_back_id': educational_background.id
                        }
                        self.env['crm.lead.edu.files'].create(file_vals)
            logger.info("=====10====----------------------------------------------------------------")
            # lead2oppurtunity_obj = self.env['crm.lead2opportunity.partner'].create(
            #     {'name': 'convert', 'opportunity_ids': [(6, 0, [international_stud.id])], 'user_id': user_id.id,
            #      'team_id': team_id.id})
            # context = {'from_website': True, 'active_ids': international_stud.id}
            # res = lead2oppurtunity_obj.with_context(context).action_apply()
            for rec in list:
                international_stud.write({'program_line_ids': [(0, 0, rec)]})
            international_stud.write({'program': program_obj1.id})
            result = {'status': 'success', 'id': international_stud.id}
            return json.dumps(result)
        except Exception as e:
            result = {'status': 'failure', 'error': str(e)}
            return json.dumps(result)

    def diff_month(self,d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month

    @api.onchange('closing_date')
    def get_lead_rating(self):
        if self.closing_date:
            currentdate = datetime.now()
            closingdate = datetime.strptime(self.closing_date, '%Y-%m-%d')
            difference = self.diff_month(currentdate, closingdate)
            if difference < 12:
                self.lead_rating = 'Hot'
            elif difference > 12 and difference < 24:
                self.lead_rating = 'Warm'
            else:
                self.lead_rating = 'Cold'
            return True

    @api.model
    def retrieve_sales_dashboard(self):
        """ Fetch data to setup Sales Dashboard """
        result = {
            'meeting': {
                'today': 0,
                'next_7_days': 0,
            },
            'activity': {
                'today': 0,
                'overdue': 0,
                'next_7_days': 0,
            },
            'closing': {
                'today': 0,
                'overdue': 0,
                'next_7_days': 0,
            },
            'done': {
                'this_month': 0,
                'last_month': 0,
            },
            'won': {
                'this_month': 0,
                'last_month': 0,
            },
            'international_leads': {
                'hot': 0,
                'cold': 0,
                'warm': 0,
            },
            'local_leads': {
                'hot': 0,
                'cold': 0,
                'warm': 0,
            },
            'nb_opportunities': 0,
        }

        stage_name=self.env['crm.stage'].search([('id','!=',False),('team_id','=',False)],order="id asc")

        view_id=self.env['ir.ui.view'].search([('name','=','crm.lead.form.opportunity')],limit=1).id

        opportunities_local_dict=collections.OrderedDict()
        opportunities_international_dict = collections.OrderedDict()
        for rec in stage_name:
            opportunities_local_dict.update({rec.name:0})
            opportunities_international_dict.update({rec.name: 0})
        opportunities = self.search([('type', '=', 'opportunity')])

        for opp in opportunities:
            # Expected closing
            if opp.lead_rating:
                if opp.lead_rating == 'Hot' and 'International' in opp.team_id.name:
                    result['international_leads']['hot'] += 1
                if opp.lead_rating == 'Cold' and 'International' in opp.team_id.name:
                    result['international_leads']['cold'] += 1
                if opp.lead_rating == 'Warm' and 'International' in opp.team_id.name:
                    result['international_leads']['warm'] += 1
                if opp.lead_rating == 'Hot' and 'Local' in opp.team_id.name:
                    result['local_leads']['hot'] += 1
                if opp.lead_rating == 'Cold' and 'Local' in opp.team_id.name:
                    result['local_leads']['cold'] += 1
                if opp.lead_rating == 'Warm' and 'Local' in opp.team_id.name:
                    result['local_leads']['warm'] += 1

            for rec in stage_name:
                if opp.stage_id.name and opp.team_id.name:
                    if opp.stage_id.name ==rec.name and 'Local' in opp.team_id.name:
                        opportunities_local_dict[rec.name] += 1
                        break
                    elif opp.stage_id.name ==rec.name and 'International' in opp.team_id.name:
                        opportunities_international_dict[rec.name] += 1
                        break
            #
            # if opp.date_deadline:
            #     date_deadline = fields.Date.from_string(opp.date_deadline)
            #     if date_deadline == date.today():
            #         result['closing']['today'] += 1
            #     if date.today() <= date_deadline <= date.today() + timedelta(days=7):
            #         result['closing']['next_7_days'] += 1
            #     if date_deadline < date.today() and not opp.date_closed:
            #         result['closing']['overdue'] += 1
            # # Next activities
            # if opp.next_activity_id and opp.date_action:
            #     date_action = fields.Date.from_string(opp.date_action)
            #     if date_action == date.today():
            #         result['activity']['today'] += 1
            #     if date.today() <= date_action <= date.today() + timedelta(days=7):
            #         result['activity']['next_7_days'] += 1
            #     if date_action < date.today() and not opp.date_closed:
            #         result['activity']['overdue'] += 1
            # # Won in Opportunities
            # if opp.date_closed:
            #     date_closed = fields.Date.from_string(opp.date_closed)
            #     if date.today().replace(day=1) <= date_closed <= date.today():
            #         if opp.planned_revenue:
            #             result['won']['this_month'] += opp.planned_revenue
            #     elif date.today() + relativedelta(months=-1, day=1) <= date_closed < date.today().replace(day=1):
            #         if opp.planned_revenue:
            #             result['won']['last_month'] += opp.planned_revenue

        result['nb_opportunities'] = len(opportunities)
        result.update({'opportunities_local':opportunities_local_dict,'opportunities_international':opportunities_international_dict,'local':'local_'+str(view_id),'international':'international_'+str(view_id)})
        # crm.activity is a very messy model so we need to do that in order to retrieve the actions done.
        # self._cr.execute("""
        #             SELECT
        #                 m.id,
        #                 m.subtype_id,
        #                 m.date,
        #                 l.user_id,
        #                 l.type
        #             FROM mail_message M
        #                 LEFT JOIN crm_lead L ON (M.res_id = L.id)
        #                 INNER JOIN crm_activity A ON (M.subtype_id = A.subtype_id)
        #             WHERE
        #                 (M.model = 'crm.lead') AND (L.user_id = %s) AND (L.type = 'opportunity')
        #         """, (self._uid,))
        # activites_done = self._cr.dictfetchall()

        # for activity in activites_done:
        #     if activity['date']:
        #         date_act = fields.Date.from_string(activity['date'])
        #         if date.today().replace(day=1) <= date_act <= date.today():
        #             result['done']['this_month'] += 1
        #         elif date.today() + relativedelta(months=-1, day=1) <= date_act < date.today().replace(day=1):
        #             result['done']['last_month'] += 1
        #
        # # Meetings
        # min_date = fields.Datetime.now()
        # max_date = fields.Datetime.to_string(datetime.now() + timedelta(days=8))
        # meetings_domain = [
        #     ('start', '>=', min_date),
        #     ('start', '<=', max_date),
        #     ('partner_ids', 'in', [self.env.user.partner_id.id])
        # ]
        # meetings = self.env['calendar.event'].search(meetings_domain)
        # for meeting in meetings:
        #     if meeting['start']:
        #         start = datetime.strptime(meeting['start'], tools.DEFAULT_SERVER_DATETIME_FORMAT).date()
        #         if start == date.today():
        #             result['meeting']['today'] += 1
        #         if date.today() <= start <= date.today() + timedelta(days=7):
        #             result['meeting']['next_7_days'] += 1
        #
        # result['done']['target'] = self.env.user.target_sales_done
        # result['won']['target'] = self.env.user.target_sales_won
        # result['currency_id'] = self.env.user.company_id.currency_id.id
        print result
        return result

    # @api.model
    # def create_new_agent(self, args):
    #     try:
    #         vals = {
    #             'name': args['full_name'],
    #             'email': args['email'],
    #             'phone': args['phone_number'],
    #             'worked_immigration': args['worked_immigration'],
    #             'assist_int_students': args['assist_int_students'],
    #             'designation': args['designation'],
    #             'agency_name': args['agency_name'],
    #             'agency_address': args['address'],
    #             'agency_postal_code': args['postal_code'],
    #             'agency_alt_phone_number': args['alt_phone_number'],
    #             'agency_fax_number': args['fax_number'],
    #             'website': args['website'],
    #             'year_established': args['year_established'],
    #             'business_team': args['business_team'],
    #             'ownership': args['ownership'],
    #             'contact_details': args['contact_details'],
    #             'select_button': True,
    #         }
    #
    #         if args.get('form_page_url',False):
    #             vals.update({'form_page_url': args['form_page_url']})
    #
    #         if args.get('head_office',False):
    #             vals.update({'head_office': args['head_office']})
    #
    #         if args.get('partner_sub_agencies',False):
    #             vals.update({'partner_sub_agencies': args['partner_sub_agencies']})
    #
    #         if args.get('recruit_post_secondary',False):
    #             vals.update({'recruit_post_secondary': args['recruit_post_secondary']})
    #
    #         if args.get('assist_last_year',False):
    #             vals.update({'assist_last_year': args['assist_last_year']})
    #
    #         if args.get('stu_sent_overseas',False):
    #             vals.update({'stu_sent_overseas': args['stu_sent_overseas']})
    #
    #         if args.get('country_send_stu_to',False):
    #             vals.update({'country_send_stu_to': args['country_send_stu_to']})
    #
    #         if args.get('programs_interest',False):
    #             vals.update({'programs_interest': args['programs_interest']})
    #
    #         if args.get('stu_anticipate_annually',False):
    #             vals.update({'stu_anticipate_annually': args['stu_anticipate_annually']})
    #
    #         if args.get('familiar_permit_requirements',False):
    #             vals.update({'familiar_permit_requirements': args['familiar_permit_requirements'].lower()})
    #
    #         if args.get('edu_counselling_stu',False):
    #             vals.update({'edu_counselling_stu': args['edu_counselling_stu']})
    #
    #         if args.get('stu_package_cost',False):
    #             vals.update({'stu_package_cost': args['stu_package_cost']})
    #
    #         if args.get('service_beside_recruit',False):
    #             vals.update({'service_beside_recruit': args['service_beside_recruit']})
    #
    #         if args.get('marketing_strategy',False):
    #             vals.update({'marketing_strategy': args['marketing_strategy']})
    #
    #         if args.get('hear_about_other',False):
    #             vals.update({'hear_about_other': args['hear_about_other']})
    #
    #         if args.get('hear_about_newspaper',False):
    #             vals.update({'hear_about_newspaper': args['hear_about_newspaper']})
    #         # Main Country and State, City
    #
    #         if args.get('country_id',False):
    #             if args['country_id']['country_name']:
    #                 country_obj = self.env['res.country'].search([('name', '=', args['country_id']['country_name'])])
    #                 if not country_obj:
    #                     country_obj = self.env['res.country'].create({'name': args['country_id']['country_name'],
    #                                                                    'code':args['country_id']['country_id']})
    #                 vals.update({'agency_country_id': country_obj.id, })
    #                 if args.get('state_id',False):
    #                     if args['state_id']['state_name']:
    #                         state_obj = self.env['res.country.state'].search([('name', '=', args['state_id']['state_name'])])
    #                         if not state_obj:
    #                             state_obj = self.env['res.country.state'].create({'name':args['state_id']['state_name'],
    #                                                                                'code':args['state_id']['state_id'],
    #                                                                                'country_id':country_obj.id})
    #                         vals.update({'agency_state_id': state_obj.id})
    #
    #         if args.get('city_id',False):
    #             if args['city_id']['city_name']:
    #                 vals.update({'city': args['city_id']['city_name']})
    #
    #         if args.get('service_provided',False):
    #             for rec in args['service_provided'].split(','):
    #                 hear_about_us = rec
    #                 if hear_about_us == 'Programs Counselling':
    #                     vals.update({'pro_coun': True})
    #                 if hear_about_us == 'Gathering documents':
    #                     vals.update({'gath_req': True})
    #                 if hear_about_us == 'Application preparation and Submission':
    #                     vals.update({'pre_sub': True})
    #                 if hear_about_us == 'Guiding applicant through offer':
    #                     vals.update({'gui_app': True})
    #                 if hear_about_us == 'Study permit preparation':
    #                     vals.update({'permit_pre': True})
    #                 if hear_about_us == 'Pre Departure Service':
    #                     vals.update({'pre_ser': True})
    #                 if hear_about_us == 'Identify possible funding sources, government grants':
    #                     vals.update({'sou_gov': True})
    #                 if hear_about_us == 'English as Second language (ESL) Testing':
    #                     vals.update({'esl_test': True})
    #
    #         if args.get('assistance_for_students',False):
    #             for rec in args['assistance_for_students'].split(','):
    #                 hear_about_us = rec
    #                 if hear_about_us == 'Housing':
    #                     vals.update({'housing': True})
    #                 if hear_about_us == 'Medical Insurance':
    #                     vals.update({'med_ins': True})
    #                 if hear_about_us == 'Travel Itinerary':
    #                     vals.update({'trav_iti': True})
    #                 if hear_about_us == 'Canadian Arrival':
    #                     vals.update({'can_arr': True})
    #                 if hear_about_us == 'Other services available':
    #                     vals.update({'ser_avi': True})
    #                 if args.get('other_services_available',False):
    #                     vals.update({'other_services_available': args['other_services_available']})
    #
    #         if args.get('hear_about_us',False):
    #             for rec in args['hear_about_us'].split(','):
    #                 hear_about_us = rec.lower()
    #                 if hear_about_us == 'google':
    #                     vals.update({'google': True})
    #                 if hear_about_us == 'facebook':
    #                     vals.update({'facebook': True})
    #                 if hear_about_us == 'radio':
    #                     vals.update({'radio': True})
    #                 if hear_about_us == 'Television Commercial':
    #                     vals.update({'tv': True})
    #                 if hear_about_us == 'job fair':
    #                     vals.update({'jobfair': True})
    #                 if hear_about_us == 'newspaper':
    #                     vals.update({'newspaper': True})
    #
    #                 if hear_about_us == 'other':
    #                     vals.update({'other_hear': True})
    #
    #
    #         agent_obj = self.env['res.partner'].create(vals)
    #
    #         if args.get('business_doc_id',False):
    #             for rec in args['business_doc_id']:
    #                 buss_vals = {'res_partner_id': agent_obj.id, 'business_doc_id': rec['file_url']}
    #                 self.env['res.partner.businessdocs'].create(buss_vals)
    #
    #         if args.get('extra_fields',False):
    #             for line in args['extra_fields']:
    #                 vals2 = {
    #
    #                     'agent_id': agent_obj.id,
    #                     'ref_contact_name': line['ref_contact_name'],
    #                     'ref_position': line['ref_position'],
    #                     'ref_agency': line['ref_agency'],
    #                     'ref_address': line['ref_address'],
    #                     'ref_phone_number': line['ref_phone_number'],
    #                     'ref_fax_number': line['ref_fax_number'],
    #                     'ref_website': line['ref_website'],
    #                     'ref_email': line['ref_email'],
    #                     'ref_years_known': line['ref_years_known'],
    #
    #                 }
    #                 extra_fields = self.env['res.partner.agent'].create(vals2)
    #
    #         result = {'status': 'success', 'id': agent_obj.id}
    #         return json.dumps(result)
    #     except Exception as e:
    #         result = {'status': 'failure', 'error': str(e)}
    #         return json.dumps(result)

    @api.model
    def create_new_agent(self, args):
        try:
            vals = {
                'name': args['full_name'],
                'email': args['email'],
                'phone': args['phone_number'],
                'worked_immigration': args['worked_immigration'],
                'assist_int_students': args['assist_int_students'],
                'designation': args['designation'],
                'agency_name': args['agency_name'],
                'agency_address': args['address'],
                'agency_postal_code': args['postal_code'],
                'agency_alt_phone_number': args['alt_phone_number'],
                'agency_fax_number': args['fax_number'],
                'website': args['website'],
                'year_established': args['year_established'],
                'business_team': args['business_team'],
                'ownership': args['ownership'],
                'contact_details': args['contact_details'],
                'select_button': True,
            }

            if args.get('form_page_url', False):
                vals.update({'form_page_url': args['form_page_url']})

            if args.get('head_office', False):
                vals.update({'head_office': args['head_office']})

            if args.get('partner_sub_agencies', False):
                vals.update({'partner_sub_agencies': args['partner_sub_agencies']})

            if args.get('recruit_post_secondary', False):
                vals.update({'recruit_post_secondary': args['recruit_post_secondary']})

            if args.get('assist_last_year', False):
                vals.update({'assist_last_year': args['assist_last_year']})

            if args.get('stu_sent_overseas', False):
                vals.update({'stu_sent_overseas': args['stu_sent_overseas']})

            if args.get('country_send_stu_to', False):
                vals.update({'country_send_stu_to': args['country_send_stu_to']})

            if args.get('programs_interest', False):
                vals.update({'programs_interest': args['programs_interest']})

            if args.get('stu_anticipate_annually', False):
                vals.update({'stu_anticipate_annually': args['stu_anticipate_annually']})

            if args.get('familiar_permit_requirements', False):
                vals.update({'familiar_permit_requirements': args['familiar_permit_requirements'].lower()})

            if args.get('edu_counselling_stu', False):
                vals.update({'edu_counselling_stu': args['edu_counselling_stu']})

            if args.get('stu_package_cost', False):
                vals.update({'stu_package_cost': args['stu_package_cost']})

            if args.get('service_beside_recruit', False):
                vals.update({'service_beside_recruit': args['service_beside_recruit']})

            if args.get('marketing_strategy', False):
                vals.update({'marketing_strategy': args['marketing_strategy']})

            if args.get('hear_about_other', False):
                vals.update({'hear_about_other': args['hear_about_other']})

            if args.get('hear_about_newspaper', False):
                vals.update({'hear_about_newspaper': args['hear_about_newspaper']})
            # Main Country and State, City

            if args.get('country_id', False):
                if args['country_id']['country_name']:
                    country_obj = self.env['res.country'].search([('name', '=', args['country_id']['country_name'])])
                    if not country_obj:
                        country_obj = self.env['res.country'].create({'name': args['country_id']['country_name'],
                                                                      'code': args['country_id']['country_id']})
                    vals.update({'agency_country_id': country_obj.id, })
                    if args.get('state_id', False):
                        if args['state_id']['state_name']:
                            state_obj = self.env['res.country.state'].search(
                                [('name', '=', args['state_id']['state_name'])])
                            if not state_obj:
                                state_obj = self.env['res.country.state'].create(
                                    {'name': args['state_id']['state_name'],
                                     'code': args['state_id']['state_id'],
                                     'country_id': country_obj.id})
                            vals.update({'agency_state_id': state_obj.id})

            if args.get('city_id', False):
                if args['city_id']['city_name']:
                    vals.update({'city': args['city_id']['city_name']})

            if args.get('service_provided', False):
                for rec in args['service_provided'].split(','):
                    hear_about_us = rec
                    if hear_about_us == 'Programs Counselling':
                        vals.update({'pro_coun': True})
                    if hear_about_us == 'Gathering documents':
                        vals.update({'gath_req': True})
                    if hear_about_us == 'Application preparation and Submission':
                        vals.update({'pre_sub': True})
                    if hear_about_us == 'Guiding applicant through offer':
                        vals.update({'gui_app': True})
                    if hear_about_us == 'Study permit preparation':
                        vals.update({'permit_pre': True})
                    if hear_about_us == 'Pre Departure Service':
                        vals.update({'pre_ser': True})
                    if hear_about_us == 'Identify possible funding sources, government grants':
                        vals.update({'sou_gov': True})
                    if hear_about_us == 'English as Second language (ESL) Testing':
                        vals.update({'esl_test': True})

            if args.get('assistance_for_students', False):
                for rec in args['assistance_for_students'].split(','):
                    hear_about_us = rec
                    if hear_about_us == 'Housing':
                        vals.update({'housing': True})
                    if hear_about_us == 'Medical Insurance':
                        vals.update({'med_ins': True})
                    if hear_about_us == 'Travel Itinerary':
                        vals.update({'trav_iti': True})
                    if hear_about_us == 'Canadian Arrival':
                        vals.update({'can_arr': True})
                    if hear_about_us == 'Other services available':
                        vals.update({'ser_avi': True})
                    if args.get('other_services_available', False):
                        vals.update({'other_services_available': args['other_services_available']})

            if args.get('hear_about_us', False):
                for rec in args['hear_about_us'].split(','):
                    hear_about_us = rec.lower()
                    if hear_about_us == 'google':
                        vals.update({'google': True})
                    if hear_about_us == 'facebook':
                        vals.update({'facebook': True})
                    if hear_about_us == 'radio':
                        vals.update({'radio': True})
                    if hear_about_us == 'Television Commercial':
                        vals.update({'tv': True})
                    if hear_about_us == 'job fair':
                        vals.update({'jobfair': True})
                    if hear_about_us == 'newspaper':
                        vals.update({'newspaper': True})

                    if hear_about_us == 'other':
                        vals.update({'other_hear': True})

            agent_obj = self.env['res.partner'].create(vals)

            if args.get('business_doc_id', False):
                for rec in args['business_doc_id']:
                    buss_vals = {'res_partner_id': agent_obj.id, 'business_doc_id': rec['file_url']}
                    self.env['res.partner.businessdocs'].create(buss_vals)

            if args.get('extra_fields', False):
                for line in args['extra_fields']:
                    vals2 = {

                        'agent_id': agent_obj.id,
                        'ref_contact_name': line['ref_contact_name'],
                        'ref_position': line['ref_position'],
                        'ref_agency': line['ref_agency'],
                        'ref_address': line['ref_address'],
                        'ref_phone_number': line['ref_phone_number'],
                        'ref_fax_number': line['ref_fax_number'],
                        'ref_website': line['ref_website'],
                        'ref_email': line['ref_email'],
                        'ref_years_known': line['ref_years_known'],

                    }
                    extra_fields = self.env['res.partner.agent'].create(vals2)

            result = {'status': 'success', 'id': agent_obj.id}
            return json.dumps(result)
        except Exception as e:
            result = {'status': 'failure', 'error': str(e)}
            return json.dumps(result)

    # @api.model
    # def create_new_student(self, args):
    #     logger.info("=====Asked Question====----------------------------------------------------------------%s" % args)
    #     try:
    #         vals = {
    #             'name':args['first_name'] +" " + args['last_name'],
		#         'contact_name':args['first_name'] +' '+args['last_name'],
    #             'email_from':args['email'],
    #             'student_message':args['message'],
    #             'new_lead':True,
    #             'mode_of_contact':'asked_question'
    #         }
    #
    #         if args.get('phone_no',False):
    #             vals.update({'phone':args['phone_no']})
    #
    #         if args.get('form_page_url',False):
    #             vals.update({'form_page_url': args['form_page_url']})
    #
    #         if args.get('country_id',False):
    #             if args['country_id']['country_name']:
    #                 country_obj = self.env['res.country'].search([('name', '=', args['country_id']['country_name'])])
    #                 if not country_obj:
    #                     country_obj = self.env['res.country'].create({'name':args['country_id']['country_name'],
    #                                                                    'code':args['country_id']['country_id']})
    #                 vals.update({'country_id': country_obj.id, })
    #
    #         if args.get('city_id',False):
    #             if args['city_id']['city_name']:
    #                 vals.update({'city': args['city_id']['city_name']})
    #
    #         if args.get('program_id', False):
    #             if args['program_id']['program_id']:
    #                 args['program_id']['program_name'] = jQ(args['program_id']['program_name']).text()
    #                 program_obj = self.env['program.details'].search(
    #                     [('name', '=', args['program_id']['program_name'])])
    #                 if not program_obj:
    #                     program_obj = self.env['program.details'].create({'name': args['program_id']['program_name'],
    #                                                                       'internal_ref': args['program_id']['program_short_name']})
    #                 vals.update({'program':program_obj.id})
    #
    #         if args.get('international_student',False):
    #             if args['international_student'] == '1':
    #                 team_id=self.env['crm.team'].search([('name','ilike','international')])
    #                 if team_id:
    #                     vals.update({'team_id':team_id.id})
    #                 user_id=self.env['res.users'].search([('name','=','Elaine Gate')])
    #                 if user_id:
    #                     vals.update({'user_id': user_id.id})
    #                 vals.update({'select_button':'international_student'})
    #             else:
    #                 team_id = self.env['crm.team'].search([('name', 'ilike', 'local')])
    #                 if team_id:
    #                     vals.update({'team_id': team_id.id})
    #                 user_id = self.env['res.users'].search([('name', '=', 'Sana Hasni')])
    #                 if user_id:
    #                     vals.update({'user_id': user_id.id})
    #                 vals.update({'select_button': 'domestic_student'})
    #
    #         crm_lead_obj=self.env['crm.lead'].create(vals)
    #         result = {'status': 'success', 'id': crm_lead_obj.id}
    #         return json.dumps(result)
    #     except Exception as e:
    #         result={'status':'failure','error':str(e)}
    #         return json.dumps(result)

    @api.model
    def create_new_student(self, args):
        list=[]
        try:
            vals = {
                'name': args['first_name'] + " " + args['last_name'],
                'contact_name': args['first_name'] + ' ' + args['last_name'],
                'email_from': args['email'],
                'student_message': args['message'],
                'new_lead': True,
                'form_filled': 'asked_question'
            }

            if args.get('phone_no', False):
                vals.update({'phone': args['phone_no']})

            if args.get('form_page_url', False):
                vals.update({'form_page_url': args['form_page_url']})

            if args.get('country_id', False):
                if args['country_id']['country_name']:
                    country_obj = self.env['res.country'].search([('name', '=', args['country_id']['country_name'])])
                    if not country_obj:
                        country_obj = self.env['res.country'].create({'name': args['country_id']['country_name'],
                                                                      'code': args['country_id']['country_id']})
                    vals.update({'country_id': country_obj.id, })

            if args.get('city_id', False):
                if args['city_id']['city_name']:
                    vals.update({'city': args['city_id']['city_name']})

            # if args.get('program_id', False):
            #     if args['program_id']['program_id']:
            #         program_obj = self.env['program.details'].search(
            #             [('internal_ref', '=', args['program_id']['program_short_name'])])
            # if args.get('program_id', False):
            #     if args['program_id']['program_id']:
            #         args['program_id']['program_name'] = jQ(args['program_id']['program_name']).text()
            #         program_obj = self.env['program.details'].search(
            #             [('name', '=', args['program_id']['program_name'])])
            #         if not program_obj:
            #             program_obj = self.env['program.details'].create({'name': args['program_id']['program_name'],
            #                                                               'internal_ref': args['program_id'][
            #                                                                   'program_short_name']})

            if args.get('program_id', False):
                if args['program_id']['program_id']:
                    args['program_id']['program_name'] = jQ(args['program_id']['program_name']).text()
                    program_obj1 = self.env['program.details'].search(
                        [('name', '=', args['program_id']['program_name'])])
                    if not program_obj1:
                        program_obj1 = self.env['program.details'].create(
                            {'name': args['program_id']['program_name'],
                             'internal_ref': args['program_id'][
                                 'program_short_name']})
                    list.append(
                        {'program_ids': program_obj1.id,'checkbox': True})

            if args.get('international_student', False):
                if args['international_student'] == '1':
                    team_id = self.env['crm.team'].search([('name', 'ilike', 'international')])
                    if team_id:
                        vals.update({'team_id': team_id.id})
                    user_id = self.env['res.users'].search([('name', '=', 'Elaine Gate')])
                    if user_id:
                        vals.update({'user_id': user_id.id})
                    vals.update({'select_button': 'international_student'})
                else:
                    team_id = self.env['crm.team'].search([('name', 'ilike', 'local')])
                    if team_id:
                        vals.update({'team_id': team_id.id})
                    user_id = self.env['res.users'].search([('name', '=', 'Sana Hasni')])
                    if user_id:
                        vals.update({'user_id': user_id.id})
                    vals.update({'select_button': 'domestic_student'})

            crm_lead_obj = self.env['crm.lead'].create(vals)
            for rec in list:
                crm_lead_obj.write({'program_line_ids': [(0, 0, rec)]})
            crm_lead_obj.write({'program': program_obj1.id})
            result = {'status': 'success', 'id': crm_lead_obj.id}
            return json.dumps(result)
        except Exception as e:
            result = {'status': 'failure', 'error': str(e)}
            return json.dumps(result)

    @api.model
    def create(self,vals):
        context = {'create_rec':True}
        return super(crm, self.with_context(context)).create(vals)

    @api.multi
    def write(self, vals):
        if not self._context.get('create_rec', False) == True:
            vals.update({'new_lead': False})
        stage_id_name=''
        if self._context.get('con_opp_merge', False):
            pass
        elif not self._context.get('con_opp', False):
            if vals.get('stage_id',False):
                stage_id=self.env['crm.stage'].search([('id','=',vals.get('stage_id'))])
                if stage_id.name != 'Lost' and stage_id.name != 'Delayed':
                    if self._context.get('con_opp', False)!= True and self.type !='lead' and self.team_id.name == 'Local Sales':
                        if self.stage_id_name == "Opportunity":
                            stage_id_name = "Opportunity"
                        elif self.stage_id_name == "Prospect":
                            stage_id_name = "Prospect"
                        elif self.stage_id_name == "Confirmed Prospect Full":
                            stage_id_name = "Confirmed Prospect Full"
                        elif self.stage_id_name == "Confirmed Prospect Conditional":
                            stage_id_name = "Confirmed Prospect Conditional"
                        elif self.stage_id_name == "Enrollment":
                            stage_id_name = "Enrollment"
                        elif self.stage_id_name == "Pre-Enrollment":
                            stage_id_name = "Pre-Enrollment"
                        elif self.stage_id_name == "Delayed":
                            stage_id_name = "Delayed"
                        elif self.stage_id_name == "Lost":
                            stage_id_name = "Lost"
                    if self._context.get('con_opp', False)!= True and self.type !='lead' and  self.team_id.name == 'International Sales':
                        if self.stage_id_name == "Opportunity":
                            stage_id_name = "IntOpportunity"
                        elif self.stage_id_name == "Prospect":
                            stage_id_name = "IntProspect"
                        elif self.stage_id_name == "Admitted":
                            stage_id_name = "Admitted"
                        elif self.stage_id_name == "Visa Granted":
                            stage_id_name = "Visa Granted"
                        elif self.stage_id_name == "Delayed":
                            stage_id_name = "IntDelayed"
                        elif self.stage_id_name == "Lost":
                            stage_id_name = "IntLost"
        res = super(crm, self).write(vals)
        # if self.stage_id_name == "Lost" and self.team_id.name == 'International Sales':
        #         if not self.lost_reason:
        #             raise UserError(_("Please enter the reason for losing the lead!"))
        # if self.stage_id_name == "Lost" and self.team_id.name == 'Local Sales':
        #         if not self.lost_reason:
        #             raise UserError(_("Please enter the reason for losing the lead!"))
        #         if not self.lost_date:
        #             raise UserError(_("Please enter the lost date for the lead!"))
        # if self.stage_id_name == "Delayed" and self.team_id.name == 'International Sales':
        #         if not self.reason_of_delay:
        #             raise UserError(_("Please enter the reason for delay!"))
        #         if not self.expected_return_date:
        #             raise UserError(_("Please select the expected return date!"))
        # if self.stage_id_name == "Delayed" and self.team_id.name == 'Local Sales':
        #         if not self.reason_of_delay:
        #             raise UserError(_("Please enter the reason for delay!"))
        #         if not self.delay_date:
        #             raise UserError(_("Please select the date for delay!"))
        #         if not self.new_start_date:
        #             raise UserError(_("Please select the new start date!"))
        # if stage_id_name:
        #     if stage_id_name == "Opportunity":
        #         if not self.academic_requirements == True:
        #             raise UserError(_("Mark as informed needs to be checked for academic requirements!"))
        #         if not self.academic_requirements_date:
        #             raise UserError(_("Please select the date for academic requirements!"))
        #         if not self.academic_requirements_user:
        #             raise UserError(_("Please enter the user for academic requirements!"))
        #         if not self.other_requirements == True:
        #             raise UserError(_("Mark as informed needs to be checked for other requirements!"))
        #         if not self.other_requirements_date:
        #             raise UserError(_("Please select the date for other requirements!"))
        #         if not self.other_requirements_user:
        #             raise UserError(_("Please enter the user for other requirements!"))
        #         if not self.seat_deposit == True:
        #             raise UserError(_("Mark as informed needs to be checked for seat deposit!"))
        #         if not self.seat_deposit_date:
        #             raise UserError(_("Please select the date for seat deposit!"))
        #         if not self.seat_deposit_user:
        #             raise UserError(_("Please enter the user for seat deposit!"))
        #     elif stage_id_name == "IntOpportunity":
        #         if not self.inquiry_follow_up_date:
        #             raise ValidationError(_("Please select the date for inquiry follow up!"))
        #         if not self.admission_app_req == True:
        #             raise UserError(_("Admission application request needs to be checked!"))
        #         if not self.date_received:
        #             raise UserError(_("Please select the date received!"))
        #         if not self.agent:
        #             raise UserError(_("Please enter the agent!"))
        #         if not self.app_fee_paid:
        #             raise UserError(_("Please select the date for Application Fee Paid!"))
        #     elif stage_id_name == "IntProspect":
        #         if not self.pre_requisite_material_submitted == True:
        #             raise UserError(_("The checkbox needs to be checked for Pre-requisite Material Submitted!"))
        #         if not self.esl_message_submitted == True:
        #             raise UserError(_("The checkbox needs to be checked for Esl Testing Submitted!"))
        #         if not self.offer_of_admission_date:
        #             raise UserError(_("Please select the date for offer of admission!"))
        #         if not self.offer_signed_and_returned == True:
        #             raise UserError(_("The checkbox needs to be checked for offer signed and returned!"))
        #     elif stage_id_name == "Admitted":
        #         if not self.international_student_letter_of_acceptance:
        #             raise UserError(_("Please fill in the International Student Letter Of Acceptance!"))
        #         if not self.date_of_issue:
        #             raise UserError(_("Please select the date of issue!"))
        #         if not self.letter_expiry_date:
        #             raise UserError(_("Please select the letter expiry date!"))
        #     elif stage_id_name == "Visa Granted":
        #         if not self.enrollment_date:
        #             raise UserError(_("Please select the enrollment date!"))
        #         if not self.expected_arrival_date:
        #             raise UserError(_("Please select the expected arrival date!"))
        #     elif stage_id_name == "Prospect":
        #         if not self.supporting_academic_docs_date:
        #             raise UserError(_("Please select the date for supporting academic documents!"))
        #         if not self.supporting_academic_docs_user:
        #             raise UserError(_("Please enter the user for supporting academic documents!"))
        #     elif stage_id_name == "Confirmed Prospect Full":
        #         if not self.assessment_test_date:
        #             raise UserError(_("Please select the date for assessment test!"))
        #         if self.seat_deposit_amount == 0.0:
        #             raise UserError(_("Please enter a valid value for seat deposit!"))
        #         if not self.deposit_payment_date:
        #             raise UserError(_("Please select the date for seat deposit payment!"))
        #         if not self.method_of_payment:
        #             raise UserError(_("Please enter a method of payment!"))
        #     elif stage_id_name == "Confirmed Prospect Conditional":
        #         if not self.pending_docs:
        #             raise UserError(
        #                 _("Please enter the pending documents!"))
        #     elif stage_id_name == "Pre-Enrollment":
        #         if not self.financial_aid_provided == True:
        #             if not self.financial_aid_provided_reason:
        #                 raise UserError(_("Please fill in the reason for Financial Aid Provided!"))
        #         if not self.payment_plan == True:
        #             if not self.payment_plan_reason:
        #                 raise UserError(_("Please fill in the reason for Payment Plan!"))
        #         if not self.police_clearance == True:
        #             if not self.police_clearance_reason:
        #                 raise UserError(_("Please fill in the reason for Police Clearance!"))
        #         if not self.health_immunization_record == True:
        #             if not self.health_immunization_record_reason:
        #                 raise UserError(_("Please fill in the reason for Health Immunization Record!"))
        #     elif stage_id_name == "Enrollment":
        #         if not self.date_of_enrollment:
        #             raise UserError(_("Please select a date of enrollment!"))
        #     elif stage_id_name == "Delayed":
        #         if not self.reason_of_delay:
        #             raise UserError(_("Please enter the reason for delay!"))
        #         if not self.delay_date:
        #             raise UserError(_("Please select the date for delay!"))
        #         if not self.new_start_date:
        #             raise UserError(_("Please select the new start date!"))
        #     elif stage_id_name == "IntDelayed":
        #         if not self.reason_of_delay:
        #             raise UserError(_("Please enter the reason for delay!"))
        #         if not self.expected_return_date:
        #             raise UserError(_("Please select the expected return date!"))
        #     elif stage_id_name == "Lost":
        #         if not self.lost_reason:
        #             raise UserError(_("Please enter the reason for losing the lead!"))
        #         if not self.lost_date:
        #             raise UserError(_("Please enter the lost date for the lead!"))
        #     elif stage_id_name == "IntLost":
        #         if not self.lost_reason:
        #             raise UserError(_("Please enter the reason for losing the lead!"))
        return res

class crm_lead_book_tour(models.Model):
    _name = 'crm.lead.book.tour'
    _rec_name = 'first_name'

    first_name = fields.Char('Contact Name')
    last_name = fields.Char('Last Name')
    phone_no = fields.Char('Contact Details')
    email = fields.Char('Email')
    state_id = fields.Many2one("res.country.state", string='State')
    city = fields.Char('City')
    program_id = fields.Many2one('product.product', string='I Am Interested In')
    preferred_date = fields.Date('Preferred Date And Time')
    preferred_time = fields.Selection([('9am_to_930am', '9 am to 9:30 am'),
                                       ('930am_to_10am', '9:30 am to 10 am'),
                                       ('10am_to_1030am', '10 am to 10:30 am'),
                                       ('1030am_to_11am', '10:30 am to 11 am'),
                                       ('1am_to_1130am', '11 am to 11:30 am'),
                                       ('1130am_to_12am', '11:30 am to 12 pm'),
                                       ('12pm_to_1230pm', '12 pm to 12:30 pm'),
                                       ('1230pm_to_1pm', '12:30 pm to 1 pm'),
                                       ('1pm_to_130pm', '1 pm to 1:30 pm'),
                                       ('130pm_to_2pm', '1:30 pm to 2 pm'),
                                       ('2pm_to_230pm', '2 pm to 2:30 pm'),
                                       ('230pm_to_3pm', '2:30 pm to 3 pm'),
                                       ('3pm_to_330pm', '3 pm to 3:30 pm'),
                                       ('330pm_to_4pm', '3:30 pm to 4 pm')], 'Preferred Time')
    form_page_url = fields.Char()
    comments = fields.Text('Comments')



    @api.model
    def create_agent_tour(self, args):
        try:
            vals = {
                'name':  args['first_name'] +' '+ args['last_name'],
                'phone': args['phone_no'],
                'email_from': args['email'],
                'preferred_date': args['preferred_date'],
                'comments': args['comments'],
                'city': args['city']['city_name'],
                'new_lead':True,
                'mode_of_contact':'book_a_tour'
            }

            if args.get('form_page_url',False):
                vals.update({'form_page_url': args['form_page_url']})

            if args.get('province', False):
                if args['province']['state_name']:
                    state_obj = self.env['res.country.state'].search([('name', '=', args['province']['state_name'])])
                    country_id = self.env['res.country'].search([('name', '=', 'Canada')]).id
                    if not state_obj:
                        state_obj = self.env['res.country.state'].create({'name': args['province']['state_name'],
                                                                          'code': args['province']['state_id'],
                                                                                'country_id': country_id})
                    vals.update({'state_id': state_obj.id})

            # if args.get('city', False):
            #     if args['city']['city_name']:
            #         vals.update({'city': args['city']['city_name']})

            if args.get('program_id', False):
                if args['program_id']['program_id']:
                    args['program_id']['program_name'] = jQ(args['program_id']['program_name']).text()
                    program_obj = self.env['program.details'].search(
                        [('name', '=', args['program_id']['program_name'])])
                    if not program_obj:
                        program_obj = self.env['program.details'].create({'name': args['program_id']['program_name'],
                                                                          'internal_ref': args['program_id']['program_short_name']})
                    vals.update({'program':program_obj.id})

            if args.get('preferred_time', False):
                if '9 am to 9:30 am' in args['preferred_time']:
                    vals.update({'preferred_time': '9am_to_930am'})
                elif '9:30 am to 10 am' in args['preferred_time']:
                    vals.update({'preferred_time': '930am_to_10am'})
                elif '10 am to 10:30 am' in args['preferred_time']:
                    vals.update({'preferred_time': '10am_to_1030am'})
                elif '10:30 am to 11 am' in args['preferred_time']:
                    vals.update({'preferred_time': '1030am_to_11am'})
                elif '11 am to 11:30 am' in args['preferred_time']:
                    vals.update({'preferred_time': '11am_to_1130am'})
                elif '11:30 am to 12 pm' in args['preferred_time']:
                    vals.update({'preferred_time': '1130am_to_12am'})
                elif '12 pm to 12:30 pm' in args['preferred_time']:
                    vals.update({'preferred_time': '12pm_to_1230pm'})
                elif '12:30 pm to 1 pm' in args['preferred_time']:
                    vals.update({'preferred_time': '1230pm_to_1pm'})
                elif '1 pm to 1:30 pm' in args['preferred_time']:
                    vals.update({'preferred_time': '1pm_to_130pm'})
                elif '1:30 pm to 2 pm' in args['preferred_time']:
                    vals.update({'preferred_time': '130pm_to_2pm'})
                elif '2 pm to 2:30 pm' in args['preferred_time']:
                    vals.update({'preferred_time': '2pm_to_230pm'})
                elif '2:30 pm to 3 pm' in args['preferred_time']:
                    vals.update({'preferred_time': '230pm_to_3pm'})
                elif '3 pm to 3:30 pm' in args['preferred_time']:
                    vals.update({'preferred_time': '3pm_to_330pm'})
                elif '3:30 pm to 4 pm' in args['preferred_time']:
                    vals.update({'preferred_time': '330pm_to_4pm'})
                else:
                    pass

            book_tour_obj = self.env['crm.lead'].create(vals)
            result = {'status': 'success', 'id': book_tour_obj.id}
            return json.dumps(result)

        except Exception as e:
            result = {'status': 'failure', 'error': str(e)}
            return json.dumps(result)

class Lead2OpportunityPartner(models.TransientModel):

    _inherit = 'crm.lead2opportunity.partner'

    @api.multi
    def action_apply(self):
        """ Convert lead to opportunity or merge lead and opportunity and open
            the freshly created opportunity view.
        """

        self.ensure_one()
        values = {
            'team_id': self.team_id.id,
        }

        if self.partner_id:
            values['partner_id'] = self.partner_id.id



        if self.name == 'merge':
            for rec in self._context.get('active_ids', []):
                self.env['merged.crm.leads'].with_context(con_opp_merge= True).create({'crm_lead_id':self.opportunity_ids[-1].id,'crm_lead':rec})
            leads = self.opportunity_ids.with_context(con_opp_merge= True).merge_opportunity()
            if leads.type == "lead":
                values.update({'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
                self.with_context(active_ids=leads.ids)._convert_opportunity(values)
            elif not self._context.get('no_force_assignation') or not leads.user_id:
                values['user_id'] = self.user_id.id
                leads.write(values)
        else:
            leads = self.env['crm.lead'].browse(self._context.get('active_ids', []))
            values.update({'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
            context = {'con_opp': True}
            self.with_context(context)._convert_opportunity(values)

        if self._context.get('from_website',False):
            return True
        else:
            return leads[0].redirect_opportunity_view()


class res_partner(models.Model):
        _inherit = 'res.partner'

        select_button = fields.Boolean('agent_detail')
        form_page_url = fields.Char()
        worked_immigration = fields.Char()
        assist_int_students = fields.Char()
        designation = fields.Char()
        bussinessdocids = fields.One2many('res.partner.businessdocs', 'res_partner_id',
                                          'Records of Excellence and Good Standing')
        agency_name = fields.Char('Name of Agency')
        agency_address = fields.Char('Address')
        agency_city_id = fields.Char('City')
        agency_state_id = fields.Many2one("res.country.state", string='')
        agency_country_id = fields.Many2one('res.country', string='Country')
        agency_postal_code = fields.Char()
        agency_alt_phone_number = fields.Char('Phone No')
        agency_fax_number = fields.Char()
        website = fields.Char()
        year_established = fields.Char()
        business_team = fields.Char()
        ownership = fields.Char()
        contact_details = fields.Char('Contact Details')

        head_office = fields.Text()
        partner_sub_agencies = fields.Text()
        recruit_post_secondary = fields.Text()
        assist_last_year = fields.Text()
        stu_sent_overseas = fields.Text()
        country_send_stu_to = fields.Text()
        programs_interest = fields.Text()
        stu_anticipate_annually = fields.Text()

        familiar_permit_requirements = fields.Selection([('yes', 'Yes'),
                                                         ('no', 'No')], 'Permit requirements ')
        edu_counselling_stu = fields.Text()

        pro_coun = fields.Boolean('Programs Counselling')
        gath_req = fields.Boolean('Gathering documents')
        pre_sub = fields.Boolean('Application preparation and Submission')
        gui_app = fields.Boolean('Guiding applicant through offer ')
        permit_pre = fields.Boolean('Study permit preparation ')
        pre_ser = fields.Boolean('Pre Departure Service ')
        sou_gov = fields.Boolean('Identify possible funding sources, government grants')
        esl_test = fields.Boolean('English as Second language (ESL) Testing ')

        housing = fields.Boolean('Housing')
        med_ins = fields.Boolean('Medical Insurance ')
        trav_iti = fields.Boolean('Travel Itinerary')
        can_arr = fields.Boolean('Canadian Arrival ')
        ser_avi = fields.Boolean('Other services available')
        # esl_test = fields.Boolean('English as Second language (ESL) Testing ')
        other_services_available = fields.Char()

        stu_package_cost = fields.Text()
        service_beside_recruit = fields.Text()


        ref_contact = fields.One2many('res.partner.agent', 'agent_id', 'References')

        marketing_strategy = fields.Text()

        google = fields.Boolean('Google')
        facebook = fields.Boolean('Facebook')
        radio = fields.Boolean('Radio')
        tv = fields.Boolean('TV')
        jobfair = fields.Boolean('Job Fair')
        newspaper = fields.Boolean('Newspaper')

        hear_about_newspaper = fields.Char()

        other_hear = fields.Boolean('Other')

        hear_about_other = fields.Char()




class ResPartnerAgent(models.Model):
        _name = 'res.partner.agent'

        ref_contact_name = fields.Char('Contact Name')
        ref_position = fields.Char('Position')
        ref_agency = fields.Char('Agency Name')
        ref_address = fields.Char('Address')
        ref_phone_number = fields.Char('Phone No')
        ref_fax_number = fields.Char('Fax No')
        ref_website = fields.Char('Website')
        ref_email = fields.Char('Email')
        ref_years_known = fields.Char('Year Known')

        agent_id = fields.Many2one('res.partner', 'Refer')

class crm_lead_educational_background(models.Model):
        _name = 'crm.lead.educational.background'

        from_year = fields.Char()
        to_year = fields.Char()
        institution_name = fields.Char('Name of Institution')
        qualifications = fields.Char('Qualification')
        file = fields.One2many('crm.lead.edu.files','crm_lead_edu_back_id')
        education_back = fields.Many2one('crm.lead', 'Educational Background ')

class crm_lead_edu_files(models.Model):
    _name = 'crm.lead.edu.files'

    crm_lead_edu_back_id=fields.Many2one('crm.lead.educational.background')
    file=fields.Char('File')

