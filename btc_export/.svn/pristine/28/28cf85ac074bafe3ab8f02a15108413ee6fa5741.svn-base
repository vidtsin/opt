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

class wizard_res_import(models.TransientModel):
    _name = "wizard.res.import"

    import_csv = fields.Binary('Import Data')

    @api.multi
    def action_res(self):
        import_data_obj = self.env['res.partner']
        statement_vals = []
        csv_datas = self.import_csv
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(csv_datas))
        fileobj.seek(0)
        str_csv_data = fileobj.read()
        list = csv.reader(StringIO.StringIO(str_csv_data), delimiter=',')

        print "=========list=========", list

        transactions = []

        rownum = 0
        for row in list:
            if row == '':
                continue

            if rownum == 0:
                print"header"
                rownum += 1
            else:


                email = ''
                if not row[1]:

                    res_id = import_data_obj.search([('name','=',row[2])])
                    for res in res_id:
                        self._cr.execute("""update crm_lead set create_date=%s where id=%s""",
                                         (row[3], res.id))

                        self._cr.commit()

                else:
                    email = row[1]

                    res_id = import_data_obj.search([('name','=',row[2]),('email','=',email)])

                    print "---------res_id----------",res_id

                    for res in res_id:
                        self._cr.execute("""update res_partner set create_date=%s where id=%s""",
                                     (row[3],res.id))

                        self._cr.commit()
















