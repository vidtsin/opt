odoo.define('sure_book.dashboard', function (require) {
"use strict";

var ajax = require('web.ajax');
var core = require('web.core');
var data_manager = require('web.data_manager');
var formats = require('web.formats');
var Model = require('web.Model');
var time = require('web.time');
var View = require('web.View');
var form_common = require('web.form_common');
var Dialog = require('web.Dialog');
var Widget = require('web.Widget');

var _t = core._t;
var _lt = core._lt;
var QWeb = core.qweb;
    

    var DashboardHomePage = Widget.extend({
        start: function() {
            var so_products = new DashboardWidget(this, ["cpu", "mouse", "keyboard", "graphic card", "screen"], "#00FF00");
            so_products.appendTo(this.$el);
        },
    });
    
    
    var DashboardWidget = Widget.extend({
        
        load_data: function() {
            var sale_order = new Model('sale.order');
            
            sale_order.call('action_arrival').then(function (list_arrive) { 
            $.each( list_arrive, function( key, value ) {
                var id = value.id;
                if(value.state == 'Checked-In'){
                    var btn = '<button type="button"  class="btn btn-info btn-xs disabled">Checked in</button>';
                }else {
                    var btn = '<button type="button" onclick="checkin('+value.id+');" class="btn btn-info btn-xs check_in">Check in</button>';
                }
                $('#arrival_data').append('<tr ><td>'+value.partner_id+'</td><td>'+value.name+'</td><td>'+value.state+'</td><td >'+btn+'</td></tr>');
            });
            });
           
           
            var arrival_count = sale_order.call('action_arrival_count').then(function (arrive_count) { 
                $('#arrival_count').text(arrive_count);
//                $('#ac').find('span').text(parseInt(arrive_count));
            });
            
            
            var departure_data = sale_order.call('action_departure').then(function (list_depart) { 
            $.each( list_depart, function( key, value ) {
                var id = value.id;
                if(value.state == 'Check-Out'){
                    var btn = '<button type="button"  class="btn btn-info btn-xs disabled">Checked Out</button>';
                }else {
                    var btn = '<button type="button" onclick="checkout('+value.id+');" class="btn btn-info btn-xs">Check Out</button>&nbsp;<button type="button" onclick="split_bill('+value.id+');" class="btn btn-success btn-xs">Split Bill</button>';
                }
                $('#departure_data').append('<tr><td>'+value.partner_id+'</td><td>'+value.name+'</td><td>'+value.state+'</td><td>'+btn+'</td></tr>');
            });
            });

            var departure_count = sale_order.call('action_departure_count').then(function (depart_count) { 
                $('#departure_count').text(depart_count);
            });
            
            var occupied_data = sale_order.call('action_occupied').then(function (list_occupy) { 
            $.each( list_occupy, function( key, value ) {
                $('#occupied_data').append('<tr><td>'+value.partner_id+'</td><td>'+value.name+'</td><td>'+value.state+'</td></tr>');
            });
            });
            
            var occupied_count = sale_order.call('action_occupied_count').then(function (occupy_count) { 
                $('#occupied_count').text(occupy_count);
            });
            
            var customer_data = sale_order.call('compute_customer').then(function (list_customer) { 
            $.each( list_customer, function( key, value ) {
                $('#customer_data').append('<tr><td>'+value.name+'</td><td>'+value.email+'</td><td>'+value.phone+'</td></tr>');
            });
            });
            
            
            var sales_data = sale_order.call('action_sales').then(function (list_sale) { 
            $.each( list_sale, function( key, value ) {
                $('#sales_data').append('<tr><td>'+value.name+'</td><td>'+value.partner_id+'</td><td>'+value.revenue+'</td><td>'+value.check_in+'</td><td>'+value.nights+'</td></tr>');
            });
            });

            var cancel_data = sale_order.call('action_cancel_data').then(function (list_cancel) { 
            $.each( list_cancel, function( key, value ) {
                $('#cancel_data').append('<tr><td>'+value.name+'</td><td>'+value.partner_id+'</td><td>'+value.check_in+'</td></tr>');
            });
            });
            

        },
        
        
        template: "DashboardWidget",
        init: function(parent, so_products) {
            this._super(parent);
            this.so_products = so_products;
            this.id="id";
            
        },
        
        start: function(parent) {
            this._super(parent);
            var self = this;
            self.load_data();
        },
        
        
    });


    core.action_registry.add("sure_book.so_dashboard", DashboardHomePage);
    
    });