from odoo import models, fields, api, _

class btc_export(models.Model):
    _inherit = 'product.template'

    course = fields.Char('Preparatory Course')
    study_type = fields.Selection([('post graduate', 'Post Graduate'),
                               ('post secondary', 'Post Secondary')],
                              string='Funding Source')
    course_duration = fields.Integer('Course Duration')
    study_hours = fields.Integer('Study hours per week')

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    orientation_date = fields.Date('Orientation Date')