# -*- coding: utf-8 -*-

from datetime import datetime
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

class booking(models.Model):
    _inherit = 'product.product'

    def default_user_id(self):
    	return self.env.context.get('default_user_id', self.env.uid)

    @api.constrains('order_id')
    def get_partner_id(self):
    	if self.order_id.partner_id:
    		self.customer = self.order_id.partner_id.name
    	return

 
   #  def default_end_date(self):
   #      return datetime.today() + timedelta(days=1)
        
   #  # 
    start_date = fields.Date(default=fields.Date.today, required="True")
    end_date = fields.Datetime(default=fields.Date.today, required="True")
    #partner_id = fields.Many2one('res.partner', string='', readonly=True, required=True, change_default=True, index=True, track_visibility='always')
    customer = fields.Char("")
   # 

class SchedulerBooking(models.Model):
    """docstring for SchedulerforBooking"""

    _name = 'scheduler.booking'

    @api.model  
    def get_products(self):
      # return True
      # import pdb;pdb.set_trace()
      vals = []
      product_ids = self.env['product.template'].search([('is_room', '=', True)])
      for record in product_ids:
          vals.append({
              'id': str(record.id),
              'name': record.name,
              'capacity': str(record.capacity),
              'status' : record.status,
          })
      return vals

    @api.model
    def fetch_order_line(self):
      rec = []
      # import pdb;pbd.set_trace()
      start_date = self.env.context['start_date']
      end_date = self.env.context['end_date']
      print " vals fetch order line==---->"
      order_ids = self.env['sale.order.line'].search([('start_date', '>=', start_date),
                                                      ('end_date', '<=', end_date),
                                                      ('product_id.is_room', '=', True)])
      print "order_ids---fetch---->>>", order_ids
      # book_id= str(record.order_id.room_booking_id.id)
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
      print "Rec===------->>>", rec

      return rec




