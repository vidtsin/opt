from odoo import api, fields, models
from datetime import date,datetime
from dateutil.relativedelta import relativedelta



class CrmCampaigntMail(models.Model):
    _name='crm.campaign.mail'

    leads = fields.Boolean("Send mail to all leads")
    opportunity = fields.Boolean("Send mail to all opportunity")
    leads_ids = fields.Many2many('crm.lead', string='Leads', domain=[('type', '=', 'lead')])
    opportunity_ids = fields.Many2many('crm.lead', string='Opportunity', domain=[('type', '=', 'opportunity')])
    recipents = fields.Char(string='Recipents')
    subject = fields.Char(string="subject")
    body = fields.Html('Contents')
    date = fields.Date("Date")

    @api.multi
    def newsletter_send_mail(self):
            if self.leads:
                lead_id = self.env['crm.lead'].search([('type', '=', 'lead')])
                for rec in lead_id:
                    # self.recipents = rec.primary_email
                    if not self.subject:
                        subject = "Direct mail."
                        mail_values = {
                            'subject': subject,
                            'body_html': self.body,
                            'email_to': rec.user_id.login,
                            'email_cc': rec.team_id.user_id.login,

                        }
                        create_and_send_email = self.env['mail.mail'].create(mail_values).send()

                    else:

                        mail_values = {
                            'subject': self.subject,
                            'body_html': self.body,
                            'email_to': rec.user_id.login,
                            'email_cc': rec.team_id.user_id.login,

                        }
                        create_and_send_email = self.env['mail.mail'].create(mail_values).send()


            else:
                for rec in self.leads_ids:
                    if not self.subject:
                        subject = "Direct mail ."
                        mail_values = {
                            'subject': subject,
                            'body_html': self.body,
                            'email_to': rec.user_id.login,
                            'email_cc': rec.team_id.user_id.login,

                        }
                        create_and_send_email = self.env['mail.mail'].create(mail_values).send()

                    else:

                        mail_values = {
                            'subject': self.subject,
                            'body_html': self.body,
                            'email_to': rec.user_id.login,
                            'email_cc': rec.team_id.user_id.login,

                        }
                        create_and_send_email = self.env['mail.mail'].create(mail_values).send()

            if self.opportunity:
                oppor_id = self.env['crm.lead'].search([('type', '=', 'opportunity')])
                for rec in oppor_id:
                    # self.recipents = rec.primary_email
                    if not self.subject:
                        subject = "Direct mail."
                        mail_values = {
                            'subject': subject,
                            'body_html': self.body,
                            'email_to': rec.user_id.login,
                            'email_cc': rec.team_id.user_id.login,

                        }
                        create_and_send_email = self.env['mail.mail'].create(mail_values).send()

                    else:

                        mail_values = {
                            'subject': self.subject,
                            'body_html': self.body,
                            'email_to': rec.user_id.login,
                            'email_cc': rec.team_id.user_id.login,

                        }
                        create_and_send_email = self.env['mail.mail'].create(mail_values).send()



            else:
                for rec in self.opportunity_ids:
                    if not self.subject:
                        subject = "Direct mail ."
                        mail_values = {
                            'subject': subject,
                            'body_html': self.body,
                            'email_to': rec.user_id.login,
                            'email_cc': rec.team_id.user_id.login,

                        }
                        create_and_send_email = self.env['mail.mail'].create(mail_values).send()

                    else:

                        mail_values = {
                            'subject': self.subject,
                            'body_html': self.body,
                            'email_to': rec.user_id.login,
                            'email_cc': rec.team_id.user_id.login,

                        }
                        create_and_send_email = self.env['mail.mail'].create(mail_values).send()

            current_date = datetime.now()
            self.date = current_date + relativedelta(days=7)
            return {'type': 'ir.actions.act_window_close'}

