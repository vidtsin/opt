# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, api, fields, _
from odoo.exceptions import UserError , ValidationError

class peachpayment_configuration(models.Model):
    _name = 'peachpayment.configuration'
    
    user_id =  fields.Char('Login User ID')
    password =  fields.Char(string='Password')
    threeD_channel_id =  fields.Char(string='3D Channel ID')
    recurring_channel_id =  fields.Char(string='Recurring Channel Id')
    mode = fields.Selection([('test','Test'),('live','Live')],string = "Mode")
    path=fields.Char('Path')
    ip_address = fields.Char('IP Address')



peachpayment_configuration()


class PeachpaymentDetail(models.Model):
    _name = 'peachpayment.detail'


    name = fields.Char('Card Token Id')
    partner_id = fields.Many2one('res.partner','Customer Name')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    payment_ids = fields.One2many('peachpayment.detail','partner_id','Payment Details')
