import base64
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
import requests
import json


class ProductImage(models.Model):
    _inherit = 'product.image'

    name = fields.Char('Name')
    image = fields.Binary('Image', attachment=True)
    product_tmpl_id = fields.Many2one('product.template', 'Related Product', copy=True)
    property_tmpl_id = fields.Many2one('myallocator.property', 'Related Property', copy=True)




class Myallocator_property(models.Model):
    _name='myallocator.property'
    _inherits = {'res.partner': 'last_website_so_id'}

    website_size_x = fields.Integer('Size X', default=1)
    website_size_y = fields.Integer('Size Y', default=1)
    website_style_ids = fields.Many2many('product.style', string='Styles')
    website_sequence = fields.Integer('Website Sequence', help="Determine the display order in the Website E-commerce",
                                      default=lambda self: self._default_website_sequence())
    product_image_ids = fields.One2many('product.image', 'property_tmpl_id', string='Images')
    
    is_property = fields.Boolean('Is Property',default=True)
    image = fields.Binary("Image", attachment=True,
        help="This field holds the image used as avatar for this contact, limited to 1024x1024px",)
    image_medium = fields.Binary("Medium-sized image", attachment=True,
        help="Medium-sized image of this contact. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved. "\
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
        help="Small-sized image of this contact. It is automatically "\
             "resized as a 64x64px image, with aspect ratio preserved. "\
             "Use this field anywhere a small image is required.")
    breakfast = fields.Selection([('IN','Included in bed/room price'),('EX','Exclusive(extra charge)')],string='Breakfast')
    currency = fields.Many2one('res.currency',string='Currency')
    is_property_created = fields.Boolean('Property Created')
    property_id = fields.Char('Property ID')
    room_ids = fields.One2many('myallocator.room.test','property_id',string='Rooms')
    my_test_ids = fields.One2many('myallocator.test','my_property_id',string='Channel')
    my_channel_id = fields.Many2one('myallocator.channel',string='Channel List')
    
    user_ids = fields.One2many('property.list','my_property_id',string='User List')
    
    
    def _default_website_sequence(self):
        self._cr.execute("SELECT MIN(website_sequence) FROM %s" % self._table)
        min_sequence = self._cr.fetchone()[0]
        return min_sequence and min_sequence - 1 or 10
    
    @api.multi
    def property_data(self,property):
        details = {}

        details['country'] = str(property.country_id.code) or ''
        details['name'] = str(property.name) or ''
        details['currency'] = str(property.currency.name) or ''

        if not property.city:
            details['city'] = ''
        else:
            details['city'] = str(property.city)
        if not property.zip:
            details['zip'] = ''
        else:
            details['zip'] = str(property.zip)
        if not property.email:
            details['email'] = ''
        else:
            details['email'] = str(property.email)
        if not property.breakfast:
            details['breakfast'] = ''
        else:
            details['breakfast'] = str(property.breakfast)
        if not property.state_id:
            details['state'] = ''
        else:
            details['state'] = str(property.state_id.name)
        if not property.street:
            details['street'] = ''
        else:
            details['street'] = str(property.street)
        return details
        
        
#    Creates property in myallocator
    @api.multi
    def create_property(self,property):
        property_data = self.property_data(property)
        room_config = self.env['product.template']
        config = self.env['myallocator.config'].search([])
        url = "https://api.myallocator.com/pms/v201408/json/PropertyCreate"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        payload = {"Auth/UserToken":str(config.usertoken),
          "Auth/VendorId":str(config.vendor_id),
          "Auth/VendorPassword":str(config.vendorpwd),
          "PropertyName":property_data['name'],
          "Currency":property_data['currency'],
          "Street":property_data['street'],
          "City":property_data['city'],
          "PostCode":property_data['zip'],
          "State":property_data['state'],
          "Country":property_data['country'],
          "Breakfast":property_data['breakfast'],
          "BookingAdjust":"1",
          "BookingAdjustCancellation":"1",
          "BookingAdjustModification":"1",
          "BookingDownload":"1",
          "EmailDefault":property_data['email'],
          "EmailChannelBooking":property_data['email'],
          "EmailBookNow":property_data['email']}
        data_json = json.dumps(payload)

        response = requests.request("POST", url, data=data_json, headers=headers)
        print(response.text)
        response_data = json.loads(response.text)
        if response_data['Success'] == True:
            property.write({'property_id':str(response_data['PropertyId']),
                            'is_property_created':str(response_data['PropertyId'])
                            })
        return True


