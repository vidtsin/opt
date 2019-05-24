from odoo import api, fields, models,tools, _

class Product(models.Model):
    _inherit = 'product.template'

    admission_requirements=fields.Text('Admission Requirements')
    other_requirements=fields.Text('Other Requirements')
    duration_in_weeks=fields.Integer('Duration/Weeks')
    duration_in_hours = fields.Integer('Duration/Hours')
    class_schedule=fields.Char('Class Schedule')
    tuition_fee=fields.Float('Tuition Fee')
    texts_book_fee=fields.Float('Text Book Fee')
    seat_deposit_fee=fields.Float('Seat Deposit Fee')
    lab_fee=fields.Float('Lab/Clinical Fee')
    lab_supply_fee=fields.Float('Lab Supply Fee')
    major_equipment_fee=fields.Float('Major Equipment Fee')
    professional_exam_fee=fields.Float('Professional Exam Fee')
    program_start_date=fields.Char('Program Start Date')
    deadline_to_apply=fields.Char('Deadline To Apply')
    scholarship=fields.Char('Scholarship')

class Product_Product(models.Model):
    _inherit = 'product.product'

    @api.multi
    def name_get(self):
        # TDE: this could be cleaned a bit I think

        def _name_get(d):
            name = d.get('name', '')
            return (d['id'], name)

        partner_id = self._context.get('partner_id')
        if partner_id:
            partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
        else:
            partner_ids = []

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []
        for product in self.sudo():
            # display only the attributes with multiple possible values on the template
            variable_attributes = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped('attribute_id')
            variant = product.attribute_value_ids._variant_name(variable_attributes)

            name = variant and "%s (%s)" % (product.name, variant) or product.name
            sellers = []
            if partner_ids:
                sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and (x.product_id == product)]
                if not sellers:
                    sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and not x.product_id]
            if sellers:
                for s in sellers:
                    seller_variant = s.product_name and (
                        variant and "%s (%s)" % (s.product_name, variant) or s.product_name
                        ) or False
                    mydict = {
                              'id': product.id,
                              'name': seller_variant or name,
                              'default_code': s.product_code or product.default_code,
                              }
                    temp = _name_get(mydict)
                    if temp not in result:
                        result.append(temp)
            else:
                mydict = {
                          'id': product.id,
                          'name': name,
                          'default_code': product.default_code,
                          }
                result.append(_name_get(mydict))
        return result