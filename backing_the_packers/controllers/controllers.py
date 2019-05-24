# -*- coding: utf-8 -*-
from openerp import http

# class BackingThePackers(http.Controller):
#     @http.route('/backing_the_packers/backing_the_packers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/backing_the_packers/backing_the_packers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('backing_the_packers.listing', {
#             'root': '/backing_the_packers/backing_the_packers',
#             'objects': http.request.env['backing_the_packers.backing_the_packers'].search([]),
#         })

#     @http.route('/backing_the_packers/backing_the_packers/objects/<model("backing_the_packers.backing_the_packers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('backing_the_packers.object', {
#             'object': obj
#         })