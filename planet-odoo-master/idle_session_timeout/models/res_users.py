# -*- coding: utf-8 -*-

import logging
from odoo import models,api

from odoo.http import root
from odoo.http import request
# from collections import defaultdict
from os import utime
from os.path import getmtime
from time import time

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _auth_timeout_ignoredurls_get(self):

        # """Pluggable method for calculating ignored urls
        # Defaults to stored config param
        # """
        param_model = self.env['ir.config_parameter']
        return param_model._auth_timeout_get_parameter_ignoredurls()

    def _auth_timeout_deadline_calculate(self):
        # """Pluggable method for calculating timeout deadline
        # Defaults to current time minus delay using delay stored as config param
        # """
        param_model = self.env['ir.config_parameter']
        delay = param_model._auth_timeout_get_parameter_delay()
        if delay is False or delay <= 0:
            return False
        return time() - delay

    def _auth_timeout_session_terminate(self, session):
        """Pluggable method for terminating a timed-out session

        This is a late stage where a session timeout can be aborted.
        Useful if you want to do some heavy checking, as it won't be
        called unless the session inactivity deadline has been reached.

        Return:
            True: session terminated
            False: session timeout cancelled
        """
        if session.db and session.uid:
            session.logout(keep_db=True)
        return True

    def _auth_timeout_check(self):
        if not request:
            return

        session = request.session

        # Calculate deadline
        deadline = self._auth_timeout_deadline_calculate()

        # Check if past deadline
        expired = False
        if deadline is not False:
            path = root.session_store.get_session_filename(session.sid)
            try:
                expired = getmtime(path) < deadline
            except OSError as e:
                _logger.warning(
                    'Exception reading session file modified time: %s'
                    % e
                )
                pass

        # Try to terminate the session
        terminated = False
        if expired:
            terminated = self._auth_timeout_session_terminate(session)

        # If session terminated, all done
        if terminated:
            return

        # Else, conditionally update session modified and access times
        ignoredurls = self._auth_timeout_ignoredurls_get()

        if request.httprequest.path not in ignoredurls:
            if 'path' not in locals():
                path = root.session_store.get_session_filename(session.sid)
            try:
                utime(path, None)
            except OSError as e:
                _logger.warning(
                    'Exception updating session file access/modified times: %s'
                    % e
                )
                pass

        return

    def _check_session_validity(self, db, uid, passwd):
        """Adaptor method for backward compatibility"""
        return self._auth_timeout_check()

    @classmethod
    def check(cls, db, uid, passwd):
        """Verifies that the given (uid, password) is authorized for the database ``db`` and
           raise an exception if it is not."""
        res = super (ResUsers, cls).check (db, uid, passwd)

        cr = cls.pool.cursor()
        try:
            self = api.Environment(cr, uid, {})[cls._name]
            self.check_credentials(passwd)
            self._check_session_validity(db, uid, passwd)

        finally:
            cr.close ()
        return res
