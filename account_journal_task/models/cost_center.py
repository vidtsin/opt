from odoo import fields,models,http,_,api

class CostCenter(models.Model):
    _name='core.cost.center'
    
    name = fields.Char("Cost Center",help="Provide Department name")
    code = fields.Char("Code", help="provide Code number")

    _sql_constraints = [
        ('name_cost_code_uniq', 'unique(code)', 'Code must be unique !'),
    ]

