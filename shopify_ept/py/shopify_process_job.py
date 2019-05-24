from odoo  import models,fields
import odoo.addons.decimal_precision as dp

    

class shopify_transaction_log(models.Model):
    _name="shopify.transaction.log"
    _order='id desc'
    _rec_name = 'create_date'
    create_date=fields.Datetime("Create Date")
    mismatch_details=fields.Boolean("Mismatch Details")
    message=fields.Text("Message")
    type=fields.Selection([('sales','Sales'),('product','Product'),('collection','Collection'),('stock','Stock'),('price','Price')],string="Type")
    shopify_instance_id=fields.Many2one("shopify.instance.ept",string="Instance")