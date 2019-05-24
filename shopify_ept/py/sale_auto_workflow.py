from odoo import models,fields,api
class sale_auto_workflow_configuration(models.Model):
    _name="sale.auto.workflow.configuration"
    
    financial_status=fields.Selection([('pending','The finances are pending'),
                                       ('authorized','The finances have been authorized'),
                                        ('partially_paid','The finances have been partially paid'),
                                        ('paid','The finances have been paid'),
                                        ('partially_refunded','The finances have been partially refunded'),
                                        ('refunded','The finances have been refunded'),
                                        ('voided','The finances have been voided')
                                        ],default="paid",required=1)
    auto_workflow_id=fields.Many2one("sale.workflow.process.ept","Auto Workflow Id",required=1)
    
    shopify_instance_id=fields.Many2one("shopify.instance.ept","Instance",required=1)
    _sql_constraints=[('_workflow_unique_constraint','unique(financial_status,shopify_instance_id)',"Financial status must be unique in the list")]
    
    