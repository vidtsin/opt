
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
import requests
import json

class Myallocator_channel(models.Model):
    _name='myallocator.channel'

    channel_id= fields.Char('Channel ID')
    name= fields.Char('Channel')
    currency = fields.Many2one('res.currency',string='Currency')
    status = fields.Selection([('NotSetup','NotSetup'),('HasErrors','HasErrors'),('Pending','Pending')],string='Status')
    is_live = fields.Boolean('isLive')
    is_beta = fields.Boolean('isBeta')
    is_calendar = fields.Boolean('isCalendarBased')
    require_activate = fields.Boolean('Require Activation')
    link= fields.Char('SignUp Link')
    is_login = fields.Boolean('isLockedLogin')
    allocator_config_id = fields.Many2one('myallocator.config',string='My Allocator Config')
    my_property_ids = fields.One2many('myallocator.property','my_channel_id',string='Property')
    
    
#    Gets all channels provided to particular property
 
    @api.multi
    def get_channel_list(self,property_id):
        config = self.env['myallocator.config'].search([])
        channel_obj = self.env['myallocator.channel']

        print "------------------------------yeah",property_id
        url = "http://api.myallocator.com/pms/v201609/json/PropertyChannelList"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        payload = {
          "Auth/UserToken":str(config.usertoken),
          "Auth/PropertyId":str(property_id.property_id),
          "Auth/VendorId":str(config.vendor_id),
          "Auth/VendorPassword":str(config.vendorpwd),
          }
        data_json = json.dumps(payload)
        print "-------------------payload---------------------", payload

        response = requests.request("POST", url, data=data_json, headers=headers)

        print(response.text)
        response_data = json.loads(response.text)

        print "---------------response_data-------------",response_data
        print "---------------response_data--------------",response_data['Properties']
        print "-------------response_data--------Success-----",response_data['Success']
        if response_data['Success'] == True:
            chan_data = response_data['Properties']
            print "---------------------",chan_data
            print "---------------------",chan_data[0].get('Channels')
            ch_li = []
            for ch_list in chan_data[0].get('Channels'):
                channel_name = ch_list
                print "---------channel_name------------",channel_name
                chk_status = chan_data[0].get('Channels').get(ch_list,False)
                status = chan_data[0].get('Channels').get(ch_list,False)['status']
                print "---------status------------",status
                currency = chan_data[0].get('Channels').get(ch_list,False)['currency']
                
                if status  != 'NotSetup':
                    channel_id = channel_obj.search([('channel_id','=',ch_list)])
                    currency_id = self.env['res.currency'].search([('name','=',currency)])

                    channel_id.write({'status': status, 'currency' : currency_id.id})
                    ch_li.append(channel_id)
        return ch_li



