from base64 import b64decode
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import xlrd
import logging
_logger = logging.getLogger(__name__)


class products_import(models.TransientModel):
    _name = 'products.import'
    _description = 'Import Products'

    data_file = fields.Binary(string='Products File', required=True, help='Get products in excel sheet format from your QuickBooks and select them here.')

    @api.multi
    def import_products_file(self):
        """
            Import Products using excel sheet
        :return: True
        """
        product_obj = self.env['product.template']

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

                    product_type=str(final_each_row[3]).strip(' ') or '',
                    print"product_type",product_type[0]

                    if final_each_row[3] == 'Inventory':
                        type ='product'


                    elif final_each_row[3] == 'Non-inventory':
                        type ='service'

                    else :
                        type='consu'







                    income_account=str(final_each_row[6]).strip(' ') or '',
                    expense_account=str(final_each_row[9]).strip(' ') or '',

                    income_account_id=self.env['account.account'].search([('name','=',income_account)])

                    expense_account_id = self.env['account.account'].search([('name', '=', expense_account)])
                    vals ={
                        'name' : final_each_row[0],
                        # 'partner_id' : str(final_each_row[1]).strip(' ') or '',
                        'description_sale': str(final_each_row[1]),
                        'default_code' : final_each_row[2],
                        'type' : type,
                        'list_price': final_each_row[4],
                        'property_account_income_id':income_account_id.id,
                        'description_purchase': str(final_each_row[7]),
                        'standard_price': final_each_row[8],
                        'property_account_expense_id':expense_account_id.id,
                        'quickbooks_import':True,
                        'taxes_id':'',
                        'supplier_taxes_id':'',

                    }
                    print"vals",vals
                    if vals.get('default_code'):
                        product_temp_id=self.env['product.template'].search([('default_code','=',vals.get('default_code'))])

                        if not product_temp_id:
                            tem_id = product_obj.create(vals)
                            product_product_id = self.env['product.product'].search([('product_tmpl_id', '=', tem_id.id)])
                            product_product_id.quick_prod_id = tem_id.quick_prod_id
                            if vals.get('type') == 'product':
                                # location_id = request.env['stock.location'].search(
                                #     [('name', '=', 'WH'), ('usage', '=', 'view')])
                                # stock_loc_id = request.env['stock.location'].search([('location_id', '=', location_id.id)])
                                if final_each_row[10] < 0:
                                    final_each_row[10] ='0'
                                stock_val = {
                                    'location_id': 15,
                                    'new_quantity':final_each_row[10],
                                    'product_id': product_product_id.id
                                }

                                stock_product_change_id = self.env['stock.change.product.qty'].create(stock_val)
                                stock_product_change_id.change_product_qty()
                        else:
                            update_product_id = product_temp_id.write(vals)
                            product_product_id =self.env['product.product'].search([('product_tmpl_id', '=', product_temp_id.id)])
                            stock_product_qty=self.env['stock.quant'].search([('product_id','=',product_temp_id.id)])
                            # if stock_product_qty:
                            #     stock_val = {
                            #         'location_id': 15,
                            #         'new_quantity': final_each_row[10],
                            #         'product_id': stock_product_qty.id
                            #     }
                            update_stock_value= stock_product_qty.update({'qty': final_each_row[10],'product_id': product_product_id.id})
                            print"update_product_id", update_stock_value
                    else:
                        product_temp_id = self.env['product.template'].search([('name', '=', vals.get('name'))])

                        if not product_temp_id:
                            tem_id = product_obj.create(vals)
                            product_product_id = self.env['product.product'].search(
                                [('product_tmpl_id', '=', tem_id.id)])
                            product_product_id.quick_prod_id = tem_id.quick_prod_id
                            if vals.get('type') == 'product':
                                # location_id = request.env['stock.location'].search(
                                #     [('name', '=', 'WH'), ('usage', '=', 'view')])
                                # stock_loc_id = request.env['stock.location'].search([('location_id', '=', location_id.id)])
                                if final_each_row[10] < 0:
                                    final_each_row[10] = '0'
                                stock_val = {
                                    'location_id': 15,
                                    'new_quantity': final_each_row[10],
                                    'product_id': product_product_id.id
                                }

                                stock_product_change_id = self.env['stock.change.product.qty'].create(stock_val)
                                stock_product_change_id.change_product_qty()
                        else:
                            update_product_id = product_temp_id.write(vals)
                            product_product_id = self.env['product.product'].search(
                                [('product_tmpl_id', '=', product_temp_id.id)])
                            stock_product_qty = self.env['stock.quant'].search(
                                [('product_id', '=', product_temp_id.id)])
                            if stock_product_qty:
                                if final_each_row[10] < 0:
                                    final_each_row[10] = '0'
                            update_stock_value = stock_product_qty.update(
                                {'qty': final_each_row[10], 'product_id': product_product_id.id})
                            print"update_product_id", update_stock_value


        return True