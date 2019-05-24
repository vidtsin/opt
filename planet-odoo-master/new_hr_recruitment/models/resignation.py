from odoo import models, fields, api


class emp_resignation(models.Model):
    _name = "emp.resignation"
    _rec_name ="employee"

    employee = fields.Many2one('hr.employee',string='Employee')
    relieving_type = fields.Selection([('resignation', 'Resignation'),
                              ('termination', 'Termination'),
                              ('bgv fails', 'BGV Fails'),
                              ('absconding', 'Absconding')],
                                      string='Relieving Type')

    reporting_manager = fields.Char('Reporting Manager')
    relieving_date = fields.Date('Relieving Date')
    relieving_request_created_by = fields.Char('Relieving Request Created By')
    relieving_created_date = fields.Date('Relieving Request Date')
    company = fields.Many2one('res.company',string='Company')
    department = fields.Char('Department')
    inform_rm_hr = fields.Boolean('Informed RM and HR')
    exit_policy = fields.Boolean('Exit Policy Verification')
    approved_notice_period = fields.Boolean('Notice Period Approved')
    exit_clearance_provided = fields.Boolean('Exit Clearance Form Provided', default=True)
    admin_clearance = fields.Boolean('Admin Clearance')
    finance_clearance = fields.Boolean('Finance Clearance')
    it_clearance = fields.Boolean('IT Clearance')
    exit_clearance_received = fields.Boolean('Exit Clearance Form Received')
    provide_document = fields.Boolean('Provide Relieving Document')
    test = fields.Boolean('make visible', default=False)

    state = fields.Selection([('new', 'New'),
                              ('in_progress', 'In Progress'),
                              ('completed', 'Completed'),
                              ('rejected', 'Rejected')],
                             string='Status', readonly=True, copy=False, index=True, default='new')

    @api.multi
    def resign_in_progress(self):
        self.state = 'in_progress'

    @api.multi
    def view_clearance(self):
        self.state = 'in_progress'

    @api.multi
    def view_clearance(self):
        self.test = 'True'

    @api.multi
    def resign_reject(self):
        self.state = 'rejected'

    @api.multi
    def resign_approve(self):
        self.state = 'completed'

    @api.multi
    def reset_new(self):
        self.state = 'new'






