from odoo import models,fields,api
class res_partner(models.Model):
    _inherit="res.partner"
    

    @api.multi
    def _commercial_fields(self):
        result = super(res_partner, self)._commercial_fields()
        if 'last_reconciliation_date' in result:
            result.remove('last_reconciliation_date')
        return result