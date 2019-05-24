from odoo import fields,models,http,_,api

class Sections(models.Model):
    _name='core.sections'

    name = fields.Char("Sections",help="Provide Section name")
    code = fields.Char("Code", help="provide Code number")

    _sql_constraints = [
        ('name_section_code_uniq', 'unique(code)', 'Code must be unique !'),
    ]
