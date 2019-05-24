odoo.define('Crm_lead_dashboard.dashboard', function (require) {
"use strict";

var core = require('web.core');
var QWeb = core.qweb;

var formats = require('web.formats');
var session = require('web.session');
//var WebClient = require('web.WebClient');
var _t = core._t;
var _lt = core._lt;
var SalesTeamDashboardView = require('sales_team.dashboard');

var global_id=[];
console.log("----leadsssssssssssssssss-------",leads_data_month);
console.log("----globalVarrrrrrrrr-------",global_id);

var lead_monthly_product=[];
var lead_monthly_source=[];
var leads_product=[];
var opportunity_product=[];
var healthy_opportunity=[];
var current_month_data=[];
var leads_data_month=[];
var source_data_month=[];
console.log("----leadsssssssssssssssss111111-------",leads_data_month);
var current_month_source_data=[];
var current_health_oppo_data=[];
var current_monthly_health=[];
var total_sales_months=[];

var test=[]
var test1=[]

console.log("----testttttt-------",test);



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

    monthleadproductFunction:function(){
            var chart = AmCharts.makeChart("chartleadproduct", {
            "type": "pie",
             "theme": "light",
            "dataProvider": lead_monthly_product,
           "valueField": "count",
            "titleField": "product_name",
           "balloon":{
           "fixedPosition":true
          },

                    });
        },



    monthleadsourceFunction:function(){
            var chart = AmCharts.makeChart("chartleadsource", {
            "type": "pie",
             "theme": "light",
            "dataProvider": lead_monthly_source,
           "valueField": "count",
            "titleField": "source_of_lead",
           "balloon":{
           "fixedPosition":true
          },

                    });
        },


    leadsproductFunction:function(){
            var chart = AmCharts.makeChart("chartleads", {
            "type": "pie",
             "theme": "light",
            "dataProvider": leads_product,
           "valueField": "count",
            "titleField": "product_name",
           "balloon":{
           "fixedPosition":true
          },

                    });
        },


    opportunityproductFunction:function(){
            var chart = AmCharts.makeChart("chartopportunity", {
            "type": "pie",
             "theme": "light",
            "dataProvider": opportunity_product,
           "valueField": "count",
            "titleField": "product_name",
           "balloon":{
           "fixedPosition":true
          },

                    });
        },


    healthopportunityFunction:function(){
            var chart = AmCharts.makeChart("charthealthoppo", {
            "type": "pie",
             "theme": "light",
            "dataProvider": healthy_opportunity,
           "valueField": "count",
            "titleField": "stage_id_name",
           "balloon":{
           "fixedPosition":true
          },

                    });
        },

    currentmonthleadsFunction:function(){
//            console.log(buss_acc_per_faculty);
            var chart = AmCharts.makeChart("chartcurrentmonth", {
                  "type": "serial",
                  "theme": "light",
                  "marginRight": 70,
                  "dataProvider": current_month_data,
                  "valueAxes": [{
                    "axisAlpha": 0,
                    "position": "left",

                  }],
                  "startDuration": 1,
                  "graphs": [{
                    "balloonText": "<b>[[category]]: [[value]]</b>",
                    "fillColorsField": "color",
                    "fillAlphas": 0.9,
                    "lineAlpha": 0.2,
                    "type": "column",
                    "valueField": "count"
                  }],
                  "chartCursor": {
                    "categoryBalloonEnabled": false,
                    "cursorAlpha": 0,
                    "zoomable": false
                  },
                  "categoryField": "product_name",
                  "categoryAxis": {
                    "gridPosition": "start",
                    "labelRotation": 45
                  },
//                  "export": {
//                    "enabled": true
//                  }

                });
            },

       currentmonthsourceFunction:function(){
//            console.log(buss_acc_per_faculty);
            var chart = AmCharts.makeChart("chartcurrentmonthsource", {
                  "type": "serial",
                  "theme": "light",
                  "marginRight": 70,
                  "dataProvider": current_month_source_data,
                  "valueAxes": [{
                    "axisAlpha": 0,
                    "position": "left",

                  }],
                  "startDuration": 1,
                  "graphs": [{
                    "balloonText": "<b>[[category]]: [[value]]</b>",
                    "fillColorsField": "color",
                    "fillAlphas": 0.9,
                    "lineAlpha": 0.2,
                    "type": "column",
                    "valueField": "count"
                  }],
                  "chartCursor": {
                    "categoryBalloonEnabled": false,
                    "cursorAlpha": 0,
                    "zoomable": false
                  },
                  "categoryField": "source_of_lead",
                  "categoryAxis": {
                    "gridPosition": "start",
                    "labelRotation": 45
                  },
//                  "export": {
//                    "enabled": true
//                  }

                });
            },


        currenthealthoppoFunction:function(){
//            console.log(buss_acc_per_faculty);
            var chart = AmCharts.makeChart("chartmonthlyhealthoppo", {
                  "type": "serial",
                  "theme": "light",
                  "marginRight": 70,
                  "dataProvider": current_health_oppo_data,
                  "valueAxes": [{
                    "axisAlpha": 0,
                    "position": "left",

                  }],
                  "startDuration": 1,
                  "graphs": [{
                    "balloonText": "<b>[[category]]: [[value]]</b>",
                    "fillColorsField": "color",
                    "fillAlphas": 0.9,
                    "lineAlpha": 0.2,
                    "type": "column",
                    "valueField": "count"
                  }],
                  "chartCursor": {
                    "categoryBalloonEnabled": false,
                    "cursorAlpha": 0,
                    "zoomable": false
                  },
                  "categoryField": "stage_id_name",
                  "categoryAxis": {
                    "gridPosition": "start",
                    "labelRotation": 45
                  },
//                  "export": {
//                    "enabled": true
//                  }

                });
            },
    totalsalesmonthlyFunction:function(){
    console.log("-----------",total_sales_months);
    var chart = AmCharts.makeChart( "charttotalsales", {
    "theme": "light",
        "type": "serial",

      "legend": {
        "horizontalGap": 10,
        "useGraphSettings": true,
        "markerSize": 10
      },
        "dataProvider": total_sales_months,
        "valueAxes": [ {
        "stackType": "regular",
        "axisAlpha": 0,
        "gridAlpha": 0,
    //    "labelsEnabled":false,
      } ],
        "graphs": [ {
        "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
        "fillAlphas": 0.8,
        "labelText": "[[value]]",
        "lineAlpha": 0.3,
        "title": "Won",
        "type": "column",
        "color": "#000000",
        "valueField": "Won"
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

    monthlyleadsFunction:function(){
        console.log("-----------",leads_data_month);
        var chart = AmCharts.makeChart( "chartmonthlylead", {
        "theme": "light",
            "type": "serial",

          "legend": {
            "horizontalGap": 10,
            "useGraphSettings": true,
            "markerSize": 10
          },
            "dataProvider": leads_data_month,
            "valueAxes": [ {
            "stackType": "regular",
            "axisAlpha": 0,
            "gridAlpha": 0,
        //    "labelsEnabled":false,
          } ],
            "graphs": [ {
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
            "fillAlphas": 0.8,
            "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": test[0],
            "type": "column",
            "color": "#000000",
            "valueField": test[0]
          }, {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title":test[1] ,
                "type": "column",
                "color": "#000000",
                "valueField": test[1]

            },
            {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title":test[2] ,
                "type": "column",
                "color": "#000000",
                "valueField": test[2]

            }
            ],

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

    monthlysourceFunction:function(){
        console.log("-----------",source_data_month);
        var chart = AmCharts.makeChart( "chartmonthlysource", {
        "theme": "light",
            "type": "serial",

          "legend": {
            "horizontalGap": 10,
            "useGraphSettings": true,
            "markerSize": 10
          },
            "dataProvider": source_data_month,
            "valueAxes": [ {
            "stackType": "regular",
            "axisAlpha": 0,
            "gridAlpha": 0,
        //    "labelsEnabled":false,
          } ],
            "graphs": [ {
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
            "fillAlphas": 0.8,
            "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title": test1[0],
            "type": "column",
            "color": "#000000",
            "valueField": test1[0]
          }, {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title":test1[1] ,
                "type": "column",
                "color": "#000000",
                "valueField": test1[1]

            },
            {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": test1[2],
                "type": "column",
                "color": "#000000",
                "valueField":test1[2]

            }
            ],

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



    monthlyhealthoppodataFunction:function(){
        console.log("-----------",current_monthly_health);
        var chart = AmCharts.makeChart( "chartmonthlyhealthoppodata", {
        "theme": "light",
            "type": "serial",

          "legend": {
            "horizontalGap": 10,
            "useGraphSettings": true,
            "markerSize": 10
          },
            "dataProvider": current_monthly_health,
            "valueAxes": [ {
            "stackType": "regular",
            "axisAlpha": 0,
            "gridAlpha": 0,
        //    "labelsEnabled":false,
          } ],
            "graphs": [ {
            "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
            "fillAlphas": 0.8,
            "labelText": "[[value]]",
            "lineAlpha": 0.3,
            "title":"Discovery",
            "type": "column",
            "color": "#000000",
            "valueField":"Discovery"
          }, {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title":"Negotiation",
                "type": "column",
                "color": "#000000",
                "valueField":"Negotiation"

            },
            {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title":"Proposal(Hot)" ,
                "type": "column",
                "color": "#000000",
                "valueField":"Proposal"

            },
            {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "Consultation(Warm)",
                "type": "column",
                "color": "#000000",
                "valueField":"Consultation"

            },
            {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "Lose",
                "type": "column",
                "color": "#000000",
                "valueField":"Lose"

            },
             {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'><b>[[value]]</b></span>",
                 "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "Won",
                "type": "column",
                "color": "#000000",
                "valueField":"Won"

            }
            ],

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



     amcharts_totalsalesmonthly:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        total_sales_months=[]
        var self=this;
        crm_model.call('retrieve_total_sales_per_months').then(function(result)
        {

          if (result == 'None')
              {
                total_sales_months=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    total_sales_months.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----total_sales_months");
                  console.log(total_sales_months)
              }

                setTimeout(function() {self.totalsalesmonthlyFunction();},300);

            });
        },

     amcharts_monthlyhealthoppo:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        current_monthly_health=[]
        var self=this;
        crm_model.call('retrieve_monthly_health_oppo_data').then(function(result)
        {

          if (result == 'None')
              {
                current_monthly_health=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    current_monthly_health.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----health opp");
                  console.log(current_monthly_health)
              }

                setTimeout(function() {self.monthlyhealthoppodataFunction();},300);

            });
        },


    amcharts_leadmonthsource:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        lead_monthly_source=[]
        var self=this;
        crm_model.call('retrieve_monthly_lead_source_data').then(function(result)
        {

          if (result == 'None')
              {
                lead_monthly_source=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    lead_monthly_source.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----health opp");
                  console.log(lead_monthly_product)
              }

                setTimeout(function() {self.monthleadsourceFunction();},300);

            });
        },



    amcharts_leadmonthproduct:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        lead_monthly_product=[]
        var self=this;
        crm_model.call('retrieve_monthly_lead_product_data').then(function(result)
        {

          if (result == 'None')
              {
                lead_monthly_product=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    lead_monthly_product.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----health opp");
                  console.log(lead_monthly_product)
              }

                setTimeout(function() {self.monthleadproductFunction();},300);

            });
        },


     amcharts_leadproducts:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        leads_product=[]
        var self=this;
        crm_model.call('retrieve_leads_product_data').then(function(result)
        {

          if (result == 'None')
              {
                leads_product=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    leads_product.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----health opp");
                  console.log(leads_product)
              }

                setTimeout(function() {self.leadsproductFunction();},300);

            });
        },

    amcharts_opportunityproducts:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        opportunity_product=[]
        var self=this;
        crm_model.call('retrieve_opportunity_product_data').then(function(result)
        {

          if (result == 'None')
              {
                opportunity_product=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    opportunity_product.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----health opp");
                  console.log(opportunity_product)
              }

                setTimeout(function() {self.opportunityproductFunction();},300);

            });
        },

    amcharts_healthopportunities:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        healthy_opportunity=[]
        var self=this;
        crm_model.call('retrieve_healthy_oppo_data').then(function(result)
        {

          if (result == 'None')
              {
                healthy_opportunity=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    healthy_opportunity.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----health opp");
                  console.log(healthy_opportunity)
              }

                setTimeout(function() {self.healthopportunityFunction();},300);

            });
        },

     amcharts_currentmonthleads:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        current_month_data=[]
        var self=this;
        crm_model.call('retrieve_current_month_leads_data').then(function(result)
        {

          if (result == 'None')
              {
                current_month_data=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    current_month_data.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----health opp");
                  console.log(current_month_data)
              }

                setTimeout(function() {self.currentmonthleadsFunction();},300);

            });
        },


    amcharts_currentmonthsource:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        current_month_source_data=[]
        var self=this;
        crm_model.call('retrieve_current_month_source_data').then(function(result)
        {

          if (result == 'None')
              {
                current_month_source_data=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    current_month_source_data.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----health opp");
                  console.log(current_month_source_data)
              }

                setTimeout(function() {self.currentmonthsourceFunction();},300);

            });
        },

    amcharts_currenthealthoppo:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        current_health_oppo_data=[]
        var self=this;
        crm_model.call('retrieve_current_health_opportunity_data').then(function(result)
        {

          if (result == 'None')
              {
                current_health_oppo_data=[]
              }
              else
              {
                  for (var i=0; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    current_health_oppo_data.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----health opp");
                  console.log(current_health_oppo_data)
              }

                setTimeout(function() {self.currenthealthoppoFunction();},300);

            });
        },


        amcharts_monthlyleads:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        leads_data_month=[]
        var self=this;
        crm_model.call('retrieve_monthly_leads_data').then(function(result)
        {

          if (result == 'None')
              {
                leads_data_month=[]
              }
              else
              {
                  for (var i=1; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    leads_data_month.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----months_leads");
                  console.log(leads_data_month)
              }
              test = result[0]

              console.log("----glooooooooooobaalllllliddddddd111",leads_data_month);
              console.log("----glooooooooooobaalllllliddddddd",test);

                setTimeout(function() {self.monthlyleadsFunction();},300);

            });
        },

    amcharts_monthlysource:function(){
        var Model= require('web.Model');
        var crm_model= new Model('crm.lead');
        source_data_month=[]
        var self=this;
        crm_model.call('retrieve_monthly_source_data').then(function(result)
        {

          if (result == 'None')
              {
                source_data_month=[]
              }
              else
              {
                  for (var i=1; result.length>i; i++)
                    {
                    console.log("-----------------------------------");
                    console.log("%s",result[i]);
//
                    source_data_month.push(result[i]);
                    console.log(result[i]);
//
                  };
                  console.log("----months_source");
                  console.log(source_data_month)
              }
              test1 = result[0]

              console.log("----glooooooooooobaalllllliddddddd111",leads_data_month);
              console.log("----glooooooooooobaalllllliddddddd111111",test1);

                setTimeout(function() {self.monthlysourceFunction();},300);

            });
        },


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
            self.amcharts_leadmonthproduct();
            self.amcharts_leadmonthsource();
            self.amcharts_leadproducts();
            self.amcharts_opportunityproducts();
            self.amcharts_healthopportunities();
            self.amcharts_currentmonthleads();
            self.amcharts_currentmonthsource();
            self.amcharts_currenthealthoppo();
            self.amcharts_monthlyleads();
            self.amcharts_monthlysource();
            self.amcharts_monthlyhealthoppo();
            self.amcharts_totalsalesmonthly();

           });
         },




       });
    });









