from odoo import models, fields, api

class bank_details(models.Model):
    _inherit = "account.journal"

    state_id = fields.Many2one('res.country.state', 'state_id')
    country_id = fields.Many2one('res.country', 'country_id')
    city = fields.Char('City')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip')
    pan_code = fields.Char('PAN Code')
    ifsc_code = fields.Char('IFSC Code')

