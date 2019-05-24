# -*- coding: utf-8 -*-

from openerp import models, fields, api


    
class sale_order(models.Model):
    _inherit = 'sale.order'
    
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('checked_in','Checked In'),
        ('sale', 'Sales Order'),
        ('done', 'Checked Out'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
        
    @api.multi
    def sale_check_in(self):
        for order in self:
            order.write({'state': 'checked_in'})
        return True
    
    @api.multi
    def sale_checked_in(self):
        return True
        
    def get_payment_vals(self):
        """ Hook for extension """
        return {
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
        }
           
    @api.multi
    def make_payment(self):
        view_ref = self.env['ir.model.data'].get_object_reference('account', 'view_account_payment_form')
        view_id = view_ref[1] if view_ref else False
        cxt = {}
        #view_id = self.env.ref('account.view_account_payment_form').id
    	cxt.update({'payment_type': "inbound",'default_partner_id': self.partner_id.id})
    	return {
            'name':'Make Payment',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'account.payment',
            'type':'ir.actions.act_window',
            #'res_id':self.id,
            'view_id':view_id,
            'target':'new',
            'context': cxt
        }
        
class product_template(models.Model):
    _inherit = 'product.template'
    
#    def _default_category(self, cr, uid, context=None):
#        if context is None:
#            context = {}
#        md = self.pool.get('ir.model.data')
#        print md
#        # = md.get_object_reference(cr, uid, 'backing_the_packers', 'product_categ_1')[1]
#        res = False
#        try:
#            res = md.get_object_reference(cr, uid, 'backing_the_packers', 'product_categ_1')[1]
#        except ValueError:
#            res = False
#        return res
        
    is_room = fields.Boolean(string="Is a Room?")
    
 #   _defaults = {
 #       'list_price': 100,
 #       'is_room': 1,
 #       'categ_id' : _default_category,
 #       'available_in_pos' : False,
 #       'type' : 'service',
 #   }
    

    

    
    
        

