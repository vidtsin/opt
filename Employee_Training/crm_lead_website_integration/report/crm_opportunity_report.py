# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools



class OpportunityCustomReport(models.Model):
    """ CRM Local Opportunity Analysis """

    _name = "crm.opportunity.custom.report"
    _auto=False
    _description = "CRM Opportunity Analysis 2"
    _rec_name = 'leads'


    create_date = fields.Datetime('Creation Date', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    team_id = fields.Many2one('crm.team', 'Sales Team', oldname='section_id', readonly=True)
    stage_id = fields.Many2one('crm.stage', string='Stage', readonly=True, domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]")
    # stage_name = fields.Char(string='Stage Name', readonly=True)
    type = fields.Selection([
        ('lead', 'Lead'),
        ('opportunity', 'Opportunity'),
    ], help="Type is used to separate Leads and Opportunities")
    date_conversion = fields.Datetime(string='Conversion Date', readonly=True)
    num_of_leads=fields.Integer(string='Number Of Leads',readonly=True)
    program=fields.Many2one('program.details',string='Program',readonly=True)
    city=fields.Char('City',readonly=True)
    country=fields.Many2one('res.country',string='Country',readonly=True)
    leads=fields.Many2one('crm.lead')
    date_order_month = fields.Char(string='Month Year')
    # date_order_year = fields.Char(string='Date Year')

    def init(self):
        print "test"
        tools.drop_view_if_exists(self._cr, 'crm_opportunity_custom_report')
        self._cr.execute("""
            CREATE Or Replace VIEW crm_opportunity_custom_report AS (
                SELECT
                    c.id,
                    c.user_id,
                    c.stage_id,
                    c.type,
                    c.team_id,
                    c.city as city,
                    c.country_id as country,
                    c.create_date as create_date,
                    (cast(date_part('month', c.create_date) as text) || cast(date_part('year', c.create_date) as text)) as date_order_month,
                    c.date_conversion as date_conversion,
                    c.program as program,
                    c.id as leads,
                    count(c.id) as num_of_leads
                FROM
                    "crm_lead" c
                GROUP BY c.id,c.user_id,c.stage_id,c.type,c.team_id,c.create_date,c.date_conversion,c.program,c.city,c.country_id
            )""")


