from odoo import api, fields, models,_
from dateutil.relativedelta import relativedelta
from datetime import date,datetime


class crm_activities_new(models.Model):
    _name='pfs.crm.activites'



    lead=fields.Many2one('crm.lead',string="Leads")
    activity=fields.Many2one('crm.activity',string='Activities')
    # activity_date=fields.Date('Activity Date')
    email=fields.Char('Email Id')
    h_filing=fields.Selection([('monthly','Monthly'),
                               ('quarterly','Quarterly'),
                               ('annually', 'Annually')], 'HST Filing Frequency')
    h_filing_date=fields.Date('HST Filing Date')
    p_filing=fields.Selection([('monthly', 'Monthly'),
                               ('quarterly', 'Quarterly'),
                               ('annually', 'Annually')], 'Payroll Filing Frequency')
    p_filing_date=fields.Date("Payroll Filing Date")









    @api.multi
    def delete_records(self):
        current_date=datetime.now()
        new_date=datetime.strftime(current_date,'%Y-%m-%d')
        payroll_template=self.env['mail.template'].search([('name', '=', 'Payroll Expiry Notification')])
        hst_template = self.env['mail.template'].search([('name', '=', 'Hst Expiry Notification')])
        if new_date==self.h_filing_date:
            body = hst_template.body_html
            body = body.replace('--first_name',self.lead.first_name)
            body = body.replace('--last_name',self.lead.last_name)
            body = body.replace('--business_name',self.lead.business_name)
            body = body.replace('--business_no',self.lead.business_number)
            body = body.replace('--hst_date', self.lead.hst_filing_date)
            body = body.replace('--hst_frequency',self.lead.hst_filing)
            mail_values = {
                'subject': hst_template.subject,
                'body_html': body,
                'email_to': self.email,

            }
            create_and_send_email=self.env['mail.mail'].create(mail_values).send()
            if self.h_filing == 'monthly':
                filing_date=self.h_filing_date
                new_filing_date=datetime.strptime(filing_date,'%Y-%m-%d')
                update_date=new_filing_date+relativedelta(months=1)
                self.lead.write({
                    'hst_filing_date': update_date,
                })
            if self.h_filing == 'quarterly':
                filing_date = self.h_filing_date
                new_filing_date = datetime.strptime(filing_date, '%Y-%m-%d')
                update_date=new_filing_date+relativedelta(months=3)
                self.lead.write({
                    'hst_filing_date': update_date,
                })
            if self.h_filing =='annually':
                filing_date = self.h_filing_date
                new_filing_date = datetime.strptime(filing_date, '%Y-%m-%d')
                update_date= new_filing_date+relativedelta(months=12)
                self.lead.write({
                    'hst_filing_date': update_date,
                })
            self.unlink()

        else:
            if new_date==self.p_filing_date:
                body = payroll_template.body_html
                body = body.replace('--first_name', self.lead.first_name)
                body = body.replace('--last_name', self.lead.last_name)
                body = body.replace('--business_name', self.lead.business_name)
                body = body.replace('--business_no', self.lead.business_number)
                body = body.replace('--payroll_date', self.lead.payroll_filing_date)
                body = body.replace('--payroll_frequency', self.lead.payroll_filing)
                mail_values = {
                    'subject': payroll_template.subject,
                    'body_html': body,
                    'email_to': self.email,

                }
                create_and_send_email = self.env['mail.mail'].create(mail_values).send()
                if self.p_filing == 'monthly':
                    filing_date = self.p_filing_date
                    new_filing_date = datetime.strptime(filing_date, '%Y-%m-%d')
                    update_date=new_filing_date+relativedelta(months=1)
                    self.lead.write({
                        'payroll_filing_date': update_date,
                    })
                if self.p_filing == 'quarterly':
                    filing_date = self.p_filing_date
                    new_filing_date = datetime.strptime(filing_date, '%Y-%m-%d')
                    update_date=new_filing_date+relativedelta(months=3)
                    self.lead.write({
                        'payroll_filing_date': update_date,
                    })
                if self.p_filing =='annually':
                    filing_date = self.p_filing_date
                    new_filing_date = datetime.strptime(filing_date, '%Y-%m-%d')
                    update_date= new_filing_date+relativedelta(months=12)
                    self.lead.write({
                        'payroll_filing_date': update_date,
                    })
                self.unlink()











