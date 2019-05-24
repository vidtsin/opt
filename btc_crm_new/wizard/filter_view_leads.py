from odoo import fields, models, tools,api, _




class FilterLeads(models.TransientModel):
    _name = 'filter.leads'
    _rec_name = 'name'

    name = fields.Char('Name')
    filter_faculty_id = fields.Many2one('faculty.details','Faculty')
    filter_program_id= fields.Many2one('program.details', 'Program')
    filter_team_id = fields.Many2one('crm.team','Sales team')


    @api.multi
    def view_lead(self):
        if not self.filter_program_id:
            if not self.filter_team_id:
                tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                form_view = self.env.ref('crm.crm_case_form_view_oppor')
                return {
                    'name': 'View Leads',
                    'type': 'ir.actions.act_window',
                    'src_model': 'filter.leads',
                    'res_model': 'crm.lead',
                    'view_type': 'form',
                    'view_mode': 'tree, form',
                    'views': [
                        (tree_view.id, 'tree'),
                        (form_view.id, 'form')],
                    'view_id': False,
                    'target': 'self',
                    'domain': [
                        # ('faculty_ids', '=', self.filter_faculty_id.id),
                        ('type', '=', 'lead'),
                        ('checked', '=', False),
                        # ('program', '=', self.filter_program_id.id),
                        # ('team_id', '=', self.filter_team_id.id),


                    ],
                    # 'context': {'group_by': self.filter_record},

                    # 'target': 'main',
                }
            else:
                tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                form_view = self.env.ref('crm.crm_case_form_view_oppor')
                return {
                    'name': 'View Leads',
                    'type': 'ir.actions.act_window',
                    'src_model': 'filter.leads',
                    'res_model': 'crm.lead',
                    'view_type': 'form',
                    'view_mode': 'tree, form',
                    'views': [
                        (tree_view.id, 'tree'),
                        (form_view.id, 'form')],
                    'view_id': False,
                    'target': 'self',
                    'domain': [
                        # ('faculty_ids', '=', self.filter_faculty_id.id),
                        ('type', '=', 'lead'),
                        ('checked', '=', False),
                        # ('program', '=', self.filter_program_id.id),
                        ('team_id', '=', self.filter_team_id.id),

                    ],
                    # 'context': {'group_by': self.filter_record},

                    # 'target': 'main',
                }
        if self.filter_program_id != False:
            if not self.filter_team_id:
                tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                form_view = self.env.ref('crm.crm_case_form_view_oppor')
                return {
                    'name': 'View Leads',
                    'type': 'ir.actions.act_window',
                    'src_model': 'filter.leads',
                    'res_model': 'crm.lead',
                    'view_type': 'form',
                    'view_mode': 'tree, form',
                    'views': [
                        (tree_view.id, 'tree'),
                        (form_view.id, 'form')],
                    'view_id': False,
                    'target': 'self',
                    'domain': [
                        # ('faculty_ids', '=', self.filter_faculty_id.id),
                        ('type', '=', 'lead'),
                        ('checked', '=', False),
                        ('program', '=', self.filter_program_id.id),
                        # ('team_id', '=', self.filter_team_id.id),

                    ],
                    # 'context': {'group_by': self.filter_record},

                    # 'target': 'main',
                }
            else:
                tree_view = self.env.ref('crm.crm_case_tree_view_leads')
                form_view = self.env.ref('crm.crm_case_form_view_oppor')
                return {
                    'name': 'View Leads',
                    'type': 'ir.actions.act_window',
                    'src_model': 'filter.leads',
                    'res_model': 'crm.lead',
                    'view_type': 'form',
                    'view_mode': 'tree, form',
                    'views': [
                        (tree_view.id, 'tree'),
                        (form_view.id, 'form')],
                    'view_id': False,
                    'target': 'self',
                    'domain': [
                        # ('faculty_ids', '=', self.filter_faculty_id.id),
                        ('type', '=', 'lead'),
                        ('checked', '=', False),
                        ('program', '=', self.filter_program_id.id),
                        ('team_id', '=', self.filter_team_id.id),

                    ],
                    # 'context': {'group_by': self.filter_record},

                    # 'target': 'main',
                }
