from odoo import models,fields,api,_
from datetime import datetime
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



            'new_opportunity':0 ,

            'lost_opportunity':0,

            'opportunity_total':0,

            'prospect_total':0,

            'admitted_total':0,

            'enrolled_total':0,

            'delayed_total': 0,

            'lead_con_ratio':0,

            'opportunity_ratio':0,

            'leads_ratio':0,

            'sales_ratio': 0,

            'lead_to_opp_ratio1':0,
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





        # Lead Opportunity Ratio

        leads=self.search([
            ('create_date','>=',date4),
            ('type','=','lead'),
        ])
        total_leads=len(leads)
        # if leads:
        #     opportunity = self.search([
        #         ('conversion_date', '>=', date4),
        #         ('type','!=','lead'),
        #         # ('stage_id.name','=','Opportunity'),
        #     ])
        #     opp=len(opportunity)
        #     total=float(ld + opp)
        #     if opp:
        #         ratio= float(total/opp)
        #         opp_ratio=("%.1f" % round(ratio, 1))
        result['leads_ratio']=total_leads

        # Lead to Sales Ratio

        opportunity = self.search([
            ('date_conversion', '>=', date4),
            ('type', '!=', 'lead'),
        ])
        total_opportunity = len(opportunity)
        result['opportunity_ratio'] = total_opportunity

        sales = self.search([
                    ('type', '!=', 'lead'),
                    ('stage_id.name','=','Won'),
                    ('date_conversion', '>=', date4),
                ])
        total_sales = len(sales)
        result['sales_ratio'] = total_sales

        # if leads:
        #     opportunity = self.search([
        #         ('type', '!=', 'lead'),
        #         ('stage_id.name','=','Won'),
        #         ('conversion_date', '>=', date4),
        #     ])
        #     sales = len(opportunity)
        #     total=float(ld + sales)
        #     if sales:
        #         ratio = float(total/sales)
        #         sale_ratio = ("%.1f" % round(ratio, 1))
        #         result['lead_to_sales_ratio'] = sale_ratio

        # product calculation

        retrieve_dip_data = """select p.product_name,c.type,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id inner join (select p.id,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id  group by p.id ORDER BY count desc limit 5) pt on p.id =pt.id group by p.product_name,c.type;
"""
        self.env.cr.execute(retrieve_dip_data)
        lead_by_diploma = self.env.cr.dictfetchall()
        lead_by_diploma_list=[]
        opportunity = lead = 0
        if lead_by_diploma[0]['type'] == 'opportunity':
            opportunity = lead_by_diploma[0]['count']
        else:
            lead = lead_by_diploma[0]['count']
        first_rec={'product_name':lead_by_diploma[0]['product_name'],'lead':lead,'opportunity':opportunity}
        lead_by_diploma_list.append(first_rec)
        for rec in lead_by_diploma:
            rec_exists=False
            for recs in lead_by_diploma_list:
                if rec['product_name'] ==recs['product_name']:
                    rec_exists=True
                    if rec['type'] == 'opportunity':
                        recs['opportunity'] = rec['count']
                    else:
                        recs['lead'] = rec['count']
            if not rec_exists:
                opportunity = lead = 0
                if rec['type'] == 'opportunity':
                    opportunity = rec['count']
                else:
                    lead = rec['count']
                lead_by_diploma_list.append(
                    {'product_name': rec['product_name'], 'opportunity': opportunity, 'lead': lead})
        # dict=[]
        # lead=[]
        # oppo=[]
        # for count in lead_by_diploma_list:
        #     lead_value = count['lead']
        #     lead.append(lead_value)
        #
        #     oppo_value = count['opportunity']
        #     oppo.append(oppo_value)
        # total_lead= sum(lead)
        # dict1={'total_lead':total_lead}
        # dict.append(dict1)
        #
        # total_oppo= sum(oppo)
        # dict2={'total_oppo':total_oppo}
        # dict.append(dict2)
        #
        #
        # print total_lead
        # print total_oppo

        if len(lead_by_diploma_list) == 0:
            return '0'
        else:
            print("retrieve_dip_data", lead_by_diploma_list)
            result['lead_to_opp_ratio1']= lead_by_diploma_list












        return result


    @api.model
    def retrieve_monthly_health_oppo_data(self):
        dict1 = {}
        dict2 = {}
        dict3 = {}
        dict4 = {}
        dict5 = {}
        dict6 = {}
        dict7 = {}
        dict8 = {}
        dict9 = {}
        dict10 = {}
        dict11 = {}
        dict12 = {}

        current_date = datetime.now()
        month1 = current_date - relativedelta(months=1)
        month_name1 = month1.strftime("%b")
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

        month7 = month6 - relativedelta(months=1)
        month_name7 = month7.strftime("%b")
        print month_name7
        month8 = month7 - relativedelta(months=1)
        month_name8 = month8.strftime("%b")

        print month_name8
        month9 = month8 - relativedelta(months=1)
        month_name9 = month9.strftime("%b")
        print month_name9
        month10 = month9 - relativedelta(months=1)
        month10_1 = month10.strftime('%Y-%m-%d')
        month_name10 = month10.strftime("%b")
        print  month_name10
        month11 = month10 - relativedelta(months=1)
        month11_1 = month11.strftime('%Y-%m-%d')
        month_name11 = month11.strftime("%b")

        print month_name11
        month12 = month11 - relativedelta(months=1)
        month_name12 = month12.strftime("%b")
        print month_name12
        current_health_opportunity = []

        # retrieve_monthly_health_oppo_data_1= """select stage_id_name,count(id) from crm_lead where type='opportunity' AND create_date>='%s' AND create_date<='%s' group by type,stage_id_name ORDER by count;""" % (
        #     month12, month11,)
        # print"retrieve_lead_by_diploma_month_data", retrieve_monthly_health_oppo_data_1
        # self.env.cr.execute(retrieve_monthly_health_oppo_data_1)
        # current_monthly_health_1= self.env.cr.dictfetchall()
        # for rec in current_monthly_health_1:
        #     dict1[rec.get('stage_id_name', False)] = rec.get('count', False)
        # var = {"month": month_name12}
        # dict1['month'] = var.get('month', False)
        # current_health_opportunity.append(dict1)
        # print"diccttttt1", dict1
        #
        # retrieve_monthly_health_oppo_data_2 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND create_date>='%s' AND create_date<='%s' group by type,stage_id_name ORDER by count;""" % (
        #     month11, month10)
        # print"varrrrrrrrrrrrr", retrieve_monthly_health_oppo_data_2
        # self.env.cr.execute(retrieve_monthly_health_oppo_data_2)
        # current_monthly_health_2 = self.env.cr.dictfetchall()
        # for rec in current_monthly_health_2:
        #     dict2[rec.get('stage_id_name', False)] = rec.get('count', False)
        # var = {"month": month_name11}
        # dict2['month'] = var.get('month', False)
        # current_health_opportunity.append(dict2)
        # print"dict2", dict2
        #
        # retrieve_monthly_health_oppo_data_3 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND create_date>='%s' AND create_date<='%s' group by type,stage_id_name ORDER by count;""" % (
        #     month10, month9)
        # print"varrrrrrrrrrrrr", retrieve_monthly_health_oppo_data_3
        # self.env.cr.execute(retrieve_monthly_health_oppo_data_3)
        # current_monthly_health_3 = self.env.cr.dictfetchall()
        # for rec in current_monthly_health_3:
        #     dict3[rec.get('stage_id_name', False)] = rec.get('count', False)
        # var = {"month": month_name10}
        # dict3['month'] = var.get('month', False)
        # current_health_opportunity.append(dict3)
        # print"dict3", dict3
        #
        # retrieve_monthly_health_oppo_data_4 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND create_date>='%s' AND create_date<='%s' group by type,stage_id_name ORDER by count;""" % (
        #     month9, month8)
        # print"varrrrrrrrrrrrr", retrieve_monthly_health_oppo_data_4
        # self.env.cr.execute(retrieve_monthly_health_oppo_data_4)
        # current_monthly_health_4 = self.env.cr.dictfetchall()
        # for rec in current_monthly_health_4:
        #     dict4[rec.get('stage_id_name', False)] = rec.get('count', False)
        # var = {"month": month_name9}
        # dict4['month'] = var.get('month', False)
        # current_health_opportunity.append(dict4)
        # print"dict4", dict4
        #
        # retrieve_monthly_health_oppo_data_5 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND create_date>='%s' AND create_date<='%s' group by type,stage_id_name ORDER by count;""" % (
        #     month8, month7)
        # print"varrrrrrrrrrrrr", retrieve_monthly_health_oppo_data_5
        # self.env.cr.execute(retrieve_monthly_health_oppo_data_5)
        # current_monthly_health_5 = self.env.cr.dictfetchall()
        # for rec in current_monthly_health_5:
        #     dict5[rec.get('stage_id_name', False)] = rec.get('count', False)
        # var = {"month": month_name8}
        # dict5['month'] = var.get('month', False)
        # current_health_opportunity.append(dict5)
        # print"dict5", dict5
        #
        # retrieve_monthly_health_oppo_data_6= """select stage_id_name,count(id) from crm_lead where type='opportunity' AND create_date>='%s' AND create_date<='%s' group by type,stage_id_name ORDER by count;""" % (
        #     month7, month6)
        # print"varrrrrrrrrrrrr", retrieve_monthly_health_oppo_data_6
        # self.env.cr.execute(retrieve_monthly_health_oppo_data_6)
        # current_monthly_health_6 = self.env.cr.dictfetchall()
        # for rec in current_monthly_health_6:
        #     dict6[rec.get('stage_id_name', False)] = rec.get('count', False)
        # var = {"month": month_name7}
        # dict6['month'] = var.get('month', False)
        # current_health_opportunity.append(dict6)
        # print"dict6", dict6

        retrieve_monthly_health_oppo_data_7 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND date_conversion >='%s' AND date_conversion<='%s' group by type,stage_id_name ORDER by count;""" % (
            month6, month5)
        print"varrrrrrrrrrrrr", retrieve_monthly_health_oppo_data_7
        self.env.cr.execute(retrieve_monthly_health_oppo_data_7)
        current_monthly_health_7 = self.env.cr.dictfetchall()
        for rec in current_monthly_health_7:
            dict7[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name6}
        dict7['month'] = var.get('month', False)
        current_health_opportunity.append(dict7)
        print"dict7", dict7

        retrieve_monthly_health_oppo_data_8 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND date_conversion >='%s' AND date_conversion<='%s' group by type,stage_id_name ORDER by count;""" % (
            month5, month4)
        print"varrrrrrrrrrrrr", retrieve_monthly_health_oppo_data_8
        self.env.cr.execute(retrieve_monthly_health_oppo_data_8)
        current_monthly_health_8 = self.env.cr.dictfetchall()
        for rec in current_monthly_health_8:
            dict8[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name5}
        dict8['month'] = var.get('month', False)
        current_health_opportunity.append(dict8)
        print"dict8", dict8

        retrieve_monthly_health_oppo_data_9 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND date_conversion >='%s' AND date_conversion<='%s' group by type,stage_id_name ORDER by count;""" % (
            month4, month3)
        print"varrrrrrrrrrrrr", retrieve_monthly_health_oppo_data_9
        self.env.cr.execute(retrieve_monthly_health_oppo_data_9)
        current_monthly_health_9 = self.env.cr.dictfetchall()
        for rec in current_monthly_health_9:
            dict9[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name4}
        dict9['month'] = var.get('month', False)
        current_health_opportunity.append(dict9)
        print"dict9", dict9

        retrieve_monthly_health_oppo_data_10 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND date_conversion >='%s' AND date_conversion<='%s' group by type,stage_id_name ORDER by count;""" % (
            month3, month2)
        print"varrrrrrrrrrrrr", retrieve_monthly_health_oppo_data_10
        self.env.cr.execute(retrieve_monthly_health_oppo_data_10)
        current_monthly_health_10 = self.env.cr.dictfetchall()
        for rec in current_monthly_health_10:
            dict10[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name3}
        dict10['month'] = var.get('month', False)
        current_health_opportunity.append(dict10)
        print"diccttttt10", dict10

        retrieve_monthly_health_oppo_data_11 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND date_conversion >='%s' AND date_conversion<='%s' group by type,stage_id_name ORDER by count;""" % (
            month2, month1)
        print"varrrrrrrrrrrrr", retrieve_monthly_health_oppo_data_11
        self.env.cr.execute(retrieve_monthly_health_oppo_data_11)
        current_monthly_health_11 = self.env.cr.dictfetchall()
        for rec in current_monthly_health_11:
            dict11[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name2}
        dict11['month'] = var.get('month', False)
        current_health_opportunity.append(dict11)
        print"diccttttt11", dict11

        retrieve_monthly_health_oppo_data_12 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND date_conversion >='%s' AND date_conversion<='%s' group by type,stage_id_name ORDER by count;""" % (
            month1, current_date)
        print"varrrrrrrrrrrrr", retrieve_monthly_health_oppo_data_12
        self.env.cr.execute(retrieve_monthly_health_oppo_data_12)
        current_monthly_health_12 = self.env.cr.dictfetchall()
        for rec in current_monthly_health_12:
            dict12[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name1}
        dict12['month'] = var.get('month', False)
        current_health_opportunity.append(dict12)
        print"diccttttt12", dict12


        if len(current_health_opportunity) == 0:
            return 'None'
        else:
            print"month dattattttaaa", current_health_opportunity
            return current_health_opportunity


    @api.model
    def retrieve_monthly_source_data(self):
        dict1 = {}
        dict2 = {}
        dict3 = {}
        dict4 = {}
        dict5 = {}
        dict6 = {}
        dict7 = {}
        dict8 = {}
        dict9 = {}
        dict10 = {}
        dict11 = {}
        dict12 = {}

        current_date = datetime.now()
        month1 = current_date - relativedelta(months=1)
        month_name1 = month1.strftime("%b")
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

        month7 = month6 - relativedelta(months=1)
        month_name7 = month7.strftime("%b")
        print month_name7
        month8 = month7 - relativedelta(months=1)
        month_name8 = month8.strftime("%b")

        print month_name8
        month9 = month8 - relativedelta(months=1)
        month_name9 = month9.strftime("%b")
        print month_name9
        month10 = month9 - relativedelta(months=1)
        month10_1 = month10.strftime('%Y-%m-%d')
        month_name10 = month10.strftime("%b")
        print  month_name10
        month11 = month10 - relativedelta(months=1)
        month11_1 = month11.strftime('%Y-%m-%d')
        month_name11 = month11.strftime("%b")

        print month_name11
        month12 = month11 - relativedelta(months=1)
        month_name12 = month12.strftime("%b")
        print month_name12
        source_data_month = []
        current_date = datetime.now()
        months = current_date - relativedelta(months=12)
        retrieve_monthly_source_data = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' group by source_of_lead ORDER BY count desc limit 3;""" % (
        months, current_date)
        print"retrieve_lead_by_diploma_month_data", retrieve_monthly_source_data
        self.env.cr.execute(retrieve_monthly_source_data)
        current_month_source = self.env.cr.dictfetchall()
        list_id = []
        source_list = []
        for rec in current_month_source:
            id = str(rec['source_of_lead'])

            source_list.append(id)
            # source_list.append(rec['source_of_lead'])
        print"iddddididi", list_id
        ids = str(tuple(source_list))
        source_data_month.append(source_list)
        # monthly_source_1 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
        #     month12, month11, ids)
        # print"varrrrrrrrrrrrr", monthly_source_1
        # self.env.cr.execute(monthly_source_1)
        # source_data_1 = self.env.cr.dictfetchall()
        # for rec in source_data_1:
        #     dict1[rec.get('source_of_lead', False)] = rec.get('count', False)
        # var = {"month": month_name12}
        # dict1['month'] = var.get('month', False)
        # source_data_month.append(dict1)
        # print"diccttttt1", dict1
        #
        # monthly_source_2 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
        #     month11, month10, ids)
        # print"varrrrrrrrrrrrr", monthly_source_2
        # self.env.cr.execute(monthly_source_2)
        # source_data_2 = self.env.cr.dictfetchall()
        # for rec in source_data_2:
        #     dict2[rec.get('source_of_lead', False)] = rec.get('count', False)
        # var = {"month": month_name11}
        # dict2['month'] = var.get('month', False)
        # source_data_month.append(dict2)
        # print"dict2", dict2
        #
        # monthly_source_3 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
        #     month10, month9, ids)
        # print"varrrrrrrrrrrrr", monthly_source_3
        # self.env.cr.execute(monthly_source_3)
        # source_data_3 = self.env.cr.dictfetchall()
        # for rec in source_data_3:
        #     dict3[rec.get('source_of_lead', False)] = rec.get('count', False)
        # var = {"month": month_name10}
        # dict3['month'] = var.get('month', False)
        # source_data_month.append(dict3)
        # print"dict3", dict3
        #
        # monthly_source_4 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
        #     month9, month8, ids)
        # print"varrrrrrrrrrrrr", monthly_source_4
        # self.env.cr.execute(monthly_source_4)
        # source_data_4 = self.env.cr.dictfetchall()
        # for rec in source_data_4:
        #     dict4[rec.get('source_of_lead', False)] = rec.get('count', False)
        # var = {"month": month_name9}
        # dict4['month'] = var.get('month', False)
        # source_data_month.append(dict4)
        # print"dict4", dict4
        #
        # monthly_source_5 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
        #     month8, month7, ids)
        # print"varrrrrrrrrrrrr", monthly_source_5
        # self.env.cr.execute(monthly_source_5)
        # source_data_5 = self.env.cr.dictfetchall()
        # for rec in source_data_5:
        #     dict5[rec.get('source_of_lead', False)] = rec.get('count', False)
        # var = {"month": month_name8}
        # dict5['month'] = var.get('month', False)
        # source_data_month.append(dict5)
        # print"dict5", dict5
        #
        # monthly_source_6 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
        #     month7, month6, ids)
        # print"varrrrrrrrrrrrr", monthly_source_6
        # self.env.cr.execute(monthly_source_6)
        # source_data_6 = self.env.cr.dictfetchall()
        # for rec in source_data_6:
        #     dict6[rec.get('source_of_lead', False)] = rec.get('count', False)
        # var = {"month": month_name7}
        # dict6['month'] = var.get('month', False)
        # source_data_month.append(dict6)
        # print"dict6", dict6

        monthly_source_7 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
            month6, month5, ids)
        print"varrrrrrrrrrrrr", monthly_source_7
        self.env.cr.execute(monthly_source_7)
        source_data_7 = self.env.cr.dictfetchall()
        for rec in source_data_7:
            dict7[rec.get('source_of_lead', False)] = rec.get('count', False)
        var = {"month": month_name6}
        dict7['month'] = var.get('month', False)
        source_data_month.append(dict7)
        print"dict7", dict7

        monthly_source_8 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
            month5, month4, ids)
        print"varrrrrrrrrrrrr", monthly_source_8
        self.env.cr.execute(monthly_source_8)
        source_data_8 = self.env.cr.dictfetchall()
        for rec in source_data_8:
            dict8[rec.get('source_of_lead', False)] = rec.get('count', False)
        var = {"month": month_name5}
        dict8['month'] = var.get('month', False)
        source_data_month.append(dict8)
        print"dict8", dict8

        monthly_source_9 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
            month4, month3, ids)
        print"varrrrrrrrrrrrr", monthly_source_9
        self.env.cr.execute(monthly_source_9)
        source_data_9 = self.env.cr.dictfetchall()
        for rec in source_data_9:
            dict9[rec.get('source_of_lead', False)] = rec.get('count', False)
        var = {"month": month_name4}
        dict9['month'] = var.get('month', False)
        source_data_month.append(dict9)
        print"dict9", dict9

        monthly_source_10 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
            month3, month2, ids)
        print"varrrrrrrrrrrrr", monthly_source_10
        self.env.cr.execute(monthly_source_10)
        source_data_10 = self.env.cr.dictfetchall()
        for rec in source_data_10:
            dict10[rec.get('source_of_lead', False)] = rec.get('count', False)
        var = {"month": month_name3}
        dict10['month'] = var.get('month', False)
        source_data_month.append(dict10)
        print"diccttttt10", dict10

        monthly_source_11 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
            month2, month1, ids)
        print"varrrrrrrrrrrrr", monthly_source_11
        self.env.cr.execute(monthly_source_11)
        source_data_11 = self.env.cr.dictfetchall()
        for rec in source_data_11:
            dict11[rec.get('source_of_lead', False)] = rec.get('count', False)
        var = {"month": month_name2}
        dict11['month'] = var.get('month', False)
        source_data_month.append(dict11)
        print"diccttttt11", dict11

        monthly_source_12 = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >= '%s' AND create_date <='%s' AND source_of_lead IN %s group by source_of_lead ORDER BY count;""" % (
            month1, current_date, ids)
        print"varrrrrrrrrrrrr", monthly_source_12
        self.env.cr.execute(monthly_source_12)
        source_data_12 = self.env.cr.dictfetchall()
        for rec in source_data_12:
            dict12[rec.get('source_of_lead', False)] = rec.get('count', False)
        var = {"month": month_name1}
        dict12['month'] = var.get('month', False)
        source_data_month.append(dict12)
        print"diccttttt12", dict12

        if len(source_data_month) == 0:
            return 'None'
        else:
            print"month dattattttaaa", source_data_month
            return source_data_month

    @api.model
    def retrieve_monthly_leads_data(self):


        dict1 = {}
        dict2 = {}
        dict3 = {}
        dict4 = {}
        dict5 = {}
        dict6 = {}
        dict7 = {}
        dict8 = {}
        dict9 = {}
        dict10 = {}
        dict11 = {}
        dict12 = {}


        current_date = datetime.now()
        month1 = current_date - relativedelta(months=1)
        month_name1 = month1.strftime("%b")
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

        month7 = month6 - relativedelta(months=1)
        month_name7 = month7.strftime("%b")
        print month_name7
        month8 = month7 - relativedelta(months=1)
        month_name8 = month8.strftime("%b")

        print month_name8
        month9 = month8 - relativedelta(months=1)
        month_name9 = month9.strftime("%b")
        print month_name9
        month10 = month9 - relativedelta(months=1)
        month10_1= month10.strftime('%Y-%m-%d')
        month_name10 = month10.strftime("%b")
        print  month_name10
        month11 = month10 - relativedelta(months=1)
        month11_1 = month11.strftime('%Y-%m-%d')
        month_name11 = month11.strftime("%b")

        print month_name11
        month12 = month11 - relativedelta(months=1)
        month_name12 = month12.strftime("%b")
        print month_name12
        leads_data_month=[]
        current_date = datetime.now()
        months = current_date - relativedelta(months=12)
        retrieve_monthly_leads_data = """select p.id,p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' group by p.product_name,p.id ORDER BY count desc limit 3;""" %(months, current_date)
        print"retrieve_monthly_leads_data",retrieve_monthly_leads_data
        self.env.cr.execute(retrieve_monthly_leads_data)
        current_month_leads = self.env.cr.dictfetchall()
        list_id=[]
        product_list=[]
        for rec in current_month_leads:
            id = rec['id']
            list_id.append(id)
            product_list.append(rec['product_name'])
        print"iddddididi",list_id
        ids = str(tuple(list_id))
        leads_data_month.append(product_list)
        # monthly_leads_1="""select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;"""%(
        #     month12,month11,ids)
        # print"varrrrrrrrrrrrr",monthly_leads_1
        # self.env.cr.execute(monthly_leads_1)
        # leads_data_1 = self.env.cr.dictfetchall()
        # for rec in leads_data_1:
        #     dict1[rec.get('product_name', False)] = rec.get('count', False)
        # var = {"month": month_name12}
        # dict1['month'] = var.get('month', False)
        # leads_data_month.append(dict1)
        # print"diccttttt1", dict1
        #
        # monthly_leads_2 = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead' AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;""" % (
        #     month11, month10,ids)
        # print"varrrrrrrrrrrrr", monthly_leads_2
        # self.env.cr.execute(monthly_leads_2)
        # leads_data_2 = self.env.cr.dictfetchall()
        # for rec in leads_data_2:
        #     dict2[rec.get('product_name', False)] = rec.get('count', False)
        # var = {"month": month_name11}
        # dict2['month'] = var.get('month', False)
        # leads_data_month.append(dict2)
        # print"dict2", dict2
        #
        # monthly_leads_3 = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;""" % (
        #     month10, month9,ids)
        # print"varrrrrrrrrrrrr", monthly_leads_3
        # self.env.cr.execute(monthly_leads_3)
        # leads_data_3 = self.env.cr.dictfetchall()
        # for rec in leads_data_3:
        #     dict3[rec.get('product_name', False)] = rec.get('count', False)
        # var = {"month": month_name10}
        # dict3['month'] = var.get('month', False)
        # leads_data_month.append(dict3)
        # print"dict3", dict3
        #
        # monthly_leads_4 = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;""" % (
        #     month9, month8, ids)
        # print"varrrrrrrrrrrrr", monthly_leads_4
        # self.env.cr.execute(monthly_leads_4)
        # leads_data_4 = self.env.cr.dictfetchall()
        # for rec in leads_data_4:
        #     dict4[rec.get('product_name', False)] = rec.get('count', False)
        # var = {"month": month_name9}
        # dict4['month'] = var.get('month', False)
        # leads_data_month.append(dict4)
        # print"dict4", dict4
        #
        # monthly_leads_5 = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;""" % (
        #     month8, month7,ids)
        # print"varrrrrrrrrrrrr", monthly_leads_5
        # self.env.cr.execute(monthly_leads_5)
        # leads_data_5 = self.env.cr.dictfetchall()
        # for rec in leads_data_5:
        #     dict5[rec.get('product_name', False)] = rec.get('count', False)
        # var = {"month": month_name8}
        # dict5['month'] = var.get('month', False)
        # leads_data_month.append(dict5)
        # print"dict5", dict5
        #
        # monthly_leads_6 = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;""" % (
        #     month7, month6,ids)
        # print"varrrrrrrrrrrrr", monthly_leads_6
        # self.env.cr.execute(monthly_leads_6)
        # leads_data_6 = self.env.cr.dictfetchall()
        # for rec in leads_data_6:
        #     dict6[rec.get('product_name', False)] = rec.get('count', False)
        # var = {"month": month_name7}
        # dict6['month'] = var.get('month', False)
        # leads_data_month.append(dict6)
        # print"dict6", dict6

        monthly_leads_7 = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;""" % (
            month6, month5,ids)
        print"varrrrrrrrrrrrr", monthly_leads_7
        self.env.cr.execute(monthly_leads_7)
        leads_data_7 = self.env.cr.dictfetchall()
        for rec in leads_data_7:
            dict7[rec.get('product_name', False)] = rec.get('count', False)
        var = {"month": month_name6}
        dict7['month'] = var.get('month', False)
        leads_data_month.append(dict7)
        print"dict7", dict7

        monthly_leads_8 = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;""" % (
            month5, month4,ids)
        print"varrrrrrrrrrrrr", monthly_leads_8
        self.env.cr.execute(monthly_leads_8)
        leads_data_8 = self.env.cr.dictfetchall()
        for rec in leads_data_8:
            dict8[rec.get('product_name', False)] = rec.get('count', False)
        var = {"month": month_name5}
        dict8['month'] = var.get('month', False)
        leads_data_month.append(dict8)
        print"dict8", dict8

        monthly_leads_9 = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;""" % (
            month4, month3, ids)
        print"varrrrrrrrrrrrr", monthly_leads_9
        self.env.cr.execute(monthly_leads_9)
        leads_data_9 = self.env.cr.dictfetchall()
        for rec in leads_data_9:
            dict9[rec.get('product_name', False)] = rec.get('count', False)
        var = {"month": month_name4}
        dict9['month'] = var.get('month', False)
        leads_data_month.append(dict9)
        print"dict9", dict9

        monthly_leads_10 = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;""" % (
            month3, month2,ids)
        print"varrrrrrrrrrrrr", monthly_leads_10
        self.env.cr.execute(monthly_leads_10)
        leads_data_10 = self.env.cr.dictfetchall()
        for rec in leads_data_10:
            dict10[rec.get('product_name', False)] = rec.get('count', False)
        var = {"month": month_name3}
        dict10['month'] = var.get('month', False)
        leads_data_month.append(dict10)
        print"diccttttt10", dict10

        monthly_leads_11 = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;""" % (
            month2, month1,ids)
        print"varrrrrrrrrrrrr", monthly_leads_11
        self.env.cr.execute(monthly_leads_11)
        leads_data_11 = self.env.cr.dictfetchall()
        for rec in leads_data_11:
            dict11[rec.get('product_name', False)] = rec.get('count', False)
        var = {"month": month_name2}
        dict11['month'] = var.get('month', False)
        leads_data_month.append(dict11)
        print"diccttttt11", dict11

        monthly_leads_12 = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead'AND c.create_date>='%s' AND c.create_date<='%s' AND p.id IN %s group by p.product_name,p.id ORDER BY count ;""" % (
            month1, current_date,ids)
        print"varrrrrrrrrrrrr", monthly_leads_12
        self.env.cr.execute(monthly_leads_12)
        leads_data_12 = self.env.cr.dictfetchall()
        for rec in leads_data_12:
            dict12[rec.get('product_name', False)] = rec.get('count', False)
        var = {"month": month_name1}
        dict12['month'] = var.get('month', False)
        leads_data_month.append(dict12)
        print"diccttttt12", dict12

        if len(leads_data_month) == 0:
            return 'None'
        else:
            print"month dattattttaaa", leads_data_month
            return leads_data_month




    @api.model
    def retrieve_monthly_lead_product_data(self):
        today = datetime.today()
        months=today-relativedelta(months=1)
        retrieve_mon_lead_product_data="""select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead' AND c.create_date >='%s' AND c.create_date <= '%s' group by c.type,p.product_name ORDER BY count desc limit 5 ;"""%(months,today)
        self.env.cr.execute(retrieve_mon_lead_product_data)
        lead_monthly_product=self.env.cr.dictfetchall()
        if len(lead_monthly_product)== 0:
            return 'None'
        else:
            print("adasdfsfsdfdsfsd",lead_monthly_product)
            return lead_monthly_product

    @api.model
    def retrieve_monthly_lead_source_data(self):
        today = datetime.today()
        months = today - relativedelta(months=1)
        retrieve_mon_lead_source_data = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >='%s' AND create_date <='%s' group by source_of_lead ORDER BY count desc limit 5;""" % (
        months, today)
        self.env.cr.execute(retrieve_mon_lead_source_data)
        lead_monthly_source = self.env.cr.dictfetchall()
        if len(lead_monthly_source) == 0:
            return 'None'
        else:
            print("adasdfsfsdfdsfsd", lead_monthly_source)
            return lead_monthly_source

    @api.model
    def retrieve_opportunity_product_data(self):

        retrieve_opportunity_product_data = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='opportunity' group by c.type,p.product_name ORDER BY count ;"""
        self.env.cr.execute(retrieve_opportunity_product_data)
        opportunity_product = self.env.cr.dictfetchall()
        if len(opportunity_product) == 0:
            return 'None'
        else:
            print("adasdfsfsdfdsfsd", opportunity_product)
            return opportunity_product

    @api.model
    def retrieve_leads_product_data(self):

        retrieve_leads_product_data = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead' group by c.type,p.product_name ORDER BY count ;"""
        self.env.cr.execute(retrieve_leads_product_data)
        leads_product = self.env.cr.dictfetchall()
        if len(leads_product) == 0:
            return 'None'
        else:
            print("adasdfsfsdfdsfsd", leads_product)
            return leads_product

    @api.model
    def retrieve_healthy_oppo_data(self):
        current_date = datetime.now()
        last_6_month = current_date - relativedelta(months=6)
        retrieve_healthy_oppo_data = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND date_conversion>='%s' AND date_conversion<='%s' group by type,stage_id_name ORDER by count;"""%(last_6_month,current_date)
        self.env.cr.execute(retrieve_healthy_oppo_data)
        healthy_opportunity = self.env.cr.dictfetchall()
        if len(healthy_opportunity) == 0:
            return 'None'
        else:
            print("adasdfsfsdfdsfsd", healthy_opportunity)
            return healthy_opportunity

    @api.model
    def retrieve_current_month_leads_data(self):
        current_date=datetime.now()
        last_month=current_date - relativedelta(months=1)


        retrieve_current_month_leads_data = """select p.product_name,count(c.id) from crm_lead c join product_detail p on c.product_id = p.id where type='lead' AND c.create_date >='%s' AND c.create_date <='%s' group by p.product_name ORDER BY count desc limit 3 ;"""%(last_month,current_date)
        self.env.cr.execute(retrieve_current_month_leads_data)
        current_month_data = self.env.cr.dictfetchall()
        count=0
        for item in current_month_data:
            if count==0:
                item.update({"color": "#FF0F00"})
            if count==1:
                item.update({"color": "#F8FF01"})
            if count==2:
                item.update({"color": "#0D52D1"})
            count= count + 1
            if count==3:
                break


        if len(current_month_data) == 0:
            return 'None'
        else:
            print("adasdfsfsdfdsfsd", current_month_data)
            return current_month_data

    @api.model
    def retrieve_current_month_source_data(self):
        current_date = datetime.now()
        last_month = current_date - relativedelta(months=1)

        retrieve_current_month_source_data = """select source_of_lead,count(*) from crm_lead where type='lead' AND create_date >='%s' AND create_date <='%s' group by source_of_lead ORDER BY count desc limit 3;"""%(last_month,current_date)
        self.env.cr.execute(retrieve_current_month_source_data)
        current_month_source_data = self.env.cr.dictfetchall()
        count = 0
        for item in current_month_source_data:
            if count == 0:
                item.update({"color": "#FF0F00"})
            if count == 1:
                item.update({"color": "#F8FF01"})
            if count == 2:
                item.update({"color": "#0D52D1"})
            count = count + 1
            if count == 3:
                break

        if len(current_month_source_data) == 0:
            return 'None'
        else:
            print("adasdfsfsdfdsfsd", current_month_source_data)
            return current_month_source_data

    @api.model
    def retrieve_current_health_opportunity_data(self):
        current_date = datetime.now()
        last_month = current_date - relativedelta(months=1)


        retrieve_current_health_opportunity_data = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND date_conversion >='%s' AND date_conversion<='%s' group by type,stage_id_name ORDER by count;"""%(last_month,current_date)
        self.env.cr.execute(retrieve_current_health_opportunity_data)
        current_health_oppo_data = self.env.cr.dictfetchall()
        count = 0
        for item in current_health_oppo_data:
            if count == 0:
                item.update({"color": "#FF0F00"})
            if count == 1:
                item.update({"color": "#F8FF01"})
            if count == 2:
                item.update({"color": "#0D52D1"})
            if count == 3:
                item.update({"color": "#696969"})
            if count == 4:
                item.update({"color": "#B22222"})
            if count == 5:
                item.update({"color": "#6495ED"})
            count = count + 1
            if count == 6:
                break

        if len(current_health_oppo_data) == 0:
            return 'None'
        else:
            print("adasdfsfsdfdsfsd", current_health_oppo_data)
            return current_health_oppo_data

    @api.model
    def retrieve_total_sales_per_months(self):
        month_1 = {}
        month_2 = {}
        month_3 = {}
        month_4 = {}
        month_5 = {}
        month_6 = {}
        total_sales_months = []
        current_date = datetime.now()
        month1 = current_date - relativedelta(months=1)
        month_name1 = month1.strftime("%b")
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

        retrieve_total_sales_per_months1 = """ select stage_id_name,count(id) from crm_lead where type='opportunity' AND stage_id_name='Won' AND date_conversion <= '%s'  AND date_conversion >= '%s'group by type,stage_id_name ORDER by count;""" % (
        month5, month6)
        print("rettrerjrfoeroeroereor", retrieve_total_sales_per_months1)
        self.env.cr.execute(retrieve_total_sales_per_months1)
        total_sales1 = self._cr.dictfetchall()
        print("total_sales1", total_sales1)
        for rec in total_sales1:
            month_1[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name6}
        month_1['month'] = var.get('month', False)
        total_sales_months.append(month_1)

        print"diccttttt", total_sales_months

        retrieve_total_sales_per_months2 = """ select stage_id_name,count(id) from crm_lead where type='opportunity' AND stage_id_name='Won' AND date_conversion <= '%s'  AND date_conversion >= '%s'group by type,stage_id_name ORDER by count;""" % (
        month4, month5)
        print("retrieve_total_sales_per_months2", retrieve_total_sales_per_months2)
        self.env.cr.execute(retrieve_total_sales_per_months2)
        total_sales2 = self._cr.dictfetchall()
        for rec in total_sales2:
            month_2[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name5}
        month_2['month'] = var.get('month', False)
        total_sales_months.append(month_2)
        print"diccttttt", total_sales_months

        retrieve_total_sales_per_months3 = """ select stage_id_name,count(id) from crm_lead where type='opportunity' AND stage_id_name='Won' AND date_conversion <= '%s'  AND date_conversion >= '%s'group by type,stage_id_name ORDER by count;""" % (
        month3, month4)
        print("retrieve_total_sales_per_months3", retrieve_total_sales_per_months3)
        self.env.cr.execute(retrieve_total_sales_per_months3)
        total_sales3 = self._cr.dictfetchall()
        for rec in total_sales3:
            month_3[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name4}
        month_3['month'] = var.get('month', False)
        total_sales_months.append(month_3)
        print"diccttttt", total_sales_months

        retrieve_total_sales_per_months4 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND stage_id_name='Won' AND date_conversion <= '%s'  AND date_conversion >= '%s'group by type,stage_id_name ORDER by count;""" % (
            month2, month3)
        print("retrieve_total_sales_per_months4", retrieve_total_sales_per_months4)
        self.env.cr.execute(retrieve_total_sales_per_months4)
        total_sales4 = self._cr.dictfetchall()
        for rec in total_sales4:
            month_4[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name3}
        month_4['month'] = var.get('month', False)
        total_sales_months.append(month_4)
        print"diccttttt", total_sales_months

        retrieve_total_sales_per_months5 = """select stage_id_name,count(id) from crm_lead where type='opportunity' AND stage_id_name='Won' AND date_conversion <= '%s'  AND date_conversion >= '%s'group by type,stage_id_name ORDER by count;""" % (
            month1, month2)
        print("retrieve_total_sales_per_months5", retrieve_total_sales_per_months5)
        self.env.cr.execute(retrieve_total_sales_per_months5)
        total_sales5 = self._cr.dictfetchall()
        for rec in total_sales5:
            month_5[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name2}
        month_5['month'] = var.get('month', False)
        total_sales_months.append(month_5)
        print"diccttttt", total_sales_months

        retrieve_total_sales_per_months6 = """ select stage_id_name,count(id) from crm_lead where type='opportunity' AND stage_id_name='Won' AND date_conversion <= '%s'  AND date_conversion >= '%s'group by type,stage_id_name ORDER by count;""" % (
            current_date, month1)
        print("health_opportunity_month1", retrieve_total_sales_per_months6)
        self.env.cr.execute(retrieve_total_sales_per_months6)
        total_sales6 = self._cr.dictfetchall()
        for rec in total_sales6:
            month_6[rec.get('stage_id_name', False)] = rec.get('count', False)
        var = {"month": month_name1}
        month_6['month'] = var.get('month', False)
        total_sales_months.append(month_6)
        print"diccttttt", month_6

        if len(total_sales_months) == 0:
            return 'None'
        else:
            print "total_sales_months", total_sales_months

            return total_sales_months

