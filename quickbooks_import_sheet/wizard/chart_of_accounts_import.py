# -*- coding: utf-8 -*-
from base64 import b64decode
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import xlrd
import logging
_logger = logging.getLogger(__name__)


class chart_of_accounts_import(models.TransientModel):
    _name = 'chart.of.accounts.import'
    _description = 'Import Chart of Accounts'

    data_file = fields.Binary(string='Chart of Accounts File', required=True, help='Get chart of accounts in excel sheet format from your QuickBooks and select them here.')

    @api.multi
    def import_chart_of_accounts_file(self):
        """
            Import Chart of Accounts using excel sheet
        :return: True
        """
        account_obj = self.env['account.account']
        account_type_obj = self.env['account.account.type']
        data_filess = b64decode(self.data_file)
        wb = xlrd.open_workbook(file_contents=data_filess)

        missing_acc_type = []
        account_account_exists = []
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

                    if final_each_row[1] == '':
                        continue

                    reconcile = False
                    type = ''
                    name = str(final_each_row[1]).strip(' ') or ''
                    acc_type = str(final_each_row[2]).strip(' ') or ''

                    if acc_type == 'Accounts Payable':
                        type = 'Payable'
                        reconcile = True
                    elif acc_type == 'Bank':
                        type = 'Bank and Cash'
                        reconcile = False
                    elif acc_type == 'Accounts Receivable':
                        type = 'Receivable'
                        reconcile = True
                    elif acc_type == 'Accounts Receivable (A/R)':
                        type = 'Receivable'
                        reconcile = True
                    elif acc_type == 'Other Current Assets':
                        type = 'Current Assets'
                        reconcile = True
                    elif acc_type == 'Fixed Assets':
                        type = 'Fixed Assets'
                        reconcile = True
                    elif acc_type == 'Credit Card':
                        type = 'Credit Card'
                        reconcile = False
                    elif acc_type == 'Other Current Liability':
                        type = 'Current Liabilities'
                        reconcile = True
                    elif acc_type == 'Other Current Liabilities':
                        type = 'Current Liabilities'
                        reconcile = True
                    elif acc_type == 'Long Term Liability':
                        type = 'Current Liabilities'
                        reconcile = True
                    elif acc_type == 'Long Term Liabilities':
                        type = 'Current Liabilities'
                        reconcile = True
                    elif acc_type == 'Equity':
                        type = 'Equity'
                        reconcile = False
                    elif acc_type == 'Income':
                        type = 'Income'
                        reconcile = False
                    elif acc_type == 'Cost of Goods Sold':
                        type = 'Current Liabilities'
                        reconcile = True
                    elif acc_type == 'Expense':
                        type = 'Expenses'
                        reconcile = False
                    elif acc_type == 'Other Income':
                        type = 'Other Income'
                        reconcile = False
                    elif acc_type == 'Other Expense':
                        type = 'Expenses'
                        reconcile = False
                    else:
                        missing_acc_type.append(acc_type)
                        continue

                    acc_type_id = account_type_obj.search([('name', '=', type)])

                    acc_id = account_obj.search([('name', '=', name), ('user_type_id', '=', acc_type_id.id)])
                    if acc_id:
                        account_account_exists.append(acc_id)
                        continue
                    else:
                        val = {
                            'name' : name,
                            'user_type_id' : acc_type_id.id,
                            'reconcile' : reconcile,
                            'quickbooks_import' : True,
                        }
                        account_id = account_obj.create(val)
                        _logger.info('<<<<<<<<<<<<<<<<account_id<<<create<<<<<<<<<<< %s', account_id)

        _logger.info('<<<<<<<<<<<<<<<<missing_acc_type<<<<<<<<<<<<<< %s', missing_acc_type)
        _logger.info('<<<<<<<<<<<<<<<<account_account_exists<<<<<<<<<<<<<< %s', account_account_exists)

        return True