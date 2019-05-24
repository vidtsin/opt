# -*- coding: utf-8 -*-
#################################################################################
#################################################################################
{
  "name"                 :  "POS Order Return",
  "summary"              :  "This module is use to Return orders in running point of sale session.",
  "category"             :  "Point Of Sale",
  "version"              :  "3.4.2",
  "sequence"             :  1,
  "author"               :  "Planet Odoo",
  "website"              :  "https://www.odoo.com/page/crm",
  "depends"              :  ['pos_orders'],
  "data"                 :  [
                             'views/pos_order_return_view.xml',
                             'views/template.xml',
                            ],
  "qweb"                 :  ['static/src/xml/pos_order_return.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}