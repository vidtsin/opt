from odoo import fields, models, tools, api
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO




class ProgramReport(models.TransientModel):
    _name = "crm.program.report"

    from_date= fields.Datetime("From")
    to_date = fields.Datetime("To")
    period_from = fields.Selection([('day', 'day'),
                                    ('week', 'Week'),
                                    ('month', 'Month'),],
                                   string="Period")
    number_of_period = fields.Integer("")
    filter_team_id = fields.Many2one('crm.team', 'Sales team')
    filter_program_id = fields.Many2one('program.details', 'Program')





    @api.multi
    def view_program(self):
        currentdate = datetime.now()
        if self.period_from == 'day':
            record = currentdate - relativedelta(days=self.number_of_period)
            date = str(record)
            if not self.filter_team_id:
                if not self.filter_program_id:
                    view = self.env.ref(
                        'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_report_view_pivot')
                    return {
                        'type': 'ir.actions.act_window',
                        'name': ' Program by day',
                        'view_type': 'pivot',
                        'view_mode': 'pivot',
                        'res_model': 'crm.opportunity.custom.report',
                        'views': [(view.id, 'pivot')],
                        'view_id': view.id,
                        'domain': [('create_date', '>=', date),
                                   ],
                    }
                else:
                    view = self.env.ref(
                        'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_report_view_pivot')
                    return {
                        'type': 'ir.actions.act_window',
                        'name': 'Program by day',
                        'view_type': 'pivot',
                        'view_mode': 'pivot',
                        'res_model': 'crm.opportunity.custom.report',
                        'views': [(view.id, 'pivot')],
                        'view_id': view.id,
                        'domain': [('create_date', '>=', date),

                                   ('program', '=',self.filter_program_id.id),

                                   ],
                    }
            else:
                if not self.filter_program_id:
                    view = self.env.ref(
                        'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_report_view_pivot')
                    return {
                        'type': 'ir.actions.act_window',
                        'name': ' Program by day',
                        'view_type': 'pivot',
                        'view_mode': 'pivot',
                        'res_model': 'crm.opportunity.custom.report',
                        'views': [(view.id, 'pivot')],
                        'view_id': view.id,
                        'domain': [('create_date', '>=', date),
                                   ('team_id', '=', self.filter_team_id.id),
                                   ],
                    }
                else:
                    view = self.env.ref(
                        'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_report_view_pivot')
                    return {
                        'type': 'ir.actions.act_window',
                        'name': 'Program by day',
                        'view_type': 'pivot',
                        'view_mode': 'pivot',
                        'res_model': 'crm.opportunity.custom.report',
                        'views': [(view.id, 'pivot')],
                        'view_id': view.id,
                        'domain': [('create_date', '>=', date),
                                   ('team_id', '=', self.filter_team_id.id),
                                   ('program', '=', self.filter_program_id.id),

                                   ],
                    }
        if self.period_from == 'week':
                record = currentdate - relativedelta(weeks=self.number_of_period)
                date = str(record)
                if not self.filter_team_id:
                    if not self.filter_program_id:
                        view = self.env.ref(
                            'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_by_week_report_view_pivot')
                        return {
                            'type': 'ir.actions.act_window',
                            'name': ' Program by day',
                            'view_type': 'pivot',
                            'view_mode': 'pivot',
                            'res_model': 'crm.opportunity.custom.report',
                            'views': [(view.id, 'pivot')],
                            'view_id': view.id,
                            'domain': [('create_date', '>=', date),
                                       ],
                        }
                    else:
                        view = self.env.ref(
                            'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_by_week_report_view_pivot')
                        return {
                            'type': 'ir.actions.act_window',
                            'name': 'Program by day',
                            'view_type': 'pivot',
                            'view_mode': 'pivot',
                            'res_model': 'crm.opportunity.custom.report',
                            'views': [(view.id, 'pivot')],
                            'view_id': view.id,
                            'domain': [('create_date', '>=', date),

                                       ('program', '=', self.filter_program_id.id),

                                       ],
                        }
                else:
                    if not self.filter_program_id:
                        view = self.env.ref(
                            'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_by_week_report_view_pivot')
                        return {
                            'type': 'ir.actions.act_window',
                            'name': ' Program by day',
                            'view_type': 'pivot',
                            'view_mode': 'pivot',
                            'res_model': 'crm.opportunity.custom.report',
                            'views': [(view.id, 'pivot')],
                            'view_id': view.id,
                            'domain': [('create_date', '>=', date),
                                       ('team_id', '=', self.filter_team_id.id),
                                       ],
                        }
                    else:
                        view = self.env.ref(
                            'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_by_week_report_view_pivot')
                        return {
                            'type': 'ir.actions.act_window',
                            'name': 'Program by day',
                            'view_type': 'pivot',
                            'view_mode': 'pivot',
                            'res_model': 'crm.opportunity.custom.report',
                            'views': [(view.id, 'pivot')],
                            'view_id': view.id,
                            'domain': [('create_date', '>=', date),
                                       ('team_id', '=', self.filter_team_id.id),
                                       ('program', '=', self.filter_program_id.id),

                                       ],
                        }
        if self.period_from == 'month':
                record = currentdate - relativedelta(months=self.number_of_period)
                date = str(record)
                if not self.filter_team_id:
                    if not self.filter_program_id:
                        view = self.env.ref(
                            'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_by_month_report_view_pivot')
                        return {
                            'type': 'ir.actions.act_window',
                            'name': ' Program by day',
                            'view_type': 'pivot',
                            'view_mode': 'pivot',
                            'res_model': 'crm.opportunity.custom.report',
                            'views': [(view.id, 'pivot')],
                            'view_id': view.id,
                            'domain': [('create_date', '>=', date),
                                       ],
                        }
                    else:
                        view = self.env.ref(
                            'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_by_month_report_view_pivot')
                        return {
                            'type': 'ir.actions.act_window',
                            'name': 'Program by day',
                            'view_type': 'pivot',
                            'view_mode': 'pivot',
                            'res_model': 'crm.opportunity.custom.report',
                            'views': [(view.id, 'pivot')],
                            'view_id': view.id,
                            'domain': [('create_date', '>=', date),

                                       ('program', '=', self.filter_program_id.id),

                                       ],
                        }
                else:
                    if not self.filter_program_id:
                        view = self.env.ref(
                            'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_by_month_report_view_pivot')
                        return {
                            'type': 'ir.actions.act_window',
                            'name': ' Program by day',
                            'view_type': 'pivot',
                            'view_mode': 'pivot',
                            'res_model': 'crm.opportunity.custom.report',
                            'views': [(view.id, 'pivot')],
                            'view_id': view.id,
                            'domain': [('create_date', '>=', date),
                                       ('team_id', '=', self.filter_team_id.id),
                                       ],
                        }
                    else:
                        view = self.env.ref(
                            'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_by_month_report_view_pivot')
                        return {
                            'type': 'ir.actions.act_window',
                            'name': 'Program by day',
                            'view_type': 'pivot',
                            'view_mode': 'pivot',
                            'res_model': 'crm.opportunity.custom.report',
                            'views': [(view.id, 'pivot')],
                            'view_id': view.id,
                            'domain': [('create_date', '>=', date),
                                       ('team_id', '=', self.filter_team_id.id),
                                       ('program', '=', self.filter_program_id.id),

                                       ],
                        }
        if self.from_date != False:
            if not self.filter_team_id:
                if not self.filter_program_id:
                    view = self.env.ref(
                        'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_report_view_pivot')
                    return {
                        'type': 'ir.actions.act_window',
                        'name': ' Program by day',
                        'view_type': 'pivot',
                        'view_mode': 'pivot',
                        'res_model': 'crm.opportunity.custom.report',
                        'views': [(view.id, 'pivot')],
                        'view_id': view.id,
                        'domain': [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date),
                                   ],
                    }
                else:
                    view = self.env.ref(
                        'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_report_view_pivot')
                    return {
                        'type': 'ir.actions.act_window',
                        'name': 'Program by day',
                        'view_type': 'pivot',
                        'view_mode': 'pivot',
                        'res_model': 'crm.opportunity.custom.report',
                        'views': [(view.id, 'pivot')],
                        'view_id': view.id,
                        'domain': [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date),

                                   ('program', '=',self.filter_program_id.id),

                                   ],
                    }
            else:
                if not self.filter_program_id:
                    view = self.env.ref(
                        'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_report_view_pivot')
                    return {
                        'type': 'ir.actions.act_window',
                        'name': ' Program by day',
                        'view_type': 'pivot',
                        'view_mode': 'pivot',
                        'res_model': 'crm.opportunity.custom.report',
                        'views': [(view.id, 'pivot')],
                        'view_id': view.id,
                        'domain': [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date),
                                   ('team_id', '=', self.filter_team_id.id),
                                   ],
                    }
                else:
                    view = self.env.ref(
                        'crm_lead_website_integration.crm_local_opportunity_pipeline_analysis_report_view_pivot')
                    return {
                        'type': 'ir.actions.act_window',
                        'name': 'Program by day',
                        'view_type': 'pivot',
                        'view_mode': 'pivot',
                        'res_model': 'crm.opportunity.custom.report',
                        'views': [(view.id, 'pivot')],
                        'view_id': view.id,
                        'domain': [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date),
                                   ('team_id', '=', self.filter_team_id.id),
                                   ('program', '=', self.filter_program_id.id),

                                   ],
                    }
