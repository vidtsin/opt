# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import odoo.addons.decimal_precision as dp
import pdb
from openerp.exceptions import except_orm, Warning, RedirectWarning
import json
import urllib2
import requests
#from odoo.addons.sale_start_end_dates.models.sale import start_date,end_date

class booking(models.Model):
    _inherit = 'product.product'

    status = fields.Selection([('Dirty', 'Dirty'), ('Cleanup', 'Clean Up'), ('Ready', 'Ready')],
                            string="Status")

    def default_user_id(self):
       return self.env.context.get('default_user_id', self.env.uid)

    @api.constrains('order_id')
    def get_partner_id(self):
       if self.order_id.partner_id:
          self.customer = self.order_id.partner_id.name
       return

    start_date = fields.Date(default=fields.Date.today, required="True")
    end_date = fields.Datetime(default=fields.Date.today, required="True")
    customer = fields.Char("")

class SchedulerBooking(models.Model):

    _name = 'scheduler.booking'

    @api.model
    def get_products(self):
      vals = []
      rec = []
      room_type = self.env.context['capacity']
      product_ids = self.env['product.template'].search([('is_a_room', '=', True)])
      dorm_info_ids = self.env['product.template'].search([('is_dorm', '=', True)])
      dorm_ids = self.env['product.product'].search([('is_dorm', '=', True)])
      if product_ids:
          for record in product_ids:
              if room_type == 'NULL' or room_type == 0:
                  vals.append({
                          'id': str(record.id),
                          'name': record.name,
                          'capacity': str(record.capacity),
                          'status': record.status,
                          # 'rec': rec,
                      })
              elif room_type == 1 and record.capacity == 1:
                   vals.append({
                          'id': str(record.id),
                          'name': record.name,
                          'capacity': str(record.capacity),
                          'status': record.status,
                          # 'rec': rec,
                      })
              elif room_type == 2 and record.capacity == 2:
                      vals.append({
                          'id': str(record.id),
                          'name': record.name,
                          'capacity': str(record.capacity),
                          'status': record.status,
                          # 'rec': rec,
                      })
              elif room_type == 4 and record.capacity >= 4:
                      vals.append({
                          'id': str(record.id),
                          'name': record.name,
                          'capacity': str(record.capacity),
                          'status': record.status,
                          # 'rec': rec,
                      })

      if dorm_ids:
          for record in dorm_info_ids:
              dorm_info = self.env['product.product'].search(
                  [('is_dorm', '=', True), ('product_tmpl_id', '=', record.id)])
              count = 0
              for dorm in dorm_info:
                  rec.append({
                      'id': str(dorm.id),
                      'name': dorm.attribute_value_ids.name,
                      'capacity': str(1),
                      'status': dorm.status,
                  })
                  tmpl_id = dorm.product_tmpl_id.id
                  count = count + 1
              vals.append({
                  'id': 'D' + str(tmpl_id),
                  'name': record.name,
                  'capacity': str(count),
                  'status': record.status,
                  'children': rec,
              })
              rec = []
      if not product_ids and not dorm_info_ids:
          raise UserError(_('No Room or Dorms in Product.'))
          return
      print"------------vals------------",vals
      return vals


    @api.model
    def fetch_order_line(self):
      rec = []
      start_date = self.env.context['start_date']
      end_date = self.env.context['end_date']
      order_ids = self.env['sale.order.line'].search([('start_date', '>=', start_date),
                                                      ('end_date', '<=', end_date)
                                                      ])
      if order_ids:
          for record in order_ids:
              rec.append({
                   'id': str(record.id),
                   'text': record.order_partner_id.name,
                   'resource': str(record.product_id.id),
                   'start': record.start_date,
                   'end': record.end_date,
                   'status': record.room_booking_status,
                   # 'bookingid': str(record.room_booking_id.id),
                   'paid': str(0),
                   'tags': {'bookingid': str(record.room_booking_id.id)}
              })
          return rec

class BookingInfo(models.Model):
  _name = 'booking.info'
  _rec_name = 'product_id'
  
  
  name = fields.Char("Product Name")
  customer = fields.Many2one('res.partner', string="Customer")
  start_date = fields.Datetime(string='Start Date')
  end_date = fields.Datetime(string='End Date')
  product_id = fields.Many2one('product.product', string="Room")
  button_flag = fields.Integer('Button Flag',default = 1)
  sale_reference = fields.Many2one('sale.order', 'Sale Reference')
  room_booking_status = fields.Selection([('new', 'New'), ('checkin', 'Check in'), ('checkout', 'Check Out')], default='new', string="Status")
  booking_lines = fields.One2many('booking.info.lines','booking_info_id', string="Booking Info Lines")
  is_multiple = fields.Boolean(string="Multiple Booking")
  multiple_booking_ids = fields.Many2many('product.product', 'room_booking_rel1', 'pid', 'bid', 'Rooms')
  amount_total = fields.Float(string="Total Price", compute="compute_room_price", store=True)
  payment_flag = fields.Integer('Payment Flag',default = 1)
  sale_order_line = fields.One2many('sale.order.line','room_booking_id','Rooms Info',related = 'sale_reference.order_line')
  booking_info_ids = fields.One2many('check.room.line','booking_info_id',string='Check In form')
  pos_order_ids = fields.One2many('pos.order','pos_order_id',string='POS Orders')
  
  @api.one
  @api.depends('sale_order_line.price_total')
  def compute_room_price(self):
      for item in self.sale_order_line:
	self.amount_total += item.price_total
     


  def _get_new_sale_line(self, product_id, start_date, end_date, room_booking_id,is_room,room_booking_status):
      res = {
          'product_id': product_id,
          'room_booking_status': room_booking_status,
          'start_date': start_date,
          'end_date': end_date,
          'is_room': is_room,
          'room_booking_id': room_booking_id,

      }
      return res

  def _get_order_lines(self, order):
      res = []
      # count = order['count']
      for rec in order:
          product_id = rec['product_id']
          room_booking_id = self.id
          room_booking_status=self.room_booking_status
          start_date = rec['start_date']
          end_date = rec['end_date']
          is_room = True
          s_date = start_date.replace("T", " ")
          e_date = end_date.replace("T", " ")
          res.append(
              (0, 0, self._get_new_sale_line(product_id, s_date, e_date, room_booking_id,is_room,room_booking_status))
          )
      return res

  #   In case of  Multiple Booking
  def multiple_booking(self, values, mult):
      rec = []
      flag = 0
      self.button_flag = 2
      partner_id = values['partner_id']
      sale_mult_vals = {
          'partner_id': partner_id,
          'room_booking_id': self.id,
          # 'date_order': date_order,
          # 'company_id': self.company_id.id,
          'order_line': self._get_order_lines(mult)
      }
      for rec in mult:
          sale_order_vals = self.env['sale.order.line'].search([
                                                                ('product_id', '=', rec['product_id'])
                                                                ])
          if sale_order_vals:
              for record in sale_order_vals:
		  
                  if (rec['start_date'] > record.start_date) and (rec['start_date'] < record.end_date)\
                          or (rec['end_date'] > record.start_date) and (rec['end_date'] < record.end_date):
                       flag = 1
                       raise_product = rec['product_id']
                       room = self.env['product.product'].browse(raise_product).name
      if flag == 1:
          raise UserError(_('%s Already Booked for this date !! Select other Room.')%(room))
      else:
              sale = self.env['sale.order'].create(sale_mult_vals)
              self.sale_reference = sale.id
              self.amount_total = sale.amount_total
      return {'type': 'ir.actions.act_window_close'}


  def insert_sale_order(self):
	mult = []
	if self.is_multiple:
	    s_date = self.start_date
	    e_date = self.end_date
	    for record in self:
		values = {
		    'partner_id': record.customer.id,

		}
	    for re in self.multiple_booking_ids:
	      mult.append({'product_id': re.id,
			    'start_date': s_date,
			      'end_date': e_date},
			    )
	    self.multiple_booking(values, mult)

	else:

	    for record in self:
		vals = {
		'partner_id': record.customer.id,

		}
		order = [
		    {'product_id': record.product_id.id,
		    'start_date': record.start_date,
		    'end_date': record.end_date,
		    }
		]
	    sale_id  = self.sale_order_booking(vals, order)
            print"---------sale_id----------",sale_id
        
        print"--------self.sale_order_line--------",self.sale_order_line
        