class Myallocator_room_test(models.Model):
    _name='myallocator.room.test'
    
    
    room_id = fields.Char('Room ID')
    unit = fields.Float('No. of Rooms')
    gender = fields.Selection([('MA','Males'),('FE','Females'),('MI','Mixed')],string='Gender')
    private_room = fields.Selection([('false','Dormitories'),('true','Private Room')],string='Dormitory')
    is_dorm = fields.Boolean(string='Is Dormitory')
    occupancy = fields.Integer('Occupancy')
    product_id = fields.Many2one('product.template',string='Rooms')
    prod_id = fields.Many2one('product.product',string='Variant')
    property_id = fields.Many2one('myallocator.property',string='Property')
    price = fields.Float('Price')
    
    
    @api.multi
    @api.onchange('product_id')
    def room_change(self):
        self.is_dorm = self.product_id.is_dorm
        self.occupancy = self.product_id.capacity
        if self.product_id.is_dorm == True:
            self.private_room = 'false'
        else:
            self.private_room = 'true'
            
        
#    @api.multi
#    @api.onchange('private_room')
#    def dorm_change(self):
#        if self.private_room == 'false':
#            print"---------is dorm-------------"
#            self.is_dorm = True
#        else:
#            print"---------is not dorm-------------"
#            self.is_dorm = False
    
    
    @api.multi
    def room_data(self,property_id):
        room_list = []
        for room in property_id.room_ids:
            if not room.room_id:
        
                vals = {
                    "PMSRoomId":str(room.id),
                    "Label":str(room.product_id.name),
                    "Units":str(room.unit),
                    "Occupancy":str(room.occupancy),
                    "PrivateRoom":str(room.private_room),
                    "Gender":str(room.gender),
                }
                room_list.append(vals)
                
        
        return room_list

#    Creates Room in myallocator
    @api.multi
    def create_room(self,property_id):
        room_data = self.room_data(property_id)
        room_obj = self.env['myallocator.room.test']
        config = self.env['myallocator.config'].search([])
        url = "http://api.myallocator.com/pms/v201408/json/RoomCreate"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        payload = {
          "Auth/UserToken":str(config.usertoken),
          "Auth/PropertyId":str(property_id.property_id),
          "Auth/VendorId":str(config.vendor_id),
          "Auth/VendorPassword":str(config.vendorpwd),
          "ValidateOnly":0,
          "AuthorizeBilling":0,
          "Rooms" : room_data
        }
        data_json = json.dumps(payload)
        response = requests.request("POST", url, data=data_json, headers=headers)

        print(response.text)
        response_data = json.loads(response.text)
        if response_data['Success'] == True:
            li_room = []
            for ro_id in response_data['Rooms']:
                room_data_id = self.search([('id','=',ro_id['PMSRoomId'])])
                room_data_id.write({'room_id' : ro_id['RoomId']})
        return True
    
    
    
    
    
class Myallocator_prod_test(models.Model):
    _name='myallocator.prod.test'
    
    
    room_id = fields.Char('Room ID')
    unit = fields.Float('No. of Rooms')
    gender = fields.Selection([('MA','Males'),('FE','Females'),('MI','Mixed')],string='Gender')
    private_room = fields.Selection([('false','Dormitories'),('true','Private Room')],string='Dormitory')
    is_dorm = fields.Boolean(string='Is Dormitory')
    occupancy = fields.Integer('Occupancy')
    product_id = fields.Many2one('product.template',string='Rooms')
    prod_id = fields.Many2one('product.product',string='Variant')
    property_id = fields.Many2one('myallocator.property',string='Property')
    price = fields.Float('Price')



class Myallocator_activity_test(models.Model):
    _name='myallocator.activity.test'
    
    
    capacity = fields.Integer('Capacity')
    product_id = fields.Many2one('product.template',string='Rooms')
    prod_id = fields.Many2one('product.product',string='Variant')
    property_id = fields.Many2one('myallocator.property',string='Property')
    price = fields.Float('Price')





class Myallocator_test(models.Model):
    _name='myallocator.test'

    my_channel_id = fields.Many2one('myallocator.channel',string='Channel List')
    my_property_id = fields.Many2one('myallocator.property',string='Property')
    currency = fields.Many2one('res.currency',string='Currency')
    status = fields.Selection([('NotSetup','NotSetup'),('HasErrors','HasErrors'),('Pending','Pending')],string='Status')
    
    
    @api.multi
    def create_test(self,property_id):
        channel_obj = self.env['myallocator.channel']
        channel_data = channel_obj.get_channel_list(property_id)
        for test in channel_data:
            vals = {
            'my_channel_id' : test.id,
            'currency' : test.currency.id,
            'status' : test.status,
            'my_property_id' : property_id.id
            }
            test_id = self.create(vals)
        return True
 