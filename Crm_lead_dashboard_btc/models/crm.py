from odoo import models,fields,api,_
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from calendar import Calendar


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

            'new_opportunity':0 ,

            'lost_opportunity':0,

            'opportunity_total':0,

            'prospect_total':0,

            'admitted_total':0,

            'enrolled_total':0,

            'delayed_total': 0,

            'lead_con_ratio':0,

            'lead_to_opp_ratio':0,

            'lead_to_sale_ratio': 0,

            'opp_to_prospect_ratio':0,

            'no_follow':0,

            'enrolled_last_three_month':0,

            'rev_last_three_months': 0,

            'rate_last_three_months':0,

            'prospect_after_three_month':0,

            'rev_after_three_months':0,

            'lead_diploma_local_per_weeks':0,

            'lead_diploma_inter_per_weeks':0,

            'lead_certificate_local_per_weeks':0,

            'lead_certificate_inter_per_weeks':0,

            'lead_diploma_total_per_weeks':0,

            'lead_certification_total_per_weeks':0,

            'lead_local_total_per_weeks':0,

            'lead_international_total_per_weeks':0,

            'lead_grand_total_per_weeks':0,

            'oppo_diploma_local_per_weeks':0,

            'oppo_diploma_inter_per_weeks': 0,

            'oppo_diploma_total_per_weeks': 0,

            'oppo_certificate_local_per_weeks': 0,

            'oppo_certificate_inter_per_weeks': 0,

            'oppo_certification_total_per_weeks': 0,

            'oppo_local_total_per_weeks': 0,

            'oppo_international_total_per_weeks': 0,

            'oppo_grand_total_per_weeks': 0,

            'lead_diploma_local_per_months':0,

            'lead_diploma_inter_per_months':0,

            'lead_certificate_local_per_months':0,

            'lead_certificate_inter_per_months':0,

            'lead_diploma_total_per_months':0,

            'lead_certification_total_per_months':0,

            'lead_local_total_per_months':0,

            'lead_international_total_per_months':0,

            'lead_grand_total_per_months':0,

            'oppo_diploma_local_per_months':0,

            'oppo_diploma_inter_per_months': 0,

            'oppo_diploma_total_per_months': 0,

            'oppo_certificate_local_per_months': 0,

            'oppo_certificate_inter_per_months': 0,

            'oppo_certification_total_per_months': 0,

            'oppo_local_total_per_months': 0,

            'oppo_international_total_per_months': 0,

            'oppo_grand_total_per_months': 0,





            'lead_diploma_local_per_year': 0,

            'lead_diploma_inter_per_year': 0,

            'lead_certificate_local_per_year': 0,

            'lead_certificate_inter_per_year': 0,

            'lead_diploma_total_per_year': 0,

            'lead_certification_total_per_year': 0,

            'lead_local_total_per_year': 0,

            'lead_international_total_per_year': 0,

            'lead_grand_total_per_year': 0,

            'oppo_diploma_local_per_year': 0,

            'oppo_diploma_inter_per_year': 0,

            'oppo_diploma_total_per_year': 0,

            'oppo_certificate_local_per_year': 0,

            'oppo_certificate_inter_per_year': 0,

            'oppo_certification_total_per_year': 0,

            'oppo_local_total_per_year': 0,

            'oppo_international_total_per_year': 0,

            'oppo_grand_total_per_year': 0,




















        }
        current_date=datetime.now()
        lead_gen_date=current_date-relativedelta(days=1)
        opp_gen_date=current_date-relativedelta(days=1)
        new_lead_date=datetime.strftime(lead_gen_date,"%Y-%m-%d")
        new_oppo_date=datetime.strftime(opp_gen_date,"%Y-%m-%d")
        one_year=current_date-relativedelta(years=1)
        one_month=current_date-relativedelta(months=1)
        one_week=current_date-relativedelta(weeks=1)
        bf_three_month=current_date-relativedelta(months=3)
        af_three_month=current_date+relativedelta(months=3)
        af_three_month=current_date+relativedelta(months=3)
        date1=datetime.strftime(one_month,"%Y-%m-%d")
        date2=datetime.strftime(bf_three_month,"%Y-%m-%d")
        date3=datetime.strftime(af_three_month,"%Y-%m-%d")
        date4=datetime.strftime(one_week,"%Y-%m-%d")
        date5=datetime.strftime(one_year,"%Y-%m-%d")


        #New leads generated records

        leads=self.search([
            ('create_date', '>=', date1),
            ('type', '=','lead')
        ])
        if leads:
            result['new_leads']=len(leads)


        # New opportunity generated record

        opportunitys = self.search([
            ('date_conversion', '>=', date1),
            ('type', '=', 'opportunity'),])
        if opportunitys:

            result['new_opportunity'] = len(opportunitys)


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
                ('date_conversion', '>=', date1),
            ])
            opp=len(opportunity)
            ratio=str((opp*100)/ld)
            opp_ratio=ratio +'%'
            result['lead_to_opp_ratio']=opp_ratio


        # Lead to sales Ratio

        leads = self.search([
            ('create_date', '>=', date1),
            ('type', '=', 'lead'),
        ])
        ld = len(leads)
        if leads:
            opportunity_admitted = self.search([
                ('type', '!=', 'lead'),
                ('stage_id.name', '=', 'Admitted'),
                ('date_conversion', '>=', date1),
            ])
            opportunity_enrolled = self.search([
                ('type', '!=', 'lead'),
                ('stage_id.name', '=', 'Enrolled'),
                ('date_conversion', '>=', date1),
            ])
            adm=opportunity_admitted
            enr=opportunity_enrolled
            opportunity=len(adm + enr)
            opp = opportunity
            ratio = str((opp * 100) / ld)
            opp_ratio = ratio + '%'
            result['lead_to_sale_ratio'] = opp_ratio

        # Opportunity to Prospect Ratio

        opportunity = self.search([
            ('type','!=','lead'),
            ('stage_id.name','=','Opportunity'),
            ('date_conversion', '>=', date1),
        ])
        opp=len(opportunity)
        if opportunity:
            prospects = self.search([
             ('type', '!=', 'lead'),
             ('stage_id.name', '=', 'Prospect'),
             ('date_conversion', '>=', date1),
             ])
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
            enrolled=self.search([('stage_id.name','=','Enrolled'),
                                  ('date_conversion', '>=', date2),
                                  ('type', '=', 'opportunity'),
                                  ])
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
            ('type', '=', 'opportunity'),
            ('stage_id.name','=','Enrolled'),
            ('date_conversion','>=',date2),])
        if enrolled:
            result['enrolled_last_three_month']=len(enrolled)


        # Revenue Quarter Last Three Months

        enrolled = self.search([
            ('type', '=', 'opportunity'),
            ('stage_id.name','=','Enrolled'),
            ('date_conversion','>=',date2), ])
        total2=0
        for record in enrolled:
            total1=record.program.total
            total2+=int(total1)
            result['rev_last_three_months']=total2


        # Prospects After Three Months

        prospects=self.search([
            ('type', '=', 'opportunity'),
            ('stage_id.name','=','Prospect'),
            ('date_conversion','<=',date3), ])
        if prospects:
            result['prospect_after_three_month']=len(prospects)

        # Revenue Quarter After Three Months

        prospects=self.search([
            ('type', '=', 'opportunity'),
            ('stage_id.name','=','Prospect'),
            ('date_conversion','<=',date3), ])
        total4=0
        for record in prospects:
            total3=record.program.total
            total4+=int(total3)
            result['rev_after_three_months']=total4

        # lead diploma local per weeks

        leads_dip_local = self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_diploma', '=',True),
            ('team_id', '=','local'),
            ('create_date', '>=', date4), ])
        print"leadssslocal",leads_dip_local
        total_dip_local = len(leads_dip_local)
        result['lead_diploma_local_per_weeks'] = total_dip_local

        # lead diploma international per weeks

        leads_dip_inter = self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_diploma', '=', True),
            ('team_id', '=', 'International'),
            ('create_date', '>=', date4), ])
        print"leadssslocal", leads_dip_inter
        total_dip_inter = len(leads_dip_inter)
        result['lead_diploma_inter_per_weeks'] = total_dip_inter

        # lead diploma total local + international

        lead_diploma_total= total_dip_local+total_dip_inter
        result['lead_diploma_total_per_weeks'] = lead_diploma_total


        # lead certification_local_per_weeks

        leads_cert_local = self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'local'),
            ('create_date', '>=', date4), ])
        print"leadssslocal", leads_cert_local
        total_cert_local = len(leads_cert_local)
        result['lead_certificate_local_per_weeks'] = total_cert_local

        # lead certification_international_per_weeks

        leads_cert_inter = self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'International'),
            ('create_date', '>=', date4), ])
        print"leadssslocal", leads_cert_inter
        total_cert_inter = len(leads_cert_inter)
        result['lead_certificate_inter_per_weeks'] = total_cert_inter

        # lead certification total local + international

        lead_certification_total = total_cert_local + total_cert_inter
        result['lead_certification_total_per_weeks'] = lead_certification_total

        # lead local total

        lead_local_total = total_dip_local + total_cert_local
        result['lead_local_total_per_weeks'] = lead_local_total

        # lead international total

        lead_international_total = total_dip_inter + total_cert_inter
        result['lead_international_total_per_weeks'] = lead_international_total

        # lead grand total

        lead_grand_total = lead_diploma_total + lead_certification_total
        result['lead_grand_total_per_weeks'] = lead_grand_total

        # opportunity diploma local per weeks

        oppo_dip_local = self.search([
            ('type', '=', 'opportunity'),'|',
            ('stage_id.name','=','Opportunity'),
            ('stage_id.name','=','Prospect'),
            ('program.lead_by_diploma', '=', True),
            ('team_id', '=', 'local'),
            ('date_conversion', '>=', date4), ])
        print"leadssslocal", oppo_dip_local
        total_oppo_dip_local = len(oppo_dip_local)
        result['oppo_diploma_local_per_weeks'] = total_oppo_dip_local

        # opportunity diploma international per weeks

        oppo_dip_inter = self.search([
            ('type', '=', 'opportunity'), '|',
            ('stage_id.name', '=', 'Opportunity'),
            ('stage_id.name', '=', 'Prospect'),
            ('program.lead_by_diploma', '=', True),
            ('team_id', '=', 'International'),
            ('date_conversion', '>=', date4), ])
        print"leadssslocal", oppo_dip_inter
        total_oppo_dip_inter = len(oppo_dip_inter)
        result['oppo_diploma_inter_per_weeks'] = total_oppo_dip_inter

        # opportunity diploma total local + international

        oppo_diploma_total = total_oppo_dip_local + total_oppo_dip_inter
        result['oppo_diploma_total_per_weeks'] = oppo_diploma_total

        # opportunity certification local per weeks

        oppo_cert_local = self.search([
            ('type', '=', 'opportunity'), '|',
            ('stage_id.name', '=', 'Opportunity'),
            ('stage_id.name', '=', 'Prospect'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'local'),
            ('date_conversion', '>=', date4), ])
        print"leadssslocal", oppo_cert_local
        total_oppo_cert_local = len(oppo_cert_local)
        result['oppo_certificate_local_per_weeks'] = total_oppo_cert_local

        # opportunity certification International per weeks

        oppo_cert_inter = self.search([
            ('type', '=', 'opportunity'), '|',
            ('stage_id.name', '=', 'Opportunity'),
            ('stage_id.name', '=', 'Prospect'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'International'),
            ('date_conversion', '>=', date4), ])
        print"leadssslocal", oppo_cert_inter
        total_oppo_cert_inter = len(oppo_cert_inter)
        result['oppo_certificate_inter_per_weeks'] = total_oppo_cert_inter

        # opportunity CERTIFICATION total local + international

        oppo_certification_total = total_oppo_cert_local + total_oppo_cert_inter
        result['oppo_certification_total_per_weeks'] = oppo_certification_total

        # opportunity  total local

        oppo_local_total = total_oppo_dip_local + total_oppo_cert_local
        result['oppo_local_total_per_weeks'] = oppo_local_total

        # opportunity  total international

        oppo_inter_total = total_oppo_dip_inter + total_oppo_cert_inter
        result['oppo_international_total_per_weeks'] = oppo_inter_total

        # opportunity  grand total

        oppo_grand_total = oppo_diploma_total + oppo_certification_total
        result['oppo_grand_total_per_weeks'] = oppo_grand_total



        #Rate of Revenue Last Three Months

        # rate=(total2*100)/total4
        # rate_percentage=str(rate)+'%'
        # result['rate_last_three_months']=rate_percentage


        leads_dip_local_months = self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_diploma', '=', True),
            ('team_id', '=', 'local'),
            ('create_date', '>=', date1), ])
        print"leadssslocal", leads_dip_local_months
        total_dip_local_months = len(leads_dip_local_months)
        result['lead_diploma_local_per_months'] = total_dip_local_months

        # lead diploma international per months

        leads_dip_inter_months = self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_diploma', '=', True),
            ('team_id', '=', 'International'),
            ('create_date', '>=', date1), ])
        print"leadssslocal", leads_dip_inter_months
        total_dip_inter_months = len(leads_dip_inter_months)
        result['lead_diploma_inter_per_months'] = total_dip_inter_months

        # lead diploma total local + international months

        lead_diploma_total_months = total_dip_local_months + total_dip_inter_months
        result['lead_diploma_total_per_months'] = lead_diploma_total_months

        # lead certification_local_per_ months

        leads_cert_local_months = self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'local'),
            ('create_date', '>=', date1), ])
        print"leadssslocal", leads_cert_local_months
        total_cert_local_months = len(leads_cert_local_months)
        result['lead_certificate_local_per_months'] = total_cert_local_months

        # lead certification_international_per_months

        leads_cert_inter_months = self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'International'),
            ('create_date', '>=', date1), ])
        print"leadssslocal", leads_cert_inter_months
        total_cert_inter_months = len(leads_cert_inter_months)
        result['lead_certificate_inter_per_months'] = total_cert_inter_months

        # lead certification total local + international months

        lead_certification_total_months = total_cert_local_months + total_cert_inter_months
        result['lead_certification_total_per_months'] = lead_certification_total_months

        # lead local total months

        lead_local_total_months = total_dip_local_months + total_cert_local_months
        result['lead_local_total_per_months'] = lead_local_total_months

        # lead international total months

        lead_international_total_months = total_dip_inter_months + total_cert_inter_months
        result['lead_international_total_per_months'] = lead_international_total_months

        # lead grand total months

        lead_grand_total_months = lead_diploma_total_months + lead_certification_total_months
        result['lead_grand_total_per_months'] = lead_grand_total_months

        # opportunity diploma international per months

        oppo_dip_local_months = self.search([
            ('type', '=', 'opportunity'), '|',
            ('stage_id.name', '=', 'Opportunity'),
            ('stage_id.name', '=', 'Prospect'),
            ('program.lead_by_diploma', '=', True),
            ('team_id', '=', 'local'),
            ('date_conversion', '>=', date1), ])
        print"leadssslocal", oppo_dip_local_months
        total_oppo_dip_local_months = len(oppo_dip_local_months)
        result['oppo_diploma_local_per_months'] = total_oppo_dip_local_months



        oppo_dip_inter_months = self.search([
            ('type', '=', 'opportunity'), '|',
            ('stage_id.name', '=', 'Opportunity'),
            ('stage_id.name', '=', 'Prospect'),
            ('program.lead_by_diploma', '=', True),
            ('team_id', '=', 'International'),
            ('date_conversion', '>=', date1), ])
        print"leadssslocal", oppo_dip_inter_months
        total_oppo_dip_inter_months = len(oppo_dip_inter_months)
        result['oppo_diploma_inter_per_months'] = total_oppo_dip_inter_months

        # opportunity diploma total local + international months

        oppo_diploma_total_months = total_oppo_dip_local_months + total_oppo_dip_inter_months
        result['oppo_diploma_total_per_months'] = oppo_diploma_total_months

        # opportunity certification local per months

        oppo_cert_local_months = self.search([
            ('type', '=', 'opportunity'), '|',
            ('stage_id.name', '=', 'Opportunity'),
            ('stage_id.name', '=', 'Prospect'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'local'),
            ('date_conversion', '>=', date1), ])
        print"leadssslocal", oppo_cert_local_months
        total_oppo_cert_local_months = len(oppo_cert_local_months)
        result['oppo_certificate_local_per_months'] = total_oppo_cert_local_months

        # opportunity certification International per months

        oppo_cert_inter_months = self.search([
            ('type', '=', 'opportunity'), '|',
            ('stage_id.name', '=', 'Opportunity'),
            ('stage_id.name', '=', 'Prospect'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'International'),
            ('date_conversion', '>=', date1), ])
        print"leadssslocal", oppo_cert_inter_months
        total_oppo_cert_inter_months = len(oppo_cert_inter_months)
        result['oppo_certificate_inter_per_months'] = total_oppo_cert_inter_months

        # opportunity CERTIFICATION total local + international months

        oppo_certification_total_months = total_oppo_cert_local_months + total_oppo_cert_inter_months
        result['oppo_certification_total_per_months'] = oppo_certification_total_months

        # opportunity  total local months

        oppo_local_total_months = total_oppo_dip_local_months + total_oppo_cert_local_months
        result['oppo_local_total_per_months'] = oppo_local_total_months

        # opportunity  total international months

        oppo_inter_total_months = total_oppo_dip_inter_months + total_oppo_cert_inter_months
        result['oppo_international_total_per_months'] = oppo_inter_total_months

        # opportunity  grand total months

        oppo_grand_total_months = oppo_diploma_total_months + oppo_certification_total_months
        result['oppo_grand_total_per_months'] = oppo_grand_total_months











        # lead diploma local per year

        leads_dip_local_year = self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_diploma', '=', True),
            ('team_id', '=', 'local'),
            ('create_date', '>=', date5), ])
        print"leadssslocal", leads_dip_local_year
        total_dip_local_year = len(leads_dip_local_year)
        result['lead_diploma_local_per_year'] = total_dip_local_year

        # lead diploma international per year

        leads_dip_inter_year = self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_diploma', '=', True),
            ('team_id', '=', 'International'),
            ('create_date', '>=', date5), ])
        print"leadssslocal", leads_dip_inter_year
        total_dip_inter_year = len(leads_dip_inter_year)
        result['lead_diploma_inter_per_year'] = total_dip_inter_year

        # lead diploma total local + international year

        lead_diploma_total_year = total_dip_local_year + total_dip_inter_year
        result['lead_diploma_total_per_year'] = lead_diploma_total_year

        # lead certification_local_per_year

        leads_cert_local_year = self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'local'),
            ('create_date', '>=', date5), ])
        print"leadssslocal", leads_cert_local_year
        total_cert_local_year = len(leads_cert_local_year)
        result['lead_certificate_local_per_year'] = total_cert_local_year

        # lead certification_international_per_year

        leads_cert_inter_year= self.search([
            ('type', '=', 'lead'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'International'),
            ('create_date', '>=', date5), ])
        print"leadssslocal", leads_cert_inter_year
        total_cert_inter_year = len(leads_cert_inter_year)
        result['lead_certificate_inter_per_year'] = total_cert_inter_year

        # lead certification total local + international year

        lead_certification_total_year = total_cert_local_year + total_cert_inter_year
        result['lead_certification_total_per_year'] = lead_certification_total_year

        # lead local total year

        lead_local_total_year = total_dip_local_year + total_cert_local_year
        result['lead_local_total_per_year'] = lead_local_total_year

        # lead international total year

        lead_international_total_year = total_dip_inter_year + total_cert_inter_year
        result['lead_international_total_per_year'] = lead_international_total_year

        # lead grand total year

        lead_grand_total_year = lead_diploma_total_year + lead_certification_total_year
        result['lead_grand_total_per_year'] = lead_grand_total_year

        # opportunity diploma local per year

        oppo_dip_local_year = self.search([
            ('type', '=', 'opportunity'), '|',
            ('stage_id.name', '=', 'Opportunity'),
            ('stage_id.name', '=', 'Prospect'),
            ('program.lead_by_diploma', '=', True),
            ('team_id', '=', 'local'),
            ('date_conversion', '>=', date5), ])
        print"leadssslocal", oppo_dip_local_year
        total_oppo_dip_local_year = len(oppo_dip_local_year)
        result['oppo_diploma_local_per_year'] = total_oppo_dip_local_year

        # opportunity diploma international per year

        oppo_dip_inter_year = self.search([
            ('type', '=', 'opportunity'), '|',
            ('stage_id.name', '=', 'Opportunity'),
            ('stage_id.name', '=', 'Prospect'),
            ('program.lead_by_diploma', '=', True),
            ('team_id', '=', 'International'),
            ('date_conversion', '>=', date5), ])
        print"leadssslocal", oppo_dip_inter_year
        total_oppo_dip_inter_year = len(oppo_dip_inter_year)
        result['oppo_diploma_inter_per_year'] = total_oppo_dip_inter_year

        # opportunity diploma total local + international year

        oppo_diploma_total_year = total_oppo_dip_local_year + total_oppo_dip_inter_year
        result['oppo_diploma_total_per_year'] = oppo_diploma_total_year

        # opportunity certification local per year

        oppo_cert_local_year = self.search([
            ('type', '=', 'opportunity'), '|',
            ('stage_id.name', '=', 'Opportunity'),
            ('stage_id.name', '=', 'Prospect'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'local'),
            ('date_conversion', '>=', date5), ])
        print"leadssslocal", oppo_cert_local_year
        total_oppo_cert_local_year = len(oppo_cert_local_year)
        result['oppo_certificate_local_per_year'] = total_oppo_cert_local_year

        # opportunity certification International per year

        oppo_cert_inter_year = self.search([
            ('type', '=', 'opportunity'), '|',
            ('stage_id.name', '=', 'Opportunity'),
            ('stage_id.name', '=', 'Prospect'),
            ('program.lead_by_certification', '=', True),
            ('team_id', '=', 'International'),
            ('date_conversion', '>=', date5), ])
        print"leadssslocal", oppo_cert_inter_year
        total_oppo_cert_inter_year = len(oppo_cert_inter_year)
        result['oppo_certificate_inter_per_year'] = total_oppo_cert_inter_year

        # opportunity CERTIFICATION total local + international year

        oppo_certification_total_year = total_oppo_cert_local_year + total_oppo_cert_inter_year
        result['oppo_certification_total_per_year'] = oppo_certification_total_year

        # opportunity  total local year

        oppo_local_total_year = total_oppo_dip_local_year + total_oppo_cert_local_year
        result['oppo_local_total_per_year'] = oppo_local_total_year

        # opportunity  total international year

        oppo_inter_total_year = total_oppo_dip_inter_year + total_oppo_cert_inter_year
        result['oppo_international_total_per_year'] = oppo_inter_total_year

        # opportunity  grand total year

        oppo_grand_total_year = oppo_diploma_total_year + oppo_certification_total_year
        result['oppo_grand_total_per_year'] = oppo_grand_total_year










        return result





    @api.model
    def retrieve_diploma_data(self):
        retrieve_dip_data=""" select p.name,p.internal_ref,count(c.id) from crm_lead c join program_details p on c.program = p.id where p.lead_by_diploma = True group by  p.name,p.internal_ref ORDER BY count desc limit 5 ;"""
        self.env.cr.execute(retrieve_dip_data)
        lead_by_diploma=self.env.cr.dictfetchall()
        if len(lead_by_diploma)== 0:
            return 'None'
        else:
            return lead_by_diploma





    @api.model
    def retrieve_certification_data(self):
        retrieve_cert_data="""select p.name,p.internal_ref,count(c.id) from crm_lead c join program_details p on c.program = p.id where p.lead_by_certification = True group by p.name,p.internal_ref ORDER BY count desc limit 5 ; """
        self.env.cr.execute(retrieve_cert_data)
        lead_by_certification=self.env.cr.dictfetchall()
        if len(lead_by_certification)== 0:
            return 'None'
        else:
            return lead_by_certification





    @api.model
    def retrieve_lead_by_diploma_month_data(self):
        retrieve_lead_by_diploma_month_data="""select to_char(c.create_date,'Mon-YYYY') create_date, count(c.id) from crm_lead c join program_details p on c.program = p.id where p.lead_by_diploma=True group by to_char(c.create_date,'Mon-YYYY') ORDER BY create_date limit 5;"""
        self.env.cr.execute(retrieve_lead_by_diploma_month_data)
        lead_by_diploma_month=self.env.cr.dictfetchall()
        # list=sorted(lead_by_diploma_month)
        # list=sorted(lead_by_diploma_month, key=lambda x: datetime.datetime.strptime(''.join(x), '%Y%m'))
        # print"dsdsadasdasd",list
        if len(lead_by_diploma_month) == 0:
            return 'None'
        else:
            print"month dattattttaaa",lead_by_diploma_month
            return lead_by_diploma_month

    @api.model
    def retrieve_lead_by_certification_month_data(self):
        retrieve_lead_by_certification_month_data = """select to_char(c.create_date,'Mon-YYYY') create_date, count(c.id) from crm_lead c join program_details p on c.program = p.id where p.lead_by_certification=True group by to_char(c.create_date,'Mon-YYYY') ORDER BY create_date limit 5;"""
        self.env.cr.execute(retrieve_lead_by_certification_month_data)
        lead_by_certification_month = self.env.cr.dictfetchall()
        if len(lead_by_certification_month) == 0:
            return 'None'
        else:
            print"month dattattttaaa", lead_by_certification_month
            return lead_by_certification_month




    @api.model
    def retrieve_source_by_diploma_data(self):
        retrieve_source_by_diploma_data="""select c.source_url,count(c.id) from crm_lead c join program_details p on c.program =p .id where p.lead_by_diploma=True group by c.source_url ORDER BY count limit 5;"""
        self.env.cr.execute(retrieve_source_by_diploma_data)
        lead_source_by_diploma=self._cr.dictfetchall()
        if len(lead_source_by_diploma) == 0:
            return 'None'
        else:
            print'source diplomaaaaaaaa',lead_source_by_diploma
            return lead_source_by_diploma

    @api.model
    def retrieve_source_by_cerification_data(self):
        retrieve_source_by_cerification_data = """select c.source_url,count(c.id) from crm_lead c join program_details p on c.program =p .id where p.lead_by_certification=True group by c.source_url ORDER BY count limit 5;"""
        self.env.cr.execute(retrieve_source_by_cerification_data)
        lead_source_by_certification = self._cr.dictfetchall()
        if len(lead_source_by_certification) == 0:
            return 'None'
        else:
            print'source certificationnnn', lead_source_by_certification
            return lead_source_by_certification

    @api.model
    def retrieve_admitted_data(self):
        dict1={}
        dict2={}
        dict3={}
        admitted_quaterly=[]

        current_date = datetime.now()
        month1 = current_date - relativedelta(months=4)
        month2 = month1 - relativedelta(months=4)
        month3 = month2 - relativedelta(months=4)

        retrieve_admitted_data1= """select team_id_name,count(id) from crm_lead where stage_id_name='Admitted' AND date_conversion >= '%s' AND date_conversion <= '%s' group by team_id_name;"""%(month3,month2)
        print"admitedd data1", retrieve_admitted_data1
        self.env.cr.execute(retrieve_admitted_data1)
        admitted_data1 = self._cr.dictfetchall()
        for rec in admitted_data1:
            dict1[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": "Quarterly"}
        dict1['month'] = var.get('month', False)
        admitted_quaterly.append(dict1)
        print"diccttttt", dict1

        retrieve_admitted_data2 = """select team_id_name,count(id) from crm_lead where stage_id_name='Admitted' AND date_conversion >= '%s' AND date_conversion <= '%s' group by team_id_name;""" % (
        month2, month1)
        print"admitedd data2", retrieve_admitted_data2
        self.env.cr.execute(retrieve_admitted_data2)
        admitted_data2 = self._cr.dictfetchall()
        for rec in admitted_data2:
            dict2[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": "Quarterly"}
        dict2['month'] = var.get('month', False)
        admitted_quaterly.append(dict2)
        print"diccttttt", dict2

        retrieve_admitted_data3 = """select team_id_name,count(id) from crm_lead where stage_id_name='Admitted' AND date_conversion >= '%s' AND date_conversion <= '%s' group by team_id_name;""" % (
        month1, current_date)
        print"admitedd data3",retrieve_admitted_data3
        self.env.cr.execute(retrieve_admitted_data3)
        admitted_data3 = self._cr.dictfetchall()
        for rec in admitted_data3:
            dict3[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": "Quarterly"}
        dict3['month'] = var.get('month', False)
        admitted_quaterly.append(dict3)
        print"diccttttt", dict3


        if len(admitted_quaterly) == 0:
            return 'None'
        else:

            print("admitted dataaaaaaaaaaaa",admitted_quaterly)
            return admitted_quaterly

    @api.model
    def retrieve_health_sec_per_faculty(self):


        dict={}
        health_sci_per_faculty=[]
        retrieve_health_sec_per_faculty = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1  group by c.team_id_name ORDER BY count desc limit 5 ;
"""
        self.env.cr.execute(retrieve_health_sec_per_faculty)
        health_science= self._cr.dictfetchall()
        for rec in health_science:
            dict[rec.get('team_id_name', False)] = rec.get('count', False)
        var2={"faculty":"Health Science"}
        dict['faculty'] = var2.get('faculty', False)
        health_sci_per_faculty.append(dict)
        print"diccttttt", dict


        if len(health_sci_per_faculty) == 0:
            return 'None'
        else:
            print"local_per_facultylocal_per_facultylocal_per_facultylocal_per_faculty",health_sci_per_faculty
            return health_sci_per_faculty

    @api.model
    def retrieve_it_dept_per_faculty(self):
        dict={}
        it_dept_per_faculty = []
        retrieve_it_dept_per_faculty = """select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=2  group by c.team_id_name ORDER BY count desc limit 5"""
        self.env.cr.execute(retrieve_it_dept_per_faculty)
        It_deptarment= self._cr.dictfetchall()
        for rec in It_deptarment:
            dict[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"faculty": "IT Department"}
        dict['faculty'] = var2.get('faculty', False)
        it_dept_per_faculty.append(dict)
        print"diccttttt", dict


        if len(it_dept_per_faculty) == 0:
            return 'None'
        else:
            print"local_per_facultylocal_per_facultylocal_per_facultylocal_per_faculty", it_dept_per_faculty
            return it_dept_per_faculty

    @api.model
    def retrieve_bussines_acc_per_faculty(self):
        dict = {}
        buss_acc_per_faculty = []
        retrieve_bussines_acc_per_faculty = """select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=3  group by c.team_id_name ORDER BY count desc limit 5"""
        self.env.cr.execute(retrieve_bussines_acc_per_faculty)
        bussiness_account = self._cr.dictfetchall()
        for rec in bussiness_account:
            dict[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"faculty": "Business Account"}
        dict['faculty'] = var2.get('faculty', False)
        buss_acc_per_faculty.append(dict)
        print"diccttttt", dict

        if len(buss_acc_per_faculty) == 0:
            return 'None'
        else:
            print"local_per_facultylocal_per_facultylocal_per_facultylocal_per_faculty", buss_acc_per_faculty
            return buss_acc_per_faculty


    @api.model
    def retrieve_health_opporunity(self):
        dict1 = {}
        dict2 = {}
        dict3 = {}
        dict4 = {}
        health_opportunity = []
        today = datetime.today()
        today1=datetime.today().strftime('%Y-%m-%d')
        datem2 = datetime(today.year, today.month, 1)
        datem1 = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')
        print type(datem1)
        cal = Calendar()  # week starts Monday
        # cal = Calendar(6) # week stars Sunday

        weeks = cal.monthdayscalendar(today.year, today.month)
        week1 = today - relativedelta(days=7)

        week2 = week1 - relativedelta(days=7)
        week3 = week2 - relativedelta(days=7)
        week4 = week3 - relativedelta(days=7)

        print type(weeks)

        retrieve_health_opporunity_local_week1 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;"""%(week3,week4)
        print("health_opportunity1",retrieve_health_opporunity_local_week1)
        self.env.cr.execute(retrieve_health_opporunity_local_week1)
        health_opportunity_local_week1 = self._cr.dictfetchall()
        print("")
        for rec in health_opportunity_local_week1:
            dict1[rec.get('team_id_name', False)] = rec.get('count', False)
        var2={"week":"week 4"}
        dict1['week'] = var2.get('week', False)

        health_opportunity.append(dict1)
        print"diccttttt", dict1
        retrieve_health_opporunity_local_week2 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;"""%(week2,week3)
        print("health_opportunity2", retrieve_health_opporunity_local_week2)
        self.env.cr.execute(retrieve_health_opporunity_local_week2)
        health_opportunity_local_week2 = self._cr.dictfetchall()
        for rec in health_opportunity_local_week2:
            dict2[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"week": "week 3"}
        dict2['week'] = var2.get('week', False)
        health_opportunity.append(dict2)
        print"diccttttt", dict2

        retrieve_health_opporunity_local_week3 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (week1, week2)
        print("health_opportunity3", retrieve_health_opporunity_local_week3)
        self.env.cr.execute(retrieve_health_opporunity_local_week3)
        health_opportunity_local_week3 = self._cr.dictfetchall()
        for rec in health_opportunity_local_week3:
            dict3[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"week": "week 2"}
        dict3['week'] = var2.get('week', False)
        health_opportunity.append(dict3)
        print"diccttttt", dict3

        retrieve_health_opporunity_local_week4 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
        today1, week1)
        print("health_opportunity4", retrieve_health_opporunity_local_week4)
        self.env.cr.execute(retrieve_health_opporunity_local_week3)
        health_opportunity_local_week4 = self._cr.dictfetchall()
        for rec in health_opportunity_local_week4:
            dict4[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"week": "week 1"}
        dict4['week'] = var2.get('week', False)
        health_opportunity.append(dict4)
        print"diccttttt", dict4

        if len(health_opportunity) == 0:
            return 'None'
        else:
            print "healthhhhhhhhhhhhhhhh",health_opportunity
            # print health_opportunity_inter
            return health_opportunity

    @api.model
    def retrieve_health_opporunity_months(self):
        month_1 = {}
        month_2= {}
        month_3 = {}
        month_4 = {}
        month_5 = {}
        month_6 = {}
        health_opportunity_months = []
        current_date = datetime.now()
        month1 = current_date - relativedelta(months=1)
        month_name1= month1.strftime("%b")
        print month_name1
        month2 = month1 - relativedelta(months=1)
        month_name2 = month2.strftime("%b")

        print month_name2
        month3 = month2 - relativedelta(months=1)
        month_name3 = month3.strftime("%b")
        print month_name3
        month4 = month3 - relativedelta(months=1)
        month_name4 = month4.strftime("%b")
        print  month_name4
        month5 = month4 - relativedelta(months=1)
        month_name5 = month5.strftime("%b")

        print month_name5
        month6 = month5 - relativedelta(months=1)
        month_name6 = month6.strftime("%b")
        print month_name6



        retrieve_health_opporunity_local_month1 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (month5, month6)
        print("rettrerjrfoeroeroereor", retrieve_health_opporunity_local_month1)
        self.env.cr.execute(retrieve_health_opporunity_local_month1)
        health_opportunity_local_months1 = self._cr.dictfetchall()
        print("health_opportunity_month6", health_opportunity_local_months1)
        for rec in health_opportunity_local_months1:
            month_1[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name6}
        month_1['month']=var.get('month',False)
        health_opportunity_months.append(month_1)

        print"diccttttt", health_opportunity_months

        retrieve_health_opporunity_local_month2 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (month4, month5)
        print("health_opportunity_month5", retrieve_health_opporunity_local_month2)
        self.env.cr.execute(retrieve_health_opporunity_local_month2)
        health_opportunity_local_month2 = self._cr.dictfetchall()
        for rec in health_opportunity_local_month2:
            month_2[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name5}
        month_2['month'] = var.get('month', False)
        health_opportunity_months.append(month_2)
        print"diccttttt", month_2

        retrieve_health_opporunity_local_month3 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (month3, month4)
        print("health_opportunity_month4", retrieve_health_opporunity_local_month3)
        self.env.cr.execute(retrieve_health_opporunity_local_month3)
        health_opportunity_local_month3 = self._cr.dictfetchall()
        for rec in health_opportunity_local_month3:
            month_3[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name4}
        month_3['month'] = var.get('month', False)
        health_opportunity_months.append(month_3)
        print"diccttttt", month_3

        retrieve_health_opporunity_local_month4 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            month2, month3)
        print("health_opportunity_month3", retrieve_health_opporunity_local_month4)
        self.env.cr.execute(retrieve_health_opporunity_local_month4)
        health_opportunity_local_month4 = self._cr.dictfetchall()
        for rec in health_opportunity_local_month4:
            month_4[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name3}
        month_4['month'] = var.get('month', False)
        health_opportunity_months.append(month_4)
        print"diccttttt", month_4

        retrieve_health_opporunity_local_month5 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            month1, month2)
        print("health_opportunity_month2", retrieve_health_opporunity_local_month5)
        self.env.cr.execute(retrieve_health_opporunity_local_month5)
        health_opportunity_local_month5 = self._cr.dictfetchall()
        for rec in health_opportunity_local_month5:
            month_5[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name2}
        month_5['month'] = var.get('month', False)
        health_opportunity_months.append(month_5)
        print"diccttttt", month_5

        retrieve_health_opporunity_local_month6 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            current_date, month1)
        print("health_opportunity_month1", retrieve_health_opporunity_local_month6)
        self.env.cr.execute(retrieve_health_opporunity_local_month6)
        health_opportunity_local_month6 = self._cr.dictfetchall()
        for rec in health_opportunity_local_month6:
            month_6[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name1}
        month_6['month'] = var.get('month', False)
        health_opportunity_months.append(month_6)
        print"diccttttt", month_6

        if len(health_opportunity_months) == 0:
            return 'None'
        else:
            print "healthhhhhhhhhhhhhhhh", health_opportunity_months
            # print health_opportunity_inter
            return health_opportunity_months

    @api.model
    def retrieve_it_dept_weeks(self):
        dict1 = {}
        dict2 = {}
        dict3 = {}
        dict4 = {}
        IT_Dept = []
        today = datetime.today()
        today1 = datetime.today().strftime('%Y-%m-%d')
        datem2 = datetime(today.year, today.month, 1)
        datem1 = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')
        print type(datem1)
        cal = Calendar()  # week starts Monday
        # cal = Calendar(6) # week stars Sunday

        weeks = cal.monthdayscalendar(today.year, today.month)
        week1 = today - relativedelta(days=7)

        week2 = week1 - relativedelta(days=7)
        week3 = week2 - relativedelta(days=7)
        week4 = week3 - relativedelta(days=7)

        print type(weeks)

        retrieve_it_dept_local_week1 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=2 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (week3, week4)
        print("retrieve_it_dept_local_week1", retrieve_it_dept_local_week1)
        self.env.cr.execute(retrieve_it_dept_local_week1)
        it_dept_local_week1 = self._cr.dictfetchall()
        print("")
        for rec in it_dept_local_week1:
            dict1[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"week": "week 4"}
        dict1['week'] = var2.get('week', False)

        IT_Dept.append(dict1)
        print"diccttttt", dict1
        retrieve_it_dept_local_week2 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=2 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
        week2, week3)
        print("retrieve_it_dept_local_week2", retrieve_it_dept_local_week2)
        self.env.cr.execute(retrieve_it_dept_local_week2)
        it_dept_local_week2 = self._cr.dictfetchall()
        for rec in it_dept_local_week2:
            dict2[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"week": "week 3"}
        dict2['week'] = var2.get('week', False)
        IT_Dept.append(dict2)
        print"diccttttt", dict2

        retrieve_it_dept_local_week3 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=2 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
        week1, week2)
        print("retrieve_it_dept_local_week3", retrieve_it_dept_local_week3)
        self.env.cr.execute(retrieve_it_dept_local_week3)
        it_dept_local_week3 = self._cr.dictfetchall()
        for rec in it_dept_local_week3:
            dict3[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"week": "week 2"}
        dict3['week'] = var2.get('week', False)
        IT_Dept.append(dict3)
        print"diccttttt", dict3

        retrieve_it_dept_local_week4 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=2 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
        today, week1)
        print("retrieve_it_dept_local_week4", retrieve_it_dept_local_week4)
        self.env.cr.execute(retrieve_it_dept_local_week4)
        it_dept_local_week4 = self._cr.dictfetchall()
        for rec in it_dept_local_week4:
            dict4[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"week": "week 1"}
        dict4['week'] = var2.get('week', False)
        IT_Dept.append(dict4)
        print"diccttttt", dict4

        if len(IT_Dept) == 0:
            return 'None'
        else:
            print "healthhhhhhhhhhhhhhhh", IT_Dept
            # print health_opportunity_inter
            return IT_Dept

    @api.model
    def retrieve_it_dept_months(self):
        month_1 = {}
        month_2 = {}
        month_3 = {}
        month_4 = {}
        month_5 = {}
        month_6 = {}
        IT_Dept_months = []
        current_date = datetime.now()
        month1 = current_date - relativedelta(months=1)
        month_name1 = month1.strftime("%b")
        print month1
        month2 = month1 - relativedelta(months=1)
        month_name2 = month2.strftime("%b")

        print month2
        month3 = month2 - relativedelta(months=1)
        month_name3 = month3.strftime("%b")
        print month3
        month4 = month3 - relativedelta(months=1)
        month_name4 = month4.strftime("%b")
        print  month4
        month5 = month4 - relativedelta(months=1)
        month_name5 = month5.strftime("%b")
        print month5
        month6 = month5 - relativedelta(months=1)
        month_name6 = month6.strftime("%b")
        print month6

        retrieve_it_dept_local_month1 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=2 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            month5, month6)
        print("retrieve_it_dept_local_month1", retrieve_it_dept_local_month1)
        self.env.cr.execute(retrieve_it_dept_local_month1)
        it_dept_local_months1 = self._cr.dictfetchall()
        print("")

        for rec in it_dept_local_months1:
            month_1[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name6}
        month_1['month'] = var.get('month', False)
        IT_Dept_months.append(month_1)

        print"diccttttt", IT_Dept_months

        retrieve_it_dept_local_month2 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=2 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
        month4, month5)
        print("retrieve_it_dept_local_month2", retrieve_it_dept_local_month2)
        self.env.cr.execute(retrieve_it_dept_local_month2)
        it_dept_local_months2 = self._cr.dictfetchall()
        for rec in it_dept_local_months2:
            month_2[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name5}
        month_2['month'] = var.get('month', False)
        IT_Dept_months.append(month_2)
        print"diccttttt", month_2

        retrieve_it_dept_local_month3 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=2 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
        month3, month4)
        print("retrieve_it_dept_local_month3", retrieve_it_dept_local_month3)
        self.env.cr.execute(retrieve_it_dept_local_month3)
        it_dept_local_months3 = self._cr.dictfetchall()
        for rec in it_dept_local_months3:
            month_3[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name4}
        month_3['month'] = var.get('month', False)
        IT_Dept_months.append(month_3)
        print"diccttttt", month_3

        retrieve_it_dept_local_month4 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=2 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            month2, month3)
        print("retrieve_it_dept_local_month4", retrieve_it_dept_local_month4)
        self.env.cr.execute(retrieve_it_dept_local_month4)
        it_dept_local_months4 = self._cr.dictfetchall()
        for rec in it_dept_local_months4:
            month_4[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name3}
        month_4['month'] = var.get('month', False)
        IT_Dept_months.append(month_4)
        print"diccttttt", month_4

        retrieve_it_dept_local_month5 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=2 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            month1, month2)
        print("retrieve_it_dept_local_month5", retrieve_it_dept_local_month5)
        self.env.cr.execute(retrieve_it_dept_local_month5)
        it_dept_local_months5 = self._cr.dictfetchall()
        for rec in it_dept_local_months5:
            month_5[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name2}
        month_5['month'] = var.get('month', False)
        IT_Dept_months.append(month_5)
        print"diccttttt", month_5

        retrieve_it_dept_local_month6 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=2 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            current_date, month1)
        print("retrieve_it_dept_local_month6", retrieve_it_dept_local_month6)
        self.env.cr.execute(retrieve_it_dept_local_month6)
        it_dept_local_months6 = self._cr.dictfetchall()
        for rec in it_dept_local_months6:
            month_6[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name1}
        month_6['month'] = var.get('month', False)
        IT_Dept_months.append(month_6)
        print"diccttttt", month_6

        if len(IT_Dept_months) == 0:
            return 'None'
        else:
            print "healthhhhhhhhhhhhhhhh", IT_Dept_months
            # print health_opportunity_inter
            return IT_Dept_months

    @api.model
    def retrieve_bussines_acc_weeks(self):
        dict1 = {}
        dict2 = {}
        dict3 = {}
        dict4 = {}
        bussines_and_acc_weeks= []
        today = datetime.today()
        today1 = datetime.today().strftime('%Y-%m-%d')
        datem2 = datetime(today.year, today.month, 1)
        datem1 = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')
        print type(datem1)
        cal = Calendar()  # week starts Monday
        # cal = Calendar(6) # week stars Sunday

        weeks = cal.monthdayscalendar(today.year, today.month)
        week1 = today - relativedelta(days=7)

        week2 = week1 - relativedelta(days=7)
        week3 = week2 - relativedelta(days=7)
        week4 = week3 -relativedelta(days=7)

        print type(weeks)

        retrieve_bussines_acc_local_week1 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=3 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            week3, week4)
        print("retrieve_bussines_acc_local_week1", retrieve_bussines_acc_local_week1)
        self.env.cr.execute(retrieve_bussines_acc_local_week1)
        business_acc_local_week1 = self._cr.dictfetchall()
        print("")
        for rec in business_acc_local_week1:
            dict1[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"week": "week 4"}
        dict1['week'] = var2.get('week', False)
        bussines_and_acc_weeks.append(dict1)
        print"diccttttt", dict1

        retrieve_bussines_acc_local_week2 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=3 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            week2, week3)
        print("retrieve_bussines_acc_local_week2", retrieve_bussines_acc_local_week2)
        self.env.cr.execute(retrieve_bussines_acc_local_week2)
        business_acc_local_week2 = self._cr.dictfetchall()
        for rec in business_acc_local_week2:
            dict2[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"week": "week 3"}
        dict2['week'] = var2.get('week', False)
        bussines_and_acc_weeks.append(dict2)
        print"diccttttt", dict2

        retrieve_bussines_acc_local_week3 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=3 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            week1, week2)
        print("retrieve_bussines_acc_local_week3", retrieve_bussines_acc_local_week3)
        self.env.cr.execute(retrieve_bussines_acc_local_week3)
        business_acc_local_week3 = self._cr.dictfetchall()
        for rec in business_acc_local_week3:
            dict3[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"week": "week 2"}
        dict3['week'] = var2.get('week', False)
        bussines_and_acc_weeks.append(dict3)
        print"diccttttt", dict3

        retrieve_bussines_acc_local_week4 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=3 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            today1, week1)
        print("retrieve_bussines_acc_local_week4", retrieve_bussines_acc_local_week4)
        self.env.cr.execute(retrieve_bussines_acc_local_week4)
        business_acc_local_week4 = self._cr.dictfetchall()
        for rec in business_acc_local_week4:
            dict4[rec.get('team_id_name', False)] = rec.get('count', False)
        var2 = {"week": "week 1"}
        dict4['week'] = var2.get('week', False)
        bussines_and_acc_weeks.append(dict4)
        print"diccttttt", dict4

        if len(bussines_and_acc_weeks) == 0:
            return 'None'
        else:
            print "healthhhhhhhhhhhhhhhh", bussines_and_acc_weeks
            # print health_opportunity_inter
            return bussines_and_acc_weeks

    @api.model
    def retrieve_bussines_acc_months(self):
        month_1 = {}
        month_2 = {}
        month_3 = {}
        month_4 = {}
        month_5 = {}
        month_6 = {}
        bussines_acc_months = []
        current_date = datetime.now()
        month1 = current_date - relativedelta(months=1)
        month_name1 = month1.strftime("%b")
        print month1
        month2 = month1 - relativedelta(months=1)
        month_name2 = month2.strftime("%b")
        print month2
        month3 = month2 - relativedelta(months=1)
        month_name3 = month3.strftime("%b")
        print month3
        month4 = month3 - relativedelta(months=1)
        month_name4 = month4.strftime("%b")
        print  month4
        month5 = month4 - relativedelta(months=1)
        month_name5 = month5.strftime("%b")
        print month5
        month6 = month5 - relativedelta(months=1)
        month_name6 = month6.strftime("%b")
        print month6

        retrieve_bussines_acc_local_month1 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=3 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            month5, month6)
        print("rettrerjrfoeroeroereor", retrieve_bussines_acc_local_month1)
        self.env.cr.execute(retrieve_bussines_acc_local_month1)
        bussines_acc_local_months1 = self._cr.dictfetchall()
        print("")

        for rec in bussines_acc_local_months1:
            month_1[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name6}
        month_1['month'] = var.get('month', False)
        bussines_acc_months.append(month_1)

        print"diccttttt", bussines_acc_months

        retrieve_bussines_acc_local_month2 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=3 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            month4, month5)
        print("rettrerjrfoeroeroereor", retrieve_bussines_acc_local_month2)
        self.env.cr.execute(retrieve_bussines_acc_local_month2)
        bussines_acc_local_months2 = self._cr.dictfetchall()
        for rec in bussines_acc_local_months2:
            month_2[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name5}
        month_2['month'] = var.get('month', False)
        bussines_acc_months.append(month_2)
        print"diccttttt", month_2

        retrieve_bussines_acc_local_month3 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=3 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            month3, month4)
        print("rettrerjrfoeroeroereor", retrieve_bussines_acc_local_month3)
        self.env.cr.execute(retrieve_bussines_acc_local_month3)
        bussines_acc_local_months3 = self._cr.dictfetchall()
        for rec in bussines_acc_local_months3:
            month_3[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name4}
        month_3['month'] = var.get('month', False)
        bussines_acc_months.append(month_3)
        print"diccttttt", month_3

        retrieve_bussines_acc_local_month4 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=3 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            month2, month3)
        print("rettrerjrfoeroeroereor", retrieve_bussines_acc_local_month4)
        self.env.cr.execute(retrieve_bussines_acc_local_month4)
        bussines_acc_local_months4 = self._cr.dictfetchall()
        for rec in bussines_acc_local_months4:
            month_4[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name3}
        month_4['month'] = var.get('month', False)
        bussines_acc_months.append(month_4)
        print"diccttttt", month_4

        retrieve_bussines_acc_local_month5 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=3 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            month1, month2)
        print("rettrerjrfoeroeroereor", retrieve_bussines_acc_local_month5)
        self.env.cr.execute(retrieve_bussines_acc_local_month5)
        bussines_acc_local_months5 = self._cr.dictfetchall()
        for rec in bussines_acc_local_months5:
            month_5[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name2}
        month_5['month'] = var.get('month', False)
        bussines_acc_months.append(month_5)
        print"diccttttt", month_5

        retrieve_bussines_acc_local_month6 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=3 AND c.date_conversion <= '%s'  AND c.date_conversion >= '%s' group by c.team_id_name ORDER BY count desc limit 5 ;""" % (
            current_date, month1)
        print("rettrerjrfoeroeroereor", retrieve_bussines_acc_local_month6)
        self.env.cr.execute(retrieve_bussines_acc_local_month6)
        bussines_acc_local_months6 = self._cr.dictfetchall()
        for rec in bussines_acc_local_months6:
            month_6[rec.get('team_id_name', False)] = rec.get('count', False)
        var = {"month": month_name1}
        month_6['month'] = var.get('month', False)
        bussines_acc_months.append(month_6)
        print"diccttttt", month_6

        if len(bussines_acc_months) == 0:
            return 'None'
        else:
            print "healthhhhhhhhhhhhhhhh", bussines_acc_months
            # print health_opportunity_inter
            return bussines_acc_months







        # retrieve_health_opporunity_local_week2 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.create_date >= current_date-interval '14' day group by c.team_id_name ORDER BY count desc limit 5 ;"""
        # self.env.cr.execute(retrieve_health_opporunity_local_week2)
        # health_opportunity_local_week2 = self._cr.dictfetchall()
        # for rec in health_opportunity_local_week2:
        #     dict2[rec.get('team_id_name', False)] = rec.get('count', False)
        # health_opportunity.append(dict2)
        # print"diccttttt", dict2
        # retrieve_health_opporunity_local_week3 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.create_date >= current_date-interval '21' day group by c.team_id_name ORDER BY count desc limit 5 ;"""
        # self.env.cr.execute(retrieve_health_opporunity_local_week3)
        # health_opportunity_local_week3 = self._cr.dictfetchall()
        # for rec in health_opportunity_local_week3:
        #     dict3[rec.get('team_id_name', False)] = rec.get('count', False)
        # health_opportunity.append(dict3)
        #
        #
        #
        # print"diccttttt",dict3
        #
        # if len(health_opportunity) == 0:
        #     return 'None'
        # else:
        #     print "healthhhhhhhhhhhhhhhh",health_opportunity
        #     # print health_opportunity_inter
        #     return health_opportunity
            #     # return [{'week':2203,'local':456,'International':12},{'week':2003,'local':46,'International':10}]

    # def get_data(self):
    #     today = datetime.today()
    #     datem = datetime(today.year, today.month, 1)
    #     cal = Calendar()  # week starts Monday
    #     # cal = Calendar(6) # week stars Sunday
    #
    #     weeks = cal.monthdayscalendar(today.year, today.month)
    #     for x in range(len(weeks)):
    #         if today.day in weeks[x]:
    #             print, x
    #     crm_rec = self.env['crm.lead']
    #     retrieve_health_opporunity_local_week1 = """ select c.team_id_name,count(p.faculty_id) from crm_lead c join program_details p on c.program = p.id where p.faculty_id=1 AND c.create_date >= current_date-interval '30' day group by c.team_id_name ORDER BY count desc limit 5 ;"""
    #     self.env.cr.execute(retrieve_health_opporunity_local_week1)
    #     health_opportunity_local_week1 = self._cr.dictfetchall()
    #     if crm_rec.create_date >= datem and crm_rec.create_date<= today:
    #         print




