# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class AccountAccount(models.Model):
    _inherit = 'account.account'

    quickbooks_import = fields.Boolean('QuickBooks Import', default=False)


class CustomerCustomer(models.Model):
    _inherit = 'res.partner'

    quickbooks_import = fields.Boolean('QuickBooks Import', default=False)

class ProductProduct(models.Model):
    _inherit = 'product.template'

    quickbooks_import = fields.Boolean('QuickBooks Import', default=False)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    quickbooks_import_invoice= fields.Boolean('QuickBooks Import', default=False)



class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    quickbooks_import_invoice_line= fields.Boolean('QuickBooks Import', default=False)