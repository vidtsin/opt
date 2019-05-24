from odoo import models, fields, api


class salary_contract(models.Model):
    _inherit = "hr.contract"

    pay_type = fields.Selection([('hourly','Hourly'),
                                 ('salary','Salary'),
                                 ('salary/exempt','Salary/exempt')],
                                string='Pay Type')

    vacation_per_year = fields.Char('Vacation per year(In hours)')
    pay_rate = fields.Float('Pay rate(Hourly)')
    vacation_used = fields.Char('Vacation used')

    sick_leave_per_year = fields.Char('Sick leave per year(In hours)')
    pay_rate_on_sick_leave = fields.Float('Pay Rate(Hourly)')
    sick_leave_used = fields.Char('Sick Leave Used')

    insurance_id = fields.Char('Insurance/ Security ID')