from odoo.addons.base.res.res_partner import FormatAddress
from odoo import api, fields, models,tools
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta
import logging
logger = logging.getLogger(__name__)
from odoo.exceptions import UserError




class Lead(FormatAddress, models.Model):

    _inherit = "crm.lead"

    stage_id_name = fields.Char(related='stage_id.name', readonly=True, store=True)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange')
    activity_ids = fields.One2many('crm.activities', 'crm_lead_id', string='Activities')

class CrmActivities(models.Model):

    _name = "crm.activities"
    _rec_name = 'crm_lead_id'

    crm_lead_id = fields.Many2one('crm.lead', 'Lead')
    crm_activity_id = fields.Many2one('crm.activity', 'Activity')
    outcome = fields.Text('Outcome')
    date_action = fields.Date('Activity Date', index=True)
    hours = fields.Selection([(str(num).zfill(2), str(num).zfill(2)) for num in range(01, 24)],
                             string='Timing')
    mins = fields.Selection([(str(num).zfill(2), str(num).zfill(2)) for num in range(01, 60)],
                            string='Mins')
    time = fields.Char(string='Timing')
    # date_action_datetime=fields.Datetime('Activity Datetime',compute="compute_activity_datetime")
    title_action = fields.Char('Activity Summary')
    state = fields.Selection([
        ('open', 'Open'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, required=True, track_visibility='always', copy=False, default='open')

    # def open_activity_wizard(self):
    #     return {
    #         "type": "ir.actions.act_window",
    #         "res_model": "crm.activities",
    #         "views": [[False, "form"]],
    #         "res_id": self.id,
    #         "view_id": 'crm_activities_form',
    #         "target": "new",
    #     }



    @api.one
    def mark_activity_done(self):
        if not self.crm_activity_id:
            raise UserError("Please select an activity!!!")
        if not self.outcome:
            raise UserError("Please enter outcome for this activity!!!")
        body_html = """<div><b>Activity:%s</b></div>""" % self.crm_activity_id.name
        if self.title_action:
            title_action = """<div>Activity Summary%s</div>""" % self.title_action
            body_html += title_action
        if self.date_action:
            date_action = """<div>Activity Date:%s</div>""" % self.date_action
            body_html += date_action
        if self.outcome:
            outcome = """<div>Activity Outcome%s</div>""" % self.outcome
            body_html += outcome
        body_html = self.env['mail.template'].render_template(body_html, 'crm.lead', self.crm_lead_id.id, )
        msg_id = self.crm_lead_id.message_post(body_html, subtype_id=self.crm_activity_id.subtype_id.id)
        self.state = 'done'
        return True

    @api.one
    def mark_activity_cancelled(self):
        if not self.crm_activity_id:
            raise UserError("Please select an activity!!!")
        if not self.outcome:
            raise UserError("Please enter outcome for this activity!!!")
        self.state = 'cancel'
        return True

    @api.onchange('hours','mins')
    def compute_time(self):
        for rec in self:
            if rec.hours and rec.mins:
                rec.time=rec.hours+':'+rec.mins

