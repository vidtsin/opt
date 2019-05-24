from odoo import fields, models, tools,api
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO


class CrmPartnerReport(models.Model):


    _name = "crm.partner.report"

    product_id =fields.Many2one('product.detail',string='Products')
    # user_id =fields.Many2one('res.users',string='Sales Person')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')

    @api.multi
    def generate_report(self):
        if self.product_id:
                if self.city:
                    if self.state_id:
                        if self.country_id:
                            tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                            form_view = self.env.ref('crm.crm_case_form_view_leads')
                            return {
                                'name': 'View Leads',
                                'type': 'ir.actions.act_window',
                                'src_model': 'crm.lead.report',
                                'res_model': 'crm.lead',
                                'view_type': 'form',
                                'view_mode': 'tree, form',
                                'views': [
                                    (tree_view.id, 'tree'),
                                    (form_view.id, 'form')],
                                'view_id': False,
                                'target': 'self',
                                'domain': [

                                    # ('type', '!=', 'lead'),
                                    ('product_id', '=', self.product_id.id),
                                    ('city', '=', self.city),
                                    ('state_id', '=', self.state_id.id),
                                    ('country_id', '=', self.country_id.id),

                                    # ('program', '=', self.filter_program_id.id),
                                    # ('team_id', '=', self.filter_team_id.id),

                                ],

                            }
                        if not self.country_id:
                            tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                            form_view = self.env.ref('crm.crm_case_form_view_leads')
                            return {
                                'name': 'View Leads',
                                'type': 'ir.actions.act_window',
                                'src_model': 'crm.lead.report',
                                'res_model': 'crm.lead',
                                'view_type': 'form',
                                'view_mode': 'tree, form',
                                'views': [
                                    (tree_view.id, 'tree'),
                                    (form_view.id, 'form')],
                                'view_id': False,
                                'target': 'self',
                                'domain': [

                                    # ('type', '!=', 'lead'),
                                    ('product_id', '=', self.product_id.id),
                                    ('city', '=', self.city),
                                    ('state_id', '=', self.state_id.id),
                                    # ('country_id', '=', self.country_id.id),

                                    # ('program', '=', self.filter_program_id.id),
                                    # ('team_id', '=', self.filter_team_id.id),

                                ],

                            }

                    if not self.state_id:
                        if self.country_id:
                            tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                            form_view = self.env.ref('crm.crm_case_form_view_leads')
                            return {
                                'name': 'View Leads',
                                'type': 'ir.actions.act_window',
                                'src_model': 'crm.lead.report',
                                'res_model': 'crm.lead',
                                'view_type': 'form',
                                'view_mode': 'tree, form',
                                'views': [
                                    (tree_view.id, 'tree'),
                                    (form_view.id, 'form')],
                                'view_id': False,
                                'target': 'self',
                                'domain': [

                                    # ('type', '!=', 'lead'),
                                    ('product_id', '=', self.product_id.id),
                                    ('city', '=', self.city),
                                    # ('state_id', '=', self.state_id.id),
                                    ('country_id', '=', self.country_id.id),

                                    # ('program', '=', self.filter_program_id.id),
                                    # ('team_id', '=', self.filter_team_id.id),

                                ],

                            }
                        if not self.country_id:
                            tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                            form_view = self.env.ref('crm.crm_case_form_view_leads')
                            return {
                                'name': 'View Leads',
                                'type': 'ir.actions.act_window',
                                'src_model': 'crm.lead.report',
                                'res_model': 'crm.lead',
                                'view_type': 'form',
                                'view_mode': 'tree, form',
                                'views': [
                                    (tree_view.id, 'tree'),
                                    (form_view.id, 'form')],
                                'view_id': False,
                                'target': 'self',
                                'domain': [

                                    # ('type', '!=', 'lead'),
                                    ('product_id', '=', self.product_id.id),
                                    ('city', '=', self.city),
                                    # ('state_id', '=', self.state_id.id),
                                    # ('country_id', '=', self.country_id.id),

                                    # ('program', '=', self.filter_program_id.id),
                                    # ('team_id', '=', self.filter_team_id.id),

                                ],

                            }


                if not self.city:
                    if self.state_id:
                        if self.country_id:
                            tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                            form_view = self.env.ref('crm.crm_case_form_view_leads')
                            return {
                                'name': 'View Leads',
                                'type': 'ir.actions.act_window',
                                'src_model': 'crm.lead.report',
                                'res_model': 'crm.lead',
                                'view_type': 'form',
                                'view_mode': 'tree, form',
                                'views': [
                                    (tree_view.id, 'tree'),
                                    (form_view.id, 'form')],
                                'view_id': False,
                                'target': 'self',
                                'domain': [

                                    # ('type', '!=', 'lead'),
                                    ('product_id', '=', self.product_id.id),
                                    # ('city', '=', self.city),
                                    ('state_id', '=', self.state_id.id),
                                    ('country_id', '=', self.country_id.id),

                                    # ('program', '=', self.filter_program_id.id),
                                    # ('team_id', '=', self.filter_team_id.id),

                                ],

                            }
                        if not self.country_id:
                            tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                            form_view = self.env.ref('crm.crm_case_form_view_leads')
                            return {
                                'name': 'View Leads',
                                'type': 'ir.actions.act_window',
                                'src_model': 'crm.lead.report',
                                'res_model': 'crm.lead',
                                'view_type': 'form',
                                'view_mode': 'tree, form',
                                'views': [
                                    (tree_view.id, 'tree'),
                                    (form_view.id, 'form')],
                                'view_id': False,
                                'target': 'self',
                                'domain': [

                                    # ('type', '!=', 'lead'),
                                    ('product_id', '=', self.product_id.id),
                                    # ('city', '=', self.city),
                                    ('state_id', '=', self.state_id.id),
                                    # ('country_id', '=', self.country_id.id),

                                    # ('program', '=', self.filter_program_id.id),
                                    # ('team_id', '=', self.filter_team_id.id),

                                ],

                            }

                    if not self.state_id:
                        if self.country_id:
                            tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                            form_view = self.env.ref('crm.crm_case_form_view_leads')
                            return {
                                'name': 'View Leads',
                                'type': 'ir.actions.act_window',
                                'src_model': 'crm.lead.report',
                                'res_model': 'crm.lead',
                                'view_type': 'form',
                                'view_mode': 'tree, form',
                                'views': [
                                    (tree_view.id, 'tree'),
                                    (form_view.id, 'form')],
                                'view_id': False,
                                'target': 'self',
                                'domain': [

                                    # ('type', '!=', 'lead'),
                                    ('product_id', '=', self.product_id.id),
                                    # ('city', '=', self.city),
                                    # ('state_id', '=', self.state_id.id),
                                    ('country_id', '=', self.country_id.id),

                                    # ('program', '=', self.filter_program_id.id),
                                    # ('team_id', '=', self.filter_team_id.id),

                                ],

                            }
                        if not self.country_id:
                            tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                            form_view = self.env.ref('crm.crm_case_form_view_leads')
                            return {
                                'name': 'View Leads',
                                'type': 'ir.actions.act_window',
                                'src_model': 'crm.lead.report',
                                'res_model': 'crm.lead',
                                'view_type': 'form',
                                'view_mode': 'tree, form',
                                'views': [
                                    (tree_view.id, 'tree'),
                                    (form_view.id, 'form')],
                                'view_id': False,
                                'target': 'self',
                                'domain': [

                                    # ('type', '!=', 'lead'),
                                    ('product_id', '=', self.product_id.id),
                                    # ('city', '=', self.city),
                                    # ('state_id', '=', self.state_id.id),
                                    # ('country_id', '=', self.country_id.id),

                                    # ('program', '=', self.filter_program_id.id),
                                    # ('team_id', '=', self.filter_team_id.id),

                                ],

                            }



        if not self.product_id:
            if self.city:
                if self.state_id:
                    if self.country_id:
                        tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                        form_view = self.env.ref('crm.crm_case_form_view_leads')
                        return {
                            'name': 'View Leads',
                            'type': 'ir.actions.act_window',
                            'src_model': 'crm.lead.report',
                            'res_model': 'crm.lead',
                            'view_type': 'form',
                            'view_mode': 'tree, form',
                            'views': [
                                (tree_view.id, 'tree'),
                                (form_view.id, 'form')],
                            'view_id': False,
                            'target': 'self',
                            'domain': [

                                # ('type', '!=', 'lead'),
                                # ('product_id', '=', self.product_id.id),
                                ('city', '=', self.city),
                                ('state_id', '=', self.state_id.id),
                                ('country_id', '=', self.country_id.id),

                                # ('program', '=', self.filter_program_id.id),
                                # ('team_id', '=', self.filter_team_id.id),

                            ],

                        }
                    if self.country_id:
                        tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                        form_view = self.env.ref('crm.crm_case_form_view_leads')
                        return {
                            'name': 'View Leads',
                            'type': 'ir.actions.act_window',
                            'src_model': 'crm.lead.report',
                            'res_model': 'crm.lead',
                            'view_type': 'form',
                            'view_mode': 'tree, form',
                            'views': [
                                (tree_view.id, 'tree'),
                                (form_view.id, 'form')],
                            'view_id': False,
                            'target': 'self',
                            'domain': [

                                # ('type', '!=', 'lead'),
                                # ('product_id', '=', self.product_id.id),
                                ('city', '=', self.city),
                                ('state_id', '=', self.state_id.id),
                                # ('country_id', '=', self.country_id.id),

                                # ('program', '=', self.filter_program_id.id),
                                # ('team_id', '=', self.filter_team_id.id),

                            ],

                        }
                if not self.state_id:
                    if self.country_id:
                        tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                        form_view = self.env.ref('crm.crm_case_form_view_leads')
                        return {
                            'name': 'View Leads',
                            'type': 'ir.actions.act_window',
                            'src_model': 'crm.lead.report',
                            'res_model': 'crm.lead',
                            'view_type': 'form',
                            'view_mode': 'tree, form',
                            'views': [
                                (tree_view.id, 'tree'),
                                (form_view.id, 'form')],
                            'view_id': False,
                            'target': 'self',
                            'domain': [

                                # ('type', '!=', 'lead'),
                                # ('product_id', '=', self.product_id.id),
                                ('city', '=', self.city),
                                # ('state_id', '=', self.state_id.id),
                                ('country_id', '=', self.country_id.id),

                                # ('program', '=', self.filter_program_id.id),
                                # ('team_id', '=', self.filter_team_id.id),

                            ],

                        }
                    if self.country_id:
                        tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                        form_view = self.env.ref('crm.crm_case_form_view_leads')
                        return {
                            'name': 'View Leads',
                            'type': 'ir.actions.act_window',
                            'src_model': 'crm.lead.report',
                            'res_model': 'crm.lead',
                            'view_type': 'form',
                            'view_mode': 'tree, form',
                            'views': [
                                (tree_view.id, 'tree'),
                                (form_view.id, 'form')],
                            'view_id': False,
                            'target': 'self',
                            'domain': [

                                # ('type', '!=', 'lead'),
                                # ('product_id', '=', self.product_id.id),
                                ('city', '=', self.city),
                                # ('state_id', '=', self.state_id.id),
                                # ('country_id', '=', self.country_id.id),

                                # ('program', '=', self.filter_program_id.id),
                                # ('team_id', '=', self.filter_team_id.id),

                            ],

                        }

            if not self.city:
                if self.state_id:
                    if self.country_id:
                        tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                        form_view = self.env.ref('crm.crm_case_form_view_leads')
                        return {
                            'name': 'View Leads',
                            'type': 'ir.actions.act_window',
                            'src_model': 'crm.lead.report',
                            'res_model': 'crm.lead',
                            'view_type': 'form',
                            'view_mode': 'tree, form',
                            'views': [
                                (tree_view.id, 'tree'),
                                (form_view.id, 'form')],
                            'view_id': False,
                            'target': 'self',
                            'domain': [

                                # ('type', '!=', 'lead'),
                                # ('product_id', '=', self.product_id.id),
                                # ('city', '=', self.city),
                                ('state_id', '=', self.state_id.id),
                                ('country_id', '=', self.country_id.id),

                                # ('program', '=', self.filter_program_id.id),
                                # ('team_id', '=', self.filter_team_id.id),

                            ],

                        }
                    if self.country_id:
                        tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                        form_view = self.env.ref('crm.crm_case_form_view_leads')
                        return {
                            'name': 'View Leads',
                            'type': 'ir.actions.act_window',
                            'src_model': 'crm.lead.report',
                            'res_model': 'crm.lead',
                            'view_type': 'form',
                            'view_mode': 'tree, form',
                            'views': [
                                (tree_view.id, 'tree'),
                                (form_view.id, 'form')],
                            'view_id': False,
                            'target': 'self',
                            'domain': [

                                # ('type', '!=', 'lead'),
                                # ('product_id', '=', self.product_id.id),
                                # ('city', '=', self.city),
                                ('state_id', '=', self.state_id.id),
                                # ('country_id', '=', self.country_id.id),

                                # ('program', '=', self.filter_program_id.id),
                                # ('team_id', '=', self.filter_team_id.id),

                            ],

                        }
                if not self.state_id:
                    if self.country_id:
                        tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                        form_view = self.env.ref('crm.crm_case_form_view_leads')
                        return {
                            'name': 'View Leads',
                            'type': 'ir.actions.act_window',
                            'src_model': 'crm.lead.report',
                            'res_model': 'crm.lead',
                            'view_type': 'form',
                            'view_mode': 'tree, form',
                            'views': [
                                (tree_view.id, 'tree'),
                                (form_view.id, 'form')],
                            'view_id': False,
                            'target': 'self',
                            'domain': [

                                # ('type', '!=', 'lead'),
                                # ('product_id', '=', self.product_id.id),
                                # ('city', '=', self.city),
                                # ('state_id', '=', self.state_id.id),
                                ('country_id', '=', self.country_id.id),

                                # ('program', '=', self.filter_program_id.id),
                                # ('team_id', '=', self.filter_team_id.id),

                            ],

                        }
                    if not self.country_id:
                        tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                        form_view = self.env.ref('crm.crm_case_form_view_leads')
                        return {
                            'name': 'View Leads',
                            'type': 'ir.actions.act_window',
                            'src_model': 'crm.lead.report',
                            'res_model': 'crm.lead',
                            'view_type': 'form',
                            'view_mode': 'tree, form',
                            'views': [
                                (tree_view.id, 'tree'),
                                (form_view.id, 'form')],
                            'view_id': False,
                            'target': 'self',
                            'domain': [

                                # ('type', '!=', 'lead'),
                                # ('product_id', '=', self.product_id.id),
                                # ('city', '=', self.city),
                                # ('state_id', '=', self.state_id.id),
                                # ('country_id', '=', self.country_id.id),

                                # ('program', '=', self.filter_program_id.id),
                                # ('team_id', '=', self.filter_team_id.id),

                            ],

                        }
