from odoo import models, fields, api, _
import csv
from odoo.http import request
from tempfile import TemporaryFile
import StringIO
import base64
import logging
_logger = logging.getLogger(__name__)

class wizard_export(models.TransientModel):
    _name = "wizard.export"

    import_data = fields.Binary('Import Data')

    @api.multi
    def action_next(self):
        import_data_obj = self.env['res.partner']
        statement_vals = []
        csv_datas = self.import_data
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
                print"row"

                latitude = row[6].strip("'")
                longitude = row[7].strip("'")
                print "--------------row[2]--------", row[2]

                country_id = self.env['res.country'].search([('code', '=', row[34])])

                vals= {'city' : row[1],
                       # 'country_id' : row[2],
                       'country_id' :country_id.id,
                       'create_date' : row[3],
                       'fax' : row[4],
                       'email' : row[5],
                       'partner_latitude' : latitude,
                       'partner_longitude' : longitude,
                       'customer' : row[8],
                       'supplier' : row[9],
                       'function' : row[10],
                       'grade_id' : row[12],
                       'partner_weight' : row[13],
                       'activation' : row[14],
                       # 'date_review' : row[15],
                       # 'date_review_next' : row[16],
                       'name' : row[17],
                       # 'comment' : row[18],
                       'state_id' : row[19],
                       'street' : row[20],
                       'street2' : row[21],
                       'vat' : row[22],
                       'category_id' : row[23],
                       # 'title' : row[24],
                       'debit' : row[25],
                       'credit' : row[26],
                       'property_supplier_payment_term_id' : row[27],
                       'property_payment_term_id' : row[28],
                       # 'property_account_payable_id' : row[29],
                       # 'property_account_receivable_id' : row[30],
                       'zip' : row[31],
                       'website' : row[32]


                }

                print "=====vals=======",vals

                import_obj = import_data_obj.create(vals)

