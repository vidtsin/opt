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
    _name = "wizard.user"

    import_csv = fields.Binary('Import Data')

    @api.multi
    def action_office(self):
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

                res_id = self.env['res.partner'].search([('name', '=', row[2]), ('email', '=', row[1])])
                _logger.info('res_id============ %s', res_id)

                if row[6] == '' or len(res_id) == 0:
                    continue
                self._cr.execute("""update res_partner set office_phone_no=%s where id=%s""", (row[6] or '', res_id[0].id))
                self._cr.commit()

    @api.multi
    def action_prospect3(self):
        import_data_obj = self.env['res.partner']
        csv_datas = self.import_csv
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(csv_datas))
        fileobj.seek(0)
        str_csv_data = fileobj.read()
        list = csv.reader(StringIO.StringIO(str_csv_data), delimiter=',')

        print "=========list=========", list
        count = 0
        rownum = 0
        for row in list:
            if row == '':
                continue

            if rownum == 0:
                print"header"
                rownum += 1
            else:
                print"row"

                # res_id = self.env['res.partner'].search([('name', '=', str(row[2].strip(' '))), ('email', '=', str(row[1].strip(' ')))])
                # if row[1] :
                #     # res_id = self.env['res.partner'].search([('name', '=', row[2]), ('email', '=', row[1])])
                #     res_id = self.env['res.partner'].search([('name', '=', row[2]), ('email', '=', row[1])])
                #
                # else:
                #     res_id = self.env['res.partner'].search([('name', '=', row[2])])
                # if row[4]:
                #     user_view_id = self.env['res.users'].search([('name', '=',row[4])])
                #     print 'user_view_id==================',user_view_id
                #
                # # _logger.info('res_id============ %s', res_id)
                #
                # if row[4] == '' or len(res_id) == 0:
                #     continue
                #
                # if user_view_id :
                #     # res_id.write({'user_id':user_view_id.id})
                #     # print "=================res_id===========", res_id
                #     # print "=================user_view_id===========", user_view_id
                #     self._cr.execute("""update res_partner set user_id=%s where id=%s""", (user_view_id.id, res_id[0].id))
                #     count+=1
                #     print "==========count====================",count
                #     self._cr.commit()

                if row[5]:
                    user_view_id = self.env['res.users'].search([('login', '=', row[5])])
                    print 'user_view_id==================', user_view_id
                    if user_view_id:
                        email = ''
                        if not row[1]:

                                    res_id = import_data_obj.search([('name','=',row[2])])


                                    for res in res_id:
                                        self._cr.execute("""update res_partner set user_id=%s where id=%s""",
                                                         (user_view_id.id, res_id[0].id))

                                        self._cr.commit()

                        else:
                                    email = row[1]

                                    res_id = import_data_obj.search([('name','=',row[2]),('email','=',email)])

                                    print "---------res_id----------",res_id

                                    for res in res_id:
                                        self._cr.execute("""update res_partner set user_id=%s where id=%s""",
                                                     (user_view_id.id,res_id[0].id))

                                        self._cr.commit()




































