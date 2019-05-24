from odoo import fields, models, tools,api, _
from odoo.exceptions import UserError, AccessError
from odoo.exceptions import UserError,ValidationError
from odoo.tools import email_re, email_split


class LeadtoOpportunity(models.TransientModel):
    _name='convert.lead.opportunity'

    @api.model
    def default_get(self, fields):
        """ Default get for name, opportunity_ids.
            If there is an exisitng partner link to the lead, find all existing
            opportunities links with this partner to merge all information together
        """
        result = super(LeadtoOpportunity, self).default_get(fields)
        print result
        # context = self._context
        # print self.crm_id
        if self._context.get('active_id'):
            tomerge = {int(self._context['active_id'])}
            lead = self.env['crm.lead'].browse(self._context['active_id'])
            fname = lead.name
            lname = lead.last_name
            email = lead.primary_email
            type=lead.crm_type

            tomerge.update(self._get_duplicated_leads_name_email(fname,lname, email,type, include_lost=True).ids)
            tomergelist = list(tomerge)

            if 'action' in fields and not result.get('action'):
                result['action'] = 'exist' if fname and fname else 'create'
            if 'name' in fields:
                result['name'] = fname
            if 'name' in fields:
                result['name'] = 'merge' if len(tomergelist) >= 2 else 'convert'
            # if 'lname' in fields:
            #     result['lname'] = lname
            # if 'lname' in fields:
            #     result['lname'] = 'merge' if len(tomergelist) >= 2 else 'convert'
            if 'opportunity_ids' in fields and len(tomergelist) >= 2:
                result['opportunity_ids'] = tomergelist

            if lead.user_id:
                result['user_id'] = lead.user_id.id
            if lead.team_id:
                result['team_id'] = lead.team_id.id
            if not fname and not lname:
                result['action'] = 'nothing'
        return result



    name = fields.Selection([
        ('convert', 'Convert to opportunity'),
        ('merge', 'Merge with existing opportunities')
    ], 'Conversion Action', required=True)
    opportunity_ids = fields.Many2many('crm.lead', string='Opportunities')
    user_id = fields.Many2one('res.users', 'Salesperson', index=True)
    team_id = fields.Many2one('crm.team', 'Sales Team', oldname='section_id', index=True)

    @api.model
    def _get_duplicated_leads_name_email(self, fname,lname,email,type, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        return self._get_duplicated_leads_by_emails_name(fname,lname, email,type, include_lost=include_lost)

    @api.model
    def _get_duplicated_leads_by_emails_name(self, fname,lname,email,type, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        partner_match_domain = []
        for email in set(email_split(email) + [email]):
            partner_match_domain.append(('primary_email', '=ilike', email))
        if fname:
            partner_match_domain.append(('name', '=', fname))
        partner_match_domain = ['&'] * (len(partner_match_domain) - 1) + partner_match_domain

        if lname:
            partner_match_domain.append(('last_name', '=', lname))
        partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain

        if type:
            partner_match_domain.append(('crm_type', '=', type))
        partner_match_domain = ['&'] * (len(partner_match_domain) - 5) + partner_match_domain


        if not partner_match_domain:
            return []
        domain = partner_match_domain
        if not include_lost:
            domain += ['&', ('active', '=', True), ('probability', '<', 100)]
        res=self.env['crm.lead'].search(domain)
        print ("---------------",res)
        return self.env['crm.lead'].search(domain)

    @api.multi
    def action_apply(self):
        """ Convert lead to opportunity or merge lead and opportunity and open
            the freshly created opportunity view.
        """
        self.ensure_one()
        values = {
            'team_id': self.team_id.id,
        }

        # if self.partner_id:
        #     values['partner_id'] = self.partner_id.id

        if self.name == 'merge':
            leads = self.opportunity_ids.merge_opportunity()
            if leads.type == "lead":
                values.update({'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
                self.with_context(active_ids=leads.ids)._convert_opportunity(values)
            elif not self._context.get('no_force_assignation') or not leads.user_id:
                values['user_id'] = self.user_id.id
                leads.write(values)
        else:
            leads = self.env['crm.lead'].browse(self._context.get('active_ids', []))
            values.update({'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
            self._convert_opportunity(values)

        return leads[0].redirect_opportunity_view1()

    @api.multi
    def _convert_opportunity(self, vals):
        self.ensure_one()
        res = False

        leads = self.env['crm.lead'].browse(vals.get('lead_ids'))
        for lead in leads:
            self_def_user = self.with_context(default_user_id=self.user_id.id)
            # name = self_def_user._create_name(
            #     lead.id, vals.get('name') or lead.name)
            res = lead._convert_opportunity_data1([], False)
        user_ids = vals.get('user_ids')

        leads_to_allocate = leads
        if self._context.get('no_force_assignation'):
            leads_to_allocate = leads_to_allocate.filtered(lambda lead: not lead.user_id)

        if user_ids:
            leads_to_allocate.allocate_salesman(user_ids, team_id=(vals.get('team_id')))

        return res