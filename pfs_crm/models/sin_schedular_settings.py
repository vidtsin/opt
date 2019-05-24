from odoo import api, fields, models



class SinSchedular_setting(models.Model):
    _name='sin.schedular.setting'
    _rec_name = 'lead_id'




    lead_id = fields.Many2one('crm.lead','Lead')

    # sin_name = fields.Char('Name')
    # sin_last_name= fields.Char('Last Name')
    # sin_primary_email = fields.Char('Email')
    # sin_no = fields.Char('SIN')
    date = fields.Date('Schedular Date')

    @api.multi
    def unlink(self):
        print"self valueeeeeeeee", self

        sin_schedular = super(SinSchedular_setting, self).unlink()
        print"sin_schedular resulttttt", sin_schedular
        return sin_schedular