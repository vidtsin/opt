from odoo import models, fields, api,_
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero



class hr_payslip(models.Model):
    _inherit = "hr.payslip"

    total_timesheet_hours = fields.Float('Total Timesheet Hours')
    overtime_hours = fields.Float('Overtime Hours')
    total_hours = fields.Float('Total Hours')
    new_line_ids = fields.One2many('new.hr.payslip.line', 'new_slip_id', string='Payslip Lines', readonly=True,
                               states={'draft': [('readonly', False)]})




    @api.multi
    def compute_sheet(self):
        for payslip in self:
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            # delete old payslip lines
            payslip.line_ids.unlink()
            # set the list of contract for which the rules have to be applied
            # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
            contract_ids = payslip.contract_id.ids or \
                           self.get_contract(payslip.employee_id, payslip.date_from, payslip.date_to)
            lines = [(0, 0, line) for line in self.get_payslip_lines(contract_ids, payslip.id)]

            payslip.write({'line_ids': lines, 'number': number})
            if not payslip.new_line_ids:
                for pl in payslip.line_ids:

                    if pl.category_id.name == 'Company Contribution' or pl.category_id.name == 'Deduction':

                        self.env['new.hr.payslip.line'].create({
                            'new_slip_id':payslip.id,
                            'rate':pl.rate,
                            'amount':pl.amount,
                            'quantity':pl.quantity,
                            'total':pl.total,
                            'name':pl.name,
                            'code':pl.code,
                            'category_id':pl.category_id.id,
                            'salary_rule_id':pl.salary_rule_id.id
                        })
                        if pl.category_id.name == 'Company Contribution':
                            pl.unlink()
            else:
                for pl in payslip.line_ids:
                    if pl.category_id.name == 'Company Contribution':
                        pl.unlink()
        return True

    #     function will check the detail of employee  credit,debit and create credit,debit,line ids while salary slip sholud be on done .
    # create employee payslip in employee payslips .
    @api.multi
    def action_payslip_done(self):
        result = super(hr_payslip, self).action_payslip_done()
        precision = self.env['decimal.precision'].precision_get('Payroll')
        for slip in self:

            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            date = slip.date or slip.date_to

            name = _('Payslip of %s') % (slip.employee_id.name)
            move_dict = {
                'narration': name,
                'ref': slip.number,
                'journal_id': slip.journal_id.id,
                'date': date,
            }
            for line in slip.new_line_ids:
                amount = slip.credit_note and -line.total or line.total
                if float_is_zero(amount, precision_digits=precision):
                    continue
                debit_account_id = line.salary_rule_id.account_debit.id
                credit_account_id = line.salary_rule_id.account_credit.id

                if debit_account_id:
                    debit_line = (0, 0, {
                        'name': line.name,
                        'partner_id': line._get_partner_id(credit_account=False),
                        'account_id': debit_account_id,
                        'journal_id': slip.journal_id.id,
                        'date': date,
                        'debit': amount > 0.0 and amount or 0.0,
                        'credit': amount < 0.0 and -amount or 0.0,
                        'analytic_account_id': line.salary_rule_id.analytic_account_id.id,
                        'tax_line_id': line.salary_rule_id.account_tax_id.id,
                    })
                    line_ids.append(debit_line)
                    debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']

                if credit_account_id:
                    credit_line = (0, 0, {
                        'name': line.name,
                        'partner_id': line._get_partner_id(credit_account=True),
                        'account_id': credit_account_id,
                        'journal_id': slip.journal_id.id,
                        'date': date,
                        'debit': amount < 0.0 and -amount or 0.0,
                        'credit': amount > 0.0 and amount or 0.0,
                        'analytic_account_id': line.salary_rule_id.analytic_account_id.id,
                        'tax_line_id': line.salary_rule_id.account_tax_id.id,
                    })
                    line_ids.append(credit_line)
                    credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

            if float_compare(credit_sum, debit_sum, precision_digits=precision) == -1:
                acc_id = slip.journal_id.default_credit_account_id.id
                if not acc_id:
                    raise UserError(_('The Expense Journal "%s" has not properly configured the Credit Account!') % (
                    slip.journal_id.name))
                adjust_credit = (0, 0, {
                    'name': _('Adjustment Entry'),
                    'partner_id': False,
                    'account_id': acc_id,
                    'journal_id': slip.journal_id.id,
                    'date': date,
                    'debit': 0.0,
                    'credit': debit_sum - credit_sum,
                })
                line_ids.append(adjust_credit)

            elif float_compare(debit_sum, credit_sum, precision_digits=precision) == -1:
                acc_id = slip.journal_id.default_debit_account_id.id
                if not acc_id:
                    raise UserError(_('The Expense Journal "%s" has not properly configured the Debit Account!') % (
                    slip.journal_id.name))
                adjust_debit = (0, 0, {
                    'name': _('Adjustment Entry'),
                    'partner_id': False,
                    'account_id': acc_id,
                    'journal_id': slip.journal_id.id,
                    'date': date,
                    'debit': credit_sum - debit_sum,
                    'credit': 0.0,
                })
                line_ids.append(adjust_debit)
            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)
            move.post()
        return True



class hr_payslip_line(models.Model):
    _inherit = "hr.payslip.line"

    is_comp_con = fields.Boolean('Company Contribution')

#
class new_hr_payslip(models.Model):
    _name='new.hr.payslip.line'


    salary_rule_id = fields.Many2one('hr.salary.rule', string='Rule')
    category_id = fields.Many2one('hr.salary.rule.category', string='Category', required=True)
    rate = fields.Float(string='Rate (%)', digits=dp.get_precision('Payroll Rate'), default=100.0)
    amount = fields.Float(digits=dp.get_precision('Payroll'))
    quantity = fields.Float(digits=dp.get_precision('Payroll'), default=1.0)
    total = fields.Float(compute='_compute_total', string='Total', digits=dp.get_precision('Payroll'), store=True)
    name = fields.Char(required=True)
    code = fields.Char(required=True,
                       help="The code of salary rules can be used as reference in computation of other rules. "
                            "In that case, it is case sensitive.")
    new_slip_id = fields.Many2one('hr.payslip', string='Pay Slip', ondelete='cascade')
    sequence = fields.Integer(required=True, index=True, default=10)


     # Get partner_id of slip line to use in account_move_line
      # use partner of salary rule or fallback on employee's address
    def _get_partner_id(self, credit_account):

        register_partner_id = self.salary_rule_id.register_id.partner_id
        partner_id = register_partner_id.id or self.new_slip_id.employee_id.address_home_id.id
        if credit_account:
            if register_partner_id or self.salary_rule_id.account_credit.internal_type in ('receivable', 'payable'):
                return partner_id
        else:
            if register_partner_id or self.salary_rule_id.account_debit.internal_type in ('receivable', 'payable'):
                return partner_id
        return False



















