from odoo import models, fields, api, _

class btc_stage(models.Model):
    _inherit = 'crm.stage'

    type = fields.Selection([('lead', 'Lead'),
                               ('opportunity', 'Opportunity'),
                               ('both', 'Both')],
                              string='Type')



