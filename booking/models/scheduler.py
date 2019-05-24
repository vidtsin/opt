from odoo import api, fields, models

class message_of_the_day(models.Model):
    _name = "oepetstore.message_of_the_day"

    @api.model
    def my_method(self):
        return {"hello": "world"}

    message = fields.Text()
    color = fields.Char(size=20)


class product111(models.Model):
    _name = "product1.product"

    max_quantity = fields.Float(string="Maximum Quantity")

    #  TEsting ..Getting product based on category  
 #    @api.multi  
	# def get_pro(self):
	# 	return True
		# import pdb;pdb.set_trace()
	 #    product_ids = self.env['product.template'].search([('categ_id.name', '=', 'Rooms')])
	 #    for record in product_ids:
	 #        vals = {
	 #            'id': record.id,
	 #            'name': record.name,
	 #        }