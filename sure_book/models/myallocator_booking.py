from datetime import datetime
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
import requests
import json
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp

class res_partner(models.Model):
    _inherit ='res.partner'

#    surname = fields.Char('Surname')    
    check_in = fields.Boolean('Is checked-in')    
    room_no = fields.Char('Room No.')    
    room_id = fields.Many2one('product.product',string='Room')    
    id_passport = fields.Char('ID/PASSPORT')
#    @api.multi
#    def name_get(self):
#        res = []
#        for partner in self:
#            name = partner.name or ''
#            surname = partner.surname or ''
#            full_name = name + " " + surname
#            name = full_name or ''
#
#            if partner.company_name or partner.parent_id:
#                if not name and partner.type in ['invoice', 'delivery', 'other']:
#                    name = dict(self.fields_get(['type'])['type']['selection'])[partner.type]
#                if not partner.is_company:
#                    name = "%s, %s" % (partner.commercial_company_name or partner.parent_id.name, name)
#            if self._context.get('show_address_only'):
#                name = partner._display_address(without_company=True)
#            if self._context.get('show_address'):
#                name = name + "\n" + partner._display_address(without_company=True)
#            name = name.replace('\n\n', '\n')
#            name = name.replace('\n\n', '\n')
#            if self._context.get('show_email') and partner.email:
#                name = "%s <%s>" % (name, partner.email)
#            if self._context.get('html_format'):
#                name = name.replace('\n', '<br/>')
#            res.append((partner.id, name))
#        return res
#    
    
class SaleOrder(models.Model):
    _inherit ='sale.order'
    
    
    def _get_current_date(self):
        for data in self:
            for date in data:
                date.new_current_date = datetime.now().date()
    
    
    new_current_date = fields.Date('Start Date', compute="_get_current_date")
    
    is_book = fields.Boolean('Is Booking')
    book_id = fields.Char('Book ID')
    allocator_id = fields.Char('My Allocator ID')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    property_id = fields.Many2one('myallocator.property',string='Property')
    room_id = fields.Many2one('product.template',string='Room')
    channel_id = fields.Many2one('myallocator.channel',string='Channel')
    descrip = fields.Text('Note') 
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Check-In'),
        ('check_out', 'Check-Out'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    
    room_no = fields.Char('Room Number')
    pos_order_ids = fields.One2many('pos.order', 'sale_order_id', 'POS Orders')
    
    @api.model
    def create(self, vals):
        print"--------",vals
        user_obj = self.env['res.users']
        book_info_obj = self.env['booking.info']
#        if not vals['property_id']:
        user_id = user_obj.search([('id','=', self._uid)])
        vals['property_id'] = user_id.property_id.id
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or 'New'

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)
        result = super(SaleOrder, self).create(vals)
        
        return result
    

    @api.model
    def action_arrival(self):
        
        sale_id = self.env['sale.order'].search([('start_date','=',datetime.now().date()), ('state','in',('draft','sale'))])
        list_arrive = []
        state_val = ''
        for sale in sale_id:
            partner_id = sale.partner_id.name
            name = sale.name
            id = sale.id
          
            if sale.state == 'sale':
                state_val = 'Checked-In'
            else:
                state_val = 'Quotation'

            values = {
                'id': id,
                'partner_id': partner_id,
                'name': name,
                'state': state_val
            }
            list_arrive.append(values)
        
        return list_arrive
    
    @api.model
    def action_arrival_count(self):
        
        sale_id = self.env['sale.order'].search([('start_date','=',datetime.now().date()), ('state','=','draft')])
        arrive_count = len(sale_id)
        return arrive_count
    
    
    @api.model
    def action_departure(self):
        
        sale_id = self.env['sale.order'].search([('end_date','=',datetime.now().date()), ('state','in',('sale','check_out'))])
        list_depart = []
        
        for sale in sale_id:
            partner_id = sale.partner_id.name
            name = sale.name
            id = sale.id
        
            if (sale.state == 'check_out'):
                state_val = 'Check-Out'
            else:
                state_val = 'Checked-In'

            values = {
                'id': id,
                'partner_id': partner_id,
                'name': name,
                'state': state_val
            }
            list_depart.append(values)
        return list_depart
    
    @api.model
    def action_departure_count(self):
        
        sale_id = self.env['sale.order'].search([('end_date','=',datetime.now().date()), ('state','=','sale')])
        depart_count = len(sale_id)
        
        return depart_count
    
    
    @api.model
    def action_occupied(self):
        
        sale_id = self.env['sale.order'].search([('start_date','<=',datetime.now().date()),
        ('end_date','>=',datetime.now().date()), ('state','=','sale')])
        list_occupy = []
        state_val = ''
        for sale in sale_id:
            partner_id = sale.partner_id.name
            name = sale.name
            id = sale.id
            
            if sale.state == 'sale':
                state_val = 'Checked-In'
            else:
                state_val = 'Check-Out'
            
            
            values = {
                'id': id,
                'partner_id': partner_id,
                'name': name,
                'state': state_val
            }
            list_occupy.append(values)
        
        return list_occupy
    
    @api.model
    def action_occupied_count(self):
        
        sale_id = self.env['sale.order'].search([('start_date','<=',datetime.now().date()),
        ('end_date','>=',datetime.now().date()), ('state','=','sale')])
        occupy_count = len(sale_id)
        return occupy_count
    
    
    @api.model
    def compute_customer(self):
        list_customer = []
        for i in self.env['res.partner'].search([]):
            if i.sale_order_ids:
                vals={
                    'name': i.name,
                    'email': i.email or '',
                    'phone': i.phone or '',
                    }
                list_customer.append(vals)
        return list_customer
    
    
    @api.model
    def action_sales(self):
        
        sale_id = self.env['sale.order'].search([('state','=','sale'),('start_date','!=',False),
        ('end_date','!=',False)])
        list_sale = []
        for sale in sale_id:
            start = sale.start_date
            end = sale.end_date
            date_format = "%Y-%m-%d"
            a = datetime.strptime(str(start), date_format)
            b = datetime.strptime(str(end), date_format)
            delta = b - a
