from odoo import models,api
import base64
from odoo.exceptions import UserError,ValidationError
import os,sys
import random
import logging
logger = logging.getLogger(__name__)

class ir_attachment(models.Model):
    _inherit = "ir.attachment"

    # for Attachment

    @api.model
    def create(self, vals):
        res = super(ir_attachment, self).create(vals)
        if vals.get('res_model'):
            modelstr = str(vals.get('res_model'))
            modelstr = modelstr.replace('.',' ').title()
            doc_config_id = self.env['document.config.dir'].search([])
            if doc_config_id:
                parent_path = str(doc_config_id.parent_path)
            else:
                parent_path = '/home/Document Storage/'

            if not os.path.exists(parent_path):
                os.mkdir (parent_path)
                os.chmod (parent_path, 0777)
            store_path = parent_path + modelstr

            if not os.path.exists(store_path):
                os.mkdir(store_path)
                os.chmod(store_path, 0777)

            rec_dir = os.path.join(store_path,str(vals.get('res_id')))
            if not os.path.exists(rec_dir):
                os.mkdir(rec_dir)
                os.chmod(rec_dir, 0777)
            name = str(vals.get('datas_fname').encode('utf-8')) if vals.get('datas_fname',False) else 'file_'+str(random.randint(1,100))
            filename = os.path.join (rec_dir, name)
            file = open(filename,'wb')
            if vals.get('datas'):
                data = base64.b64decode(vals.get('datas'))
                file.write(data)
                os.chmod(filename, 0777)
                if vals.get('res_model') == 'res.partner':
                    if not self.env[vals.get('res_model')].browse(vals.get('res_id')).is_attached_doc:
                        self.env[vals.get('res_model')].browse(vals.get('res_id')).write({'is_attached_doc':True})
                file.close()
        return res
