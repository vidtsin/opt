from odoo import models, fields, api, _

class PartnerLevel(models.Model):
    _name = 'res.partner.level'
    _order = 'name'

    name = fields.Char(string='Level', translate=True)


class PartnerActive(models.Model):
    _name = 'res.partner.active'
    _order = 'name'

    name = fields.Char(string='Active', translate=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # grade_id = fields.Many2one('res.partner.level',String='Level')
    # activation = fields.Many2one('res.partner.active',String='Activation')
    partner_weight = fields.Integer('Level Weight')
    # date_review = fields.Date('Latest Partner Review')
    # date_review_next = fields.Date('Next Partner Review')
    # date_partnership = fields.Date('Partnership Date')
    assigned_partner_id = fields.Many2one('res.partner', String='Implemented by')
    office_phone_no = fields.Char('Office Phone')

    x_program = fields.Char('Program of Interest', size=160)


