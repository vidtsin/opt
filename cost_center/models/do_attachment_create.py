from odoo import fields,models,api,_
import base64

class donation_donation(models.Model):
    _inherit = 'donation.donation'


    # function will create donation attachment of donor
    @api.model
    def create(self, vals):
        res = super(donation_donation, self).create(vals)
        ir_attachment_obj = self.env['ir.attachment']

        result = self.env['report'].sudo().get_pdf([res.id], 'cost_center.report_donation_print_save')
        result = base64.b64encode(result)

        attachment_vals = {
            'name': 'Donation of '+res.partner_id.name+'.pdf',
            'datas':result,
            'res_id': res.id,
            'datas_fname': 'Donation of '+res.partner_id.name+'.pdf',
            'res_model': 'donation.donation',
            'type':'binary',
            }

        ir_attachment_obj.create(attachment_vals)

        return res

