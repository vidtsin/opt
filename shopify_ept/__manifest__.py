{
    'name': 'Shopify-Odoo Connector',
    'version': '10.0',
    'category': 'Sales',
    'summary' : 'Integrate & Manage your all your Shopify operations from Odoo',
    'description': """
        This module used to smoothly integrate your Shopify account with Odoo. \n

        After installation of our module, you can manager following Shopify operations in Odoo, \n
  
        Our module supports following features related to Shopify. \n

    * Shopify Instance Configuration & Setup \n
    * Multi Shopify Instance setup \n
    *.Sync Shopify Products With Odoo Products \n
    * Export Product, Inventory, Images \n
    * Update Product to Shopify \n
    * Import Sale Order from Shopify \n
    * Export Shipping Details with tracking no. \n
    * Cancel order to Shopify \n
    * Export Custom Collection,Smart Collection \n
    * Update Collection \n
    * Import Collection \n
    * Auto Stock/Orders/Shipping status export \n
    * Create Invoice / Payment / Delivery Order in Odoo (Automatically) \n
    
====================================================================

For support on this module contact us at info@emiprotechnologies.com \n

To subscribe our support packages visit following link, \n

http://www.emiprotechnologies.com/odoo/support \n 

Visit following link to find our other cool apps to shape your system . \n

https://www.odoo.com/apps/modules?author=Emipro%20Technologies%20Pvt.%20Ltd. \n

For more information about us, visit www.emiprotechnologies.com \n
    """,

    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com/',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',
    'depends': ['sale_stock', 'auto_invoice_workflow_ept', 'delivery', 'web','base','point_of_sale', 'product'],
    'init_xml': [],
    'data': [
             'security/group.xml',
             'view/shopify_instance_view.xml',
             'view/res_config_view.xml',
             'view/res_partner.xml',
             'view/sale_order.xml',
             'view/processes.xml',
             'view/product_view.xml',
             'view/shopify_job_log.xml',
             'view/variants_view.xml',
             'view/stock_quant_package_view.xml',
             'view/stock_picking_view.xml',
             'view/account_invoice_view.xml',
             'view/product_category_view.xml',
             'view/ir_cron.xml',
             'view/shopify_cancel_order_wizard_view.xml',
             'view/shopify_collection_view.xml',
             'view/pos_view.xml',

             'view/web_templates.xml',
             'view/shopify_reorder_wizard_view.xml',
             'view/sale_workflow_config.xml',
             'view/shopify_operation.xml',
             # 'report/sale_report_view.xml',
             # 'report/product_report.xml',
             'data/shopify.operations.ept.csv',
             'security/ir.model.access.csv',
             ],
    'demo_xml': [],
    'images': ['static/description/main_screen.png'],
    'installable': True,
    'auto_install': False,
    'application' : True,
    'price': 299.00,
    'currency': 'EUR',

}
