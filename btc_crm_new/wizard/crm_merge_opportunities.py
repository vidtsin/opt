from odoo import api, fields, models,_
from odoo.tools import email_re, email_split


class MergeLeadOpportunity(models.TransientModel):
    """
        Merge opportunities together.
        If we're talking about opportunities, it's just because it makes more sense
        to merge opps than leads, because the leads are more ephemeral objects.
        But since opportunities are leads, it's also possible to merge leads
        together (resulting in a new lead), or leads and opps together (resulting
        in a new opp).
    """

    _name='crm.merge.lead.opportunity'
    _description = 'Merge lead opportunities'

    @api.model
    def default_get(self, fields):
        """ Use active_ids from the context to fetch the leads/opps to merge.
            In order to get merged, these leads/opps can't be in 'Dead' or 'Closed'
        """
        record_ids = self._context.get('active_ids')
        result = super(MergeLeadOpportunity, self).default_get(fields)

        if record_ids:
            if 'opportunity_ids' in fields:
                opp_ids = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100).ids
                result['opportunity_ids'] = opp_ids

        return result


    crm_id = fields.Many2one('crm.lead', 'Crm Id')
    user_id = fields.Many2one('res.users', 'Salesperson', index=True)
    team_id = fields.Many2one('crm.team', 'Sales Team', oldname='section_id', index=True)
    lead_name = fields.Boolean('Name')
    lead_email = fields.Boolean('Email')
    lead_phone = fields.Boolean('Phone')

    convert_stage = fields.Selection([('Opportunity', 'Opportunity'),
                                      ('Delayed', 'Delayed'),
                                      ('Dead', 'Dead')],
                                     string='Convert Stage')
    opportunity_ids = fields.Many2many('crm.lead', string='Opportunities')
    # name = fields.Selection([
    #     ('convert', 'Convert to opportunity'),
    #     ('merge', 'Merge with existing opportunities')
    # ], 'Conversion Action', required=True)


    @api.multi
    def _convert_to_opportunity(self, vals):
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

    @api.multi
    def action_merge_lead(self):
        """ Convert lead to opportunity or merge lead and opportunity and open
            the freshly created opportunity view.
        """
        self.ensure_one()
        values = {
            'team_id': self.team_id.id,
        }
        # ids = [id.id for id in self.opportunity_ids]

        # if partner_id:
        #     values['partner_id'] = partner_id

        # leads = self.opportunity_ids.with_context(con_opp_merge=True).merge_opportunity()
        for rec in self._context.get('active_ids', []):
            # if rec:
            rec2 = self.env['crm.lead'].browse(rec)
            for p in rec2:
                p2 = p.id
                # self.opportunity_ids=data

                # value1={
                #     'crm_lead_id':self.opportunity_ids.id,
                #     'crm_lead':p.id
                # }

                mergedid = self.env['merged.crm.leads'].create(
                    {'crm_lead_id': self.opportunity_ids[-1].id, 'crm_lead': p2})

                # merge_id=self.env['merged.crm.leads'].create(value1)
        leads = self.opportunity_ids.with_context(con_opp_merge=True).merge_opportunity_2()
        if leads.type == "lead":
            values.update({'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
            self.with_context(active_ids=leads.ids)._convert_to_opportunity(values)
        elif not self._context.get('no_force_assignation') or not leads.user_id:
            values['user_id'] = self.user_id.id
            leads.write(values)
        return leads[0].redirect_opportunity_view()

    @api.onchange('lead_name', 'lead_email', 'lead_phone')
    def _onchange_deduplicate(self):
        if self.lead_name  and self.lead_email == True:
            active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
            leads_with_duplicates = []
            for rec in active_leads:
                rec2 = self.env['crm.lead'].browse(rec)


            # partner_ids = [(lead.name, lead.email_from) for lead in
            #                active_leads]
            # partners_duplicated_leads = {}
            # for name, email_from in partner_ids:
            #     duplicated_leads = self._name_email(name, email_from)
            #     if len(duplicated_leads) > 1:
            #         partners_duplicated_leads.setdefault((name, email_from), []).extend(duplicated_leads)
            #
            # leads_with_duplicates = []
            # for lead in active_leads:
            #     lead_tuple = (lead.name, lead.email_from if lead.name else lead.email_from)
            #     if len(partners_duplicated_leads.get(lead_tuple, [])) > 1:
            #         leads_with_duplicates.append(lead.id)
            #
            # self.opportunity_ids = self.env['crm.lead'].browse(leads_with_duplicates)

    @api.model
    def _name_email(self, name, email, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        return self._by_name_emails(name, email, include_lost=include_lost)

    @api.model
    def _by_name_emails(self, name, email, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        partner_match_domain = []
        for email in set(email_split(email) + [email]):
            partner_match_domain.append(('email_from', '=ilike', email))
        if name:
            partner_match_domain.append(('name', '=', name))
        partner_match_domain = ['&'] * (len(partner_match_domain) - 1) + partner_match_domain
        if not partner_match_domain:
            return []
        domain = partner_match_domain
        if not include_lost:
            domain += ['&', ('active', '=', True), ('probability', '<', 100)]
        return self.env['crm.lead'].search(domain)
    #

    # @api.onchange('lead_name', 'lead_email', 'lead_phone')
    # def _onchange_deduplicate(self):
    #
    #
    #     global ids
    #
    #     if self.lead_name and self.lead_phone and self.lead_email == True:
    #         active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
    #         partner_ids = [(lead.name, lead.email_from, lead.phone) for lead in
    #                        active_leads]
    #         partners_duplicated_leads = {}
    #         for name, email_from, phone in partner_ids:
    #             duplicated_leads = (self._get_duplicated_leads(name, email_from, phone).ids)
    #             if len(duplicated_leads) >= 2:
    #                 partners_duplicated_leads.setdefault((name, email_from, phone), []).extend(duplicated_leads)
    #
    #         leads_with_duplicates = []
    #         for duplicate in duplicated_leads:
    #             rec2 = self.env['crm.lead'].browse(duplicate)
    #             lead_tuple = (
    #             rec2.name, rec2.email_from, rec2.phone if rec2.email_from and rec2.phone and rec2.name else rec2.phone)
    #             if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
    #                 leads_with_duplicates.append(duplicate)
    #         tomergedup = list(leads_with_duplicates)
    #         tempdup = list(leads_with_duplicates)
    #         for rec in tempdup:
    #             rec2 = self.env['crm.lead'].browse(rec)
    #             if rec2.checked == True:
    #                 tomergedup.remove(rec)
    #         self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         ids = [id.id for id in opportunity_ids]
    #         self._cr.commit()
    #
    #     elif self.lead_name and self.lead_email == True:
    #         # val ={}
    #         active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
    #         partner_ids = [(lead.name, lead.email_from) for lead in
    #                        active_leads]
    #         partners_duplicated_leads = {}
    #         for name, email_from in partner_ids:
    #             duplicated_leads = (self._name_email(name, email_from).ids)
    #             if len(duplicated_leads) > 1:
    #                 partners_duplicated_leads.setdefault((name, email_from), []).extend(duplicated_leads)
    #         leads_with_duplicates = []
    #         for duplicate in active_leads:
    #             rec2 = self.env['crm.lead'].browse(duplicate)
    #             lead_tuple = (rec2.name, rec2.email_from)
    #             if len(partners_duplicated_leads.get(lead_tuple, [])) > 1:
    #                 leads_with_duplicates.append(duplicate)
    #         tomergedup = list(leads_with_duplicates)
    #         tempdup = list(leads_with_duplicates)
    #         for rec in tempdup:
    #             rec2 = self.env['crm.lead'].browse(rec)
    #             if rec2.checked == True:
    #                 tomergedup.remove(rec)
    #
    #         # val= leads_with_duplicates
    #         # return {'opportunity_ids':val}
    #         # self.write({'opportunity_ids': (6, 0, leads_with_duplicates), })
    #         # self._cr.commit()
    #         # user_rel_id=(4,leads_with_duplicates)
    #         # self.write({'opportunity_ids':  user_rel_id})
    #         self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         ids = [id.id for id in opportunity_ids]
    #         self._cr.commit()
    #     elif self.lead_name and self.lead_phone == True:
    #         # values = {}
    #         active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
    #         partner_ids = [(lead.name, lead.phone) for lead in
    #                        active_leads]
    #         partners_duplicated_leads = {}
    #         for name, phone in partner_ids:
    #             duplicated_leads = (self._name_phone(name, phone).ids)
    #             if len(duplicated_leads) >= 2:
    #                 partners_duplicated_leads.setdefault((name, phone), []).extend(duplicated_leads)
    #
    #         leads_with_duplicates = []
    #         for duplicate in duplicated_leads:
    #             rec2 = self.env['crm.lead'].browse(duplicate)
    #             lead_tuple = (rec2.name, rec2.phone if rec2.name and rec2.phone else rec2.phone)
    #             if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
    #                 leads_with_duplicates.append(duplicate)
    #         tomergedup = list(leads_with_duplicates)
    #         tempdup = list(leads_with_duplicates)
    #         for rec in tempdup:
    #             rec2 = self.env['crm.lead'].browse(rec)
    #             if rec2.checked == True:
    #                 tomergedup.remove(rec)
    #
    #         # val= leads_with_duplicates
    #         # return {'opportunity_ids':val}
    #         # self.write({'opportunity_ids': (6, 0, leads_with_duplicates), })
    #         # self._cr.commit()
    #         # user_rel_id=(4,leads_with_duplicates)
    #         # self.write({'opportunity_ids':  user_rel_id})
    #         self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         ids = [id.id for id in opportunity_ids]
    #         self._cr.commit()
    #
    #     elif self.lead_email and self.lead_phone == True:
    #         active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
    #         partner_ids = [(lead.email_from, lead.phone) for lead in
    #                        active_leads]
    #         partners_duplicated_leads = {}
    #         for email_from, phone in partner_ids:
    #             duplicated_leads = (self._emails_phone(email_from, phone).ids)
    #             if len(duplicated_leads) >= 2:
    #                 partners_duplicated_leads.setdefault((email_from, phone), []).extend(duplicated_leads)
    #
    #         leads_with_duplicates = []
    #         for duplicate in duplicated_leads:
    #             rec2 = self.env['crm.lead'].browse(duplicate)
    #             lead_tuple = (rec2.email_from, rec2.phone if rec2.email_from and rec2.phone else rec2.phone)
    #             if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
    #                 leads_with_duplicates.append(duplicate)
    #
    #         tomergedup = list(leads_with_duplicates)
    #         tempdup = list(leads_with_duplicates)
    #         for rec in tempdup:
    #             rec2 = self.env['crm.lead'].browse(rec)
    #             if rec2.checked == True:
    #                 tomergedup.remove(rec)
    #
    #         # val= leads_with_duplicates
    #         # return {'opportunity_ids':val}
    #         # self.write({'opportunity_ids': (6, 0, leads_with_duplicates), })
    #         # self._cr.commit()
    #         # user_rel_id=(4,leads_with_duplicates)
    #         # self.write({'opportunity_ids':  user_rel_id})
    #         self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         ids = [id.id for id in opportunity_ids]
    #         self._cr.commit()
    #     elif self.lead_name == True:
    #         active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
    #         partner_ids = [(lead.name) for lead in
    #                        active_leads]
    #         partners_duplicated_leads = {}
    #         for name in partner_ids:
    #             duplicated_leads = (self.lead_by_name(name).ids)
    #             if len(duplicated_leads) >= 2:
    #                 partners_duplicated_leads.setdefault((name), []).extend(duplicated_leads)
    #
    #         leads_with_duplicates = []
    #         for duplicate in duplicated_leads:
    #             rec2 = self.env['crm.lead'].browse(duplicate)
    #             lead_tuple = (rec2.name)
    #             if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
    #                 leads_with_duplicates.append(duplicate)
    #         tomergedup = list(leads_with_duplicates)
    #         tempdup = list(leads_with_duplicates)
    #         for rec in tempdup:
    #             rec2 = self.env['crm.lead'].browse(rec)
    #             if rec2.checked == True:
    #                 tomergedup.remove(rec)
    #         self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         ids = [id.id for id in opportunity_ids]
    #         self._cr.commit()
    #     elif self.lead_email == True:
    #         active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
    #         partner_ids = [(lead.email_from) for lead in
    #                        active_leads]
    #         partners_duplicated_leads = {}
    #         for email_from in partner_ids:
    #             duplicated_leads = (self.lead_by_email(email_from).ids)
    #             if len(duplicated_leads) >= 2:
    #                 partners_duplicated_leads.setdefault((email_from), []).extend(duplicated_leads)
    #
    #         leads_with_duplicates = []
    #         for duplicate in duplicated_leads:
    #             rec2 = self.env['crm.lead'].browse(duplicate)
    #             lead_tuple = (rec2.email_from)
    #             if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
    #                 leads_with_duplicates.append(duplicate)
    #         tomergedup = list(leads_with_duplicates)
    #         tempdup = list(leads_with_duplicates)
    #         for rec in tempdup:
    #             rec2 = self.env['crm.lead'].browse(rec)
    #             if rec2.checked == True:
    #                 tomergedup.remove(rec)
    #         self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         ids = [id.id for id in opportunity_ids]
    #         self._cr.commit()
    #     elif self.lead_phone == True:
    #         active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
    #         partner_ids = [(lead.phone) for lead in
    #                        active_leads]
    #         partners_duplicated_leads = {}
    #         for phone in partner_ids:
    #             duplicated_leads = (self.lead_by_phone(phone).ids)
    #             if len(duplicated_leads) >= 2:
    #                 partners_duplicated_leads.setdefault((phone), []).extend(duplicated_leads)
    #
    #         leads_with_duplicates = []
    #         for duplicate in duplicated_leads:
    #             rec2 = self.env['crm.lead'].browse(duplicate)
    #             lead_tuple = (rec2.phone)
    #             if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
    #                 leads_with_duplicates.append(duplicate)
    #         tomergedup = list(leads_with_duplicates)
    #         tempdup = list(leads_with_duplicates)
    #         for rec in tempdup:
    #             rec2 = self.env['crm.lead'].browse(rec)
    #             if rec2.checked == True:
    #                 tomergedup.remove(rec)
    #         self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         opportunity_ids = self.env['crm.lead'].browse(tomergedup)
    #         ids = [id.id for id in opportunity_ids]
    #         self._cr.commit()
    #
    # @api.model
    # def lead_by_phone(self, phone, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     return self._by_phone(phone, include_lost=include_lost)
    #
    # @api.model
    # def _by_phone(self, phone, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     partner_match_domain = []
    #     # for email in set(email_split(email) + [email]):
    #     #     partner_match_domain.append(('email_from', '=ilike', email))
    #     # if name:
    #     #     partner_match_domain.append(('name', '=', name))
    #     # partner_match_domain = [] * (len(partner_match_domain) - 1) + partner_match_domain
    #     if phone:
    #         partner_match_domain.append(('phone', '=', phone))
    #     partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain
    #     if not partner_match_domain:
    #         return []
    #     domain = partner_match_domain
    #     if not include_lost:
    #         domain += ['&', ('active', '=', True), ('probability', '<', 100)]
    #     return self.env['crm.lead'].search(domain)
    #
    # @api.model
    # def lead_by_email(self, email, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     return self._by_email(email, include_lost=include_lost)
    #
    # @api.model
    # def _by_email(self, email, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     partner_match_domain = []
    #     for email in set(email_split(email) + [email]):
    #         partner_match_domain.append(('email_from', '=ilike', email))
    #     # if name:
    #     #     partner_match_domain.append(('name', '=', name))
    #     # partner_match_domain = [] * (len(partner_match_domain) - 1) + partner_match_domain
    #     # if phone:
    #     #     partner_match_domain.append(('phone', '=', phone))
    #     # partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain
    #     if not partner_match_domain:
    #         return []
    #     domain = partner_match_domain
    #     if not include_lost:
    #         domain += ['&', ('active', '=', True), ('probability', '<', 100)]
    #     return self.env['crm.lead'].search(domain)
    #
    # @api.model
    # def lead_by_name(self, name, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     return self._by_name(name, include_lost=include_lost)
    #
    # @api.model
    # def _by_name(self, name, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     partner_match_domain = []
    #     if name:
    #         partner_match_domain.append(('name', '=', name))
    #     partner_match_domain = [] * (len(partner_match_domain) - 1) + partner_match_domain
    #     if not partner_match_domain:
    #         return []
    #     domain = partner_match_domain
    #     if not include_lost:
    #         domain += ['&', ('active', '=', True), ('probability', '<', 100)]
    #     return self.env['crm.lead'].search(domain)
    #
    # @api.model
    # def _emails_phone(self, email, phone, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     return self._by_emails_phone(email, phone, include_lost=include_lost)
    #
    # @api.model
    # def _by_emails_phone(self, email, phone, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     partner_match_domain = []
    #     for email in set(email_split(email) + [email]):
    #         partner_match_domain.append(('email_from', '=ilike', email))
    #     # if name:
    #     #     partner_match_domain.append(('name', '=', name))
    #     # partner_match_domain = [] * (len(partner_match_domain) - 1) + partner_match_domain
    #     if phone:
    #         partner_match_domain.append(('phone', '=', phone))
    #     partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain
    #     if not partner_match_domain:
    #         return []
    #     domain = partner_match_domain
    #     if not include_lost:
    #         domain += ['&', ('active', '=', True), ('probability', '<', 100)]
    #     return self.env['crm.lead'].search(domain)
    #
    # @api.model
    # def _name_phone(self, name, phone, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     return self._by_name_phone(name, phone, include_lost=include_lost)
    #
    # @api.model
    # def _by_name_phone(self, name, phone, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     partner_match_domain = []
    #     # for email in set(email_split(email) + [email]):
    #     #     partner_match_domain.append(('email_from', '=ilike', email))
    #     if name:
    #         partner_match_domain.append(('name', '=', name))
    #     partner_match_domain = [] * (len(partner_match_domain) - 1) + partner_match_domain
    #     if phone:
    #         partner_match_domain.append(('phone', '=', phone))
    #     partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain
    #     if not partner_match_domain:
    #         return []
    #     domain = partner_match_domain
    #     if not include_lost:
    #         domain += ['&', ('active', '=', True), ('probability', '<', 100)]
    #     return self.env['crm.lead'].search(domain)
    #
    # @api.model
    # def _name_email(self, name, email, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     return self._by_name_emails(name, email, include_lost=include_lost)
    #
    # @api.model
    # def _by_name_emails(self, name, email, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     partner_match_domain = []
    #     for email in set(email_split(email) + [email]):
    #         partner_match_domain.append(('email_from', '=ilike', email))
    #     if name:
    #         partner_match_domain.append(('name', '=', name))
    #     partner_match_domain = ['&'] * (len(partner_match_domain) - 1) + partner_match_domain
    #     if not partner_match_domain:
    #         return []
    #     domain = partner_match_domain
    #     if not include_lost:
    #         domain += ['&', ('active', '=', True), ('probability', '<', 100)]
    #     return self.env['crm.lead'].search(domain)
    #
    # @api.model
    # def _get_duplicated_leads(self, name, email, phone, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     return self._get_duplicated_leads_by_emails(name, email, phone, include_lost=include_lost)
    #
    # @api.model
    # def _get_duplicated_leads_by_emails(self, name, email, phone, include_lost=False):
    #     """ Search for opportunities that have the same partner and that arent done or cancelled """
    #     partner_match_domain = []
    #     for email in set(email_split(email) + [email]):
    #         partner_match_domain.append(('email_from', '=ilike', email))
    #     if name:
    #         partner_match_domain.append(('name', '=', name))
    #     partner_match_domain = ['&'] * (len(partner_match_domain) - 1) + partner_match_domain
    #     if phone:
    #         partner_match_domain.append(('phone', '=', phone))
    #     partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain
    #     if not partner_match_domain:
    #         return []
    #     domain = partner_match_domain
    #     if not include_lost:
    #         domain += ['&', ('active', '=', True), ('probability', '<', 100)]
    #     return self.env['crm.lead'].search(domain)

