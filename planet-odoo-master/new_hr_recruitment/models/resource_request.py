from odoo import models, fields, api


class resource_request(models.Model):
    _name = "resource.request"


    resource = fields.Many2one('hr.resource')
    name = fields.Char('Request No')
    image = fields.Binary("Photo", attachment=True)
    requestor = fields.Many2one('res.users',string='Requested By')
    resource_manager = fields.Many2one('hr.employee',string='Resource Manager')
    state = fields.Selection([('draft', 'Draft'),
                              ('waiting_for_approval', 'Waiting for approval'),
                              ('pending', 'Pending'),
                              ('cancelled', 'Cancelled'),
                              ('approved', 'Approved')],
                             string='Status', readonly=True, copy=False, index=True, default='draft')

    members_data = fields.One2many('resource.members', 'resource_member_id', String="Members Data")
    priority = fields.Selection([('low', 'Low'),
                                 ('high', 'High'),
                                 ('medium', 'Medium')],
                                string='Priority')
    purpose = fields.Text('Purpose')

    @api.multi
    def request_for_resource(self):
        self.state = 'waiting_for_approval'

    @api.multi
    def request_cancelled(self):
        self.state = 'cancelled'

    @api.multi
    def request_approved(self):
        self.state = 'approved'

    @api.multi
    def request_pending(self):
        self.state = 'pending'

    @api.multi
    def reset_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('resource.request')
        result = super(resource_request, self).create(vals)
        return result




