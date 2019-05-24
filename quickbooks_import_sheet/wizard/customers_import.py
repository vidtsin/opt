from base64 import b64decode
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import xlrd
import logging
_logger = logging.getLogger(__name__)


class customers_import(models.TransientModel):
    _name = 'customers.import'
    _description = 'Import Customers'

    data_file = fields.Binary(string='Customers File', required=True, help='Get customers in excel sheet format from your QuickBooks and select them here.')

    @api.multi
    def import_customers_file(self):
        """
            Import Customers using excel sheet
        :return: True
        """
        customer_obj = self.env['res.partner']
        data_filess = b64decode(self.data_file)
        wb = xlrd.open_workbook(file_contents=data_filess)
        for s in wb.sheets():
            for row in range(s.nrows):
                if row == 0:
                    continue
                else:
                    data_row = []
                    for col in range(s.ncols):
                        value = (s.cell(row, col).value)
                        data_row.append(value)

                    # get final row with data
                    final_each_row = data_row
                    # print"final_each_row<<<<<<<<<<<<<<<<", final_each_row

                    state_code=str(final_each_row[4]).strip(' ') or '',
                    country_name=str(final_each_row[5]).strip(' ') or '',

                    country_id=self.env['res.country'].search([('name','=',country_name)])

                    state_id = self.env['res.country.state'].search([('country_id', '=', country_id.id),('code','=',state_code)])
                    vals ={
                        'name' : str(final_each_row[0]).strip(' ') or '',
                        # 'partner_id' : str(final_each_row[1]).strip(' ') or '',
                        'street': str(final_each_row[2]).strip(' ') or '',
                        'city' : str(final_each_row[3]).strip(' ') or '',
                        'state_id' : state_id.id,
                        'country_id': country_id.id,
                        'zip': str(final_each_row[6]).strip(' ') or '',
                        'phone': str(final_each_row[7]).strip(' ') or '',
                        'email': str(final_each_row[8]).strip(' ') or '',
                        'comment': str(final_each_row[12]).strip(' ') or '',
                        'quickbooks_import': True

                    }
                    print"vals", vals
                    if vals.get('name') or vals.get('email') or vals.get('phone'):
                        customer_rec=customer_obj.search([('name', '=', vals.get('name')),('email','=',vals.get('email')),('phone','=',vals.get('phone'))])
                        if customer_rec:
                            customer_rec.write(vals)

                        customer_rec_name_email= customer_obj.search(
                            [('name', '=', vals.get('name')), ('email', '=', vals.get('email')), ('phone', '=',False)])
                        if customer_rec_name_email:
                            customer_rec_name_email.write(vals)

                        customer_rec_name_phone = customer_obj.search(
                            [('name', '=', vals.get('name')), ('email', '=', False), ('phone','=',vals.get('phone'))])
                        if customer_rec_name_phone:
                            customer_rec_name_phone.write(vals)

                        customer_rec_email_phone = customer_obj.search(
                            [('name', '=', False), ('email', '=', vals.get('email')), ('phone', '=', vals.get('phone'))])
                        if customer_rec_email_phone:
                            customer_rec_email_phone.write(vals)

                        customer_rec_name = customer_obj.search(
                            [('name', '=', vals.get('name')), ('email', '=', False), ('phone', '=', False)])
                        if customer_rec_name:
                            customer_rec_name.write(vals)



                        if not  customer_rec and not customer_rec_name_email and not customer_rec_name_phone and not customer_rec_name:
                             customer_id = customer_obj.create(vals)
                             _logger.info('<<<<<<<<<<<<<<<<account_id<<<create<<<<<<<<<<< %s', customer_id)









                    # elif vals.get('name') and vals.get('email'):
                    #     customer_rec=customer_obj.search([('name', '=', vals.get('name')),('email','=',vals.get('email'))])
                    #     if customer_rec:
                    #         customer_rec.write(vals)
                    #
                    #     customer_rec_name_email= customer_obj.search(
                    #         ['|',('name', '=', vals.get('name')), ('email', '=', vals.get('email'))])
                    #     if customer_rec_name_email:
                    #         customer_rec_name_email.write(vals)
                    #
                    #     if not  customer_rec and not customer_rec_name_email:
                    #          customer_id = customer_obj.create(vals)
                    #          _logger.info('<<<<<<<<<<<<<<<<account_id<<<create<<<<<<<<<<< %s', customer_id)
                    #
                    # elif vals.get('email') and vals.get('phone'):
                    #     customer_rec=customer_obj.search([('email','=',vals.get('email')),('phone','=',vals.get('phone'))])
                    #     if customer_rec:
                    #         customer_rec.write(vals)
                    #
                    #     customer_rec_email_phone = customer_obj.search(
                    #         ['|',('email', '=', vals.get('email')), ('phone', '=', vals.get('phone'))])
                    #     if customer_rec_email_phone:
                    #         customer_rec_email_phone.write(vals)
                    #
                    #
                    #     if not  customer_rec and not customer_rec_name:
                    #          customer_id = customer_obj.create(vals)
                    #          _logger.info('<<<<<<<<<<<<<<<<account_id<<<create<<<<<<<<<<< %s', customer_id)
                    # elif vals.get('name') and vals.get('phone'):
                    #     customer_rec=customer_obj.search([('name', '=', vals.get('name')),('phone','=',vals.get('phone'))])
                    #     if customer_rec:
                    #         customer_rec.write(vals)
                    #
                    #     customer_rec_name_phone= customer_obj.search(
                    #         ['|',('name', '=', vals.get('name')), ('phone', '=',vals.get('phone'))])
                    #     if customer_rec_name_email:
                    #         customer_rec_name_email.write(vals)
                    #
                    #
                    #     if not  customer_rec and not customer_rec_name_phone:
                    #          customer_id = customer_obj.create(vals)
                    #          _logger.info('<<<<<<<<<<<<<<<<account_id<<<create<<<<<<<<<<< %s', customer_id)
                    # else:
                    #     customer_rec_name = customer_obj.search(
                    #         [('name', '=', vals.get('name'))])
                    #     if customer_rec_name_email:
                    #         customer_rec_name_email.write(vals)
                    #     if not customer_rec_name_email:
                    #         customer_id = customer_obj.create(vals)


        return True
