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

class wizard_prospect(models.TransientModel):
    _name = "wizard.prospect"

    import_csv = fields.Binary('Import Data')

    @api.multi
    def action_prospect(self):
        import_data_obj = self.env['res.partner']
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

                res_id = self.env['res.partner'].search([('name', '=', row[3]), ('email', '=', row[4])])
                _logger.info('res_id============ %s', res_id)

                if row[1] == '' or len(res_id) == 0:
                    continue
                self._cr.execute("""update res_partner set phone=%s where id=%s""", (row[1] or '', res_id[0].id))
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















