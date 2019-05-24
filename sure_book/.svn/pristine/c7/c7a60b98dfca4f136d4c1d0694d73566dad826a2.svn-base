odoo.define('sure_book.scheduler', function (require) {
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


    var SchedulerHomePage = Widget.extend({
        start: function() {
            ajax.loadJS('/sure_book/static/js/jquery/jquery-1.9.1.min.js');
            var products = new SchedulerWidget(
                this, ["cpu", "mouse", "keyboard", "graphic card", "screen"], "#00FF00");
            products.appendTo(this.$el);
        },
    });

    var SchedulerWidget = Widget.extend({
        events: {
            "click .trigger_button": "button_clicked",
        },

        load_scheduler: function() {
            var self = this;
            $(document).ready(function(){
                    var nav = new DayPilot.Navigator("nav");
                    nav.selectMode = "month";
                    nav.showMonths = 4;
                    nav.skipMonths = 4;
                    nav.onTimeRangeSelected = function(args) {
                        loadTimeline(args.start);
                        loadEvents();
                    };
                    nav.init();

                    $("#timerange").change(function() {
                        switch (this.value) {
                            case "week":
                                dp.days = 7;
                                nav.selectMode = "Week";
                                nav.select(nav.selectionDay);
                                break;
                            case "month":
                                dp.days = dp.startDate.daysInMonth();
                                nav.selectMode = "Month";
                                nav.select(nav.selectionDay);
                                break;
                        }
                    });
		    $("#autocellwidth").click(function() {
                        dp.cellWidth = 40;  // reset for "Fixed" mode
                        dp.cellWidthSpec = $(this).is(":checked") ? "Auto" : "Fixed";
                        dp.update();
                    });	



                    var dp = new DayPilot.Scheduler("dp");

                    dp.allowEventOverlap = false;
                    dp.treeEnabled = true;
                    dp.treePreventParentUsage = true;
                    dp.hourFontSize = "25px";
                    dp.heightSpec = "Max";
                    dp.height = "100%";	

                    //dp.startDate = new DayPilot.Date().firstDayOfMonth();
                    dp.days = dp.startDate.daysInMonth();
                    loadTimeline(DayPilot.Date.today().firstDayOfMonth());

                    dp.eventDeleteHandling = "Update";

                    dp.timeHeaders = [
                        { groupBy: "Month", format: "MMMM yyyy" },
                        { groupBy: "Day", format: "d" }
                    ];

                    dp.eventHeight = 50;
                    dp.bubble = new DayPilot.Bubble({});

                    dp.rowHeaderColumns = [
                        {title: "Room", width: 80},
                        {title: "Capacity", width: 80},
                        {title: "Status", width: 80}
                    ];

                    dp.onBeforeResHeaderRender = function(args) {
                        var beds = function(count) {
                            return count;
                        };

                        args.resource.columns[0].html = beds(args.resource.capacity);
                        args.resource.columns[1].html = args.resource.status;
                        switch (args.resource.status) {
                            case "Dirty":
                                args.resource.cssClass = "status_dirty";
                                break;
                            case "Cleanup":
                                args.resource.cssClass = "status_cleanup";
                                break;
                        }

                        args.resource.areas = [{
                                    top:3,
                                    right:4,
                                    height:14,
                                    width:14,
                                    action:"JavaScript",
                                    js: function(r) {
                                        var room_context = {};
                                        room_context["default_product_id"] = parseInt(r.id);
                                        update_room_status(room_context);
                                    },
                                    v:"Hover",
                                    css:"icon icon-edit",
                                }];
                    };

                    // http://api.daypilot.org/daypilot-scheduler-oneventmoved/
                    dp.onEventMoved = function (args) {
                        var sale_order_id = args.e.id();
                        var booking_id = args.e.tag("bookingid");
                        var new_start = args.newStart.toString();
                        var new_end = args.newEnd.toString();
                        var new_room = args.newResource;

                        new_start = new_start.replace("T", " ");
                        new_end = new_end.replace("T", " ");
                        var moved_context = {};
                        moved_context["sale_order_id"] = sale_order_id;
                        moved_context["booking_id"] = booking_id;
                        moved_context["new_start"] = new_start;
                        moved_context["new_end"] = new_end;
                        moved_context["new_room"] = new_room;

                        var model = new Model("booking.info");
                        var movedData = model.call("update_sale_order_line", {context: moved_context}).then(function(result) {
                            //tasks if any, here
                        });
                        setTimeout(function () {
                                if (true) {
                                   loadEvents();
                                }
                        }, 1000);
                    };

                    // http://api.daypilot.org/daypilot-scheduler-oneventresized/
                    dp.onEventResized = function (args) {
                        var sale_order_line_id = args.e.id();
                        var booking_id = args.e.tag("bookingid");
                        var new_start_date = args.newStart.toString();
                        var new_end_date = args.newEnd.toString();

                        // stripping out T within date from Scheduler
                        new_start_date = new_start_date.replace("T", " ");
                        new_end_date = new_end_date.replace("T", " ");

                        var extend_context = {};
                        extend_context["sale_order_line_id"] = sale_order_line_id;
                        extend_context["booking_id"] = booking_id;
                        extend_context["new_start_date"] = new_start_date;
                        extend_context["new_end_date"] = new_end_date;

                        var model = new Model("booking.info");
                        var extendData = model.call("extend_booking", {context: extend_context}).then(function(result) {

                        });

                        setTimeout(function () {
                                if (true) {
                                   loadEvents();
                                }
                        }, 1000);
                    };

                    dp.onEventDeleted = function(args) {
                        var sale_order_line_id = args.e.id();
                        var booking_id = args.e.tag("bookingid");
                        var delete_context = {};
                        delete_context["sale_order_line_id"] = sale_order_line_id;
                        delete_context["booking_id"] = booking_id;

                        var model = new Model("booking.info");
                        var deleteData = model.call("unlink_booking", {context: delete_context}).then(function(result) {

                        });

                        setTimeout(function () {
                            if (true) {
                                loadEvents();
                            }
                        }, 1000);
                        
                    };

                    // event creating
                    // http://api.daypilot.org/daypilot-scheduler-ontimerangeselected/
                    dp.onTimeRangeSelected = function (args) {
                        var modal = new DayPilot.Modal();
                        modal.closed = function() {
                            dp.clearSelection();

                            // reload all events
                            var data = this.result;
                            if (data && data.result === "OK") {
                                loadEvents();
                            }
                        };
                        var self = this;
                        var room_id = args.resource;
                        var s_date = args.start.toString();
                        var e_date = args.end.toString();
                        var is_multiple = 0;
                        var create_context = {};

                        //reading multiple booking ids
                        var selected_room_ids = [];
                        var json = dp.rows.selection.get();
                        for(var i = 0; i < json.length; i++) {
                            var obj = json[i].id;
                            obj = parseInt(obj);
                            selected_room_ids.push(obj);
                        }

                        if($.isEmptyObject(json) != true) { // multi booking true
                            is_multiple = 1;
                            create_context["default_multiple_booking_ids"] = selected_room_ids;
                        } 

                        else {
                            create_context["default_product_id"] = parseInt(room_id);
                        }
                        
                        create_context["default_is_multiple"] = is_multiple;
                        create_context["default_start_date"] = s_date.replace("T", " ");
                        create_context["default_end_date"] = e_date.replace("T", " ");
                        create_booking(create_context);
                        dp.clearSelection();
                        loadEvents();
                    };

                    dp.onEventClick = function(args) {
                        var update_context = {};
                        var book_id = args.e.tag("bookingid");
                        book_id = parseInt(book_id);
                        update_booking(update_context, book_id);
                    };

                    dp.onBeforeCellRender = function(args) {
                        var dayOfWeek = args.cell.start.getDayOfWeek();
                        if (dayOfWeek === 6 || dayOfWeek === 0) {
                            args.cell.backColor = "#f8f8f8";
                        }
                    };

                    dp.onBeforeEventRender = function(args) {
                        var start = new DayPilot.Date(args.e.start);
                        var end = new DayPilot.Date(args.e.end);

                        var today = DayPilot.Date.today();
                        var now = new DayPilot.Date();

                        args.e.html = args.e.text + " (" + start.toString("M/d/yyyy") + " - " + end.toString("M/d/yyyy") + ")";

                        switch (args.e.status) {
                            case "new":
                                var in2days = today.addDays(1);

                                if (start < in2days) {
                                    args.e.barColor = 'red';
                                    args.e.toolTip = 'Expired (not confirmed in time)';
                                }
                                else {
                                    args.e.barColor = '#f9ba25';
                                    args.e.toolTip = 'New';
                                }
                                break;
                            case "Confirmed":
                                var arrivalDeadline = today.addHours(18);

                                if (start < today || (start.getDatePart() === today.getDatePart() && now > arrivalDeadline)) { // must arrive before 6 pm
                                    args.e.barColor = "#f41616";  // red
                                    args.e.toolTip = 'Late arrival';
                                }
                                else {
                                    args.e.barColor = "green";
                                    args.e.toolTip = "Confirmed";
                                }
                                break;
                            case 'checkin': // arrived
                                var checkoutDeadline = today.addHours(10);

                                if (end < today || (end.getDatePart() === today.getDatePart() && now > checkoutDeadline)) { // must checkout before 10 am
                                    args.e.barColor = "#f41616";  // red
                                    args.e.toolTip = "Late checkout";
                                }
                                else
                                {
                                    args.e.barColor = "#1691f4";  // blue
                                    args.e.toolTip = "Arrived";
                                }
                                break;
                            case 'checkout': // checked out
                                args.e.barColor = "purple";
                                args.e.toolTip = "Checked out";
                                break;
                            default:
                                args.e.toolTip = "Unexpected state";
                                break;
                        }

                        args.e.html = args.e.html + "<br /><span style='color:gray'>" + args.e.toolTip + "</span>";

                        var paid = args.e.paid;
                        var paidColor = "#aaaaaa";
                        var bookingid = args.e.bookingid;
                        args.e.areas = [
                            
                            { bottom: 10, right: 4, html: "<div style='color:" + paidColor + "; font-size: 8pt;'>Paid: " + paid + "%</div>", v: "Invisible"},
                            { left: 4, bottom: 8, right: 4, height: 2, html: "<div style='background-color:" + paidColor + "; height: 100%; width:" + paid + "%'></div>", v: "Invisible" }
                            
                        ];

                    };

                    dp.onRowClicked = function(args) {

                        var room_variants =  dp.rows.find(args.row.id).children();
                        var selection_pool = dp.rows.selection.get();
                        var count_children_in_selection_pool = 0;
                        if (room_variants === undefined || room_variants.length == 0) { // No Children
                            toggleSingleRowSelection(args.row);
                        } else { // Has Children

                                // calculate the count of room_variants already in selection_pool
                                for (var i = 0; i < room_variants.length; i++){
                                    var child_row = room_variants[i];

                                    for (var j = 0; j < selection_pool.length; j++){
                                        var selection_pool_row = selection_pool[j];
                                        if (JSON.stringify(child_row) === JSON.stringify(selection_pool_row)) {
                                            count_children_in_selection_pool++;
                                            break;
                                        }

                                    }

                                }

                                if (count_children_in_selection_pool == room_variants.length) {
                                    // All children (variants) are within the selection_pool
                                    // Remove all children and clear parent class
                                    for (var i = 0; i < room_variants.length; i++){
                                        var child_row_to_remove = room_variants[i];
                                            dp.rows.selection.remove(child_row_to_remove);
                                    }
                                    args.row.removeClass("scheduler_default_rowheader_selected");
                                } else {
                                    // Some or No children within selection_pool
                                    // Add remaining children
                                    // Set parent class
                                    for (var i = 0; i < room_variants.length; i++){
                                        var child_row_to_add = room_variants[i];
                                        if (!dp.rows.selection.isSelected(child_row_to_add)) {
                                            dp.rows.selection.add(child_row_to_add);
                                        } 
                                    }
                                    args.row.addClass("scheduler_default_rowheader_selected");
                                }
                        }
                    }

                    function toggleSingleRowSelection(row) {
                        if (dp.rows.selection.isSelected(row)) {
                            dp.rows.selection.remove(row);
                            // Fix to remove selection of parent resource if child is unselected
                            var parent = dp.rows.find(row.id).parent();
                            if(parent != null){
                                parent.removeClass("scheduler_default_rowheader_selected");
                            }
                        } else {
                            dp.rows.selection.add(row);
                        }
                    }

                    function toggleMultiRowSelection(row,variants) {
                        if (dp.rows.selection.isSelected(row)) {
                            dp.rows.selection.remove(row);
                            dp.rows.selection.remove(variants);
                        } else {
                            dp.rows.selection.add(row);
                            dp.rows.selection.add(variants);
                        }
                    }

			dp.cellWidth = 40;  // reset for "Fixed" mode
                        dp.cellWidthSpec = "Auto";

                   	dp.init();

                    loadResources();
                    loadEvents();

                    function loadTimeline(date) {
                        dp.scale = "Manual";
                        dp.timeline = [];
                        // var start = date.getDatePart().addHours(12);
                        var start = date.getDatePart();

                        for (var i = 0; i < dp.days; i++) {
                            dp.timeline.push({start: start.addDays(i), end: start.addDays(i+1)});
                        }
                        dp.update();
                    }

                    function loadEvents() {
                        var start = dp.visibleStart();
                        var end = dp.visibleEnd();
                        var date_context = {};
                        date_context["start_date"] = start;
                        date_context["end_date"] = end;
                        var model = new Model("scheduler.booking");
                        var bookingdata = model.call("fetch_order_line", {context: date_context}).then(function(result) {
                        dp.events.list = result;
                        dp.update();
                        });
                    }

                    function loadResources() {
                        var resource_context = {};
                        resource_context["capacity"] = parseInt($("#filter").val());
                        var model = new Model("scheduler.booking");
                        var roomdata = model.call("get_products", {context: resource_context}).then(function(result) {
                            dp.resources = result;
                            dp.update();
                        });

                    }


                    /**
                     * Dialog to create a task.
                     */

                    function create_booking(context) {
                        var self = this;
                        new form_common.FormViewDialog(this, {
                            res_model: "booking.info",
                            context: context,
                            title: _t("Create New Booking"),
                            buttons: [
                                {text: _lt("Close"), classes: 'btn-default right', close: true, click: function () {
                                    dp.rows.selection.clear();
                                    loadEvents();
                                }},
                            ]
                        }).open();

                    }

                    /**
                     * Dialog to edit a task.
                     */

                    function update_booking(context, book_id) {
                        var self = this;
                        new form_common.FormViewDialog(this, {
                            res_model: "booking.info",
                            res_id: book_id,
                            context: context,
                            title: _t("Update Booking"),
                            buttons: [
                                {text: _lt("Close"), classes: 'btn-default right', close: true, click: function () {
                                    loadEvents();
                                }},
                                {text: _lt("Make Payment"), classes: 'btn btn-sm btn-primary btn-default right', close: true, click: function () {
                                    global_self.do_make_payment();

                                }},
                            ]
                        }).open();

                    }


                    /**
                     * Dialog to edit room data.
                     */

                    function update_room_status(context) {
                        var self = this;
                        new form_common.FormViewDialog(this, {  
                            res_model: "room.status.change",
                            context: context,
                            title: _t("Update Room Status"),
                            buttons: [
                                {text: _lt("Close"), classes: 'btn-default right', close: true, click: function () {
                                    loadResources();
                                    loadEvents();
                                }}
                            ]
                        }).open();

                    }

                    $(document).ready(function() {
                        $("#filter").change(function() {
                            loadResources();
                        });
                    });
          });
        var global_self = this;
        },

        do_make_payment: function() {
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: "account.payment",
                views: [[false, 'form']],
                target: 'new',
                context: {},
            });
        },

        template: "SchedulerWidget",
        init: function(parent, products, color) {
            this._super(parent);
            this.products = products;
            this.color = color;
            this.id="id";
        },

        start: function(parent) {
            this._super(parent);
            var self = this;
            setTimeout(function () {
                if (true) {
                    self.$el.find("div.scheduler-control").removeClass("hidden");
                    self.load_scheduler();
                }
            }, 500);
        },

    });
    core.action_registry.add("sure_book.homepage", SchedulerHomePage);
});
