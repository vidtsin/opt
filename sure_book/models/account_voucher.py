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
from odoo import models, api, fields,_
from odoo.exceptions import UserError , ValidationError
import urllib, urllib2, json
import os , sys, stat
import datetime
import math
from datetime import date, timedelta
from xml.dom.minidom import parseString
from authorized import peachpayment_configuration
import logging
_logger = logging.getLogger(__name__)



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    checkout_id = fields.Char('Checkout_id')
    payment_desc = fields.Char('Description')
    is_success = fields.Boolean('Is Success')
    is_fail = fields.Boolean('Is Fail')
    payment_brand = fields.Char('Payment Brand')
    cardlastdigit = fields.Char('Last4Digit')
    descriptor = fields.Char('Descriptor')



class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    checkout_id = fields.Char('Checkout_id')
    payment_desc = fields.Char('Description')
    is_success = fields.Boolean('Is Success')
    is_fail = fields.Boolean('Is Fail')
    payment_brand=fields.Char('Payment Brand')
    cardlastdigit= fields.Char('Last4Digit')
    descriptor = fields.Char('Descriptor')



class account_payment(models.Model):
    _inherit = "account.payment"

    create_tran = fields.Boolean('Payment Through Peach Payment')



    # Generate the checkout_id of transaction

    @api.multi
    def request(self):
        acc_inv_obj = self.env['account.invoice']
        _logger.error('========== def request==============')
        print "=============self._context==============",self._context
        if self._context.get('active_id'):
            inv_id = self._context.get('active_id')

        if self.create_tran:
            if self._context.get('active_model') == 'sale.order':
                invoice = self.env['sale.order'].browse(inv_id)
            else:
                invoice = acc_inv_obj.browse(inv_id)
            param = self.env['peachpayment.configuration']
            user_id = param.search([])[0].user_id
            password = param.search([])[0].password
            mode = param.search([])[0].mode
            threeD_channel_id = param.search([])[0].threeD_channel_id
            recurring_channel_id = param.search([])[0].recurring_channel_id
            if mode=='test':
                url='https://test.oppwa.com/v1/checkouts'
            else:
                url ='https://oppwa.com/v1/checkouts'
            resgistered_id = {}
            if invoice.partner_id.payment_ids:
                temp =0
                for pay in invoice.partner_id.payment_ids:
                    resgistered_id['registrations['+str(temp)+'].id'] =pay.name
                    temp+=1

            fraction, whole = math.modf(self.amount)
            if fraction == 0.0:
                amount = int(self.amount)
            else:
                amount = self.amount
            data = {
                'authentication.userId': user_id,
                'authentication.password': password,
                'authentication.entityId': threeD_channel_id,
                'amount': amount,
                'currency': invoice.company_id.currency_id.name,
                'paymentType': 'CD',
                'createRegistration': 'true'
            }
            data.update(resgistered_id)
            try:
                opener = urllib2.build_opener(urllib2.HTTPHandler)
                request = urllib2.Request(url, data=urllib.urlencode(data))
                request.get_method = lambda: 'POST'
                response = opener.open(request)
                return json.loads(response.read());
            except urllib2.HTTPError, e:
                return e.code;

    @api.multi
    def checkout_status(self):
        sys_parameter_obj = self.env['ir.config_parameter']
        payment_obj = self.env['peachpayment.detail']
        sys_parameter_id = sys_parameter_obj.search([('key', '=', 'web.base.url')])
        host = sys_parameter_id.value
        if self._context.get('active_id'):
            inv = self._context.get('active_id')
            if self._context.get('active_model') != 'sale.order':
                inv_id = self.env['account.invoice'].browse(inv)
            else:
                inv_id = self.env['sale.order'].browse(inv)
        if not inv_id.checkout_id:
            raise UserError(_("Please Do payment before Validate Transaction!!!!!!"))

        data =self.validate_checkout_status(inv_id.checkout_id)
        print '=======result=============',data
        if str(data) == 'HTTP Error 400: Bad Request':
            # raise UserError(_('Work order %s is still running') % wo.name)
            raise ValidationError(('Your Transaction has been Failed :  %s') % (data))
        result = data.get('result')
        card = data.get('card')
        if result.get('description'):
            des = result.get('description')
        if data.get('paymentBrand'):
            brand = data.get('paymentBrand')
        if card.get('last4Digits'):
            lastdigit =card.get('last4Digits')
        if data.get('descriptor'):
            descriptor =data.get('descriptor')
        if result.get('code') == '000.100.110':

            inv_id.write({'payment_desc':des,'is_success':True,'payment_brand':brand,'cardlastdigit':lastdigit,'descriptor':descriptor})

            if data.get('registrationId'):
                flag=False
                for pay in inv_id.partner_id.payment_ids:
                    if pay.name ==data.get('registrationId'):
                        flag = True
                if not flag:
                    vals = {
                        'name':data.get('registrationId'),
                        'partner_id':inv_id.partner_id.id
                    }
                    payment_obj.create(vals)
            url = host+'/sure_book/static/src/xml/successfull.html'
            # url = 'http://localhost:1001/sure_book/static/src/xml/successfull.html'
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'current'
            }
        else:
            inv_id.write({'checkout_id':''})
            # url = 'http://localhost:1001/sure_book/static/src/xml/transaction_rejected.html'
            url = host+'/sure_book/static/src/xml/transaction_rejected.html'
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'current'
            }



    @api.multi
    def validate_checkout_status(self,checkout_id):
        param = self.env['peachpayment.configuration']
        user_id = param.search([])[0].user_id
        password = param.search([])[0].password
        mode = param.search([])[0].mode
        threeD_channel_id = param.search([])[0].threeD_channel_id
        recurring_channel_id = param.search([])[0].recurring_channel_id
        if mode == 'test':
            url = 'https://test.oppwa.com/v1/checkouts/'
        else:
            url = 'https://oppwa.com/v1/checkouts/'
        url = url+checkout_id+"/payment"
        url += '?authentication.userId='+user_id
        url += '&authentication.password='+password
        url += '&authentication.entityId='+threeD_channel_id
        print"=========url============",url
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            request = urllib2.Request(url, data='')
            request.get_method = lambda: 'GET'
            response = opener.open(request)
            return json.loads(response.read());
        except urllib2.HTTPError, e:
            return e;

    @api.multi
    def post(self):
        sys_parameter_obj = self.env['ir.config_parameter']
        sys_parameter_id = sys_parameter_obj.search([('key','=','web.base.url')])
        host = sys_parameter_id.value
        print "==========self._context===============",self._context
        if not self.create_tran:
            print "==========not self.create_tran==============="
            return super(account_payment, self).post()

        inv = self._context.get('active_id')
        inv_id = self.env['account.invoice'].browse(inv) if self._context.get('active_model') != 'sale.order' else self.env['sale.order'].browse(inv)
        if inv_id.checkout_id and inv_id.is_success:
            print "==========inv_id.checkout_id and inv_id.is_success==============="
            return super(account_payment, self).post()

        responseData = self.request();
        _logger.error('==============responseData==============%s', responseData)
        if responseData == 400:
            raise ValidationError(('Your Transaction has been Failed :  %s') % (responseData))
        _logger.error('===========responseData==============%s',responseData)
        param = self.env['peachpayment.configuration']
        path = param.search([])[0].path
        ip_address = param.search([])[0].ip_address
        mode = param.search([])[0].mode
        if mode == 'test':
            url = 'https://test.oppwa.com/'
        else:
            url = 'https://oppwa.com/'
        print "=====================================================================",responseData
        print "==========inv_id.checkout_id===============",inv_id
        if responseData['id']:
            inv_id.write({'checkout_id':responseData['id']})
            print "=================responseData['id']===================",responseData['id']
            html_str = '''<!DOCTYPE html>
                        <html>
                        <body>
                         <form action="'''+str(host)+'''/sure_book/static/src/xml/thankyou.html" class="paymentWidgets" data-brands="VISA MASTER AMEX">
                        </form>
                        <script>
                        var wpwlOptions ={registrations: { requireCvv: true,hideInitialPaymentForms: false}}
                        </script>
                        <script src="'''+url+'''v1/paymentWidgets.js?checkoutId='''+responseData['id']+'''">
                        </script>
                        
                        </body>
                        </html>'''
            file = path + responseData['id']+".html"
            print "====file=======>",file
#            os.chmod(file, 0777)
            if not os.path.exists(path):
                print "====not exists=======>"
                os.makedirs (path)
            if os.path.exists(file):
                print "====exists=======>"
                os.remove(file)
                
            Html_file = open(file ,"w")
            print "====Html_file=======>",Html_file
            Html_file.write(html_str.encode('UTF-8'))
            Html_file.close()

            url = '/sure_book/static/src/'+ responseData['id']+".html"
            print "==============url==================", url
            res = super(account_payment, self).post()
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'current'
            }


account_payment()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: