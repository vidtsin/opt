from odoo import api, fields, models,_
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)
from odoo.exceptions import UserError


class crm_lead_new(models.Model):
    _inherit = 'crm.lead'
    _rec_name = 'name'

    @api.one
    @api.depends('product_ids.product_name_id')
    def compute_program(self):
        name=''
        for rec in self.product_ids:
            if name:
                name=name+"\t , \n"+rec.product_name_id.product_name
            else:
                name=rec.product_name_id.product_name
        self.program_compute = name



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
    # contact_email = fields.Char('Email Id')
    gender = fields.Selection([('male', 'Male'),('female', 'Female')], 'Gender')
    Child_ids=fields.One2many('crm.child','child_id',string="Children")
    spouse_occupation=fields.Char("Occupation")
    personal_occupation=fields.Char("Occupation")
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    city = fields.Char('City')
    spouse_province=fields.Char("Province")
    personal_province=fields.Char("Province")
    spouse_home_phone=fields.Integer("Home Phone")
    spouse_sin =fields.Char("SIN #")
    account_name_id=fields.Many2one('account.company','Account Name')
    department=fields.Char('Department')
    mailing_address=fields.Char('Mailing Address')
    created_by=fields.Char("Created By")
    click_to_call_phone=fields.Char("Click_to_call Phone")
    product_id=fields.Many2one('product.detail','Product Interest')
    open_activity_ids = fields.One2many(comodel_name='crm.activities',  inverse_name='crm_lead_id', string='Open Activity',domain=[('state','=','open')])
    activity_history_ids = fields.One2many(comodel_name='crm.activities',  inverse_name='crm_lead_id',string='Activity History',domain=[('state','=','done')])
    competitors=fields.Char('Competitors')
    lead_state = fields.Selection([
        ('open', 'Open'), ('contacted', 'Contacted')], string="State", default='open')
    # lead_id = fields.Many2one('sin.schedular.setting','leads')
    personal_sin = fields.Char("SIN #")
    title = fields.Char('Title')



    # Additional Info
    referral_details=fields.Many2one('referral.detail', string="Referral Details")
    # product_interest=fields.Many2one('product.detail',string="Product Interest")
    source_of_lead=fields.Selection([('website', 'Website'),
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
    # user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange')
    activity_ids = fields.One2many(comodel_name='crm.activities',inverse_name='crm_lead_id', string='Activities')

    # Company info

    account_id =fields.Many2one('account.company',string="Company Info")

    # contacts

    product_ids = fields.One2many('product.display','product_id', string="Products")

    upload_attachment_ids = fields.One2many('ir.attachment', 'upload_attachment_id', string='Attachment')
    lead_source = fields.Selection([('website', 'Website'),
                                        ('referral', 'Referral'),
                                       ('social_media', 'Socal Media'),
                                       ('other', 'Other')], 'Lead Source')
    opportunity_id = fields.Many2one('account.company', 'Opportunity')
    # contact_id = fields.Many2one('account.company', string="contacts")



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







    #Business Information

    business_name=fields.Char('Business Name')
    business_number=fields.Char('Business Number')
    business_address=fields.Text('Business Address')
    business_year_end=fields.Date('Business Year End')
    business_start_year=fields.Date('Business Registration Date')
    hst_filing=fields.Selection([('monthly','Monthly'),
                                 ('quarterly','Quarterly'),
                                 ('annually', 'Annual')], 'HST Filing Frequency')
    hst_filing_date=fields.Date('HST Filing Date')
    payroll_filing=fields.Selection([('monthly', 'Monthly'),
                                     ('quarterly', 'Quarterly'),
                                     ('annually', 'Annual')], 'Payroll Filing Frequency')
    payroll_filing_date=fields.Date('Payroll Filing Date')
    annual_filing=fields.Date('Annual Filing Date')
    sin_reminder = fields.Many2one('sin.schedular.setting','SIN Reminder')
    attachment_file = fields.Binary(string='Attachment File')

    stage_id_name = fields.Char(related='stage_id.name', readonly=True, store=True)



    convert_consultation=fields.Boolean("Convert Consultation")
    convert_proposal=fields.Boolean("Convert Proposal")
    convert_negotiation=fields.Boolean("Convert Negotiation")
    convert_closed=fields.Boolean("Convert Closed")
    program_compute = fields.Char("Program Interested", compute='compute_program')
    # conversion_date =fields.Date("Conversion Date")
    convert_to_client=fields.Boolean("Clients")

    # @api.onchange('stage_id')
    # def onchange_convert_stage(self):
    #     if self.Consultation == True:
    #         view_id = self.env['crm.stage'].search([('name', '=', 'Consultation')])
    #         self.stage_id= view_id.id
    #     if self.convert_proposal == True:
    #         view_id = self.env['crm.stage'].search([('name', '=', 'Proposal')])
    #         self.stage_id= view_id.id
    #     if self.convert_negotiation == True:
    #         view_id = self.env['crm.stage'].search([('name', '=', 'Negotiation')])
    #         self.stage_id= view_id.id
    #     if self.convert_closed == True:
    #         view_id = self.env['crm.stage'].search([('name', '=', 'Closed')])
    #         self.stage_id= view_id.id

    @api.onchange('product_ids')
    def onchange_program(self):
        temp = 0
        for id in self.product_ids:
            if id.product_check == True:
                temp += 1
        if temp > 1:
            raise ValidationError("You cannot select more than one product")
        else:
            for id in self.product_ids:
                if id.product_check == True:
                    self.product_id= id.product_name_id



    @api.multi
    def name_get(self):
        result = []
        for record in self:
            person_id = '' + str(record.name) + '' + ' ' + str(record.last_name)
            result.append((record.id, person_id))
        return result

    @api.model
    def create(self, vals):
        result = super(crm_lead_new, self).create(vals)
        if not self.spouse_sin:
            current_date = datetime.now()
            lead_gen_date = current_date + relativedelta(days=7)
            act_obj = self.env['sin.schedular.setting'].create( {
                    'lead_id': result.id,

                    'date': lead_gen_date
                                            })
        # res=self.env['crm.stage'].search([('name', '=', 'Client Won')])
        # result.stage_id=res

        print result
        return result



    @api.multi
    def write(self, vals):
        result = super(crm_lead_new, self).write(vals)
        if self.spouse_sin != False:
            rec_id = self.env['sin.schedular.setting'].search([('lead_id','=',self.id)])
            rec_id.unlink()
        list = []
        if self.product_ids:
            for p in self.product_ids:
                if p.product_check == True:
                    p1 = p.product_check
                    list.append(p1)

            if len(list) > 1:
                raise UserError(_("You cannot select more than one product"))


        print result
        return result

    @api.multi
    def delete_sin(self):
        print"self valueeeeeeeee", self
        for rec in self:
            if rec.sin_reminder:
                rec.sin_reminder.unlink()
            else:
                raise ValidationError("first select the SIN Reminder to delete")

    @api.multi
    def open_client(self):
        clients = self.env.ref('pfs_crm.crm_oppor_clients_details_form_view', False)
        view_id = self.env['crm.lead']
        vals = {
            # 'checkbox_other': self.other_requirements.name,

            'convert_to_client':True,

        }
        new = self.write(vals)
        return {
            'name': _('Convert Stage'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': self.id,
            'view_id': clients.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current'
        }


    @api.multi
    def redirect_opportunity_view1(self):
        self.ensure_one()
        # Get opportunity views
        current_date = datetime.now()
        form_view = self.env.ref('crm.crm_case_form_view_oppor')
        tree_view = self.env.ref('crm.crm_case_tree_view_oppor')
        crm_id =self.env['crm.lead'].browse(self._context['active_id'])
        if self.crm_type =='individual':
            # self.conversion_date=current_date
            return {
                'name': _('Opportunity'),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'crm.lead',
                'domain': [('type', '=', 'opportunity')],
                'res_id': self.id,
                'view_id': False,
                'views': [
                    (form_view.id, 'form'),
                    (tree_view.id, 'tree'),
                    (False, 'kanban'),
                    (False, 'calendar'),
                    (False, 'graph')
                ],
                'type': 'ir.actions.act_window',
                'context': {'default_type': 'opportunity'}
            }
        if self.crm_type == 'business':

            view_id=self.env['account.company']
            src = view_id.search([('company_name','=',self.business_name)])
            if src.company_name == self.business_name:
                return {
                    'name': _('Opportunity'),
                    'view_type': 'form',
                    'view_mode': 'tree, form',
                    'res_model': 'crm.lead',
                    'domain': [('type', '=', 'opportunity')],
                    'res_id': self.id,
                    'view_id': False,
                    'views': [
                        (form_view.id, 'form'),
                        (tree_view.id, 'tree'),
                        (False, 'kanban'),
                        (False, 'calendar'),
                        (False, 'graph')
                    ],
                    'type': 'ir.actions.act_window',
                    'context': {'default_type': 'opportunity'}
                }
            vals = {
                # 'checkbox_other': self.other_requirements.name,
                'company_name': self.business_name

            }
            new = view_id.with_context(active_id=self.id).create(vals)
            self.account_name_id = new
            # self.conversion_date = current_date
            return {
                'name': _('Opportunity'),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'crm.lead',
                'domain': [('type', '=', 'opportunity')],
                'res_id': self.id,
                'view_id': False,
                'views': [
                    (form_view.id, 'form'),
                    (tree_view.id, 'tree'),
                    (False, 'kanban'),
                    (False, 'calendar'),
                    (False, 'graph')
                ],
                'type': 'ir.actions.act_window',
                'context': {'default_type': 'opportunity'}
            }
    @api.multi
    def _convert_opportunity_data1(self, name, team_id=False):
        """ Extract the data from a lead to create the opportunity
            :param customer : res.partner record
            :param team_id : identifier of the sales team to determine the stage
        """
        if not team_id:
            team_id = self.team_id.id if self.team_id else False

        value = {
            # 'planned_revenue': self.planned_revenue,
            # 'probability': self.probability,
            'name': self.name,
            # 'partner_id': customer.id if customer else False,
            'type': 'opportunity',
            # 'upload_attachment_ids': self.upload_attachment_ids.id,
            'date_open': fields.Datetime.now(),
            'primary_email': self.primary_email,
            'last_name': self.last_name,
            'date_conversion': fields.Datetime.now(),
        }
        self.write(value)

        if not self.stage_id:
            stage = self._stage_find(team_id=team_id)
            value['stage_id'] = stage.id
            if stage:
                value['probability'] = stage.probability
        return value

    @api.multi
    def open_opportunity(self):
        oportunity = self.env.ref('crm.crm_case_form_view_oppor', False)
        view_id = self.env['crm.lead']
        vals = {
            # 'checkbox_other': self.other_requirements.name,
            'type': 'opportunity'

        }
        new = self.write(vals)
        return {
            'name': _('Convert Stage'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': self.id,
            'view_id': oportunity.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current'
        }

    @api.multi
    def open_consultation(self):

            oportunity = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Consultation(Warm)')])

            vals = {

                'stage_id': view_id.id
            }
            new = self.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.id,
                'view_id': oportunity.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }

    @api.multi
    def open_proposal(self):

            oportunity = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Proposal(Hot)')])

            vals = {

                'stage_id': view_id.id
            }
            new = self.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.id,
                'view_id': oportunity.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }

    @api.multi
    def open_negotiation(self):

            oportunity = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Negotiation')])

            vals = {

                'stage_id': view_id.id
            }
            new = self.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.id,
                'view_id': oportunity.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }

    @api.multi
    def open_won(self):
        oportunity = self.env.ref('pfs_crm.crm_oppor_clients_details_form_view', False)
        view_id = self.env['crm.stage'].search([('name', '=', 'Client Won')])

        vals = {

            'stage_id': view_id.id
        }
        new = self.write(vals)

        return {
            'name': _('Convert Stage'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': self.id,
            'view_id': oportunity.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current'
        }

        # res=self.env['crm.stage'].search([('name', '=', 'Client Won')])
        result.stage_id=view_id
        return result

    @api.multi
    def open_lose(self):

        oportunity = self.env.ref('crm.crm_case_form_view_oppor', False)
        view_id = self.env['crm.stage'].search([('name', '=', 'Lose')])

        vals = {

            'stage_id': view_id.id
        }
        new = self.write(vals)
        return {
            'name': _('Convert Stage'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': self.id,
            'view_id': oportunity.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current'
        }

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
            'context': {'default_recipient': self.primary_email}

        }

    @api.multi
    def send_newsletter_campaign_schedular(self):
        current_date = datetime.now()
        new_date = datetime.strftime(current_date, '%m-%d-%y')
        mail_mail = self.env['mail.mail']
        mail_ids = []
        campaign_email = self.env['crm.campaign.mail'].search([('date', '=', current_date)])
        update_date = current_date + relativedelta(days=7)
        if campaign_email:

            try:
                for rec in campaign_email:
                    if rec.leads:
                        lead_id = self.env['crm.lead'].search([('type', '=', 'lead')])
                        for id in lead_id:
                            sales_email = id.user_id.login
                            manager_email = id.team_id.user_id.login
                            name = id.name
                            subject = "Newsletter Campaign"
                            body = _("Hello,\n")
                            body += _("\tNewsletter Campaign \n")
                            footer = _("Kind regards.\n")
                            footer += _("PFS Team.\n")
                            mail_ids.append(mail_mail.create({
                                'email_to': sales_email,
                                'email_cc': manager_email,
                                'subject': subject,
                                'body_html': '<pre><span class="inner-pre" style="font-size: 15px">%s<br>%s</span></pre>' % (
                                    body, footer)
                            }))
                            mail_mail.send(mail_ids)
                    else:
                        for id in rec.leads_ids:
                            sales_email = id.user_id.login
                            manager_email = id.team_id.user_id.login
                            name = id.name
                            subject = "Newsletter Campaign"
                            body = _("Hello,\n")
                            body += _("\tNewsletter Campaign \n")
                            footer = _("Kind regards.\n")
                            footer += _("PFS Team.\n")
                            mail_ids.append(mail_mail.create({
                                'email_to': sales_email,
                                'email_cc': manager_email,
                                'subject': subject,
                                'body_html': '<pre><span class="inner-pre" style="font-size: 15px">%s<br>%s</span></pre>' % (
                                    body, footer)
                            }))
                            mail_mail.send(mail_ids)

                    if rec.opportunity:
                        oppor_id = self.env['crm.lead'].search([('type', '=', 'opportunity')])
                        for id in oppor_id:
                            sales_email = id.user_id.login
                            manager_email = id.team_id.user_id.login
                            name = id.name
                            subject = "Newsletter Campaign"
                            body = _("Hello,\n")
                            body += _("\tNewsletter Campaign \n")
                            footer = _("Kind regards.\n")
                            footer += _("PFS Team.\n")
                            mail_ids.append(mail_mail.create({
                                'email_to': sales_email,
                                'email_cc': manager_email,
                                'subject': subject,
                                'body_html': '<pre><span class="inner-pre" style="font-size: 15px">%s<br>%s</span></pre>' % (
                                    body, footer)
                            }))
                            mail_mail.send(mail_ids)
                    else:
                        for id in rec.opportunity_ids:
                            sales_email = id.user_id.login
                            manager_email = id.team_id.user_id.login
                            name = id.name
                            subject = "Newsletter Campaign"
                            body = _("Hello,\n")
                            body += _("\tNewsletter Campaign \n")
                            footer = _("Kind regards.\n")
                            footer += _("PFS Team.\n")
                            mail_ids.append(mail_mail.create({
                                'email_to': sales_email,
                                'email_cc': manager_email,
                                'subject': subject,
                                'body_html': '<pre><span class="inner-pre" style="font-size: 15px">%s<br>%s</span></pre>' % (
                                    body, footer)
                            }))
                            mail_mail.send(mail_ids)

                    sin_obj = rec.write({
                        'date': update_date
                })
                print sin_obj

            except Exception, e:
                print "Exception", e
            return None

    @api.multi
    def send_sin_schedular(self):
        current_date = datetime.now()
        new_date = datetime.strftime(current_date, '%m-%d')
        mail_mail = self.env['mail.mail']
        mail_ids = []
        sin_email = self.env['sin.schedular.setting'].search([('date', '=', current_date)])
        update_date=current_date + relativedelta(days=7)
        if sin_email:
            try:
                for val in sin_email:
                    sales_email = val.lead_id.user_id.login
                    manager_email = val.lead_id.team_id.user_id.login
                    name = val.lead_id.name
                    subject = "SIN Number Reminder"
                    body = _("Hello,\n")
                    body += _("\tField the SIN number.\n")
                    footer = _("Kind regards.\n")
                    footer += _("PFS Team.\n")
                    mail_ids.append(mail_mail.create({
                        'email_to':sales_email,
                        'email_cc':manager_email,
                        'subject': subject,
                        'body_html': '<pre><span class="inner-pre" style="font-size: 15px">%s<br>%s</span></pre>' % (
                            body, footer)
                    }))
                    mail_mail.send(mail_ids)
                    sin_obj = val.write({
                        'date':update_date
                    })
                    print sin_obj

            except Exception, e:
                print "Exception", e
            return None

    @api.multi
    def send_next_activity_schedular(self):
        current_date = datetime.now()
        new_date = datetime.strftime(current_date, '%m-%d')
        mail_mail = self.env['mail.mail']
        mail_ids = []
        next_activity = self.env['crm.lead'].search([('activity_ids.next_step', '!=', False)])
        if next_activity:
            try:
                for val in next_activity:
                    sales_email = val.user_id.login
                    manager_email = val.team_id.user_id.login
                    name = val.name
                    subject = "Next Activity Step"
                    body = _("Hello,\n")
                    body += _("\tThe next activity \n")
                    footer = _("Kind regards.\n")
                    footer += _("PFS Team.\n")
                    mail_ids.append(mail_mail.create({
                        'email_to': sales_email,
                        'email_cc': manager_email,
                        'subject': subject,
                        'body_html': '<pre><span class="inner-pre" style="font-size: 15px">%s<br>%s</span></pre>' % (
                            body, footer)
                    }))
                    mail_mail.send(mail_ids)
            except Exception, e:
                print "Exception", e
            return None


    @api.multi
    def business_end_date_schedular(self):
        current_date = datetime.now()
        new_date = datetime.strftime(current_date, '%y-%m-%d')
        mail_mail = self.env['mail.mail']
        mail_ids = []
        business_end_year = self.env['crm.lead'].search([('business_year_end', 'ilike', new_date)])
        if business_end_year:
            try:
                for val in business_end_year:
                    sales_email = val.user_id.login
                    manager_email = val.team_id.user_id.login
                    name = val.name
                    subject = "Alert expired business date"
                    body = _("Hello,\n")
                    body += _("\tyour %s\n" %(val.business_name)+"is expired on %s\n" %(val.business_year_end))
                    footer = _("Kind regards.\n")
                    footer += _("PFS Team.\n")
                    mail_ids.append(mail_mail.create({
                        'email_to': sales_email,
                        'email_cc': manager_email,
                        'subject': subject,
                        'body_html': '<pre><span class="inner-pre" style="font-size: 15px">%s<br>%s</span></pre>' % (
                        body, footer)
                    }))
                    mail_mail.send(mail_ids)
            except Exception, e:
                print "Exception", e
            return None

    @api.multi
    def send_birthday_schedular(self):
        current_date = datetime.now()
        new_date = datetime.strftime(current_date, '%m-%d')
        # crm_obj = self.env['crm.lead'].search([('primary_dob', '!=', False)])
        mail_mail = self.env['mail.mail']
        mail_ids=[]
        birthday = self.env['crm.lead'].search([('primary_dob','ilike',new_date)])
        if birthday:
            try:
                for val in birthday:
                    sales_email = val.user_id.login
                    manager_email = val.team_id.user_id.login
                    name = val.name
                    subject = "Birthday Wishes"
                    body = _("Hello,\n")
                    body += _("\tWish you Happy Birthday\n")
                    footer = _("Kind regards.\n")
                    footer += _("PFS Team.\n")
                    mail_ids.append(mail_mail.create({
                        'email_to': sales_email,
                        'email_cc': manager_email,
                        'subject': subject,
                        'body_html': '<pre><span class="inner-pre" style="font-size: 15px">%s<br>%s</span></pre>' % (body, footer)
                    }))
                    mail_mail.send(mail_ids)
            except Exception, e:
                print "Exception", e
            return None

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
                body = body.replace('--name',record.lead.name)
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

# class ContactDetail(models.Model):
#     _name = 'contact.detail'
#     _rec_name = 'opportunity_id'
#
#     contact_id=fields.Many2one('account.company',string="contacts")
#     opportunity_id = fields.Many2one('crm.lead','Contacts')

class crm_childs(models.Model):
    _name = 'crm.child'
    _rec_name = 'child_id'


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
    # product_id = fields.Many2one('crm.lead',string='Products')



class ProductDisplay(models.Model):
    _name = "product.display"
    _rec_name = 'product_name_id'

    product_id = fields.Many2one("crm.lead",string="Product_list")
    product_name_id = fields.Many2one("product.detail", string="Products")
    product_check = fields.Boolean("Choice")


class AccountCompany(models.Model):
    _name = 'account.company'
    _rec_name = 'company_name'

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
    contact_ids = fields.One2many('crm.lead',inverse_name='account_name_id',string='Contacts')







# class ContactsDetails(models.Model):
#     _name = 'contacts.details'
#     _rec_name = 'name'
#
#     contact_id=fields.Many2one('account.company','Contact')
#     name=fields.Char('Name')
#     account_name=fields.Many2one('account.company','Account Name')
#     title=fields.Text('Title')
#     department=fields.Char('Department')
#     birth_date=fields.Date('Birthdate')
#     lead_source = fields.Selection([('website', 'Website'),
#                                        ('referral', 'Referral'),
#                                        ('social_media', 'Socal Media'),
#                                        ('other', 'Other')], 'Lead Source')
#     mailing_address=fields.Char('Mailing Address')
#     created_by=fields.Char('Created By')
#     click_to_call_phone=fields.Char('Click to call phone')
#     email=fields.Char('Email')
#     phone=fields.Char('Phone')
#     mobile =fields.Char('Mobile')
#     opportunity_id=fields.Many2one('account.company','Opportunity')
#     open_activity_ids = fields.One2many(comodel_name='crm.activities', inverse_name='open_activity_id',
#                                         string='Open Activity', domain=[('state', '=', 'open')])
#     activity_history_ids = fields.One2many(comodel_name='crm.activities', inverse_name='activity_history_id',
#                                            string='Activity History', domain=[('state', '=', 'done')])



class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    upload_files_id = fields.Many2one('files.details', 'Upload Files')
    upload_attachment_id = fields.Many2one('crm.lead', 'Upload Document')
    notes = fields.Char('Notes')
    # attachments = fields.Binary("Attachments")


class ForecastsDetails(models.Model):
    _name = 'forecasts.details'


    opportunity_id=fields.Many2one('crm.lead','Opportunity Name')
    account_id=fields.Many2one('account.company','Company')
    amount=fields.Float("Possible Sales")
    close_date=fields.Date("Close Date")
    stage_id=fields.Many2one('crm.stage',string="Stage")
    profitability=fields.Char("Profitability")
    forecast_category=fields.Char("Forecast Category")
    possible_revenue=fields.Char('Possible Revenue')

    @api.onchange('opportunity_id')
    def onchange_opportunity_id(self):
        if self.opportunity_id:
            oppo_name = self.env['crm.lead'].search([('id', '=', self.opportunity_id.id)])
            self.account_id = oppo_name.account_name_id.id


class ContractsDetails(models.Model):
    _name = 'contracts.details'


    contract_number=fields.Char("Contract Number")
    contract_name=fields.Char("Contract Name")
    product_id=fields.Many2one('product.detail','Product')
    contract_start_date=fields.Date('Contract Start Date')
    contract_end_date=fields.Date('Contract End Date')
    status=fields.Selection([
        ('open', 'Open'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')],string="Status of Contract")
    contact_owner=fields.Char("Contact Owner")

class FilesDetails(models.Model):
    _name = 'files.details'
    _rec_name = 'person_id'

    person_id=fields.Many2one('crm.lead',"Person Name")
    # personal_last_name=fields.Char("Personal Last Name")
    company_id=fields.Many2one('account.company','Company Name')
    upload_files_ids = fields.One2many('ir.attachment', inverse_name='upload_files_id', string='Uploaded Files')



    @api.onchange('person_id')
    def onchange_person_id(self):
        if self.person_id:
            acc_name=self.env['crm.lead'].search([('id','=',self.person_id.id)])
            self.company_id = acc_name.account_name_id.id
            print"company_id",self.company_id


class CrmActivities(models.Model):

    _name = "crm.activities"
    _rec_name = 'crm_activity_id'

    @api.model
    def default_get(self, fields):
        result = super(CrmActivities, self).default_get(fields)
        obj = self.env['crm.lead'].search([])
        act_id = self._context.get('default_lead_id')
        record = obj.browse(act_id)
        result.update({'crm_lead_id':record.id})
        return result

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
    next_step=fields.Many2one('crm.activity',string="Next Step")

    # def open_activity_wizard(self):
    #     return {
    #         "type": "ir.actions.act_window",
    #         "res_model": "crm.activities",
    #         "views": [[False, "form"]],
    #         "res_id": self.id,
    #         "view_id": 'crm_activities_form',
    #         "target": "new",
    #     }



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

