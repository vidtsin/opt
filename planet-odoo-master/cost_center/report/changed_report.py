# -*- coding: utf-8 -*-
# © 2014-2016 Barroux Abbey (http://www.barroux.org)
# © 2014-2016 Akretion France (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import tools
from odoo import models, fields, api
import unicodecsv as csv
import StringIO, datetime
from datetime import timedelta
import base64
from dateutil.relativedelta import relativedelta


class DonationReport (models.Model):
    _name = "donation.report"
    _description = "Donations Analysis"
    _auto = False
    _rec_name = 'donation_date'
    _order = "donation_date desc"

    donation_date = fields.Date (string='Donation Date', readonly=True)
    product_id = fields.Many2one (
        'product.product', string='Product', readonly=True)
    partner_id = fields.Many2one ('res.partner', string='Donor', readonly=True)
    country_id = fields.Many2one (
        'res.country', string='Partner Country', readonly=True)
    company_id = fields.Many2one (
        'res.company', string='Company', readonly=True)
    product_categ_id = fields.Many2one (
        'product.category', string='Category of Product', readonly=True)
    campaign_id = fields.Many2one (
        'donation.campaign', string='Donation Campaign', readonly=True)
    in_kind = fields.Boolean (string='In Kind')
    tax_receipt_ok = fields.Boolean (string='Eligible for a Tax Receipt')
    company_currency_id = fields.Many2one (
        'res.currency', string='Company Currency', readonly=True)
    amount_company_currency = fields.Monetary (
        'Amount', readonly=True, currency_field='company_currency_id')
    tax_receipt_amount = fields.Monetary (
        'Tax Receipt Eligible Amount', readonly=True,
        currency_field='company_currency_id')
    create_uid = fields.Many2one ('res.users', string='User', invisible=True)


    # sql query for donation details.

    def _select(self):
        select = """
            SELECT min(l.id) AS id,
                d.donation_date AS donation_date,
                l.product_id AS product_id,
                l.in_kind AS in_kind,
                l.tax_receipt_ok AS tax_receipt_ok,
                pt.categ_id AS product_categ_id,
                d.company_id AS company_id,
                d.partner_id AS partner_id,
                d.country_id AS country_id,
                d.campaign_id AS campaign_id,
                d.create_uid AS create_uid,
                d.company_currency_id AS company_currency_id,
                sum(l.amount_company_currency) AS amount_company_currency,
                sum(l.tax_receipt_amount) AS tax_receipt_amount
                """
        return select

    def _from(self):
        from_sql = """
            donation_line l
                LEFT JOIN donation_donation d ON (d.id=l.donation_id)
                LEFT JOIN product_product pp ON (l.product_id=pp.id)
                LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
            """
        return from_sql

    def _where(self):
        where = """
            WHERE d.state='done'
            """
        return where

    def _group_by(self):
        group_by = """
            GROUP BY l.product_id,
                l.in_kind,
                l.tax_receipt_ok,
                pt.categ_id,
                d.donation_date,
                d.partner_id,
                d.country_id,
                d.campaign_id,
                d.company_id,
                d.company_currency_id,
                d.create_uid
            """
        return group_by

    def init(self):
        tools.drop_view_if_exists (self._cr, self._table)
        sql = "CREATE OR REPLACE VIEW %s AS (%s FROM %s %s %s)" % (
            self._table, self._select (), self._from (),
            self._where (), self._group_by ())
        self._cr.execute (sql)


