from odoo import models,fields,api,_
from odoo.exceptions import Warning
from .. import shopify
# from odoo.addons.shopify_ept.shopify import *
from datetime import datetime
from dateutil.relativedelta import relativedelta

_intervalTypes = {
    'work_days': lambda interval: relativedelta(days=interval),
    'days': lambda interval: relativedelta(days=interval),
    'hours': lambda interval: relativedelta(hours=interval),
    'weeks': lambda interval: relativedelta(days=7*interval),
    'months': lambda interval: relativedelta(months=interval),
    'minutes': lambda interval: relativedelta(minutes=interval),
}

class shopify_instance_config(models.TransientModel):
    _name = 'res.config.shopify.instance'
    
    name = fields.Char("Instance Name")
    api_key=fields.Char("API Key",required=True)
    password=fields.Char("Password",required=True)
    shared_secret=fields.Char("Secret Key",required=True)
    host=fields.Char("Host",required=True)
    country_id = fields.Many2one('res.country',string = "Country",required=True)
    @api.multi
    def test_shopify_connection(self):
        shop=self.host.split("//")
        if len(shop) == 2:
            shop_url = shop[0]+"//"+self.api_key+":"+self.password+"@"+shop[1]+"/admin"
        else :
            shop_url = "https://"+self.api_key+":"+self.password+"@"+shop[0]+"/admin"
        shopify.ShopifyResource.set_site(shop_url)
        try:
            shop_id = shopify.Shop.current()
        except Exception, e:
            raise Warning(e)    
        self.env['shopify.instance.ept'].create({'name':self.name,
                                                 'api_key':self.api_key,                                                 
                                                 'password':self.password,
                                                 'shared_secret':self.shared_secret,
                                                 'host':self.host,
                                                 'country_id':self.country_id.id,
                                                 'company_id':self.env.user.company_id.id 
                                                        })        
        return True
    
