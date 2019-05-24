from odoo import fields, models, tools
from odoo.exceptions import UserError

class Leads_Creation_Period_Report(models.TransientModel):
    _name='leads.creation.period.report'


    program = fields.Many2one('program.details', 'Program')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    all_programs=fields.Boolean('All Programs')
    by_period=fields.Selection([('day', 'By Days'),('week', 'By Weeks'),('month', 'By Months')],default='day',string='Period')



    def generate_report(self):
        if self.by_period:
            if self.by_period == 'day':
                view=self.env.ref('crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_report_view_pivot')
            elif self.by_period == 'week':
                view = self.env.ref('crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_by_week_report_view_pivot')
            else:
                view = self.env.ref('crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_by_month_report_view_pivot')
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
            if self.all_programs:
                res['domain']=[('create_date', '>=', self.start_date),('create_date', '<=', self.end_date),('program','!=',False)]
            else:
                if self.program:
                    res['domain'] = [('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date),('program','!=',False),('program','=',self.program.id)]
                else:
                    res['domain'] = [('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date),
                                     ('program', '!=', False)]
            return res