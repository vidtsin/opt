from odoo import models, fields, api


class hr_salary(models.Model):
    _inherit = "hr.salary.rule.category"

    type = fields.Selection([('taxes', 'Taxes'),
                             ('insurance', 'Insurance'),
                             ('pension', 'Pension'),
                             ('federal/provincial', 'Federal/Provincial'),
                             ('unemployment', 'Unemployment'),
                             ('other', 'Other')],
                            string='Deduction Type')

    premium_type = fields.Selection([('monthly', 'Monthly'),
                                     ('quarterly', 'Quarterly'),
                                     ('annualy', 'Annualy'),
                                     ('other', 'Other')],
                                    string='Premium Type')


    other_premium_type = fields.Char('Define Premium Type')
