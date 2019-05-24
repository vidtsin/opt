from odoo import models, fields, api, _
import csv
import StringIO
import base64
import logging
_logger = logging.getLogger(__name__)


class btc_mail_messages(models.TransientModel):
    _name = "btc.mail.messages"

    @api.multi
    def import_mail_messages(self):
        mail_message_obj = self.env['mail.message']
        fileobj = open('/opt/mail_message.csv')
        str_csv_data = fileobj.read()
        list = csv.reader(StringIO.StringIO(str_csv_data), delimiter='|')

        create_id_list = []
        mail_message_list = []
        double_id_list = []
        no_id_list = []
        rownum = 0
        for row in list:
            if row == '':
                continue

            if rownum == 0:
                rownum += 1
            else:
                try:
                    print "<<<<<<<<<row[0]<<<<<<<<<<<",row[0]
                    crm_lead_id = self.env['crm.lead'].search([('name', '=', str(row[0]).strip())])
                    _logger.info('<<<<<<<<<<<crm_lead_id<<<<<<<< %s', crm_lead_id)

                    if len(crm_lead_id) > 1:
                        double_id_list.append(crm_lead_id)

                    if len(crm_lead_id) == 0:
                        no_id_list.append(str(row[0]).strip())
                        type = ''
                        if str(row[14]).strip() == 'Email':
                            type = 'email'
                        elif str(row[14]).strip() == 'Comment':
                            type = 'comment'
                        else:
                            type = 'notification'


                        vals = {
                            'subject': str(row[3]).strip(),
                            'message_id': str(row[4]).strip(),
                            'body': str(row[5]).strip(),
                            'record_name': str(row[6]).strip(),
                            'no_auto_thread': str(row[7]).strip(),
                            'date': str(row[8]).strip(),
                            'model': str(row[9]).strip(),
                            'reply_to': str(row[10]).strip(),
                            'message_type': type,
                            'email_from': str(row[12]).strip(),
                            'website_published': str(row[13]).strip(),
                            'path': str(row[14]).strip(),

                        }
                        _logger.info('<<<<<<<<<<<<<<<<vals<<<<<<<<<<<<<< %s', vals)

                        mail_message_id = self.env['mail.message'].search([('message_id', '=', str(row[4]).strip())])
                        _logger.info('<<<<<<<<<<<mail_message_id<<<<<<<< %s', mail_message_id)

                        if mail_message_id:
                            mail_message_list.append(mail_message_id)
                            continue

                        message_id = mail_message_obj.create(vals)
                        _logger.info('<<<<<<<<<<<<<<message_id<<<<<<<<<<< %s', message_id)
                        create_id_list.append(message_id)

                        if row[2] == '' or len(message_id) == 0:
                            continue
                        self._cr.execute("""update mail_message set create_date=%s where id=%s""",(row[2] or False, message_id.id))
                        self._cr.commit()


                    if len(crm_lead_id) <= 1:
                        type = ''
                        if str(row[14]).strip() == 'Email':
                            type = 'email'
                        elif str(row[14]).strip() == 'Comment':
                            type = 'comment'
                        else:
                            type = 'notification'

                        vals = {
                            'subject': str(row[3]).strip(),
                            'message_id': str(row[4]).strip(),
                            'body': str(row[5]).strip(),
                            'record_name': str(row[6]).strip(),
                            'no_auto_thread': str(row[7]).strip(),
                            'date': str(row[8]).strip(),
                            'model': str(row[9]).strip(),
                            'reply_to': str(row[10]).strip(),
                            'message_type': type,
                            'email_from': str(row[12]).strip(),
                            'website_published': str(row[13]).strip(),
                            'path': str(row[14]).strip(),
                            'res_id': crm_lead_id.id or False,

                        }
                        _logger.info('<<<<<<<<<<<<<<<<vals<<<<<<<<<<<<<< %s', vals)

                        mail_message_id = self.env['mail.message'].search([('message_id', '=', str(row[4]).strip())])
                        _logger.info('<<<<<<<<<<<mail_message_id<<<<<<<< %s', mail_message_id)

                        if mail_message_id:
                            mail_message_list.append(mail_message_id)
                            continue

                        message_id = mail_message_obj.create(vals)
                        _logger.info('<<<<<<<<<<<message_id<<<<<<<< %s', message_id)
                        create_id_list.append(message_id)


                        if row[2] == '' or len(message_id) == 0:
                            continue
                        self._cr.execute("""update mail_message set create_date=%s where id=%s""",(row[2] or False, message_id.id))
                        self._cr.commit()


                except Exception,e:
                    _logger.info('<<<<<<<<<<<<<Exception<<<<<<<<<<<< %s', e)


        _logger.info('<<<<<<<<<<<<<double_id_list<<<<<<<<<<<< %s', double_id_list)
        _logger.info('<<<<<<<<<<<<<no_id_list<<<<<<<<<<<< %s', no_id_list)
        _logger.info('<<<<<<<<<<<<<create_id_list<<<<<<<<<<<< %s', create_id_list)
        _logger.info('<<<<<<<<<<<<<mail_message_list<<<<<<<<<<<< %s', mail_message_list)

        _logger.info('<<<<<len<<<<<<<<double_id_list<<<<<<<<<<<< %s', len(double_id_list))
        _logger.info('<<<<<len<<<<<<<<no_id_list<<<<<<<<<<<< %s', len(no_id_list))
        _logger.info('<<<<<len<<<<<<<<create_id_list<<<<<<<<<<<< %s', len(create_id_list))
        _logger.info('<<<<<len<<<<<<<<mail_message_list<<<<<<<<<<<< %s', len(mail_message_list))
















