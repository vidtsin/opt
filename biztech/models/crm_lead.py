import logging
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.tools import email_re, email_split
from odoo.exceptions import UserError, AccessError

from odoo.addons.base.res.res_partner import FormatAddress
import logging
logger = logging.getLogger(__name__)


class Lead(models.Model):

    _inherit = "crm.lead"



    @api.multi
    def action_set_done(self):
        """ Won semantic: probability = 100 (active untouched) """
        for lead in self:
            stage_id = lead._stage_find(domain=[('name', '=', 'Done'), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 100})
        return True

    @api.multi
    def log_next_activity_done(self):
        to_clear_ids = []
        logger.error(
            "=====nfvtfg====-----------------------------------------------------------------%s",self)
        for lead in self:
            logger.error("=====next_activity_id============------------------------------------------------------------------, %s",
                         lead.next_activity_id)
            if not lead.next_activity_id:
                continue
            body_html = """<div><b>${object.next_activity_id.name}</b></div>
    %if object.title_action:
    <div>${object.title_action}</div>
    %endif"""
            body_html = self.env['mail.template'].render_template(body_html, 'crm.lead', lead.id,
                                                                   )
            msg_id = lead.message_post(body_html, subtype_id=lead.next_activity_id.subtype_id.id)
            to_clear_ids.append(lead.id)
            self.write({'last_activity_id': lead.next_activity_id.id})

        if to_clear_ids:
            self.cancel_next_activity()
        return True

    @api.multi
    def cancel_next_activity(self):
        return self.write({
            'next_activity_id': False,
            'date_action': False,
            'title_action': False,
        })


    # @api.model
    # def default_get(self, fields):
    #     rec = super(Lead, self).default_get(fields)
    #     print "<<<<<<<<<<rec<<<<<<<<", rec
    #     context = dict(self._context or {})
    #     # active_model = context.get('active_model')
    #     # active_ids = context.get('active_ids')
    #     user_id = self.env['res.users'].search([('id', '=', 1)])
    #     print "<<<<<<<<<<<<<user_id<<<<<<<<<<<<<<", user_id.name
    #     team_id = self.env['crm.team'].search([('id', '=', 4)])
    #     stage_id = self.env['crm.stage'].search([('name', '=', 'New')])
    #     # stage_id = self._stage_find(domain=[('name', '=', 'New')])
    #     print "<<<<<<<<<<<stage_id<<<<<<<<<<<<<<", stage_id.name
    #     print "<<<<<<<<<<<team_id<<<<<<<<<<<<<<", team_id.name
    #     print "<<<<<<<<<<<self._uid<<<<<<<<<<<<<<", self._uid
    #     if stage_id:
    #         if self._uid == user_id.id:
    #             rec.update({ 'team_id': team_id.id
    #
    #                          })
    #
    #     return rec


    @api.model
    def default_get(self, fields):
        rec = super(Lead, self).default_get(fields)
        print "<<<<<<<<<<rec<<<<<<<<", rec
        context = dict(self._context or {})

        user_id = self.env['res.users'].search([('id', '=', 35)])
        print "<<<<<<<<<<<<<user_id<<<<<<<<<<<<<<", user_id.name
        team_id = self.env['crm.team'].search([('id', '=', 1)])
        # stage_id = self.env['crm.stage'].search([('stage_id', '=', 'Opportunity')])
        stage_id = self._stage_find(domain=[('name', '=', 'Opportunity')])
        print "<<<<<<<<<<<team_id<<<<<<<<<<<<<<", team_id.name
        print "<<<<<<<<<<<self._uid<<<<<<<<<<<<<<", self._uid
        if stage_id:
            if self._uid == user_id.id:
                rec.update({'team_id': team_id.id

                            })

        return rec



