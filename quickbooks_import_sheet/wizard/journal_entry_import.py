from base64 import b64decode
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import xlrd
import logging
_logger = logging.getLogger(__name__)


class journal_entry_import(models.TransientModel):
    _name = 'journal.entry.import'
    _description = 'Import Journal Entry'

    data_file = fields.Binary(string='Journal Entry File', required=True, help='Get customers in excel sheet format from your QuickBooks and select them here.')

    @api.multi
    def import_journal_entry_file(self):
        """
            Import Journal entry using excel sheet
        :return: True
        """
        acc_move = self.env['account.move']
        data_filess = b64decode(self.data_file)
        wb = xlrd.open_workbook(file_contents=data_filess)
        for s in wb.sheets():
            for row in range(s.nrows):
                if row <= 1:
                    continue
                else:
                    data_row = []
                    for col in range(s.ncols):
                        value = (s.cell(row, col).value)
                        data_row.append(value)

                    # get final row with data
                    final_each_row = data_row
                    # print"final_each_row<<<<<<<<<<<<<<<<", final_each_row


                    acc_move_vals = {
                        'journal_id':'',
                        'date':'',
                        'ref':'',

                    }
                    account_move = acc_move.create(acc_move_vals)
                    acc_move_line_vals={
                                     'journal_id': account_move.id,
                                    'accound_id':'',
                                    'debit':'',
                                    'credit':'',

                    }
                    account_move_line =self.env['account.move.line'].create(acc_move_line_vals)





        return True