#          -------Done by Planet-Odoo------Check-In Form------
        for order in self.sale_order_line:
            print"---------order----------",order
            product  = order.product_id
            if product.is_a_room and product.capacity:
                cnt = order.product_id.capacity
                count = 1
                while (count <= cnt):

                    vals = {
                        'product_id' : order.product_id.id,
                        'booking_info_id' : self.id,
                    }
                    
                    room_line_id = self.env['check.room.line'].create(vals)
                    print"---------room_line_id----------",room_line_id
                    count = count + 1
            if product.is_dorm:
                vals = {
                        'product_id' : order.product_id.id,
                        'booking_info_id' : self.id,
                    }
                room_line_id = self.env['check.room.line'].create(vals)
                print"---------room_line_id----------",room_line_id
#          -------Done by Planet-Odoo------------
                
	
  @api.one
  def sale_order_booking(self, vals, order):
      self.button_flag = 2

      partner_id = vals['partner_id']
      sale_vals = {
          'partner_id': partner_id,
          'room_booking_id': self.id,
          # 'date_order': date_order,
          # 'company_id': self.company_id.id,
          'order_line' : self._get_order_lines(order)
      }
      for rec in order:
	
        sale_order_vals = self.env['sale.order.line'].search([('start_date', '>=', rec['start_date']),
                                                            ('start_date', '<=', rec['end_date']),
                                                            ('end_date', '>=', rec['start_date']),
                                                            ('end_date', '<=', rec['end_date']),
                                                            ('product_id', '=', rec['product_id'])],)
      if sale_order_vals:
	  
          raise UserError(_('%s Already Booked for this date !! Select other Room.') % (rec['product_id']))

      else:
          sale = self.env['sale.order'].create(sale_vals)
          for order in sale.order_line:
              order.write({ 'res_partner_id' : order.order_id.partner_id.id,
              })
          self.sale_reference = sale.id
          self.amount_total = sale.amount_total

  # For Spliting Booking
  @api.model
  def update_sale_order_line(self):
      #pdb.set_trace()
      sale_order_id = self.env.context['sale_order_id']
      booking_id = self.env.context['booking_id']
      new_start = self.env.context['new_start']
      new_end = self.env.context['new_end']
      new_room = self.env.context['new_room']
      book_id = int(booking_id)
      room_id = int(new_room)
      room_book = self.env['booking.info'].search([('id', '=', book_id)])
      order_line_info = self.env['sale.order.line'].search([('id', '=', sale_order_id)])
      date_1 = datetime.strptime(new_start, "%Y-%m-%d %H:%M:%S")
      new_end_date = date_1
      # + timedelta(days=-1)
      if order_line_info.room_booking_status == 'checkout':
          raise UserError(_('Room has been Checked Out'))
          return
      elif new_start <= order_line_info.start_date and order_line_info.room_booking_status != 'new':
          raise UserError(_("Backward Movement Is Not Possible after booking is Confirmed!!!!"))
          return
      elif (new_start > order_line_info.start_date and order_line_info.room_booking_status != 'new') and order_line_info.product_id.id == room_id:
          raise UserError(_("Forward Movement Is Not Possible after booking is Confirmed!!!!!!!!"))
          return

      else:
        if room_id != room_book.product_id.id and order_line_info.room_booking_status == 'checkin':
	   
            booking_info = self.env['booking.info'].create({
                'name': room_book.name,
                'customer': room_book.customer.id,
                'start_date': new_start,
                'end_date': order_line_info.end_date,
                'product_id': room_id,
                'button_flag': 2,
                'sale_reference': room_book.sale_reference.id,
                'room_booking_status': 'checkin',
            })
	    
            order_line = room_book.env['sale.order.line'].create({
                'order_id': booking_info.sale_reference.id,
                'product_id': booking_info.product_id.id,
                'start_date': booking_info.start_date,
                'end_date': booking_info.end_date,
                'room_booking_status': booking_info.room_booking_status,
                'room_booking_id': booking_info.id,
            })
	    

            order_line_info.room_booking_status = 'checkout'
            order_line_info.end_date = new_end_date
            room_book.end_date = new_end_date
            room_book.payment_flag = 2
            prod_id = order_line_info.product_id
            if order_line_info.room_booking_status == 'checkout':
                product_info = self.env['product.template'].search([('id', '=', prod_id.id)])
                if product_info:
                    product_info.write({'status': 'Dirty'})
        else:
            room_book.write({'start_date': new_start, 'end_date': new_end, 'product_id': room_id})
            order_line_info.write({'start_date': new_start, 'end_date': new_end, 'product_id': room_id})
      return True



  def update_status(self):
    order_line_info = self.env['sale.order.line'].search([('room_booking_id', '=', self.id)])
    booking_line_info = self.env['booking.info'].search([('id', '=', self.id)])

    if order_line_info:
        order_line_info.write({'room_booking_status': self.room_booking_status})

    if booking_line_info:
        booking_line_info.write({'room_booking_status': self.room_booking_status})

    return{'type': 'ir.actions.act_window_close'}
    
  @api.multi
  def unlink(self):
    return super(BookingInfo, self).unlink()

  @api.model
  def unlink_booking(self):
    booking_id = self.env.context['booking_id']
    sale_order_line_id = self.env.context['sale_order_line_id']
    order_line_info = self.env['sale.order.line'].search([('id', '=', sale_order_line_id)])
    if sale_order_line_id:
      for rec in order_line_info:
	chk_order_id = self.env['sale.order.line'].search([('order_id', '=', rec.order_id.id)])
	if len(chk_order_id) <= 1:
	    self.env['booking.info'].search([('id', '=', booking_id)]).unlink()
	    self.env['sale.order'].search([('id', '=', rec.order_id.id)]).unlink()
	    
	if len(chk_order_id) > 1:
	    self.env.cr.execute('''delete from room_booking_rel1 where bid =%s ''',((order_line_info.product_id.id),))
	    self.env['sale.order.line'].search([('id', '=', sale_order_line_id)]).unlink()
	    

  # For Extending Booking
  @api.model
  def extend_booking(self):
      sale_order_line_id = int(self.env.context['sale_order_line_id'])
      booking_id = int(self.env.context['booking_id'])
      new_start_date = self.env.context['new_start_date']
      new_end_date = self.env.context['new_end_date']
      flag = 0
      sale_update_info = self.env['sale.order.line'].browse(sale_order_line_id)
      booking_update_info = self.env['booking.info'].browse(booking_id)
      if new_start_date < sale_update_info.start_date and sale_update_info.room_booking_status != 'new':
          raise UserError(_('Back Extension of Room is not possible after Confirmed the Booking'))

      elif new_start_date > sale_update_info.start_date and sale_update_info.room_booking_status != 'new':
          raise UserError(_('Contraction of Room is not possible after Confirmed the Booking'))

      elif new_end_date > sale_update_info.end_date and sale_update_info.room_booking_status == 'checkout':
          raise UserError(_('Extension of Room is not possible after Check Out'))

      elif new_end_date < sale_update_info.end_date and sale_update_info.room_booking_status == 'checkout':
          raise UserError(_('Contraction of Room is not possible after Confirmed the Booking'))
	
      elif new_start_date < datetime.now().strftime("%Y-%m-%d %H:%M:%S") and sale_update_info.room_booking_status != 'new':
          raise UserError(_("You can't able to extend room for Past Date"))

      for rec in sale_update_info:
          room_info = self.env['sale.order.line'].search([('product_id', '=', rec.product_id.id)])
          for order in room_info:
              if order.id != sale_order_line_id:
                  if order.start_date > new_start_date and order.start_date < new_end_date:
                      flag = 1
                  elif order.end_date > new_start_date and order.end_date < new_end_date:
                      flag = 1
      if flag == 0:
          if booking_id:
              booking_update_info.write({'start_date': new_start_date, 'end_date': new_end_date})
          if sale_order_line_id:
              sale_update_info.write({'start_date': new_start_date, 'end_date': new_end_date})
      else:
          raise UserError(_('Booking is Not Possible'))
      return True
  def create_booking_lines(self):
    if self.is_multiple == True:
      for rooms in self.multiple_booking_ids:
        room = self.env['booking.info.lines'].create({
                                                      'product_id': rooms.id,
                                                     })
  def do_checkin(self):
