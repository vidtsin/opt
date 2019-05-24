from odoo import models,fields,api,_
import odoo.addons.decimal_precision  as dp
from odoo.exceptions import UserError
# from odoo.addons.shopify_ept.shopify import *
from .. import shopify
# from odoo.custom.shopify_ept.shopify.pyactiveresource.util import xml_to_dict
import sys
reload(sys)
sys.getdefaultencoding()
sys.path.append("/opt/odoo_10/custom_modules/shopify_ept/shopify/pyactiveresource")
from util import xml_to_dict
import time
import json
import requests
from datetime import timedelta,datetime
import logging
_logger = logging.getLogger(__name__)

class sale_order(models.Model):
    _inherit="sale.order"

    @api.one
    def _get_shopify_order_status(self):
        for order in self:
            flag=False
            for picking in order.picking_ids:
                if picking.state!='cancel':
                    flag=True
                    break
            if not flag:
                continue
            if order.picking_ids:
                order.updated_in_shopify=True
            else:
                order.updated_in_shopify=False
            for picking in order.picking_ids:
                if picking.state =='cancel':
                    continue
                if picking.picking_type_id.code!='outgoing':
                    continue
                if not picking.updated_in_shopify:
                    order.updated_in_shopify=False
                    break
    @api.multi
    @api.depends('risk_ids')
    def _check_order(self):
        for order in self:
            flag=False
            for risk in order.risk_ids:
                if risk.recommendation!='accept':
                    flag=True
                    break
            order.is_risky_order=flag
    def _search_order_ids(self,operator,value):
        query="""select stock_picking.group_id from stock_picking
                    inner join stock_picking_type on stock_picking.picking_type_id=stock_picking_type.id
                    where coalesce(updated_in_shopify,False)=%s and stock_picking_type.code='%s' and state='%s'
              """%(False,'outgoing','done')
        self._cr.execute(query)
        results = self._cr.fetchall()
        group_ids=[]
        for result_tuple in results:
            group_ids.append(result_tuple[0])
        sale_ids=self.search([('procurement_group_id','in',group_ids)])
        return [('id','in',sale_ids.ids)]


    shopify_order_id=fields.Char("Shopify Order Ref")
    shopify_order_number=fields.Char("Shopify Order Number")
    shopify_reference_id=fields.Char("Shopify Reference")
    checkout_id=fields.Char("Checkout Id")
    auto_workflow_process_id=fields.Many2one("sale.workflow.process.ept","Auto Workflow")
    updated_in_shopify=fields.Boolean("Updated In Shopify",compute=_get_shopify_order_status,search='_search_order_ids')
    shopify_instance_id=fields.Many2one("shopify.instance.ept","Instance")
    closed_at_ept=fields.Datetime("Closed At")
    risk_ids=fields.One2many("shopify.order.risk",'odoo_order_id',"Risks")
    is_risky_order=fields.Boolean("Risky Order ?",compute=_check_order,store=True)
    is_pos_order=fields.Boolean("Is POS Order ?")

    @api.multi
    def create_or_update_customer(self, vals, result, is_company=False, parent_id=False, type=False, instance=False):

        country_obj = self.env['res.country']
        state_obj = self.env['res.country.state']
        partner_obj = self.env['res.partner']

        partner_data = vals.get('default_address')
        if partner_data:
            email = vals.get('email')
            company_name = partner_data.get('company')
            if company_name:
                company_ids = partner_obj.search([('name', '=', company_name)])
                if not company_ids:
                    company_vals = {
                            'name': partner_data.get('company') or '',
                            'is_company': 'company'
                        }
                    company_ids = partner_obj.create(company_vals)

            else:
                company_ids = False

            partner_ids = partner_obj.search([('email', '=', email)])

            if not partner_ids:

                first_name = vals.get('first_name')
                last_name = vals.get('last_name')
                if not last_name:
                    name = first_name
                else:
                    name = first_name + ' ' + last_name

                phone = partner_data.get('phone')
                state_name = partner_data.get('province')
                state_code = partner_data.get('province_code')

                city = partner_data.get('city')
                zip = partner_data.get('zip')
                street = partner_data.get('address1')
                street1 = partner_data.get('address2')

                country_name = partner_data.get('country')
                country_code = partner_data.get('country_code')

                country = country_obj.search([('code', '=', country_code)])

                if not country:
                    country = country_obj.search([('name', '=', country_name)])

                if not country:
                    state = state_obj.search([('code', '=', state_code)])
                else:
                    state = state_obj.search([('code', '=', state_code), ('country_id', '=', country.id)])

                if not state:
                    if not country:
                        state = state_obj.search([('name', '=', state_name)])
                    else:
                        state = state_obj.search([('name', '=', state_name), ('country_id', '=', country.id)])

                if len(state.ids) > 1:
                    state = state_obj.search([('code', '=', state_code), ('name', '=', state_name)])

                # if not company_ids:
                #     company_vals = {
                #         'name': partner_data.get('company') or '',
                #         'is_company': 'company'
                #     }
                #     company_ids = partner_obj.create(company_vals)




                if company_ids:
                    partner_vals = {'name': name,
                                    'state_id': state.id,
                                    'city': city,
                                    'zip': zip,
                                    'street': street,
                                    'street2': street1,
                                    'country_id': country.id,
                                    'parent_id': company_ids.id,
                                    'email': email,
                                    'company_name_ept': company_name or '',
                                    'phone': phone or '',
                                    'company_type' : 'person',}

                    partner_ids = partner_obj.create(partner_vals)
                else:
                    partner_vals = {'name': name,
                                    'state_id': state.id,
                                    'city': city,
                                    'zip': zip,
                                    'street': street,
                                    'street2': street1,
                                    'country_id': country.id,
                                    'email': email,
                                    'phone': phone or '',
                                    'company_type': 'person', }

                    partner_ids = partner_obj.create(partner_vals)


        else:
            email = vals.get('email')
            partner_ids = partner_obj.search([('email', '=', email)])

            first_name = vals.get('first_name')
            last_name = vals.get('last_name')
            if not last_name:
                name = first_name
            else:
                name = first_name + ' ' + last_name
            print "-----first_name-----" , first_name
            print "-----last_name-----" , last_name


            if not partner_ids:
                partner_vals = {
                    'name': name,
                    'company_type': 'person',
                    'email': email,
                }

                partner_ids = partner_obj.create(partner_vals)
            else:
                partner_vals = {
                    'name': name,
                    'company_type': 'person',
                    'email': email,
                }

                partner_ids = partner_ids.write(partner_vals)






        return partner_ids



    @api.model
    def createAccountTax(self,value,price_included,company,title):
        accounttax_obj = self.env['account.tax']

        if price_included:
            name='%s_(%s %s included)_%s'%(title,str(value),'%',company.name)
        else:
            name='%s_(%s %s excluded)_%s'%(title,str(value),'%',company.name)

        accounttax_id = accounttax_obj.create({'name':name,'amount':float(value),'type_tax_use':'sale','price_include':price_included,'company_id':company.id})

        return accounttax_id

    @api.model
    def get_tax_id_ept(self,instance,order_line,tax_included):
        tax_id=[]
        taxes=[]
        for tax in order_line:
            rate=float(tax.get('rate',0.0))
            rate = rate*100
            if rate!=0.0:
                acctax_id = self.env['account.tax'].search([('price_include','=',tax_included),('type_tax_use', '=', 'sale'), ('amount', '=', rate),('company_id','=',instance.warehouse_id.company_id.id)])
                if not acctax_id:
                    acctax_id = self.createAccountTax(rate,tax_included,instance.warehouse_id.company_id,tax.get('title'))
                    if acctax_id:
                        transaction_log_obj=self.env["shopify.transaction.log"]
                        message="""Tax was not found in ERP ||
                        Automatic Created Tax,%s ||
                        tax rate  %s ||
                        Company %s"""%(acctax_id.name,rate,instance.company_id.name)
                        transaction_log_obj.create(
                                                    {'message':message,
                                                     'mismatch_details':True,
                                                     'type':'sales',
                                                     'shopify_instance_id':instance.id
                                                    })
                if acctax_id:
                    taxes.append(acctax_id.id)
        if taxes:
            tax_id = [(6, 0, taxes)]

        return tax_id


    @api.model
    def check_mismatch_details(self,lines,instance,order_number):
        transaction_log_obj=self.env["shopify.transaction.log"]
        odoo_product_obj=self.env['product.product']
        shopify_product_obj=self.env['shopify.product.product.ept']
        mismatch=False
        for line in lines:
            barcode=0
            odoo_product=False
            shopify_variant=False
            if line.get('variant_id',None):
                shopify_variant=shopify_product_obj.search([('variant_id','=',line.get('variant_id')),('shopify_instance_id','=',instance.id)])
                if shopify_variant:
                    continue
                try:
                    shopify_variant=shopify.Variant().find(line.get('variant_id'))
                except:
                    shopify_variant=False
                    message="Variant Id %s not found in shopify || default_code %s || order ref %s"%(line.get('variant_id',None),line.get('sku'),order_number)
                    log=transaction_log_obj.search([('shopify_instance_id','=',instance.id),('message','=',message)])
                    if not log:
                        transaction_log_obj.create(
                                                    {'message':message,
                                                     'mismatch_details':True,
                                                     'type':'sales',
                                                     'shopify_instance_id':instance.id
                                                    })

                if shopify_variant:
                    shopify_variant=shopify_variant.to_dict()
                    barcode=shopify_variant.get('barcode')
                else:
                    barcode=0
            sku=line.get('sku')
            shopify_variant=barcode and shopify_product_obj.search([('product_id.barcode','=',barcode),('shopify_instance_id','=',instance.id)])
            if not shopify_variant:
                odoo_product=barcode and odoo_product_obj.search([('barcode','=',barcode)]) or False
            if not odoo_product and not shopify_variant:
                shopify_variant=sku and shopify_product_obj.search([('default_code','=',sku),('shopify_instance_id','=',instance.id)])
                if not shopify_variant:
                    odoo_product=sku and odoo_product_obj.search([('default_code','=',sku)])

            if not shopify_variant and not odoo_product:
                message="%s Product Code Not found for order %s"%(sku,order_number)
                log=transaction_log_obj.search([('shopify_instance_id','=',instance.id),('message','=',message)])
                if not log:
                    transaction_log_obj.create(
                                                {'message':message,
                                                 'mismatch_details':True,
                                                 'type':'sales',
                                                 'shopify_instance_id':instance.id
                                                })
                mismatch=True
                break
        return mismatch

    @api.model
    def create_sale_order_line(self,line,tax_ids,product,quantity,fiscal_position,partner,pricelist_id,name,order,price,is_shipping=False):
        sale_order_line_obj=self.env['sale.order.line']
        uom_id=product and product.uom_id and product.uom_id.id or False

        new_record = sale_order_line_obj.new({
                                                'product_id':product and product.ids[0] or False,
                                                'order_id':order.id,
                                                'company_id':order.company_id.id,
                                                'product_uom':uom_id,
                                                'name':name
                                            })
        new_record.product_id_change()
        product_data = sale_order_line_obj._convert_to_write(new_record._cache)

        product_data.update(
                            {
                            'order_id':order.id,
                            'product_uom_qty':quantity,
                            'price_unit':price,
                            'shopify_line_id':line.get('id'),
                            'tax_id':tax_ids,
                            'is_delivery':is_shipping
                            }
                            )
        order_line=sale_order_line_obj.create(product_data)

        return order_line

    @api.model
    def create_or_update_product(self,line,instance):
        shopify_product_tmpl_obj=self.env['shopify.product.template.ept']
        shopify_product_obj=self.env['shopify.product.product.ept']
        variant_id=line.get('variant_id')
        shopify_product=False
        if variant_id:
            shopify_product=shopify_product_obj.search([('shopify_instance_id','=',instance.id),('variant_id','=',variant_id)])
            if shopify_product:
                return shopify_product
            shopify_product=shopify_product_obj.search([('shopify_instance_id','=',instance.id),('default_code','=',line.get('sku'))])
            shopify_product and shopify_product.write({'variant_id':variant_id})
            if shopify_product:
                return shopify_product
            shopify_product_tmpl_obj.sync_products(instance,line.get('product_id'),update_templates=True)
            shopify_product=shopify_product_obj.search([('shopify_instance_id','=',instance.id),('variant_id','=',variant_id)])
        else:
            shopify_product=shopify_product_obj.search([('shopify_instance_id','=',instance.id),('default_code','=',line.get('sku'))])
            if shopify_product:
                return shopify_product
        return shopify_product

    @api.model
    def create_order(self,result,instance,is_pos):

        workflow_config = self.env['sale.auto.workflow.configuration'].search([('shopify_instance_id', '=', instance.id)])
        # workflow_config = self.env['sale.auto.workflow.configuration'].search([('shopify_instance_id', '=', instance)])
        workflow = workflow_config and workflow_config.auto_workflow_id or False
        if workflow:
            workflow = workflow.id,
        _logger.info("--------workflow-------: %s", workflow)
        partner_obj = self.env['res.partner']
        orderline_obj = self.env['sale.order.line']
        product_obj = self.env['product.product']
        product_template_obj = self.env['product.template']
        product_uom_obj = self.env['product.uom']
        transaction_log_obj = self.env["shopify.transaction.log"]

        tax_obj = self.env['account.tax']
        uom_obj = self.env['product.uom']


        customer = result.get('customer')
        if customer:
        #     _logger.info("-------------customer-----------: %s", customer)
            partner_id = self.get_customer(customer)
        else:
            partner_id = partner_obj.search([('name', '=', 'Guest User'), ('shopify_customer_id', '=', 'Guest User')])
            if not partner_id:
                partner_vals = {'name': 'Guest User',
                                'email': '',
                                'phone': '',
                                'shopify_customer_id': 'Guest User',
                                'customer': True,
                                }
                _logger.info("-------------partner_vals-----------: %s", partner_vals)
                partner_id = partner_obj.create(partner_vals)
                _logger.info("-------------partner_id-----------: %s", partner_id)


        # first_name = customer.get('first_name')
        # last_name = customer.get('last_name')
        # last_order_name= customer.get('last_order_name')
        # last_order_id = customer.get('last_order_id')
        # email = result.get('email')
        # if not last_name:
        #     name = first_name
        # else:
        #     name = first_name + ' ' + last_name
        # total_line_items_price = result.get('total_line_items_price')
        created_at = result.get('created_at')

        shipping_address = result.get('shipping_address')

        # customer_id = partner_obj.search([('name','=',name),('email', '=', email)])
        shopify_id= result.get('id')
        shopify_name = result.get('name')
        order = self.search([('shopify_order_number', '=', result.get('name')), ('shopify_order_id', '=', result.get('id'))])

        if not order:
            sale_order_vals = {
                'partner_id' : partner_id.id,
                'date_order' : created_at,
                'picking_policy' : 'direct',
                'shopify_order_id' : shopify_id,
                'shopify_order_number' : shopify_name,
                'shopify_instance_id': instance.id,
                # 'shopify_instance_id': instance,
                'auto_workflow_process_id': workflow,
                'is_pos_order': is_pos,
                # 'unique_sales_rec_no': last_order_name,
            }
            _logger.info("----sale_order_vals----: %s", sale_order_vals)
            order = self.create(sale_order_vals)
            _logger.info("----order--create_order--: %s", order)

            line_items = result['line_items']
            for items in line_items:
                price = items.get('price')
                quantity = items.get('quantity')
                title = items.get('title')
                sku = items.get('sku')
                shopify_line_id = items.get('id')
                if not sku:
                    continue
                if 'grams' in items:
                    product_uom_id = product_uom_obj.search([('name', '=', 'g')])

                if not items.get('product_id') and not items.get('variant_id'):
                    message = "Line Items Not Having Product ID and Variant ID In %s Order and Order ID %s" % (result.get('order_number'), shopify_id)
                    log = transaction_log_obj.search([('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                    if not log:
                        transaction_log_obj.create(
                            {'message': message,
                             'mismatch_details': True,
                             'type': 'sales',
                             'shopify_instance_id': instance.id
                             })
                    continue

                product_template_id = product_template_obj.search([('shopify_product_id', '=', items.get('product_id')),
                                                                    ('shopify_variant_id', '=', items.get('variant_id'))])
                taxes_list = []
                tax_lines = items.get('tax_lines')
                for tax_line in tax_lines:
                    if tax_line:
                        account_tax_id = self.get_taxes(tax_line)
                        taxes_list.append(account_tax_id.id)
                if not product_template_id:
                    # taxes_list = []
                    # for tax_line in tax_lines:
                    #     if tax_line:
                    #         account_tax_id = self.get_taxes(tax_line)
                    #         taxes_list.append(account_tax_id.id)
                    product_vals = {'uom_id': product_uom_id.id,
                                    'uom_po_id': product_uom_id.id,
                                    'categ_id': 1,
                                    'name': items.get('name'),
                                    'type': 'product',
                                    # 'tracking': 1,
                                    'shopify_product_id': items.get('product_id'),
                                    'shopify_variant_id': items.get('variant_id'),
                                    'list_price': items.get('price'),
                                    'default_code': items.get('sku'),
                                    'taxes_id': [(6, 0, taxes_list)],
                                    }
                    product_template_id = product_template_obj.create(product_vals)

                product_product_id = product_obj.search([('product_tmpl_id', '=', product_template_id.id)])
                order_line_vals = {
                    'product_id': product_product_id.id,
                    'name': product_product_id.name,
                    'product_uom_qty': quantity,
                    'product_uom': product_uom_id.id,
                    'customer_lead': 1,
                    'price_unit': price,
                    'tax_id': [(6,0,taxes_list)],
                    'order_id': order.id,
                    'shopify_line_id': shopify_line_id
                    }
                products = orderline_obj.create(order_line_vals)
            if result['shipping_lines']:
                self.create_shipping_line(result,order)

        return order

    @api.model
    def create_shipping_line(self, result,order):
        product_template_obj = self.env['product.template']
        product_obj = self.env['product.product']
        product_uom_obj = self.env['product.uom']
        orderline_obj = self.env['sale.order.line']
        product_uom_id = product_uom_obj.search([('name', '=', 'Unit(s)')])
        for shipping_line in result['shipping_lines']:
            product_template_id = product_template_obj.search([('name', '=', 'Shipping & Handling')])
            if not product_template_id:
                product_vals = {'uom_id': product_uom_id.id,
                                'uom_po_id': product_uom_id.id,
                                'categ_id': 1,
                                'name': 'Shipping & Handling',
                                'type': 'service',
                                # 'tracking': 1,
                                'list_price': shipping_line.get('price'),
                                'description_sale': shipping_line.get('title'),
                                }
                product_template_id = product_template_obj.create(product_vals)
            else:
                product_vals = {'list_price': shipping_line.get('price'),
                                'description_sale': shipping_line.get('title'),
                                }
                product_template_id.write(product_vals)
            product_product_id = product_obj.search([('product_tmpl_id', '=', product_template_id.id)])
            order_line_vals = {
                'product_id': product_product_id.id,
                'name': product_product_id.name,
                'product_uom_qty': 1,
                'product_uom': product_uom_id.id,
                'customer_lead': 1,
                'price_unit': shipping_line.get('price'),
                'order_id': order.id,
            }
            products = orderline_obj.create(order_line_vals)
        return True


    @api.model
    def create_order_product(self, result,items):
        product_tmpl_obj = self.env['product.template']
        product_obj = self.env['product.product']

        product_uom_obj = self.env['product.uom']
        print "=======result===================",result
        print "============items==============",items
        barcode = False
        product_name = items.get('name')
        sku = items.get('sku')
        price = items.get('price')
        grams_weight = items.get('grams')
        grams_weight = grams_weight * 0.001

        product_uom_id = product_uom_obj.search([('name', '=', 'g')])
        variant_id = items.get('variant_id')
        shopify_product_id = items.get('product_id')
        vals = {
            'name': product_name,
            'type': 'product',
            'default_code': sku,
            'barcode': barcode,
            'list_price': price,
            'weight' : grams_weight,
            'uom_id': product_uom_id.id,
            'uom_po_id': product_uom_id.id,
            'categ_id': 1,
            'shopify_product_id': shopify_product_id,
            'shopify_variant_id': variant_id,

        }
        product_id = product_tmpl_obj.create(vals)
        # self._cr.commit()
        product_id = product_obj.search([('product_tmpl_id', '=', product_id.id)])

        print"======product_id==============",product_id
        return product_id
    @api.model
    def check_fulfilled_or_not(self,result):
        fulfilled=True
        for line in result.get('line_items'):
            if not line.get('fulfillment_status'):
                fulfilled=False
                break
        return fulfilled

    @api.multi
    def list_all_orders(self,result):
        sum_of_result=result
        if not sum_of_result:
            return sum_of_result
        order_ids=[result_id.id for result_id in result]
        since_id=max(order_ids)
        new_result=shopify.Order().find(status='any',limit=250,since_id=since_id)
        while new_result:
            order_ids=[result_id.id for result_id in new_result]
            since_id=max(order_ids)
            sum_of_result=sum_of_result+new_result
            new_result=shopify.Order().find(status='any',limit=250,since_id=since_id)
        return sum_of_result

    @api.model
    def auto_import_sale_order_ept(self):
        shopify_instance_obj=self.env['shopify.instance.ept']
        ctx = dict(self._context) or {}
        shopify_instance_id = ctx.get('shopify_instance_id',False)
        if shopify_instance_id:
            instance=shopify_instance_obj.search([('id','=',shopify_instance_id)])
            self.import_shopify_orders(instance)
        else:
            instances = shopify_instance_obj.search([])
            for instance in instances:
                self.import_shopify_orders(instance)
        return True

    @api.model
    def get_customer(self, customer):
        partner_obj = self.env['res.partner']
        first_name = customer.get('first_name') or ''
        last_name = customer.get('last_name')
        if last_name:
            first_name = first_name + ' ' + last_name
        _logger.info("-------------first_name-----------: %s", first_name)
        partner_id = partner_obj.search([('name', '=', first_name), ('shopify_customer_id', '=', customer.get('id'))])
        _logger.info("-------------partner_id-----------: %s", partner_id)
        if not partner_id:
            partner_vals = {'name': first_name,
                            'email': customer.get('email'),
                            'phone': customer.get('phone'),
                            'shopify_customer_id': customer.get('id'),
                            'customer': True,
                            }
            _logger.info("-------------partner_vals-----------: %s", partner_vals)
            partner_id = partner_obj.create(partner_vals)
            _logger.info("-------------partner_id-----------: %s", partner_id)
        return partner_id

    @api.model
    def get_taxes(self, tax_line):
        account_tax_obj = self.env['account.tax']
        account_tax_id = account_tax_obj.search([('name', '=', tax_line.get('title'))])
        if not account_tax_id:
            tax_rate = float(tax_line.get('rate')) * 100
            tax_vals = {'name': tax_line.get('title'),
                        'type_tax_use': 'sale',
                        'amount_type': 'percent',
                        'amount': tax_rate}
            account_tax_id = account_tax_obj.create(tax_vals)
        return account_tax_id

    @api.model
    def create_pos_order(self, result,pos_session_id):
        product_template_obj = self.env['product.template']
        product_product_obj = self.env['product.product']
        pos_order_obj = self.env['pos.order']

        pos_order_line_obj = self.env['pos.order.line']
        product_uom_obj = self.env['product.uom']

        partner_id = None
        # result = {'subtotal_price': '9.99',
        #         'buyer_accepts_marketing': True,
        #         'reference': None,
        #         'shipping_lines': [],
        #         'cart_token': None,
        #         'updated_at': '2017-04-03T18:12:26-07:00',
        #         'taxes_included': False,
        #         'currency': 'USD',
        #         'discount_codes': [],
        #         'financial_status': 'paid',
        #         'source_name': 'pos',
        #         'closed_at': None,
        #         'processed_at': '2017-04-03T18:12:24-07:00',
        #         'payment_gateway_names': ['store-credit'],
        #         'location_id': 7027718,
        #         'gateway': 'store-credit',
        #         'confirmed': True,
        #         'user_id': 61379718,
        #         'fulfillments':
        #             [{'status': 'success',
        #             'line_items':
        #                 [{'requires_shipping': True,
        #                 'variant_id': 11554068422,
        #                 'id': 11045240908,
        #                 'product_exists': True,
        #                 'sku': 'SSF-212',
        #                 'title': '1/4" MJIC x 1/2" MNPT- Pack of 2',
        #                 'name': '1/4" MJIC x 1/2" MNPT- Pack of 2',
        #                 'fulfillment_service': 'manual',
        #                 'total_discount': '0.00',
        #                 'variant_title': None,
        #                 'vendor': 'Xtractor Depot',
        #                 'tax_lines':
        #                     [{'price': '0.72','rate': '0.0725','title': 'CA State Tax'},
        #                     {'price': '0.05', 'rate': '0.005', 'title': 'San Bernardino County Tax'},
        #                     {'price': '0.02', 'rate': '0.0025', 'title': 'San Bernardino Municipal Tax'}],
        #                 'price': '9.99',
        #                 'taxable': True,
        #                 'properties': [],
        #                 'grams': 105,
        #                 'fulfillable_quantity': 0,
        #                 'product_id': 3960171782,
        #                 'gift_card': False,
        #                 'fulfillment_status': 'fulfilled',
        #                 'variant_inventory_management': 'shopify',
        #                 'quantity': 1}],
        #             'service': 'manual',
        #             'created_at': '2017-04-03T18:12:25-07:00',
        #             'receipt': None,
        #             'shipment_status': None,
        #             'tracking_urls': [],
        #             'tracking_url': None,
        #             'updated_at': '2017-04-03T18:12:25-07:00',
        #             'tracking_number': None,
        #             'tracking_numbers': [],
        #             'tracking_company': None,
        #             'id': 4668443212}],
        #         'landing_site_ref': None,
        #         'token': '3b1777ac78232a78e48117b1f4ca96ee',
        #         'source_identifier': '7027718-2-2273',
        #         'id': 5461312972,
        #         'note': None,
        #         'landing_site': None,
        #         'browser_ip': None,
        #         'total_line_items_price': '9.99',
        #         'cancelled_at': None,
        #         'test': False,
        #         'email': None,
        #         'total_tax': '0.79',
        #         'cancel_reason': None,
        #         'tax_lines': [{'price': '0.72', 'rate': '0.0725', 'title': 'CA State Tax'},
        #                 {'price': '0.05', 'rate': '0.005', 'title': 'San Bernardino County Tax'},
        #                 {'price': '0.02', 'rate': '0.0025', 'title': 'San Bernardino Municipal Tax'}],
        #         'tags': None,
        #         'source_url': None,
        #         'total_discounts': '0.00',
        #         'number': 6691,
        #         'checkout_id': None,
        #         'processing_method': None,
        #         'device_id': 2,
        #         'customer': {'total_spent': '88.53',
        #                 'first_name': 'Jay',
        #                 'last_name': None,
        #                 'last_order_name': '#2-2273',
        #                 'orders_count': 2,
        #                 'created_at': '2017-03-08T15:46:16-08:00',
        #                 'tags': None,
        #                 'updated_at': '2017-04-03T18:12:25-07:00',
        #                 'email': None,
        #                 'note': None,
        #                 'phone': None,
        #                 'state': 'disabled',
        #                 'multipass_identifier': None,
        #                 'tax_exempt': False,
        #                 'accepts_marketing': True,
        #                 'id': 5872723276,
        #                 'last_order_id': 5461312972,
        #                 'verified_email': False},
        #         'line_items':
        #             [{'requires_shipping': True,
        #                 'variant_id': 11554068422,
        #                 'id': 11045240908,
        #                 'product_exists': True,
        #                 'sku': 'SSF-212',
        #                 'title': '1/4" MJIC x 1/2" MNPT- Pack of 2',
        #                 'name': '1/4" MJIC x 1/2" MNPT- Pack of 2',
        #                 'fulfillment_service': 'manual',
        #                 'total_discount': '0.00',
        #                 'variant_title': None,
        #                 'vendor': 'Xtractor Depot',
        #                 'tax_lines':
        #                     [{'price': '0.72', 'rate': '0.0725', 'title': 'CA State Tax'},
        #                     {'price': '0.05', 'rate': '0.005', 'title': 'San Bernardino County Tax'},
        #                     {'price': '0.02', 'rate': '0.0025', 'title': 'San Bernardino Municipal Tax'}],
        #                 'price': '9.99',
        #                 'taxable': True,
        #                 'properties': [],
        #                 'grams': 105,
        #                 'fulfillable_quantity': 0,
        #                 'product_id': 3960171782,
        #                 'gift_card': False,
        #                 'fulfillment_status': 'fulfilled',
        #                 'variant_inventory_management': 'shopify',
        #                 'quantity': 1}],
        #         'total_price': '10.78',
        #         'name': '#2-2273',
        #         'refunds': [],
        #         'checkout_token': None,
        #         'created_at': '2017-04-03T18:12:25-07:00',
        #         'note_attributes': [],
        #         'fulfillment_status': 'fulfilled',
        #         'total_price_usd': '10.78',
        #         'referring_site': None,
        #         'contact_email': None,
        #         'order_status_url': None,
        #         'order_number': 7691,
        #         'total_weight': 105}
        _logger.info("-------------result-----------: %s", len(result))
        customer = result.get('customer')
        if customer:
            _logger.info("-------------customer-----------: %s", customer)
            partner_id = self.get_customer(customer)
            # first_name = customer.get('first_name') or ''
            # last_name = customer.get('last_name')
            # if last_name:
            #     first_name = first_name +' '+ last_name
            # _logger.info("-------------first_name-----------: %s", first_name)
            # partner_id = partner_obj.search([('name','=',first_name),('shopify_customer_id','=',customer.get('id'))])
            # _logger.info("-------------partner_id-----------: %s", partner_id)
            # if not partner_id:
            #     partner_vals = {'name': first_name,
            #                     'email': customer.get('email'),
            #                     'phone': customer.get('phone'),
            #                     'shopify_customer_id': customer.get('id'),
            #                     'customer': True,
            #                 }
            #     _logger.info("-------------partner_vals-----------: %s", partner_vals)
            #     partner_id = partner_obj.create(partner_vals)
            #     _logger.info("-------------partner_id-----------: %s", partner_id)
            partner_id = partner_id.id
        pos_order_id = pos_order_obj.search([('shopify_name', '=', result.get('name')),('shopify_id', '=', result.get('id'))])
        if not pos_order_id:
            pos_vals = {'session_id':pos_session_id[0].id,
                        'partner_id':partner_id, #POS can be made without customer
                        'company_id':1,
                        'pricelist_id':1,
                        'name':'/',
                        'shopify_name':result.get('name'),
                        'shopify_id':result.get('id'),
                        }
            _logger.info("-------------pos_vals-----------: %s", pos_vals)
            pos_order_id = pos_order_obj.create(pos_vals)
            _logger.info("-------------pos_order_id-----------: %s", pos_order_id)
            if pos_order_id:
                line_items = result.get('line_items')
                for line_item in line_items:
                    product_template_id = product_template_obj.search([('shopify_product_id', '=', line_item.get('product_id')),
                                                                       ('shopify_variant_id', '=', line_item.get('variant_id'))])
                    taxes_list = []
                    if not product_template_id:
                        if 'grams' in line_item:
                            product_uom_id = product_uom_obj.search([('name','=','g')])

                        for tax_line in line_item.get('tax_lines'):
                            if tax_line:
                                account_tax_id = self.get_taxes(tax_line)
                            # account_tax_id = account_tax_obj.search([('name','=',tax_line.get('title'))])
                            # if not account_tax_id:
                            #     tax_rate = tax_line.get('rate')*100
                            #     tax_vals = {'name':tax_line.get('title'),
                            #                 'type_tax_use':'sale',
                            #                 'amount_type':'percent',
                            #                 'amount':tax_rate}
                            #     account_tax_id = account_tax_obj.create(tax_vals)
                            taxes_list.append(account_tax_id.id)
                        product_vals = {'uom_id':product_uom_id.id,
                                        'uom_po_id': product_uom_id.id,
                                        'categ_id': 1,
                                        'name': line_item.get('name'),
                                        'type': 'product',
                                        # 'tracking': 1,
                                        'shopify_product_id' : line_item.get('product_id'),
                                        'shopify_variant_id' : line_item.get('variant_id'),
                                        'list_price' : line_item.get('price'),
                                        'default_code':line_item.get('sku'),
                                        'taxes_id':[(6,0,taxes_list)],
                                        }
                        product_template_id = product_template_obj.create(product_vals)
                    _logger.info("-------------product_template_id-----------: %s", product_template_id)
                    product_product_id = product_product_obj.search([('product_tmpl_id','=',product_template_id.id)])
                    pos_line_vals = {'company_id': 1,
                                'name': product_template_id.name,
                                'product_id': product_product_id.id,
                                'qty': line_item.get('quantity'),
                                'price_unit': line_item.get('price'),
                                'discount': line_item.get('total_discount'),
                                'tax_ids': [(6,0,taxes_list)],
                                'order_id': pos_order_id.id,
                                'company_id': 1,
                            }
                pos_order_line_obj.create(pos_line_vals)
        return True

    @api.model
    def import_shopify_orders(self,instance=False):
        order_risk_obj=self.env['shopify.order.risk']
        pos_session_obj = self.env['pos.session']
        instances=[]
        # result=[]
        count_id = 1
        if not instance:
            instances=self.env['shopify.instance.ept'].search([('order_auto_import','=',True),('state','=','confirmed')])
        else:
            instances.append(instance)
        for instance in instances:
            instance.connect_in_shopify()
            try:
                shop = instance.host.split("//")
                shop_url =  "https://" + instance.api_key + ":" + instance.password + "@" + shop[0] + "/admin/orders/count.json"
                print "------shop_url-----" , shop_url
                order_count = requests.get(shop_url)
                total_order_count = json.loads(order_count.text)
                total_records = total_order_count.get('count')
                pages = total_records / 250
                print "---------" , total_order_count
                print "---pages------" , pages
                counter = 1
                order_ids = []
                # while counter<=pages:
                while len(order_ids)<=total_records:
                    order_id = shopify.Order().find(status='any', limit=250, page=counter)
                    print "---order_ids----", order_ids, type(order_ids)
                    order_ids += order_id
                    counter += 1
                print "---order_ids--22--", order_ids, type(order_ids)
            except Exception,e:
                raise Warning(e)
            # if len(order_ids)>=50:
            #     print "---len(order_ids)----" , len(order_ids)
            #     order_ids=self.list_all_orders(order_ids)
            import_order_ids=[]
            transaction_log_obj=self.env["shopify.transaction.log"]

            # pooling obj of customer
            # order_ids = [order.id for order in order_ids]
            # order_ids_setted = set(order_ids)
            # print "------order_ids_setted--------" , order_ids_setted , len(order_ids_setted)
            # result_list = []
            # for order_id in order_ids:
            #     result=xml_to_dict(order_id.to_xml())
            #     result=result.get('order')
            #     result_list.append(result)
            # print "-------",result_list
            # print "-------",len(result_list)

            is_pos = False
            for order_id in order_ids:
                result=xml_to_dict(order_id.to_xml())
                result=result.get('order')

                _logger.info("----------count_id-----: %s", count_id)
                count_id += 1

                _logger.info("-------------result-----------: %s", result)
                _logger.info("-------------result-----------: %s", result.get('source_name'))
                if result.get('source_name') == 'pos':
                    # is_pos = True
                    continue
                else:
                    is_pos = False
                #     pos_session_id = pos_session_obj.search([('state', '=', 'opened')])
                #     if pos_session_id:
                #         self.create_pos_order(result,pos_session_id)
                #     continue


                # if self.check_fulfilled_or_not(result):
                #     continue

                if self.search([('shopify_order_id','=',result.get('id')),('shopify_order_number','=',result.get('order_number'))]):
                    continue

                if len(result['line_items']) == 1:
                    for items in result['line_items']:
                        if not items.get('product_id') and not items.get('variant_id'):
                            message = "Line Items are Not Available In %s Order and Order ID %s" % (result.get('order_number'), result.get('id'))
                            log = transaction_log_obj.search([('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                            if not log:
                                transaction_log_obj.create(
                                    {'message': message,
                                     'mismatch_details': True,
                                     'type': 'sales',
                                     'shopify_instance_id': instance.id
                                     })
                            continue

                if not result.get('customer') and result.get('source_name') != 'pos':
                    message = "Customer Not Available In %s Order" % (result.get('order_number'))
                    log = transaction_log_obj.search(
                        [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                    if not log:
                        transaction_log_obj.create(
                            {'message': message,
                             'mismatch_details': True,
                             'type': 'sales',
                             'shopify_instance_id': instance.id
                             })
                    continue
                customer = result.get('customer')
                if customer:
                    if not customer.get('email') and result.get('source_name') != 'pos':
                        message = "Customer Not Having Email ID In %s Order" % (result.get('order_number'))
                        log = transaction_log_obj.search(
                            [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                        if not log:
                            transaction_log_obj.create(
                                {'message': message,
                                 'mismatch_details': True,
                                 'type': 'sales',
                                 'shopify_instance_id': instance.id
                                 })
                        continue

                # partner=result.get('customer',{}) and self.create_or_update_customer(result.get('customer',{}),result,False,False,False,instance) or False

                order = self.create_order(result,instance,is_pos)
                _logger.info("-------------order-----------: %s", order)
                if order:
                    import_order_ids.append(order.id)
            if import_order_ids:
                _logger.info("-------------import_order_ids-----------: %s", import_order_ids)
                self.env['sale.workflow.process.ept'].auto_workflow_process(ids=import_order_ids)


        return True

    @api.model
    def closed_at(self,instances):
        for instance in instances:
            if not instance.auto_closed_order: 
                continue
            sales_orders = self.search([('warehouse_id','=',instance.warehouse_id.id),
                                        ('shopify_order_id','!=',False),
                                        ('shopify_instance_id','=',instance.id),
                                        ('state','=','done'),('closed_at_ept','=',False)],order='date_order')

            instance.connect_in_shopify()

            for sale_order in sales_orders:
                order = shopify.Order.find(sale_order.shopify_order_id)
                order.close()
                sale_order.write({'closed_at_ept':datetime.now() })
        return True

    @api.model
    def auto_update_order_status_ept(self):
        shopify_instance_obj=self.env['shopify.instance.ept']
        ctx = dict(self._context) or {}
        shopify_instance_id = ctx.get('shopify_instance_id',False)
        if shopify_instance_id:
            instance=shopify_instance_obj.search([('id','=',shopify_instance_id)])
            self.update_order_status(instance)
        return True
    
    @api.model
    def update_order_status(self,instance):
        instances=[]
        if not instance:
            instances=self.env['shopify.instance.ept'].search([('order_auto_import','=',True),('state','=','confirmed')])
        else:
            instances.append(instance)
        for instance in instances:
            instance.connect_in_shopify()    
            sales_orders = self.search([('warehouse_id','=',instance.warehouse_id.id),
                                                         ('shopify_order_id','!=',False),
                                                         ('shopify_instance_id','=',instance.id),
                                                          ],order='date_order')
            # ('updated_in_shopify', '=', False)
            
            for sale_order in sales_orders:
                order = shopify.Order.find(sale_order.shopify_order_id)
                print "========order=====",order
                for picking in sale_order.picking_ids:
                    """Here We Take only done picking and  updated in shopify false"""
                    updated_in_shopify = picking.updated_in_shopify
                    if picking.updated_in_shopify or picking.state =='done':
                        continue                    
                    if not picking.carrier_tracking_ref:
                        continue
                    line_items={}
                    list_of_tracking_number=[]
                    tracking_numbers=[]
                    carrier_name1 = picking.carrier_id

                    carrier_name=picking.carrier_id and picking.carrier_id.shopify_code  or ''   
                    if not carrier_name:
                        carrier_name=picking.carrier_id and picking.carrier_id.name or ''                                           
                    
                    
                
                    for move in picking.move_lines:
                        if move.procurement_id and move.procurement_id.sale_line_id and move.procurement_id.sale_line_id.shopify_line_id:
                            shopify_line_id=move.procurement_id.sale_line_id.shopify_line_id
                            
                        """Create Package for the each parcel"""
                        for operation_link in move.linked_move_operation_ids:
                            if operation_link.operation_id:
                                tracking_no=False
                                if sale_order.shopify_instance_id.multiple_tracking_number:                                        
                                    if (operation_link.operation_id.result_package_id and operation_link.operation_id.result_package_id.tracking_no):  
                                        tracking_no=operation_link.operation_id.result_package_id.tracking_no
                                    if (operation_link.operation_id.package_id and operation_link.operation_id.package_id.tracking_no):  
                                        tracking_no=operation_link.operation_id.package_id.tracking_no
                                else:
                                    tracking_no = picking.carrier_tracking_ref or False
                                
                                if not tracking_no:
                                    continue
                                list_of_tracking_number.append(tracking_no)
                                product_qty=operation_link.qty or 0.0
                                product_qty=int(product_qty)
                                if line_items.has_key(shopify_line_id):
                                    if line_items.get(shopify_line_id).has_key('tracking_no'):
                                        quantity=line_items.get(shopify_line_id).get('quantity')
                                        quantity=quantity+product_qty                                
                                        line_items.get(shopify_line_id).update({'quantity':quantity})                                    
                                        if tracking_no not in line_items.get(shopify_line_id).get('tracking_no'):
                                            line_items.get(shopify_line_id).get('tracking_no').append(tracking_no)
                                    else:
                                        line_items.get(shopify_line_id).update({'tracking_no':[]})
                                        line_items.get(shopify_line_id).update({'quantity':product_qty})                                    
                                        line_items.get(shopify_line_id).get('tracking_no').append(tracking_no)                                    
                                else:
                                    line_items.update({shopify_line_id:{}})
                                    line_items.get(shopify_line_id).update({'tracking_no':[]})
                                    line_items.get(shopify_line_id).update({'quantity':product_qty})                                    
                                    line_items.get(shopify_line_id).get('tracking_no').append(tracking_no)                                    
    
                    
                    update_lines=[]

                    for sale_line_id in line_items:
                        tracking_numbers+=line_items.get(sale_line_id).get('tracking_no')

                        update_lines.append({'id':int(sale_line_id),'quantity':line_items.get(sale_line_id).get('quantity')})

                    try:

                        new_fulfillment = shopify.Fulfillment({'order_id':order.id,'tracking_numbers':list(set(tracking_numbers)),'tracking_company':carrier_name,'line_items':update_lines})
                        fulfillment_status = new_fulfillment

                        new_fulfillment.save()                        
                    except Exception,e:
                        raise Warning(e)
                    picking.write({'updated_in_shopify':True})
        self.closed_at(instances)
        return True


    @api.multi
    def update_carrier(self):
        instances=self.env['shopify.instance.ept'].search([('state','=','confirmed')])
        for instance in instances:
            instance.connect_in_shopify()
            try:
                order_ids = shopify.Order().find()
            except Exception,e:
                raise Warning(e)
            if len(order_ids)>=50:
                order_ids=self.list_all_orders(order_ids)
            for order_id in order_ids:
                result=xml_to_dict(order_id.to_xml())
                result=result.get('order')
                odoo_order=self.search([('shopify_order_id','=',result.get('id')),('shopify_order_number','=',result.get('order_number'))])
                if odoo_order:
                    for line in odoo_order.order_line:
                        if line.product_id.type=='service':
                            shipping_product=instance.shipment_charge_product_id 
                            for line in result.get('shipping_lines',[]):
                                delivery_method=line.get('code')
                                if delivery_method:
                                    carrier=self.env['delivery.carrier'].search(['|',('name','=',delivery_method),('shopify_code','=',delivery_method)])
                                    if not carrier:
                                        carrier=self.env['delivery.carrier'].create({'name':delivery_method,'shopify_code':delivery_method,'partner_id':self.env.user.company_id.partner_id.id,'product_id':shipping_product.id})
                                    odoo_order.write({'carrier_id':carrier.id})
                                    odoo_order.picking_ids.write({'carrier_id':carrier.id})
            return True

    @api.multi
    def delivery_set(self):
        if self.shopify_order_id:
            raise UserError(_('You are not allow to chagne manually shipping charge in Shopify order.'))
        else:
            super(sale_order,self).delivery_set()
        
class sale_order_line(models.Model):
    _inherit="sale.order.line"
    
    shopify_line_id=fields.Char("Shopify Line")
