odoo.define('Crm_lead_dashboard_btc.dashboard', function (require) {
"use strict";

var core = require('web.core');
var QWeb = core.qweb;

var formats = require('web.formats');
var session = require('web.session');
var _t = core._t;
var _lt = core._lt;
var SalesTeamDashboardView = require('sales_team.dashboard');



var lead_by_diploma=[];
//var diploma_category=[];
//var match_categ=[];
var lead_by_certification=[];
var lead_by_diploma_month=[];
var lead_by_certification_month=[];
var lead_source_by_diploma=[];
var lead_source_by_certification=[];
var health_sci_per_faculty=[];
var it_dept_per_faculty=[];
var buss_acc_per_faculty=[];
var health_opportunity=[];
var health_opportunity_months=[];
var IT_Dept=[];
var IT_Dept_months=[];
var bussines_and_acc_weeks=[];
var bussines_acc_months=[];
var admitted_quaterly=[];
var dip_categ=[];
var count=[];
//var local_per_faculty_new=[];
//var internation_per_faculty=[];

//console.log("dip");
//console.log(lead_by_diploma);
//console.log("-----categ");
console.log("---di--???????????%s",health_opportunity);
//console.log(local_per_faculty);


var SalesTeamDashboardView = SalesTeamDashboardView.include({

    display_name: _lt('Dashboard'),
    icon: 'fa-dashboard',
    searchview_hidden: true,
    events: {
        'click .o_dashboard_action': 'on_dashboard_action_clicked',
        'click .o_target_to_set': 'on_dashboard_target_clicked',
            },

    fetch_data: function() {

        return new Model('crm.lead')
            .call('retrieve_sales_dashboard', [], {context: this.session.user_context || {}});


                },

    diptimeoutFunction:function(){
            var chart = AmCharts.makeChart("chartdiv1", {
            "theme": "light",
            "type": "serial",
            "dataProvider": lead_by_diploma,
            "allLabels":{
                  "x": 0,
                  "y": -5,
                  "align": "left",
                },
            "valueAxes": [{
                "axisAlpha": 0,
                "gridAlpha":0,
                "position": "left",
                "labelsEnabled":false,
              }],
            "graphs": [{
                "balloonText": "Income in [[category]]:[[value]]",
                "fillAlphas":1,
                "lineAlpha": 0,
                "type": "column",
                "fillColors":"#FFCE33",
                "valueField":"count",
                "labelsEnabled": false,
                 "balloonFunction": function(lead_by_diploma, graph) {
      var category = lead_by_diploma.dataContext.full_name;
      var count=lead_by_diploma.dataContext.count;
//      console.log('----data---',lead_by_diploma);
//      console.log("------category----%s",category);
//      console.log("----di------%s",diploma_category);
      return category+':'+count;
    }

            }],
            "rotate": true,
            "categoryField":"program_internal_ref",
            "categoryAxis": {
                "gridPosition":"start",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position":"left",
                "gridThickness": 0,
                 },
            });
        },




    certitimeoutFunction:function(){
        var chart = AmCharts.makeChart("chartdiv2",{
        "theme": "light",
        "type": "serial",
        "dataProvider": lead_by_certification,
        "valueAxes": [{
                "axisAlpha":0,
                "gridAlpha":0,
                "position":"left",
                "labelsEnabled":false,
              }],
        "graphs": [{
            "balloonText": "Income in [[category]]:[[value]]",
            "fillAlphas":1,
            "lineAlpha": 0,
            "type": "column",
            "fillColors": "#FF7F50",
            "valueField":"count",
            "labelsEnabled": false,
                 "balloonFunction": function(lead_by_certification, graph) {
      var category = lead_by_certification.dataContext.full_name;
      var count=lead_by_certification.dataContext.count;
//      console.log('----data---',lead_by_diploma);
//      console.log("------category----%s",category);
//      console.log("----di------%s",diploma_category);
      return category+':'+count;
    }
        }],
        "rotate": true,
        "categoryField": "program_internal_ref",
        "categoryAxis": {
            "gridPosition":"start",
            "axisAlpha": 0,
            "gridAlpha": 0,
            "position": "left",
            "gridThickness": 0,
             },
        });
    },




    mthtimeoutdiplomaFunction:function(){
        var chart = AmCharts.makeChart("chartdiv3",{
        "theme": "light",
        "type": "serial",
        "dataProvider": lead_by_diploma_month,
        "valueAxes": [{
                "axisAlpha":0,
                "gridAlpha":0,
                "position":"left",
                "labelsEnabled":false,
              }],
        "graphs": [{
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas":1,
            "lineAlpha": 0,
            "type": "column",
            "fillColors": "#FF7F50",
            "valueField":"count",
            "labelsEnabled": false,

        }],
         "rotate": true,
        "categoryField": "create_date",
        "categoryAxis": {
                "gridPosition":"start",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position": "left",
                "gridThickness": 0,
                 },
        });
    },



     mthtimeoutcertificationFunction:function(){
        var chart = AmCharts.makeChart("chartmonthcertification",{
        "theme": "light",
        "type": "serial",
        "dataProvider": lead_by_certification_month,
        "valueAxes": [{
                "axisAlpha":0,
                "gridAlpha":0,
                "position":"left",
                "labelsEnabled":false,
              }],
        "graphs": [ {
        "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
        "fillAlphas": 0.8,
        "labelText": "[[value]]",
        "lineAlpha": 0.3,
//        "title": "Local",
        "type": "column",
        "color": "#000000",
        "valueField": "count"

        }],
        "rotate": true,
        "categoryField": "create_date",
        "categoryAxis": {
                "gridPosition":"start",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position": "left",
                "gridThickness": 0,
                 },
        });
    },


    admitteddataFunction:function(){
        console.log("-----------",admitted_quaterly);
        var chart = AmCharts.makeChart( "chartdiv13", {
        "theme": "light",
        "type": "serial",
        "legend": {
        "horizontalGap": 10,
        "useGraphSettings": true,
        "markerSize": 10,
         },
        "dataProvider": admitted_quaterly,
        "valueAxes": [ {
        "stackType": "regular",
        "axisAlpha": 0,
        "gridAlpha": 0,
    //    "labelsEnabled":false,
      } ],
        "graphs": [ {
        "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
        "fillAlphas": 0.8,
        "labelText": "[[value]]",
        "lineAlpha": 0.3,
        "title": "Local",
        "type": "column",
        "color": "#000000",
        "valueField": "local"
         }, {
            "balloonText": "[[title]], [[category]]<br><span style='font-size:14px;'><b>[[value]]</b> </span>",
             "fillAlphas": 0.8,
            "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": "International",
            "type": "column",
            "color": "#000000",
            "valueField": "International"

        }],
//
        "categoryField": "month",
        "categoryAxis": {
                "gridPosition":"start",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position": "left",
                "gridThickness": 0,
                 },
    //    "export": {
    //    	"enabled": true
    //     }

    });
        },




    srcitimeoutdiplomaFunction:function(){
        var chart = AmCharts.makeChart("chartsourcediploma", {
        "theme": "light",
        "type": "serial",
        "dataProvider": lead_source_by_diploma,
        "valueAxes": [{
                "axisAlpha":0,
                "gridAlpha":0,
                "position":"left",
                "labelsEnabled":false,
              }],
        "graphs": [ {
        "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
        "fillAlphas": 0.8,
        "labelText": "[[value]]",
        "lineAlpha": 0.3,
//        "title": "Local",
        "type": "column",
        "color": "#000000",
        "valueField": "count"

        }],
        "rotate": true,
        "categoryField": "source_url",
        "categoryAxis": {
                "gridPosition":"start",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position": "left",
                "gridThickness": 0,
                 },
        });
    },

     srcitimeoutcerificationFunction:function(){
        var chart = AmCharts.makeChart("chartsourcecertification", {
        "theme": "light",
        "type": "serial",
        "dataProvider": lead_source_by_certification,
         "valueAxes": [{
                "axisAlpha":0,
                "gridAlpha":0,
                "position":"left",
                "labelsEnabled":false,
              }],
        "graphs": [ {
        "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
        "fillAlphas": 0.8,
        "labelText": "[[value]]",
        "lineAlpha": 0.3,
//        "title": "Local",
        "type": "column",
        "color": "#000000",
        "valueField": "count"

        }],
        "rotate": true,
        "categoryField": "source_url",
        "categoryAxis": {
                "gridPosition":"start",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position": "left",
                "gridThickness": 0,
                 },
        });
    },

    healthoppoFunction:function(){
        console.log("-----------",health_opportunity);
        var chart = AmCharts.makeChart( "chartdiv7", {
        "theme": "light",
            "type": "serial",

          "legend": {
            "horizontalGap": 10,
            "useGraphSettings": true,
            "markerSize": 10
          },
            "dataProvider": health_opportunity,
            "valueAxes": [ {
            "stackType": "regular",
            "axisAlpha": 0,
            "gridAlpha": 0,
        //    "labelsEnabled":false,
          } ],
            "graphs": [ {
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas": 0.8,
            "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": "Local",
            "type": "column",
            "color": "#000000",
            "valueField": "local"
          }, {
                "balloonText": "[[title]], [[category]]<br><span style='font-size:14px;'><b>[[value]]</b> </span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "International",
                "type": "column",
                "color": "#000000",
                "valueField": "International"

            }],

            "categoryField": "week",
            "categoryAxis": {
                    "gridPosition":"start",
                    "axisAlpha": 0,
                    "gridAlpha": 0,
                    "position": "left",
                    "gridThickness": 0,
                     },
        //    "export": {
        //    	"enabled": true
        //     }

        });
    },

    healthoppomonthsFunction:function(){
        console.log("-----------",health_opportunity_months);
        var chart = AmCharts.makeChart( "chartdiv8", {
        "theme": "light",
        "type": "serial",
        "legend": {
        "horizontalGap": 10,
        "useGraphSettings": true,
        "markerSize": 10,
         },
        "dataProvider": health_opportunity_months,
        "valueAxes": [ {
        "stackType": "regular",
        "axisAlpha": 0,
        "gridAlpha": 0,
    //    "labelsEnabled":false,
      } ],
        "graphs": [ {
        "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
        "fillAlphas": 0.8,
        "labelText": "[[value]]",
        "lineAlpha": 0.3,
        "title": "Local",
        "type": "column",
        "color": "#000000",
        "valueField": "local"
         }, {
            "balloonText": "[[title]], [[category]]<br><span style='font-size:14px;'><b>[[value]]</b> </span>",
             "fillAlphas": 0.8,
            "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": "International",
            "type": "column",
            "color": "#000000",
            "valueField": "International"

        }],
//
        "categoryField": "month",
        "categoryAxis": {
                "gridPosition":"start",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position": "left",
                "gridThickness": 0,
                 },
    //    "export": {
    //    	"enabled": true
    //     }

    });
        },

    itdeptFunction:function(){
        console.log("-----------",IT_Dept);
        var chart = AmCharts.makeChart( "chartdiv9", {
        "theme": "light",
            "type": "serial",

          "legend": {
            "horizontalGap": 10,
            "useGraphSettings": true,
            "markerSize": 10
          },
            "dataProvider": IT_Dept,
            "valueAxes": [ {
            "stackType": "regular",
            "axisAlpha": 0,
            "gridAlpha": 0,
        //    "labelsEnabled":false,
          } ],
            "graphs": [ {
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas": 0.8,
            "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": "Local",
            "type": "column",
            "color": "#000000",
            "valueField": "local"
          }, {
                "balloonText": "[[title]], [[category]]<br><span style='font-size:14px;'><b>[[value]]</b> </span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "International",
                "type": "column",
                "color": "#000000",
                "valueField": "International"

            }],

            "categoryField": "week",
            "categoryAxis": {
                    "gridPosition":"start",
                    "axisAlpha": 0,
                    "gridAlpha": 0,
                    "position": "left",
                    "gridThickness": 0,
                     },
        //    "export": {
        //    	"enabled": true
        //     }

        });
    },


    itdeptmonthsFunction:function(){
        console.log("-----------",IT_Dept_months);
        var chart = AmCharts.makeChart( "chartdiv10", {
        "theme": "light",
            "type": "serial",

          "legend": {
            "horizontalGap": 10,
            "useGraphSettings": true,
            "markerSize": 10
          },
            "dataProvider": IT_Dept_months,
            "valueAxes": [ {
            "stackType": "regular",
            "axisAlpha": 0,
            "gridAlpha": 0,
        //    "labelsEnabled":false,
          } ],
            "graphs": [ {
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas": 0.8,
            "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": "Local",
            "type": "column",
            "color": "#000000",
            "valueField": "local"
          }, {
                "balloonText": "[[title]], [[category]]<br><span style='font-size:14px;'><b>[[value]]</b> </span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "International",
                "type": "column",
                "color": "#000000",
                "valueField": "International"

            }],

            "categoryField": "month",
            "categoryAxis": {
                    "gridPosition":"start",
                    "axisAlpha": 0,
                    "gridAlpha": 0,
                    "position": "left",
                    "gridThickness": 0,
                     },
        //    "export": {
        //    	"enabled": true
        //     }

        });
    },


     bussinesaccweekFunction:function(){
        console.log("-----------",bussines_and_acc_weeks);
        var chart = AmCharts.makeChart( "chartdiv11", {
        "theme": "light",
            "type": "serial",

          "legend": {
            "horizontalGap": 10,
            "useGraphSettings": true,
            "markerSize": 10
          },
            "dataProvider": bussines_and_acc_weeks,
            "valueAxes": [ {
            "stackType": "regular",
            "axisAlpha": 0,
            "gridAlpha": 0,
        //    "labelsEnabled":false,
          } ],
            "graphs": [ {
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas": 0.8,
            "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": "Local",
            "type": "column",
            "color": "#000000",
            "valueField": "local"
          }, {
                "balloonText": "[[title]], [[category]]<br><span style='font-size:14px;'><b>[[value]]</b> </span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "International",
                "type": "column",
                "color": "#000000",
                "valueField": "International"

            }],

            "categoryField": "week",
            "categoryAxis": {
                    "gridPosition":"start",
                    "axisAlpha": 0,
                    "gridAlpha": 0,
                    "position": "left",
                    "gridThickness": 0,
                     },
        //    "export": {
        //    	"enabled": true
        //     }

        });
    },


    bussinesaccmonthsFunction:function(){
        console.log("-----------",bussines_acc_months);
        var chart = AmCharts.makeChart( "chartdiv12", {
        "theme": "light",
            "type": "serial",

          "legend": {
            "horizontalGap": 10,
            "useGraphSettings": true,
            "markerSize": 10
          },
            "dataProvider": bussines_acc_months,
            "valueAxes": [ {
            "stackType": "regular",
            "axisAlpha": 0,
            "gridAlpha": 0,
        //    "labelsEnabled":false,
          } ],
            "graphs": [ {
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas": 0.8,
            "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": "Local",
            "type": "column",
            "color": "#000000",
            "valueField": "local"
          }, {
                "balloonText": "[[title]], [[category]]<br><span style='font-size:14px;'><b>[[value]]</b> </span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "International",
                "type": "column",
                "color": "#000000",
                "valueField": "International"

            }],

            "categoryField": "month",
            "categoryAxis": {
                    "gridPosition":"start",
                    "axisAlpha": 0,
                    "gridAlpha": 0,
                    "position": "left",
                    "gridThickness": 0,
                     },
        //    "export": {
        //    	"enabled": true
        //     }

        });
    },

    totalhealthscienceFunction:function(){
        console.log(health_sci_per_faculty);
        var chart = AmCharts.makeChart("chartdiv5",{
        "type": "serial",
        "theme": "light",
        "legend": {
            "horizontalGap": 10,
            "maxColumns": 1,
            "position": "right",
            "useGraphSettings": true,
            "markerSize": 10
        },
        "dataProvider":health_sci_per_faculty,



        "valueAxes": [{
            "stackType": "regular",
            "axisAlpha": 0,
            "gridAlpha": 0,
            "labelsEnabled":false,
        }],
        "graphs": [{
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas": 0.8,
    //        "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": "Local",
            "type": "column",
            "color": "#000000",
            "valueField": "local"
        },
        {
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas":1,
    //        "labelText": "[[value]]",
            "lineAlpha":1,
            "title": "International",
            "type": "column",
            "color": "#000000",
            "valueField": "International"
            }],
        "rotate": true,
        "categoryField": "faculty",
        "categoryAxis": {
            "gridPosition": "start",
            "axisAlpha": 0,
            "gridAlpha": 0,
            "position": "left"
        },
    //    "export": {
    //    	"enabled": true
    //     }

        });
    },

    totalitdepartmentFunction:function(){
            console.log(it_dept_per_faculty);
            var chart = AmCharts.makeChart("chartdiv6",{
            "type": "serial",
        "theme": "light",
        "legend": {
            "horizontalGap": 10,
            "maxColumns": 1,
            "position": "right",
            "useGraphSettings": true,
            "markerSize": 10
        },
        "dataProvider": it_dept_per_faculty,

        "valueAxes": [{
            "stackType": "regular",
            "axisAlpha": 0,
            "gridAlpha": 0,
            "labelsEnabled":false,
        }],
        "graphs": [{
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas": 0.8,
    //        "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": "Local",
            "type": "column",
            "color": "#000000",
            "valueField": "local"
        },
        {
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas":1,
    //        "labelText": "[[value]]",
            "lineAlpha":1,
            "title": "International",
            "type": "column",
            "color": "#000000",
            "valueField": "International"
            }],
        "rotate": true,
        "categoryField": "faculty",
        "categoryAxis": {
            "gridPosition": "start",
            "axisAlpha": 0,
            "gridAlpha": 0,
            "position": "left"
        },
    //    "export": {
    //    	"enabled": true
    //     }

            });
        },


    totalbusinessaccountFunction:function(){
            console.log(buss_acc_per_faculty);
            var chart = AmCharts.makeChart("chartdivtotalbusiness",{
            "type": "serial",
        "theme": "light",
        "legend": {
            "horizontalGap": 10,
            "maxColumns": 1,
            "position": "right",
            "useGraphSettings": true,
            "markerSize": 10
        },
        "dataProvider": buss_acc_per_faculty,

        "valueAxes": [{
            "stackType": "regular",
            "axisAlpha": 0,
            "gridAlpha": 0,
            "labelsEnabled":false,
        }],
        "graphs": [{
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas": 0.8,
    //        "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": "Local",
            "type": "column",
            "color": "#000000",
            "valueField": "local"
        },
        {
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
            "fillAlphas":1,
    //        "labelText": "[[value]]",
            "lineAlpha":1,
            "title": "International",
            "type": "column",
            "color": "#000000",
            "valueField": "International"
            }],
        "rotate": true,
        "categoryField": "faculty",
        "categoryAxis": {
            "gridPosition": "start",
            "axisAlpha": 0,
            "gridAlpha": 0,
            "position": "left"
        },
    //    "export": {
    //    	"enabled": true
    //     }

            });
        },




    amcharts_diploma:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        lead_by_diploma=[]
        var self=this;
//        var diploma_category=[]
//        var match_categ=[]
        crm_model.call('retrieve_diploma_data').then(function(result)
        {

          if (result == 'None')
              {
                lead_by_diploma=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                  {
                      var title=result[i].internal_ref;
                      var value=result[i].count;
                      var dip_categ=result[i].name;
                      lead_by_diploma.push({'program_internal_ref':title,'count':value,'full_name':dip_categ});
//                      match_categ.push({'program_internal_ref':title,'diploma_category':dip_categ});
//                      console.log("------------%s",title);
//                      var main_dict={}
//                      main_dict[title]={'diploma_category':dip_categ,'count':value}
//                      console.log("---di--???????????%s",main_dict);
//                      diploma_category.push({main_dict});
//                      console.log(diploma_category);
                  };
              }

                setTimeout(function() {self.diptimeoutFunction();},300);

            });
        },


    amcharts_healthoppo:function(){
    var Model= require('web.Model');
    var crm_model= new Model('crm.lead');
    health_opportunity=[]
    var self=this;
//        var diploma_category=[]
//        var match_categ=[]
    crm_model.call('retrieve_health_opporunity').then(function(result)
    {

      if (result == 'None')
          {
            health_opportunity=[]
          }
          else
          {
              console.log("-result?%s",result);
              for (var i=0; result.length>i; i++)
              {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//                      var title=result[i].internal_ref;
//                      var value=result[i].count;
//                      var dip_categ=result[i].team_id_name;
                    health_opportunity.push(result[i]);
                    console.log(result[i]);
//                      match_categ.push({'program_internal_ref':title,'diploma_category':dip_categ});
//                      console.log("------------%s",title);
//                      var main_dict={}
//                      main_dict[title]={'diploma_category':dip_categ,'count':value}
//                      console.log("---di--???????????%s",dip_categ);
//                      console.log("---di--???????????%s",value);
//                      diploma_category.push({main_dict});
//                      console.log(diploma_category);
              };
              console.log("----health opp");
              console.log(health_opportunity)
          }

            setTimeout(function() {self.healthoppoFunction();},300);

        });
    },


    amcharts_healthoppomonths:function(){
    var Model= require('web.Model');
    var crm_model= new Model('crm.lead');
    health_opportunity_months=[]
    var self=this;
//        var diploma_category=[]
//        var match_categ=[]
    crm_model.call('retrieve_health_opporunity_months').then(function(result)
    {

      if (result == 'None')
          {
            health_opportunity_months=[]
          }
          else
          {
              console.log("-result?%s",result);
              for (var i=0; result.length>i; i++)
              {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//                      var title=result[i].internal_ref;
//                      var value=result[i].count;
//                      var dip_categ=result[i].team_id_name;
                    health_opportunity_months.push(result[i]);
                    console.log(result[i]);
//                      match_categ.push({'program_internal_ref':title,'diploma_category':dip_categ});
//                      console.log("------------%s",title);
//                      var main_dict={}
//                      main_dict[title]={'diploma_category':dip_categ,'count':value}
//                      console.log("---di--???????????%s",dip_categ);
//                      console.log("---di--???????????%s",value);
//                      diploma_category.push({main_dict});
//                      console.log(diploma_category);
              };
              console.log("----health opp month");
              console.log(health_opportunity_months)
          }

            setTimeout(function() {self.healthoppomonthsFunction();},300);

        });
    },


    amcharts_itdept:function(){
    var Model= require('web.Model');
    var crm_model= new Model('crm.lead');
    IT_Dept=[]
    var self=this;
//        var diploma_category=[]
//        var match_categ=[]
    crm_model.call('retrieve_it_dept_weeks').then(function(result)
    {

      if (result == 'None')
          {
            IT_Dept=[]
          }
          else
          {
              console.log("-result?%s",result);
              for (var i=0; result.length>i; i++)
              {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//                      var title=result[i].internal_ref;
//                      var value=result[i].count;
//                      var dip_categ=result[i].team_id_name;
                    IT_Dept.push(result[i]);
                    console.log(result[i]);
//                      match_categ.push({'program_internal_ref':title,'diploma_category':dip_categ});
//                      console.log("------------%s",title);
//                      var main_dict={}
//                      main_dict[title]={'diploma_category':dip_categ,'count':value}
//                      console.log("---di--???????????%s",dip_categ);
//                      console.log("---di--???????????%s",value);
//                      diploma_category.push({main_dict});
//                      console.log(diploma_category);
              };
              console.log("----health opp month");
              console.log(IT_Dept)
          }

            setTimeout(function() {self.itdeptFunction();},300);

        });
    },

    amcharts_itdeptmonths:function(){
    var Model= require('web.Model');
    var crm_model= new Model('crm.lead');
    IT_Dept_months=[]
    var self=this;
//        var diploma_category=[]
//        var match_categ=[]
    crm_model.call('retrieve_it_dept_months').then(function(result)
    {

      if (result == 'None')
          {
            IT_Dept_months=[]
          }
          else
          {
              console.log("-result?%s",result);
              for (var i=0; result.length>i; i++)
              {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//                      var title=result[i].internal_ref;
//                      var value=result[i].count;
//                      var dip_categ=result[i].team_id_name;
                    IT_Dept_months.push(result[i]);
                    console.log(result[i]);
//                      match_categ.push({'program_internal_ref':title,'diploma_category':dip_categ});
//                      console.log("------------%s",title);
//                      var main_dict={}
//                      main_dict[title]={'diploma_category':dip_categ,'count':value}
//                      console.log("---di--???????????%s",dip_categ);
//                      console.log("---di--???????????%s",value);
//                      diploma_category.push({main_dict});
//                      console.log(diploma_category);
              };
              console.log("----health opp month");
              console.log(IT_Dept_months)
          }

            setTimeout(function() {self.itdeptmonthsFunction();},300);

        });
    },
//



    amcharts_bussinesaccountweeks:function(){
    var Model= require('web.Model');
    var crm_model= new Model('crm.lead');
    bussines_and_acc_weeks=[]
    var self=this;
//        var diploma_category=[]
//        var match_categ=[]
    crm_model.call('retrieve_bussines_acc_weeks').then(function(result)
    {

      if (result == 'None')
          {
            bussines_and_acc_weeks=[]
          }
          else
          {
              console.log("-result?%s",result);
              for (var i=0; result.length>i; i++)
              {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//                      var title=result[i].internal_ref;
//                      var value=result[i].count;
//                      var dip_categ=result[i].team_id_name;
                    bussines_and_acc_weeks.push(result[i]);
                    console.log(result[i]);
//                      match_categ.push({'program_internal_ref':title,'diploma_category':dip_categ});
//                      console.log("------------%s",title);
//                      var main_dict={}
//                      main_dict[title]={'diploma_category':dip_categ,'count':value}
//                      console.log("---di--???????????%s",dip_categ);
//                      console.log("---di--???????????%s",value);
//                      diploma_category.push({main_dict});
//                      console.log(diploma_category);
              };
              console.log("----health opp month");
              console.log(bussines_and_acc_weeks)
          }

            setTimeout(function() {self.bussinesaccweekFunction();},300);

        });
    },

    amcharts_bussinesaccountmonths:function(){
    var Model= require('web.Model');
    var crm_model= new Model('crm.lead');
    bussines_acc_months=[]
    var self=this;
//        var diploma_category=[]
//        var match_categ=[]
    crm_model.call('retrieve_bussines_acc_months').then(function(result)
    {

      if (result == 'None')
          {
            bussines_acc_months=[]
          }
          else
          {
              console.log("-result?%s",result);
              for (var i=0; result.length>i; i++)
              {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//                      var title=result[i].internal_ref;
//                      var value=result[i].count;
//                      var dip_categ=result[i].team_id_name;
                    bussines_acc_months.push(result[i]);
                    console.log(result[i]);
//                      match_categ.push({'program_internal_ref':title,'diploma_category':dip_categ});
//                      console.log("------------%s",title);
//                      var main_dict={}
//                      main_dict[title]={'diploma_category':dip_categ,'count':value}
//                      console.log("---di--???????????%s",dip_categ);
//                      console.log("---di--???????????%s",value);
//                      diploma_category.push({main_dict});
//                      console.log(diploma_category);
              };
              console.log("----health opp month");
              console.log(bussines_acc_months)
          }

            setTimeout(function() {self.bussinesaccmonthsFunction();},300);

        });
    },
//




    amcharts_certification:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        lead_by_certification=[]
        var self=this;
        crm_model.call('retrieve_certification_data').then(function(result)
        {
           if (result == 'None')
              {
                lead_by_certification=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                  {
                      var title=result[i].internal_ref;
                      var value=result[i].count;
                      var dip_categ=result[i].name;
                      lead_by_certification.push({'program_internal_ref':title,'count':value,'full_name':dip_categ});
                      console.log("------%s",value);
                      console.log("------%s",title);
                  };
              }
                setTimeout(function() {self.certitimeoutFunction();},300);

            });
        },


    amcharts_totalhealthscience:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        health_sci_per_faculty=[]
        var self=this;
//        var diploma_category=[]
//        var match_categ=[]
        crm_model.call('retrieve_health_sec_per_faculty').then(function(result)
        {

          if (result == 'None')
              {
                health_sci_per_faculty=[]
              }
              else
              {
                  console.log("-result?%s",result);
              for (var i=0; result.length>i; i++)
              {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//                      var title=result[i].internal_ref;
//                      var value=result[i].count;
//                      var dip_categ=result[i].team_id_name;
                    health_sci_per_faculty.push(result[i]);
                    console.log(result[i]);
//                      match_categ.push({'program_internal_ref':title,'diploma_category':dip_categ});
//                      console.log("------------%s",title);
//                      var main_dict={}
//                      main_dict[title]={'diploma_category':dip_categ,'count':value}
//                      console.log("---di--???????????%s",dip_categ);
//                      console.log("---di--???????????%s",value);
//                      diploma_category.push({main_dict});
//                      console.log(diploma_category);
              };
              console.log("----health opp month");
              console.log(health_sci_per_faculty)
              }

                setTimeout(function() {self.totalhealthscienceFunction();},300);

            });
        },

    amcharts_totalitdeptarment:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        it_dept_per_faculty=[]
        var self=this;
//        var diploma_category=[]
//        var match_categ=[]
        crm_model.call('retrieve_it_dept_per_faculty').then(function(result)
        {

          if (result == 'None')
              {
                it_dept_per_faculty=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                   {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//                      var title=result[i].internal_ref;
//                      var value=result[i].count;
//                      var dip_categ=result[i].team_id_name;
                    it_dept_per_faculty.push(result[i]);
                    console.log(result[i]);
//                      match_categ.push({'program_internal_ref':title,'diploma_category':dip_categ});
//                      console.log("------------%s",title);
//                      var main_dict={}
//                      main_dict[title]={'diploma_category':dip_categ,'count':value}
//                      console.log("---di--???????????%s",dip_categ);
//                      console.log("---di--???????????%s",value);
//                      diploma_category.push({main_dict});
//                      console.log(diploma_category);
              };
              console.log("----health opp month");
              console.log(it_dept_per_faculty)
              }

                setTimeout(function() {self.totalitdepartmentFunction();},300);

            });
        },
