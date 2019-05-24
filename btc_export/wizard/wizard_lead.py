from odoo import models, fields, api, _
import csv
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.http import request
from tempfile import TemporaryFile
import StringIO
import base64
# import time
# import datetime
import logging
_logger = logging.getLogger(__name__)

class wizard_export_lead(models.TransientModel):
    _name = "wizard.lead.import"

    import_csv = fields.Binary('Import Data')

    @api.multi
    def action_next1(self):
        import_data_obj = self.env['crm.lead']
        csv_datas = self.import_csv
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(csv_datas))
        fileobj.seek(0)
        str_csv_data = fileobj.read()
        list = csv.reader(StringIO.StringIO(str_csv_data), delimiter=',')

        print "=========list=========", list

        rownum = 0
        for row in list:
            if row == '':
                continue

            if rownum == 0:
                print"header"
                rownum += 1
            else:
                print"row"

                crm_id = self.env['crm.lead'].search([('contact_name', '=', row[3]), ('email_from', '=', row[4])])
                _logger.info('crm_id============ %s', crm_id)

                if row[2] == '' or len(crm_id) == 0:
                    continue
                self._cr.execute("""update crm_lead set create_date=%s where id=%s""", (row[2] or '', crm_id[0].id))
                self._cr.commit()





















        # import_data_obj = self.env['crm.lead']
        # statement_vals = []
        # csv_datas = self.import_csv
        # fileobj = TemporaryFile('w+')
        # fileobj.write(base64.decodestring(csv_datas))
        # fileobj.seek(0)
        # str_csv_data = fileobj.read()
        # list = csv.reader(StringIO.StringIO(str_csv_data), delimiter=',')
        #
        # print "=========list=========", list
        #
        # transactions = []
        #
        # rownum = 0
        # for row in list:
        #     if row == '':
        #         continue
        #
        #     if rownum == 0:
        #         print"header"
        #         rownum += 1
        #     else:
        #
        #
        #         email = ''
        #         if not row[1]:
        #
        #             lead_id = import_data_obj.search([('name','=',row[5])])
        #             for lead in lead_id:
        #                 self._cr.execute("""update crm_lead set create_date=%s where id=%s""",
        #                                  (row[7], lead.id))
        #
        #                 self._cr.commit()
        #
        #         else:
        #             email = row[1]
        #
        #             lead_id = import_data_obj.search([('name','=',row[5]),('email_from','=',email)])
        #         #
        #             print "---------lead_id----------",lead_id
        #         # if lead_id:
        #         #     currentTimeTo = row[7]
        #         #     currentTimeTo = time.strptime(str(currentTimeTo), "%Y-%m-%d %H:%M:%S")
        #         #     currentTimeTo = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT, currentTimeTo)
        #         #     write_resp = lead_id[0].write({'create_date': currentTimeTo})
        #             for lead in lead_id:
        #                 self._cr.execute("""update crm_lead set create_date=%s where id=%s""",
        #                              (row[7],lead.id))
        #
        #                 self._cr.commit()
        #















