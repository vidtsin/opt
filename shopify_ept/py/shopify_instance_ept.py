from odoo import models,fields,api,_
from odoo.exceptions import Warning
# from odoo.addons.shopify_ept.shopify import *
from .. import shopify
class shopify_instance_ept(models.Model):
    _name="shopify.instance.ept"
    
    name = fields.Char(size=120, string='Name', required=True)
    company_id = fields.Many2one('res.company',string='Company', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    lang_id = fields.Many2one('res.lang', string='Language')
    order_prefix = fields.Char(size=10, string='Order Prefix')
    order_auto_import = fields.Boolean(string='Auto Order Import?')
    order_auto_update=fields.Boolean(string="Auto Order Update ?")
    stock_auto_export=fields.Boolean(string="Stock Auto Export?")    
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position')
    stock_field = fields.Many2one('ir.model.fields', string='Stock Field')
    country_id=fields.Many2one("res.country","Country")    
    api_key=fields.Char("API Key",required=True)
    password=fields.Char("Password",required=True)
    shared_secret=fields.Char("Secret Key",required=True)
    host=fields.Char("Host",required=True)
    shipment_charge_product_id=fields.Many2one("product.product","Shipment Fee",domain=[('type','=','service')])
    section_id=fields.Many2one('crm.team', 'Sales Team')
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Term')    
    discount_product_id=fields.Many2one("product.product","Discount",domain=[('type','=','service')])
    add_discount_tax=fields.Boolean("Calculate Discount Tax",default=False)
    last_inventory_update_time=fields.Datetime("Last Inventory Update Time")
    auto_closed_order=fields.Boolean("Auto Closed Order",default=False)
    state=fields.Selection([('not_confirmed','Not Confirmed'),('confirmed','Confirmed')],default='not_confirmed')
    workflow_config_ids=fields.One2many("sale.auto.workflow.configuration","shopify_instance_id","Workflows")
    multiple_tracking_number = fields.Boolean(string='One order can have multiple Tracking Number',default=False)
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
        except Exception,e:
            raise Warning(e)        
        raise Warning('Service working properly')
        
    @api.multi
    def reset_to_confirm(self):
        self.write({'state':'not_confirmed'})
        return True
    @api.multi
    def confirm(self):
        self.connect_in_shopify()
        try:
            shop_id = shopify.Shop.current()            
        except Exception,e:
            raise Warning(e)
        self.write({'state':'confirmed'})
        return True        
        
    @api.multi
    def show_shopify_credential(self):
        form = self.env.ref('shopify_ept.shopify_instance_credential_form', False)
        return {
            'name': _('Shopify MWS Credential'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'shopify.instance.ept',
            'view_id': form.id,
            'nodestroy': True,
            'target': 'new',
            'context': {},
            'res_id': self and self.ids[0] or False,
        }
        
    @api.model
    def connect_in_shopify(self):
        instance=self        
        shop=instance.host.split("//")
        if len(shop) == 2:
            shop_url = shop[0]+"//"+instance.api_key+":"+instance.password+"@"+shop[1]+"/admin"
        else :
            shop_url = "https://"+instance.api_key+":"+instance.password+"@"+shop[0]+"/admin"
        shopify.ShopifyResource.set_site(shop_url)        
        return True

    @api.model
    def count_product_in_shopify(self):
        instance = self
        shop = instance.host.split("//")
        if len(shop) == 2:
            shop_url = shop[0] + "//" + instance.api_key + ":" + instance.password + "@" + shop[1] + "/admin"
        else:
            shop_url = "https://" + instance.api_key + ":" + instance.password + "@" + shop[0] + "/admin"
        return shop_url

