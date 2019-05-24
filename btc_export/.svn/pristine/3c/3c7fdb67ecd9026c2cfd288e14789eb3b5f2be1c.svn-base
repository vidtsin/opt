from odoo import models, fields, api, _
import csv
from odoo.http import request
from tempfile import TemporaryFile
import StringIO
import base64
import logging
_logger = logging.getLogger(__name__)

class wizard_export(models.TransientModel):
    _name = "wizard.lead.pipeline"

    import_data = fields.Binary('Import Data')

    @api.multi
    def action_next3(self):
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
                try:
                    country_code = row[4]
                    country_id = self.env['res.country'].search([('code', '=', country_code)])
                    _logger.info('country_id============ %s', country_id)

                    state_name = row[21]
                    state_id = self.env['res.country.state'].search([('name', '=', state_name)])
                    _logger.info('state_id============ %s', state_id)

                    next_activity_id = self.env['crm.activity'].search([('name', '=', row[11])])
                    _logger.info('next_activity_id============ %s', next_activity_id)

                    sales_team = self.env['crm.team'].search([('name', '=', row[17] or '')])
                    _logger.info('sales_team============ %s', sales_team)

                    stage_id = self.env['crm.stage'].search([('name', '=', row[22] or '')])
                    _logger.info('stage_id============ %s', stage_id)


                    # partner_id = self.env['res.partner'].search([('name', '=', row[3])])
                    # _logger.info('partner_id============ %s', partner_id)


                    user_id = self.env['res.users'].search([('name', '=', row[18] or ''),('email', '=', row[19] or '')])
                    _logger.info('user_id============ %s', user_id)


                    latitude = row[9].strip("'")
                    longitude = row[10].strip("'")

                    vals= {'country_id' : country_id.id or '',
                           'city':row[2] or '',
                           'contact_name': row[3] or '',
                            'partner_name' : row[5] or '',
                           'email_from': row[6],
                           'fax': row[7],
                           'partner_latitude': latitude,
                           'partner_longitude': longitude,
                           'next_activity_id': next_activity_id.id or '',
                           # 'date_action': row[12] or '',
                           'opt_out': row[13] or '',
                           'phone':row[14] or '',
                           'probability':row[15] or '',
                           'referred':row[16] or '',
                           'team_id': sales_team.id or '',
                           'user_id': user_id.id or '',
                           'zip': row[20],
                           'stage_id': stage_id.id or '',
                           'state_id': state_id.id or '',
                           'name': str(row[24]).strip(),
                           'street': row[25] or '',
                           'street2': row[26] or '',
                           'day_open': row[27] or '',
                           'day_close': row[28] or '',
                            'type' : 'opportunity',
                            # 'partner_id' : partner_id.id or '',
                           }

                    print "=====vals=======", vals

                    lead_id = import_data_obj.create(vals)
                    _logger.info('lead_id============ %s', lead_id)

                except Exception,e:
                    _logger.info('error=====exception============ %s', e)







