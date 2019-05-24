#-*- coding:utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import netsvc
from odoo import fields,models,api,_
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.translate import _
from odoo.exceptions import UserError


class hr_transfer(models.Model):

    _name = 'hr.department.transfer'
    _description = 'Departmental Transfer'

    _inherit = ['mail.thread', 'ir.needaction_mixin']


    employee_id = fields.Many2one('hr.employee', 'Employee', required=True, readonly=True,
                                   states={'draft': [('readonly', False)]})
    src_id = fields.Many2one('hr.job', 'From', required=True, readonly=True,states={'draft': [('readonly', False)]})
    dst_id = fields.Many2one('hr.job', 'Destination', required=True, readonly=True,states={'draft': [('readonly', False)]})
    src_department_id = fields.Many2one('hr.department',related='src_id.department_id',  string='From Department',
                                        store=True, readonly=True)
    dst_department_id =  fields.Many2one('hr.department',related='dst_id.department_id', store=True,
                                        string='Destination Department', readonly=True)
    src_contract_id = fields.Many2one('hr.contract', 'From Contract', readonly=True,
                                       states={'draft': [('readonly', False)]})
    dst_contract_id = fields.Many2one('hr.contract', 'Destination Contract', readonly=True)
    date = fields.Date('Effective Date', required=True, readonly=True,states={'draft': [('readonly', False)]})
    state =  fields.Selection([('draft', 'Draft'),
                                ('confirm', 'Confirmed'),
                                ('pending', 'Pending'),
                                ('done', 'Done'),
                                ('cancel', 'Cancelled'),],'State', readonly=True,default='draft')


    _rec_name = 'date'


    @api.multi
    def _needaction_domain_get(self):

        users_obj = self.env['res.users']

        domain = []
        if users_obj.has_group('hr.group_hr_manager'):
            domain = [('state', '=', 'confirm')]
            return domain

        return False

    @api.multi
    def unlink(self):
        for xfer in self:
            if xfer.state not in ['draft']:
                raise UserError(_('Transfer has been initiated. Either cancel the transfer or create another transfer to undo it.'))

        return super(hr_transfer, self).unlink()

    @api.one
    @api.onchange('employee_id')
    def onchange_employee(self):

        res = {'value': {'src_id': False, 'src_contract_id': False}}

        if self.employee_id:
            ee = self.employee_id
            res['value']['src_id'] = ee.contract_id.job_id.id
            res['value']['src_contract_id'] = ee.contract_id.id

        return res
    @api.multi
    def effective_date_in_future(self):

        today = datetime.now().date()
        for xfer in self:
            effective_date = datetime.strptime(
                xfer.date, DEFAULT_SERVER_DATE_FORMAT).date()
            if effective_date <= today:
                return False

        return True

    @api.multi
    def _check_state(self,contract_id, effective_date):
        contract_obj = self.env['hr.contract']
        contract_id = contract_obj.browse(contract_id)

        if contract_id.state not in ['trial', 'trial_ending', 'open', 'contract_ending']:
            raise UserError(_('The current state of the contract does not permit changes.'))

        if contract_id.date_end:
            dContractEnd = datetime.strptime(
                contract_id.date_end, DEFAULT_SERVER_DATE_FORMAT)
            dEffective = datetime.strptime(
                effective_date, DEFAULT_SERVER_DATE_FORMAT)
            if dEffective >= dContractEnd:
                raise UserError(_('The contract end date is on or before the effective date of the transfer.'))

        return True


    # Copy the contract and adjust start/end dates, job id, etc. accordingly.
    @api.multi
    def transfer_contract(self,contract_id, job_id, xfer_id, effective_date):
        contract_obj = self.env['hr.contract']
        contract_id = contract_obj.browse(contract_id)


        default = {
            'employee_id':contract_id.employee_id.id,
            'wage':contract_id.wage,
            'job_id': job_id,
            'date_start': effective_date,
            'name': contract_id.name,
            'state': False,
            'message_ids': False,
            'trial_date_start': False,
            'trial_date_end': contract_id.trial_date_end,
        }


        c_id = contract_obj.create(default)

        if c_id:
            vals = {}
            c_id.signal_workflow('signal_confirm')
            # Set the new contract to the appropriate state
            # Terminate the current contract (and trigger appropriate state
            # change)
            vals['date_end'] = datetime.strptime(
                effective_date, '%Y-%m-%d').date() + relativedelta(days=-1)
            contract_id.write(vals)

            # contract_id.signal_workflow('signal_done')
            contract_id.write({'state':'done'})
            # Link to the new contract
            xfer_id.write({'dst_contract_id': c_id})

        return

    @api.multi
    def state_confirm(self):
        for xfer in self:
            self._check_state(xfer.src_contract_id.id, xfer.date)
            xfer.write({'state': 'confirm'})

        return True

    @api.multi
    def state_done(self):
        employee_obj = self.env['hr.employee']
        today = datetime.now().date()
        for xfer in self:
            if datetime.strptime(xfer.date, DEFAULT_SERVER_DATE_FORMAT).date() <= today:
                self._check_state(xfer.src_contract_id.id, xfer.date)
                xfer.employee_id.write({'department_id': xfer.dst_department_id.id})
                self.transfer_contract(xfer.src_contract_id.id, xfer.dst_id.id,xfer.id, xfer.date)
                xfer.write({'state': 'done'})
            else:
                return False

        return True


    # """Completes pending departmental transfers. Called from the scheduler."""
    @api.multi
    def try_pending_department_transfers(self):

        xfer_obj = self.env['hr.department.transfer']
        today = datetime.now().date()
        xfer_ids = xfer_obj.search([('state', '=', 'pending'),('date', '<=', today.strftime(DEFAULT_SERVER_DATE_FORMAT))])
        for xfer in xfer_ids:
            xfer.write({'state':'done'})

        return True
