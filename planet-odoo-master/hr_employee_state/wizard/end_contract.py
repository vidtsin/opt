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

from datetime import datetime

from odoo import netsvc
from odoo import fields, models,api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class employee_set_inactive(models.TransientModel):

    _name = 'hr.contract.end'
    _description = 'Employee De-Activation Wizard'

    @api.multi
    def _get_contract(self):
        context = self._context
        if context == None:
            context = {}

        return context.get ('end_contract_id', False)

    @api.multi
    def _get_employee(self):
        context = self._context
        if context == None:
            context = {}

        contract_id = context.get ('end_contract_id', False)
        if not contract_id:
            return False

        data = self.env['hr.contract'].read (contract_id, ['employee_id'])
        return data['employee_id'][0]

    contract_id = fields.Many2one('hr.contract', 'Contract', readonly=True,default=_get_contract)
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True, readonly=True,default=_get_employee)
    date = fields.Date('Date', required=True,default = datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT))
    reason_id = fields.Many2one('hr.employee.termination.reason', 'Reason', required=True)
    notes = fields.Text('Notes')

    #
    # _defaults = {
    #     'date': datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT),
    #     'employee_id': _get_employee,
    #     'contract_id': _get_contract,
    # }

    @api.multi
    def set_employee_inactive(self):

        data = self.read(['employee_id', 'contract_id', 'date', 'reason_id', 'notes'])
        vals = {
            'name': data['date'],
            'employee_id': data['employee_id'][0],
            'reason_id': data['reason_id'][0],
            'notes': data['notes'],
        }

        contract_obj = self.env['hr.contract']
        contract = contract_obj.browse(data['contract_id'][0])
        contract_obj.setup_pending_done(contract, vals)

        return {'type': 'ir.actions.act_window_close'}
