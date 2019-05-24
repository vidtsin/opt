from odoo import models, fields, api,_

import logging

logger = logging.getLogger(__name__)

class document_config_dir(models.Model):
    _name = 'document.config.dir'

    parent_path = fields.Char('Document Parent Path')

    _rec_name = 'parent_path'


class res_partner(models.Model):
    _inherit = 'res.partner'

    is_attached_doc = fields.Boolean("Attached")


