from odoo import models,fields,api,_
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError



class crmlead(models.Model):
    _inherit = 'crm.lead'




    name = fields.Char('Opportunity', required=False, invisible=1)





    @api.model
    def retrieve_sales_dashboard(self):
        """ Fetch data to setup Sales Dashboard """

        result = {
            'meeting': {
                'today': 0,
                'next_7_days': 0,
            },
            'activity': {
                'today': 0,
                'overdue': 0,
                'next_7_days': 0,
            },
            'closing': {
                'today': 0,
                'overdue': 0,
                'next_7_days': 0,
            },
            'done': {
                'this_month': 0,
                'last_month': 0,
            },
            'won': {
                'this_month': 0,
                'last_month': 0,
            },

            'new_leads':0 ,

            'lost_opportunity':0,

            'opportunity_total':0,

            'prospect_total':0,

            'admitted_total':0,

            'enrolled_total':0,

            'delayed_total': 0,

            'lead_con_ratio':0,

            'lead_to_opp_ratio':0,

            'opp_to_prospect_ratio':0,

            'no_follow':0,

            'enrolled_last_three_month':0,

            'rev_last_three_months': 0,

            'rate_last_three_months':0,

            'prospect_after_three_month':0,

            'rev_after_three_months':0,



        }
        current_date=datetime.now()
        lead_gen_date=current_date-relativedelta(days=1)
        new_lead_date=datetime.strftime(lead_gen_date,"%Y-%m-%d")
        one_month=current_date-relativedelta(months=1)
        bf_three_month=current_date-relativedelta(months=3)
        af_three_month=current_date+relativedelta(months=3)
        date1=datetime.strftime(one_month,"%Y-%m-%d")
        date2=datetime.strftime(bf_three_month,"%Y-%m-%d")
        date3=datetime.strftime(af_three_month,"%Y-%m-%d")


        #New leads generated records

        leads=self.search([
            ('new_lead','=',True)])
        if leads:
            result['new_leads']=len(leads)


        #Opportunities records

        opportunities=self.search([('stage_id.name','=','Opportunity'),('type','!=','lead')])
        if opportunities:
            result['opportunity_total']=len(opportunities)

        #Prospects records

        prospects=self.search([('stage_id.name','=','Prospect')])
        if prospects:
            result['prospect_total']=len(prospects)


        # Admitted  records

        admitted=self.search([('stage_id.name','=','Admitted')])
        if admitted:
            result['admitted_total']=len(admitted)


        # Enrolled records

        enrolled=self.search([('stage_id.name','=','Enrolled')])
        if enrolled:

            result['enrolled_total']=len(enrolled)


        # Delayed  records

        delayed=self.search([('stage_id.name','=','Delayed')])
        if delayed:
            result['delayed_total']=len(delayed)


        # Lost records

        lost = self.search([('stage_id.name','=','Lost')])
        if lost:
            result['lost_opportunity'] = len(lost)


        # Lead Opportunity Ratio

        leads=self.search([
            ('create_date','>=',date1),
            ('type','=','lead'),
        ])
        ld=len(leads)
        if leads:
            opportunity = self.search([
                ('type','!=','lead'),
                ('stage_id.name','=','Opportunity'),
            ])
            opp=len(opportunity)
            ratio=str((opp*100)/ld)
            opp_ratio=ratio +'%'
            result['lead_to_opp_ratio']=opp_ratio

        # Opportunity to Prospect Ratio

        opportunity = self.search([
            ('type','!=','lead'),
            ('stage_id.name','=','Opportunity'),
        ])
        opp=len(opportunity)
        if opportunity:
            prospects = self.search([('stage_id.name','=','Prospect')])
            pro=len(prospects)
            ratio=str((pro*100)/opp)
            pro_ratio=ratio +'%'
            result['opp_to_prospect_ratio']=pro_ratio

        # Leads Conversion Ratio

        leads=self.search([
            ('create_date','>=',date2),
            ('type','=','lead'),
        ])
        ld=str(len(leads))
        if leads:
            enrolled=self.search([('stage_id.name','=','Enrolled')])
            enrl=str(len(enrolled))
            ratio=ld+':'+enrl
            result['lead_con_ratio']=ratio

        #No follows More than 30days

        leads=self.search([
            ('create_date','>=',date1),
            ('type','=','lead'),
        ])
        if leads:
            result['no_follow']=len(leads)



        # Enrolled Last Three Months

        enrolled=self.search([
            ('stage_id.name','=','Enrolled'),
            ('create_date','>=',date2),])
        if enrolled:
            result['enrolled_last_three_month']=len(enrolled)


        # Revenue Quarter Last Three Months

        enrolled = self.search([
            ('stage_id.name','=','Enrolled'),
            ('create_date','>=',date2), ])
        total2=0
        for record in enrolled:
            total1=record.program.total
            total2+=int(total1)
            result['rev_last_three_months']=total2


        # Prospects After Three Months

        prospects=self.search([
            ('stage_id.name','=','Prospect'),
            ('create_date','<=',date3), ])
        if prospects:
            result['prospect_after_three_month']=len(prospects)

        # Revenue Quarter After Three Months

        prospects=self.search([
            ('stage_id.name','=','Prospect'),
            ('create_date','<=',date3), ])
        total4=0
        for record in prospects:
            total3=record.program.total
            total4+=int(total3)
            result['rev_after_three_months']=total4


        #Rate of Revenue Last Three Months

        # rate=(total2*100)/total4
        # rate_percentage=str(rate)+'%'
        # result['rate_last_three_months']=rate_percentage


        return result





    @api.model
    def retrieve_diploma_data(self):
        retrieve_dip_data=""" select p.internal_ref,count(c.id) from crm_lead c join program_details p on c.program = p.id where p.lead_by_diploma = True group by p.internal_ref ORDER BY count desc limit 5 ;"""
        self.env.cr.execute(retrieve_dip_data)
        lead_by_diploma=self.env.cr.dictfetchall()
        if len(lead_by_diploma)== 0:
            return 'None'
        else:
            return lead_by_diploma





    @api.model
    def retrieve_certification_data(self):
        retrieve_cert_data="""select p.internal_ref,count(c.id) from crm_lead c join program_details p on c.program = p.id where p.lead_by_certification = True group by p.internal_ref ORDER BY count desc limit 5 ; """
        self.env.cr.execute(retrieve_cert_data)
        lead_by_certification=self.env.cr.dictfetchall()
        if len(lead_by_certification)== 0:
            return 'None'
        else:
            return lead_by_certification





    @api.model
    def retrieve_month_data(self):
        retrieve_data_query="""select to_char(create_date,'Mon-YYYY') create_date, count(id) from crm_lead GROUP BY to_char(create_date,'Mon-YYYY') ORDER BY create_date limit 5;"""
        self.env.cr.execute(retrieve_data_query)
        leads_count=self.env.cr.dictfetchall()
        if len(leads_count) == 0:
            return 'None'
        else:
            return leads_count





    @api.model
    def retrieve_source_data(self):
        retrieve_source_data="""select source_url,count(*) from crm_lead group by source_url ORDER BY count desc limit 5 ;"""
        self.env.cr.execute(retrieve_source_data)
        lead_by_source=self._cr.dictfetchall()
        if len(lead_by_source) == 0:
            return 'None'
        else:
            return lead_by_source


