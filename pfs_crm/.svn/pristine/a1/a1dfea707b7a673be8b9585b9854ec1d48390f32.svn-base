from odoo import api, fields, models



class CrmDirectMail(models.TransientModel):
    _name='crm.direct.mail'

    leads = fields.Boolean("Send mail to all leads")
    opportunity = fields.Boolean("Send mail to all opportunity")
    leads_ids = fields.Many2many('crm.lead', string='Leads', domain=[('type','=','lead')])
    opportunity_ids = fields.Many2many('crm.lead', string='Opportunity', domain=[('type','=','opportunity')])
    recipents = fields.Char(string='Recipents')
    subject = fields.Char(string="subject")
    body = fields.Html('Contents')

    # @api.onchange('leads_ids')
    # def onchange_lead_email_send(self):
    #     if self.leads_ids:
    #         leads=[]
    #         for rec in self.leads_ids:
    #             lead_tuple=rec.primary_email
    #             leads.append(lead_tuple)
    #
    #         self.recipents_ids=leads
    #
    #
    #         print"receipent",self.recipents_ids


    @api.multi
    def send_mail(self):
        if self.leads:
            lead_id = self.env['crm.lead'].search([('type', '=','lead')])
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
                    subject="Direct mail ."
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
            oppor_id = self.env['crm.lead'].search([('type', '=','opportunity')])
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
                    subject="Direct mail ."
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


        return {'type': 'ir.actions.act_window_close'}