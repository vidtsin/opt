
from odoo import tools
from odoo import models, fields

class DonationReport(models.Model):
    _inherit = "donation.report"

    core_sections = fields.Many2one('core.sections', string='Section')


    # sql query for donation.
    def _select(self):
        select = """
            SELECT min(l.id) AS id,
                d.donation_date AS donation_date,
                l.product_id AS product_id,
                l.in_kind AS in_kind,
                l.tax_receipt_ok AS tax_receipt_ok,
                pt.categ_id AS product_categ_id,
                d.company_id AS company_id,
                d.core_sections AS core_sections,
                d.partner_id AS partner_id,
                d.country_id AS country_id,
                d.campaign_id AS campaign_id,
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
            WHERE d.state='done' and d.admin_id=1 and d.create_uid ="""+str(self.env.uid)+"""
            """
        return where


    def _group_by(self):
        group_by = """
            GROUP BY l.product_id,
                l.in_kind,
                l.tax_receipt_ok,
                pt.categ_id,
                d.donation_date,
                d.core_sections,
                d.partner_id,
                d.country_id,
                d.campaign_id,
                d.company_id,
                d.company_currency_id,
                d.user_id
                
            """
        return group_by

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        sql = "CREATE OR REPLACE VIEW %s AS (%s FROM %s %s %s)" % (
            self._table, self._select(), self._from(),
            self._where(), self._group_by())
        self._cr.execute(sql)
