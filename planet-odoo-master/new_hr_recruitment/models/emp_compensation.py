from odoo import models, fields, api


class emp_compensation(models.Model):
    _name = "emp.compensation"

    name = fields.Many2one('hr.employee', string='Employee')
    hours = fields.Char('Hours')
    approver = fields.Many2one('res.users', string='Approver')
    date = fields.Date('Date')

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('rejected', 'Rejected'),
                              ('approved', 'Approved'),
                              ('completed', 'Completed')],
                             string='Status', readonly=True, copy=False, index=True, default='draft')

    description = fields.Text('Description')
    journal_type = fields.Many2one('account.journal', string='Journal Type')
    compensation_type = fields.Char('Compensation Type')
    amount = fields.Float('Amount')
    compensation_date = fields.Date('Compensation Date')



    @api.multi
    def compensation_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def compensation_reject(self):
        self.state = 'rejected'

    @api.multi
    def compensation_approve(self):
        self.state = 'approved'

    @api.multi
    def reset_draft(self):
        self.state = 'draft'


    @api.multi
    def compensatory_work(self):
        self.state = 'completed'
