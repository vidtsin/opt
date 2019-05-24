from pygments.lexer import _inherit
from datetime import datetime
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
import requests
import json
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp



class Myallocator_property(models.Model):
    _name='myallocator.property'
    _inherits = {'res.partner': 'last_website_so_id'}
    
    name = fields.Char('Name')
    


#Activity
class Myallocator_activity_test(models.Model):
    _name='myallocator.activity.test'
    
    
    capacity = fields.Integer('Capacity')
    product_id = fields.Many2one('product.template',string='Rooms')
    prod_id = fields.Many2one('product.product',string='Variant')
    property_id = fields.Many2one('myallocator.property',string='Property')
    price = fields.Float('Price')
    
    
    
    
class Product_template(models.Model):
    _inherit='product.template'

    
#    For Activity
    is_activities = fields.Boolean('Is Activities')
    product_activity_ids = fields.One2many('myallocator.activity.test','product_id',string='Rooms')



    
class SaleOrder(models.Model):
    _inherit ='sale.order'
    
    
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    property_id = fields.Many2one('myallocator.property',string='Property')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Check-In'),
        ('check_out', 'Check-Out'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    

    
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    current_date = fields.Date('Current Date', default=datetime.now().date())
    activities = fields.Selection([('morning','Morning'),('midday','Midday'),('sunset','Sunset')],'Activities')
    res_partner_id = fields.Many2one('res.partner',string='Partner')
    is_available = fields.Boolean('Is Available')
    is_room = fields.Boolean('Is Room')
    is_activities = fields.Boolean('Is Activities')
    is_transport = fields.Boolean('Is Transport')
    property_id = fields.Many2one('myallocator.property',string='Property')
    
    
    @api.multi
    def get_start_date(self):
        sale_obj = self.env['sale.order']
        sale_id = sale_obj.search([('id','=', self.order_id.id)])
        if sale_id:
            if self.order_id == sale_id and self.is_room == True:
                sale_id.write({'start_date': self.start_date, 'end_date': self.end_date})
 
    
#    Create function - Checking available rooms and activities
    @api.model
    def create(self, values):
        onchange_fields = ['name', 'price_unit', 'product_uom', 'tax_id']
        if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
            line = self.new(values)
            line.product_id_change()
            for field in onchange_fields:
                if field not in values:
                    values[field] = line._fields[field].convert_to_write(line[field], line)
                    
        line = super(SaleOrderLine, self).create(values)
        
        line.get_start_date()
        

                            
#        For Activities - Morning
        line_id_morning = self.search([('current_date','=', values.get('current_date')),('activities','=', 'morning'),('product_id','=', values.get('product_id')),
                 ('order_id','!=', ''),('state','!=', 'cancel'),('property_id','=', line.property_id.id) ])
        
        test_list = []
        for test in line_id_morning:
            if test.current_date == values.get('current_date'):
                test_list.append(test.id)
        line_id_morning = []
        for test in sorted(test_list):
            act_morn = self.browse(test)
            line_id_morning.append(act_morn)
        
        morning_count = 0
        m_count = 0
        for li in line_id_morning:
            print"------------li------------",li
            if li.order_id.state != 'cancel':
                if li.product_id.product_activity_ids:
                    for activity in li.product_id.product_activity_ids:
                        if activity.property_id == li.property_id:
                
                            morning_count = float(morning_count) + li.product_uom_qty
                            capacity = activity.capacity
                            if morning_count <= capacity:
                                print"-----------morning_count------------",morning_count
                            else:
                                print"-----------morning_count-----2-------",morning_count
                                m_count = morning_count - li.product_uom_qty
                                m_count = activity.capacity - m_count
                                raise UserError(_("Activities with capacity %s is remaining")% m_count)


#        For Activities - Midday            
        line_id_midday = self.search([('current_date','=', values.get('current_date')),('activities','=', 'midday'),('product_id','=', values.get('product_id')),
                 ('order_id','!=', ''),('state','!=', 'cancel') ,('property_id','=', line.property_id.id)])
        
        test_list = []
        for test in line_id_midday:
            if test.current_date == values.get('current_date'):
                test_list.append(test.id)
        print"------------test_list------------",test_list
        print"------------test_list------------",sorted(test_list)
        line_id_midday = []
        for test in sorted(test_list):
            act_mid = self.browse(test)
            line_id_midday.append(act_mid)
        print"------------line_id_midday------------",line_id_midday
        
        morning_count = 0
        m_count = 0
        for li in line_id_midday:
            print"------------li------------",li
            if li.order_id.state != 'cancel':
                if li.product_id.product_activity_ids:
                    for activity in li.product_id.product_activity_ids:
                        if activity.property_id == li.property_id:
                
                            morning_count = float(morning_count) + li.product_uom_qty
                            capacity = activity.capacity
                            if morning_count <= capacity:
                                print"-----------morning_count------------",morning_count
                            else:
                                print"-----------morning_count-----2-------",morning_count
                                m_count = morning_count - li.product_uom_qty
                                m_count = activity.capacity - m_count
                                raise UserError(_("Activities with capacity %s is remaining")% m_count)
        
#        For Activities - Sunset        
        line_id_sunset = self.search([('current_date','=', values.get('current_date')),('activities','=', 'sunset'),('product_id','=', values.get('product_id')),
                 ('order_id','!=', ''),('state','!=', 'cancel'),('property_id','=', line.property_id.id) ])
        print"------------line_id_sunset------------",line_id_sunset
        
        test_list = []
        for test in line_id_sunset:
            if test.current_date == values.get('current_date'):
                test_list.append(test.id)
        print"------------test_list------------",test_list
        print"------------test_list------------",sorted(test_list)
        line_id_sunset = []
        for test in sorted(test_list):
            act_set = self.browse(test)
            line_id_sunset.append(act_set)
        print"------------line_id_sunset------------",line_id_sunset
        
        morning_count = 0
        m_count = 0
        for li in line_id_sunset:
            print"------------li------------",li
            if li.order_id.state != 'cancel':
                if li.product_id.product_activity_ids:
                    for activity in li.product_id.product_activity_ids:
                        if activity.property_id == li.property_id:
                
                            morning_count = float(morning_count) + li.product_uom_qty
                            capacity = activity.capacity
                            if morning_count <= capacity:
                                print"-----------morning_count------------",morning_count
                            else:
                                print"-----------morning_count-----2-------",morning_count
                                m_count = morning_count - li.product_uom_qty
                                m_count = activity.capacity - m_count
                                raise UserError(_("Activities with capacity %s is remaining")% m_count)

        
        if line.state == 'sale':
            line._action_procurement_create()
        return line
    
    
#    Write function - Checking available rooms and activities
    @api.multi
    def write(self, values):
        lines = False
        if 'product_uom_qty' in values:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            lines = self.filtered(
                lambda r: r.state == 'sale' and float_compare(r.product_uom_qty, values['product_uom_qty'], precision_digits=precision) == -1)
        result = super(SaleOrderLine, self).write(values)
        
        self.get_start_date()
        

        
#        For Activities - Morning
        line_id_morning = self.search([('current_date','=', self.current_date),('activities','=', 'morning'),('product_id','=', self.product_id.id),
                 ('order_id','!=', ''),('state','!=', 'cancel'),('property_id','=', self.property_id.id) ])
        
        test_list = []
        for test in line_id_morning:
            if test.current_date == self.current_date:
                test_list.append(test.id)
        line_id_morning = []
        for test in sorted(test_list):
            act_morn = self.browse(test)
            line_id_morning.append(act_morn)
        
        morning_count = 0
        m_count = 0
        for li in line_id_morning:
            if li.order_id.state != 'cancel':
                if li.product_id.product_activity_ids:
                    for activity in li.product_id.product_activity_ids:
                        if activity.property_id == li.property_id:
                            morning_count = float(morning_count) + li.product_uom_qty
                            capacity = activity.capacity
                            if morning_count <= capacity:
                                print
                            else:
                                m_count = morning_count - li.product_uom_qty
                                m_count = activity.capacity - m_count
                                raise UserError(_("Activities with capacity %s is remaining")% m_count)
        
#        For Activities - Midday
        line_id_midday = self.search([('current_date','=', self.current_date),('activities','=', 'midday'),('product_id','=', self.product_id.id),
                 ('order_id','!=', ''),('state','!=', 'cancel') ,('property_id','=', self.property_id.id)])
        
        test_list = []
        for test in line_id_midday:
            if test.current_date == self.current_date:
                test_list.append(test.id)
        line_id_midday = []
        for test in sorted(test_list):
            act_mid = self.browse(test)
            line_id_midday.append(act_mid)
        
        morning_count = 0
        m_count = 0
        for li in line_id_midday:
            if li.order_id.state != 'cancel':
                if li.product_id.product_activity_ids:
                    for activity in li.product_id.product_activity_ids:
                        if activity.property_id == li.property_id:
                
                            morning_count = float(morning_count) + li.product_uom_qty
                            capacity = activity.capacity
                            if morning_count <= capacity:
                                print
                            else:
                                m_count = morning_count - li.product_uom_qty
                                m_count = activity.capacity - m_count
                                raise UserError(_("Activities with capacity %s is remaining")% m_count)
        
        
#        For Activities - Sunset
        line_id_sunset = self.search([('current_date','=', self.current_date),('activities','=', 'sunset'),('product_id','=', self.product_id.id),
                 ('order_id','!=', ''),('state','!=', 'cancel'),('property_id','=', self.property_id.id) ])
        
        test_list = []
        for test in line_id_sunset:
            if test.current_date == self.current_date:
                test_list.append(test.id)
        line_id_sunset = []
        for test in sorted(test_list):
            act_set = self.browse(test)
            line_id_sunset.append(act_set)
        
        morning_count = 0
        m_count = 0
        for li in line_id_sunset:
            if li.order_id.state != 'cancel':
                if li.product_id.product_activity_ids:
                    for activity in li.product_id.product_activity_ids:
                        if activity.property_id == li.property_id:
                            morning_count = float(morning_count) + li.product_uom_qty
                            capacity = activity.capacity
                            if morning_count <= capacity:
                                print
                            else:
                                m_count = morning_count - li.product_uom_qty
                                m_count = activity.capacity - m_count
                                raise UserError(_("Activities with capacity %s is remaining")% m_count)
        if lines:
            lines._action_procurement_create()
        return result
    
    
    
#    Room Onchange 
    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.category_id.id != self.product_uom.category_id.id):
            vals['product_uom'] = self.product_id.uom_id

        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id.id,
            quantity=self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )
        
        name = product.name_get()[0][1]
        if product.description_sale:
            name += '\n' + product.description_sale
        vals['name'] = name
        
        self.is_available = self.product_id.is_available
        self.is_room = self.product_id.is_room
        self.is_activities = self.product_id.is_activities
        self.is_transport = self.product_id.is_transport
        
        if self.order_id.property_id:
            self.property_id = self.order_id.property_id.id
        else:
            user_id = self.env['res.users'].search([('id','=', self._uid)])
            self.property_id = user_id.property_id.id
        
        
        if self.is_room:
            for prod in product.product_room_ids:
                if prod.property_id == self.property_id:
                    product.write({'list_price' : prod.price})
        elif self.is_activities:
            for prod in product.product_activity_ids:
                if prod.property_id == self.property_id:
                    product.write({'list_price' : prod.price})
        
        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price(self._get_display_price(product), product.taxes_id, self.tax_id)
        self.update(vals)
        
        title = False
        message = False
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            if product.sale_line_warn == 'block':
                self.product_id = False
            return {'warning': warning}
        
        return {'domain': domain}
    
    