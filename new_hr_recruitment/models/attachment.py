from odoo import models, fields, api

class resume_letter(models.Model):
    _inherit = "ir.attachment"

    job_position = fields.Many2one('hr.job', string='Job Position')

    doc_id = fields.Many2one('hr.employee',string='Document')

    @api.model
    def default_get(self, fields_list):
        res = {}
        if self._context.get('active_id'):
            res['doc_id'] = self._context.get('active_id')
        return res


