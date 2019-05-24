# -*- coding: utf-8 -*-
#################################################################################

{
  "name"                 :  "POS All Orders List",
  "summary"              :  "POS All Orders List model display all old orders and this model linked with POS order reprint and POS Reorder.",
  "category"             :  "Point Of Sale",
  "version"              :  "3.3.1",
  "sequence"             :  1,
  "author"               :  "Planet Odoo",
  "website"              :  "https://www.odoo.com/page/crm",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'views/pos_orders_view.xml',
                             'views/template.xml',
                            ],
  "qweb"                 :  ['static/src/xml/pos_orders.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}