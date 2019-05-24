from IPython.testing import tools

from odoo import api, fields, models,_
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)
from odoo.exceptions import UserError


class crm_lead_new(models.Model):
    _inherit = 'crm.lead'


    #Basic Information

    name = fields.Char('Opportunity', required=False, invisible=1)
    crm_type=fields.Selection([('individual', 'Individual'), ('business', 'Business')],string='Crm Type',)
    first_name=fields.Char('First Name')
    last_name=fields.Char('Last Name')
    spouse_first_name=fields.Char('First Name')
    spouse_last_name = fields.Char('Last Name')
    primary_marital_status=fields.Selection([('married','Married'),
                                     ('un_married','Un-Married')], 'Marital Status')
    spouse_marital_status = fields.Selection([('married', 'Married'),
                                               ('un_married', 'Un-Married')], 'Marital Status')
    address=fields.Text('Address')
    primary_dob=fields.Date('DOB')
    spouse_dob=fields.Date('DOB')
    primary_mobile=fields.Integer('Mobile Number')
    spouse_mobile=fields.Integer('Mobile Number')
    primary_email=fields.Char('Email Id')
    spouse_email = fields.Char('Email Id')
    gender = fields.Selection([('male', 'Male'),('female', 'Female')], 'Gender')
    Child_ids=fields.One2many('crm.child','child_id',string="Children")
    spouse_occupation=fields.Char("Occupation")
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    city = fields.Char('City')
    spouse_province=fields.Char("Province")
    spouse_home_phone=fields.Integer("Home Phone")
    spouse_sin =fields.Char("SIN #")


    # Additional Info
    referral_details=fields.Many2one('referral.detail', string="Referral Details")
    product_interest=fields.Many2one('product.detail',string="Product Interest")
    Source_of_lead=fields.Selection([('website', 'Website'),
                                     ('referral', 'Referral'),
                                     ('social_media', 'Socal Media'),
                                     ('other', 'Other')], 'Source Of Lead')
    lead_status = fields.Selection([('hot', 'Hot'),
                               ('warm', 'Warm'),
                               ('cold', 'Cold')],
                              string="Lead Status")
    Rating=fields.Char("Rating")
    facebook=fields.Text("Facebook")
    sic=fields.Text("SIC(Standard Industrial Classification)")
    number_of_location=fields.Char("Number Of Location")


    # Activity
    stage_id_name = fields.Char(related='stage_id.name', readonly=True, store=True)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange')
    activity_ids = fields.One2many('crm.activities', 'crm_lead_id', string='Activities')

    # Company info

    account_id =fields.Many2one('account.company',string="Company Info")

    # contacts

    contacts_id = fields.Many2one('contacts.details', string="contacts")


    # company_name=fields.Char("Company Name")
    # type_of_company=fields.Char("Type of Company")
    # establish_on_date=fields.Date("Establish On Date")
    # industry=fields.Char("Industry")
    # website=fields.Char("Website")
    # linked_in_profile=fields.Text("LinkedIn Profile")
    # linked_in_company=fields.Text("LinkedIn Company")
    # company_facebook=fields.Text("Facebook")
    # company_twitter=fields.Text("Twitter")
    # micro_sites=fields.Text("Micro Sites")
    # currency_id = fields.Many2one(comodel_name='res.currency', string="Country Currency")
    # company_revenue=fields.Monetary("Company Revenue",currency_field='currency_id')







    #Financial Information

    business_name=fields.Char('Business Name')
    business_number=fields.Char('Business Number')
    business_address=fields.Text('Business Address')
    business_year_end=fields.Date('Business End Year')
    business_start_year=fields.Date('Business start Year')
    hst_filing=fields.Selection([('monthly','Monthly'),
                                 ('quarterly','Quarterly'),
                                 ('annually', 'Annual')], 'HST Filing Frequency')
    hst_filing_date=fields.Date('HST Filing Date')
    payroll_filing=fields.Selection([('monthly', 'Monthly'),
                                     ('quarterly', 'Quarterly'),
                                     ('annually', 'Annual')], 'Payroll Filing Frequency')
    payroll_filing_date=fields.Date('Payroll Filing Date')
    annual_filing=fields.Date('Annual Filing Date')
    recipient = fields.Char('Recipient')
    subject = fields.Char('Subject')
    body = fields.Html('Body')

    @api.multi
    def create_wizard(self, vals):
        view = self.env.ref('pfs_crm.pfs_wizard_form_view')
        new_id = self.env['pfs.wizard']


        return {
            'name': _("Asset Data Confirmation"),
            'view_mode': 'form',
            'view_id': view.id,

            'view_type': 'form',
            'res_model': 'pfs.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context' :{'default_recipient':self.primary_email}

        }







    @api.multi
    def activity_record_scheduler(self):
        current_date=datetime.now()
        filing_obj=self.env['new.filing.settings'].search([
            ('hst_filing_monthly','!=',False),
            ('hst_filing_quarterly','!=',False),
            ('hst_filing_annually','!=',False),
            ('payroll_filing_monthly','!=',False),
            ('payroll_filing_quarterly','!=',False),
            ('payroll_filing_annually','!=',False),

        ])
        hst_filing_month=filing_obj.hst_filing_monthly
        hst_filing_quarter=filing_obj.hst_filing_quarterly
        hst_filing_annual=filing_obj.hst_filing_annually
        payroll_filing_month=filing_obj.payroll_filing_monthly
        payroll_filing_quarter=filing_obj.payroll_filing_quarterly
        payroll_filing_annual=filing_obj.payroll_filing_annually
        if hst_filing_month:
            filing_date=current_date+relativedelta(days=+hst_filing_month)
        if hst_filing_quarter:
            filing_date=current_date+relativedelta(days=+hst_filing_quarter)
        if hst_filing_annual:
            filing_date=current_date+relativedelta(days=+hst_filing_annual)

        hst_obj=self.env['crm.lead'].search([('hst_filing_date','=', filing_date)])
        for records in hst_obj:
            act_obj=self.env['pfs.crm.activites'].create({
                'lead':records.id,
                'email':records.primary_email,
                'h_filing_date':records.hst_filing_date,
                'h_filing':records.hst_filing,
                'activity_date':filing_date,
            })

        if payroll_filing_month:
                filing_date = current_date + relativedelta(days=+payroll_filing_month)
        if payroll_filing_quarter:
                filing_date = current_date + relativedelta(days=+payroll_filing_quarter)
        if payroll_filing_annual:
                filing_date = current_date + relativedelta(days=+payroll_filing_annual)

        payroll_obj=self.env['crm.lead'].search([('payroll_filing_date','=',filing_date)])
        for record in payroll_obj:
            act_obj=self.env['pfs.crm.activites'].create({
                'lead':record.id,
                'email':record.primary_email,
                'p_filing_date':record.payroll_filing_date,
                'p_filing':record.payroll_filing,
                'activity_date':filing_date,
            })





    @api.multi
    def send_alert_mail(self):
        current_date=datetime.now()
        new_date = datetime.strftime(current_date, '%Y-%m-%d')
        hst_obj=self.env['pfs.crm.activites'].search([('h_filing','!=',False)])
        payroll_obj=self.env['pfs.crm.activites'].search([('p_filing','!=',False)])
        hst_template = self.env['mail.template'].search([('name', '=', 'Hst Expiry Notification')])
        payroll_template = self.env['mail.template'].search([('name', '=', 'Payroll Expiry Notification')])
        for record in hst_obj:
            if new_date == record.h_filing_date:
                body = hst_template.body_html
                body = body.replace('--first_name',record.lead.first_name)
                body = body.replace('--last_name',record.lead.last_name)
                body = body.replace('--business_name',record.lead.business_name)
                body = body.replace('--business_no',record.lead.business_number)
                body = body.replace('--hst_date', record.lead.hst_filing_date)
                body = body.replace('--hst_frequency',record.lead.hst_filing)
                mail_values = {
                    'subject': hst_template.subject,
                    'body_html': body,
                    'email_to': record.email,

                }
                create_and_send_email = self.env['mail.mail'].create(mail_values).send()
                if record.h_filing == 'monthly':
                    filing_date=record.h_filing_date
                    new_filing_date= datetime.strptime(filing_date,'%Y-%m-%d')
                    update_date = new_filing_date + relativedelta(months=1)
                    record.lead.write({
                        'hst_filing_date': update_date,
                    })
                if record.h_filing== 'quarterly':
                    filing_date=record.h_filing_date
                    new_filing_date=datetime.strptime(filing_date, '%Y-%m-%d')
                    update_date=new_filing_date+relativedelta(months=3)
                    record.lead.write({
                        'hst_filing_date': update_date,
                    })
                if record.h_filing == 'annually':
                    filing_date=record.h_filing_date
                    new_filing_date=datetime.strptime(filing_date, '%Y-%m-%d')
                    update_date = new_filing_date+relativedelta(months=12)
                    record.lead.write({
                        'hst_filing_date': update_date,
                    })
                record.unlink()

        for record in payroll_obj:
            if new_date == record.p_filing_date:
                body = payroll_template.body_html
                body = body.replace('--first_name',record.lead.first_name)
                body = body.replace('--last_name', record.lead.last_name)
                body = body.replace('--business_name',record.lead.business_name)
                body = body.replace('--business_no', record.lead.business_number)
                body = body.replace('--payroll_date',record.lead.payroll_filing_date)
                body = body.replace('--payroll_frequency',record.lead.payroll_filing)
                mail_values = {
                    'subject': payroll_template.subject,
                    'body_html': body,
                    'email_to': record.email,

                }
                create_and_send_email = self.env['mail.mail'].create(mail_values).send()
                if record.p_filing == 'monthly':
                    filing_date=record.p_filing_date
                    new_filing_date = datetime.strptime(filing_date, '%Y-%m-%d')
                    update_date=new_filing_date+relativedelta(months=1)
                    new_update_date=datetime.strftime(update_date,'%Y-%m-%d')
                    record.lead.write({
                        'payroll_filing_date': update_date,
                    })
                if record.p_filing == 'quarterly':
                    filing_date = record.p_filing_date
                    new_filing_date = datetime.strptime(filing_date, '%Y-%m-%d')
                    update_date = new_filing_date+relativedelta(months=3)
                    record.lead.write({
                        'payroll_filing_date': update_date,
                    })
                if record.p_filing == 'annually':
                    filing_date=record.p_filing_date
                    new_filing_date=datetime.strptime(filing_date, '%Y-%m-%d')
                    update_date=new_filing_date + relativedelta(months=12)
                    record.lead.write({
                        'payroll_filing_date': update_date,
                    })
                record.unlink()





