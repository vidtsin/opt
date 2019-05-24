from odoo import fields,models,api,_
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare
from datetime import date
from odoo import api, SUPERUSER_ID
import base64
import calendar
from datetime import *
from dateutil.relativedelta import relativedelta




class product_template(models.Model):
    _inherit = 'product.template'

    cost_core = fields.Many2one('core.cost.center',string="Cost Center")
    core_dept = fields.Many2one('core.departments',string='Department')

class product_product(models.Model):
    _inherit = 'product.product'

    cost_core = fields.Many2one('core.cost.center',related='product_tmpl_id.cost_core',string="Cost Center")
    core_dept = fields.Many2one('core.departments',related='product_tmpl_id.core_dept',string='Department')

class donation_line(models.Model):
    _inherit = 'donation.line'

    cost_core = fields.Many2one('core.cost.center',related='product_id.cost_core', string="Cost Center")
    core_dept = fields.Many2one('core.departments',related='product_id.core_dept', string='Department')

class donation_donation(models.Model):
    _inherit = 'donation.donation'

    core_sections = fields.Many2one('core.sections',string='Section')
    user_id = fields.Many2one('res.users',string='Related User')
    admin_id = fields.Many2one('res.users',string='Admin User')
    donation_created = fields.Boolean(string ='Donation Created')
    end_date = fields.Date(
        string='End Date', required=True,
        states={'done': [('readonly', True)]}, index=True,
        track_visibility='onchange')
    cancel_recurring = fields.Boolean("Cancel Recurring")

    # function will check on validation button in recurring donation if in payment method if default credit,debit is false it will raise
    #   create move line in donation
    @api.multi
    def _prepare_donation_move(self):
        self.ensure_one ()
        if not self.journal_id.default_debit_account_id:
            raise UserError (
                _ ("Missing Default Debit Account on journal '%s'.")
                % self.journal_id.name)
        movelines = []
        if self.company_id.currency_id.id != self.currency_id.id:
            currency_id = self.currency_id.id
        else:
            currency_id = False
        # Note : we can have negative donations for donors that use direct
        # debit when their direct debit rejected by the bank
        amount_total_company_cur = 0.0
        total_amount_currency = 0.0
        name = self._prepare_move_line_name ()
        aml = {}
        precision = self.env['decimal.precision'].precision_get ('Account')
        cost_center = False
        core_dept = False
        for donation_line in self.line_ids:
            if donation_line.in_kind:
                continue
            amount_total_company_cur += donation_line.amount_company_currency
            account_id = donation_line.product_id.property_account_income_id.id
            cost_center = donation_line.cost_core.id or False
            core_dept = donation_line.core_dept.id or False
            if not account_id:
                account_id = donation_line.product_id.categ_id. \
                    property_account_income_categ_id.id
            if not account_id:
                raise UserError (
                    _ ("Missing income account on product '%s' or on it's "
                       "related product category")
                    % donation_line.product_id.name)
            analytic_account_id = donation_line.get_analytic_account_id ()
            amount_currency = 0.0
            if float_compare (
                    donation_line.amount_company_currency, 0,
                    precision_digits=precision) == 1:
                credit = donation_line.amount_company_currency
                debit = 0
                amount_currency = donation_line.amount * -1
            else:
                debit = donation_line.amount_company_currency * -1
                credit = 0
                amount_currency = donation_line.amount

            # TODO Take into account the option group_invoice_lines ?
            if (account_id, analytic_account_id) in aml:
                aml[(account_id, analytic_account_id)]['credit'] += credit
                aml[(account_id, analytic_account_id)]['debit'] += debit
                aml[(account_id, analytic_account_id)]['amount_currency'] \
                    += amount_currency
            else:
                aml[(account_id, analytic_account_id)] = {
                    'credit': credit,
                    'debit': debit,
                    'amount_currency': amount_currency,
                }
        if not aml:  # for full in-kind donation
            return False

        for (account_id, analytic_account_id), content in aml.iteritems ():
            movelines.append ((0, 0, {
                'name': name,
                'credit': content['credit'],
                'debit': content['debit'],
                'account_id': account_id,
                'cost_center_id':cost_center,
                'department_id':core_dept,
                'analytic_account_id': analytic_account_id,
                'partner_id': self.commercial_partner_id.id,
                'sections_id': self.core_sections.id,
                'currency_id': currency_id,
                'amount_currency': (
                        currency_id and content['amount_currency'] or 0.0),
            }))
        # counter-part

        ml_core_vals= self._prepare_counterpart_move_line_core(name, amount_total_company_cur,
                                                               total_amount_currency,core_dept,cost_center,currency_id)

        # movelines.append((0, 0, ml_vals))
        movelines.append((0, 0, ml_core_vals))

        vals = {
            'journal_id': self.journal_id.id,
            'date': self.donation_date,

            'ref': self.payment_ref,
            'line_ids': movelines,
        }
        return vals

    # this function work on validate will count, compare amount total ,credit,debit check the value and create donation
    @api.multi
    def _prepare_counterpart_move_line_core(self, name, amount_total_company_cur, total_amount_currency,
                                            core_dept,cost_center,currency_id):
        self.ensure_one ()
        precision = self.env['decimal.precision'].precision_get ('Account')
        if float_compare (
                amount_total_company_cur, 0, precision_digits=precision) == 1:
            debit = amount_total_company_cur
            credit = 0
            total_amount_currency = self.amount_total
        else:
            credit = amount_total_company_cur * -1
            debit = 0
            total_amount_currency = self.amount_total * -1
        vals = {
            'debit': debit,
            'credit': credit,
            'name': name,
            'account_id': self.journal_id.default_debit_account_id.id,
            'cost_center_id': cost_center,
            'department_id': core_dept,
            'sections_id': self.core_sections.id,
            'partner_id': self.commercial_partner_id.id,
            'currency_id': currency_id,
            'amount_currency': (
                    currency_id and total_amount_currency or 0.0),
        }
        return vals


    # this function will create attachement it will check all the condition  and create donation will be goes to done state
    #   it will check start date and end date based on that it will create tht much donation aftr which are done it will show in history
    @api.multi
    def validate(self):
        ir_attachment_obj = self.env['ir.attachment']

        result = self.env['report'].sudo().get_pdf ([self.id], 'cost_center.report_donation_print_save')
        result = base64.b64encode(result)

        check_total = self.env['res.users'].has_group (
            'donation.group_donation_check_total')
        for donation in self:
            if not donation.line_ids:
                raise UserError (_ (
                    "Cannot validate the donation of %s because it doesn't "
                    "have any lines!") % donation.partner_id.name)

            if float_is_zero (
                    donation.amount_total,
                    precision_rounding=donation.currency_id.rounding):
                raise UserError (_ (
                    "Cannot validate the donation of %s because the "
                    "total amount is 0 !") % donation.partner_id.name)

            if donation.state != 'draft':
                raise UserError (_ (
                    "Cannot validate the donation of %s because it is not "
                    "in draft state.") % donation.partner_id.name)

            # if check_total and float_compare (
            #         donation.check_total, donation.amount_total,
            #         precision_rounding=donation.currency_id.rounding):
            #     raise UserError (_ (
            #         "The amount of the donation of %s (%s) is different "
            #         "from the sum of the donation lines (%s).") % (
            #                          donation.partner_id.name, donation.check_total,
            #                          donation.amount_total))

            vals = {'state': 'done'}

            if not float_is_zero (
                    donation.amount_total,
                    precision_rounding=donation.currency_id.rounding):
                move_vals = donation._prepare_donation_move()
                # when we have a full in-kind donation: no account move
                if move_vals:
                    move = self.env['account.move'].create(move_vals)
                    move.post()
                    vals['move_id'] = move.id
                else:
                    donation.message_post (_ (
                        'Full in-kind donation: no account move generated'))

            receipt = donation.generate_each_tax_receipt()
            if receipt:
                vals['tax_receipt_id'] = receipt.id

            donation.write(vals)
            self._cr.commit()

            attachment_vals = {
                'datas': result,
                'res_id': self.id,
                'res_model': 'donation.donation',
                'type': 'binary',
            }
            if self.number:
                attachment_vals.update({
                    'name': 'Donation ' + self.number.replace('/','-') + '.pdf',
                    'datas_fname': 'Donation ' + self.number.replace('/','-') + '.pdf',
                })

            else:

                attachment_vals.update ({
                    'name': 'Donation of  ' + self.partner_id.name + '.pdf',
                    'datas_fname': 'Donation of ' + self.partner_id.name + '.pdf',
                })

            ir_attachment_obj.create(attachment_vals)
            if not donation.donation_created:
                if donation.donation_date and donation.end_date:
                    date1 = datetime.strptime(donation.donation_date, "%Y-%m-%d")
                    date2 = datetime.strptime(donation.end_date, "%Y-%m-%d")
                    r = relativedelta(date2, date1)
                    r.months
                    count = 1
                    while count <= r.months:
                        date = datetime.now() + relativedelta(months=+count)
                        op = datetime.strftime(date, "%m-%d-%Y")


                        list = []
                        vals1 = {}
                        for line in donation.line_ids:
                            vals1 = {'product_id': line.product_id.id, 'quantity': line.quantity,
                                     'unit_price': line.unit_price,
                                      'amount': line.amount}
                            list.append((0, 0, vals1))

                        vals = {'partner_id': donation.partner_id.id, 'journal_id': donation.journal_id.id,
                                'donation_date': op, 'payment_ref': donation.payment_ref,
                                'end_date': donation.end_date, 'donation_created': True, 'recurring_template': False, 'line_ids': list
                                }

                        donation_id = self.env['donation.donation'].create(vals)
                        count = count + 1

            if donation.state=='done':
                parent_rec = self.env['donation.donation'].search(
                    [('partner_id', '=', self.partner_id.id), ('recurring_template', '!=', False),
                     ('state', '=', 'done'),('cancel_recurring','=', False)])
                if parent_rec:

                    parent_rec.write({'recurring_donation_ids': [(4, donation.id)]})

        return

    # this function will check on create button it will give  default value  first it will search in hr employee if it not get,
    # then it will create name, code in core section
    @api.model
    def default_get(self, fields):
        res = super(donation_donation, self).default_get(fields)
        res['tax_receipt_option'] = 'none'
        res['donation_date'] = date.today().strftime('%Y-%m-%d')
        core_sec = self.env['core.sections']
        hr_employee = self.env['hr.employee']
        res_user = self.env['res.users']
        if self._uid:
            u_id = res_user.browse(self._uid)
            hr_emp = hr_employee.search([('user_id','=',u_id.id)])
            if hr_emp:
                core_id = core_sec.search([('name','=',hr_emp.name)])
                if not core_id:
                    core_id = core_sec.create({'name':hr_emp.name,'code':hr_emp.name})
                res['core_sections'] = core_id.id
        return res

    # function will work on onchange based on condition
    @api.onchange('partner_id')
    def partner_id_change(self):
        res_users = self.env['res.users']
        if self.partner_id and not self.tax_receipt_option:
            self.tax_receipt_option = 'none'

        if self.partner_id:
            user_id = res_users.search([('partner_id','=',self.partner_id.id)])
            if user_id:
                self.user_id = user_id.id
            else:
                self.user_id = False

    @api.model
    def create(self, vals):
        res = super(donation_donation, self).create(vals)
        res.write({'admin_id':self.env.uid})
        return res

    @api.multi
    def write(self, vals):
        vals.update({'admin_id':self.env.uid})
        res = super(donation_donation, self).write(vals)
        return res

