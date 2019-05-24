from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    room_id = fields.Many2one('product.product', 'Room')
    sale_order_id = fields.Many2one('sale.order', 'Sale Order ID')
    pos_order_id = fields.Many2one('booking.info', 'Booking ID')
    parent_id = fields.Many2one('pos.order', string="Parent Id", store=True)
    
    
    # Add Room No. in POS Order
 
    
#    @api.model
#    def _order_fields(self, ui_order):
#        print"---------self-----------",self
#        print"----------ui_order----------",ui_order
#        res = super(PosOrder, self)._order_fields(ui_order)
#        print"----------res----------",res
#        
#
#        partner_id = self.env['res.partner'].search([('id', '=', ui_order['partner_id'])])
#        print"----------partner_id----------",partner_id
#        product_id = self.env['product.product'].search([('id', '=', partner_id.room_no)])
#        print"----------product_id----------",product_id
#        sale_line_id = self.env['sale.order.line'].search([('product_id', '=', product_id.id)])
#        print"----------sale_line_id----------",sale_line_id
#        for sale_line in sale_line_id:
#            if sale_line.order_id.state == 'sale':
#                order_id = sale_line.order_id
#        
#        if ui_order.has_key('room_no'):
#            res.update({
#                'room_no': partner_id.room_no,
#                'sale_order_id':order_id.id,
#            })
#        print"----------res----------",res
#        return res
#    
#   
#
#    # Use for add POS Order in 'POS Order' tab in sale order
#    @api.model
#    def create_from_ui(self, orders):
#        print"----------orders---------",orders
#        order_id_list = super(PosOrder, self).create_from_ui(orders)
#        print"----------order_id_list---------",order_id_list
#        for order_list in order_id_list:
#            order_id = self.env['pos.order'].browse(order_list)
#            print"----------order_id---------",order_id
##        if order_id.
#            _logger.error('<<<<<<<order_id<<<<%s', order_id)
#            update_id = order_id.write({'parent_id': order_id.id,})
#            print"----------update_id---------",update_id
#        return order_id_list

    @api.model
    def create_from_ui(self, orders):
        # Keep only new orders
        submitted_references = [o['data']['name'] for o in orders]
        pos_order = self.search([('pos_reference', 'in', submitted_references)])
        existing_orders = pos_order.read(['pos_reference'])
        existing_references = set([o['pos_reference'] for o in existing_orders])
        orders_to_save = [o for o in orders if o['data']['name'] not in existing_references]
        order_ids = []

        for tmp_order in orders_to_save:
            to_invoice = tmp_order['to_invoice']
            order = tmp_order['data']
            if to_invoice:
                self._match_payment_to_invoice(order)
            pos_order = self._process_order(order)
            
#            ---------To add POS to SO ---------------------------------
            
            for statement in pos_order.statement_ids: 
                print"----------statement------------",statement.journal_id
                print"----------statement------------",statement.name
                if statement.journal_id.add_to_room:
                    sale_line_id = self.env['sale.order.line'].search([('product_id', '=', pos_order.partner_id.room_id.id),
                          ('room_booking_status', '=', 'checkin')])
                    print"----------sale_line_id----------",sale_line_id
                    print"----------sale_line_id----------",sale_line_id.order_id
                    pos_order.update({'sale_order_id': sale_line_id.order_id.id,
                                      'room_id': pos_order.partner_id.room_id.id,
                                      'pos_order_id': sale_line_id.order_id.room_booking_id.id,
                                      })
#            ---------To add POS to SO ---------------------------------

            order_ids.append(pos_order.id)

            try:
                pos_order.action_pos_order_paid()
            except psycopg2.OperationalError:
                # do not hide transactional errors, the order(s) won't be saved!
                raise
            except Exception as e:
                _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))

            if to_invoice:
                pos_order.action_pos_order_invoice()
                pos_order.invoice_id.sudo().action_invoice_open()
        return order_ids




