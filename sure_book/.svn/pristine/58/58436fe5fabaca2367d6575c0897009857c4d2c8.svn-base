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



class update_room(models.TransientModel):
    _name='update.room'
    
    @api.multi
    def update_room(self):
        print"--------self----------",self
        print"--------self----------",self._context['active_ids']
        for active in self._context['active_ids']:
            product_id = self.env['product.product'].browse(active)
            
            if product_id.product_room_ids and not product_id.room_variant_ids:
                for prod in product_id.product_room_ids:
                    vals = {
                        'property_id': prod.property_id.id,
                        'room_id': prod.room_id,
                        'product_id': prod.product_id.id,
                        'prod_id': product_id.id,
                        'private_room': prod.private_room,
                        'is_dorm': prod.is_dorm,
                        'gender': prod.gender,
                        'unit': prod.unit,
                        'occupancy': prod.occupancy,
                        'price': prod.price,
                    }
                    allocator_prod_id = self.env['myallocator.prod.test'].create(vals)
                    print"--------allocator_prod_id----------",allocator_prod_id
                    
            elif product_id.room_variant_ids:
                list = []
                not_list = []
                room_id = self.env['myallocator.room.test'].search([('product_id','=',product_id.id)])
                print"--------room_id----------",room_id
                for test in room_id:
                    room_data_id = self.env['myallocator.prod.test'].search([('property_id','=',test.property_id.id),
                                 ('room_id','=',test.room_id)])
                    
                    if not room_data_id:
                        vals = {
                            'property_id': test.property_id.id,
                            'room_id': test.room_id,
                            'product_id': test.product_id.id,
                            'prod_id': product_id.id,
                            'private_room': test.private_room,
                            'is_dorm': test.is_dorm,
                            'gender': test.gender,
                            'unit': test.unit,
                            'occupancy': test.occupancy,
                            'price': test.price,
                        }
                        
                        allocator_prod_id = self.env['myallocator.prod.test'].create(vals)
                        print"--------allocator_prod_id----1------",allocator_prod_id

        return True
    
 

