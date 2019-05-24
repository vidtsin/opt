from odoo import api, fields, models, _


class Crm_lead(models.Model):
    _inherit = 'crm.lead'


    program = fields.Many2one('program.details','Program')
    program_1 = fields.Many2one('program.details', 'Program')
    program_2 = fields.Many2one('program.details', 'Program')
    program_3 = fields.Many2one('program.details', 'Program')



class Program_details(models.Model):
    _name = 'program.details'


    name=fields.Char('Program Name')
    international=fields.Boolean('International')
    domestic=fields.Boolean('Domestic')


    internal_ref=fields.Char('Internal Reference')
    adm_require=fields.Char('Admission Requirements')
    other_require=fields.Char('Other Requirements')
    dur_weeks=fields.Integer('Duration/Weeks')
    dur_hours=fields.Integer('Duration/Hours')
    schedule=fields.Char('Class Schedule')
    start_date=fields.Char('Program Start Date')
    deadline=fields.Char('Deadline to Apply')
    scholarship=fields.Char('Scholarship')

    currency_id = fields.Many2one('res.currency', 'Currency',default=lambda self: self.env.user.company_id.currency_id.id,required=True)
    tution_fee=fields.Float('Tuition Fee')
    textbook_fee=fields.Float('Textbook Fee')
    seat_deposit_fee=fields.Float('Seat Deposit Fee')
    lab_fee=fields.Float('Lab/Clinical Fee')
    lab_supply_fee=fields.Float('Lab Supply Fee')
    maj_equip_fee=fields.Float('Major Equipment Fee')
    prof_exam_fee=fields.Float('Professional Exam Fee')


    other_com_fee=fields.Float('Other Compulsory Fee')
    opt_fee=fields.Float('Optional Fee')
    reg_fee=fields.Float('Registration Fee')
    uniform_fee=fields.Float('Uniform & Equipment Fee')
    field_trip=fields.Float('Field Trip Fee')
    inter_fee=fields.Float('International Fee')
    application_fee=fields.Float('Application Fee For International Students Only')
    total=fields.Float('Totals',compute='_calculate_total')
    lead_by_diploma = fields.Boolean('Diploma')

    lead_by_certification = fields.Boolean('Certification')
    faculty_id = fields.Many2one('faculty.details','Faculty')

    def _calculate_total(self):
        for rec in self:
            rec.total=rec.tution_fee + rec.textbook_fee + rec.seat_deposit_fee + rec.lab_fee + rec.lab_supply_fee \
            + rec.maj_equip_fee + rec.prof_exam_fee + rec.other_com_fee + rec.opt_fee + rec.reg_fee \
            + rec.uniform_fee + rec.field_trip + rec.inter_fee + rec.application_fee