//

     amcharts_totalbusinessaccount:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        buss_acc_per_faculty=[]
        var self=this;
//        var diploma_category=[]
//        var match_categ=[]
        crm_model.call('retrieve_bussines_acc_per_faculty').then(function(result)
        {

          if (result == 'None')
              {
                buss_acc_per_faculty=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                   {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//                      var title=result[i].internal_ref;
//                      var value=result[i].count;
//                      var dip_categ=result[i].team_id_name;
                    buss_acc_per_faculty.push(result[i]);
                    console.log(result[i]);
//                      match_categ.push({'program_internal_ref':title,'diploma_category':dip_categ});
//                      console.log("------------%s",title);
//                      var main_dict={}
//                      main_dict[title]={'diploma_category':dip_categ,'count':value}
//                      console.log("---di--???????????%s",dip_categ);
//                      console.log("---di--???????????%s",value);
//                      diploma_category.push({main_dict});
//                      console.log(diploma_category);
              };
              console.log("----health opp month");
              console.log(buss_acc_per_faculty)
              }

                setTimeout(function() {self.totalbusinessaccountFunction();},300);

            });
        },


    amcharts_monthsdiploma:function(){
            var Model= require('web.Model');
            var crm_model= new Model('crm.lead');
            lead_by_diploma_month=[]
            var self=this
            crm_model.call('retrieve_lead_by_diploma_month_data').then(function(result)
            {
              if (result == 'None')
                  {
                    lead_by_diploma_month=[]
                  }
                  else
                  {
                      for (var i=0; result.length>i; i++)
                      {
                         lead_by_diploma_month.push(result[i]);
                         console.log(result[i]);
                      };
                  }
                    setTimeout(function() {self.mthtimeoutdiplomaFunction();},300);

                });
            },

    amcharts_monthscertification:function(){
            var Model= require('web.Model');
            var crm_model= new Model('crm.lead');
            lead_by_certification_month=[]
            var self=this
            crm_model.call('retrieve_lead_by_certification_month_data').then(function(result)
            {
              if (result == 'None')
                  {
                    lead_by_certification_month=[]
                  }
                  else
                  {
                      for (var i=0; result.length>i; i++)
                      {
                         lead_by_certification_month.push(result[i]);
                         console.log(result[i]);
                      };
                  }
                    setTimeout(function() {self.mthtimeoutcertificationFunction();},300);

                });
            },

    amcharts_admittedquaterly:function(){
    var Model= require('web.Model');
    var crm_model= new Model('crm.lead');
    admitted_quaterly=[]
    var self=this;
//        var diploma_category=[]
//        var match_categ=[]
    crm_model.call('retrieve_admitted_data').then(function(result)
    {

      if (result == 'None')
          {
            admitted_quaterly=[]
          }
          else
          {
              console.log("-result?%s",result);
              for (var i=0; result.length>i; i++)
              {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//                      var title=result[i].internal_ref;
//                      var value=result[i].count;
//                      var dip_categ=result[i].team_id_name;
                    admitted_quaterly.push(result[i]);
                    console.log(result[i]);
//                      match_categ.push({'program_internal_ref':title,'diploma_category':dip_categ});
//                      console.log("------------%s",title);
//                      var main_dict={}
//                      main_dict[title]={'diploma_category':dip_categ,'count':value}
//                      console.log("---di--???????????%s",dip_categ);
//                      console.log("---di--???????????%s",value);
//                      diploma_category.push({main_dict});
//                      console.log(diploma_category);
              };
              console.log("----health opp month");
              console.log(admitted_quaterly)
          }

            setTimeout(function() {self.admitteddataFunction();},300);

        });
    },
