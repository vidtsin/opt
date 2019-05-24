from odoo import models, fields, api, _
import base64, urllib

class shopify_product_image_ept(models.Model):
    _name = 'shopify.product.image.ept'

    @api.one
    def set_image(self):
        for template in self:
            if template.url:          
                try:  
                    (filename, header) = urllib.urlretrieve(template.url)
                    with open(filename , 'rb') as f:
                        img = base64.b64encode(f.read())
                    template.url_image_id=img
                except Exception:
                    pass    
    is_image_url=fields.Boolean("Is Image Url ?",default=False)
    name = fields.Char(size=60, string='Name', required=True)
    shopify_product_tmpl_id = fields.Many2one('shopify.product.template.ept', string='Shopify Product')    
    url = fields.Char(size=600, string='Image URL')    
    instance_id=fields.Many2one("shopify.instance.ept",string="Instance",related="shopify_product_tmpl_id.instance_id",required=True,readonly=True)
    image_id=fields.Binary("Image")
    url_image_id=fields.Binary("Image",compute=set_image,store=False)
    shopify_image_id=fields.Char("Shopify Image Id")     