#            delta = sale.end_date - sale.start_date
            nights = delta.days + 1
            partner_id = sale.partner_id.name
            name = sale.name
            revenue = sale.amount_total
            check_in = sale.start_date

            values = {
                'partner_id': partner_id,
                'name': name,
                'revenue': revenue,
                'check_in': check_in,
                'nights': nights,
            }
            list_sale.append(values)
        
        return list_sale
    
    
    @api.model
    def action_cancel_data(self):
        
        sale_id = self.env['sale.order'].search([('state','=','cancel'),('start_date','!=',False),
        ('end_date','!=',False)])
        list_cancel = []
        for sale in sale_id:
            partner_id = sale.partner_id.name
            name = sale.name
            check_in = sale.start_date

            values = {
                'partner_id': partner_id,
                'name': name,
                'check_in': check_in,
            }
            list_cancel.append(values)
        
        return list_cancel
    
    
  
    @api.multi
    def action_confirm(self):
        for order in self:
#            order.create_booking()
            order.state = 'sale'
            order.confirmation_date = fields.Datetime.now()
            if self.env.context.get('send_email'):
                self.force_quotation_send()
            order.order_line._action_procurement_create()
            for line in order.order_line:
                if line.room_booking_status == 'new':
                    line.write({'room_booking_status': 'checkin'})
                line.partner_ids
                print"------------line.partner_ids------------",line.partner_ids 
                for partner in line.partner_ids:
                    partner.write({'check_in' : True,
                                    'room_no' : line.product_id.id,
                                    'room_id' : line.product_id.id,
                    })
        if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
            self.action_done()
        
        return True
    
    
    @api.multi
    def action_cancel(self):
        for line in self.order_line:
            for partner in line.partner_ids:
                    partner.write({'check_in' : False,
                                    'room_no' : '',
                                    'room_id' : '',
                    })
        self.write({'state': 'cancel'})
    
    
    @api.multi
    def action_check_out(self):
        self.write({'state': 'check_out'})
    
    
    @api.multi
    def check_out_process(self):
        print"----------self-------------",self
        inv_obj = self.env['account.invoice']
        sale_line_obj = self.env['sale.order.line']
        journal_id = self.env['account.invoice'].default_get(['journal_id'])['journal_id']
        if not journal_id:
            raise UserError(_('Please define an accounting sale journal for this company.'))
        print"-------self.order_line--------",self.order_line
        
        inv_list = []
        order_list = []
        
        vals = {
                'name': self.client_order_ref or '',
                'origin': self.name,
                'type': 'out_invoice',
                'account_id': self.partner_id.property_account_receivable_id.id,
                'partner_id': self.partner_id.id,
                'partner_shipping_id': self.partner_shipping_id.id,
                'journal_id': journal_id,
                'currency_id': self.pricelist_id.currency_id.id,
                'comment': self.note,
                'payment_term_id': self.payment_term_id.id,
                'fiscal_position_id': self.fiscal_position_id.id or self.partner_id.property_account_position_id.id,
                'company_id': self.company_id.id,
                'user_id': self.user_id and self.user_id.id,
                'team_id': self.team_id.id
        }
        inv_id = inv_obj.create(vals)
        
        for line in self.order_line:    
            print"----------line-------------",line

            account = line.product_id.property_account_income_id or line.product_id.categ_id.property_account_income_categ_id
            if not account:
                raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                    (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

            fpos = line.order_id.fiscal_position_id or line.order_id.partner_id.property_account_position_id
            if fpos:
                account = fpos.map_account(account)

            res = {
                'name': line.name,
                'sequence': line.sequence,
                'origin': line.order_id.name,
                'account_id': account.id,
                'price_unit': line.price_unit,
                'quantity': line.qty_to_invoice,
                'discount': line.discount,
                'uom_id': line.product_uom.id,
                'product_id': line.product_id.id or False,
                'layout_category_id': line.layout_category_id and line.layout_category_id.id or False,
                'product_id': line.product_id.id or False,
                'invoice_line_tax_ids': [(6, 0, line.tax_id.ids)],
                'account_analytic_id': line.order_id.project_id.id,
                'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
            }
            print"-------------res-----------",res

            res.update({'invoice_id': inv_id.id})
            print"-------------res--------rrrr---",res
            inv_line_id = self.env['account.invoice.line'].create(res)
            print"-------------inv_line_id-----------",inv_line_id

        in_list = []
        for pos_order_id in self.pos_order_ids:
            if not pos_order_id.invoice_id:
                pos_inv_id = pos_order_id.action_pos_order_invoice()
                print"-------------pos_inv_id-----------",pos_inv_id
#                print"-------------pos_inv_id-----------",pos_inv_id.name
                pos_order_id.invoice_id.write({'origin' : self.name})
                
                in_list.append(pos_order_id.invoice_id)
                print"-------------in_list-----------",in_list
        
        del_list = []
        for pos_line in in_list:
            print"-------------pos_line-----------",pos_line
            print"-------------pos_line-----------",pos_line.name
            for inv_line in pos_line.invoice_line_ids:
                print"-------------inv_line-----------",inv_line
#                print"-------------inv_line-----------",inv_line.name
                del_inv_id = inv_line.invoice_id
                del_list.append(del_inv_id)
                inv_line.write({'invoice_id' : inv_id.id,})
                print"-------------inv_line-----123------",inv_line
        print"-------------del_list-----123------",del_list 
        
        for delete in del_list:
            del_inv_id = self.env['account.invoice'].search([('id','=', delete.id)])
            if del_inv_id:
                delete.unlink()


        for_tax = self.env['account.invoice'].search([('origin','=', self.name)]) 
        for inv in for_tax:
            inv.compute_taxes()
            inv.action_date_assign()
            inv.action_move_create()
            inv.invoice_validate()
            
            domain = ('account_id', '=', inv.account_id.id), ('partner_id', '=', self.env['res.partner']._find_accounting_partner(inv.partner_id).id), ('reconciled', '=', False), ('amount_residual', '!=', 0.0)
            lines = self.env['account.move.line'].search(domain)
            for line in lines:
                inv.assign_outstanding_credit(line.id)
        
        self.action_check_out()   
        for line in self.order_line:
            if line.room_booking_status == 'checkin':
                line.write({'room_booking_status': 'checkout'})
            for partner in line.partner_ids:
                    partner.write({'check_in' : False,
                                    'room_no' : '',
                                    'room_id' : '',
                    })
        return True

    @api.multi
    def merge_invoices(self):
        self.check_out_process()
        return self.action_view_invoice()

    
    
    @api.multi
    def split_invoices(self):
        print"----------self-------------",self
        inv_obj = self.env['account.invoice']
        sale_line_obj = self.env['sale.order.line']
        journal_id = self.env['account.invoice'].default_get(['journal_id'])['journal_id']
        if not journal_id:
            raise UserError(_('Please define an accounting sale journal for this company.'))
        print"-------self.order_line--------",self.order_line
        
        inv_list = []
        order_list = []
        
        for line in self.order_line:    
            print"----------line-------------",line
            print"----------line-------------",len(line.partner_ids)
            for li in line.partner_ids:
                print"--------li-----------",li
                vals = {
                        'name': self.client_order_ref or '',
                        'origin': self.name,
                        'type': 'out_invoice',
                        'account_id': li.property_account_receivable_id.id,
                        'partner_id': li.id,
                        'partner_shipping_id': self.partner_shipping_id.id,
                        'journal_id': journal_id,
                        'currency_id': self.pricelist_id.currency_id.id,
                        'comment': self.note,
                        'payment_term_id': self.payment_term_id.id,
                        'fiscal_position_id': self.fiscal_position_id.id or li.property_account_position_id.id,
                        'company_id': self.company_id.id,
                        'user_id': self.user_id and self.user_id.id,
                        'team_id': self.team_id.id
                    }
                inv_id = inv_obj.create(vals)
                print"----------inv_id-------------",inv_id  
                print
                account = line.product_id.property_account_income_id or line.product_id.categ_id.property_account_income_categ_id
                if not account:
                    raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                        (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

                fpos = line.order_id.fiscal_position_id or line.order_id.partner_id.property_account_position_id
                if fpos:
                    account = fpos.map_account(account)

                res = {
                    'name': line.name,
                    'sequence': line.sequence,
                    'origin': line.order_id.name,
                    'account_id': account.id,
                    'price_unit': line.price_unit/len(line.partner_ids),
                    'quantity': line.qty_to_invoice,
                    'discount': line.discount,
                    'uom_id': line.product_uom.id,
                    'product_id': line.product_id.id or False,
                    'layout_category_id': line.layout_category_id and line.layout_category_id.id or False,
                    'product_id': line.product_id.id or False,
                    'invoice_line_tax_ids': [(6, 0, line.tax_id.ids)],
                    'account_analytic_id': line.order_id.project_id.id,
                    'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                }
                print"-------------res-----------",res

                res.update({'invoice_id': inv_id.id})
                print"-------------res--------rrrr---",res
                inv_line_id = self.env['account.invoice.line'].create(res)
                print"-------------inv_line_id-----------",inv_line_id

        in_list = []
        not_in_list = []
        for pos_order_id in self.pos_order_ids:
            if not pos_order_id.invoice_id:
                pos_inv_id = pos_order_id.action_pos_order_invoice()
                if pos_order_id.invoice_id.partner_id == inv_line_id.partner_id:
                    pos_order_id.invoice_id.write({'origin' : self.name})
                    in_list.append(pos_order_id.invoice_id)
                else: 
                    pos_order_id.invoice_id.write({'origin' : self.name})
                    not_in_list.append(pos_order_id.invoice_id)
        
        del_pos_line = []
        for pos_line in in_list:
            for inv_line in pos_line.invoice_line_ids:
                print"-------------inv_line-----------",inv_line
                del_inv_id = inv_line.invoice_id
                del_pos_line.append(del_inv_id)
                inv_line.write({'invoice_id' : inv_id.id,})
                
        for delete_pos in del_pos_line:
            del_inv_id = self.env['account.invoice'].search([('id','=', delete_pos.id)])
            if del_inv_id:
                delete_pos.unlink()
        
        del_pos_not_line = []
        for pos_not_line in not_in_list:  
            print"-------------pos_not_line-----------",pos_not_line
            inv_id = self.env['account.invoice'].search([('origin','=', self.name),
                ('partner_id','=', pos_not_line.partner_id.id)])
            print"-------------inv_id-----------",inv_id
            if len(inv_id) > 1:
                data = inv_id[0]
                for inv in inv_id[1:]:
                    for inv_line in inv.invoice_line_ids:
                        del_inv_id = inv_line.invoice_id
                        del_pos_not_line.append(del_inv_id)
                        inv_line.write({'invoice_id' : data.id,})
                        
        for delete_pos in del_pos_not_line:
            del_inv_id = self.env['account.invoice'].search([('id','=', delete_pos.id)])
            if del_inv_id:
                delete_pos.unlink()
                                
        for_tax = self.env['account.invoice'].search([('origin','=', self.name)]) 
        for inv in for_tax:
            inv.compute_taxes()
            print"-------------inv-----------",inv        
            inv.action_date_assign()
            inv.action_move_create()
            inv.invoice_validate()
            
            domain = ('account_id', '=', inv.account_id.id), ('partner_id', '=', self.env['res.partner']._find_accounting_partner(inv.partner_id).id), ('reconciled', '=', False), ('amount_residual', '!=', 0.0)
            lines = self.env['account.move.line'].search(domain)
            for line in lines:
                inv.assign_outstanding_credit(line.id)

        self.action_check_out()  
        for line in self.order_line:
            if line.room_booking_status == 'checkin':
                line.write({'room_booking_status': 'checkout'})
            for partner in line.partner_ids:
                    partner.write({'check_in' : False,
                                    'room_no' : '',
                                    'room_id' : '',
                    })
            
        return self.action_view_invoice()
    
    

#    @api.multi
#    def book_data(self,book):
#        list = []
#        if not self.book_id:
#            if self.order_line:
#                
#                room_id_val = ""
#                price_val = 0.0
#                unit = 0.0
#                desc = ""
#                occupancy = 0.0
#                for order in self.order_line:
#                    if order.is_room:
#                        for room in order.product_id.room_variant_ids:
#                            if order.property_id == room.property_id:
#                                room_id_val = room.room_id
#                                price_val = room.price
#                                unit = room.unit
#                                desc = room.product_id.name
#                                occupancy = room.occupancy
#        
#                                vals = {
#                                    "StartDate":str(order.start_date),
#                                    "EndDate":str(order.end_date),
#                                    "RoomTypeId":str(room_id_val),
#        #                            "RoomTypeId":str(self.order.room_id),
#        #                            "ChannelRoomType":str(self.channel_id.channel_id),
#                                    "Units": str(unit),
#                    #                "RateId": "123",
#                                    "RoomDayRate": str(price_val),
#                    #                "RoomDayDescription": str(self.room_id.name),
#        #                            "RoomDayDescription": str(self.room_id.description_sale),
#                                    "CustomerFName": str(self.partner_id.name),
#                                    "CustomerLName": str(self.partner_id.surname),
#                                    "RoomDesc": str(desc),
#                    #                "OccupantSmoker": "false",
#                    #                "OccupantNote": "Please do not put me by the elevator. Thanks!",
#                    #                "OccupantFName": "Tyler",
#                    #                "OccupantLName": "Green",
#                                    "Occupancy": str(occupancy),
#                    #                "Policy": "No smoking.",
#                                }
#                                list.append(vals)
#        if list:
#            list = list[0]
#        else:
#            list = {}
#
#        return list
    
#    Creates Booking in MyAllocator
    @api.multi
    def create_booking(self):
        if not self.book_id:
            for order in self.order_line:
                if order.is_room:
                    order.create_booking_line()
        return True
    
#    @api.multi
#    def create_booking(self):
#        book = {}
#        book_data = self.book_data(book)
#        config = self.env['myallocator.config'].search([])
#        url = "http://api.myallocator.com/pms/v201408/json/LoopBookingCreate"
#        headers = {
#            'content-type': "application/json",
#            'cache-control': "no-cache",
#        }
#        if book_data:
#            payload = {
#              "Auth/UserToken":str(config.usertoken),
#              "Auth/PropertyId":str(self.property_id.property_id),
#              "Auth/VendorId":str(config.vendor_id),
#              "Auth/VendorPassword":str(config.vendorpwd),
#              "Booking":book_data,
#              }
#            data_json = json.dumps(payload)
#            print"---------data_json-----------",data_json
#            response = requests.request("POST", url, data=data_json, headers=headers)
#            print(response.text)
#            response_data = json.loads(response.text)
#            booking = response_data['Booking']
#            if response_data['Success'] == True:
#                self.write({'book_id':str(booking['OrderId']),
#                            'allocator_id':str(booking['MyallocatorId']),
#                            'is_book':response_data['Success'] ,
#                                })
#                print"---------self-----------",self.book_id
#                print"---------self-----------",self.allocator_id
#                print"---------self-----------",self.is_book
##                self.action_confirm()
#        return True
    
    
    
    @api.multi
    def check_availability(self):
        config = self.env['myallocator.config'].search([])
        url = "http://api.myallocator.com/pms/v201408/json/RoomAvailabilityList"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        payload = {
          "Auth/UserToken":str(config.usertoken),
          "Auth/PropertyId":str(self.property_id.property_id),
          "Auth/VendorId":str(config.vendor_id),
          "Auth/VendorPassword":str(config.vendorpwd),
          "StartDate":str(self.start_date),
          "EndDate":str(self.end_date),
          }
        data_json = json.dumps(payload)
        response = requests.request("POST", url, data=data_json, headers=headers)

        print(response.text)
        response_data = json.loads(response.text)

        room_detail = response_data['Rooms']
        
        if self.room_detail_id:
            for rd in self.room_detail_id:
                rd.unlink()
        
        for detail in room_detail:
            for date_detail in detail['Dates']:
                vals = {
                    'room_id' : detail['RoomId'],
                    'name' : detail['RoomName'],
                    'date' : date_detail['Date'],
                    'is_private' : detail['isPrivate'],
                    'min_stay' : date_detail['MinStay'],
                    'max_stay' : date_detail['MaxStay'],
                    'unit' : date_detail['Units'],
                    'price' : date_detail['Price'],
                    'booking_list_id' : self.id,
                }
                available_id = available_obj.create(vals)
        return True

    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    current_date = fields.Date('Current Date', default=datetime.now().date())
    activities = fields.Selection([('morning','Morning'),('midday','Midday'),('sunset','Sunset')],'Activities')
    partner_ids = fields.Many2many('res.partner', string='Recipients')
    res_partner_id = fields.Many2one('res.partner',string='Partner')
    is_available = fields.Boolean('Is Available')
    is_room = fields.Boolean('Is Room')
    is_activities = fields.Boolean('Is Activities')
    is_transport = fields.Boolean('Is Transport')
    property_id = fields.Many2one('myallocator.property',string='Property')
    
    is_book = fields.Boolean('Is Booking')
    book_id = fields.Char('Book ID')
    allocator_id = fields.Char('My Allocator ID')
    
    
    
    @api.multi
    def get_start_date(self):
        print"------------self---------",self
#        print"------------self---------",self.order_id
        for date_order in self:
            sale_obj = self.env['sale.order']
            sale_id = sale_obj.search([('id','=', date_order.order_id.id)])
            print"------------self---------",self
            if sale_id:
                if date_order.order_id == sale_id and date_order.is_room == True:
                    sale_id.write({'start_date': date_order.start_date, 'end_date': date_order.end_date})
 
    
    @api.multi
    def get_booking_info(self):
        book_info_obj = self.env['booking.info']
        book_info_id = book_info_obj.create({
                'customer': self.order_id.partner_id.id,
                'start_date' : self.start_date,
                'end_date' : self.end_date,
                'product_id' : self.product_id.id,
                'sale_reference' : self.order_id.id,
                'room_booking_status' : 'new',
                'button_flag' : 1,
                'amount_total': self.order_id.amount_total
                })
        print"----book_info_id----",book_info_id
#        print"----line.order_id.amount_total----",line.order_id.amount_total
        self.order_id.write({'room_booking_id': book_info_id.id})
        print"----self.order_id----",self.order_id.room_booking_id
        book_vals = {
            'room_booking_status' : 'new',
            'order_line' : book_info_id.id,
        }
        self.write(book_vals)
        return True
    
    
    
#    Create function - Checking available rooms and activities
    @api.model
    def create(self, values):
        print"------------values------------",values
        book_info_obj = self.env['booking.info']
        prod_temp_obj = self.env['product.template']
        onchange_fields = ['name', 'price_unit', 'product_uom', 'tax_id']
        if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
            line = self.new(values)
            line.product_id_change()
            for field in onchange_fields:
                if field not in values:
                    values[field] = line._fields[field].convert_to_write(line[field], line)
                    
        
        
        
        line_id = self.search([('is_room','=', True), ('product_id','=', values.get('product_id')),
        ('order_id','!=', ''),('state','!=', 'cancel'),('property_id','=', values.get('property_id'))])
        print"------------line_id------------",line_id
        test_list = []
#        if not self.order_id.is_calendar:
        for test in line_id:
            print"------------test------------",test.product_id
            if test.start_date <= values.get('start_date') < test.end_date or test.start_date < values.get('end_date') <= test.end_date:
                raise UserError(_("Room is already reserved for that day")) 
            else:
                print"----------------------"
        
        line = super(SaleOrderLine, self).create(values)
        print"------------line------------",line
        print"------------line------------",line.product_id
        
        
#        if not line.order_id.room_booking_id: 
#            book_info_id = book_info_obj.create({
#                    'customer': line.order_id.partner_id.id,
#                    'start_date' : line.start_date,
#                    'end_date' : line.end_date,
#                    'product_id' : line.product_id.id,
#                    'sale_reference' : line.order_id.id,
#                    'room_booking_status' : 'new',
##                    'amount_total': line.order_id.amount_total
#                })
#            print"----book_info_id----",book_info_id
#            print"----line.order_id.amount_total----",line.order_id.amount_total
#            line.order_id.write({'room_booking_id': book_info_id.id})
#            print"----line.order_id----",line.order_id.room_booking_id
#            book_vals = {
#                'room_booking_status' : 'new',
#                'order_line' : book_info_id.id,
#            }
#            
#            line.write(book_vals)
#            amount_total = line.order_id.amount_total
#            book_info_id.write({'product_id' : line.product_id.id,'amount_total' : amount_total})
#            print"-------line----------",line.room_booking_status
#            print"-------line----------",line.order_line
            
            
        if not line.order_id.room_booking_id:
            line.get_booking_info()
        line.get_start_date()
        
        
        line_id_morning = self.search([('current_date','=', values.get('current_date')),('activities','=', 'morning'),('product_id','=', values.get('product_id')),
                 ('order_id','!=', ''),('state','!=', 'cancel'),('property_id','=', line.property_id.id) ])
        print"------------line_id_morning------------",line_id_morning
        test_list = []
        
        
        for test in line_id_morning:
            if test.current_date == values.get('current_date'):
                test_list.append(test.id)
        print"------------test_list------------",test_list
        print"------------test_list------------",sorted(test_list)
        line_id_morning = []
        for test in sorted(test_list):
            act_morn = self.browse(test)
            line_id_morning.append(act_morn)
        print"------------line_id_morning------------",line_id_morning
        
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


            
        line_id_midday = self.search([('current_date','=', values.get('current_date')),('activities','=', 'midday'),('product_id','=', values.get('product_id')),
                 ('order_id','!=', ''),('state','!=', 'cancel') ,('property_id','=', line.property_id.id)])
        print"------------line_id_midday------------",line_id_midday
        
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
#            if li.order_id.state == 'sale':
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
        print"----------self------------",self
        lines = False
        if 'product_uom_qty' in values:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            lines = self.filtered(
                lambda r: r.state == 'sale' and float_compare(r.product_uom_qty, values['product_uom_qty'], precision_digits=precision) == -1)
        result = super(SaleOrderLine, self).write(values)
        
        self.get_start_date()
        
        
        
        line_id = self.search([('is_room','=', True), ('product_id','=', values.get('product_id')),
        ('order_id','!=', ''),('state','!=', 'cancel'),('property_id','=', values.get('property_id'))])
        print"------------line_id------------",line_id
        test_list = []
#        if not self.order_id.is_calendar:
        for test in line_id:
            print"------------test------------",test.product_id
            if test.start_date <= values.get('start_date') < test.end_date or test.start_date < values.get('end_date') <= test.end_date:
                raise UserError(_("Room is already reserved for that day")) 
            else:
                print"----------------------"
#        print"----------self.current_date------------",self.current_date

        for activity in self:
            if activity.is_activities:
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
#        lll
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
    
    
    
    
    
    @api.multi
    def create_booking_line(self):
        book = {}
        book_data = self.book_data(book)
        config = self.env['myallocator.config'].search([])
        url = "http://api.myallocator.com/pms/v201408/json/LoopBookingCreate"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        if book_data:
            payload = {
              "Auth/UserToken":str(config.usertoken),
              "Auth/PropertyId":str(self.property_id.property_id),
              "Auth/VendorId":str(config.vendor_id),
              "Auth/VendorPassword":str(config.vendorpwd),
              "Booking":book_data,
              }
            data_json = json.dumps(payload)
            print"---------data_json-----------",data_json
            response = requests.request("POST", url, data=data_json, headers=headers)
            print(response.text)
            response_data = json.loads(response.text)
            booking = response_data['Booking']
            if response_data['Success'] == True:
                self.write({'book_id':str(booking['OrderId']),
                            'allocator_id':str(booking['MyallocatorId']),
                            'is_book':response_data['Success'] ,
                                })
                print"---------self-----------",self.book_id
                print"---------self-----------",self.allocator_id
                print"---------self-----------",self.is_book
        return True
    
    @api.multi
    def book_data(self,book):
        if self.is_room:
            for room in self.product_id.room_variant_ids:
                room_id_val = ""
                price_val = 0.0
                unit = 0.0
                desc = ""
                occupancy = 0.0
                if self.property_id == room.property_id:
                    room_id_val = room.room_id
                    price_val = room.price
                    unit = room.unit
                    desc = room.product_id.name
                    occupancy = room.occupancy

                    vals = {
                        "StartDate":str(self.start_date),
                        "EndDate":str(self.end_date),
                        "RoomTypeId":str(room_id_val),
#                            "RoomTypeId":str(self.order.room_id),
#                            "ChannelRoomType":str(self.channel_id.channel_id),
                        "Units": str(unit),
        #                "RateId": "123",
                        "RoomDayRate": str(price_val),
        #                "RoomDayDescription": str(self.room_id.name),
#                            "RoomDayDescription": str(self.room_id.description_sale),
                        "CustomerFName": str(self.order_id.partner_id.name),
#                        "CustomerLName": str(self.partner_id.surname),
                        "RoomDesc": str(desc),
        #                "OccupantSmoker": "false",
        #                "OccupantNote": "Please do not put me by the elevator. Thanks!",
        #                "OccupantFName": "Tyler",
        #                "OccupantLName": "Green",
                        "Occupancy": str(occupancy),
        #                "Policy": "No smoking.",
                    }

        return vals
    