class crm_childs(models.Model):
    _name = 'crm.child'


    child_id=fields.Many2one('crm.lead',string="Children")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')
    dob=fields.Date("DOB")


class ReferralDetails(models.Model):
    _name = 'referral.detail'
    _rec_name = 'referral_name'


    referral_name=fields.Char("Referral Name")
    referral_phone=fields.Integer("Referral Phone")



class ProductDetail(models.Model):
    _name = 'product.detail'
    _rec_name = 'product_name'


    product_name=fields.Char("Product Name")


class AccountCompany(models.Model):
    _name = 'account.company'

    # Company info

    company_name = fields.Char("Company Name")
    type_of_company = fields.Char("Type of Company")
    establish_on_date = fields.Date("Establish On Date")
    industry = fields.Char("Industry")
    website = fields.Char("Website")
    linked_in_profile = fields.Text("LinkedIn Profile")
    linked_in_company = fields.Text("LinkedIn Company")
    company_facebook = fields.Text("Facebook")
    company_twitter = fields.Text("Twitter")
    micro_sites = fields.Text("Micro Sites")
    currency_id = fields.Many2one(comodel_name='res.currency', string="Country Currency")
    company_revenue = fields.Monetary("Company Revenue", currency_field='currency_id')






class ContactsDetails(models.Model):
    _name = 'contacts.details'

    name=fields.Char('Name')
    account_name=fields.Char('Account Name')
    title=fields.Text('Title')
    department=fields.Char('Department')
    birth_date=fields.Date('Birthdate')
    lead_source = fields.Selection([('website', 'Website'),
                                       ('referral', 'Referral'),
                                       ('social_media', 'Socal Media'),
                                       ('other', 'Other')], 'Lead Source')
    mailing_address=fields.Char('Mailing Address')
    created_by=fields.Char('Created By')
    click_to_call_phone=fields.Char('Click to call phone')
    email=fields.Char('Email')
    phone=fields.Char('Phone')
    mobile =fields.Char('Mobile')
    opportunity_id=fields.Many2one('account.company','Opportunity')
    open_activity_ids=fields.One2many('crm.activities',inverse_name='open_activity_id',string='Open Activity')
    activity_history_ids=fields.One2many('crm.activities',inverse_name='activity_history_id',string='Activity History')
    upload_attachment_ids = fields.One2many('ir.attachment', 'upload_attachment_id', string='Attachment')


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    upload_attachment_id = fields.Many2one('crm.lead', 'Upload Document')
    notes = fields.Char('Notes')
    # attachments = fields.Binary("Attachments")





