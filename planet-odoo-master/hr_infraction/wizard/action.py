#-*- coding:utf-8 -*-
from odoo import netsvc
from odoo import fields,models,_,api

from odoo.addons.hr_infraction.hr_infraction import ACTION_TYPE_SELECTION


class action_wizard(models.TransientModel):

    _name = 'hr.infraction.action.wizard'
    _description = 'Choice of Actions for Infraction'

    # _columns = {
    action_type = fields.Selection(ACTION_TYPE_SELECTION, 'Action', required=True)
    memo = fields.Text('Notes')
    new_job_id = fields.Many2one('hr.job', 'New Job')
    xfer_effective_date = fields.Date('Effective Date')
    effective_date = fields.Date('Effective Date')
    # }

    @api.multi
    def create_action(self):
        context = self._context
        if context == None:
            context = {}
        infraction_id = context.get('active_id', False)
        if not infraction_id:
            return False

        infraction_id = self.env['hr.infraction'].browse(infraction_id)
        vals = {
            'infraction_id': infraction_id.id,
            'type': self.action_type,
            'memo': self.memo or '',
        }
        action_id = self.env['hr.infraction.action'].create(vals)

        # Update state of infraction, if not already done so
        #
        infraction_obj = self.env['hr.infraction']

        if infraction_id.state == 'confirm':
            infraction_id.signal_workflow('signal_action')
        infraa_obj = self.env['hr.infraction.action']
        imd_obj = self.env['ir.model.data']
        iaa_obj = self.env['ir.actions.act_window']

        # If the action is a warning create the appropriate record, reference it from the action,
        # and pull it up in the view (in case the user needs to make any changes.
        #
        if self.action_type in ['warning_verbal', 'warning_letter']:
            vals = {
                'name': (self.action_type == 'warning_verbal' and 'Verbal' or 'Written') + ' Warning',
                'type': self.action_type == 'warning_verbal' and 'verbal' or 'written',
                'action_id': action_id.id,
            }
            warning_id = self.env['hr.infraction.warning'].create(vals)
            action_id.write({'warning_id': warning_id.id})
            view_id = imd_obj.get_object_reference('hr_infraction','open_hr_infraction_warning')[0]
            dict_act_window = {}
            dict_act_window['res_id'] = warning_id.id
            dict_act_window['view_id'] = view_id

            dict_act_window['view_mode'] = 'form,tree'
            dict_act_window['domain'] = [('id', '=', warning_id.id)]
            dict_act_window['res_model'] = 'hr.infraction.warning'

            return dict_act_window

        # If the action is a departmental transfer create the appropriate record, reference it from
        # the action, and pull it up in the view (in case the user needs to make any changes.
        #
        elif self.action_type == 'transfer':
            xfer_obj = self.env['hr.department.transfer']
            ee = infraction_id.employee_id

            _tmp = xfer_obj.onchange_employee()
            vals = {
                'employee_id': ee.id,
                'src_id': ee.contract_id.job_id.id,
                'dst_id': self.new_job_id.id or False,
                'src_contract_id': ee.contract_id.id,
                'date': self.xfer_effective_date or False,
            }
            xfer_id = xfer_obj.create(vals)
            action_id.write({ 'transfer_id': xfer_id.id})

            view_id = imd_obj.get_object_reference('hr_transfer','open_hr_department_transfer')
            dict_act_window ={}


            dict_act_window['res_id'] = xfer_id.id
            dict_act_window['view_id'] = view_id
            dict_act_window['view_mode'] = 'form,tree'
            dict_act_window['domain'] = [('id', '=', xfer_id.id)]
            dict_act_window['res_model'] = 'hr.department.transfer'
            return dict_act_window

        # The action is dismissal. Begin the termination process.
        #
        elif self.action_type == 'dismissal':
            term_obj = self.env['hr.employee.termination']
            ee = infraction_id.employee_id

            # We must create the employment termination object before we set
            # the contract state to 'done'.
            res_id = imd_obj.get_object_reference('hr_infraction', 'term_dismissal')

            vals = {
                'employee_id': ee.id,
                'name': self.effective_date or False,
                'reason_id': res_id,
            }
            term_id = term_obj.create(vals)
            action_id.write( {'termination_id': term_id.id})

            # End any open contracts
            for contract in ee.contract_ids:
                if contract.state not in ['done']:
                    contract.signal_workflow('signal_pending_done')


            # Set employee state to pending deactivation
            infraction_id.employee_id.signal_workflow('signal_pending_inactive')


            # Trigger confirmation of termination record
            term_id.signal_workflow('signal_confirmed')
            view_id = imd_obj.get_object_reference('hr_employee_state','open_hr_employee_termination')
            dict_act_window = {}
            dict_act_window['res_id'] = term_id.id
            dict_act_window['view_id'] = view_id
            dict_act_window['view_mode'] = 'form,tree'
            dict_act_window['domain'] = [('id', '=', term_id.id)]
            dict_act_window['res_model'] = 'hr.employee.termination'

            return dict_act_window

        return True
