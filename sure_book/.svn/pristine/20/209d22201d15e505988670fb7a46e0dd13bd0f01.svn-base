from odoo import api, fields, models

class check_in_room(models.Model):
    _name = "check.room"
    
    name = fields.Char('Name')
    check_in_room_ids = fields.One2many('check.room.line','check_in_room_id',string='Check In form')


class check_in_room_line(models.Model):
    _name = "check.room.line"

    name = fields.Char('Name')
    product_id = fields.Many2one('product.product',string='Room')
    partner_id = fields.Many2one('res.partner',string='Name')
    email = fields.Char('Email')
    mobile = fields.Char('Mobile')
    id_passport = fields.Char('ID/PASSPORT')
    check_in_room_id = fields.Many2one('check.room',string='Check In Room')
    booking_info_id = fields.Many2one('booking.info',string='Booking Info')
    
    
    
    @api.multi
    @api.onchange('partner_id')
    def product_id_change(self):
        self.email = self.partner_id.email
        self.mobile = self.partner_id.mobile
        self.id_passport = self.partner_id.id_passport
        