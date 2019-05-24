
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
import requests
import json

class Product_product(models.Model):
    _inherit='product.product'
    
    room_variant_ids = fields.One2many('myallocator.prod.test','prod_id',string='Rooms')
    
    
    
class Data_record(models.Model):
    _name='data.record'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    property_id = fields.Many2one('myallocator.property',string='Property')
    res_user_id = fields.Many2one('res.users',string='User')
    team_id = fields.Many2one('crm.team',string='Crm')
    
    
class Product_template(models.Model):
    _inherit='product.template'

    is_a_room = fields.Boolean('Is Room ?')
    is_room = fields.Boolean('Is Room')
    is_available = fields.Boolean('Is Available')
    is_activities = fields.Boolean('Is Activities')
    is_transport = fields.Boolean('Is Transport')
    product_room_ids = fields.One2many('myallocator.room.test','product_id',string='Rooms')
    product_activity_ids = fields.One2many('myallocator.activity.test','product_id',string='Rooms')


class Property_list(models.Model):
    _name='property.list'
    
    my_property_id = fields.Many2one('myallocator.property',string='Property')
    res_user_id = fields.Many2one('res.users',string='Users')
    
class Users(models.Model):
    _inherit='res.users'
    
    @api.depends('property_ids')
    def _get_property(self):
        for user in self:
            if user.property_ids:
                if len(user.property_ids) == 1:
                    user.property_id = user.property_ids[0].my_property_id.id
                
    
    property_id = fields.Many2one('myallocator.property',string='Property List', compute='_get_property', store=True)
    property_ids = fields.One2many('property.list','res_user_id',string='Property List')
    
   