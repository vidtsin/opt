from odoo import models, fields, api, _
import csv
from tempfile import TemporaryFile
import StringIO
import base64
import logging
_logger = logging.getLogger(__name__)

class btc_ir_attach(models.TransientModel):
    _name = "btc.ir.attach"

    import_data = fields.Binary('Upload CSV')

    @api.multi
    def import_ir_attchment(self):
        ir_attachment_obj = self.env['ir.attachment']
        csv_datas = self.import_data
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(csv_datas))
        fileobj.seek(0)
        str_csv_data = fileobj.read()
        list = csv.reader(StringIO.StringIO(str_csv_data), delimiter='|')

        error_list = []
        id_list = []
        no_id_list = []
        rownum = 0
        for row in list:
            if row == '':
                continue

            if rownum == 0:
                rownum += 1
            else:
                try:
                    crm_lead_id = self.env['crm.lead'].search([('name', '=', str(row[0]).strip())])
                    _logger.info('<<<<<<<<<<<crm_lead_id<<<<<<<< %s', crm_lead_id)

                    # user_id = self.env['res.users'].search([('email', '=', row[20] or '')])
                    # _logger.info('<<<<<<<<<<<user_id<<<<<<<<<< %s', user_id)
                    if len(crm_lead_id) > 1:
                        id_list.append(crm_lead_id)

                    if len(crm_lead_id) == 0:
                        no_id_list.append(str(row[0]).strip())
                        type = ''
                        if str(row[14]).strip() == 'URL':
                            type = 'url'
                        else:
                            type = 'binary'

                        vals = {
                            'name': str(row[1]).strip(),
                            'checksum': str(row[2]).strip() or False,
                            'db_datas': str(row[3]).strip() or False,
                            'create_date': row[4] or False,
                            'datas_fname': str(row[5]).strip() or False,
                            'file_size': row[6] or False,
                            'public': row[7] or False,
                            'mimetype': str(row[8]).strip() or False,
                            'res_field': str(row[9]).strip() or False,
                            # 'res_id': False,
                            'res_model': str(row[11]).strip() or False,
                            'res_name': str(row[12]).strip() or False,
                            'store_fname': str(row[13]).strip() or False,
                            'type': type,
                            'url': str(row[15]).strip() or False,

                        }

                        _logger.info('<<<<<<<<<<<<<<<<vals<<<<<<<<<<<<<< %s', vals)

                        attachment_id = ir_attachment_obj.create(vals)
                        _logger.info('<<<<<<<<<<<<<<<<attachment_id<<<without_id<<<<<<<<<<< %s', attachment_id)

                        if row[4] == '' or len(attachment_id) == 0:
                            continue
                        self._cr.execute("""update ir_attachment set create_date=%s where id=%s""",
                                         (row[4] or False, attachment_id[0].id))
                        self._cr.commit()


                    if len(crm_lead_id) <= 1:
                        type = ''
                        if str(row[14]).strip() == 'URL':
                            type = 'url'
                        else:
                            type = 'binary'

                        vals= {
                               'name': str(row[1]).strip(),
                               'checksum':str(row[2]).strip() or False,
                               'db_datas': str(row[3]).strip() or False,
                               'create_date': row[4] or False,
                               'datas_fname': str(row[5]).strip() or False,
                               'file_size': row[6] or False,
                               'public': row[7] or False,
                               'mimetype': str(row[8]).strip() or False,
                               'res_field': str(row[9]).strip() or False,
                               'res_id': crm_lead_id[0].id or False,
                               'res_model':str(row[11]).strip() or False,
                               'res_name': str(row[12]).strip() or False,
                               'store_fname': str(row[13]).strip() or False,
                               'type': type,
                               'url': str(row[15]).strip() or False,

                               }

                        _logger.info('<<<<<<<<<<<<<<<<vals<<<<<<<<<<<<<< %s', vals)

                        attachment_id = ir_attachment_obj.create(vals)
                        _logger.info('<<<<<<<<<<<<<<<<attachment_id<<<<<<<<<<<<<< %s', attachment_id)

                        if row[4] == '' or len(attachment_id) == 0:
                            continue
                        self._cr.execute("""update ir_attachment set create_date=%s where id=%s""",(row[4] or False, attachment_id[0].id))
                        self._cr.commit()


                except Exception,e:
                    _logger.info('<<<<<<<<<<<<<Exception<<<<<<<<<<<< %s', e)

        _logger.info('<<<<<<<<<<<<<id_list<<<<<<<<<<<< %s', id_list)
        _logger.info('<<<<<len<<<<<<<<id_list<<<<<<<<<<<< %s', len(id_list))
        _logger.info('<<<<<<<<<<<<<no_id_list<<<<<<<<<<<< %s', no_id_list)
        _logger.info('<<<<<len<<<<<<<<no_id_list<<<<<<<<<<<< %s', len(no_id_list))
















    # @api.multi
    # def import_ir_attchment(self):
    #     ir_attachment_obj = self.env['ir.attachment']
    #     csv_datas = self.import_data
    #     fileobj = TemporaryFile('w+')
    #     fileobj.write(base64.decodestring(csv_datas))
    #     fileobj.seek(0)
    #     str_csv_data = fileobj.read()
    #     list = csv.reader(StringIO.StringIO(str_csv_data), delimiter='|')
    #
    #     error_list = []
    #     id_list = []
    #     rownum = 0
    #     for row in list:
    #         if row == '':
    #             continue
    #
    #         if rownum == 0:
    #             rownum += 1
    #         else:
    #             try:
    #                 crm_lead_id = self.env['crm.lead'].search([('name', '=', str(row[0]).strip())])
    #                 _logger.info('<<<<<<<<<<<crm_lead_id<<<<<<<< %s', crm_lead_id)
    #
    #                 # user_id = self.env['res.users'].search([('email', '=', row[20] or '')])
    #                 # _logger.info('<<<<<<<<<<<user_id<<<<<<<<<< %s', user_id)
    #                 if len(crm_lead_id) > 1:
    #                     id_list.append(crm_lead_id)
    #
    #                 if len(crm_lead_id) <= 1:
    #                     type = ''
    #                     if str(row[14]).strip() == 'URL':
    #                         type = 'url'
    #                     else:
    #                         type = 'binary'
    #
    #                     vals= {
    #                            'name': str(row[1]).strip(),
    #                            'checksum':str(row[2]).strip() or False,
    #                            'db_datas': str(row[3]).strip() or False,
    #                            'create_date': row[4] or False,
    #                            'datas_fname': str(row[5]).strip() or False,
    #                            'file_size': row[6] or False,
    #                            'public': row[7] or False,
    #                            'mimetype': str(row[8]).strip() or False,
    #                            'res_field': str(row[9]).strip() or False,
    #                            'res_id': crm_lead_id[0].id or False,
    #                            'res_model':str(row[11]).strip() or False,
    #                            'res_name': str(row[12]).strip() or False,
    #                            'store_fname': str(row[13]).strip() or False,
    #                            'type': type,
    #                            'url': str(row[15]).strip() or False,
    #
    #                            }
    #
    #                     _logger.info('<<<<<<<<<<<<<<<<vals<<<<<<<<<<<<<< %s', vals)
    #
    #                     attachment_id = ir_attachment_obj.create(vals)
    #                     _logger.info('<<<<<<<<<<<<<<<<attachment_id<<<<<<<<<<<<<< %s', attachment_id)
    #
    #                     if row[4] == '' or len(attachment_id) == 0:
    #                         continue
    #                     self._cr.execute("""update ir_attachment set create_date=%s where id=%s""",(row[4] or False, attachment_id[0].id))
    #                     self._cr.commit()
    #
    #                 else:
    #                     error_list.append(vals)
    #
    #             except Exception,e:
    #                 _logger.info('<<<<<<<<<<<<<Exception<<<<<<<<<<<< %s', e)
    #
    #     _logger.info('<<<<<<<<<<<<<error_list<<<<<<<<<<<< %s', error_list)
    #     _logger.info('<<<<<<<<<<<<<id_list<<<<<<<<<<<< %s', id_list)