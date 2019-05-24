from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class btc_export(models.Model):
    _inherit = 'crm.lead'
    _order = 'create_date desc'

    x_program = fields.Char('Program of Interest', size=160)
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

    x_program_id = fields.Many2one('x_programs', string='Program')

    date_deadline = fields.Date('Expected Closing')
    partner_latitude = fields.Float('Geo Latitude', digits=(16, 5))
    partner_longitude = fields.Float('Geo Longitude', digits=(16, 5))
    prospect_id = fields.Integer('Prospect ID')

    comment = fields.Text('Comments')

    x_career_option = fields.Char('Career Option')
    x_qualification = fields.Char('Qualifications')
    x_prospect_id = fields.Integer('Prospect ID')

    state = fields.Selection([('draft', 'Draft'),
                              ('lost', 'Lost')],
                             string='Status', readonly=True, copy=False, index=True, default='draft')

    x_dob = fields.Date(string='Date of Birth')

    @api.multi
    def lost_lead(self):
        self.state = 'lost'




class x_programs_data(models.Model):
    _name = 'x_programs'

    x_name = fields.Char('Program Name')
    x_Domestic = fields.Boolean('offerred Domestically')
    x_international = fields.Boolean('Offerred Internationally ')



