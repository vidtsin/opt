from odoo import models, fields, api


class resource_category(models.Model):
    _name = "resource.category"


    name = fields.Char('Category')
    category_id = fields.Char('Category Code')

    # this function will create category id in sequence.
    @api.model
    def create(self, vals):
        if vals.get('category_id', 'New') == 'New':
            vals['category_id'] = self.env['ir.sequence'].next_by_code('resource.category')
        result = super(resource_category, self).create(vals)
        return result