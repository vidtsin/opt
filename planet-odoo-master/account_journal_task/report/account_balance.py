# -*- coding: utf-8 -*-

import time
from odoo import api, models, fields


class ReportTrialBalanceCustom(models.AbstractModel):
    _inherit = 'report.account.report_trialbalance'

    invoice_id = fields.Many2one('account.invoice.line', string='Invoice Reference',
    ondelete='cascade', index=True)

    department_id = fields.Many2one("core.departments", related='invoice_id.department_id', string="Departments")
    cost_center_id = fields.Many2one("core.cost.center", related='invoice_id.cost_center_id', string="Cost Center")
    sections_id = fields.Many2one("core.sections", related='invoice_id.sections_id', string="Sections")

    def _get_accounts(self, accounts, display_account):
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
                `department`: Account Department,
                `cost_center_id`: Account cost center,
                `sections_id`: Account Sections,
        """

        account_result = {}
        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = self.env['account.move.line']._query_get()
        tables = tables.replace('"','')
        if not tables:
            tables = 'account_move_line'
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        # compute the balance, debit and credit for the provided accounts
        request = ("SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" +\
                   " FROM " + tables + " WHERE account_id IN %s " + filters + " GROUP BY account_id")
        params = (tuple(accounts.ids),) + tuple(where_params)
        self.env.cr.execute(request, params)
        for row in self.env.cr.dictfetchall():
            account_result[row.pop('id')] = row

        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            
            res['code'] = account.code
            res['name'] = account.name
            res['department_id'] = account.department_id
            res['cost_center_id'] = account.cost_center_id
            res['sections_id'] = account.sections_id
            if account.id in account_result.keys():
                res['debit'] = account_result[account.id].get('debit')
                res['credit'] = account_result[account.id].get('credit')
                res['balance'] = account_result[account.id].get('balance')
            
            if display_account == 'all':
                account_res.append(res)
            if display_account in ['movement', 'not_zero'] and not currency.is_zero(res['balance']):
                account_res.append(res)
        return account_res

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        display_account = data['form'].get('display_account')
        accounts = docs if self.model == 'account.account' else self.env['account.account'].search([])
        account_res = self.with_context(data['form'].get('used_context'))._get_accounts(accounts, display_account)

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': account_res,
        }
        return self.env['report'].render('account.report_trialbalance', docargs)
    
    
class InvoiceLineTrial(models.Model):
    _inherit = "account.account"
      
    invoice_id = fields.Many2one('account.bank.statement.line', string='Invoice Reference',
    ondelete='cascade', index=True)
      
    department_id = fields.Many2one("core.departments", related='invoice_id.department_id', string="Departments")
    cost_center_id = fields.Many2one("core.cost.center", related='invoice_id.cost_center_id', string="Cost Center")
    sections_id = fields.Many2one("core.sections", related='invoice_id.sections_id', string="Sections")


