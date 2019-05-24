odoo.define('crm_lead_enhancement.sales_team_dashboard', function (require) {
"use strict";

var SalesTeamDashboardView = require('sales_team.dashboard');
var Model = require('web.Model');

SalesTeamDashboardView.include({

    events: {
        'click .o_dashboard_action_new': 'on_dashboard_action_new_clicked',
    },



    on_dashboard_action_new_clicked: function(ev){
        ev.preventDefault();
        var $action = $(ev.currentTarget);
        var action_name = $action.attr('name');
        var action_extra = $action.data('extra');
        var additional_context = {};





        // TODO: find a better way to add defaults to search view
        if (action_name === 'crm_lead_website_integration.action_your_local_pipeline') {
            if (action_extra === 'local_hot') {
                additional_context['search_default_local_hot'] = 1;
            }else if (action_extra === 'local_cold') {
                additional_context['search_default_local_cold'] = 1;
            }else if (action_extra === 'local_warm') {
                additional_context['search_default_local_warm'] = 1;
            }
            this.do_action(action_name, {additional_context: additional_context});
        }else if (action_name === 'crm_lead_website_integration.action_your_international_pipeline') {
            if (action_extra === 'international_hot') {
                additional_context['search_default_International_hot'] = 1;
            }else if (action_extra === 'international_cold') {
                additional_context['search_default_International_cold'] = 1;
            }else if (action_extra === 'international_warm') {
                additional_context['search_default_International_warm'] = 1;
            }
            this.do_action(action_name, {additional_context: additional_context});
        }
        else{
            var action_name_splited=action_name.split('_');
            console.log(action_name_splited[0]);
            console.log(action_name_splited[1]);
            if (action_name_splited[0] === 'local') {
                this.do_action({name:action_extra,views: [[false, 'list'], [parseInt(action_name_splited[1]), 'form']],view_type: 'form', view_mode: 'tree,form', res_model: 'crm.lead', type: 'ir.actions.act_window',domain: [['type', '=', 'opportunity'],['stage_id_name','=',action_extra],['team_id.name','ilike','local']]});
            }else if (action_name_splited[0] === 'international') {
            this.do_action({name:action_extra,views: [[false, 'list'], [parseInt(action_name_splited[1]), 'form']],view_type: 'form', view_mode: 'tree,form', res_model: 'crm.lead', type: 'ir.actions.act_window',domain: [['type', '=', 'opportunity'],['stage_id_name','=',action_extra],['team_id.name','ilike','international']]});
            }
        }
    },
});

});


