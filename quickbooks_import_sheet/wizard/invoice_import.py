from base64 import b64decode
from odoo import api, fields, models, _
from odoo.exceptions import UserError
# import datetime
from datetime import datetime
import xlrd
import logging
_logger = logging.getLogger(__name__)
import array


class invoices_import(models.TransientModel):
    _name = 'invoice.import'
    _description = 'Import Invoice'

    data_file = fields.Binary(string='Customers File', required=True, help='Get customers in excel sheet format from your QuickBooks and select them here.')

    @api.multi
    def import_invoices_file(self):
        """
            Import Invoices using excel sheet
        :return: True
        """
        account_obj = self.env['account.invoice']

        data_filess = b64decode(self.data_file)
        wb = xlrd.open_workbook(file_contents=data_filess)
        for s in wb.sheets():
            for row in range(s.nrows-1):
                if row <= 1:
                    continue
                else:
                    data_row = []
                    for col in range(s.ncols):
                        value = (s.cell(row, col).value)
                        data_row.append(value)

                    # get final row with data
                    final_each_row = data_row
                    inv_date = final_each_row[3]

                    if inv_date:
                        a1_as_datetime = datetime(*xlrd.xldate_as_tuple(inv_date, wb.datemode))
                        print 'datetime: %s' % a1_as_datetime
                        date= datetime.strptime(str(a1_as_datetime), '%Y-%m-%d %H:%M:%S')
                        date_invoice=date.strftime("%Y-%m-%d")

                    type=final_each_row[11]
                    account_type=self.env['account.account.type'].search([('name','=',type)])
                    account=final_each_row[7].strip(' ')
                    account_split=account.split(' ')[1]
                    print"account_split",account_split
                    account_code =account.split(account_split)[0]
                    print"account_code",account_code
                    account_name = account.split(account_split)[1]
                    print"account_name", account_name
                    account_id = self.env['account.account'].search([('name','=',account_name)])
                    if not account_id:
                        account_id=self.env['account.account'].create({'name':account_name,'user_type_id':account_type.id,'quickbooks_import':True})
                    product=final_each_row[5].strip()
                    product_temp_id = self.env['product.template'].search([('name', '=', product)])
                    if not product_temp_id:
                        product_temp_id= self.env['product.product'].create({'name':product})

                    customer=  final_each_row[4]
                    if customer:
                        partner_id = self.env['res.partner'].search([('name','=',customer)])
                        if not partner_id:
                            partner_id= self.env['res.partner'].create({'name':customer})


                        customers_invoice_vals = {
                            'date_invoice': date_invoice,
                            'partner_id' : partner_id.id,
                            'account_id': account_id.id,
                            'quickbooks_import_invoice':True

                        }
                        customer_invoice_id = self.env['account.invoice'].create(customers_invoice_vals)
                        inv_line_vals = {
                            'invoice_id': customer_invoice_id.id,
                            # 'name': row[3].strip(),
                            'product_id': product_temp_id.id,
                            'name': final_each_row[6],
                            'account_id': account_id.id,
                            'quantity': final_each_row[8],
                            'price_unit': final_each_row[9],
                            'quickbooks_import_invoice_line':True,

                        }
                        invoice_line_ids = self.env['account.invoice.line'].create(inv_line_vals)
                    else:
                        inv_line_vals = {
                            'invoice_id': customer_invoice_id.id,
                            'product_id': product_temp_id.id,
                            'name': final_each_row[7],
                            'account_id': account_id.id,
                            'quantity': final_each_row[9],
                            'price_unit': final_each_row[10],
                            'quickbooks_import_invoice_line': True,
                        }

                        invoice_line_ids = self.env['account.invoice.line'].create(inv_line_vals)
                    customer_invoice_id.action_invoice_open()

                    self.env.cr.commit()

        return True