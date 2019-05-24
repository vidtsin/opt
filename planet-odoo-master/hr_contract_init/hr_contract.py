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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import netsvc
from odoo.addons import decimal_precision as dp
from odoo import fields,models,api,_
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT
from odoo.tools.translate import _
from odoo.exceptions import UserError


class contract_init(models.Model):

    _name = 'hr.contract.init'
    _description = 'Initial Contract Settings'

    _inherit = 'ir.needaction_mixin'

    # _columns = {
    name= fields.Char('Name', size=64, required=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    date= fields.Date('Effective Date', required=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    wage_ids= fields.One2many('hr.contract.init.wage', 'contract_init_id',
                                'Starting Wages', readonly=True,
                                states={'draft': [('readonly', False)]})
    struct_id= fields.Many2one('hr.payroll.structure', 'Payroll Structure', readonly=True,
                                 states={'draft': [('readonly', False)]})
    trial_period= fields.Integer('Trial Period', readonly=True,
                                   states={'draft': [('readonly', False)]},
                                   help="Length of Trial Period, in days",default=0)
    active= fields.Boolean('Active',default=True)
    state= fields.Selection([('draft', 'Draft'),
                               ('approve', 'Approved'),
                               ('decline', 'Declined')], 'State', readonly=True,default='draft')


    # Return records with latest date first
    _order = 'date desc'

    @api.model
    def _needaction_domain_get(self):

        users_obj = self.env['res.users']
        domain = []

        if users_obj.has_group('base.group_hr_director'):
            domain = [('state', 'in', ['draft'])]
            return domain

        return False

    @api.multi
    def unlink(self):
        ids = self._ids[0]
        if isinstance(ids, (int, long)):
            ids = [ids]
        data = self.read(ids, ['state'])
        for d in data:
            if d['state'] in ['approve', 'decline']:
                raise UserError(_('You may not a delete a record that is not in a "Draft" state'))
        return super(contract_init, self).unlink(ids)

    @api.multi
    def set_to_draft(self):
        self.write({'state':'draft'})
        return True

    @api.multi
    def state_approve(self):
        self.write({'state': 'approve'})
        # return True

    @api.multi
    def state_decline(self):
        self.write({'state': 'decline'})
        # return True


class init_wage(models.Model):

    _name = 'hr.contract.init.wage'
    _description = 'Starting Wages'

    job_id = fields.Many2one('hr.job', 'Job')
    starting_wage = fields.Float('Starting Wage', digits_compute=dp.get_precision('Payroll'),
                                  required=True)
    is_default = fields.Boolean('Use as Default',help="Use as default wage")
    contract_init_id = fields.Many2one('hr.contract.init', 'Contract Settings')
    category_ids = fields.Many2many('hr.employee.category', 'contract_init_category_rel', 'contract_init_id', 'category_id', 'Tags')


    _sql_constraints = [('unique_job_cinit', 'UNIQUE(job_id,contract_init_id)', _(
        'A Job Position cannot be referenced more than once in a Contract Settings record.'))]

    @api.multi
    def unlink(self):
        ids = self._ids[0]
        if isinstance(ids, (int, long)):
            ids = [ids]
        data = self.contract_init_id
        for d in data:
            if not d.get('contract_init_id', False):
                continue
            d2 = self.pool.get( 'hr.contract.init').read(d['contract_init_id'][0],['state'])
            if d2['state'] in ['approve', 'decline']:
                raise UserError(_('You may not a delete a record that is not in a "Draft" state'))
        return super(init_wage, self).unlink()


class hr_contract(models.Model):

    _inherit = 'hr.contract'

    @api.multi
    def _get_wage(self,job_id=None):

        res = 0
        default = 0
        init = self.get_latest_initial_values()
        if job_id:
            catdata = self.env['hr.job'].read(job_id, ['category_ids'])
        else:
            catdata = False
        if init != None:
            for line in init.wage_ids:
                if job_id != None and line.job_id.id == job_id:
                    res = line.starting_wage
                elif catdata:
                    cat_id = False
                    category_ids = [c.id for c in line.category_ids]
                    for ci in catdata['category_ids']:
                        if ci in category_ids:
                            cat_id = ci
                            break
                    if cat_id:
                        res = line.starting_wage
                if line.is_default and default == 0:
                    default = line.starting_wage
                if res != 0:
                    break
        if res == 0:
            res = default
        return res

    @api.multi
    def _get_struct(self, cr, uid, context=None):

        res = False
        init = self.get_latest_initial_values(cr, uid, context=context)
        if init != None and init.struct_id:
            res = init.struct_id.id
        return res

    @api.multi
    def _get_trial_date_start(self):

        res = False
        init = self.get_latest_initial_values()
        if init != None and init.trial_period and init.trial_period > 0:
            res = datetime.now().strftime(OE_DFORMAT)
        return res

    @api.multi
    def _get_trial_date_end(self):

        res = False
        init = self.get_latest_initial_values()
        if init != None and init.trial_period and init.trial_period > 0:
            dEnd = datetime.now().date() + timedelta(days=init.trial_period)
            res = dEnd.strftime(OE_DFORMAT)
        return res

    _defaults = {
        'wage': _get_wage,
        'struct_id': _get_struct,
        'trial_date_start': _get_trial_date_start,

    }


    @api.multi
    def onchange_job(self, job_id):

        res = False
        if job_id:
            wage = self._get_wage(job_id=job_id)
            res = {'value': {'wage': wage}}
        return res

    @api.multi
    @api.onchange('trial_date_start')
    def onchange_trial(self):

        res = {'value': {'trial_date_end': False}}

        init = self.get_latest_initial_values()
        if init != None and init.trial_period and init.trial_period > 0:
            dStart = datetime.strptime(self.trial_date_start, OE_DFORMAT)
            dEnd = dStart + timedelta(days=init.trial_period)
            res['value']['trial_date_end'] = dEnd.strftime(OE_DFORMAT)

        return res

    # '''Return a record with an effective date before today_str but greater than all others'''
    @api.multi
    def get_latest_initial_values(self, today_str=None):

        init_obj = self.env['hr.contract.init']
        if today_str == None:
            today_str = datetime.now().strftime(OE_DFORMAT)
        dToday = datetime.strptime(today_str, OE_DFORMAT).date()

        res = None
        ids = init_obj.search([('date', '<=', today_str), ('state', '=', 'approve')])
        # for init in init_obj.browse(cr, uid, ids, context=context):
        for init in ids:
            d = datetime.strptime(init.date, OE_DFORMAT).date()
            if d <= dToday:
                if res == None:
                    res = init
                elif d > datetime.strptime(res.date, OE_DFORMAT).date():
                    res = init

        return res