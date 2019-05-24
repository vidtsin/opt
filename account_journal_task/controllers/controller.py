from odoo import http,_
from odoo.addons.web.controllers.main import WebClient, Binary, Home

class Website(Home):

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        page = 'homepage'
        
    