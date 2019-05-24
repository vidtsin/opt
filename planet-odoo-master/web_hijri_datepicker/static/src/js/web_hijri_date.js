odoo.define('web_hijri_datepicker.web_hijri_datepicker', function(require) {
"use strict";

    var core = require('web.core');
    var formats = require('web.formats');
    var time = require('web.time');
    var Widget = require('web.Widget');
    var datepicker = require('web.datepicker');
    var _t = core._t;

    datepicker.DateWidget.include({
        start: function() {
            this.$input_extra_date = this.$el.find('input.o_extra_date');
            this.$input_extra_time = this.$el.find('input.o_extra_time');
            this._super();
        },

        on_picker_select: function(text, instance) {
            this._super(text, instance);
            text = instance.currentYear +'-'+ (instance.currentMonth+1) +'-'+ instance.currentDay;
            var value = convert_gregorian_hijri(text, this.type_of_date);
            $(this.$input_extra_date).val(value[0]);
            $(this.$input_extra_time).val(value[1]);
        },

        set_value: function(value) {
            this._super(value);
            var value = convert_gregorian_hijri(value, this.type_of_date);
            $(this.$input_extra_date).val(value[0]);
            $(this.$input_extra_time).val(value[1]);
        },

        set_value_from_ui: function() {
            var value = this.$input.val() || false;
            this.set_value(this.parse_client(value));
            //var text = formats.format_value(value, this, '');
            var value = convert_gregorian_hijri(this.parse_client(this.$input.val()), this.type_of_date);
            $(this.$input_extra_date).val(value[0]);
            $(this.$input_extra_time).val(value[1]);
        },

        set_readonly: function(readonly) {
            this.$input_extra_date.prop('readonly', this.readonly);
            this._super(readonly);
        },

        set_datetime_default: function() {
            this._super();
            var value = convert_gregorian_hijri(this.parse_client(this.$input.val()), this.type_of_date);
            $(this.$input_extra_date).val(value[0]);
            $(this.$input_extra_time).val(value[1]);
        },

    });
    
    core.form_widget_registry.map.date.include({
        initialize_content: function() {

            if (this.datewidget) {
                this.datewidget.destroy();
                this.datewidget = undefined;
            }

            if (!this.get("effective_readonly")) {
                this.datewidget = this.build_widget();
                this.datewidget.on('datetime_changed', this, function() {
                    this.internal_set_value(this.datewidget.get_value());
                });

                var self = this;
                this.datewidget.appendTo('<div>').done(function() {
                    self.datewidget.$el.addClass(self.$el.attr('class'));
                    self.replaceElement(self.datewidget.$el);
                    self.datewidget.$input.addClass('o_form_input');
                    self.setupFocus(self.datewidget.$input);
                });
               
                function convert_date_hijri(date) {
                    if (!date || date.length == 0) {
                        return false
                    }

                    var jd = $.calendars.instance('islamic').toJD(parseInt(date[0].year()),parseInt(date[0].month()),parseInt(date[0].day()));
                    var gre_date = $.calendars.instance('gregorian').fromJD(jd).add(-1,'d');
                    var date_value = new Date(parseInt(gre_date.year()),parseInt(gre_date.month())-1,parseInt(gre_date.day()));

                    var text = formats.format_value(gre_date, this, '');
                    self.$el.find(".o_extra_date").val(text);

                    var formated_date = moment(date_value).format(self.datewidget.picker.format);

                    self.datewidget.$input.val(formats.parse_value(formated_date, {"widget": self.type_of_date}));
                    self.datewidget.change_datetime();
                }

                this.$('.o_extra_date').calendarsPicker({
                    calendar: $.calendars.instance('islamic','ar'),
                    dateFormat: 'M d, yyyy',
                    onSelect: convert_date_hijri,
                    localNumbers: true,
                });
                this.$('.o_extra_time').timeEntry({
                    showSeconds: true,
                    spinnerImage: '',
                    show24Hours: true
                }).change(function() {
                    var new_time = $(".o_extra_time").val();
                    var $date = $(".o_extra_time").parent().find(".o_datepicker_input");
                    var date = self.datewidget.get_value()
                    var date_split = convert_gregorian_hijri(date, 'datetime');
                    var old_split = date.split(' ');

                    if (date_split.length > 1){
                        self.datewidget.set_value(old_split[0]+ ' ' + new_time);
                        var formated_date = formats.format_value(old_split[0]+ ' ' + new_time, self, '');
                        $date.val(formated_date);
                        self.datewidget.change_datetime();
                    }
                });
            }
        },
        render_value: function() {
            if (this.get("effective_readonly")) {
                var formated_date = formats.format_value(this.get('value'), this, '');
                this.$el.text(formated_date);
                var value = convert_gregorian_hijri(this.get('value'), this.field.type)

                if (this.field.type=='date'){
                    this.$el.append("<p>" + value[0] + "</p>");
                } else {
                    this.$el.append("<p>" + value[0] + ' ' + value[1] + "</p>");
                }

            } else {
                this.datewidget.set_value(this.get('value'));
                var value = convert_gregorian_hijri(this.get('value'), this.field.type);

                if (this.field.type=='date'){
                    this.$el.find('input.o_extra_date').val(value[0]);
                    this.$el.find('input.o_extra_date').removeClass("odoo_extra_date");
                    this.$el.find('input.o_extra_time').remove();
                } else {
                    this.$el.find('input.o_extra_date').val(value[0]);
                    this.$el.find('input.o_extra_time').val(value[1]);
                }

            }
        },
    });

    function convert_gregorian_hijri(text,type) {
        var day = '';
        var year = '';
        var month = '';
        var text_split = '';
        var calendar = $.calendars.instance('gregorian', 'ar');
        var hijri_calendar = $.calendars.instance('islamic', 'ar');

        if (text) {
            if (text.indexOf('-')!= -1){
                text_split = text.split('-');
                year = parseInt(text_split[0]);
                month = parseInt(text_split[1]);
                day = parseInt(text_split[2]);
            }
            if(text.indexOf('/')!= -1){
                text_split = text.split('/');
                year = parseInt(text_split[2]);
                month = parseInt(text_split[0]);
                day = parseInt(text_split[1]);
            }
            var jd = calendar.toJD(year,month,day);
            var date = hijri_calendar.fromJD(jd);

            var res = hijri_calendar.formatDate('M d, Y', date.add(1,'d'));
            if (type=='datetime' && (text.split(' ')).length > 1) {
                var time = text.split(' ')[1].split(':');
                return [('%s',res) , ('%s',time[0])+':'+('%s',time[1])+':'+('%s',time[2])];
            } else {
                return [res,''];
            }

        }
        return '';
    }
});
