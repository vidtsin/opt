from odoo import models, fields, api


class emp_education(models.Model):
    _name = "emp.education"

    degree = fields.Char('Degree')
    institute = fields.Char('Institute')
    passing_year = fields.Integer('Passing Year')
    grade = fields.Char('Grade/Class')
    subject = fields.Char('Major Subjects')
    edu_id = fields.Many2one('hr.employee', String='Education')

    emp_id = fields.Many2one('hr.employee', String='Employee')
    organization = fields.Char('Organization')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    responsibilities = fields.Char('Responsibilities')
    supervisor = fields.Char('Supervisor')

    family_id = fields.Many2one('hr.employee', String='Family')
    relation = fields.Char('Relation')
    name = fields.Char('Name')
    age = fields.Integer('Age')

    medical_id = fields.Many2one('hr.employee', String='Medical')
    medical_test = fields.Char('Medical Test')
    result = fields.Char('Result')

    skill_id = fields.Many2one('hr.employee', String='Skill')
    skill = fields.Char('Skill')
    rating = fields.Integer('Rate out of 10')


