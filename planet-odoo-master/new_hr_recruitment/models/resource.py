from odoo import models, fields, api


class hr_resource(models.Model):
    _name = "hr.resource"

    name = fields.Char('Resource')
    resource_id = fields.Char('Resource ID')
    category = fields.Many2one('resource.category', string='Category')
    availability = fields.Selection([('availavle', 'Available'),
                              ('not_availavle', 'Not availavle')],
                             string='Availability')

    # this will create sequence resource id.
    @api.model
    def create(self, vals):
        if vals.get('resource_id', 'New') == 'New':
            vals['resource_id'] = self.env['ir.sequence'].next_by_code('hr.resource')
        result = super(hr_resource, self).create(vals)
        return result

