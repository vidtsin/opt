from odoo import models,fields,api
from .. import shopify


class account_move_line(models.Model):
    _inherit="account.move.line"
    
    updated_in_shopify=fields.Boolean("Updated In Shopify",default=False)
    
class account_invoice(models.Model):
    _inherit="account.invoice"
    
    shopify_instance_id=fields.Many2one("shopify.instance.ept","Instances")
    is_refund_in_shopify=fields.Boolean("Refund In Shopify",default=False)
    source_invoice_id = fields.Many2one('account.invoice','Source Invoice')
    picking_id = fields.Many2one('stock.picking','Picking')
    
    @api.multi
    def refund_in_shopify(self):
        self.ensure_one()
        for refund in self:
            if not refund.shopify_instance_id:
                continue
            refund.shopify_instance_id.connect_in_shopify()

            if refund.source_invoice_id:
                lines=self.env['sale.order.line'].search([('invoice_lines.invoice_id','=',refund.source_invoice_id.id)])
                order_ids=[line.order_id.id for line in lines]
                orders=order_ids and self.env['sale.order'].browse(list(set(order_ids))) or []
                
            elif refund.picking_id:
                for move in refund.picking_id.move_lines:
                    if move.procurement_id.sale_line_id:
                        orders = move.procurement_id.sale_line_id.order_id
                        break
                    
            for order in orders:
                transaction=shopify.Transaction()
                transaction.create({'amount':refund.amount_total,'kind':'refund','order_id':order.shopify_order_id,'currency':refund.currency_id.name})
            refund.write({'is_refund_in_shopify':True})
        return True

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        
        val=super(account_invoice,self)._prepare_refund(invoice=invoice, date_invoice=date_invoice, date=date, description=description, journal_id=journal_id)
        invoice_id = self.env.context.get('active_id', False)
        val.update({'source_invoice_id':invoice_id})
        return val
    
class sale_order(models.Model):
    _inherit="sale.order"
 
    def _prepare_invoice(self):    
        inv_val=super(sale_order,self)._prepare_invoice()        
        if self.shopify_instance_id:
            inv_val.update({'shopify_instance_id':self.shopify_instance_id.id})
            
        return inv_val
    
class stock_picking(models.Model):
    _inherit="stock.picking"
    
    def _create_invoice_from_picking(self, cr, uid, picking, vals, context=None):
        if picking.sale_id and picking.sale_id.shopify_instance_id:                                         
            vals.update({'shopify_instance_id':picking.sale_id.shopify_instance_id.id})
        return super(stock_picking,self)._create_invoice_from_picking(cr,uid,picking,vals,context)
