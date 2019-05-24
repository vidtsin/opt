from odoo import models, fields, api


class compensation_type(models.Model):
    _name = "compensation.type"

    name = fields.Char('Compensation Type')
    journal_type = fields.Many2one('account.journal', string='Journal Type')
    amount = fields.Float('Amount')
