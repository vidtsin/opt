from odoo import fields, models, http, _, api
from odoo.exceptions import UserError, ValidationError
# from amazonproduct.api import API

class InvoiceLine(models.Model):
    _inherit = "account.invoice.line"
    
    department_id = fields.Many2one("core.departments", string="Departments")
    cost_center_id = fields.Many2one("core.cost.center", string="Cost Center")
    sections_id = fields.Many2one("core.sections", string="Sections")


class VendorDetails(models.Model):
    _inherit = "account.invoice"



    department_id = fields.Many2one("core.departments", string="Departments")
    cost_center_id = fields.Many2one("core.cost.center", string="Cost Center")
    sections_id = fields.Many2one("core.sections", string="Sections")


    #it will check in invoice line ids if line quantity is 0 it will continue it will check in invoice line tax ids
    # it will create in move line
    @api.model
    def invoice_line_move_line_get(self):
        res = []
        for line in self.invoice_line_ids:
            if line.quantity == 0:
                continue
            tax_ids = []
            for tax in line.invoice_line_tax_ids:
                tax_ids.append((4, tax.id, None))
                for child in tax.children_tax_ids:
                    if child.type_tax_use != 'none':
                        tax_ids.append((4, child.id, None))
            analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]

            move_line_dict = {
                'invl_id': line.id,
                'type': 'src',
                'name': line.name.split('\n')[0][:64],
                'price_unit': line.price_unit,
                'quantity': line.quantity,
                'price': line.price_subtotal,
                'account_id': line.account_id.id,
                'product_id': line.product_id.id,
                'uom_id': line.uom_id.id,
                'account_analytic_id': line.account_analytic_id.id,
                'tax_ids': tax_ids,
                'invoice_id': self.id,
                'analytic_tag_ids': analytic_tag_ids,
                'department_id': line.department_id.id,
                'cost_center_id': line.cost_center_id.id,
                'sections_id': line.sections_id.id,

            }
            if line['account_analytic_id']:
                move_line_dict['analytic_line_ids'] = [(0, 0, line._get_analytic_line())]
            res.append(move_line_dict)
        return res



    @api.model
    def line_get_convert(self, line, part):
        return {
            'date_maturity': line.get('date_maturity', False),
            'partner_id': part,
            'name': line['name'][:64],
            'debit': line['price'] > 0 and line['price'],
            'credit': line['price'] < 0 and -line['price'],
            'account_id': line['account_id'],
            'analytic_line_ids': line.get('analytic_line_ids', []),
            'amount_currency': line['price'] > 0 and abs(line.get('amount_currency', False)) or -abs(
                line.get('amount_currency', False)),
            'currency_id': line.get('currency_id', False),
            'quantity': line.get('quantity', 1.00),
            'product_id': line.get('product_id', False),
            'product_uom_id': line.get('uom_id', False),
            'analytic_account_id': line.get('account_analytic_id', False),
            'invoice_id': line.get('invoice_id', False),
            'tax_ids': line.get('tax_ids', False),
            'tax_line_id': line.get('tax_line_id', False),
            'department_id': line.get('department_id'),
            'cost_center_id': line.get('cost_center_id'),
            'sections_id': line.get('sections_id'),
            'analytic_tag_ids': line.get('analytic_tag_ids', False),
        }

class Bank(models.Model):
    _inherit = "account.bank.statement.line"
    
    department_id = fields.Many2one("core.departments", string="Departments")
    cost_center_id = fields.Many2one("core.cost.center", string="Cost Center")
    sections_id = fields.Many2one("core.sections", string="Sections")
    

class BankLine(models.Model):
    _inherit = "account.move.line"
    invoice_id = fields.Many2one('account.bank.statement.line', string='Invoice Reference',
        ondelete='cascade', index=True)
    

class JournalLine(models.Model):
    _inherit = "account.move.line"
    invoice_id = fields.Many2one('account.invoice.line', string='Invoice Reference',
        ondelete='cascade', index=True)
    
    department_id = fields.Many2one("core.departments", string="Departments")
    cost_center_id = fields.Many2one("core.cost.center",  string="Cost Center")
    sections_id = fields.Many2one("core.sections", string="Sections")



 
    

   
   
     