class Donation_Csv_Report (models.TransientModel):
    _name = "donation.csv.report"

    Header = ['Donation Number', 'Donor', 'Donation Date', 'Donation Amount', 'Payment Method', 'Payment Reference',
              'Section']
    createdfilename = fields.Char ()
    createdfile = fields.Binary ('File', readonly=True)
    state = fields.Selection ([('new', "New"), ('created', "Created")], default='new', string="Status")
    start_date = fields.Date ('Start Date')

    def _select(self):

        select = """
                select dl.product_id,dl.amount,dd.donation_date from donation_line dl left join donation_donation dd on (dl.donation_id = dd.id)  where donation_id in (select id from donation_donation where 
                donation_date >= '%s' and create_uid = %s) 
                """ % (self.start_date, self.env.uid)
        return select

    def diff_month(self, d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month


    # to generate csv report  for donation.
    @api.multi
    def generate_donation_report_csv(self):
        prod_obj = self.env['product.product']
        csvfile = StringIO.StringIO ()
        w = csv.writer (csvfile)
        donation_id = self.env['donation.donation'].search ([('create_uid', '=', self._uid)])
        if donation_id:
            section = donation_id.core_sections.name

        currentdate = datetime.datetime.now ()
        start_date = datetime.datetime.strptime (self.start_date, '%Y-%m-%d')
        viewname = "donation_report_view_" + str (currentdate.strftime ('%Y_%m_%d_%H_%M')) + "_" + str (self._uid)
        sql = "CREATE OR REPLACE VIEW %s AS (%s)" % (viewname, self._select ())
        self._cr.execute (sql)
        self._cr.commit ()
        product_sql = 'select distinct dr.product_id,pt.name from %s dr left join product_template pt on dr.product_id = pt.id order by product_id asc' % (
            viewname)
        self._cr.execute (product_sql)
        product_ids = self._cr.dictfetchall ()
        if product_ids:
            modified_row = []
            modified_row.append ('')
            product_ids_list = []
            for prod in product_ids:
                modified_row.append (prod['name'])
                product_ids_list.append (prod['product_id'])
            w.writerow (modified_row)
            modified_row = []
            modified_row.append ('')
            for prod in product_ids:
                modified_row.append ('Amount')
            modified_row.append ('Amount')
            w.writerow (modified_row)
            total = 0
            product_total_header = 'select sum(amount) from %s group by product_id order by product_id asc' % (viewname)
            self._cr.execute (product_total_header)
            total_header = self._cr.fetchall ()
            total_header = list (sum (total_header, ()))
            modified_row = []
            modified_row.append ('Total')
            for prod_total in total_header:
                modified_row.append (prod_total)
                total += prod_total
            modified_row.append (total)
            w.writerow (modified_row)
            iterations = currentdate.date () - start_date.date ()
            iterations = self.diff_month (currentdate.date (), start_date.date ())
            iterations += 1
            test_no = 0
            for iteration in range (0, iterations):
                if len (product_ids_list) == 1:
                    month_wise_total_sql = 'select distinct product_id,sum(amount) as amount from %s' \
                                           ' where product_id = %s and EXTRACT(MONTH FROM donation_date)= %s and EXTRACT(YEAR FROM donation_date)=%s group by product_id order by product_id asc' % (
                                               viewname, product_ids_list[0], start_date.month, start_date.year)
                else:
                    month_wise_total_sql = 'select distinct product_id,sum(amount) as amount from %s' \
                                           ' where product_id in %s and EXTRACT(MONTH FROM donation_date)= %s and EXTRACT(YEAR FROM donation_date)=%s group by product_id order by product_id asc' % (
                                               viewname, tuple (product_ids_list), start_date.month, start_date.year)
                self._cr.execute (month_wise_total_sql)
                month_wise_total = self._cr.dictfetchall ()
                month_total = 0
                modified_row = []
                modified_row.append (start_date.strftime ("%B") + " " + str (start_date.year))
                if len (month_wise_total) > 0:
                    for rec in product_ids:
                        if month_wise_total:
                            if rec['product_id'] == month_wise_total[0]['product_id']:
                                modified_row.append (month_wise_total[0]['amount'])
                                month_total += month_wise_total[0]['amount']
                                month_wise_total.pop (0)
                            else:
                                modified_row.append ('')
                        else:
                            modified_row.append ('')
                    modified_row.append (month_total)
                    w.writerow (modified_row)
                start_date += relativedelta (months=1)
            csv_value = csvfile.getvalue ()
            csvfile.close ()
            dropquery = 'drop view %s' % (viewname)
            self._cr.execute (dropquery)
            self._cr.commit ()
            self.createdfilename = str (datetime.date.today ().strftime ('%Y.%d.%m')) + '_Donation_Report.csv'
            self.createdfile = base64.encodestring (csv_value)
            self.state = 'created'
        return {
            "type": "ir.actions.do_nothing",
        }


