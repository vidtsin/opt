
from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit='res.users'

    parent_id=fields.Many2one('res.users',string='Manager')

class CrmLead(models.Model):
    _inherit = 'crm.lead'


