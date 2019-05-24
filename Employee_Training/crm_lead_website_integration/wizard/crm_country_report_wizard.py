from odoo import fields, models, tools
from odoo.exceptions import UserError

class CrmCountryReportWizard(models.TransientModel):
    _name='crm.country.report.wizard'

    country = fields.Many2one('res.country', 'Country')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    all_country = fields.Boolean('All Country')

    def generate_report(self):
        view=self.env.ref('crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_report_view_pivot')
        if not self.start_date:
            raise UserError(("Please specify the start date!"))
        if not self.end_date:
            raise UserError(("Please specify the end date!"))
        res={
            'type': 'ir.actions.act_window',
            'name': 'Pipeline Analysis By Program by day',
            'view_type': 'pivot',
            'view_mode': 'pivot',
            'res_model': 'crm.opportunity.custom.report',
            'views': [(view.id, 'pivot')],
            'view_id': view.id,
        }
        if self.all_country:
            res['domain']=[('create_date', '>=', self.start_date),('create_date', '<=', self.end_date),('country','!=',False)]
        else:
            if self.country:
                res['domain'] = [('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date),('country','!=',False),('country','=',self.country.id)]
            else:
                res['domain'] = [('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date),
                                 ('country', '!=', False)]
        return res


