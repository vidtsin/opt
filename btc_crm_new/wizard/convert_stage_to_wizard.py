from odoo import fields, models, tools,api, _
from odoo.exceptions import UserError, AccessError
from odoo.exceptions import UserError,ValidationError
from odoo.tools import email_re, email_split





class ConvertStageto(models.TransientModel):
    _name='convert.stage.wizard'




        
    @api.model
    def default_get(self, fields):
        """ Default get for name, opportunity_ids.
            If there is an exisitng partner link to the lead, find all existing
            opportunities links with this partner to merge all information together
        """
        result = super(ConvertStageto, self).default_get(fields)
        print result
        # context = self._context
        # print self.crm_id
        if self._context.get('active_id'):
            tomerge = {int(self._context['active_id'])}
            lead = self.env['crm.lead'].browse(self._context['active_id'])
            name = lead.name
            phone = lead.phone
            email = lead.email_from

            tomerge.update(self._get_duplicated_leads(name, email,phone, include_lost=True).ids)
            tomergelist = list(tomerge)
            temp = list(tomerge)
            for rec in temp:
                rec2 = self.env['crm.lead'].browse(rec)
                if rec2.checked == True:
                    tomergelist.remove(rec)
            if 'action' in fields and not result.get('action'):
                result['action'] = 'exist' if name else 'create'
            if 'name' in fields:
                result['name'] = name
            if 'name' in fields:
                result['name'] = 'merge' if len(tomergelist) >= 2 else 'convert'
            if 'opportunity_ids' in fields and len(tomergelist) >= 2:
                # # result['opportunity_ids'] = list(tomerge)
                # tomergelist=list(tomerge)
                # temp=list(tomerge)
                # for rec in temp:
                #     rec2 = self.env['crm.lead'].browse(rec)
                #     if rec2.checked ==  True:
                #         tomergelist.remove(rec)
                result['opportunity_ids']=tomergelist


            if lead.user_id:
                result['user_id'] = lead.user_id.id
            if lead.team_id:
                result['team_id'] = lead.team_id.id
            if not name and not lead.phone:
                result['action'] = 'nothing'
        return result

    crm_id = fields.Many2one('crm.lead','Crm Id')
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
    name = fields.Selection([
        ('convert', 'Convert to opportunity'),
        ('merge', 'Merge with existing opportunities')
    ], 'Conversion Action', required=True)



    @api.onchange('lead_name','lead_email','lead_phone')
    def _onchange_deduplicate(self):

        global ids

        if self.lead_name and self.lead_phone and self.lead_email == True:
            active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
            partner_ids = [(lead.name, lead.email_from, lead.phone) for lead in
                           active_leads]
            partners_duplicated_leads = {}
            for name, email_from, phone in partner_ids:
                duplicated_leads = (self._get_duplicated_leads(name,email_from,phone).ids)
                if len(duplicated_leads) >= 2:
                    partners_duplicated_leads.setdefault((name, email_from, phone), []).extend(duplicated_leads)

            leads_with_duplicates = []
            for duplicate in duplicated_leads:
                rec2 = self.env['crm.lead'].browse(duplicate)
                lead_tuple = (rec2.name, rec2.email_from, rec2.phone if rec2.email_from and rec2.phone and rec2.name else rec2.phone)
                if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
                    leads_with_duplicates.append(duplicate)
            tomergedup = list(leads_with_duplicates)
            tempdup = list(leads_with_duplicates)
            for rec in tempdup:
                rec2 = self.env['crm.lead'].browse(rec)
                if rec2.checked == True:
                    tomergedup.remove(rec)
            self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            ids = [id.id for id in opportunity_ids]
            self._cr.commit()

        elif self.lead_name and self.lead_email == True:
            # val ={}
            active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
            partner_ids = [(lead.name,lead.email_from) for lead in
                           active_leads]
            partners_duplicated_leads = {}
            for name, email_from in partner_ids:
                duplicated_leads = (self._name_email(name, email_from).ids)
                if len(duplicated_leads) >= 2:
                    partners_duplicated_leads.setdefault((name, email_from), []).extend(duplicated_leads)
            leads_with_duplicates = []
            for duplicate in duplicated_leads:
                rec2 = self.env['crm.lead'].browse(duplicate)
                lead_tuple = (rec2.name, rec2.email_from if rec2.name and rec2.email_from else rec2.email_from)
                if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
                    leads_with_duplicates.append(duplicate)
            tomergedup = list(leads_with_duplicates)
            tempdup = list(leads_with_duplicates)
            for rec in tempdup:
                rec2 = self.env['crm.lead'].browse(rec)
                if rec2.checked == True:
                    tomergedup.remove(rec)

            # val= leads_with_duplicates
            # return {'opportunity_ids':val}
            # self.write({'opportunity_ids': (6, 0, leads_with_duplicates), })
            # self._cr.commit()
            # user_rel_id=(4,leads_with_duplicates)
            # self.write({'opportunity_ids':  user_rel_id})
            self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            ids=[id.id for id in opportunity_ids]
            self._cr.commit()
        elif self.lead_name and self.lead_phone == True:
            # values = {}
            active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
            partner_ids = [(lead.name, lead.phone) for lead in
                           active_leads]
            partners_duplicated_leads = {}
            for name, phone in partner_ids:
                duplicated_leads = (self._name_phone(name, phone).ids)
                if len(duplicated_leads) >= 2:
                    partners_duplicated_leads.setdefault((name, phone), []).extend(duplicated_leads)

            leads_with_duplicates = []
            for duplicate in duplicated_leads:
                rec2 = self.env['crm.lead'].browse(duplicate)
                lead_tuple = (rec2.name, rec2.phone if rec2.name and rec2.phone else rec2.phone)
                if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
                    leads_with_duplicates.append(duplicate)
            tomergedup = list(leads_with_duplicates)
            tempdup = list(leads_with_duplicates)
            for rec in tempdup:
                rec2 = self.env['crm.lead'].browse(rec)
                if rec2.checked == True:
                    tomergedup.remove(rec)

            # val= leads_with_duplicates
            # return {'opportunity_ids':val}
            # self.write({'opportunity_ids': (6, 0, leads_with_duplicates), })
            # self._cr.commit()
            # user_rel_id=(4,leads_with_duplicates)
            # self.write({'opportunity_ids':  user_rel_id})
            self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            ids = [id.id for id in opportunity_ids]
            self._cr.commit()

        elif self.lead_email and self.lead_phone == True:
            active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
            partner_ids = [(lead.email_from, lead.phone) for lead in
                           active_leads]
            partners_duplicated_leads = {}
            for email_from, phone in partner_ids:
                duplicated_leads = (self._emails_phone(email_from, phone).ids)
                if len(duplicated_leads) >= 2:
                    partners_duplicated_leads.setdefault((email_from, phone), []).extend(duplicated_leads)

            leads_with_duplicates = []
            for duplicate in duplicated_leads:
                rec2 = self.env['crm.lead'].browse(duplicate)
                lead_tuple = (rec2.email_from, rec2.phone if rec2.email_from and rec2.phone else rec2.phone)
                if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
                    leads_with_duplicates.append(duplicate)

            tomergedup = list(leads_with_duplicates)
            tempdup = list(leads_with_duplicates)
            for rec in tempdup:
                rec2 = self.env['crm.lead'].browse(rec)
                if rec2.checked == True:
                    tomergedup.remove(rec)

            # val= leads_with_duplicates
            # return {'opportunity_ids':val}
            # self.write({'opportunity_ids': (6, 0, leads_with_duplicates), })
            # self._cr.commit()
            # user_rel_id=(4,leads_with_duplicates)
            # self.write({'opportunity_ids':  user_rel_id})
            self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            ids = [id.id for id in opportunity_ids]
            self._cr.commit()
        elif self.lead_name == True:
            active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
            partner_ids = [(lead.name) for lead in
                           active_leads]
            partners_duplicated_leads = {}
            for name in partner_ids:
                duplicated_leads = (self.lead_by_name(name).ids)
                if len(duplicated_leads) >= 2:
                    partners_duplicated_leads.setdefault((name), []).extend(duplicated_leads)

            leads_with_duplicates = []
            for duplicate in duplicated_leads:
                rec2 = self.env['crm.lead'].browse(duplicate)
                lead_tuple = (rec2.name)
                if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
                    leads_with_duplicates.append(duplicate)
            tomergedup = list(leads_with_duplicates)
            tempdup = list(leads_with_duplicates)
            for rec in tempdup:
                rec2 = self.env['crm.lead'].browse(rec)
                if rec2.checked == True:
                    tomergedup.remove(rec)
            self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            ids = [id.id for id in opportunity_ids]
            self._cr.commit()
        elif self.lead_email == True:
            active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
            partner_ids = [(lead.email_from) for lead in
                           active_leads]
            partners_duplicated_leads = {}
            for email_from in partner_ids:
                duplicated_leads = (self.lead_by_email(email_from).ids)
                if len(duplicated_leads) >= 2:
                    partners_duplicated_leads.setdefault((email_from), []).extend(duplicated_leads)

            leads_with_duplicates = []
            for duplicate in duplicated_leads:
                rec2 = self.env['crm.lead'].browse(duplicate)
                lead_tuple = (rec2.email_from)
                if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
                    leads_with_duplicates.append(duplicate)
            tomergedup = list(leads_with_duplicates)
            tempdup = list(leads_with_duplicates)
            for rec in tempdup:
                rec2 = self.env['crm.lead'].browse(rec)
                if rec2.checked == True:
                    tomergedup.remove(rec)
            self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            ids = [id.id for id in opportunity_ids]
            self._cr.commit()
        elif self.lead_phone == True:
            active_leads = self.env['crm.lead'].browse(self._context['active_ids'])
            partner_ids = [(lead.phone) for lead in
                           active_leads]
            partners_duplicated_leads = {}
            for phone in partner_ids:
                duplicated_leads = (self.lead_by_phone(phone).ids)
                if len(duplicated_leads) >= 2:
                    partners_duplicated_leads.setdefault((phone), []).extend(duplicated_leads)

            leads_with_duplicates = []
            for duplicate in duplicated_leads:
                rec2 = self.env['crm.lead'].browse(duplicate)
                lead_tuple = (rec2.phone)
                if len(partners_duplicated_leads.get(lead_tuple, [])) >= 2:
                    leads_with_duplicates.append(duplicate)
            tomergedup = list(leads_with_duplicates)
            tempdup = list(leads_with_duplicates)
            for rec in tempdup:
                rec2 = self.env['crm.lead'].browse(rec)
                if rec2.checked == True:
                    tomergedup.remove(rec)
            self.opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            opportunity_ids = self.env['crm.lead'].browse(tomergedup)
            ids = [id.id for id in opportunity_ids]
            self._cr.commit()

    @api.model
    def lead_by_phone(self, phone, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        return self._by_phone(phone, include_lost=include_lost)

    @api.model
    def _by_phone(self, phone, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        partner_match_domain = []
        # for email in set(email_split(email) + [email]):
        #     partner_match_domain.append(('email_from', '=ilike', email))
        # if name:
        #     partner_match_domain.append(('name', '=', name))
        # partner_match_domain = [] * (len(partner_match_domain) - 1) + partner_match_domain
        if phone:
            partner_match_domain.append(('phone', '=', phone))
        partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain
        if not partner_match_domain:
            return []
        domain = partner_match_domain
        if not include_lost:
            domain += ['&', ('active', '=', True), ('probability', '<', 100)]
        return self.env['crm.lead'].search(domain)
    @api.model
    def lead_by_email(self, email, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        return self._by_email(email, include_lost=include_lost)

    @api.model
    def _by_email(self, email, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        partner_match_domain = []
        for email in set(email_split(email) + [email]):
            partner_match_domain.append(('email_from', '=ilike', email))
        # if name:
        #     partner_match_domain.append(('name', '=', name))
        # partner_match_domain = [] * (len(partner_match_domain) - 1) + partner_match_domain
        # if phone:
        #     partner_match_domain.append(('phone', '=', phone))
        # partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain
        if not partner_match_domain:
            return []
        domain = partner_match_domain
        if not include_lost:
            domain += ['&', ('active', '=', True), ('probability', '<', 100)]
        return self.env['crm.lead'].search(domain)

    @api.model
    def lead_by_name(self, name, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        return self._by_name(name, include_lost=include_lost)

    @api.model
    def _by_name(self, name,  include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        partner_match_domain = []
        # for email in set(email_split(email) + [email]):
        #     partner_match_domain.append(('email_from', '=ilike', email))
        if name:
            partner_match_domain.append(('name', '=', name))
        partner_match_domain = [] * (len(partner_match_domain) - 1) + partner_match_domain
        # if phone:
        #     partner_match_domain.append(('phone', '=', phone))
        # partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain
        if not partner_match_domain:
            return []
        domain = partner_match_domain
        if not include_lost:
            domain += ['&', ('active', '=', True), ('probability', '<', 100)]
        return self.env['crm.lead'].search(domain)

    @api.model
    def _emails_phone(self, email, phone, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        return self._by_emails_phone(email, phone, include_lost=include_lost)

    @api.model
    def _by_emails_phone(self, email, phone, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        partner_match_domain = []
        for email in set(email_split(email) + [email]):
            partner_match_domain.append(('email_from', '=ilike', email))
        # if name:
        #     partner_match_domain.append(('name', '=', name))
        # partner_match_domain = [] * (len(partner_match_domain) - 1) + partner_match_domain
        if phone:
            partner_match_domain.append(('phone', '=', phone))
        partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain
        if not partner_match_domain:
            return []
        domain = partner_match_domain
        if not include_lost:
            domain += ['&', ('active', '=', True), ('probability', '<', 100)]
        return self.env['crm.lead'].search(domain)



    @api.model
    def _name_phone(self, name, phone, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        return self._by_name_phone(name, phone, include_lost=include_lost)

    @api.model
    def _by_name_phone(self, name, phone, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        partner_match_domain = []
        # for email in set(email_split(email) + [email]):
        #     partner_match_domain.append(('email_from', '=ilike', email))
        if name:
            partner_match_domain.append(('name', '=', name))
        partner_match_domain = [] * (len(partner_match_domain) - 1) + partner_match_domain
        if phone:
            partner_match_domain.append(('phone', '=', phone))
        partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain
        if not partner_match_domain:
            return []
        domain = partner_match_domain
        if not include_lost:
            domain += ['&', ('active', '=', True), ('probability', '<', 100)]
        return self.env['crm.lead'].search(domain)

    @api.model
    def _name_email(self, name, email,include_lost=False):
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





    @api.model
    def _get_duplicated_leads(self, name, email,phone, include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        return self._get_duplicated_leads_by_emails(name, email,phone, include_lost=include_lost)

    @api.model
    def _get_duplicated_leads_by_emails(self, name, email,phone,include_lost=False):
        """ Search for opportunities that have the same partner and that arent done or cancelled """
        partner_match_domain = []
        for email in set(email_split(email) + [email]):
            partner_match_domain.append(('email_from', '=ilike', email))
        if name:
            partner_match_domain.append(('name', '=', name))
        partner_match_domain = ['&'] * (len(partner_match_domain) - 1) + partner_match_domain
        if phone:
            partner_match_domain.append(('phone', '=', phone))
        partner_match_domain = ['&'] * (len(partner_match_domain) - 3) + partner_match_domain
        if not partner_match_domain:
            return []
        domain = partner_match_domain
        if not include_lost:
            domain += ['&', ('active', '=', True), ('probability', '<', 100)]
        res = self.env['crm.lead'].search(domain)
        print ("---------------", res)
        return self.env['crm.lead'].search(domain)



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


    @api.multi
    def action_apply(self):
        """ Convert lead to opportunity or merge lead and opportunity and open
            the freshly created opportunity view.
        """
        # global ids
        self.ensure_one()
        values = {
            'team_id': self.team_id.id,
        }
        # ids = [id.id for id in self.opportunity_ids]

        # if partner_id:
        #     values['partner_id'] = partner_id
        if self.lead_name and self.lead_phone and self.lead_email != True:
            data=ids
            self.opportunity_ids = data
        if self.name == 'merge':
            # leads = self.opportunity_ids.with_context(con_opp_merge=True).merge_opportunity()
            for rec in self._context.get('active_ids', []):
                # if rec:
                rec2 = self.env['crm.lead'].browse(rec)
                for p in rec2:
                    p2=p.id
                    # self.opportunity_ids=data


                    # value1={
                    #     'crm_lead_id':self.opportunity_ids.id,
                    #     'crm_lead':p.id
                    # }

                    mergedid = self.env['merged.crm.leads'].create(
                         {'crm_lead_id':self.opportunity_ids[-1].id, 'crm_lead':p2})

                    # merge_id=self.env['merged.crm.leads'].create(value1)
            leads = self.opportunity_ids.with_context(con_opp_merge=True).merge_opportunity_2()
            if leads.type == "lead":
                values.update({'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
                self.with_context(active_ids=leads.ids)._convert_opportunity(values)
            elif not self._context.get('no_force_assignation') or not leads.user_id:
                values['user_id'] = self.user_id.id
                leads.write(values)





        if self.convert_stage == "Opportunity" and self.name =='convert':
            print "call wizard fucntion"
            wizard_form = self.env.ref('crm_lead_website_integration.lead_to_oppor_wizard_form', False)
            view_id = self.env['lead.opportunity.wizard']
            vals = {
                'crm_id': self.crm_id.id,
            }
            new = view_id.create(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'lead.opportunity.wizard',
                'res_id': new.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new'
            }
        if self.convert_stage == "Delayed" and self.name =='convert':
            wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Delayed')])
            vals = {
                'type': 'opportunity',
                'stage_id': view_id.id,
                'date_conversion': fields.Datetime.now(),
            }
            new = self.crm_id.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.crm_id.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }
        if self.convert_stage == "Dead" and self.name =='convert':
            wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Dead')])
            vals = {
                'type': 'opportunity',
                'stage_id': view_id.id,
                'date_conversion': fields.Datetime.now(),
            }
            new = self.crm_id.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.crm_id.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }

        return leads[0].redirect_opportunity_view()



    # @api.multi
    # def _opportunity(self):
    #     if self.convert_stage == "Opporortunity":
    #         print "call wizard fucntion"
    #         wizard_form = self.env.ref('crm_lead_website_integration.lead_to_oppor_wizard_form', False)
    #         view_id = self.env['lead.opportunity.wizard']
    #         vals = {
    #             'crm_id': self.crm_id.id,
    #         }
    #         new = view_id.create(vals)
    #
    #
    #         return {
    #             'name': _('Convert Stage'),
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'lead.opportunity.wizard',
    #             'res_id': new.id,
    #             'view_id': wizard_form.id,
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'target': 'new'
    #         }
    #     if self.convert_stage == "Delayed":
    #         wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
    #         view_id = self.env['crm.stage'].search([('name', '=', 'Delayed')])
    #         vals = {
    #             'type': 'opportunity',
    #             'stage_id': view_id.id
    #         }
    #         new = self.crm_id.write(vals)
    #         return {
    #             'name': _('Convert Stage'),
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'crm.lead',
    #             'res_id': self.crm_id.id,
    #             'view_id': wizard_form.id,
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'target': 'current'
    #         }
    #     if self.convert_stage == "Dead":
    #         wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
    #         view_id = self.env['crm.stage'].search([('name', '=', 'Dead')])
    #         vals = {
    #             'type': 'opportunity',
    #             'stage_id': view_id.id
    #         }
    #         new = self.crm_id.write(vals)
    #         return {
    #             'name': _('Convert Stage'),
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'crm.lead',
    #             'res_id': self.crm_id.id,
    #             'view_id': wizard_form.id,
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'target': 'current'
    #         }


class ConvertStage2to(models.TransientModel):
    _name = 'convert.stage2.wizard'

    crm_id = fields.Many2one('crm.lead', 'Crm Id')

    convert_stage_2 = fields.Selection([('Prospect', 'Prospect'),
                                      ('Delayed', 'Delayed'),
                                      ('Lost', 'Lost')],
                                     string='Convert Stage')


    @api.multi
    def prospect(self):
        if self.convert_stage_2 == "Prospect":
            print "call wizard fucntion"
            wizard_form = self.env.ref('crm_lead_website_integration.oppor_to_prospect_wizard_form', False)
            view_id = self.env['opportunity.prospect.wizard']
            # view_id1 = self.env['other.requirement'].search([('name', '=', self.name)])
            vals = {
                # 'rel_checkbox_other': view_id1,
                'crm_id': self.crm_id.id,
                'stage': self.convert_stage_2
            }
            new = view_id.create(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'opportunity.prospect.wizard',
                'res_id': new.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new'
            }
        if self.convert_stage_2 == 'Delayed':
            print "call wizard fucntion"
            wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Delayed')])
            vals = {
                'stage_id': view_id.id
            }
            new = self.crm_id.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.crm_id.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }
        elif self.convert_stage_2 == 'Lost':
            wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Lost')])
            vals = {
                'stage_id': view_id.id
            }
            new = self.crm_id.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.crm_id.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }

class ConvertStage3to(models.TransientModel):
    _name = 'convert.stage3.wizard'

    crm_id = fields.Many2one('crm.lead', 'Crm Id')
    convert_stage_3 = fields.Selection([('Admitted', 'Admitted'),
                                        ('Delayed', 'Delayed'),
                                        ('Lost', 'Lost')],
                                       string='Convert Stage')


    @api.multi
    def admitted(self):
        if self.convert_stage_3 == "Admitted":
            print "call wizard fucntion"
            wizard_form = self.env.ref('crm_lead_website_integration.prospect_to_admitted_wizard_form', False)
            view_id = self.env['prospect.admitted.wizard']
            vals = {
                'crm_id': self.crm_id.id,
                'stage': self.convert_stage_3
            }
            new = view_id.create(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model':'prospect.admitted.wizard',
                'res_id': new.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new'
            }
        if self.convert_stage_3 == 'Delayed':
            print "call wizard fucntion"
            wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Delayed')])
            vals = {
                'stage_id': view_id.id
            }
            new = self.crm_id.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.crm_id.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }
        elif self.convert_stage_3 == 'Lost':
            wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Lost')])
            vals = {
                'stage_id': view_id.id
            }
            new = self.crm_id.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.crm_id.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }


class ConvertStage4to(models.TransientModel):
    _name = 'convert.stage4.wizard'

    crm_id = fields.Many2one('crm.lead', 'Crm Id')
    convert_stage_4 = fields.Selection([('Enrolled', 'Enrolled'),
                                        ('Delayed', 'Delayed'),
                                        ('Lost', 'Lost')],
                                       string='Convert Stage')

    @api.multi
    def enrolled(self):
        if self.convert_stage_4 == "Enrolled":
            print "call wizard fucntion"
            wizard_form = self.env.ref('crm_lead_website_integration.admitted_to_enrolled_wizard_form', False)
            view_id = self.env['admitted.enrolled.wizard']
            vals = {
                'crm_id': self.crm_id.id,
                'stage': self.convert_stage_4
            }
            new = view_id.create(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'admitted.enrolled.wizard',
                'res_id': new.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new'
            }
        if self.convert_stage_4 == 'Delayed':
            print "call wizard fucntion"
            wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Delayed')])
            vals = {
                'stage_id': view_id.id
            }
            new = self.crm_id.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.crm_id.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }
        elif self.convert_stage_4 == 'Lost':
            wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Lost')])
            vals = {
                'stage_id': view_id.id
            }
            new = self.crm_id.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.crm_id.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }


class ConvertStage5to(models.TransientModel):
    _name = 'convert.stage5.wizard'

    crm_id = fields.Many2one('crm.lead', 'Crm Id')
    current_stage = fields.Char("Current Stage")
    convert_stage_5 = fields.Selection([('Delayed', 'Delayed'),
                                        ('Lost', 'Lost')],
                                       string='Convert Stage')


    @api.multi
    def open_lost(self):
        if self.convert_stage_5 == 'Delayed':
            print "call wizard fucntion"
            wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Delayed')])
            vals = {
                'stage_id': view_id.id
            }
            new = self.crm_id.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.crm_id.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }
        elif self.convert_stage_5 =='Lost':
            wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
            view_id = self.env['crm.stage'].search([('name', '=', 'Lost')])
            vals = {
                'stage_id': view_id.id
            }
            new = self.crm_id.write(vals)
            return {
                'name': _('Convert Stage'),
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.crm_id.id,
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current'
            }




# class OtherRequirement(models.TransientModel):
#     _name = 'other.requirement'
#
#     name = fields.Char(string='Name')




class LeadOpportunityWizard(models.TransientModel):
    _name = 'lead.opportunity.wizard'

    crm_id = fields.Many2one('crm.lead', 'Crm Id')

    rel_academic_requirements = fields.Boolean(related='crm_id.academic_requirements')
    rel_assessment_test = fields.Boolean(related='crm_id.assessment_test')
    rel_seat_deposit = fields.Boolean(related='crm_id.seat_deposit')

    rel_other_requirements = fields.Many2one('other.requirement', related='crm_id.other_requirements', string='Other Requirement')
    rel_checkbox_other = fields.Boolean(related='crm_id.checkbox')

    @api.multi
    def open_opportunity(self):
        print "call wizard fucntion"
        wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
        view_id = self.env['crm.lead']
        vals = {
            # 'checkbox_other': self.other_requirements.name,
            'type': 'opportunity',
            'date_conversion': fields.Datetime.now(),

        }
        new = self.crm_id.write(vals)
        return {
            'name': _('Convert Stage'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': self.crm_id.id,
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current'
        }

class LeadOpportunityWizard(models.TransientModel):
    _name = 'opportunity.prospect.wizard'

    crm_id = fields.Many2one('crm.lead', 'Crm Id')
    rel_academic_requirements = fields.Boolean(related='crm_id.academic_requirements')
    rel_assessment_test = fields.Boolean(related='crm_id.assessment_test')
    rel_seat_deposit = fields.Boolean(related='crm_id.seat_deposit')
    rel_other_requirements = fields.Many2one('other.requirement', related='crm_id.other_requirements',
                                             string='Other Requirement')
    rel_checkbox_other = fields.Boolean(related='crm_id.checkbox')
    stage = fields.Char('Stage')
    @api.multi
    def open_prospect(self):
        print "call wizard fucntion"
        wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
        view_id = self.env['crm.stage'].search([('name', '=', self.stage)])
        vals = {
            'stage_id': view_id.id
        }
        new = self.crm_id.write(vals)
        return {
            'name': _('Convert Stage'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': self.crm_id.id,
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current'
        }

class ProspectAdmittedWizard(models.TransientModel):
    _name = 'prospect.admitted.wizard'

    crm_id = fields.Many2one('crm.lead', 'Crm Id')
    rel_supp_academic_document = fields.Boolean(related='crm_id.support_academic_document')
    rel_assessment_test_completed = fields.Boolean(related='crm_id.assessment_test_completed')
    rel_seat_deposit_collected = fields.Boolean(related='crm_id.seat_deposit_completed')
    rel_amount_collected = fields.Float(related='crm_id.seat_deposit_amount')
    rel_method_payment = fields.Char(related='crm_id.method_of_payment')

    stage = fields.Char('Stage')

    @api.multi
    def open_admitted(self):
        print "call wizard fucntion"
        wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
        view_id = self.env['crm.stage'].search([('name', '=', self.stage)])
        vals = {
            'stage_id': view_id.id
        }
        new = self.crm_id.write(vals)
        return {
            'name': _('Convert Stage'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': self.crm_id.id,
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current'
        }

class AdmittedEnrolledWizard(models.TransientModel):
    _name = 'admitted.enrolled.wizard'

    crm_id = fields.Many2one('crm.lead', 'Crm Id')
    rel_financial_aid_approved = fields.Boolean(related='crm_id.financial_aid_provided')
    rel_payment_plan = fields.Boolean(related='crm_id.payment_plan')
    rel_police_clearance = fields.Boolean(related='crm_id.police_clearance')
    rel_health_immunization_record = fields.Boolean(related='crm_id.health_immunization_record')
    rel_agreement_signed = fields.Boolean(related='crm_id.agreement_signed')
    stage = fields.Char('Stage')

    @api.multi
    def open_enrolled(self):
        print "call wizard fucntion"
        wizard_form = self.env.ref('crm.crm_case_form_view_oppor', False)
        view_id = self.env['crm.stage'].search([('name', '=', self.stage)])
        vals = {
            'stage_id': view_id.id
        }
        new = self.crm_id.write(vals)
        return {
            'name': _('Convert Stage'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': self.crm_id.id,
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current'
        }
class EmailSend(models.TransientModel):
    _name = 'email.send'

    recipents = fields.Char(string="Recipents")
    subject = fields.Char(string="subject")
    body = fields.Html('Contents')

    @api.model
    def default_get(self, fields):
        result = super(EmailSend, self).default_get(fields)
        context = self._context
        obj = self.env['crm.lead']
        t = context.get('active_ids')
        brws = obj.browse(t)
        for brr in brws:
            result.update({'recipents': brws.email_from})
        return result

    @api.multi
    def send_mail(self):
            mail_values = {
                'subject': self.subject,
                'body_html':self.body,
                'email_to': self.recipents,

            }
            create_and_send_email = self.env['mail.mail'].create(mail_values).send()