class BookingInfo(models.Model):
  _name = 'booking.info'
  name = fields.Char("Product Name")
  customer = fields.Many2one('res.partner', string="Customer")
  start_date = fields.Datetime(string='Start Date')
  end_date = fields.Datetime(string='End Date')
  product_id = fields.Many2one('product.template', string="Product")
  button_flag = fields.Integer('Button Flag',default = 1)
  sale_reference = fields.Many2one('sale.order', 'Sale Reference')
  room_booking_status = fields.Selection([('new', 'New'),('checkin', 'Check in'),('checkout', 'Check Out')], default='new', string="Status")
  booking_lines = fields.One2many('booking.info.lines','booking_info_id', string="Booking Info Lines")
  is_multiple = fields.Boolean(string="Multiple Booking")
  multiple_booking_ids = fields.Many2many('product.template', 'room_booking_rel', 'pid', 'bid', 'Multiple Booking')



  def _get_new_sale_line(self, product_id, start_date, end_date, room_booking_id,room_booking_status):
      # import pdb;pdb.set_trace()
      
      res = {
          'product_id': product_id.id,
          'room_booking_status': room_booking_status,
          'start_date': start_date,
          'end_date': end_date,
          'room_booking_id': room_booking_id,

      }
      return res

  # datetime.datetime.strptime(tmp, '%Y-%m-%d %H:%M:%S')

  def _get_order_lines(self, order):
      res = []
      # count = order['count']
      for rec in order:
          product_id = rec['product_id']
          room_booking_id = self.id
          room_booking_status=self.room_booking_status
          start_date = rec['start_date']
          end_date = rec['end_date']
          s_date = start_date.replace("T", " ")
          e_date = end_date.replace("T", " ")
          # price_unit = rec['price_unit']
          res.append(
              (0, 0, self._get_new_sale_line(product_id, s_date, e_date, room_booking_id,room_booking_status))
          )
          # import pdb;pdb.set_trace()
      return res

  def multiple_booking(self, values, mult):
      rec = []
      self.button_flag = 2
      partner_id = values['partner_id']
      sale_mult_vals = {
          'partner_id': partner_id,

          # 'date_order': date_order,
          # 'company_id': self.company_id.id,
          'order_line': self._get_order_lines(mult)
      }
      for rec in mult:
          sale_order_vals = self.env['sale.order.line'].search([('start_date', '>', rec['start_date']),
                                                                ('start_date', '<', rec['end_date']),
                                                                ('end_date', '>', rec['start_date']),
                                                                ('end_date', '<', rec['end_date']), ])

      if sale_order_vals:
          raise UserError(_('Already Booked !! Select a new date.'))

      else:
          sale = self.env['sale.order'].create(sale_mult_vals)
          self.sale_reference = sale.id
      return {'type': 'ir.actions.act_window_close'}


  # @api.onchange('date_order')

  def insert_sale_order(self):
      mult = []
      if self.is_multiple:
          s_date = self.start_date
          e_date = self.end_date
          for record in self:
              values = {
                  'partner_id': record.customer.id,

              }
          for re in self.booking_lines:
            mult.append({'product_id': re['product_id'],
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
                  {'product_id': record.product_id,
                   'start_date': record.start_date,
                   'end_date': record.end_date,
                   }
              ]
          self.sale_order_booking(vals, order)


  @api.one
  def sale_order_booking(self, vals, order):
      self.button_flag = 2

      partner_id = vals['partner_id']

      # date_order = vals['date_order']
      # import pdb; pdb.set_trace()
      # order_line = self._get_order_lines(order)
      # self.write({'order_line.room_booking_status' : self.room_booking_status})
   
      sale_vals = {
          'partner_id': partner_id,
          
          # 'date_order': date_order,
          # 'company_id': self.company_id.id,
          'order_line'  : self._get_order_lines(order)
      }
      for rec in order:
        sale_order_vals = self.env['sale.order.line'].search([('start_date', '>', rec['start_date']),
                                                            ('start_date', '<', rec['end_date']),
                                                            ('end_date', '>', rec['start_date']),
                                                            ('end_date', '<', rec['end_date']), ])
      if sale_order_vals:
          raise UserError(_('Already Booked !! Select a new date.'))

      else:
          sale = self.env['sale.order'].create(sale_vals)
          self.sale_reference = sale.id
      return {'type': 'ir.actions.act_window_close'}

  @api.model
  def update_sale_order_line(self):

    sale_order_id = self.env.context['sale_order_id']
    booking_id = self.env.context['booking_id']
    new_start = self.env.context['new_start']
    new_end = self.env.context['new_end']
    new_room = self.env.context['new_room']
    # import pdb;pdb.set_trace()
    book_id = int(booking_id)
    room_id = int(new_room)
    room_book = self.env['booking.info'].search([('id','=',book_id)])
    # import pdb;pdb.set_trace()
    order_line_info = self.env['sale.order.line'].search([('id', '=', sale_order_id)])
    count = self.env['sale.order.line'].search_count([('order_id','=',room_book.sale_reference.id)])
    index = count - 1
    if room_id != room_book.product_id.id and room_book.sale_reference.order_line[index].room_booking_status=='checkin':

      booking_info = self.env['booking.info'].create({
                                                  'name': room_book.name,
                                                  'customer': room_book.customer.id,
                                                  'start_date': new_start,
                                                  'end_date':room_book.sale_reference.order_line[index].end_date,
                                                  'product_id':room_id ,
                                                  'button_flag': 2,
                                                  'sale_reference': room_book.sale_reference.id,
                                                  'room_booking_status': 'checkin',
                                                   })
      order_line = room_book.env['sale.order.line'].create({
                                                  'order_id': booking_info.sale_reference.id,
                                                  'product_id': booking_info.product_id.id,
                                                  'start_date': booking_info.start_date,
                                                  'end_date':booking_info.end_date,
                                                  'room_booking_status': booking_info.room_booking_status,
                                                  'room_booking_id': booking_info.id,
                                                   })
      room_book.sale_reference.order_line[index].room_booking_status = 'checkout'
      room_book.sale_reference.order_line[index].end_date = new_start

    else:
      room_book.write({'start_date': new_start, 'end_date': new_end, 'product_id': room_id})
      order_line_info.write({'start_date': new_start, 'end_date': new_end, 'product_id': room_id})

    # else:
    #   return


  def update_status(self):
    # self.update_flag = 2
    order_line_info = self.env['sale.order.line'].search([('room_booking_id', '=', self.id)])
    booking_line_info = self.env['booking.info'].search([('id', '=', self.id)])
    # print "booking_line_info====------------>>>>", booking_line_info

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
    # booking_id = 14
    # sale_order_line_id = 35
    order_line_info = self.env['sale.order.line'].search([('id', '=', sale_order_line_id)])
    if sale_order_line_id:
      for rec in order_line_info:
        chk_order_id = self.env['sale.order.line'].search([('order_id', '=', rec.order_id.id)])
        if len(chk_order_id) <= 1:
            self.env['sale.order'].search([('id', '=', rec.order_id.id)]).unlink()
    #  book id to be passed to search
    if booking_id:
      self.env['booking.info'].search([('id', '=', booking_id)]).unlink()

    if sale_order_line_id:
         self.env['sale.order.line'].search([('id', '=', sale_order_line_id)]).unlink()

  @api.model
  def extend_booking(self):
    sale_order_line_id = int(self.env.context['sale_order_line_id'])
    booking_id = int(self.env.context['booking_id'])
    new_start_date = self.env.context['new_start_date']
    new_end_date = self.env.context['new_end_date']
    # booking_id = 17
    # sale_order_line_id = 52
    flag = 0
    # new_start_date = '2017-07-23 00:00:00'
    # new_end_date = '2017-07-29 00:00:00'
    # chk_dates = self.env['sale.order.line'].search([('start_date', '>=', new_start_date),
    #                                                 ('end_date', '<=', new_start_date)])
    sale_update_info = self.env['sale.order.line'].browse(sale_order_line_id)
    booking_update_info = self.env['booking.info'].browse(booking_id)
    ####----
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
    # print "check dates==--->>>", chk_dates
    # if chk_dates:
    #     raise UserError(_('Booking is Not Possible'))
    # else:
      if sale_order_line_id:
            sale_update_info.write({'start_date': new_start_date, 'end_date': new_end_date})
    else:
        raise UserError(_('Booking is Not Possible'))

  @api.onchange('customer')
  def create_booking_lines(self):
    # import pdb; 
    if self.is_multiple == True:
      for rooms in self.multiple_booking_ids:
        # pdb.set_trace()
        room = self.env['booking.info.lines'].create({
                                                       'booking_info_id' : self.id,
                                                      'product_id' : rooms.id,
                                                     

          })

class Product(models.Model):
  """docstring for Product"""
  _inherit = 'product.template'

  booking_info = fields.One2many('booking.info', 'product_id', 'Bookings')
  capacity = fields.Integer(string="Capacity")
  status = fields.Selection([('Dirty', 'Dirty'), ('Cleanup', 'Clean Up'), ('Ready', 'Ready')],
                            string="Status")



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    room_booking_status = fields.Selection([('new', 'New'),('checkin', 'Check in'),('checkout', 'Check Out')],default='new', string="Status")
    room_booking_id = fields.Many2one('booking.info','Booking Reference')

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