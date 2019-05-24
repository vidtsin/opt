from odoo import models,fields,api
class res_partner(models.Model):
    _inherit="res.partner"
    company_name_ept=fields.Char("Company Name")
    shopify_customer_id=fields.Char("Shopify Cutstomer Id")