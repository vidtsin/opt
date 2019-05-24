# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2015 - Present Teckzilla Software Solutions Pvt. Ltd. All Rights Reserved
#    Author: [Teckzilla Software Solutions]  <[sales@teckzilla.net]>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of the GNU General Public License is available at:
#    <http://www.gnu.org/licenses/gpl.html>.
#
##############################################################################


from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import requests
import sha
import binascii
import base64
from bs4 import BeautifulSoup
import time
import random
import os
import datetime

import logging
from xml.dom.minidom import parse, parseString
import xml.etree.ElementTree as ET
from pyPdf import PdfFileWriter, PdfFileReader
from tempfile import mkstemp
from datetime import timedelta



# _logger = logging.getLogger('sale')

class create_booking(models.TransientModel):
    _name='create.booking'
    
#    @api.model 
#    def _default_update_booking(self):
#        property_obj = self.env['myallocator.property']
#        updatecarrier_line_items = {}
#        list_line = []
#        for property in property_obj.browse(self._context['active_ids']):
#            property_line_items = {
#                'property_id':property.id,
#            }
#            list_line.append(property_line_items)
#        return list_line
#    
#    
#    
#    my_property_ids = fields.One2many('create.booking.base.wizard', 'bulk_property_id', string='Delivery Order For Update', default=_default_update_booking)

#    @api.multi
#    def create_property_wizard(self):
#        my_property_ids = self.my_property_ids
#        for bulk_property in my_property_ids:
#            property = bulk_property.property_id
#            if not property.is_property:
#
#                continue
#            else:
#                property_obj = self.env['myallocator.property']
#                property_obj.create_property(property)
#
#        return True
    
    @api.multi
    def create_property_wizard(self):
        property_obj = self.env['myallocator.property']
        for property in self._context['active_ids']:
            property_id = property_obj.search([('id','=',property)])
            print"------------property_id--------------",property_id
            if not property_id.is_property:

                continue
            else:
                property_obj = self.env['myallocator.property']
                property_obj.create_property(property_id)

        return True
    
    @api.multi
    def export_room_wizard(self):
        print"------------self--------------",self
        print"------------self--------------",self._context
        print"------------self--------------",self._context['active_ids']
        property_obj = self.env['myallocator.property']
        room_obj = self.env['myallocator.room.test']
        for property in self._context['active_ids']:
            property_id = property_obj.search([('id','=',property)])
            print"------------property_id--------------",property_id
            if property_id.is_property:
                rt = room_obj.create_room(property_id)
                print"------------rt--------------",rt
            else:
                continue

        return True
    
    @api.multi
    def get_channel_wizard(self):
        print"------------self--------------",self
        print"------------self--------------",self._context
        print"------------self--------------",self._context['active_ids']
        property_obj = self.env['myallocator.property']
        test_obj = self.env['myallocator.test']
        for property in self._context['active_ids']:
            property_id = property_obj.search([('id','=',property)])
            print"------------property_id--------------",property_id
            if property_id.is_property:
                rt = test_obj.create_test(property_id)
                print"------------rt--------------",rt
            else:
                continue

        return True


create_booking()

#class create_booking_base_wizard(models.TransientModel):
#    _name='create.booking.base.wizard'
#
#    property_id = fields.Many2one('myallocator.property', 'Property', required=True)
#
#    bulk_property_id =fields.Many2one('create.booking', 'Property Line Items')
#    
#    
#create_booking_base_wizard()





class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    _description = "Sales Advance Payment Invoice"
    
    
    @api.multi
    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        print"---------sale_orders--------",sale_orders

        if self.advance_payment_method == 'delivered':
            sale_orders.action_invoice_create()
            sale_orders.action_check_out()
        elif self.advance_payment_method == 'all':
            sale_orders.action_invoice_create(final=True)
            sale_orders.action_check_out()
        else:
            # Create deposit product if necessary
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.values'].sudo().set_default('sale.config.settings', 'deposit_product_id_setting', self.product_id.id)

            sale_line_obj = self.env['sale.order.line']
            for order in sale_orders:
                print"---------order--------",order
                if self.advance_payment_method == 'percentage':
                    amount = order.amount_untaxed * self.amount / 100
                else:
                    amount = self.amount
                if self.product_id.invoice_policy != 'order':
                    raise UserError(_('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(_("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                if order.fiscal_position_id and self.product_id.taxes_id:
                    tax_ids = order.fiscal_position_id.map_tax(self.product_id.taxes_id).ids
                else:
                    tax_ids = self.product_id.taxes_id.ids
                so_line = sale_line_obj.create({
                    'name': _('Advance: %s') % (time.strftime('%m %Y'),),
                    'price_unit': amount,
                    'product_uom_qty': 0.0,
                    'order_id': order.id,
                    'discount': 0.0,
                    'product_uom': self.product_id.uom_id.id,
                    'product_id': self.product_id.id,
                    'tax_id': [(6, 0, tax_ids)],
                })
                self._create_invoice(order, so_line, amount)
                sale_orders.action_check_out()
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}

    