#          -------Done by Planet-Odoo-----Add customer to room-------
      if self.booking_info_ids:
        for book_line in self.booking_info_ids:
            if book_line.partner_id.id == False:
                raise UserError(_('Please fill the Check-In Form'))
            
        line_ids = self.sale_order_line
        for line in line_ids:
            book_line_id = self.env['check.room.line'].search([('product_id', '=', line.product_id.id), 
              ('booking_info_id', '=', self.id)])
            print"---------book_line_id----------",book_line_id
            list = []
            for book in book_line_id:
                print"--------list--------",list
                list.append(book.partner_id.id)
            print"--------list--------",list
            line.write({'partner_ids' : [(6, 0, list)]})
            print"--------list--------",line.partner_ids
#          -------Done by Planet-Odoo------------    

            
      self.write({'room_booking_status': 'checkin'})
      order_line = self.env['sale.order'].search([('room_booking_id', '=', self.id)])
      order_line_info = self.env['sale.order.line'].search([('room_booking_id', '=', self.id)])
      if order_line_info:
          order_line_info.write({'room_booking_status': 'checkin'})

      order_line.sale_check_in()

  def do_checkout(self):
      self.write({'room_booking_status': 'checkout'})
      order_line = self.env['sale.order'].search([('room_booking_id', '=', self.id)])
      order_line_info = self.env['sale.order.line'].search([('room_booking_id', '=', self.id)])
      if order_line_info:
          order_line_info.write({'room_booking_status': 'checkout'})

