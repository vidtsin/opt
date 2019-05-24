# -*- coding: utf-8 -*-
from odoo import http

# class booking(http.Controller):
#     @http.route('/booking/booking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/booking/booking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('booking.listing', {
#             'root': '/booking/booking',
#             'objects': http.request.env['booking.booking'].search([]),
#         })

#     @http.route('/booking/booking/objects/<model("booking.booking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('booking.object', {
#             'object': obj
#         })