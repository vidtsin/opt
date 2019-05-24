from odoo import models,fields,api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import time

class shopify_operations_ept(models.Model):
    _name="shopify.operations.ept"
    _order = "sequence,id"
    
    @api.model
    def find_shopify_cron(self,action_id):
        import_order_cron = self.env.ref('shopify_ept.ir_cron_import_shopify_orders',raise_if_not_found=False)
        update_order_cron = self.env.ref('shopify_ept.ir_cron_auto_update_order_status',raise_if_not_found=False)
        export_stock_cron = self.env.ref('shopify_ept.ir_cron_auto_export_inventory',raise_if_not_found=False)
        cron_ids = []
        if import_order_cron:
            cron_ids.append(import_order_cron.id)
        if update_order_cron:
            cron_ids.append(update_order_cron.id)
        if export_stock_cron:
            cron_ids.append(export_stock_cron.id)
        for instance in self.env['shopify.instance.ept'].search([('state','=','confirmed')]):
            export_stock_cron = self.env.ref('shopify_ept.ir_cron_auto_export_inventory_instance_%d'%(instance.id),raise_if_not_found=False)
            import_order_cron = self.env.ref('shopify_ept.ir_cron_import_shopify_orders_instance_%d'%(instance.id),raise_if_not_found=False)
            update_order_cron = self.env.ref('shopify_ept.ir_cron_auto_update_order_status_instance_%d'%(instance.id),raise_if_not_found=False)
            
            if import_order_cron:
                cron_ids.append(import_order_cron.id)
            if update_order_cron:
                cron_ids.append(update_order_cron.id)
            if export_stock_cron:
                cron_ids.append(export_stock_cron.id)        
        return cron_ids
            
    @api.one
    def _count_operations(self):
        if self.action_id and self.display_record_count:
            if self.action_id.res_model == 'ir.cron':
                cron_ids = self.find_shopify_cron(self.action_id)
                self.count_record = len(cron_ids) or 0
            else:    
                domain =[]
                if self.action_id.domain:
                    domain = eval(self.action_id.domain)
                count = self.env[self.action_id.res_model].search_count(domain)
                self.count_record = count or 0
            
    @api.multi
    def count_all(self):
        picking_obj=self.env['stock.picking']
        sale_order_obj=self.env['sale.order']
        product_obj=self.env['shopify.product.template.ept']
        collection_obj=self.env['shopify.collection.ept']
        invoice_obj=self.env['account.invoice']
        for record in self:

            pickings=picking_obj.search([('shopify_instance_id','!=',False),('state','=','confirmed')])
            record.count_picking_confirmed=len(pickings.ids)
            pickings=picking_obj.search([('shopify_instance_id','!=',False),('state','=','assigned')])
            record.count_picking_assigned=len(pickings.ids)
            pickings=picking_obj.search([('shopify_instance_id','!=',False),('state','=','partially_available')])
            record.count_picking_partial=len(pickings.ids)
            pickings=picking_obj.search([('shopify_instance_id','!=',False),('state','=','done')])
            record.count_picking_done=len(pickings.ids)
            
            

            count_picking_late=[('min_date', '<', time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)), ('state', 'in', ('assigned', 'waiting', 'confirmed', 'partially_available')),('shopify_instance_id','!=',False)]
            count_picking_backorders=[('backorder_id', '!=', False), ('state', 'in', ('confirmed', 'assigned', 'waiting', 'partially_available')),('shopify_instance_id','!=',False)]
            count_picking=[('state', 'in', ('assigned', 'waiting', 'confirmed', 'partially_available')),('shopify_instance_id','!=',False)]

            count_picking=picking_obj.search(count_picking)
            count_picking_late=picking_obj.search(count_picking_late)
            count_picking_backorders=picking_obj.search(count_picking_backorders)
            
            if count_picking:
                record.rate_picking_late=len(count_picking_late.ids)*100/len(count_picking.ids)
                record.rate_picking_backorders=len(count_picking_backorders.ids)*100/len(count_picking.ids)
            else:
                record.rate_picking_late=0
                record.rate_picking_backorders=0
            record.count_picking_late=len(count_picking_late.ids)
            record.count_picking_backorders=len(count_picking_backorders.ids)
            orders=sale_order_obj.search([('shopify_instance_id','!=',False),('state','in',['draft','sent'])])
            record.count_quotations=len(orders.ids)
            orders=sale_order_obj.search([('shopify_instance_id','!=',False),('state','not in',['draft','sent','cancel'])])
            record.count_orders=len(orders.ids)
            count_risky_orders=sale_order_obj.search([('shopify_instance_id','!=',False),('state','=','draft'),('is_risky_order','!=',False)])
            record.count_risky_orders=len(count_risky_orders.ids)


            products=product_obj.search([('shopify_instance_id','!=',False),('exported_in_shopify','=',True)])
            record.count_exported_products=len(products.ids)
            products=product_obj.search([('shopify_instance_id','!=',False),('exported_in_shopify','=',False)])
            record.count_ready_products=len(products.ids)
            products=product_obj.search([('shopify_instance_id','!=',False),('website_published','=',True)])
            record.count_published_products=len(products.ids)
            products=product_obj.search([('shopify_instance_id','!=',False),('website_published','=',False),('exported_in_shopify','=',True)])
            record.count_not_published_products=len(products.ids)
            
            collections=collection_obj.search([('shopify_instance_id','!=',False),('is_smart_collection','=',False)])
            record.count_custom_collection=len(collections.ids)
            collections=collection_obj.search([('shopify_instance_id','!=',False),('is_smart_collection','=',True)])
            record.count_smart_collection=len(collections.ids)
            
            invoices=invoice_obj.search([('shopify_instance_id','!=',False),('state','=','open'),('type','=','out_invoice')])
            record.count_open_invoices=len(invoices.ids)

            invoices=invoice_obj.search([('shopify_instance_id','!=',False),('state','=','paid'),('type','=','out_invoice')])
            record.count_paid_invoices=len(invoices.ids)
            
            invoices=invoice_obj.search([('shopify_instance_id','!=',False),('type','=','out_refund')])
            record.count_refund_invoices=len(invoices.ids)

            
    action_id = fields.Many2one('ir.actions.act_window',string='Action')
    url = fields.Char('Image URL')
    sequence = fields.Integer('Sequence')
    color = fields.Integer('Color')
    name = fields.Char('Name', translate=True, required=True)
    count_record = fields.Integer(compute=_count_operations, string='# Record')
    display_inline_image = fields.Boolean('Display Number of records in Kanban ?')
    display_outline_image = fields.Boolean('Display Number of records in Kanban ?')

    use_quotations=fields.Boolean('Quotations', help="Check this box to manage quotations")
    use_products=fields.Boolean("Products",help="Check this box to manage Products")
    use_invoices=fields.Boolean("Invoices",help="Check This box to manage Invoices")
    use_delivery_orders=fields.Boolean("Delivery Orders",help="Check This box to manage Delivery Orders")
    use_shopify_workflow=fields.Boolean("Use Shopify Workflow",help="Check This box to manage Shopify Workflow")
    use_log=fields.Boolean("Use Log",help="Check this box to manage Shopify Log")
    use_collection=fields.Boolean("Use Collection",help="Check this box to manage Collection")

    count_quotations=fields.Integer("Count Sales Quotations",compute="count_all")
    count_orders=fields.Integer("Count Sales Orders",compute="count_all")
    count_risky_orders=fields.Integer("Count Risky Orders",compute="count_all")

    count_exported_products=fields.Integer("Count Exported Products",compute="count_all")
    count_ready_products=fields.Integer("Count Exported Products",compute="count_all")
    count_published_products=fields.Integer("Count Exported Products",compute="count_all")
    count_not_published_products=fields.Integer("Count Exported Products",compute="count_all")

    count_picking_confirmed=fields.Integer(string="Count Picking Waiting",compute="count_all")
    count_picking_assigned=fields.Integer(string="Count Picking Waiting",compute="count_all")
    count_picking_partial=fields.Integer(string="Count Picking Waiting",compute="count_all")
    count_picking_done=fields.Integer(string="Count Picking Waiting",compute="count_all")
    
    count_custom_collection=fields.Integer(string="Count Custom Collection",compute="count_all")
    count_smart_collection=fields.Integer(string="Count Smart Collection",compute="count_all")

    count_open_invoices=fields.Integer(string="Count Open Invoices",compute="count_all")
    count_paid_invoices=fields.Integer(string="Count Open Invoices",compute="count_all")
    count_refund_invoices=fields.Integer(string="Count Refund Invoices",compute="count_all")

    rate_picking_late=fields.Integer(string="Count Rate Pickings",compute="count_all")
    rate_picking_backorders=fields.Integer(string="Count Back Orders",compute="count_all")
    count_picking_late=fields.Integer(string="Count Rate Pickings",compute="count_all")
    count_picking_backorders=fields.Integer(string="Count Back Orders",compute="count_all")

    @api.multi
    def view_data(self):
        result = {}
        if self.action_id:
            result = self.action_id and self.action_id.read()[0] or {}
            if self.action_id.res_model == 'ir.cron':
                cron_ids = self.find_shopify_cron(self.action_id)
                result['domain'] = "[('id','in',[" + ','.join(map(str, cron_ids)) + "])]"        
            else:
                result = self.action_id and self.action_id.read()[0] or {}
        return result   
    
    
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(shopify_operations_ept, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        return res  