class shopify_config_settings(models.TransientModel):
    _name = 'shopify.config.settings'
    _inherit = 'res.config.settings'
    
    @api.model
    def _default_instance(self):
        instances = self.env['shopify.instance.ept'].search([])
        return instances and instances[0].id or False
    
   
    @api.model
    def _get_default_company(self):
        company_id = self.env.user._get_company()
        if not company_id:
            raise Warning(_('There is no default company for the current user!'))
        return company_id
    
    multiple_tracking_number = fields.Boolean(string='One order can have multiple Tracking Number ?',default=False)   
    shopify_instance_id = fields.Many2one('shopify.instance.ept', 'Instance', default=_default_instance)
    warehouse_id = fields.Many2one('stock.warehouse',string = "Warehouse")
    company_id = fields.Many2one('res.company',string='Company')
    country_id = fields.Many2one('res.country',string = "Country")
    lang_id = fields.Many2one('res.lang', string='Language')
    order_prefix = fields.Char(size=10, string='Order Prefix')
    add_discount_tax=fields.Boolean("Calculate Discount Tax",default=False)
    order_auto_import = fields.Boolean(string='Auto Order Import?')
    order_auto_update=fields.Boolean(string="Auto Order Update ?")
    stock_auto_export=fields.Boolean(string="Stock Auto Export?")    

    stock_field = fields.Many2one('ir.model.fields', string='Stock Field')
    
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Term')
    
    shipment_charge_product_id=fields.Many2one("product.product","Shipment Fee",domain=[('type','=','service')])

    discount_product_id=fields.Many2one("product.product","Discount",domain=[('type','=','service')],required=False)

    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position')
    
    auto_closed_order=fields.Boolean("Auto Closed Order",Default=False)
    
    section_id=fields.Many2one('crm.team', 'Sales Team')
    inventory_export_interval_number = fields.Integer('Export stock Interval Number',help="Repeat every x.")
    inventory_export_interval_type = fields.Selection( [('minutes', 'Minutes'),
            ('hours','Hours'), ('work_days','Work Days'), ('days', 'Days'),('weeks', 'Weeks'), ('months', 'Months')], 'Export Stock Interval Unit')
    
    order_import_interval_number = fields.Integer('Import Order Interval Number',help="Repeat every x.")
    order_import_interval_type = fields.Selection( [('minutes', 'Minutes'),
            ('hours','Hours'), ('work_days','Work Days'), ('days', 'Days'),('weeks', 'Weeks'), ('months', 'Months')], 'Import Order Interval Unit')
    
    order_update_interval_number = fields.Integer('Update Order Interval Number',help="Repeat every x.")
    order_update_interval_type = fields.Selection( [('minutes', 'Minutes'),
            ('hours','Hours'), ('work_days','Work Days'), ('days', 'Days'),('weeks', 'Weeks'), ('months', 'Months')], 'Update Order Interval Unit')    
        
    @api.onchange('shopify_instance_id')
    def onchange_instance_id(self):
        values = {} 
        context = dict(self._context or {})
        instance = self.shopify_instance_id or False
        self.company_id=instance and instance.company_id and instance.company_id.id or False
        self.warehouse_id = instance and instance.warehouse_id and instance.warehouse_id.id or False
        self.country_id = instance and instance.country_id and instance.country_id.id or False
        self.lang_id = instance and instance.lang_id and instance.lang_id.id or False
        self.order_prefix = instance and instance.order_prefix and instance.order_prefix
        self.stock_field = instance and instance.stock_field and instance.stock_field.id or False
        self.pricelist_id = instance and instance.pricelist_id and instance.pricelist_id.id or False
        self.payment_term_id = instance and instance.payment_term_id and instance.payment_term_id.id or False 
        self.shipment_charge_product_id = instance and instance.shipment_charge_product_id and instance.shipment_charge_product_id.id or False
        self.fiscal_position_id = instance and instance.fiscal_position_id and instance.fiscal_position_id.id or False
        self.discount_product_id=instance and instance.discount_product_id and instance.discount_product_id.id or False
        self.add_discount_tax=instance and instance.add_discount_tax
        self.order_auto_import=instance and instance.order_auto_import
        self.stock_auto_export=instance and instance.stock_auto_export
        self.auto_closed_order=instance and instance.auto_closed_order
        self.order_auto_update=instance and instance.order_auto_update
        self.section_id=instance and instance.section_id and instance.section_id.id or False
        self.multiple_tracking_number=instance and instance.multiple_tracking_number or False
        try:
            inventory_cron_exist = instance and self.env.ref('shopify_ept.ir_cron_auto_export_inventory_instance_%d'%(instance.id))
        except:
            inventory_cron_exist=False
        if inventory_cron_exist:
            self.inventory_export_interval_number=inventory_cron_exist.interval_number or False
            self.inventory_export_interval_type=inventory_cron_exist.interval_type or False
            
        try:
            order_import_cron_exist = instance and self.env.ref('shopify_ept.ir_cron_import_shopify_orders_instance_%d'%(instance.id))
        except:
            order_import_cron_exist=False
        if order_import_cron_exist:
            self.order_import_interval_number = order_import_cron_exist.interval_number or False
            self.order_import_interval_type = order_import_cron_exist.interval_type or False
        try:
            order_update_cron_exist = instance and self.env.ref('shopify_ept.ir_cron_auto_update_order_status_instance_%d'%(instance.id))
        except:
            order_update_cron_exist=False
        if order_update_cron_exist:
            self.order_update_interval_number= order_update_cron_exist.interval_number or False
            self.order_update_interval_type= order_update_cron_exist.interval_type or False

    @api.multi
    def execute(self):
        instance = self.shopify_instance_id
        values = {}
        res = super(shopify_config_settings,self).execute()
        if instance:
            values['company_id'] = self.company_id and self.company_id.id or False
            values['warehouse_id'] = self.warehouse_id and self.warehouse_id.id or False
            values['country_id'] = self.country_id and self.country_id.id or False
            values['lang_id'] = self.lang_id and self.lang_id.id or False
            values['order_prefix'] = self.order_prefix and self.order_prefix
            values['stock_field'] = self.stock_field and self.stock_field.id or False
            values['pricelist_id'] = self.pricelist_id and self.pricelist_id.id or False
            values['payment_term_id'] = self.payment_term_id and self.payment_term_id.id or False 
            values['shipment_charge_product_id'] = self.shipment_charge_product_id and self.shipment_charge_product_id.id or False
            values['fiscal_position_id'] = self.fiscal_position_id and self.fiscal_position_id.id or False
            values['discount_product_id']=self.discount_product_id.id or False
            values['add_discount_tax']=self.add_discount_tax
            values['order_auto_import']=self.order_auto_import
            values['stock_auto_export']=self.stock_auto_export
            values['auto_closed_order']=self.auto_closed_order
            values['order_auto_update']=self.order_auto_update
            values['section_id']=self.section_id and self.section_id.id or False
            values['multiple_tracking_number']=self.multiple_tracking_number
            instance.write(values)
            self.setup_inventory_export_cron(instance)
            self.setup_order_import_cron(instance)
            self.setup_order_update_cron(instance)                 

        return res   
    @api.multi   
    def setup_inventory_export_cron(self,instance):
        if self.stock_auto_export:
            try:                
                cron_exist = self.env.ref('shopify_ept.ir_cron_auto_export_inventory_instance_%d'%(instance.id))
            except:
                cron_exist=False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.inventory_export_interval_type](self.inventory_export_interval_number)
            vals = {'active' : True,
                    'interval_number':self.inventory_export_interval_number,
                    'interval_type':self.inventory_export_interval_type,
                    'nextcall':nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                    'args':"([{'shopify_instance_id':%d}])"%(instance.id)}
            if cron_exist:
                vals.update({'name' : cron_exist.name})
                cron_exist.write(vals)
            else:
                try:                    
                    export_stock_cron = self.env.ref('shopify_ept.ir_cron_auto_export_inventory')
                except:
                    export_stock_cron=False
                if not export_stock_cron:
                    raise Warning('Core settings of Shopify are deleted, please upgrade Shopify module to back this settings.')
                
                name = instance.name + ' : ' +export_stock_cron.name
                vals.update({'name':name})
                new_cron = export_stock_cron.copy(default=vals)
                self.env['ir.model.data'].create({'module':'shopify_ept',
                                                  'name':'ir_cron_auto_export_inventory_instance_%d'%(instance.id),
                                                  'model': 'ir.cron',
                                                  'res_id' : new_cron.id,
                                                  'noupdate' : True
                                                  })
        else:
            try:
                cron_exist = self.env.ref('shopify_ept.ir_cron_auto_export_inventory_instance_%d'%(instance.id))
            except:
                cron_exist=False
            if cron_exist:
                cron_exist.write({'active':False})        
        return True
            
    @api.multi   
    def setup_order_import_cron(self,instance):
        if self.order_auto_import:
            try:
                cron_exist = self.env.ref('shopify_ept.ir_cron_import_shopify_orders_instance_%d'%(instance.id))
            except:
                cron_exist=False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.order_import_interval_type](self.order_import_interval_number)
            vals = {
                    'active' : True,
                    'interval_number':self.order_import_interval_number,
                    'interval_type':self.order_import_interval_type,
                    'nextcall':nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                    'args':"([{'shopify_instance_id':%d}])"%(instance.id)}
                    
            if cron_exist:
                vals.update({'name' : cron_exist.name})
                cron_exist.write(vals)
            else:
                try:
                    import_order_cron = self.env.ref('shopify_ept.ir_cron_import_shopify_orders')
                except:
                    import_order_cron=False
                if not import_order_cron:
                    raise Warning('Core settings of Shopify are deleted, please upgrade Shopify module to back this settings.')
                
                name = instance.name + ' : ' +import_order_cron.name
                vals.update({'name' : name})
                new_cron = import_order_cron.copy(default=vals)
                self.env['ir.model.data'].create({'module':'shopify_ept',
                                                  'name':'ir_cron_import_shopify_orders_instance_%d'%(instance.id),
                                                  'model': 'ir.cron',
                                                  'res_id' : new_cron.id,
                                                  'noupdate' : True
                                                  })
        else:
            try:
                cron_exist = self.env.ref('shopify_ept.ir_cron_import_shopify_orders_instance_%d'%(instance.id))
            except:
                cron_exist=False
            
            if cron_exist:
                cron_exist.write({'active':False})
        return True
    @api.multi   
    def setup_order_update_cron(self,instance):
        if self.order_auto_update:
            try:
                cron_exist = self.env.ref('shopify_ept.ir_cron_auto_update_order_status_instance_%d'%(instance.id))
            except:
                cron_exist=False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.order_update_interval_type](self.order_update_interval_number)
            vals = {'active' : True,
                    'interval_number':self.order_update_interval_number,
                    'interval_type':self.order_update_interval_type,
                    'nextcall':nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                    'args':"([{'shopify_instance_id':%d}])"%(instance.id)}
                    
            if cron_exist:
                vals.update({'name' : cron_exist.name})
                cron_exist.write(vals)
            else:
                try:
                    update_order_cron = self.env.ref('shopify_ept.ir_cron_auto_update_order_status')
                except:
                    update_order_cron=False
                if not update_order_cron:
                    raise Warning('Core settings of Shopify are deleted, please upgrade Shopify module to back this settings.')
                
                name = instance.name + ' : ' +update_order_cron.name
                vals.update({'name' : name}) 
                new_cron = update_order_cron.copy(default=vals)
                self.env['ir.model.data'].create({'module':'shopify_ept',
                                                  'name':'ir_cron_auto_update_order_status_instance_%d'%(instance.id),
                                                  'model': 'ir.cron',
                                                  'res_id' : new_cron.id,
                                                  'noupdate' : True
                                                  })
        else:
            try:
                cron_exist = self.env.ref('shopify_ept.ir_cron_auto_update_order_status_instance_%d'%(instance.id))
            except:
                cron_exist=False
            if cron_exist:
                cron_exist.write({'active':False})
        return True            
        