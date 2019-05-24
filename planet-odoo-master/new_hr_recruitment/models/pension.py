from odoo import models, fields, api

class emp_pension(models.Model):
    _name = "emp.pension"
    _rec_name = "employee"

    employee = fields.Many2one('hr.employee')
    spouse = fields.Char('Spouse')
    date_start = fields.Date('Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date('End Date')
    department = fields.Many2one('hr.department',string='Department')
    job_title = fields.Many2one('hr.job',string='Job Title')
    fixed_amount = fields.Float('Fixed Amount')
    schedule_pay = fields.Selection([('monthly', 'Monthly'),
                              ('quarterly', 'Quarterly'),
                              ('semi-annually', 'Semi-annually'),
                              ('annually', 'Annually')],
                                 string='Scheduled Pay', default='monthly')
    pension_journal = fields.Many2one('account.journal', string='Pension Journal')