#      order_line.order_process_now()
      order_line.check_out_process()

  @api.model
  def do_make_payment(self):
      # if self.room_booking_status == 'checkout':
      #     order_line = self.env['sale.order'].search([('room_booking_id', '=', self.id)])
      #     order_line.make_payment()

      view_ref = self.env['ir.model.data'].get_object_reference('account', 'view_account_payment_form')
      view_id = view_ref[1] if view_ref else False

      cxt = {}
      # view_id = self.env.ref('account.view_account_payment_form').id
      cxt.update({'payment_type': "inbound", 'default_partner_id': self.customer.id})
      return {
          'name': 'Make Payment',
          'view_type': 'form',
          'view_mode': 'form',
          'res_model': 'account.payment',
          'type': 'ir.actions.act_window',
          # 'res_id':self.id,
          'view_id': view_id,
          'target': 'new',
          # 'context': cxt
      }


class Product(models.Model):
  """docstring for Product"""
  _inherit = 'product.template'

  booking_info = fields.One2many('booking.info', 'product_id', 'Bookings')
  capacity = fields.Integer(string="Capacity")
  status = fields.Selection([('Dirty', 'Dirty'), ('Cleanup', 'Clean Up'), ('Ready', 'Ready')],
                            string="Status")
  is_dorm = fields.Boolean(string="Is a Dorm")
  room_acc = fields.Boolean(string="Select Accomodation") #value will be passed through context in action(Setting Internal Category)
  # For Setting available_in_pos value to false
  @api.constrains('available_in_pos')
  def change_available_in_pos(self):
	if self.available_in_pos:
		self.available_in_pos = False
  # Setting Internal Category to Accomodation 			
  @api.onchange('room_acc')
  def onchange_room_acc(self):
	if self.room_acc:
 		product_cat_obj = self.env['product.category'].search([('name', '=', "Accomodation")])
		self.categ_id = product_cat_obj
		

  @api.constrains('capacity')
  def onchnge_create_delete_beds(self):
    #pdb.set_trace()
    if self.is_dorm :
      beds_existed = self.product_variant_count
      variant = self.env['product.attribute'].search([('name','ilike','bed')])
      if variant :
	variant_values = self.env['product.attribute.value'].search([('attribute_id','=',variant[0].id)])
	value_count = len(variant_values)
	
	count = self.capacity - beds_existed
	if count > 0:
	  for i in range (0,count):
	    if value_count < self.capacity :
	      vals = {
		      'name' : 'Bed%s'%str(value_count+1),
		      'attribute_id' : variant[0].id,
		      }
	      new_variant = self.env['product.attribute.value'].create(vals)
	      value_count +=1
      
      else :
	variant = self.env['product.attribute'].create({
							'name' : 'Bed',
							})
	
	for i in range(0,self.capacity):
	  variant_values = self.env['product.attribute.value'].create({
								      'name' : 'Bed%s'%str(i+1),
								      'attribute_id' : variant[0].id,
								      })
     
      if self.capacity > beds_existed:
	if self.attribute_line_ids :
	  variants_to_create = self.env['product.attribute.value'].search([('id','not in',(self.attribute_line_ids.value_ids.ids))])
	  new_variants_to_create = variants_to_create[:count]
	
	    
	  for item in new_variants_to_create:  
	    val_vals = {
		    'name' : item.name,
		    'attribute_id' : variant[0].id,
		    }
	    self.attribute_line_ids.value_ids = [(1,item.id,val_vals)]
	    
	    prod_vals = {
			  'name':self.name,
			  'product_tmpl_id':self.id,
			  'attribute_value_ids':[(6, 0, item.ids)]
			  
			}
	    self.env['product.product'].create(prod_vals)
	    
	else :
	  values = self.env['product.attribute.value'].search([('attribute_id','=',variant[0].id)])
	  var_vals = {
		      'product_tmpl_id': self.id,
		      'attribute_id': variant[0].id,
		      'value_ids': [(6,0, values.ids[:self.capacity])]
		      
		      }
	  product_variant = self.env['product.attribute.line'].create(var_vals)
	  
	  for item in values[:self.capacity]:
	    prod_vals = {
			    'name':self.name,
			    'product_tmpl_id':self.id,
			    'attribute_value_ids':[(6, 0, item.ids)]
			    
			  }
	    self.env['product.product'].create(prod_vals)

      elif self.capacity < beds_existed:
	
	delet_num = beds_existed - self.capacity
	index_val = beds_existed - delet_num
	variants_to_delete = self.env['product.attribute.value'].search(
	    [('id', 'in', (self.attribute_line_ids.value_ids.ids))])
	new_variants_to_delete = variants_to_delete[index_val:]
	for item in new_variants_to_delete:
	    self.attribute_line_ids.value_ids = [(2, item.id)]
	pro_id = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
	for rec in pro_id[self.capacity:]:
	    self.env['product.product'].search([('id', '=', rec.id)]).unlink()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    room_booking_status = fields.Selection([('new', 'New'),('checkin', 'Check in'),('checkout', 'Check Out')],default='new', string="Status")
    room_booking_id = fields.Many2one('booking.info','Booking Reference')
    order_id = fields.Many2one('sale.order','Sale Reference')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    no_of_days = fields.Integer('No of Days',compute='calculate_room_stay_days')
    
    @api.constrains('start_date','end_date')
    @api.depends('start_date','end_date')
    def calculate_room_stay_days(self):
      for item in self:
	if item.start_date and item.end_date:
	  room_days = datetime.strptime(item.end_date, "%Y-%m-%d %H:%M:%S") - datetime.strptime(item.start_date, "%Y-%m-%d %H:%M:%S")
	  item.no_of_days = room_days.days
	  item.write({'product_uom_qty':item.no_of_days})


