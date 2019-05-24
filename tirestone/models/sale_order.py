from odoo import api, fields, models, _

class Sale_Order(models.Model):
    _inherit = "sale.order"


    custom_create_date=fields.Date("Create Date")
    phone_no=fields.Char(related='partner_id.phone',string='Phone')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'sale.order') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or _('New')

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id',
                                                   partner.property_product_pricelist and partner.property_product_pricelist.id)
        result = super(Sale_Order, self).create(vals)
        result.write({'custom_create_date': result.create_date})
        return result

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        menus = super(Sale_Order, self).search(args, offset=0, limit=None, order=order, count=False)
        if menus:
            # menu filtering is done only on main menu tree, not other menu lists
            for arg in args:
                if 'name' in arg:
                    var=arg[2]

                    print(var)

            # if not self._context.get('ir.ui.menu.full_list'):
            #     menus = menus._filter_visible_menus()
            # if offset:
            #     menus = menus[long(offset):]
            # if limit:
            #     menus = menus[:long(limit)]
        return len(menus) if count else menus


# class Account_Invoice(models.Model):
#     _inherit = "account.invoice"
#
#     # @api.depends('company_id')
#     # def deafult_company(self):
#     #   for each in self:
#     #
#     #     user_id=self.env['res.users'].search([('id','=',each.env.uid)])
#     #
#     #     each.company_id=user_id.company_id.id
#     #     return each.company_id
#
#     company_id=fields.Many2one('res.company','Company', default=lambda self: self.env.user.company_id)



# class Res_Company(models.Model):
#     _inherit = "res.company"
#
#
#
#     send_note=fields.Text()

