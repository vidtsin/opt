from odoo import api, fields, models



class Hst_Payroll_Settings(models.Model):
    _name='new.filing.settings'



    hst_filing_monthly=fields.Integer('Hst Filing Monthly')
    hst_filing_quarterly=fields.Integer('Hst Filing Quarterly')
    hst_filing_annually=fields.Integer('Hst Filing Annually ')
    payroll_filing_monthly=fields.Integer('Payroll Filing Monthly')
    payroll_filing_quarterly=fields.Integer('Payroll Filing Quarterly')
    payroll_filing_annually=fields.Integer("Payroll Filing Annually")