# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import time
import babel
from datetime import datetime, timedelta
from odoo import api, fields, models,tools, _
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class hr_employee(models.Model):
    _description = "Employee"
    _inherit = "hr.employee"



    doc_count = fields.Integer(compute='_get_attached_docs',string='Number of documents attached')


    @api.multi
    def attachment_tree_view(self):

        domain = ['&', ('res_model', '=', 'hr.employee'), ('res_id', 'in', [self.id])]
        res_id = self.id and self._ids[0] or False

        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, res_id)
        }





class hr_salary_rule(models.Model):
    _inherit = 'hr.salary.rule'

    is_gcc_app = fields.Boolean ('GCC Applicable')
    gcc_percent = fields.Float ('GCC variable Percent')

    @api.onchange('gcc_percent')
    def onchange_gcc_percent(self):
        if self.gcc_percent != 0.00 and self.gcc_percent:
            self.amount_select = 'code'
            gcc_percent_amount = float(self.gcc_percent/100)
            self.amount_python_compute = 'result =- (categories.BASIC + categories.ALW) *'+ str(gcc_percent_amount)

class hr_payroll_structure(models.Model):
    _inherit = 'hr.payroll.structure'

    applicable = fields.Selection([('saudi','Saudi'),
                                   ('non_saudi','Non Saudi'),('gcc','GCC')],string='Applicable for')

class hr_payslip(models.Model):
    _inherit = 'hr.payslip'


    # it will check the employee id ,date from,date to check the detail of employee and contract then create Employee salary slip in employee payslip.
    @api.onchange ('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            return

        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to

        hr_payroll_s = self.env['hr.payroll.structure']


        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(date_from, "%Y-%m-%d")))
        locale = self.env.context.get('lang', 'en_US')
        self.name = _('Salary Slip of %s for %s') % (employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
        self.company_id = employee.company_id
        gcc_countries=['Kuwait','United Arab Emirates','Qatar','Bahrain','Oman']
        if not self.env.context.get('contract') or not self.contract_id:
            contract_ids = self.get_contract(employee, date_from, date_to)
            if not contract_ids:
                return
            self.contract_id = self.env['hr.contract'].browse(contract_ids[0])
        if not self.contract_id.struct_id:
            return
        if employee.country_id:
            payroll_id = ''
            country = employee.country_id
            if country.name == 'Saudi Arabia':
                payroll_id = hr_payroll_s.search([('applicable','=','saudi')])[0]
            elif country.name in gcc_countries:
                payroll_id = hr_payroll_s.search ([('applicable', '=', 'gcc')])[0]
            else:
                payroll_id = hr_payroll_s.search ([('applicable', '=', 'non_saudi')])[0]
            self.struct_id = payroll_id.id
        else:
            self.struct_id = self.contract_id.struct_id

        #computation of the salary input

        worked_days_line_ids = self.get_worked_day_lines(contract_ids, date_from, date_to)
        worked_days_lines = self.worked_days_line_ids.browse([])
        for r in worked_days_line_ids:
            worked_days_lines += worked_days_lines.new(r)
        self.worked_days_line_ids = worked_days_lines

        input_line_ids = self.get_inputs(contract_ids, date_from, date_to)
        input_lines = self.input_line_ids.browse([])
        for r in input_line_ids:
            input_lines += input_lines.new(r)
        self.input_line_ids = input_lines

        return


