# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    appraisal_id = fields.Many2one('hr.appraisal', string='Appraisal')

    @api.model
    def create(self, vals):
        ctx = self.env.context
        if ctx.get('active_id') and ctx.get('active_model') == 'hr.appraisal':
            vals['appraisal_id'] = ctx.get('active_id')
        return super(SurveyUserInput, self).create(vals)

    # ''' Override to open the survey results in a new window if it's the answer to an appraisal '''
    @api.multi
    def action_survey_results(self):
        action = super(SurveyUserInput, self).action_survey_results()
        if self.env.context.get('active_model') == 'hr.appraisal':
            action['target'] = 'new'
        return action

    # ''' Override to open the survey results in a new window if it's the answer to an appraisal '''
    @api.multi
    def action_view_answers(self):
        action = super(SurveyUserInput, self).action_view_answers()
        if self.env.context.get('active_model') == 'hr.appraisal':
            action['target'] = 'new'
        return action