class CrmActivities(models.Model):

    _name = "crm.activities"
    _rec_name = 'crm_lead_id'

    open_activity_id = fields.Many2one('contacts.details','Open Activity')
    activity_history_id = fields.Many2one('contacts.details','Activity History')
    crm_lead_id = fields.Many2one('crm.lead', 'Lead')
    crm_activity_id = fields.Many2one('crm.activity', 'Activity')
    outcome = fields.Text('Outcome')
    date_action = fields.Date('Activity Date', index=True)
    hours = fields.Selection([(str(num).zfill(2), str(num).zfill(2)) for num in range(01, 24)],
                             string='Timing')
    mins = fields.Selection([(str(num).zfill(2), str(num).zfill(2)) for num in range(01, 60)],
                            string='Mins')
    time = fields.Char(string='Timing',store=True)
    # date_action_datetime=fields.Datetime('Activity Datetime',compute="compute_activity_datetime")
    title_action = fields.Char('Activity Summary')
    state = fields.Selection([
        ('open', 'Open'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, required=True, track_visibility='always', copy=False, default='open')
    next_step=fields.Char(string="Next Step")
    def open_activity_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "crm.activities",
            "views": [[False, "form"]],
            "res_id": self.id,
            "view_id": 'crm_activities_form',
            "target": "new",
        }



    @api.one
    def mark_activity_done(self):
        if not self.crm_activity_id:
            raise UserError("Please select an activity!!!")
        if not self.outcome:
            raise UserError("Please enter outcome for this activity!!!")
        body_html = """<div><b>Activity:%s</b></div>""" % self.crm_activity_id.name
        if self.title_action:
            title_action = """<div>Activity Summary%s</div>""" % self.title_action
            body_html += title_action
        if self.date_action:
            date_action = """<div>Activity Date:%s</div>""" % self.date_action
            body_html += date_action
        if self.outcome:
            outcome = """<div>Activity Outcome%s</div>""" % self.outcome
            body_html += outcome
        body_html = self.env['mail.template'].render_template(body_html, 'crm.lead', self.crm_lead_id.id, )
        msg_id = self.crm_lead_id.message_post(body_html, subtype_id=self.crm_activity_id.subtype_id.id)
        self.state = 'done'
        return True

    @api.one
    def mark_activity_cancelled(self):
        if not self.crm_activity_id:
            raise UserError("Please select an activity!!!")
        if not self.outcome:
            raise UserError("Please enter outcome for this activity!!!")
        self.state = 'cancel'
        return True

    @api.onchange('hours','mins')
    def compute_time(self):
        for rec in self:
            if rec.hours and rec.mins:
                rec.time=rec.hours+':'+rec.mins


class Pfswizard(models.TransientModel):
    _name = 'pfs.wizard'


    recipient = fields.Char('Recipient')
    subject = fields.Char('Subject')
    body = fields.Html('Body')
    template_use = fields.Many2one('mail.template',string='Template id')

    @api.multi
    def send_mail(self):
        mail_env = self.env['mail.mail']
        file_notification = {
            'email_to': self.recipient,
            'subject': self.subject,
            'body_html': self.body,


        }

        mail = mail_env.create(file_notification)
        mail.send()
