from odoo import api, fields, models,_




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