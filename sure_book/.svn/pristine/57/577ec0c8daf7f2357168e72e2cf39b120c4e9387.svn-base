odoo.define('sure_book.products', function (require) {
"use strict";

var ajax = require('web.ajax');
var base = require('web_editor.base');
var core = require('web.core');
var _t = core._t;

 $(document).on("click","#check_availability",function(){
    var start_date = $('#datepicker');
    var end_date = $('#datepicker1');
    if(start_date && end_date) {
        var start = start_date.val();
        var end = end_date.val();
        ajax.jsonRpc("/property/<model("myallocator.property"):property>", 'call', {'start_date': start, 'end_date': end})
                .then(function (data) {
                    window.location.reload();
       });
    }
});
