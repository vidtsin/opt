import sys,os
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

# for file size check .
class FilestoreGeneric(object):
    def __init__(self, file_data='', extension='',file_name=''):
        self.file_data = file_data
        self.extension = extension
        self.file_name = file_name

    def check_size(self,file_data,extension):
        file_size = sys.getsizeof(file_data)

        allow_ext_lst = ['.jpeg', '.jpg', '.gif', '.doc', '.docx', '.xls', '.xlsx']
        flag = False
        if extension == '.pdf' and file_size > 3000000:
            flag = True
            raise UserError(_('File size exceeds the specified size limit!'
                              '\n Kindly upload files of proper size..'))
        else:
            for ext in allow_ext_lst:
                if extension == ext and file_size > 500000:
                    flag = True
                    raise UserError(_('File size exceeds the specified size limit!'
                                      '\n Kindly upload files of proper size..'))

        return flag

    # for file extension
    def check_extension(self,file_name1):
        allow_ext_lst = ['.pdf', '.jpeg', '.jpg', '.gif', '.doc', '.docx', '.xls', '.xlsx']
        flag = False
        if file_name1:
            extension = file_name1[file_name1.rfind('.'):]
            if extension not in allow_ext_lst:
                flag = True
        return flag