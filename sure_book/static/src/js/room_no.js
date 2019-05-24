odoo.define('sure_book.room_no', function (require) {
"use strict";

var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var core = require('web.core');

var QWeb = core.qweb;
var _t   = core._t;

var _super_order = models.Order.prototype;

models.Order = models.Order.extend({
    initialize: function(attr, options) {
        _super_order.initialize.call(this,attr,options);
        this.room_no = this.room_no || "";
    },
    set_room_no: function(room_no){
        this.room_no = room_no;
        console.log('<<<<<<set<<<<<<<<room_no<<<<<<<<<<<<<<'+this.room_no);
        this.trigger('change',this);
    },
    get_room_no: function(room_no){
        console.log('<<<<<<<get<<<<<<<room_no<<<<<<<<<<<<<<'+this.room_no);
        return this.room_no;
    },
    export_as_JSON: function(){
        var json = _super_order.export_as_JSON.call(this);
        json.room_no = this.room_no;
        return json;
    },
    init_from_JSON: function(json){
        _super_order.init_from_JSON.apply(this,arguments);
        this.room_no = json.room_no;
    },
});


var RoomNoButton = screens.ActionButtonWidget.extend({
    template: 'RoomNoButton',
    button_click: function(){
        var order = this.pos.get_order();
        console.log('<<<<<<<<<<<<order<<jjjjjj<<<<<<<<<<<<<<'+JSON.stringify(order))

        if (order) {
            this.gui.show_popup('textinput',{
                title: _t('Add Room No.'),
                value:   order.get_room_no(),
                confirm: function(room_no) {
                // Change Button String
                $('.roombtn').text('Room No. '+room_no);
                    order.set_room_no(room_no);
                },
            });
        }
    },

});

screens.define_action_button({
    'name': 'room_no',
    'widget': RoomNoButton,
    'condition': function(){
        return this.pos.config.iface_room_no;
    },
});


screens.ReceiptScreenWidget.include({
    renderElement: function() {
        var self = this;
        this._super();
        this.$('.next').click(function(){
            if (!self._locked) {
                self.click_next();
                $('.roombtn').text('Room No. ');  //Clear button String
                console.log('<<<<<<<<<<<<<<<<inherit<<<<<<<<<<<<<<<<<')
            }
        });

    },

});



});





//odoo.define('sure_book.models_check', function (require) {
//"use strict";
//
//var utils = require('web.utils');
//var models = require('point_of_sale.models');
//var db = require('point_of_sale.DB');
//var round_pr = utils.round_precision;
//var Backbone = window.Backbone;
//
//    console.log('====inherited==========');
//
//    models.load_models({
//        model:  'res.partner',
//        fields: ['name','room_no','street','city','state_id','country_id','vat','phone','zip','mobile','email','barcode','write_date','property_account_position_id'],
//        domain: [['customer','=',true],['check_in','=',true]], 
//        loaded: function(self,partners){
//            self.partners = partners;
//            console.log('====inherited===1234=======');
//            self.db.add_partners(partners);
//        },
//
//
//});
//
//models.PosModel.include({
//    
//    
//    load_new_partners: function(){
//        var self = this;
//        this._super();
//        console.log('====self=========='+self);
//        var def  = new $.Deferred();
//        var fields = _.find(this.models,function(model){ return model.model === 'res.partner'; }).fields;
//        new Model('res.partner')
//            .query(fields)
//            .filter([['customer','=',true],['check_in','=',true],['write_date','>',this.db.get_partner_write_date()]])
//            .all({'timeout':3000, 'shadow': true})
//            .then(function(partners){
//                if (self.db.add_partners(partners)) {   // check if the partners we got were real updates
//                    def.resolve();
//                } else {
//                    def.reject();
//                }
//            }, function(err,event){ event.preventDefault(); def.reject(); });    
////        return def._super();
//        return def;
//    },
//});   
//    
//
//
//});



