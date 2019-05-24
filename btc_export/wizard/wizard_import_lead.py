from odoo import models, fields, api, _
import csv
from odoo.http import request
from odoo.exceptions import UserError
from tempfile import TemporaryFile
import StringIO
import base64
import logging
_logger = logging.getLogger(__name__)

class wizard_export(models.TransientModel):
    _name = "wizard.lead"

    import_data = fields.Binary('Import Data')

    @api.multi
    def action_lead_import(self):
        import_data_obj = self.env['crm.lead']
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

                latitude = row[8].strip("'")
                longitude = row[9].strip("'")

                if row[28]:
                    crm_team_id = self.env['crm.team'].search([('name', '=', row[28] or '')])
                    _logger.info('crm_id============ %s', crm_team_id)

                # if row[29]:
                #     user_id = self.env['res.users'].search([('name', '=', row[18] or ''), ('email', '=', row[19] or '')])
                #     _logger.info('user_id============ %s', user_id)


                vals= {'app_id' : row[1],
                        'partner_assigned_id' : row[2],
                        'city' : row[3],
                        # 'comment' : row[4],
                        'create_date' : row[7],
                        'form no' : row[10],
                        'mobile' : row[12],
                        'fax' : row[13],
                        'email_from' : row[14],
                        'name' : row[15],
                        'opt_out' : row[20],
                        'phone' : row[21],
                        'probability' : row[22],
                        'program' : row[23],
                        'prospect_id' : row[25],
                        'referred' : row[27],
                        'street2' : row[32],
                        'street' : row[33],
                        'tag_ids' : row[34],
                        'zip' : row[36],
                        'contact_name' : row[37],
                       'country_id': row[6],
                       'partner_lattitude': latitude,
                       'partner_longitude': longitude,
                       # 'team_id': crm_team_id.id,
                       # 'user_id': user_id.id,

                       }

                _logger.info('vals===lead========= %s', vals)

                crm_id = import_data_obj.create(vals)
                _logger.info('crm_id============ %s', crm_id)







    @api.multi
    def import_date_fields(self):
        import_data_obj = self.env['crm.lead']
        csv_datas = self.import_data
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

                crm_id = self.env['crm.lead'].search([('contact_name', '=', row[11] or ''),('email_from', '=', row[9] or '')])
                _logger.info('crm_id============ %s', crm_id)

                partner_id = self.env['res.partner'].search([('name', '=', row[11])])
                _logger.info('partner_id============ %s', partner_id)

                funding_val = ''
                # row[6]
                if row[6] == 'Family':
                    funding_val = 'family'
                elif row[6] == 'OSAP':
                    funding_val = 'osap'
                elif row[6] == 'Second Career':
                    funding_val = 'career'
                elif row[6] == 'WSIB':
                    funding_val = 'wsib'
                elif row[6] == 'Registered Retiremnet Saving Paln RRSP':
                    funding_val = 'retirement'
                elif row[6] == 'Registered Education Saving Paln RRSP':
                    funding_val = 'education'
                elif row[6] == 'Out of Province Funding':
                    funding_val = 'province_funding'
                elif row[6] == 'Bank Loan':
                    funding_val = 'bank_loan'
                elif row[6] == 'Self Funded':
                    funding_val = 'self_funded'
                elif row[6] == 'Other':
                    funding_val = 'other'

                partner = False
                if len(partner_id):
                    partner=partner_id[0].id



                if crm_id:
                    vals= {'app_id' : row[1] or False,
                           'x_dob': row[2] or False,
                           'form_no': row[3] or False,
                           'x_program': row[4] or False,

                           'x_career_option': row[5] or False,
                           'x_funding': funding_val or False,
                           'x_prospect_id': row[7] or False,
                           'x_qualification': row[8] or False,
                           'partner_id': partner,

                           }

                    lead_id = crm_id.write(vals)
                    _logger.info('lead_id===update======== %s', lead_id)


                    if row[12] == '' or len(crm_id) == 0:
                        continue
                    self._cr.execute("""update crm_lead set create_date=%s where id=%s""", (row[12] or '', crm_id[0].id))
                    self._cr.commit()

                    self._cr.commit()




    @api.multi
    def import_sales_data(self):
        import_data_obj = self.env['crm.lead']
        csv_datas = self.import_data
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


                crm_id = self.env['crm.lead'].search([('contact_name', '=', row[5] or ''),('email_from', '=', row[6] or '')])
                _logger.info('crm_id============ %s', crm_id)

                sales_team = self.env['crm.team'].search([('name', '=', row[1] or '')])
                _logger.info('sales_team============ %s', sales_team)

                user_id = self.env['res.users'].search([('name', '=', row[3] or ''), ('email', '=', row[2] or '')])
                _logger.info('user_id============ %s', user_id)


                if user_id:
                    sales_person = user_id
                else:
                    in_user_id = self.env['res.users'].search([('name', '=', 'Administrator' or '')])
                    _logger.info('in_user_id======else====== %s', in_user_id)
                    sales_person = in_user_id

                if crm_id:
                    vals = {'user_id': sales_person.id or '',
                            'team_id': sales_team.id or '',
                            }

                    lead_id = crm_id.write(vals)
                    _logger.info('lead_id===update======== %s', lead_id)
                    self._cr.commit()



    @api.multi
    def import_desc_comment(self):
        import_data_obj = self.env['crm.lead']
        # csv_datas = self.import_data
        # fileobj = TemporaryFile('w+')
        # fileobj.write(base64.decodestring(csv_datas))
        # fileobj.seek(0)
        fileobj = open('/opt/comment_data_desc.csv')
        str_csv_data = fileobj.read()
        list = csv.reader(StringIO.StringIO(str_csv_data), delimiter='|')

        rownum = 0
        faulty = []
        for row in list:
            if row == '':
                continue
            if rownum == 0:
                rownum += 1
            else:
                try:
                    if len(row) < 2:
                        raise UserError(_('Len less than 2'))
                    if not row[0]:
                        continue
                    _logger.info('email============ %s',row[0])
                    crm_id = self.env['crm.lead'].search([('email_from', '=', str(row[0]).strip(' '))])
                    _logger.info('crm_id============ %s', crm_id)

                    if crm_id:
                        vals = {
                                'description': str(row[1]).strip(' ') or '',
                                'comment': str(row[2]).strip(' ') or '',
                        }

                        lead_id = crm_id.write(vals)
                        _logger.info('lead_id===update======== %s', lead_id)
                        self._cr.commit()
                    else:
                        faulty.append(row[0])
                    rownum += 1
                except Exception,e:
                    # faulty.append(row[0])
                    _logger.info('exception  in row %s error %s',rownum,e)
                    continue
        _logger.info('faulty=========== %s', faulty)
        return True