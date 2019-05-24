from odoo import fields, models, tools
from odoo.exceptions import UserError
from datetime import datetime

class CrmComparativeReportWizard(models.TransientModel):
    _name='crm.comparative.report.wizard'

    first_month = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],'First Month')
    first_year= fields.Selection([(str(num), str(num)) for num in range(2017, (datetime.now().year)+1)], 'First Year')
    second_month = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],'Second Month')
    second_year = fields.Selection([(str(num), str(num)) for num in range(2017, (datetime.now().year)+1)], 'Second Year')

    def generate_report(self):
        view=self.env.ref('crm_lead_website_integration.crm_comparative_by_month_report_view_pivot')
        if not self.first_month:
            raise UserError(("Please specify the first month!"))
        if not self.first_year:
            raise UserError(("Please specify the first year!"))
        if not self.second_month:
            raise UserError(("Please specify the second month!"))
        if not self.second_year:
            raise UserError(("Please specify the second year!"))
        first_month=self.first_month+self.first_year
        second_month=self.second_month+self.second_year
        res={
            'type': 'ir.actions.act_window',
            'name': 'Pipeline Analysis By Program by day',
            'view_type': 'pivot',
            'view_mode': 'pivot',
            'res_model': 'crm.opportunity.custom.report',
            'views': [(view.id, 'pivot')],
            'view_id': view.id,
        }

        res['domain'] = ['|',('date_order_month', '=',first_month),('date_order_month', '=', second_month)]
        return res