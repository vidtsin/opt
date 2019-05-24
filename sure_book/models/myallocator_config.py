from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
import requests
import json
import logging
logger = logging.getLogger(__name__)


class Myallocator_config(models.Model):
    _name='myallocator.config'

    name= fields.Char('Name')
    usertoken = fields.Char('User Token')
    vendor_id = fields.Char('Vendor ID')
    vendorpwd = fields.Char('Vendor Password')
    my_channel_ids = fields.One2many('myallocator.channel','allocator_config_id',string='Channel')


#    Gets all channels from myallocator
    @api.multi
    def create_channel_list(self):
        url = "http://api.myallocator.com/pms/v201408/json/ChannelList"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        payload ={
                    "Auth/VendorId":str(self.vendor_id),
                    "Auth/VendorPassword":str(self.vendorpwd),
                    }
        data_json=json.dumps(payload)
        response = requests.request("POST", url, data=data_json, headers=headers)

        response_data = json.loads(response.text)
        
        if response_data['Success'] == True:
            chan_list = []
            for chan in response_data['Channels']:
                chan_data = response_data['Channels'].get(chan,False)
                
                channel_obj = self.env['myallocator.channel']
                
                vals = {
                    'name' : chan_data.get('name'),
                    'channel_id' : chan,
                    'allocator_config_id' : self.id,
                }
                channels = channel_obj.create(vals)
                
        return True
    
    
    
    
