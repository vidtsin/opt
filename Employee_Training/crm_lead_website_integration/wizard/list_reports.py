from odoo import fields, models, tools
from odoo.exceptions import UserError

class CrmListReportsWizard(models.TransientModel):
    _name='crm.list.reports.wizard'

    program = fields.Many2one('program.details', 'Program')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    all_programs = fields.Boolean('All Programs')

    def generate_report(self):
        view=self.env.ref('crm_lead_website_integration.crm_leads_custom_list_report_tree_view')
        if not self.start_date:
            raise UserError(("Please specify the start date!"))
        if not self.end_date:
            raise UserError(("Please specify the end date!"))
        res={
            'type': 'ir.actions.act_window',
            'name': 'List Of Leads',
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'crm.lead',
            'views': [(view.id, 'tree')],
            'view_id': view.id,
        }
        if self.all_programs:
            res['domain']=[('create_date', '>=', self.start_date),('create_date', '<=', self.end_date),('program','!=',False)]
        else:
            if self.program:
                res['domain'] = [('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date),('program','!=',False),('program','=',self.program.id)]
            else:
                res['domain'] = [('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date),
                                 ('program', '!=', False)]
        return res