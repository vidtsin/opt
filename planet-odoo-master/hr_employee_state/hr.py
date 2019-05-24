#-*- coding:utf-8 -*-

#


import time

from datetime import datetime

from odoo import netsvc
from odoo import fields, models,api,_
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.translate import _
from odoo.exceptions import UserError


class hr_employee(models.Model):

    _inherit = 'hr.employee'


    # 'state' is already being used by hr_attendance
    status = fields.Selection([('new', 'New-Hire'),
                               ('onboarding', 'On-Boarding'),
                               ('active', 'Active'),
                               ('pending_inactive', 'Pending Deactivation'),
                               ('inactive', 'Inactive'),
                               ('reactivated', 'Re-Activated'),
                               ],'Status', readonly=True,default='new')
    inactive_ids = fields.One2many('hr.employee.termination', 'employee_id', 'Deactivation Records')
    saved_department_id = fields.Many2one('hr.department','Saved Department')

    @api.multi
    def condition_finished_onboarding(self):
        employee = self._ids[0]
        if self.status == 'onboarding':
            return True

        return False



class hr_employee_termination_reason(models.Model):

    _name = 'hr.employee.termination.reason'
    _description = 'Reason for Employment Termination'

    name = fields.Char('Name', size=256, required=True)



class hr_employee_termination(models.Model):

    _name = 'hr.employee.termination'
    _description = 'Data Related to Deactivation of Employee'

    _inherit = ['mail.thread', 'ir.needaction_mixin']


    name = fields.Date('Effective Date', required=True, readonly=True,states={'draft': [('readonly', False)]})
    reason_id = fields.Many2one('hr.employee.termination.reason', 'Reason', required=True,
                                readonly=True, states={'draft': [('readonly', False)]})
    notes = fields.Text('Notes', readonly=True, states={'draft': [('readonly', False)]})
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True, readonly=True)
    department_id = fields.Many2one('hr.department',related='employee_id.department_id',
                                    store=True, string="Department")
    saved_department_id = fields.Many2one('hr.department',related='employee_id.saved_department_id', type='many2one',
                                          relation='hr.department', store=True, string="Department")
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('cancel', 'Cancelled'),
                              ('done', 'Done'),
                              ],'State', readonly=True,default='draft')


    _defaults = {
        'state': 'draft',
    }


    @api.model
    def _needaction_domain_get(self):

        users_obj = self.env['res.users']
        domain = []

        if users_obj.has_group('hr.group_hr_user'):
            domain = [('state', 'in', ['draft'])]

        if users_obj.has_group('hr.group_hr_manager'):
            if len(domain) > 0:
                domain = ['|'] + domain + [('state', '=', 'confirm')]
            else:
                domain = [('state', '=', 'confirm')]

        if len(domain) > 0:
            return domain

        return False

    @api.multi
    def unlink(self):
        for term in self:
            if term.state not in ['draft']:
                raise UserError(_('Employment termination already in progress. Use the "Cancel" button instead.'))

            # Trigger employee status change back to Active and contract back
            # to Open
            wkf = netsvc.LocalService('workflow')
            term.employee_id.signal_workflow ('signal_active')
            for contract in term.employee_id.contract_ids:
                if contract.state == 'pending_done':
                    contract.signal_workflow('signal_open')

        return super(hr_employee_termination, self).unlink()

    @api.multi
    def effective_date_in_future(self):
        today = datetime.now().date()
        for term in self:
            effective_date = datetime.strptime(term.name, DEFAULT_SERVER_DATE_FORMAT).date()
            if effective_date <= today:
                return False

        return True

    def state_cancel(self):
        ids = self._ids
        if isinstance(ids, (int, long)):
            ids = [ids]

        for term in self:

            # Trigger a status change of the employee and his contract(s)
            wkf = netsvc.LocalService('workflow')
            # wkf.trg_validate(uid, 'hr.employee', term.employee_id.id, 'signal_active', cr)
            term.employee_id.signal_workflow ('signal_active')
            for contract in term.employee_id.contract_ids:
                if contract.state == 'pending_done':
                    # wkf.trg_validate(uid, 'hr.contract', contract.id, 'signal_open', cr)
                    contract.signal_workflow ('signal_active')
                    contract.write({'state':'open'})

        self.write({'state': 'cancel'})

        # return True

    @api.multi
    def state_done(self):
        for term in self:
            if self.effective_date_in_future([term.id]):
                raise UserError(_('Unable to deactivate employee!Effective date is still in the future.'))

            # Trigger a status change of the employee and any contracts pending
            # termination.
            wkf = netsvc.LocalService('workflow')
            for contract in term.employee_id.contract_ids:
                if contract.state == 'pending_done':
                    # wkf.trg_validate(uid, 'hr.contract', contract.id, 'signal_done', cr)
                    contract.signal_workflow ('signal_done')
            # wkf.trg_validate(uid, 'hr.employee', term.employee_id.id, 'signal_inactive', cr)
            term.employee_id.signal_workflow('signal_inactive')

            self.write({'state': 'done'})

        # return True


