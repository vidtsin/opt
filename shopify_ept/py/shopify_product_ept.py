from odoo import models,fields,api
import odoo.addons.decimal_precision  as dp
# from odoo.addons.shopify_ept.shopify import *
from .. import shopify
import time
import urllib
import base64
from datetime import timedelta,datetime
# from odoo.osv import osv
import hashlib
# import csv
# from unicodecsv import csv
import unicodecsv as csv
# from cStringIO import StringIO
import urllib2
import base64
import logging
_logger = logging.getLogger(__name__)
import json
import requests
import math
import StringIO
from tempfile import TemporaryFile
# from pyactiveresource.util import xml_to_dict


class product_attribute(models.Model):
    _inherit="product.attribute"
    shopify_name=fields.Char("Shopify Name")

class product_template(models.Model):
    _inherit="product.template"
    shopify_product_id=fields.Char("shopify product id")
    # shopify_variant_id = fields.Char("Shopify variant id")
    info = fields.Text("Add Additional Info", help="Add your additional Info here")
    # inventory_item_id = fields.Char('Inventory Item ID')


class shopify_product_template_ept(models.Model):
    _name="shopify.product.template.ept"
    
    
    @api.multi
    @api.depends('shopify_product_ids.exported_in_shopify','shopify_product_ids.variant_id')
    def get_total_sync_variants(self):
        shopify_product_obj=self.env['shopify.product.product.ept']
        for template in self:
            variants=shopify_product_obj.search([('id','in',template.shopify_product_ids.ids),('exported_in_shopify','=',True),('variant_id','!=',False)]) 
            template.total_sync_variants=len(variants.ids)
    name=fields.Char("Name")
    shopify_instance_id=fields.Many2one("shopify.instance.ept","Instance",required=1)
    product_tmpl_id=fields.Many2one("product.template","Product Template")
    shopify_tmpl_id=fields.Char("Shopify Tmpl Id")
    exported_in_shopify=fields.Boolean("Exported In Shopify")
    shopify_product_ids=fields.One2many("shopify.product.product.ept","shopify_template_id","Products")
    template_suffix=fields.Char("Template Suffix")
    created_at=fields.Datetime("Created At")
    updated_at=fields.Datetime("Updated At")
    published_at=fields.Datetime("Publish at")
    inventory_management=fields.Selection([('shopify','Shopify tracks this product Inventory'),('Dont track Inventory','Dont track Inventory')],default='shopify')
    check_product_stock=fields.Boolean("Sale out of stock products ?",default=False)
    taxable=fields.Boolean("Taxable",default=True)
    fulfillment_service=fields.Selection([('manual','Manual'),('shopify','shopify')],default='manual')
    website_published=fields.Boolean('Available in the website', copy=False)
    tag_ids=fields.Many2many("shopify.tags","shopify_tags_rel","product_tmpl_id","tag_id","Tags")
    description=fields.Html("Description")
    total_variants_in_shopify=fields.Integer("Total Shopify Varaints",default=0)
    total_sync_variants=fields.Integer("Total Sync Variants",compute="get_total_sync_variants",store=True)

    @api.multi
    def reorder_variants(self):
        res = self.env.ref('shopify_ept.view_shopify_reorder_variants_wizard')
                    
        action = {
        'name':'Reorder Variants',
        'view_type': 'form',
        'view_mode': 'form',
        'view_id': res.ids,
        'res_model': 'shopify.variant.reorder.ept',
        'context': self._context,
        'type': 'ir.actions.act_window',
        'nodestroy': True,
        'target':'new',
               }
        return action


    @api.multi
    def list_all_products(self, result):
        sum_of_result = result
        if not sum_of_result:
            return sum_of_result
        product_ids = [result_id.id for result_id in result]
        since_id = max(product_ids)
        # since_id=min(product_ids)
        new_result = shopify.Product().find(limit=250, since_id=since_id)
        # product_ids1 = [result_id.id for result_id in new_result]
        while new_result:
            sum_of_result = sum_of_result + new_result
            product_ids = [result_id.id for result_id in new_result]
            since_id = max(product_ids)
            new_result = shopify.Product().find(limit=250, since_id=since_id)
        return sum_of_result

    @api.multi
    def update_image(self, variants,images,template):
        # for variant in variants:
        for image in images:
            if variants['image_id'] == image['id']:
                img = image.get('src')
                image = urllib2.urlopen(img)
                imgs = image.read()
                image_base64 = base64.encodestring(imgs)
                template.write({'image_medium': image_base64})
        return True


    @api.multi
    def sync_products(self,instance,shopify_tmpl_id=False,update_price=False,update_templates=True):
        shopify_product_obj=self.env['shopify.product.product.ept']
        transaction_log_obj=self.env["shopify.transaction.log"]
        odoo_product_obj=self.env['product.product']
        instance.connect_in_shopify()
        shop_url = instance.count_product_in_shopify()
        product_count = requests.get(shop_url + "/products/count.json")
        total_product_count = json.loads(product_count.text).get('count')
        _logger.info("------total_product_count-----: %s", total_product_count)
        pages = float(total_product_count) / 250.0
        counter = int(math.ceil(pages))
        results = []
        product_tmpl_ids_count = 0
        shopify_template_count = 0
        if shopify_tmpl_id:
            results=[shopify.Product().find(shopify_tmpl_id)]
            _logger.info("------results-----: %s", results)
        else:
            while counter:
                product_ids =shopify.Product().find(limit=250,page=counter)
                results += product_ids
                counter-=1

            # if len(results)>=250:
            #     results=self.list_all_products(results)

        #pooling obj
        product_obj = self.env['product.template']
        product_categ_obj = self.env['product.category']
        product_public_category_obj = self.env['product.public.category']
        attribute_name_obj = self.env['product.attribute']
        attribute_value_obj = self.env['product.attribute.value']
        attribute_line_obj = self.env['product.attribute.line']
        product_uom_obj = self.env['product.uom']
        _logger.info("-----results-----: %s", results)
        _logger.info("-------len(results)------: %s", len(results))

        for response_template in results:
            _logger.info("-------------response_template-----------: %s", response_template)
            response_template=response_template.to_dict()

            img_var = response_template.get('image')
            # _logger.info("-------------img_var-----------: %s", img_var)
            image_base64 = ''
            if img_var :
                img = img_var.get('src')
                image = urllib2.urlopen(img)
                imgs = image.read()
                image_base64 = base64.encodestring(imgs)


            shopify_product_id = response_template.get('id')
            product_name = response_template.get('title')
            _logger.info("-------------product_name-----------: %s", product_name)

            # if product_name == 'AI Easy Vac 1.8 CFM Compact Vacuum Pump w/ Oil Mist Filter':
            #     _logger.info("-------------response_template-----------: %s", response_template)
            #     kk


            attri_position1 = []
            attri_position2 = []
            attri_position3 = []
            value_position1 = []
            value_position2 = []
            value_position3 = []

            for variant_options in response_template.get('options'):
                name = variant_options.get('name')
                attribute_name_id = attribute_name_obj.search([('name', '=', name)])
                _logger.info("------attribute_name_id------: %s", attribute_name_id)
                if not attribute_name_id:
                    attribute_vals = {
                        'name': name,
                        'create_variant': True,
                    }
                    attribute_name_id = attribute_name_obj.create(attribute_vals)
                if variant_options.get('position') == 1:
                    attri_position1.append(attribute_name_id.id)
                elif variant_options.get('position') == 2:
                    attri_position2.append(attribute_name_id.id)
                else:
                    attri_position3.append(attribute_name_id.id)

                for values in variant_options.get('values'):
                    attribute_value_id = attribute_value_obj.search(
                        [('attribute_id', '=', attribute_name_id.id), ('name', '=',values)])
                    if not attribute_value_id:
                        attribute_value_vals = {
                            'attribute_id': attribute_name_id.id,
                            'name': values,
                        }
                        attribute_value_id = attribute_value_obj.create(attribute_value_vals)
                    if variant_options.get('position') == 1:
                        value_position1.append(attribute_value_id.id)
                    elif variant_options.get('position') == 2:
                        value_position2.append(attribute_value_id.id)
                    else:
                        value_position3.append(attribute_value_id.id)

                    attrivals = {
                                str(attri_position1) : value_position1,
                                str(attri_position2) : value_position2,
                                str(attri_position3) : value_position3,
                     }
            product_type = response_template.get('product_type')
            if product_type:
                product_categ_id = product_categ_obj.search([('name', '=', str(product_type))])
                if not product_categ_id:
                    categ_vals = {'name':str(product_type),
                                  'property_valuation':'manual_periodic'}
                    product_categ_id = product_categ_obj.create(categ_vals)


                product_public_categ_id = product_public_category_obj.search([('name', '=', str(product_type))])
                if not product_public_categ_id:
                    web_categ_vals = {'name': str(product_type),}
                    product_public_categ_id = product_public_category_obj.create(web_categ_vals)

                product_categ_id = product_categ_id.id
                product_public_categ_id = product_public_categ_id.id
            else:
                product_categ_id = 1

                product_public_categ_id = product_public_category_obj.search([('name', '=', 'General Category')])
                if not product_public_categ_id:
                    web_categ_vals = {'name': 'General Category', }
                    product_public_categ_id = product_public_category_obj.create(web_categ_vals)
                product_public_categ_id = product_public_categ_id.id

            for variant in response_template.get('variants'):
                _logger.info("------variant------: %s", variant)
                barcode = str(variant.get('barcode', ''))
                shopify_barcode = product_obj.search([('barcode', '=', barcode)])
                shopify_template = product_obj.search([('shopify_product_id', '=', shopify_product_id),('shopify_variant_id', '=', variant.get('id'))])
                _logger.info("-------------shopify_template-----------: %s", shopify_template)
                if shopify_template:
                    shopify_template_count += 1
                    _logger.info("-------------shopify_template_count-----------: %s", shopify_template_count)
                    product_barcode = None
                    if len(response_template.get('images')) > 1:
                        if variant.get('image_id'):
                            self.update_image(variant, response_template.get('images'), shopify_template)
                        else:
                            shopify_template.write({'image_medium': image_base64})
                    else:
                        vals = {'image_medium': image_base64}
                        shopify_template.write(vals)
                    _logger.info("-------shopify_template.shopify_variant_id-------: %s", shopify_template.shopify_variant_id)
                    _logger.info("-------variant.get('id')-------: %s", variant.get('id'))
                    if int(shopify_template.shopify_variant_id) == variant.get('id'):
                        if variant.get('barcode'):
                            product_barcode = variant.get('barcode')
                            _logger.info("-------product_barcode-------: %s", product_barcode)
                        vals = {'list_price': variant.get('price'),
                                # 'barcode': product_barcode,
                                'categ_id': product_categ_id,
                                'default_code': str(variant.get('sku','')),
                                'website_description': response_template.get('body_html'),
                                'public_categ_ids': [(6,0,[product_public_categ_id])],
                                }
                        _logger.info("-----------vals-----------: %s", vals)
                        shopify_template.write(vals)
                    continue

                if shopify_barcode:
                    continue
                if barcode == 'None':
                    barcode = False

                grams_weight=variant.get('grams')
                weight_unit=variant.get('weight_unit')

                if weight_unit == 'kg':
                    grams_weight = grams_weight * 0.001
                    pass

                if weight_unit == 'g':
                    grams_weight = grams_weight * 0.001
                    pass
                if weight_unit == 'lb':

                    weight_unit = weight_unit+'(s)'
                    if grams_weight:
                        grams_weight = grams_weight * 0.00220462

                if weight_unit == 'oz':
                    weight_unit = weight_unit + '(s)'
                    if grams_weight:
                        grams_weight = grams_weight * 0.035274

                product_uom_id = product_uom_obj.search([('name', '=', weight_unit)])

                sku=str(variant.get('sku',''))
                if sku == 'None':
                    sku = False

                price=variant.get('price')
                variant_id=variant.get('id')
                title=variant.get('title')
                splitted_titles = title.split(' / ')

                counter = 0
                attribute_value_id0 = []
                attribute_value_id1 = []
                attribute_value_id2 = []

                for split_title in splitted_titles:

                    if counter == 0:
                        if split_title:
                            sp = split_title.strip(' ')
                            attribute_value_id0 = attribute_value_obj.search(
                                [('attribute_id', '=', attri_position1[0]), ('name', '=', sp)])
                    elif counter == 1:
                        if split_title:

                            sp1 = split_title.strip(' ')
                            attribute_value_id1 = attribute_value_obj.search(
                                [('attribute_id', '=', attri_position2[0]), ('name', '=', sp1)])
                    elif counter == 2:
                        if split_title:
                            sp2 = split_title.strip(' ')
                            attribute_value_id2 = attribute_value_obj.search(
                                [('attribute_id', '=', attri_position3[0]), ('name', '=', sp2)])
                    counter += 1

                vals = {
                        'name':product_name,
                        'type': 'product',
                        'default_code': sku,
                        'barcode': barcode,
                        'list_price': price,
                        'image_medium': image_base64,
                        'weight': grams_weight or False,
                        'uom_id': product_uom_id.id,
                        'uom_po_id': product_uom_id.id,
                        'categ_id':product_categ_id,
                        'public_categ_ids': [(6,0,[product_public_categ_id])],
                        'shopify_product_id':shopify_product_id,
                        'shopify_variant_id':variant_id,
                        'website_description': response_template.get('body_html'),
                        }
                _logger.info("--------vals-----111------: %s", vals)
                product_tmpl_ids = product_obj.create(vals)
                _logger.info("-------------product_tmpl_ids-----------: %s", product_tmpl_ids)
                product_tmpl_ids_count += 1
                _logger.info("------product_tmpl_ids---count----: %s", product_tmpl_ids_count)
                if attri_position1:
                    attribute_line_vals = { 'product_tmpl_id': product_tmpl_ids.id,
                                        'attribute_id': attri_position1[0],
                                        'value_ids': [(6, 0, [attribute_value_id0.id])],
                        }
                    _logger.info("-------------attribute_line_vals-----------: %s", attribute_line_vals)
                    attribute_line_ids1 = attribute_line_obj.create(attribute_line_vals)
                if attri_position2:
                    attribute_line_vals = { 'product_tmpl_id': product_tmpl_ids.id,
                                        'attribute_id': attri_position2[0],
                                        'value_ids': [(6, 0, [attribute_value_id1.id])],
                        }
                    _logger.info("-------------attribute_line_vals-----------: %s", attribute_line_vals)
                    attribute_line_ids2 = attribute_line_obj.create(attribute_line_vals)
                if attri_position3:
                    attribute_line_vals = { 'product_tmpl_id': product_tmpl_ids.id,
                                        'attribute_id': attri_position3[0],
                                        'value_ids': [(6, 0, [attribute_value_id2.id])],
                        }
                    _logger.info("-------------attribute_line_vals-----------: %s", attribute_line_vals)
                    attribute_line_ids3 = attribute_line_obj.create(attribute_line_vals)
            self._cr.commit()
        return True


    @api.multi
    def create_all_products(self, instance, shopify_tmpl_id=False, update_price=False, update_templates=True):
        odoo_product_obj = self.env['product.product']
        product_obj = self.env['product.template']
        product_categ_obj = self.env['product.category']
        product_public_category_obj = self.env['product.public.category']
        attribute_name_obj = self.env['product.attribute']
        attribute_value_obj = self.env['product.attribute.value']
        attribute_line_obj = self.env['product.attribute.line']
        product_uom_obj = self.env['product.uom']
        AttributePrice = self.env['product.attribute.price']

        instance.connect_in_shopify()
        shop_url = instance.count_product_in_shopify()
        product_count = requests.get(shop_url + "/products/count.json")
        total_product_count = json.loads(product_count.text).get('count')
        _logger.info("------total_product_count-----: %s", total_product_count)
        pages = float(total_product_count) / 250.0
        counter = int(math.ceil(pages))
        results = []
        product_tmpl_ids_count = 0
        product_product_count = 0
        shopify_template_count = 0
        shopify_template_variant_up = 0
        attrivals = {}
        product_counter = 0
        if shopify_tmpl_id:
            results = [shopify.Product().find(shopify_tmpl_id)]
            _logger.info("------results-----: %s", results)
        else:
            while counter:
                product_ids = shopify.Product().find(limit=250, page=counter)
                results += product_ids
                counter -= 1
        _logger.info("-----results-----: %s", results)
        _logger.info("-------len(results)------: %s", len(results))

        try:
            for response_template in results:
                product_counter +=1
                _logger.info("------product_counter-------%s-", product_counter)
                _logger.info("-------------response_template-----------: %s", response_template)
                response_template = response_template.to_dict()

                shopify_product_id = response_template.get('id')
                shopify_template = product_obj.search([('shopify_product_id', '=', shopify_product_id)])

                # Update product.template if exists
                if shopify_template:
                    shopify_template_count += 1
                    _logger.info("-------------shopify_template_count-----------: %s", shopify_template_count)
                    # product.template image
                    img_var = response_template.get('image')
                    image_base64 = ''
                    if img_var:
                        img = img_var.get('src')
                        image = urllib2.urlopen(img)
                        imgs = image.read()
                        image_base64 = base64.encodestring(imgs)
                        shopify_template.write({'image_medium': image_base64,})

                    # For variants
                    for variant in response_template.get('variants'):
                        product_product_id = odoo_product_obj.search([('shopify_variant_id', '=', variant.get('id'))])
                        _logger.info("-------------product_product_id-----------: %s", product_product_id)
                        # Update variant if exists
                        if product_product_id:
                            shopify_template_variant_up += 1
                            # _logger.info("-------------shopify_template_variant_up-----------: %s", shopify_template_variant_up)
                            product_barcode = False
                            if variant.get('barcode'):
                                product_barcode = variant.get('barcode')
                            _logger.info("-------product_barcode-------: %s", product_barcode)
                            sku = str(variant.get('sku'))
                            if sku == 'None':
                                sku = False
                            image_base64_vr = ''
                            image_id = variant.get('image_id')
                            if image_id:
                                for img_vr in response_template.get('images'):
                                    if image_id == img_vr.get('id'):
                                        img = img_vr.get('src')
                                        image = urllib2.urlopen(img)
                                        imgs = image.read()
                                        image_base64_vr = base64.encodestring(imgs)
                            vals = {
                                'barcode': product_barcode,
                                'default_code': sku,
                                'image_medium': image_base64_vr,
                            }
                            product_product_id.write(vals)
                    continue

                product_name = response_template.get('title')
                _logger.info("-------------product_name-----------: %s", product_name)

                # if product_name == 'Tri Clamp Sight Glass - Individual':
                #     _logger.info("-------------product_name------innnnn-----: %s", product_name)
                attri_position1 = 0
                attri_position2 = 0
                attri_position3 = 0
                value_position1 = []
                value_position2 = []
                value_position3 = []

                # product.template image
                img_var = response_template.get('image')
                image_base64 = ''
                if img_var:
                    img = img_var.get('src')
                    image = urllib2.urlopen(img)
                    imgs = image.read()
                    image_base64 = base64.encodestring(imgs)

                # For variants
                for variant_options in response_template.get('options'):
                    name = variant_options.get('name')
                    attribute_name_id = attribute_name_obj.search([('name', '=', name)])
                    _logger.info("------attribute_name_id------: %s", attribute_name_id)
                    if not attribute_name_id:
                        attribute_vals = {
                            'name': name,
                            'create_variant': True,
                        }
                        attribute_name_id = attribute_name_obj.create(attribute_vals)
                    if variant_options.get('position') == 1:
                        attri_position1 = attribute_name_id.id
                    elif variant_options.get('position') == 2:
                        attri_position2 = attribute_name_id.id
                    else:
                        attri_position3 = attribute_name_id.id

                    for values in variant_options.get('values'):
                        attribute_value_id = attribute_value_obj.search([('attribute_id', '=', attribute_name_id.id), ('name', '=', values)])
                        if not attribute_value_id:
                            attribute_value_vals = {
                                'attribute_id': attribute_name_id.id,
                                'name': values,
                            }
                            attribute_value_id = attribute_value_obj.create(attribute_value_vals)
                        if variant_options.get('position') == 1:
                            value_position1.append(attribute_value_id.id)
                        elif variant_options.get('position') == 2:
                            value_position2.append(attribute_value_id.id)
                        else:
                            value_position3.append(attribute_value_id.id)

                        attrivals = {
                            attri_position1 : value_position1,
                            attri_position2 : value_position2,
                            attri_position3 : value_position3,
                        }

                # For Product Category
                product_type = response_template.get('product_type')
                if product_type:
                    product_categ_id = product_categ_obj.search([('name', '=', str(product_type))])
                    if not product_categ_id:
                        categ_vals = {'name': str(product_type),
                                      'property_valuation': 'manual_periodic'}
                        product_categ_id = product_categ_obj.create(categ_vals)

                    product_public_categ_id = product_public_category_obj.search([('name', '=', str(product_type))])
                    if not product_public_categ_id:
                        web_categ_vals = {'name': str(product_type), }
                        product_public_categ_id = product_public_category_obj.create(web_categ_vals)

                    product_categ_id = product_categ_id.id
                    product_public_categ_id = product_public_categ_id.id
                else:
                    product_categ_id = 1

                    product_public_categ_id = product_public_category_obj.search([('name', '=', 'General Category')])
                    if not product_public_categ_id:
                        web_categ_vals = {'name': 'General Category', }
                        product_public_categ_id = product_public_category_obj.create(web_categ_vals)
                    product_public_categ_id = product_public_categ_id.id

                # Create product.template
                vals = {
                    'name': product_name,
                    'type': 'product',
                    'list_price': 0,
                    'image_medium': image_base64,
                    # 'uom_id': product_uom_id.id,
                    # 'uom_po_id': product_uom_id.id,
                    'categ_id': product_categ_id,
                    'public_categ_ids': [(6, 0, [product_public_categ_id])],
                    'shopify_product_id': shopify_product_id,
                    'website_description': response_template.get('body_html'),
                }
                # _logger.info("--------vals-----111------: %s", vals)
                product_tmpl_ids = product_obj.create(vals)
                _logger.info("-------------product_tmpl_ids-----------: %s", product_tmpl_ids)
                product_tmpl_ids_count += 1
                _logger.info("------product_tmpl_ids---count----: %s", product_tmpl_ids_count)

                # Create product.attribute.line of product.template
                for key, value in attrivals.items():
                    print "---------key------------ : ", key
                    print "---------value------------ : ", value
                    if key and value:
                        attribute_line_vals = {
                            'product_tmpl_id': product_tmpl_ids.id,
                            'attribute_id': key,
                            'value_ids': [(6, 0, value)],
                        }
                        # _logger.info("-------------attribute_line_vals-----------: %s", attribute_line_vals)
                        attribute_line_ids = attribute_line_obj.create(attribute_line_vals)
                        _logger.info("-------------attribute_line_ids-----------: %s", attribute_line_ids)
                # To create product.product
                product_tmpl_ids.create_variant_ids()

                print "<<<<<<<<<<product_tmpl_ids.product_variant_ids<<<<<<<<<<", product_tmpl_ids.product_variant_ids


                price = None
                sku = None
                inventory_item_id = None
                image_base64_vr = None
                grams_weight = None
                variant_id = None
                price_extra = None

                for product_variant_id in product_tmpl_ids.product_variant_ids:
                    for variant in response_template.get('variants'):
                        p_product_variant_id = None
                        # _logger.info("------variant------: %s", variant)
                        if variant:
                            price = variant.get('price')
                            attribute_value_ids = product_variant_id.attribute_value_ids
                            print "<<<<<<<<<<attribute_value_ids<<<<<<<<", attribute_value_ids
                            attribute_value_len = len(attribute_value_ids)
                            print "<<<<attribute_value_len<<<<<<", attribute_value_len
                            # Get variant id
                            option1 = variant.get('option1')
                            option2 = variant.get('option2')
                            option3 = variant.get('option3')
                            if (option1 and option2 and option3) and attribute_value_len == 3:
                                name1, name2, name3 = '', '', ''
                                counter_name = 1
                                for attribute_value_id in attribute_value_ids:
                                    if counter_name == 1:
                                        name1 = attribute_value_id.name
                                    if counter_name == 2:
                                        name2 = attribute_value_id.name
                                    if counter_name == 3:
                                        name3 = attribute_value_id.name
                                    counter_name += 1
                                if ((name1 == option1) or (name1 == option2) or (name1 == option3)) and ((name2 == option1) or (name2 == option2) or (name2 == option3)) and ((name3 == option1) or (name3 == option2) or (name3 == option3)):
                                    p_product_variant_id = product_variant_id
                            elif (option1 and option2) and attribute_value_len == 2:
                                name1, name2 = '', ''
                                counter_name = 1
                                for attribute_value_id in attribute_value_ids:
                                    if counter_name == 1:
                                        name1 = attribute_value_id.name
                                    if counter_name == 2:
                                        name2 = attribute_value_id.name
                                    counter_name += 1
                                if ((name1 == option1) or (name1 == option2)) and ((name2 == option1) or (name2 == option2)):
                                    p_product_variant_id = product_variant_id
                            elif option1 and attribute_value_len == 1:
                                if attribute_value_ids.name == option1:
                                    p_product_variant_id = product_variant_id
                                    # Add price in product.template
                                    if product_tmpl_ids.list_price == 0.0:
                                        product_tmpl_ids.write({'list_price': float(price)})
                                    if attribute_value_ids.price_extra == 0.0:
                                        variant_price_extra = float(price) - product_tmpl_ids.list_price
                                        if variant_price_extra != 0.0:
                                            attribute_value_ids.write({'price_extra': variant_price_extra})
                                            prices = AttributePrice.search([('value_id', '=', attribute_value_ids.id), ('product_tmpl_id', '=', product_tmpl_ids.id)])
                                            # updated = prices.mapped('value_id')
                                            if prices:
                                                prices.write({'price_extra': variant_price_extra})
                                            else:
                                                AttributePrice_id = AttributePrice.create({
                                                    'product_tmpl_id': product_tmpl_ids.id,
                                                    'value_id': attribute_value_ids.id,
                                                    'price_extra': variant_price_extra,
                                                })

                            if not p_product_variant_id:
                                continue

                            variant_id = variant.get('id')
                            # variant image
                            image_id = variant.get('image_id')
                            image_base64_vr = ''
                            if image_id:
                                for img_vr in response_template.get('images'):
                                    if image_id == img_vr.get('id'):
                                        img = img_vr.get('src')
                                        image = urllib2.urlopen(img)
                                        imgs = image.read()
                                        image_base64_vr = base64.encodestring(imgs)

                            sku = str(variant.get('sku', ''))
                            if sku == 'None':
                                sku = False

                            product_product_id = odoo_product_obj.search([('shopify_variant_id', '=', variant_id)])
                            _logger.info("-------------product_product_id-----------: %s", product_product_id)

                            # Update variant if exists
                            if product_product_id:
                                product_product_count += 1
                                _logger.info("-------------product_product_count-----------: %s", product_product_count)
                                product_barcode = None
                                if variant.get('barcode'):
                                    product_barcode = variant.get('barcode')
                                    _logger.info("-------product_barcode-------: %s", product_barcode)
                                vals = {
                                    'lst_price': price,
                                    'barcode': product_barcode,
                                    'default_code': sku,
                                    'image_medium': image_base64_vr,
                                }
                                # _logger.info("-----------vals-----------: %s", vals)
                                product_product_id.write(vals)
                                continue

                            shopify_barcode = None
                            barcode = str(variant.get('barcode')) or False
                            _logger.info("-------barcode-------: %s", barcode)
                            if barcode:
                                shopify_barcode = odoo_product_obj.search([('barcode', '=', barcode)])

                            if shopify_barcode:
                                continue

                            grams_weight = variant.get('grams')
                            weight_unit = variant.get('weight_unit')
                            inventory_item_id = variant.get('inventory_item_id')

                            if weight_unit == 'kg':
                                grams_weight = grams_weight * 0.001
                                # convert to lb(s)
                                grams_weight = grams_weight * 2.20462
                                pass

                            if weight_unit == 'g':
                                grams_weight = grams_weight * 0.001
                                # convert to lb(s)
                                grams_weight = grams_weight * 0.00220462
                                pass

                            if weight_unit == 'lb':

                                weight_unit = weight_unit + '(s)'
                                if grams_weight:
                                    grams_weight = grams_weight * 0.00220462

                            if weight_unit == 'oz':
                                weight_unit = weight_unit + '(s)'
                                if grams_weight:
                                    grams_weight = grams_weight * 0.035274
                                    grams_weight = grams_weight * 0.0625

                            # product_uom_id = product_uom_obj.search([('name', '=', weight_unit)])
                            product_uom_id = product_uom_obj.search([('name', '=', 'lb(s)')])

                        p_vals = {
                            # 'price_extra': price_extra,
                            'image_medium': image_base64_vr,
                            'weight': grams_weight or False,
                            "default_code": sku,
                            "barcode": barcode,
                            "inventory_item_id": inventory_item_id,
                            'uom_id': product_uom_id.id,
                            'uom_po_id': product_uom_id.id,
                            'shopify_product_id': shopify_product_id,
                            'shopify_variant_id': variant_id,
                        }
                        # _logger.info("-------p_vals----111------: %s", p_vals)
                        updated_product_id = p_product_variant_id.write(p_vals)

                self._cr.commit()
            _logger.info("------shopify_template_count-------%s-", shopify_template_count)
            _logger.info("------product_product_count-------%s-", product_product_count)
            _logger.info("------product_tmpl_ids---count----: %s", product_tmpl_ids_count)

        except Exception as e:
            _logger.info("--Exception------create_all_products-----%s-", e)
        return True


    # Import Produts using Shopify Product Id
    @api.multi
    def import_products_using_shopify_product_id(self, instance, shopify_tmpl_id=False, update_price=False, update_templates=True,):
        product_obj = self.env['product.template']
        product_categ_obj = self.env['product.category']
        product_public_category_obj = self.env['product.public.category']
        attribute_name_obj = self.env['product.attribute']
        attribute_value_obj = self.env['product.attribute.value']
        attribute_line_obj = self.env['product.attribute.line']
        product_uom_obj = self.env['product.uom']
        product_id_count = 0
        rownum = 0
        product_tmpl_ids_count = 0
        shopify_template_count = 0
        response_template_not_data = 0
        shopify_product_id_count = 0
        count_row = 1

        fileobj = open('/opt/final_shopify_product_ids.csv', 'rb')
        str_csv_data = fileobj.read()
        list = csv.reader(StringIO.StringIO(str_csv_data), delimiter=',')

        for row in list:
            if row == '':
                continue
            if rownum == 0:
                rownum += 1
            else:
                _logger.info("-------------count_row-----------: %s", count_row)
                instance.connect_in_shopify()
                shop_url = instance.count_product_in_shopify()

                id = str(row[2]).strip()
                url = shop_url + "/products/" + str(id) + ".json"
                _logger.info("-------------url-----------: %s", url)

                request = requests.get(url)
                request_data = json.loads(request.text)
                _logger.info("------request_data-----: %s", request_data)

                response_template = request_data.get('product')
                _logger.info("-------------response_template-----------: %s", response_template)

                if not response_template:
                    response_template_not_data += 1
                    _logger.info("-----response_template_not_data------: %s", response_template_not_data)
                    continue

                # response_template = response_template.to_dict()
                img_var = response_template.get('image')
                image_base64 = ''
                if img_var:
                    img = img_var.get('src')
                    image = urllib2.urlopen(img)
                    imgs = image.read()
                    image_base64 = base64.encodestring(imgs)

                shopify_product_id = response_template.get('id')
                product_name = response_template.get('title')
                _logger.info("-------------product_name-----------: %s", product_name)

                attri_position1 = []
                attri_position2 = []
                attri_position3 = []
                value_position1 = []
                value_position2 = []
                value_position3 = []

                for variant_options in response_template.get('options'):
                    name = variant_options.get('name')
                    attribute_name_id = attribute_name_obj.search([('name', '=', name)])
                    _logger.info("------attribute_name_id------: %s", attribute_name_id)
                    if not attribute_name_id:
                        attribute_vals = {
                            'name': name,
                            'create_variant': True,
                        }
                        attribute_name_id = attribute_name_obj.create(attribute_vals)
                    if variant_options.get('position') == 1:
                        attri_position1.append(attribute_name_id.id)
                    elif variant_options.get('position') == 2:
                        attri_position2.append(attribute_name_id.id)
                    else:
                        attri_position3.append(attribute_name_id.id)

                    for values in variant_options.get('values'):
                        attribute_value_id = attribute_value_obj.search(
                            [('attribute_id', '=', attribute_name_id.id), ('name', '=', values)])
                        if not attribute_value_id:
                            attribute_value_vals = {
                                'attribute_id': attribute_name_id.id,
                                'name': values,
                            }
                            attribute_value_id = attribute_value_obj.create(attribute_value_vals)
                        if variant_options.get('position') == 1:
                            value_position1.append(attribute_value_id.id)
                        elif variant_options.get('position') == 2:
                            value_position2.append(attribute_value_id.id)
                        else:
                            value_position3.append(attribute_value_id.id)

                        attrivals = {
                            str(attri_position1): value_position1,
                            str(attri_position2): value_position2,
                            str(attri_position3): value_position3,
                        }
                product_type = response_template.get('product_type')
                if product_type:
                    product_categ_id = product_categ_obj.search([('name', '=', str(product_type))])
                    if not product_categ_id:
                        categ_vals = {'name': str(product_type),
                                      'property_valuation': 'manual_periodic'}
                        product_categ_id = product_categ_obj.create(categ_vals)

                    product_public_categ_id = product_public_category_obj.search([('name', '=', str(product_type))])
                    if not product_public_categ_id:
                        web_categ_vals = {'name': str(product_type), }
                        product_public_categ_id = product_public_category_obj.create(web_categ_vals)

                    product_categ_id = product_categ_id.id
                    product_public_categ_id = product_public_categ_id.id
                else:
                    product_categ_id = 1

                    product_public_categ_id = product_public_category_obj.search([('name', '=', 'General Category')])
                    if not product_public_categ_id:
                        web_categ_vals = {'name': 'General Category', }
                        product_public_categ_id = product_public_category_obj.create(web_categ_vals)
                    product_public_categ_id = product_public_categ_id.id

                for variant in response_template.get('variants'):
                    _logger.info("------variant------: %s", variant)
                    # barcode = str(variant.get('barcode', ''))
                    # shopify_barcode = product_obj.search([('barcode', '=', barcode)])
                    # _logger.info("-------------shopify_barcode-----------: %s", shopify_barcode)
                    shopify_template = product_obj.search(
                        [('shopify_product_id', '=', shopify_product_id), ('shopify_variant_id', '=', variant.get('id'))])
                    _logger.info("-------------shopify_template-----------: %s", shopify_template)
                    if shopify_template:
                        # product_barcode = None
                        if len(response_template.get('images')) > 1:
                            if variant.get('image_id'):
                                self.update_image(variant, response_template.get('images'), shopify_template)
                            else:
                                shopify_template.write({'image_medium': image_base64})
                        else:
                            vals = {'image_medium': image_base64}
                            shopify_template.write(vals)
                        _logger.info("-------shopify_template.shopify_variant_id-------: %s",
                                     shopify_template.shopify_variant_id)
                        _logger.info("-------variant.get('id')-------: %s", variant.get('id'))
                        if int(shopify_template.shopify_variant_id) == variant.get('id'):
                            # if variant.get('barcode'):
                            #     product_barcode = variant.get('barcode')
                            #     _logger.info("-------product_barcode-------: %s", product_barcode)
                            vals = {'list_price': variant.get('price'),
                                    # 'barcode': product_barcode,
                                    'categ_id': product_categ_id,
                                    'default_code': str(variant.get('sku', '')),
                                    'website_description': response_template.get('body_html'),
                                    'public_categ_ids': [(6, 0, [product_public_categ_id])],
                                    }
                            _logger.info("-----------vals-----------: %s", vals)
                            shopify_template.write(vals)
                            shopify_template_count += 1
                        continue

                    # if shopify_barcode:
                    #     shopify_barcode_count += 1
                    #     continue
                    # if barcode == 'None':
                    #     barcode = False

                    grams_weight = variant.get('grams')
                    weight_unit = variant.get('weight_unit')

                    if weight_unit == 'kg':
                        grams_weight = grams_weight * 0.001
                        pass

                    if weight_unit == 'g':
                        grams_weight = grams_weight * 0.001
                        pass
                    if weight_unit == 'lb':

                        weight_unit = weight_unit + '(s)'
                        if grams_weight:
                            grams_weight = grams_weight * 0.00220462

                    if weight_unit == 'oz':
                        weight_unit = weight_unit + '(s)'
                        if grams_weight:
                            grams_weight = grams_weight * 0.035274

                    product_uom_id = product_uom_obj.search([('name', '=', weight_unit)])

                    sku = str(variant.get('sku', ''))
                    if sku == 'None':
                        sku = False

                    price = variant.get('price')
                    variant_id = variant.get('id')
                    title = variant.get('title')
                    splitted_titles = title.split(' / ')

                    counter = 0
                    attribute_value_id0 = []
                    attribute_value_id1 = []
                    attribute_value_id2 = []

                    for split_title in splitted_titles:

                        if counter == 0:
                            if split_title:
                                sp = split_title.strip(' ')
                                attribute_value_id0 = attribute_value_obj.search(
                                    [('attribute_id', '=', attri_position1[0]), ('name', '=', sp)])
                        elif counter == 1:
                            if split_title:
                                sp1 = split_title.strip(' ')
                                attribute_value_id1 = attribute_value_obj.search(
                                    [('attribute_id', '=', attri_position2[0]), ('name', '=', sp1)])
                        elif counter == 2:
                            if split_title:
                                sp2 = split_title.strip(' ')
                                attribute_value_id2 = attribute_value_obj.search(
                                    [('attribute_id', '=', attri_position3[0]), ('name', '=', sp2)])
                        counter += 1

                    vals = {
                        'name': product_name,
                        'type': 'product',
                        'default_code': sku,
                        # 'barcode': barcode,
                        'list_price': price,
                        'image_medium': image_base64,
                        'weight': grams_weight or False,
                        'uom_id': product_uom_id.id,
                        'uom_po_id': product_uom_id.id,
                        'categ_id': product_categ_id,
                        'public_categ_ids': [(6, 0, [product_public_categ_id])],
                        'shopify_product_id': shopify_product_id,
                        'shopify_variant_id': variant_id,
                        'website_description': response_template.get('body_html'),
                    }
                    _logger.info("--------vals-----111------: %s", vals)
                    product_tmpl_ids = product_obj.create(vals)
                    _logger.info("-------------product_tmpl_ids-----------: %s", product_tmpl_ids)
                    product_tmpl_ids_count += 1
                    _logger.info("------product_tmpl_ids---count----: %s", product_tmpl_ids_count)
                    if attri_position1:
                        attribute_line_vals = {'product_tmpl_id': product_tmpl_ids.id,
                                               'attribute_id': attri_position1[0],
                                               'value_ids': [(6, 0, [attribute_value_id0.id])],
                                               }
                        _logger.info("-------------attribute_line_vals-----------: %s", attribute_line_vals)
                        attribute_line_ids1 = attribute_line_obj.create(attribute_line_vals)
                    if attri_position2:
                        attribute_line_vals = {'product_tmpl_id': product_tmpl_ids.id,
                                               'attribute_id': attri_position2[0],
                                               'value_ids': [(6, 0, [attribute_value_id1.id])],
                                               }
                        _logger.info("-------------attribute_line_vals-----------: %s", attribute_line_vals)
                        attribute_line_ids2 = attribute_line_obj.create(attribute_line_vals)
                    if attri_position3:
                        attribute_line_vals = {'product_tmpl_id': product_tmpl_ids.id,
                                               'attribute_id': attri_position3[0],
                                               'value_ids': [(6, 0, [attribute_value_id2.id])],
                                               }
                        _logger.info("-------------attribute_line_vals-----------: %s", attribute_line_vals)
                        attribute_line_ids3 = attribute_line_obj.create(attribute_line_vals)
                self._cr.commit()
                count_row += 1
            _logger.info("-------------shopify_template_count----fianl-------: %s", shopify_template_count)
            _logger.info('<<<<<<<<<<<product_id_count<<<<<<<< %s', product_id_count)

        return True

    # Import Products Tags using Shopify Product Id

    @api.multi
    def import_products_tags_using_shopify_product_id(self, instance, shopify_tmpl_id=False, update_price=False,
                                                 update_templates=True, ):
        product_obj = self.env['product.template']
        product_categ_obj = self.env['product.category']
        product_public_category_obj = self.env['product.public.category']
        attribute_name_obj = self.env['product.attribute']
        attribute_value_obj = self.env['product.attribute.value']
        attribute_line_obj = self.env['product.attribute.line']
        product_uom_obj = self.env['product.uom']
        product_id_count = 0
        rownum = 0
        product_tmpl_ids_count = 0
        shopify_template_count = 0
        response_template_not_data = 0
        shopify_product_id_count = 0
        count_row = 1

        fileobj = open('/opt/final_shopify_product_ids.csv', 'rb')
        str_csv_data = fileobj.read()
        list = csv.reader(StringIO.StringIO(str_csv_data), delimiter=',')

        shopify_product_ids=product_obj.search([('shopify_product_id','!=', False)])

        if shopify_product_ids:
            for product_id in shopify_product_ids:
                instance.connect_in_shopify()
                shop_url = instance.count_product_in_shopify()

                id = product_id.shopify_product_id
                url = shop_url + "/products/" + str(id) + ".json"
                request = requests.get(url)
                request_data = json.loads(request.text)
                _logger.info("------request_data-----: %s", request_data)

                response_template = request_data.get('product')
                _logger.info("-------------response_template-----------: %s", response_template)

                if not response_template:
                    response_template_not_data += 1
                    _logger.info("-----response_template_not_data------: %s", response_template_not_data)
                    continue

                product_tags = response_template.get('tags')
                splits_tags=[tags.strip() for tags in product_tags.split(',')]
                for tag in splits_tags:
                    product_tag_id=self.env['product.tags'].search([('name','=',tag)])
                    if product_tag_id:
                        shopify_product_ids.write({'tag_ids':[(4,product_tag_id.id)]})
                    else:
                       product_tag= self.env['product.tags'].create({'name':tag})
                       shopify_product_ids.write({'tag_ids':[(4,product_tag.id)]})

        return True
        _logger.info("-------------url-----------: %s", url)


    # Improt Customers from Shopify to Odoo
    @api.multi
    def import_customers(self, instance, cumstomer_temp_id):
        instance.connect_in_shopify()
        shop_url = instance.count_product_in_shopify()
        customer_count = requests.get(shop_url + "/customers/count.json")
        total_customer_count = json.loads(customer_count.text).get('count')
        _logger.info("------total_customer_count-----: %s", total_customer_count)
        pages = float(total_customer_count) / 250.0
        counter = int(math.ceil(pages))
        results = []
        count_id = 1
        list_partner_id = []
        no_name = []
        partner_id_create = 0
        partner_id_write = 0

        if cumstomer_temp_id:
            results = [shopify.Customer().find(cumstomer_temp_id)]
            _logger.info("------results-----: %s", results)
        else:
            while counter:
                cumstomer_ids = shopify.Customer().find(limit=250, page=counter)
                results += cumstomer_ids
                counter -= 1

        _logger.info("-----results-----: %s", results)
        _logger.info("-------len(results)------: %s", len(results))

        country_obj = self.env['res.country']
        state_obj = self.env['res.country.state']
        partner_obj = self.env['res.partner']

        for response_template in results:
            _logger.info("-------------response_template-----------: %s", response_template)
            response_template = response_template.to_dict()
            _logger.info("-------------response_template----data-------: %s", response_template)
            _logger.info("----------count_id-----: %s", count_id)
            count_id += 1

            partner_id = partner_obj.search([('shopify_customer_id', '=', response_template.get('id'))])
            _logger.info("-------------partner_id-----------: %s", partner_id)

            if partner_id:
                list_partner_id.append(partner_id)
                continue

            if not response_template.get('first_name') and not response_template.get('last_name'):
                no_name.append(response_template.get('id'))
                continue


            # Create res.partner
            partner_data = response_template.get('default_address')
            if partner_data:
                email = response_template.get('email')
                company_name = partner_data.get('company')
                if company_name:
                    company_ids = partner_obj.search([('name', '=', company_name)])
                    if not company_ids:
                        company_vals = {
                            'name': partner_data.get('company') or False,
                            'is_company': 'company',
                            'shopify_customer_id': response_template.get('id') or False,
                        }
                        company_ids = partner_obj.create(company_vals)
                        _logger.info("-------------company_ids-----------: %s", company_ids)
                        partner_id_create += 1

                else:
                    company_ids = False

                partner_ids = partner_obj.search([('email', '=', email)])

                if not partner_ids:
                    first_name = response_template.get('first_name')
                    last_name = response_template.get('last_name')
                    if not last_name and first_name:
                        name = first_name
                    elif not first_name and last_name:
                        name = last_name
                    elif first_name and last_name:
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
                                        'company_name_ept': company_name or False,
                                        'phone': phone or False,
                                        'company_type': 'person',
                                        'shopify_customer_id': response_template.get('id') or False,
                                        }
                        partner_ids = partner_obj.create(partner_vals)
                        _logger.info("-------------partner_ids-----------: %s", partner_ids)
                        partner_id_create += 1
                    else:
                        partner_vals = {'name': name,
                                        'state_id': state.id,
                                        'city': city,
                                        'zip': zip,
                                        'street': street,
                                        'street2': street1,
                                        'country_id': country.id,
                                        'email': email,
                                        'phone': phone or False,
                                        'company_type': 'person',
                                        'shopify_customer_id': response_template.get('id') or False,
                                        }
                        partner_ids = partner_obj.create(partner_vals)
                        _logger.info("-------------partner_ids-----------: %s", partner_ids)
                        partner_id_create += 1

            else:
                email = response_template.get('email')
                partner_ids = partner_obj.search([('email', '=', email)])

                first_name = response_template.get('first_name')
                last_name = response_template.get('last_name')
                if not last_name and first_name:
                    name = first_name
                elif not first_name and last_name:
                    name = last_name
                elif first_name and last_name:
                    name = first_name + ' ' + last_name

                if not partner_ids:
                    partner_vals = {
                        'name': name,
                        'company_type': 'person',
                        'email': email,
                        'shopify_customer_id': response_template.get('id') or False,
                    }
                    partner_ids = partner_obj.create(partner_vals)
                    _logger.info("-------------partner_ids-----------: %s", partner_ids)
                    partner_id_create += 1
                else:
                    partner_vals = {
                        'name': name,
                        'company_type': 'person',
                        'email': email,
                    }
                    partner_ids = partner_ids.write(partner_vals)
                    _logger.info("-------------partner_ids-----------: %s", partner_ids)
                    partner_id_write += 1
            self._cr.commit()
        _logger.info("-----partner_id_create-----: %s", partner_id_create)
        _logger.info("-----partner_id_write-----: %s", partner_id_write)

        _logger.info("-----list_partner_id---already_create---: %s", list_partner_id)
        _logger.info("-------len(list_partner_id)---already_create-----: %s", len(list_partner_id))
        _logger.info("-----no_name------: %s", no_name)
        _logger.info("-------len(no_name)--------: %s", len(no_name))

        return True


    # Import Stock from shopify
    @api.multi
    def import_stock(self, instance):
        pro_obj = self.env['product.product']
        instance.connect_in_shopify()
        shop_url = instance.count_product_in_shopify()
        list_prod_ids = pro_obj.search([('shopify_product_id', '!=', False)])
        try:
            if list_prod_ids:
                n = 50
                batches = [list_prod_ids[i:i + n] for i in range(0, len(list_prod_ids), n)]

                print("-batch", batches)

                for list_prod in batches:
                    list_prod_data = ''
                    i = 0
                    while i < (len(list_prod) - 1):
                        if list_prod[i].inventory_item_id:
                            list_prod_data += list_prod[i].inventory_item_id
                            list_prod_data += ','
                        i += 1
                    list_prod_data += str(list_prod[-1].inventory_item_id)
                    url = shop_url + "/inventory_levels.json?inventory_item_ids=" + str(list_prod_data)
                    response = requests.request("GET", url)
                    request_data = json.loads(response.text)
                    dict = {}

                    for invl in request_data.get('inventory_levels', ''):
                        if invl.get('inventory_item_id') in dict:
                            dict[invl.get('inventory_item_id')]['sum_qty'] += invl.get('available')
                        else:
                            dict.update({invl.get('inventory_item_id'): {'sum_qty': invl.get('available')}})
                    for d, value in dict.items():
                        prod_id = pro_obj.search([('inventory_item_id', '=', str(d))])
                        location_id = self.env.ref('stock.stock_location_stock').id
                        product_qty = value.get('sum_qty', 0.00)
                        if product_qty < 0.00:
                            product_qty = 0.00
                        stock_id = self.env['stock.change.product.qty'].create({
                             'product_id': prod_id.id, 'product_tmpl_id': prod_id.product_tmpl_id,
                             'new_quantity': product_qty,
                             'location_id': location_id,
                        })
                        if stock_id:
                            stock_id.change_product_qty()
        except Exception as e:
            _logger.info("--Exception----------import stock-----%s-", e)
        return True



    # To compare products
    @api.multi
    def compare_products(self, instance, shopify_tmpl_id=False, update_price=False, update_templates=True):
        odoo_product_obj = self.env['product.product']
        product_obj = self.env['product.template']
        instance.connect_in_shopify()
        shop_url = instance.count_product_in_shopify()
        product_count = requests.get(shop_url + "/products/count.json")
        total_product_count = json.loads(product_count.text).get('count')
        _logger.info("------total_product_count-----: %s", total_product_count)
        pages = float(total_product_count) / 250.0
        counter = int(math.ceil(pages))
        results = []
        product_counter = 0
        not_product_template = []
        not_product_product = []
        if shopify_tmpl_id:
            results = [shopify.Product().find(shopify_tmpl_id)]
            _logger.info("------results-----: %s", results)
        else:
            while counter:
                product_ids = shopify.Product().find(limit=250, page=counter)
                results += product_ids
                counter -= 1
        _logger.info("-----results-----: %s", results)
        _logger.info("-------len(results)------: %s", len(results))
        try:
            for response_template in results:
                product_counter += 1
                _logger.info("------product_counter-------%s-", product_counter)
                _logger.info("-------------response_template-----------: %s", response_template)
                response_template = response_template.to_dict()

                shopify_product_id = response_template.get('id')
                shopify_template = product_obj.search([('shopify_product_id', '=', shopify_product_id)])

                if not shopify_template:
                    not_product_template.append(response_template.get('id'))
                    continue

                if shopify_template:
                    # For variants
                    for variant in response_template.get('variants'):
                        product_product_id = odoo_product_obj.search([('shopify_variant_id', '=', variant.get('id'))])
                        if not product_product_id:
                            not_product_product.append(variant.get('id'))

            _logger.info("------not_product_template-------%s-", not_product_template)
            _logger.info("------not_product_product-------%s-", not_product_product)
            _logger.info("------len(not_product_template-------%s-", len(not_product_template))
            _logger.info("------len(not_product_product-------%s-", len(not_product_product))

        except Exception as e:
            _logger.info("--Exception------compare_products-----%s-", e)
        return True


    @api.multi
    def get_stock(self,shopify_product,warehouse_id,stock_type='virtual_available'):
        product=self.env['product.product'].with_context(warehouse=warehouse_id).browse(shopify_product.product_id.id)
        print "==============product========",product
        actual_stock=getattr(product, 'virtual_available')
        if actual_stock >= 1.00:
            if shopify_product.fix_stock_type=='fix':
                if shopify_product.fix_stock_value >=actual_stock:
                    return actual_stock
                else:
                    return shopify_product.fix_stock_value  
                              
            elif shopify_product.fix_stock_type == 'percentage':
                quantity = int(actual_stock * shopify_product.fix_stock_value)
                if quantity >= actual_stock:
                    return actual_stock
                else:
                    return quantity
        return actual_stock       

    @api.model
    def auto_update_stock_ept(self):
        shopify_instance_obj=self.env['shopify.instance.ept']
        ctx = dict(self._context) or {}
        shopify_instance_id = ctx.get('shopify_instance_id',False)
        if shopify_instance_id:
            instance=shopify_instance_obj.search([('id','=',shopify_instance_id)])
            self.update_stock_in_shopify(instance=instance)
        return True

    @api.model
    def update_stock_in_shopify(self,instance=False,products=False):
        transaction_log_obj=self.env['shopify.transaction.log']
        instances=[]
        if not instance:
            instances=self.env['shopify.instance.ept'].search([('stock_auto_export','=',True),('state','=','confirmed')])
        else:
            instances.append(instance)
        for instance in instances:  
            location_ids=instance.warehouse_id.lot_stock_id.child_ids.ids
            location_ids.append(instance.warehouse_id.lot_stock_id.id)
            if not products:
                shopify_products=self.search([('shopify_instance_id','=',instance.id),('exported_in_shopify','=',True)])      
            else:
                shopify_products=self.search([('shopify_instance_id','=',instance.id),('exported_in_shopify','=',True),('id','in',products.ids)])      
                
            instance.connect_in_shopify()
            
            for template in shopify_products:
                try:
                    new_product = shopify.Product().find(template.shopify_tmpl_id)
                except:
                    message="Template %s not found in shopify When update Stock"%(template.shopify_tmpl_id)
                    log=transaction_log_obj.search([('shopify_instance_id','=',instance.id),('message','=',message)])
                    if not log:
                        transaction_log_obj.create(
                                                    {'message':message,
                                                     'mismatch_details':True,
                                                     'type':'stock',
                                                     'shopify_instance_id':instance.id
                                                    })                        
                    continue
                    
                new_product.id=template.shopify_tmpl_id
                variants=[]
                info={}
                for variant in template.shopify_product_ids:
                    if  variant.variant_id:
                        quantity=self.get_stock(variant,instance.warehouse_id.id,instance.stock_field.name)
                        info.update({'id':variant.variant_id,'inventory_quantity':int(quantity)})
                        variants.append(info)
                        info={}
                if variants:
                    new_product.variants=variants
                    try:
                        new_product.save()
                    except:
                        message="Template %s removed in shopify"%(template.shopify_tmpl_id)
                        log=transaction_log_obj.search([('shopify_instance_id','=',instance.id),('message','=',message)])
                        if not log:
                            transaction_log_obj.create(
                                                        {'message':message,
                                                         'mismatch_details':True,
                                                         'type':'stock',
                                                         'shopify_instance_id':instance.id
                                                        })    
                        continue                    
            if not products:       
                instance.write({'last_inventory_update_time':datetime.now()})
            return True
    @api.model
    def update_price_in_shopify(self,instance,products):
        transaction_log_obj=self.env['shopify.transaction.log']
        instance.connect_in_shopify()
        
        if not products:
            shopify_products=self.search([('shopify_instance_id','=',instance.id),('exported_in_shopify','=',True)])      
        else:
            shopify_products=self.search([('shopify_instance_id','=',instance.id),('exported_in_shopify','=',True),('id','in',products.ids)])
                
        for template in shopify_products:
            try:
                new_product = shopify.Product().find(template.shopify_tmpl_id)
            except:
                message="Template %s not found in shopify When update Price"%(template.shopify_tmpl_id)
                log=transaction_log_obj.search([('shopify_instance_id','=',instance.id),('message','=',message)])
                if not log:
                    transaction_log_obj.create(
                                                    {'message':message,
                                                     'mismatch_details':True,
                                                     'type':'price',
                                                     'shopify_instance_id':instance.id
                                                    })      
                continue
            
            new_product.id=template.shopify_tmpl_id
            variants=[]
            info={}
            for variant in template.shopify_product_ids:
                # , context = self._context
                price=instance.pricelist_id.with_context(uom=variant.product_id.uom_id.id).price_get(variant.product_id.id,1.0,partner=False)[instance.pricelist_id.id]
                variant.variant_id and info.update({'id':variant.variant_id,'price':price})
                variants.append(info)
                info={}
            new_product.variants=variants
            new_product.save()
        return True


    @api.multi
    def shopify_unpublished(self):
        instance=self.shopify_instance_id
        instance.connect_in_shopify()
        if self.shopify_tmpl_id:
            
            new_product = shopify.Product.find(self.shopify_tmpl_id)
           
            if new_product:    
            
                new_product.id=self.shopify_tmpl_id
                new_product.published='false'
                new_product.published_at=None
                result=new_product.save()
                if result:
                    result_dict=new_product.to_dict()
                    updated_at=result_dict.get('updated_at')
                    published_at=result_dict.get('published_at')
                    self.write({'updated_at':updated_at,'published_at':False,'website_published':False})
        return True
    @api.multi
    def shopify_published(self):
        transaction_log_obj=self.env['shopify.transaction.log']
        instance=self.shopify_instance_id
        instance.connect_in_shopify()
        if self.shopify_tmpl_id:
           
            try:
                new_product = shopify.Product.find(self.shopify_tmpl_id)
            
                if new_product:    
            
                    new_product.published='true'
                    new_product.id=self.shopify_tmpl_id
                    published_at = datetime.utcnow() 
                    published_at = published_at.strftime("%Y-%m-%dT%H:%M:%S")
                    new_product.published_at=published_at
                    result=new_product.save()
                    if result:
                        result_dict=new_product.to_dict()
                        updated_at=result_dict.get('updated_at')
                        published_at=result_dict.get('published_at')
                        self.write({'updated_at':updated_at,'published_at':published_at,'website_published':True})
            except:
                message="Template %s not found in shopify When Publish"%(self.shopify_tmpl_id)
                log=transaction_log_obj.search([('shopify_instance_id','=',instance.id),('message','=',message)])
                if not log:
                    transaction_log_obj.create(
                                                    {'message':message,
                                                     'mismatch_details':True,
                                                     'type':'product',
                                                     'shopify_instance_id':instance.id
                                                    }) 
        return True

    @api.onchange("product_tmpl_id")
    def on_change_product(self):
        for record in self:
            record.name=record.product_tmpl_id.name
    @api.model
    def update_products_in_shopify(self,instance,templates):
        transaction_log_obj=self.env['shopify.transaction.log']
        instance.connect_in_shopify()

        for template in templates:
            try:
                new_product = shopify.Product().find(template.shopify_tmpl_id)
            except:
                message="Template %s not found in shopify When update Product"%(template.shopify_tmpl_id)
                log=transaction_log_obj.search([('shopify_instance_id','=',instance.id),('message','=',message)])
                if not log:
                    transaction_log_obj.create(
                                                    {'message':message,
                                                     'mismatch_details':True,
                                                     'type':'product',
                                                     'shopify_instance_id':instance.id
                                                    })
                continue
                
            new_product.id=template.shopify_tmpl_id            
            if template.description:
                new_product.body_html=template.description

            new_product.product_type=template.product_tmpl_id.categ_id.name
            
            new_product.tags=[tag.name for tag in template.tag_ids]
            
            if template.template_suffix:
                new_product.template_suffix=template.template_suffix

            images=[]
            image_position=1
            images_with_position={}
            for variant in template.shopify_product_ids:
                if variant.product_id.image_medium :
                    key=hashlib.md5(variant.product_id.image_medium).hexdigest()
                    if not images_with_position.has_key(key):
                        images_with_position.update({key:image_position})
                        image_position=image_position+1

            image_with_position=[]
            exist_images=[]
            for variant in template.shopify_product_ids:            
                image_info={}                
                if variant.product_id.image_medium :
                    key=hashlib.md5(variant.product_id.image_medium).hexdigest()
                    if key not in exist_images:
                        image_info.update({'attachment':variant.product_id.image_medium,'position':images_with_position.get(key)})
                        exist_images.append(key)
                        images.append(image_info)
                    image_with_position.append({'position':images_with_position.get(key),'variant':variant})
            if images:
                new_product.images=images                                


            new_product.title=template.name
            variants=[]
            info={}
            for variant in template.shopify_product_ids:
                info={}
                info.update({
                            'barcode':variant.product_id.barcode, 
                            'id':variant.variant_id
                             })
                print "========= barcode============", info
                if template.fulfillment_service=='manual':
                    info.update({
                                'fulfillment_service':'manual' 
                                 })
                info.update({
                             'grams':int(variant.product_id.weight*1000),
                             'weight':(variant.product_id.weight),
                             'weight_unit':'kg',
                             })
                if template.inventory_management=='shopify':
                    info.update({
                                 'inventory_management':template.inventory_management
                                 })
                if template.check_product_stock:
                    info.update({
                                 'inventory_policy':'continue'
                                 })
                    print "========= inventory_policy============", info
                info.update({
                             'requires_shipping':'true','sku':variant.default_code,
                             'taxable':template.taxable and 'true' or 'false',
                             'title':variant.name,
                             })
                print "========= title============", info
                option_index=0
                option_index_value=['option1','option2','option3']  
                attribute_value_obj=self.env['product.attribute.value']
                att_values=attribute_value_obj.search([('id','in',variant.product_id.attribute_value_ids.ids)],order="attribute_id")           
                for att_value in att_values:
                    info.update({option_index_value[option_index]:att_value.name})
                    option_index=option_index+1
                    if option_index>2:
                        break
                variants.append(info)         
            new_product.variants=variants
            variants=[]

            attribute_position=1
            if template.product_tmpl_id.attribute_line_ids:
                for attribute_line in template.product_tmpl_id.attribute_line_ids:
                    info={}
                    attribute=attribute_line.attribute_id
                    values=[]
                    value_ids=attribute_line.value_ids.ids
                    for variant in template.shopify_product_ids:
                        for value in variant.product_id.attribute_value_ids:
                            if value.id in value_ids and  value.id not in values:
                                values.append(value.id)
                    value_names=[]
                    for value in self.env['product.attribute.value'].browse(values):
                        value_names.append(value.name)
                    for value in attribute_line.value_ids:
                        if value.id not in values:
                            value_names.append(value.name)

                    info.update({'name':attribute.shopify_name or attribute.name ,'values':value_names ,'position':attribute_position })
                    print "=================info============================",info
                    variants.append(info)
                    attribute_position=attribute_position+1
                    if attribute_position>3:
                        break
                new_product.options = variants
            else:
                variants = []
            result=new_product.save()
            if result:
                result_dict=new_product.to_dict()
                created_at=result_dict.get('created_at')
                updated_at=result_dict.get('updated_at')
                published_at=result_dict.get('published_at')
                tmpl_id=result_dict.get('id')
                template.write({'created_at':created_at,'updated_at':updated_at,
                                'published_at':published_at,
                                'shopify_tmpl_id':tmpl_id,
                                'exported_in_shopify':True,
                                'total_variants_in_shopify':len(result_dict.get('variants'))

                                })
                for variant_dict in result_dict.get('variants'):
                    updated_at=variant_dict.get('updated_at')
                    created_at=variant_dict.get('created_at')
                    variant_id=variant_dict.get('id')
                    sku=variant_dict.get('sku')
                    shopify_variant=self.env['shopify.product.product.ept'].search([('default_code','=',sku),('shopify_instance_id','=',instance.id)])
                    shopify_variant and shopify_variant.write({
                                                               'variant_id':variant_id,
                                                               'updated_at':updated_at,
                                                               'created_at':created_at,
                                                               'exported_in_shopify':True
                                                               })
                for image in image_with_position:
                    for image_line in result_dict.get('images'):
                        if image.get('position')==image_line.get('position'):
                            image.get('variant').write({'shopify_image_id':image_line.get('id')})

                variants=[]
                info={}
                for variant in template.shopify_product_ids:
                    if variant.variant_id:
                        if variant.shopify_image_id:
                            info={}
                            info.update({'id':variant.variant_id,'image_id':variant.shopify_image_id})
                            variants.append(info)
                new_product.id=template.shopify_tmpl_id
                new_product.variants=variants
                new_product.save()

        return True


    @api.model
    def export_products_in_shopify(self,instance,templates,update_price,update_stock,publish):
        instance.connect_in_shopify()
        for template in templates:
            new_product = shopify.Product()
                        
            if template.description:
                new_product.body_html=template.description

            new_product.product_type=template.product_tmpl_id.categ_id.name
            # new_product.price=template.product_tmpl_id.list_price

            new_product.tags=[tag.name for tag in template.tag_ids]

            if template.template_suffix:
                new_product.template_suffix=template.template_suffix
            images=[]
            image_position=1
            images_with_position={}
            for variant in template.shopify_product_ids:
                if variant.product_id.image_medium :
                    key=hashlib.md5(variant.product_id.image_medium).hexdigest()
                    if not images_with_position.has_key(key):
                        images_with_position.update({key:image_position})
                        image_position=image_position+1

            image_with_position=[]
            exist_images=[]
            for variant in template.shopify_product_ids:            
                image_info={}                
                if variant.product_id.image_medium :
                    key=hashlib.md5(variant.product_id.image_medium).hexdigest()
                    if key not in exist_images:
                        image_info.update({'attachment':variant.product_id.image_medium,'position':images_with_position.get(key)})
                        exist_images.append(key)
                        images.append(image_info)
                    image_with_position.append({'position':images_with_position.get(key),'variant':variant})
            if images:
                new_product.images=images                                
            
            new_product.published=publish and 'true' or 'false'
            new_product.title=template.name
            variants=[]
            info={}
            for variant in template.shopify_product_ids:
                info={}
                info.update({
                            'barcode':variant.product_id.barcode, 
                             })

                if update_stock:
                    quantity=self.get_stock(variant,instance.warehouse_id.id,instance.stock_field.name)
                    info.update({'inventory_quantity':int(quantity)})
                
                if update_price:
                    # context = self._context
                    price=instance.pricelist_id.with_context(uom=variant.product_id.uom_id.id).price_get(variant.product_id.id,1.0,partner=False)[instance.pricelist_id.id]
                    info.update({'price':int(price)})

                if template.fulfillment_service=='manual':
                    info.update({
                                'fulfillment_service':'manual' 
                                 })
                info.update({
                             'grams':int(variant.product_id.weight*1000),
                             'weight':(variant.product_id.weight),
                             'weight_unit':'kg',
                             })
                if template.inventory_management=='shopify':
                    info.update({
                                 'inventory_management':template.inventory_management
                                 })
                if template.check_product_stock:
                    info.update({
                                 'inventory_policy':'continue'
                                 })                
                
                info.update({
                             'requires_shipping':'true','sku':variant.default_code,
                             'taxable':template.taxable and 'true' or 'false',
                             'title':variant.name,
                             })   
                option_index=0
                option_index_value=['option1','option2','option3']  
                attribute_value_obj=self.env['product.attribute.value']           
                att_values=attribute_value_obj.search([('id','in',variant.product_id.attribute_value_ids.ids)],order="attribute_id")
                for att_value in att_values:
                    info.update({option_index_value[option_index]:att_value.name})
                    option_index=option_index+1
                    if option_index>2:
                        break
                variants.append(info)         
            new_product.variants=variants
            variants=[]
            attribute_position=1
            for attribute_line in template.product_tmpl_id.attribute_line_ids:
                info={}
                attribute=attribute_line.attribute_id
                values=[]
                value_ids=attribute_line.value_ids.ids
                for variant in template.shopify_product_ids:
                    for value in variant.product_id.attribute_value_ids:
                        if value.id in value_ids and  value.id not in values:
                            values.append(value.id)
                value_names=[]
                for value in self.env['product.attribute.value'].browse(values):
                    value_names.append(value.name)                
                for value in attribute_line.value_ids:
                    if value.id not in values:
                        value_names.append(value.name)
                
                info.update({'name':attribute.shopify_name or attribute.name,'values':value_names,'position':attribute_position})
                variants.append(info)
                attribute_position=attribute_position+1
                if attribute_position>3:
                    break
            new_product.options=variants            
            result=new_product.save()
            if result:
                result_dict=new_product.to_dict()
                created_at=result_dict.get('created_at')
                updated_at=result_dict.get('updated_at')
                published_at=result_dict.get('published_at')
                tmpl_id=result_dict.get('id')                
                template.write({'created_at':created_at,'updated_at':updated_at,
                                'published_at':published_at,
                                'shopify_tmpl_id':tmpl_id,
                                'exported_in_shopify':True,
                                'total_variants_in_shopify':len(result_dict.get('variants'))                                     
                                })
                for variant_dict in result_dict.get('variants'):
                    updated_at=variant_dict.get('updated_at')
                    created_at=variant_dict.get('created_at')
                    variant_id=variant_dict.get('id')
                    sku=variant_dict.get('sku')
                    shopify_variant=self.env['shopify.product.product.ept'].search([('default_code','=',sku),('shopify_instance_id','=',instance.id)])
                    shopify_variant and shopify_variant.write({
                                                               'variant_id':variant_id,
                                                               'updated_at':updated_at,
                                                               'created_at':created_at,  
                                                               'exported_in_shopify':True                                                                                                                            
                                                               })                
                for image in image_with_position:
                    for image_line in result_dict.get('images'):
                        if image.get('position')==image_line.get('position'):
                            image.get('variant').write({'shopify_image_id':image_line.get('id')})
                variants=[]
                info={}
                for variant in template.shopify_product_ids:
                    if variant.variant_id:
                        if variant.shopify_image_id:
                            info={}                    
                            info.update({'id':variant.variant_id,'image_id':variant.shopify_image_id})        
                            variants.append(info)
                new_product.id=template.shopify_tmpl_id
                new_product.variants=variants

                new_product.save()
        return True

            
            
