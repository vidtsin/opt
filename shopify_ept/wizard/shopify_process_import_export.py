from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning,Warning
from datetime import datetime
import time
import hashlib
import urllib2
import base64
import StringIO
import unicodecsv as csv
import logging
_logger = logging.getLogger(__name__)


class shopify_process_import_export(models.TransientModel):
    _name = 'shopify.process.import.export'
   
    
    instance_ids = fields.Many2many("shopify.instance.ept",'shopify_instance_import_export_rel','process_id','shopify_instance_id',"Instances")

    update_price_in_product=fields.Boolean("Set Price",default=False)
    update_stock_in_product=fields.Boolean("Set Stock",default=False)
    publish=fields.Boolean("Publish In Website",default=False)
    publish_collection=fields.Boolean("Publish In Website",default=False)
    
    is_import_orders=fields.Boolean("Import Orders")
    is_export_products=fields.Boolean("Export Products")
    is_update_products=fields.Boolean("Update Products")
    
    is_publish_products=fields.Boolean("Publish Products")
    is_publish_collection=fields.Boolean("Publish Collection")
    is_export_collection=fields.Boolean("Export Collection")
    is_update_collection=fields.Boolean("Update Collection")
    is_update_stock=fields.Boolean("Update Stock")

    is_update_price=fields.Boolean("Update Price")
    sync_product_from_shopify=fields.Boolean("Sync Products")
    is_import_collection=fields.Boolean("Import Collection")
    is_update_order_status=fields.Boolean("Update Order Status")

    # Custom
    is_import_product_from_shopify = fields.Boolean("Import Products Using Shopify Product Id")
    is_import_product_tags_from_shopify = fields.Boolean("Import Products Tags Using Shopify Product Id")
    is_import_customers_csv = fields.Boolean("Import Customers Using CSV")
    is_import_customers = fields.Boolean("Import Customers")
    is_import_stock = fields.Boolean("Import Stock")
    is_import_products = fields.Boolean("Import Products")
    is_compare_products = fields.Boolean("Compare Products")

    @api.model
    def default_get(self,fields):
        res = super(shopify_process_import_export,self).default_get(fields)
        if 'instance_ids' in fields:
            instance_ids = self.env['shopify.instance.ept'].search([('state','=','confirmed')])
            res.update({'instance_ids':[(6,0,instance_ids.ids)]})
        return res
    
        
    @api.multi
    def execute(self):
        if self.is_import_orders:
            self.import_export_processes()
        if self.sync_product_from_shopify:
            self.sync_products()
        if self.is_import_collection:
            self.import_collection()
        if self.is_export_products:
            self.export_products()
        if self.is_update_products:
            self.update_products()
        if self.is_update_price:
            self.update_price()
        if self.is_update_stock:
            self.update_stock_in_shopify()
        if self.is_export_collection:
            self.export_collection()
        if self.is_update_collection:
            self.update_collection()
        if self.is_update_order_status:
            self.update_order_status()
        if self.is_publish_products:
            self.publish_multiple_products()
        if self.is_publish_collection:
            self.publish_multiple_collection()
        if self.is_import_product_from_shopify:
            self.import_products_using_shopify_product_id()
        if self.is_import_product_tags_from_shopify:
            self.import_products_tags_using_shopify_product_id()
        if self.is_import_customers:
            self.import_customers()
        if self.is_import_customers_csv:
            self.import_customers_csv()
        if self.is_import_stock:
            self.import_stock_using_shopify_product_id()
        if self.is_import_products:
            self.create_all_products()
        if self.is_compare_products:
            self.compare_products()
        return True
            
            
    @api.multi
    def import_export_processes(self):
        sale_order_obj=self.env['sale.order']
        for instance in self.instance_ids:
            sale_order_obj.import_shopify_orders(instance)
        return True
    
    @api.multi
    def update_order_status(self):
        sale_order_obj=self.env['sale.order']
        for instance in self.instance_ids:
            sale_order_obj.update_order_status(instance)
        return True
    
    @api.multi
    def update_stock_in_shopify(self):
        shopify_product_tmpl_obj=self.env['shopify.product.template.ept']
        if self._context.get('process')=='update_stock':
            product_tmpl_ids=self._context.get('active_ids')
            instances=self.env['shopify.instance.ept'].search([])
        else:            
            product_tmpl_ids=[]
            instances=self.instance_ids

        
        for instance in instances:
            if product_tmpl_ids:
                products=shopify_product_tmpl_obj.search([('shopify_instance_id','=',instance.id),('id','in',product_tmpl_ids)])
            else:
                products=shopify_product_tmpl_obj.search([('shopify_instance_id','=',instance.id),('exported_in_shopify','=',True)])
            shopify_product_tmpl_obj.update_stock_in_shopify(instance,products)
        return True
            
    @api.multi
    def update_price(self):
        shopify_product_tmpl_obj=self.env['shopify.product.template.ept']
        if self._context.get('process')=='update_price':
            product_tmpl_ids=self._context.get('active_ids')
            instances=self.env['shopify.instance.ept'].search([])
        else:            
            product_tmpl_ids=[]
            instances=self.instance_ids

        for instance in instances:
            if product_tmpl_ids:
                products=shopify_product_tmpl_obj.search([('shopify_instance_id','=',instance.id),('id','in',product_tmpl_ids)])
            else:
                products=shopify_product_tmpl_obj.search([('shopify_instance_id','=',instance.id),('exported_in_shopify','=',True)])

            shopify_product_tmpl_obj.update_price_in_shopify(instance,products)
        return True

    @api.multi
    def check_products(self,products):
        if self.env['shopify.product.product.ept'].search([('shopify_template_id','in',products.ids),('default_code','=',False)]):
            raise Warning("Default code is not set in some variants")
    @api.multi
    def filter_templates(self,products):
        filter_templates=[]
        for template in products:
            if not self.env['shopify.product.product.ept'].search([('shopify_template_id','=',template.id),('default_code','=',False)]):
                filter_templates.append(template)
        return filter_templates
    
    @api.multi
    def export_products(self):
        shopify_product_tmpl_obj=self.env['shopify.product.template.ept']
        if self._context.get('process')=='export_products':
            product_ids=self._context.get('active_ids')
            instances=self.env['shopify.instance.ept'].search([])
        else:            
            product_ids=[]
            instances=self.instance_ids

        for instance in instances:
            if product_ids:
                products=shopify_product_tmpl_obj.search([('shopify_instance_id','=',instance.id),('id','in',product_ids),('exported_in_shopify','=',False)])
                products=self.filter_templates(products)
            else:
                products=shopify_product_tmpl_obj.search([('shopify_instance_id','=',instance.id),('exported_in_shopify','=',False)])
                self.check_products(products)

            shopify_product_tmpl_obj.export_products_in_shopify(instance,products,self.update_price_in_product,self.update_stock_in_product,self.publish)
        return True

    @api.multi
    def update_products(self):
        shopify_product_tmpl_obj=self.env['shopify.product.template.ept']
        if self._context.get('process')=='update_products':
            product_ids=self._context.get('active_ids')
            instances=self.env['shopify.instance.ept'].search([])
        else:            
            instances=self.instance_ids
            product_ids=[]

        for instance in instances:
            if product_ids:
                products=shopify_product_tmpl_obj.search([('shopify_instance_id','=',instance.id),('id','in',product_ids),('exported_in_shopify','=',True)])
            else:
                products=shopify_product_tmpl_obj.search([('shopify_instance_id','=',instance.id),('exported_in_shopify','=',True)])

            shopify_product_tmpl_obj.update_products_in_shopify(instance,products)
        return True

    
    @api.multi
    def update_payment(self):
        account_invoice_obj=self.env['account.invoice']
        invoices=self.invoice_ids
        sale_order_ids=[]
        for invoice in invoices:
            sale_order_ids+=invoice.sale_ids.ids
        account_invoice_obj.update_payment(sale_order_ids,invoices.ids)
        
        return True
        
    @api.multi
    def prepare_product_for_export(self):

        shopify_template_obj=self.env['shopify.product.template.ept']
        shopify_product_obj=self.env['shopify.product.product.ept']
        template_ids=self._context.get('active_ids',[])
        odoo_templates=self.env['product.template'].search([('id','in',template_ids),('type','!=','service')])
        for instance in self.instance_ids:
            for odoo_template in odoo_templates:
                shopify_template=shopify_template_obj.search([('shopify_instance_id','=',instance.id),('product_tmpl_id','=',odoo_template.id)])                
                if not shopify_template:
                    shopify_template=shopify_template_obj.create({'shopify_instance_id':instance.id,'product_tmpl_id':odoo_template.id,'name':odoo_template.name,'description':odoo_template.description_sale})
                sequence=1
                for variant in odoo_template.product_variant_ids:
                    shopify_variant=shopify_product_obj.search([('shopify_instance_id','=',instance.id),('product_id','=',variant.id)])
                    if not shopify_variant:
                        shopify_product_obj.create({'shopify_instance_id':instance.id,'product_id':variant.id,'shopify_template_id':shopify_template.id,'default_code':variant.default_code,'name':variant.name,'sequence':sequence})
                    else:
                        shopify_variant.write({'sequence':sequence})
                    sequence=sequence+1
        return True
    
    @api.multi
    def publish_multiple_products(self):
        shopify_template_obj=self.env['shopify.product.template.ept']
        if self._context.get('process')=='publish_multiple_products':
            template_ids=self._context.get('active_ids',[])
            templates=shopify_template_obj.search([('id','in',template_ids),('exported_in_shopify','=',True)])
        else:
            templates=shopify_template_obj.search([('exported_in_shopify','=',True)])
        for template in templates:
            template.shopify_published()
        return True
    
    @api.multi
    def publish_multiple_collection(self):
        collection_obj=self.env['shopify.collection.ept']
        if self._context.get('process')=='publish_multiple_collection':
            collection_ids=self._context.get('active_ids')
            collections=collection_obj.search([('id','in',collection_ids),('exported_in_shopify','=',True)])
        else:
            collections=collection_obj.search([('exported_in_shopify','=',True)])
        for collection in collections:
            collection.shopify_published()
        return True
    @api.multi
    def export_collection(self):
        collection_obj=self.env['shopify.collection.ept']
        if self._context.get('process')=='create_collection':
            collection_ids=self._context.get('active_ids')
            instances=self.env['shopify.instance.ept'].search([])
        else:            
            instances=self.instance_ids
            collection_ids=collection_obj.search([]).ids

        for instance in instances:
            collections=collection_obj.search([('shopify_instance_id','=',instance.id),('id','in',collection_ids),('is_smart_collection','=',False),('exported_in_shopify','=',False)])
            collections and collection_obj.export_custom_collection(instance,collections,self.publish_collection)

            collections=collection_obj.search([('shopify_instance_id','=',instance.id),('id','in',collection_ids),('is_smart_collection','=',True),('exported_in_shopify','=',False)])
            collections and collection_obj.export_smart_collection(instance,collections,self.publish_collection)
        return True
    @api.multi
    def update_collection(self):
        collection_obj=self.env['shopify.collection.ept']
        if self._context.get('process')=='update_collection':
            collection_ids=self._context.get('active_ids')
            instances=self.env['shopify.instance.ept'].search([])
        else:            
            instances=self.instance_ids
            collection_ids=collection_obj.search([]).ids
        for instance in instances:
            collections=collection_obj.search([('shopify_instance_id','=',instance.id),('id','in',collection_ids),('is_smart_collection','=',False),('exported_in_shopify','=',True)])
            collections and collection_obj.update_custom_collection(instance,collections)

            collections=collection_obj.search([('shopify_instance_id','=',instance.id),('id','in',collection_ids),('is_smart_collection','=',True),('exported_in_shopify','=',True)])
            collections and collection_obj.update_smart_collection(instance,collections)

        return True


    @api.multi
    def import_collection(self):
        collection_obj=self.env['shopify.collection.ept']
        for instance in self.instance_ids:
            collection_obj.import_collection(instance)
        return True


    @api.multi
    def sync_selective_products(self):
        active_ids=self._context.get('active_ids')
        shopify_template_obj=self.env['shopify.product.template.ept']
        for instance in self.instance_ids:
            shopify_templates=shopify_template_obj.search([('id','in',active_ids),('shopify_instance_id','=',instance.id),('shopify_tmpl_id','=',False)])
            if shopify_templates:
                raise Warning("You can only sync already exported products")
            shopify_templates=shopify_template_obj.search([('id','in',active_ids),('shopify_instance_id','=',instance.id)])
            for shopify_template in shopify_templates:
                shopify_template_obj.sync_products(instance,shopify_tmpl_id=shopify_template.shopify_tmpl_id)
        return True


    @api.multi
    def sync_products(self):
        shopify_template_obj=self.env['shopify.product.template.ept']
        for instance in self.instance_ids:
            shopify_template_obj.sync_products(instance,update_price=self.update_price_in_product,)
        return True

    # Import all products with proper variants
    @api.multi
    def create_all_products(self):
        shopify_template_obj = self.env['shopify.product.template.ept']
        for instance in self.instance_ids:
            shopify_template_obj.create_all_products(instance,update_price=self.update_price_in_product,)
        return True

    # Improt Produts using Shopify Product Id
    @api.multi
    def import_products_using_shopify_product_id(self):
        shopify_template_obj = self.env['shopify.product.template.ept']
        for instance in self.instance_ids:
            shopify_template_obj.import_products_using_shopify_product_id(instance, update_price=self.update_price_in_product, )
        return True

    # Import Products Tags Using Shopify Product ID
    @api.multi
    def import_products_tags_using_shopify_product_id(self):
        shopify_template_obj = self.env['shopify.product.template.ept']
        for instance in self.instance_ids:
            shopify_template_obj.import_products_tags_using_shopify_product_id(instance,
                                                                          update_price=self.update_price_in_product, )
        return True

    # Improt Customers from Shopify to Odoo
    @api.multi
    def import_customers(self):
        shopify_template_obj = self.env['shopify.product.template.ept']
        for instance in self.instance_ids:
            shopify_template_obj.import_customers(instance, cumstomer_temp_id=False)
        return True

    # Improt Stock using Shopify Product Id
    @api.multi
    def import_stock_using_shopify_product_id(self):
        shopify_template_obj = self.env['shopify.product.template.ept']
        for instance in self.instance_ids:
            shopify_template_obj.import_stock(instance)
        return True

    # compare_products (in odoo and shopify)
    @api.multi
    def compare_products(self):
        shopify_template_obj = self.env['shopify.product.template.ept']
        for instance in self.instance_ids:
            shopify_template_obj.compare_products(instance, update_price=self.update_price_in_product, )
        return True

    # Improt Customers using csv
    @api.multi
    def import_customers_csv(self):
        country_obj = self.env['res.country']
        state_obj = self.env['res.country.state']
        partner_obj = self.env['res.partner']
        rownum = 0
        count_row = 1

        without_name = []
        shopify_cust = []
        create_cust = []

        fileobj = open('/opt/vendors.csv', 'rb')
        str_csv_data = fileobj.read()
        list = csv.reader(StringIO.StringIO(str_csv_data), delimiter='|')

        for row in list:
            if row == '':
                continue
            if rownum == 0:
                rownum += 1
                print "header<<<<<<<<<<<<<<",row
            else:
                print "row<<<<<<<<<<<<<<", row
                _logger.info("-------------count_row-----------: %s", count_row)

                if str(row[19]).strip() == 't':
                    is_company = True
                else:
                    is_company = False

                vals = {
                        'name': str(row[1]).strip() or False,
                        'company_id': 1,
                        'comment': str(row[3]).strip() or False,
                        'function': str(row[4]).strip() or False,
                        'color': str(row[6]).strip() or False,
                        'company_type': str(row[7]).strip() or False,
                        'date': str(row[8]).strip() or False,
                        'street': str(row[9]).strip() or False,
                        'city': str(row[10]).strip() or False,
                        'display_name': str(row[11]).strip() or False,

                        'zip': str(row[12]).strip() or False,
                        # 'title': str(row[13]).strip() or False,
                        'country_id': str(row[14]).strip() or False,
                        # 'parent_id': str(row[15]).strip() or False,
                        'supplier': True,
                        'ref': str(row[17]).strip() or False,
                        'email': str(row[18]).strip() or False,

                        'is_company': is_company,
                        'website': str(row[20]).strip() or False,
                        'customer': False,
                        'fax': str(row[22]).strip() or False,

                        'street2': str(row[23]).strip() or False,
                        'barcode': str(row[24]).strip() or False,
                        'employee': False,
                        'credit_limit': str(row[26]).strip() or False,
                        'active': True,
                        'tz': str(row[29]).strip() or False,
                        'lang': str(row[31]).strip() or False,
                        'phone': str(row[33]).strip() or False,
                        'mobile': str(row[34]).strip() or False,
                        'type': str(row[35]).strip() or False,
                        'use_parent_address': False,

                        'user_id': str(row[37]).strip() or False,
                        'birthdate': str(row[38]).strip() or False,
                        'vat': str(row[39]).strip() or False,
                        'state_id': str(row[40]).strip() or False,
                        # 'commercial_partner_id': str(row[41]).strip() or False,
                        'notify_email': str(row[42]).strip() or False,
                        'message_last_post': str(row[43]).strip() or False,
                        'opt_out': False,
                        'signup_type': str(row[45]).strip() or False,
                        'signup_expiration': str(row[46]).strip() or False,
                        'signup_token': str(row[47]).strip() or False,

                        'last_time_entries_checked': str(row[48]).strip() or False,
                        'debit_limit': str(row[49]).strip() or False,
                        'country_code': str(row[50]).strip() or False,
                        'tax_exempt': False,
                        'total_orders': str(row[52]).strip() or False,
                        'accepts_marketing': False,
                        'total_spent': str(row[54]).strip() or False,
                        'province_code': str(row[55]).strip() or False,
                        'team_id': str(row[56]).strip() or False,
                        'website_description': str(row[57]).strip() or False,
                        'website_meta_keywords': str(row[58]).strip() or False,

                        'website_meta_description': str(row[59]).strip() or False,
                        'website_meta_title': str(row[60]).strip() or False,
                        'website_published': False,
                        'website_short_description': str(row[62]).strip() or False,
                        'last_website_so_id': str(row[63]).strip() or False,
                        'calendar_last_notif_ack': str(row[64]).strip() or False,
                        'company_name_ept': str(row[65]).strip() or False,
                        'shopify_customer_id': str(row[66]).strip() or False,

                        }

                _logger.info("-------------vals-----------: %s", vals)

                partner_id = partner_obj.create(vals)
                _logger.info("-------------partner_id-----------: %s", partner_id)

                if partner_id.is_company or not partner_id.parent_id:
                    partner_id.commercial_partner_id = partner_id
                    print "<<<<<<<if<<<<<<<<<<"
                else:
                    partner_id.commercial_partner_id = partner_id.parent_id.commercial_partner_id
                    print "<<<<<else<<<<<<<<<<"

                create_cust.append(partner_id)

                self._cr.execute("""update res_partner set create_date=%s, write_date=%s where id=%s""",
                                 (row[5] or False, row[27] or False, partner_id[0].id))
                self._cr.commit()
                count_row += 1

        _logger.info("-------------without_name-----------: %s", without_name)
        _logger.info("-------------without_name----len-------: %s", len(without_name))
        _logger.info("-------------shopify_cust---------: %s", shopify_cust)
        _logger.info("-------------shopify_cust---len--------: %s", len(shopify_cust))
        _logger.info("-------------create_cust-----------: %s", create_cust)
        _logger.info("-------------create_cust----len-------: %s", len(create_cust))


        return True