//



    amcharts_sourcediploma:function(){
            var Model= require('web.Model');
            var crm_model= new Model('crm.lead');
            lead_source_by_diploma=[]
            var self=this;
            crm_model.call('retrieve_source_by_diploma_data').then(function(result)
            {

              if (result == 'None')
                  {
                    lead_source_by_diploma=[]
                  }
                  else
                  {
                      for (var i=0; result.length>i; i++)
                      {
                          lead_source_by_diploma.push(result[i]);
                           console.log(result[i]);
                      };
                  }
                    setTimeout(function() {self.srcitimeoutdiplomaFunction();},300);

                });
               },

    amcharts_sourcecertification:function(){
            var Model= require('web.Model');
            var crm_model= new Model('crm.lead');
            lead_source_by_certification=[]
            var self=this;
            crm_model.call('retrieve_source_by_cerification_data').then(function(result)
            {

              if (result == 'None')
                  {
                    lead_source_by_certification=[]
                  }
                  else
                  {
                      for (var i=0; result.length>i; i++)
                      {
                          lead_source_by_certification.push(result[i]);
                           console.log(result[i]);
                      };
                  }
                    setTimeout(function() {self.srcitimeoutcerificationFunction();},300);

                });
               },
//






    render: function() {
        var super_render = this._super;
        var self = this;
        return this.fetch_data().then(function(result){

            self.show_demo = result && result.nb_opportunities === 0;
            var sales_dashboard = QWeb.render('sales_team.SalesDashboard', {
                widget: self,
                show_demo: self.show_demo,
                values: result,
            });
            super_render.call(self);
            $(sales_dashboard).prependTo(self.$el);
            self.amcharts_diploma();
            self.amcharts_certification();
            self.amcharts_totalhealthscience();
            self.amcharts_totalitdeptarment();
            self.amcharts_totalbusinessaccount();
            self.amcharts_sourcediploma();
            self.amcharts_sourcecertification();
            self.amcharts_monthsdiploma();
            self.amcharts_monthscertification();
            self.amcharts_healthoppo();
            self.amcharts_healthoppomonths();
            self.amcharts_itdept();
            self.amcharts_itdeptmonths();
            self.amcharts_bussinesaccountweeks();
            self.amcharts_bussinesaccountmonths();
            self.amcharts_admittedquaterly();
           });
         },




       });
    });