class shopify_product_product_ept(models.Model):
    _name="shopify.product.product.ept"
    
    _order='sequence'
    
    sequence=fields.Integer("Position",default=1)
    name=fields.Char("Title")    
    shopify_instance_id=fields.Many2one("shopify.instance.ept","Instance",required=1)
    default_code=fields.Char("Default Code")
    product_id=fields.Many2one("product.product","Product",required=1)
    shopify_template_id=fields.Many2one("shopify.product.template.ept","Shopify Template",required=1,ondelete="cascade")
    exported_in_shopify=fields.Boolean("Exported In Shopify")
    variant_id=fields.Char("Variant Id")
    fix_stock_type =  fields.Selection([('fix','Fix'),('percentage','Percentage')], string='Fix Stock Type')
    fix_stock_value = fields.Float(string='Fix Stock Value',digits=dp.get_precision("Product UoS"))
    created_at=fields.Datetime("Created At")
    updated_at=fields.Datetime("Updated At")
    shopify_image_id=fields.Char("Shopify Image Id")

class shopify_tags(models.Model):
    _name="shopify.tags"
    
    name=fields.Char("Name",required=1)
    sequence=fields.Integer("Sequence",required=1)


class product_product(models.Model):
    _inherit="product.product"

    shopify_variant_id = fields.Char("Shopify variant id")
    inventory_item_id = fields.Char('Inventory Item ID')
    # lst_price = fields.Float('Sale Price', digits=dp.get_precision('Product Price'), store=True, help="The sale price is managed from the product template. Click on the 'Variant Prices' button to set the extra attribute prices.")

    @api.multi
    def create_product_ept(self):
        not_found=[]
        for line in csv.reader(open('/tmp/product.csv','rb'),delimiter=',', quotechar='"'):      
            self.create({'name':line[0],'default_code':line[1]})
        return True


# get variant using sku
# https: // demacho - labs.myshopify.com / admin / products / search.json?query = sku:000425