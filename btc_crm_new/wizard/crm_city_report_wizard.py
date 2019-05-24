from odoo import fields, models, tools
from odoo.exceptions import UserError

class CrmCityReportWizard(models.TransientModel):
    _name='crm.city.report.wizard'

    city = fields.Char('City')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    all_city=fields.Boolean('All City')

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
        if self.all_city:
            res['domain']=[('create_date', '>=', self.start_date),('create_date', '<=', self.end_date),('city','!=',False)]
        else:
            if self.city:
                res['domain'] = [('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date),('city','!=',False),('city','=',self.city)]
            else:
                res['domain'] = [('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date),
                                 ('city', '!=', False)]
        return res