class SaleOrderBooking(models.Model):
    _inherit = 'sale.order' 

    room_booking_id = fields.Many2one('booking.info','Booking Reference')

###############Booking Info Order Lines########################
class BookingInfoLines(models.Model):
  """booking info order lines"""
  _name = 'booking.info.lines'

  product_id = fields.Many2one('product.template', string="Rooms")
  capacity = fields.Integer(string="Capacity")
  booking_info_id = fields.Many2one('booking.info')

  @api.onchange('product_id')
  def capacity_update(self):
      if self.product_id:
          product_line_info = self.env['product.template'].search([('id', '=', self.product_id.id)])
          for rec in product_line_info:
              self.capacity = rec.capacity

class RoomStatusChange(models.TransientModel):
    _name = 'room.status.change'
    _description = 'To Change Status Of Room'
    product_id = fields.Many2one('product.product', string="Product")
################### Room Status Changing #######################
    # Need To Change Accordingly based on products_id passed
    @api.multi
    def change_to_dirty(self):

      if self.product_id:
          product_info = self.env['product.product'].search([('id', '=', self.product_id.id)])
          if product_info.is_a_room:
              product_info.product_tmpl_id.write({'status': 'Dirty'})
          elif product_info.is_dorm:
            product_info.write({'status': 'Dirty'})

    @api.multi
    def change_to_cleanup(self):
        if self.product_id:
            product_info = self.env['product.product'].search([('id', '=', self.product_id.id)])
            if product_info.is_a_room:
                product_info.product_tmpl_id.write({'status': 'Cleanup'})
            elif product_info.is_dorm:
                product_info.write({'status': 'Cleanup'})

    @api.multi
    def change_to_ready(self):
        if self.product_id:
            product_info = self.env['product.product'].search([('id', '=', self.product_id.id)])
            if product_info.is_a_room:
                product_info.product_tmpl_id.write({'status': 'Ready'})
            elif product_info.is_dorm:
                product_info.write({'status': 'Ready'})




