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

from odoo import fields,models,api,_
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.translate import _
from odoo.exceptions import UserError


class hr_infraction_category(models.Model):

    _name = 'hr.infraction.category'
    _description = 'Infraction Type'


    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)



class hr_infraction(models.Model):

    _name = 'hr.infraction'
    _description = 'Infraction'

    _inherit = ['mail.thread', 'ir.needaction_mixin']

    # _columns = {
    name = fields.Char('Subject', size=256, required=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    date = fields.Date('Date', required=True, readonly=True,
                        states={'draft': [('readonly', False)]},default=time.strftime(DEFAULT_SERVER_DATE_FORMAT))
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True, readonly=True,
                                   states={'draft': [('readonly', False)]})
    category_id = fields.Many2one('hr.infraction.category', 'Category', required=True,
                                   readonly=True, states={'draft': [('readonly', False)]})
    action_ids = fields.One2many('hr.infraction.action', 'infraction_id', 'Actions',readonly=True)
    memo = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                               ('confirm', 'Confirmed'),
                               ('action', 'Actioned'),
                               ('noaction', 'No Action'),
                               ],
                              'State', readonly=True,default='draft')
    # }


    @api.model
    def _needaction_domain_get(self):

        users_obj = self.env['res.users']

        domain = []
        if users_obj.has_group('hr.group_hr_manager'):
            domain = [('state', '=', 'confirm')]

        if len(domain) == 0:
            return False

        return domain

    # for delete hr infraction.
    @api.multi
    def unlink(self):
        for infraction in self:
            if infraction.state not in ['draft']:
                raise UserError(_('Infractions that have progressed beyond "Draft" state may not be removed.'))
        return super(hr_infraction, self).unlink()


    @api.onchange('category_id')
    def onchange_category(self):
        res = {'value': {'name': False}}
        if self.category_id:
            res['value']['name'] = self.category_id.name
        return res

ACTION_TYPE_SELECTION = [
    ('warning_verbal', 'Verbal Warning'),
    ('warning_letter', 'Written Warning'),
    ('transfer', 'Transfer'),
    ('suspension', 'Suspension'),
    ('dismissal', 'Dismissal'),
]


class hr_infraction_action(models.Model):

    _name = 'hr.infraction.action'
    _description = 'Action Based on Infraction'

    infraction_id = fields.Many2one('hr.infraction', 'Infraction', ondelete='cascade',
                                     required=True, readonly=True)
    type = fields.Selection(ACTION_TYPE_SELECTION, 'Type', required=True)
    memo = fields.Text('Notes')
    employee_id = fields.Many2one('hr.employee',related='infraction_id.employee_id', store=True,
                                   string='Employee', readonly=True)
    warning_id = fields.Many2one('hr.infraction.warning', 'Warning', readonly=True)
    transfer_id = fields.Many2one('hr.department.transfer', 'Transfer', readonly=True)
    

    _rec_name = 'type'
    @api.multi
    def unlink(self):
        for action in self:
            if action.infraction_id.state not in ['draft']:
                raise UserError(_('Actions belonging to Infractions not in "Draft" state may not be removed.'))
        return super(hr_infraction_action, self).unlink()


class hr_warning(models.Model):

    _name = 'hr.infraction.warning'
    _description = 'Employee Warning'

    name = fields.Char('Subject', size=256)
    date = fields.Date('Date Issued',default=time.strftime(DEFAULT_SERVER_DATE_FORMAT))
    type = fields.Selection([('verbal', 'Verbal'), ('written', 'Written')], 'Type',required=True,default='written')
    action_id = fields.Many2one('hr.infraction.action', 'Action', ondelete='cascade',readonly=True)
    infraction_id = fields.Many2one('hr.infraction',related='action_id.infraction_id',string='Infraction', readonly=True)
    employee_id = fields.Many2one('hr.employee',related='infraction_id.employee_id', string='Employee', readonly=True)
    


    @api.multi
    def unlink(self):
        for warning in self:
            if warning.action_id and warning.action_id.infraction_id.state not in ['draft']:
                raise UserError(_('Warnings attached to Infractions not in "Draft" state may not be removed.'))

        return super(hr_warning, self).unlink()


class hr_employee(models.Model):

    # _name = 'hr.employee'
    _inherit = 'hr.employee'


    infraction_ids = fields.One2many('hr.infraction', 'employee_id', 'Infractions',readonly=True)
    infraction_action_ids = fields.One2many('hr.infraction.action','employee_id','Disciplinary Actions',readonly=True)