class hr_contract(models.Model):

    # _name = 'hr.contract'
    _inherit = 'hr.contract'

    @api.multi
    def end_contract(self):

        ids = self._ids
        context = self._context
        if isinstance(ids, (int, long)):
            ids = [ids]

        if len(ids) == 0:
            return False

        context.update({'end_contract_id': ids[0]})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.contract.end',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context
        }
    @api.multi
    def _state_common(self):

        wkf = netsvc.LocalService('workflow')
        for contract in self:
            if contract.employee_id.status == 'new':
                # wkf.trg_validate('hr.employee', contract.employee_id.id, 'signal_confirm')
                contract.signal_workflow('signal_confirm')

    # """Override 'trial' contract state to also change employee state: new -> onboarding"""
    @api.multi
    def state_trial(self):

        res = super(hr_contract, self).state_trial()
        self._state_common()
        return res

    # """Override 'open' contract state to also change employee state: new -> onboarding"""
    @api.multi
    def state_open(self):

        res = super(hr_contract, self).state_open()
        self._state_common()
        return res

    @api.multi
    def try_signal_contract_completed(self):
        d = datetime.now().date()
        ids = self.search([('state', '=', 'open'),('date_end', '<', d.strftime(DEFAULT_SERVER_DATE_FORMAT))])
        if len(ids) == 0:
            return

        for c in self:
            vals = {
                'name': c.date_end and c.date_end or time.strftime(DEFAULT_SERVER_DATE_FORMAT),
                'employee_id': c.employee_id.id,
                'reason': 'contract_end',
            }
            c.setup_pending_done(c,vals)

        return

    @api.multi
    def setup_pending_done(self,contract,term_vals):
        """Start employee deactivation process."""

        term_obj = self.env['hr.employee.termination']
        dToday = datetime.now().date()

        # If employee is already inactive simply end the contract
        wkf = netsvc.LocalService('workflow')
        if not contract.employee_id.active:
            # wkf.trg_validate(uid, 'hr.contract', contract.id, 'signal_done', cr)
            contract.write({'state':'done'})
            return

        # Ensure there are not other open contracts
        open_contract = False
        ee = self.env['hr.employee'].browse(contract.employee_id.id)
        for c2 in ee.contract_ids:
            if c2.id == contract.id or c2.state == 'draft':
                continue

            if (not c2.date_end or datetime.strptime(c2.date_end, DEFAULT_SERVER_DATE_FORMAT).date() >= dToday) and c2.state != 'done':
                open_contract = True

        # Don't create an employment termination if the employee has an open contract or
        # if this contract is already in the 'done' state.
        if open_contract or contract.state == 'done':
            return

        # Also skip creating an employment termination if there is already one in
        # progress for this employee.
        #
        term_ids = term_obj.search([('employee_id','=',contract.employee_id.id),('state', 'in', ['draft', 'confirm'])])
        if len(term_ids) > 0:
            return

        term_obj.create(term_vals)

        # Set the contract state to pending completion
        wkf = netsvc.LocalService('workflow')
        # wkf.trg_validate(uid, 'hr.contract', contract.id, 'signal_pending_done', cr)
        contract.signal_workflow('signal_pending_done')

        # Set employee state to pending deactivation
        # wkf.trg_validate(id, 'hr.employee', contract.employee_id.id, 'signal_pending_inactive', cr)
        contract.employee_id.signal_workflow ('signal_pending_inactive')


class hr_job(models.Model):

    # _name = 'hr.job'
    _inherit = 'hr.job'

    # Override calculation of number of employees in job. Remove employees for
    # which the termination process has already started.
    #
    @api.multi
    def _no_of_employee(self):
        res = {}
        count = 0
        # for job in self.browse(cr, uid, ids, context=context):
        for job in self:
            for ee in job.employee_ids:
                if ee.active and ee.status not in ['pending_inactive']:
                    count += 1

            res[job.id] = {
                'no_of_employee': count,
                'expected_employees': count + job.no_of_recruitment,
            }
        return res

    @api.multi
    def _get_job_position(self):
        res = []
        data = self.env['hr.employee'].read(['job_id'])
        [res.append(d['job_id'][0]) for d in data if d['job_id']]
        return res

        # Override from base class. Also, watch 'status' field of hr.employee
    no_of_employee = fields.Integer(compute='_no_of_employee', string="Current Number of Employees",
                                    help='Number of employees currently occupying this job position.'
                                    ,multi='no_of_employee')
    expected_employees = fields.Integer(compute='_no_of_employee', string='Total Forecasted Employees',
                                        help='Expected number of employees for this job position after new recruitment.',multi='no_of_employee')



