from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class ethnic_classify(models.Model):
    _name = 'ethnic.classify'

    name = fields.Char('Category Name')
    descrp = fields.Text('Description of the category')
    country_ids = fields.Many2many('res.country',string = 'Countries/Regions')

class hr_employee(models.Model):
    _inherit = 'hr.employee'

    ethnic_grp = fields.Many2one('ethnic.classify',string = 'Ethnic group')



