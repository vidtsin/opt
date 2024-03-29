from odoo import models, fields, api


class resource_members(models.Model):
    _name = "resource.members"

    resource_member_id = fields.Many2one('resource.request', String='Members')
    name= fields.Many2one('hr.employee', string='Name')
    work_phone= fields.Char('Work Phone')
    work_email= fields.Char('Work Email')
    department= fields.Char('Department')
    job_title= fields.Char('Job Title')
    manager= fields.Char('Manager')