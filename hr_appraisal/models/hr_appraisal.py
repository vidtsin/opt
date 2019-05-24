# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrAppraisal(models.Model):
    _name = "hr.appraisal"
    _inherit = ['mail.thread']
    _description = "Employee Appraisal"
    _order = 'date_close, date_final_interview'
    _rec_name = 'employee_id'

    APPRAISAL_STATES = [
        ('new', 'To Start'),
        ('pending', 'Appraisal Sent'),
        ('done', 'Done'),
        ('cancel', "Cancelled"),
    ]

    active = fields.Boolean(default=True)
    action_plan = fields.Text(string="Action Plan", help="If the evaluation does not meet the expectations, you can propose an action plan")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    color = fields.Integer(string='Color Index', help='This color will be used in the kanban view.')
    employee_id = fields.Many2one('hr.employee', required=True, string='Employee', index=True)
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string='Department', store=True)
    date_close = fields.Date(string='Appraisal Deadline', required=True)
    state = fields.Selection(APPRAISAL_STATES, string='Status', track_visibility='onchange', required=True, readonly=True, copy=False, default='new', index=True)
    manager_appraisal = fields.Boolean(string='Manager', help="This employee will be appraised by his managers")
    manager_ids = fields.Many2many('hr.employee', 'appraisal_manager_rel', 'hr_appraisal_id')
    manager_survey_id = fields.Many2one('survey.survey', string="Manager's Appraisal")
    collaborators_appraisal = fields.Boolean(string='Collaborator', help="This employee will be appraised by his collaborators")
    collaborators_ids = fields.Many2many('hr.employee', 'appraisal_subordinates_rel', 'hr_appraisal_id')
    collaborators_survey_id = fields.Many2one('survey.survey', string="Collaborator's Appraisal")
    colleagues_appraisal = fields.Boolean(string='Colleagues', help="This employee will be appraised by his colleagues")
    colleagues_ids = fields.Many2many('hr.employee', 'appraisal_colleagues_rel', 'hr_appraisal_id')
    colleagues_survey_id = fields.Many2one('survey.survey', string="Colleague's Appraisal")
    employee_appraisal = fields.Boolean(help="This employee will do a self-appraisal")
    employee_survey_id = fields.Many2one('survey.survey', string='Self Appraisal')
    survey_sent_ids = fields.One2many('survey.user_input', 'appraisal_id', string='Sent Forms')
    count_sent_survey = fields.Integer(string="Number of Sent Forms", compute='_compute_sent_survey')
    survey_completed_ids = fields.One2many('survey.user_input', 'appraisal_id', string='Answers', domain=lambda self: [('state', '=', 'done')])
    count_completed_survey = fields.Integer(string="Number of Answers", compute='_compute_completed_survey')
    mail_template_id = fields.Many2one('mail.template', string="Email Template for Appraisal", default=lambda self: self.env.ref('hr_appraisal.send_appraisal_template'))
    meeting_id = fields.Many2one('calendar.event', string='Meeting')
    date_final_interview = fields.Date(string="Final Interview", index=True, track_visibility='onchange')


    # for  count  sent appraisal
    @api.multi
    def _compute_sent_survey(self):
        survey_sent = self.env['survey.user_input'].read_group([('appraisal_id', 'in', self.ids)], ['appraisal_id'], ['appraisal_id'])
        result = dict((data['appraisal_id'][0], data['appraisal_id_count']) for data in survey_sent)
        for appraisal in self:
            appraisal.count_sent_survey = result.get(appraisal.id, 0)

    # for completed appraisal
    @api.multi
    def _compute_completed_survey(self):
        completed_survey = self.env['survey.user_input'].read_group([('appraisal_id', 'in', self.ids), ('state', '=', 'done')], ['appraisal_id'], ['appraisal_id'])
        result = dict((data['appraisal_id'][0], data['appraisal_id_count']) for data in completed_survey)
        for appraisal in self:
            appraisal.count_completed_survey = result.get(appraisal.id, 0)

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            self.department_id = self.employee_id.department_id
            self.manager_appraisal = self.employee_id.appraisal_by_manager
            self.manager_ids = self.employee_id.appraisal_manager_ids
            self.manager_survey_id = self.employee_id.appraisal_manager_survey_id
            self.colleagues_appraisal = self.employee_id.appraisal_by_colleagues
            self.colleagues_ids = self.employee_id.appraisal_colleagues_ids
            self.colleagues_survey_id = self.employee_id.appraisal_colleagues_survey_id
            self.employee_appraisal = self.employee_id.appraisal_self
            self.employee_survey_id = self.employee_id.appraisal_self_survey_id
            self.collaborators_appraisal = self.employee_id.appraisal_by_collaborators
            self.collaborators_ids = self.employee_id.appraisal_collaborators_ids
            self.collaborators_survey_id = self.employee_id.appraisal_collaborators_survey_id


    # Subscribes the employee and his manager to the appraisal thread.
    # Also subscribes other employees designed as manager for this appraisal, and the manager of the employee's department if he's different from the employee's direct manager.

    @api.multi
    def subscribe_employees(self):
        for appraisal in self:
            partner_ids = [emp.related_partner_id.id for emp in appraisal.manager_ids if emp.related_partner_id]

            if appraisal.employee_id.related_partner_id:
                partner_ids.append(appraisal.employee_id.related_partner_id.id)
            if appraisal.employee_id.parent_id.related_partner_id:
                partner_ids.append(appraisal.employee_id.parent_id.related_partner_id.id)
            if appraisal.employee_id.department_id.manager_id.related_partner_id:
                partner_ids.append(appraisal.employee_id.department_id.manager_id.related_partner_id.id)

            partner_ids = list(set(partner_ids))
            appraisal.message_subscribe(partner_ids=partner_ids)
        return True

    #  Creates event when user enters date manually from the form view.
    #  If users edit the already entered date, created meeting is updated accordingly.

    @api.multi
    def schedule_final_meeting(self, interview_deadline):
        CalendarEvent = self.env['calendar.event']
        values = {'start': interview_deadline, 'stop': interview_deadline}
        for appraisal in self:
            if appraisal.meeting_id and appraisal.meeting_id.allday:
                appraisal.meeting_id.write(values)
            elif appraisal.meeting_id and not appraisal.meeting_id.allday:
                date = fields.Date.from_string(interview_deadline)
                meeting_date = fields.Datetime.to_string(date)
                appraisal.meeting_id.write({'start_datetime': meeting_date, 'stop_datetime': meeting_date})
            if not appraisal.meeting_id:
                attendee_ids = [(4, manager.related_partner_id.id) for manager in appraisal.manager_ids if manager.related_partner_id]
                if appraisal.employee_id.related_partner_id:
                    attendee_ids.append((4, appraisal.employee_id.related_partner_id.id))
                values['name'] = _('Appraisal Meeting For %s') % appraisal.employee_id.name_related
                values['allday'] = True
                values['partner_ids'] = attendee_ids
                appraisal.meeting_id = CalendarEvent.create(values)
        return True
    
    # for user appraisal receiver.
    def _prepare_user_input_receivers(self):

        appraisal_receiver = []
        if self.manager_appraisal and self.manager_ids and self.manager_survey_id:
            appraisal_receiver.append((self.manager_survey_id, self.manager_ids))
        if self.colleagues_appraisal and self.colleagues_ids and self.colleagues_survey_id:
            appraisal_receiver.append((self.colleagues_survey_id, self.colleagues_ids))
        if self.collaborators_appraisal and self.collaborators_ids and self.collaborators_survey_id:
            appraisal_receiver.append((self.collaborators_survey_id, self.collaborators_ids))
        if self.employee_appraisal and self.employee_survey_id:
            appraisal_receiver.append((self.employee_survey_id, self.employee_id))
        return appraisal_receiver


    # for appraisal send on mail.
    @api.multi
    def send_appraisal(self):
        ComposeMessage = self.env['survey.mail.compose.message']
        for appraisal in self:
            appraisal_receiver = appraisal._prepare_user_input_receivers()
            for survey, receivers in appraisal_receiver:
                for employee in receivers:
                    email = employee.related_partner_id.email or employee.work_email
                    render_template = appraisal.mail_template_id.with_context(email=email, survey=survey, employee=employee).generate_email([appraisal.id])
                    values = {
                        'survey_id': survey.id,
                        'public': 'email_private',
                        'partner_ids': employee.related_partner_id and [(4, employee.related_partner_id.id)] or False,
                        'multi_email': email,
                        'subject': survey.title,
                        'body': render_template[appraisal.id]['body'],
                        'date_deadline': appraisal.date_close,
                        'model': appraisal._name,
                        'res_id': appraisal.id,
                    }
                    compose_message_wizard = ComposeMessage.with_context(active_id=appraisal.id, active_model=appraisal._name).create(values)
                    compose_message_wizard.send_mail()  # Sends a mail and creates a survey.user_input
            appraisal.message_post(body=_("Appraisal(s) form have been sent"), subtype="hr_appraisal.mt_appraisal_sent")
        return True


   # Cancels the appraisal process, removing related calendar events, and removes sent surveys.

    @api.multi
    def cancel_appraisal(self):

        for appraisal in self:
            if appraisal.meeting_id:
                appraisal.meeting_id.unlink()

            appraisal.survey_sent_ids.unlink()
            appraisal.date_final_interview = False

    @api.model
    def create(self, vals):
        result = super(HrAppraisal, self.with_context(mail_create_nolog=True)).create(vals)
        result.subscribe_employees()
        date_final_interview = vals.get('date_final_interview')
        if date_final_interview:
            # creating employee meeting and interview date
            result.schedule_final_meeting(date_final_interview)
        return result

    @api.multi
    def write(self, vals):
        if vals.get('state'):
            if vals['state'] == 'cancel':
                self.cancel_appraisal()
            if vals['state'] == 'pending':
                self.send_appraisal()
        result = super(HrAppraisal, self).write(vals)
        date_final_interview = vals.get('date_final_interview')
        if date_final_interview:
            # creating employee meeting and interview date
            self.schedule_final_meeting(date_final_interview)
        return result

    @api.multi
    def unlink(self):
        for appraisal in self:
            if appraisal.state != 'new' and appraisal.state != 'cancel':
                appraisal_state = dict(self.APPRAISAL_STATES)
                raise UserError(_("You cannot delete appraisal which is in '%s' state") % (appraisal_state[appraisal.state]))
        return super(HrAppraisal, self).unlink()

    # """ Override read_group to always display all states and order them appropriatly. """
    # Get standard results
    # Update standard results with default results

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if groupby and groupby[0] == "state":
            states = [('new', _('To Start')), ('pending', _('Appraisal Sent')), ('done', _('Done')), ('cancel', _('Cancelled'))]
            read_group_all_states = [{
                '__context': {'group_by': groupby[1:]},
                '__domain': domain + [('state', '=', state_value)],
                'state': state_value,
                'state_count': 0,
            } for state_value, state_name in states]
            read_group_res = super(HrAppraisal, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby)

            result = []
            for state_value, state_name in states:
                res = filter(lambda x: x['state'] == state_value, read_group_res)
                if not res:
                    res = filter(lambda x: x['state'] == state_value, read_group_all_states)
                res[0]['state'] = [state_value, state_name]
                if res[0]['state'][0] == 'done' or res[0]['state'][0] == 'cancel':
                    res[0]['__fold'] = True
                result.append(res[0])
            return result
        else:
            return super(HrAppraisal, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby)

    # """ Link to open sent appraisal"""
    @api.multi
    def action_get_users_input(self):
        self.ensure_one()
        action = self.env.ref('survey.action_survey_user_input').read()[0]
        if self.env.context.get('answers'):
            users_input = self.survey_completed_ids
        else:
            users_input = self.survey_sent_ids
        action['domain'] = str([('id', 'in', users_input.ids)])
        action['context'] = {}  # Remove default group_by for surveys.
        return action

    # """ Link to open calendar view for creating employee interview/meeting"""
    @api.multi
    def action_calendar_event(self):
        self.ensure_one()
        partner_ids = [manager.related_partner_id.id for manager in self.manager_ids if manager.related_partner_id]
        if self.employee_id.related_partner_id:
            partner_ids.append(self.employee_id.related_partner_id.id)
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        partner_ids.append(self.env.user.partner_id.id)
        action['context'] = {
            'default_partner_ids': partner_ids,
            'search_default_mymeetings': 1
        }
        return action

    @api.multi
    def button_send_appraisal(self):
        self.write({'state': 'pending'})

    @api.multi
    def button_done_appraisal(self):
        self.write({'state': 'done'})

    @api.multi
    def button_cancel_appraisal(self):
        self.write({'state': 'cancel'})

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'new':
            return 'hr_appraisal.mt_appraisal_new'
        if 'date_final_interview' in init_values and not self.meeting_id:
            return 'hr_appraisal.mt_appraisal_meeting'
        return super(HrAppraisal, self)._track_subtype(init_values)
