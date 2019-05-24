#-*- coding:utf-8 -*-
#
#
#    Copyright (C) 2013 Michael Telahun Makonnen <mmakonnen@gmail.com>.
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

import time

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import netsvc
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import fields,models,api,_


class hr_contract(models.Model):

    _name = 'hr.contract'
    _inherit = ['hr.contract', 'mail.thread', 'ir.needaction_mixin','hr.contract']

    @api.multi
    def _get_ids_from_employee(self):
        res = []
        for ee in self.employee_id:
            for contract in ee.contract_ids:
                if contract.state not in ['pending_done', 'done']:
                    res.append(contract.id)
        return res

    @api.multi
    def _get_department(self):
        ids = self
        res = dict.fromkeys(ids, False)
        for contract in self:
            if contract.department_id and contract.state in ['pending_done', 'done']:
                res[contract.id] = contract.department_id.id
            elif contract.employee_id.department_id:
                res[contract.id] = contract.employee_id.department_id.id
        return res


    state = fields.Selection([('draft', 'Draft'),
                                   ('trial', 'Trial'),
                                   ('trial_ending', 'Trial Period Ending'),
                                   ('open', 'Open'),
                                   ('contract_ending', 'Ending'),
                                   ('pending_done', 'Pending Termination'),
                                   ('done', 'Completed')],
                                  'State',readonly=True,default='draft')

        # store this field in the database and trigger a change only if the contract is
        # in the right state: we don't want future changes to an employee's department to
        # impact past contracts that have now ended. Increased priority to
        # override hr_simplify.
    department_id = fields.Many2one('hr.department',compute='_get_department', method=True,
                                     string="Department", readonly=True,)
                                     # store={'hr.employee': (_get_ids_from_employee, ['department_id'], 10)})

        # At contract end this field will hold the job_id, and the
        # job_id field will be set to null so that modules that
        # reference job_id don't include deactivated employees.
    end_job_id = fields.Many2one('hr.job', 'Job Title', readonly=True)

        # The following are redefined again to make them editable only in
        # certain states
    employee_id = fields.Many2one('hr.employee', "Employee", required=True, readonly=True,
                                       states={'draft': [('readonly', False)]})
    type_id = fields.Many2one('hr.contract.type', "Contract Type", required=True, readonly=True,
                               states={'draft': [('readonly', False)]})
    date_start = fields.Date('Start Date', required=True, readonly=True,
                              states={'draft': [('readonly', False)]})
    wage = fields.Float('Wage', digits=(16, 2), required=True, readonly=True,
                             states={'draft': [('readonly', False)]},
                             help="Basic Salary of the employee")




    @api.model
    def _needaction_domain_get(self):
        users_obj = self.env['res.users']
        domain = []
        if users_obj.has_group('base.group_hr_manager'):
            domain = [('state', 'in', ['draft', 'contract_ending', 'trial_ending'])]
            return domain
        return False

    @api.onchange('job_id')
    def onchange_job(self):
        if self.job_id:
            ids = self._ids
            import logging
            _l = logging.getLogger(__name__)
            _l.warning('hr_contract_state: onchange_job()')
            res = False
            if ids:
                if self.state != 'draft':
                    return res


    @api.multi
    def condition_trial_period(self):
        for contract in self:
            if not contract.trial_date_start:
                return False
        return True
    @api.multi
    def try_signal_ending_contract(self):
        d = datetime.now().date() + relativedelta(days=+30)
        ids = self.search([('state', '=', 'open'),('date_end', '<=', d.strftime(DEFAULT_SERVER_DATE_FORMAT))])
        if len(ids) == 0:
            return

        for contract in self:
            contract.write({'state':'contract_ending'})

        return

    @api.multi
    def try_signal_contract_completed(self):
        d = datetime.now().date()
        ids = self.search([('state', '=', 'open'),('date_end', '<', d.strftime(DEFAULT_SERVER_DATE_FORMAT)) ])
        if len(ids) == 0:
            return

        for contract in self:
            contract.write ({'state': 'pending_done'})

        return


    @api.multi
    def try_signal_ending_trial(self):

        d = datetime.now().date() + relativedelta(days=+10)
        ids = self.search([('state','=', 'trial'),('trial_date_end','<=', d.strftime(DEFAULT_SERVER_DATE_FORMAT))])
        if len(ids) == 0:
            return

        for contract in self:
            contract.write ({'state': 'trial_ending'})

        return


    @api.multi
    def try_signal_open(self):
        d = datetime.now().date() + relativedelta(days=-5)
        ids = self.search([('state', '=', 'trial_ending'),('trial_date_end', '<=', d.strftime(DEFAULT_SERVER_DATE_FORMAT))])
        if len(ids) == 0:
            return

        for contract in self:
            contract.write ({'state': 'open'})

        return

    @api.onchange('date_start')
    def onchange_start(self):
        res = {'value': {}}
        res['value']['trial_date_start'] = self.date_start

        return res

    @api.multi
    def state_trial(self):
        self.write({'state': 'trial'})
        return True

    @api.multi
    def state_open(self):

        self.write({'state': 'open'})
        return True

    @api.multi
    def state_pending_done(self):

        self.write({'state': 'pending_done'})
        return True

    @api.multi
    def state_done(self):

        for i in self:
            data = i.read(['date_end', 'job_id'])
            vals = {'state': 'done',
                    'date_end': False,
                    'job_id': False,
                    'end_job_id': data['job_id'][0]}

            if data.get('date_end', False):
                vals['date_end'] = data['date_end']
            else:
                vals['date_end'] = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

            self.write(vals)

        return True
