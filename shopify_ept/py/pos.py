from odoo import models,fields,api


class pos_order(models.Model):
    _inherit="pos.order"

    shopify_name=fields.Char("Shopify Name",readonly="True")
    shopify_id=fields.Char("Shopify ID",readonly="True")


