from odoo import fields,models,http,_,api

class Departments(models.Model):
    _name='core.departments'
    
    name = fields.Char("Department",help="Provide Department name")
    code = fields.Char("Code", help="provide Code number")

    _sql_constraints = [
        ('name_department_code_uniq', 'unique(code)', 'Code must be unique !'),
    ]
   