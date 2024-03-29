# -*- coding: utf-8 -*-
from odoo import models, api, tools, SUPERUSER_ID

DELAY_KEY = 'inactive_session_time_out_delay'
IGNORED_PATH_KEY = 'inactive_session_time_out_ignored_url'


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    @tools.ormcache('db')
    def get_session_parameters(self, db):
        param_model = self.env['ir.config_parameter']
        cr = self.pool.cursor()
        delay = False
        urls = []
        try:
            delay = int(param_model.get_param(DELAY_KEY, 900))
            urls = param_model.get_param(IGNORED_PATH_KEY, '').split(',')
        finally:
            cr.close()
        return delay, urls

    def _auth_timeout_get_parameter_delay(self):
        delay, urls = self.get_session_parameters(self.pool.db_name)
        return delay

    def _auth_timeout_get_parameter_ignoredurls(self):
        delay, urls = self.get_session_parameters(self.pool.db_name)
        return urls

    @api.multi
    def write(self, vals, context=None):
        res = super(IrConfigParameter, self).write(vals)
        if self.key == DELAY_KEY:
            self.get_session_parameters.clear_cache(self)
        elif self.key == IGNORED_PATH_KEY:
            self.get_session_parameters.clear_cache(self)
        return res
