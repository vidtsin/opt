
from odoo import api, fields, models,tools, _



class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    upload_attachment_id = fields.Many2one('crm.lead','Upload Document')
    document_type = fields.Char('Document type')
    category = fields.Char('Category')
    verification = fields.Char('Verification')
    submitted_to = fields.Char('Submitted To')
    attachments = fields.Binary("Attachments")


# class Faculty(models.Model):
#     _name = 'faculty.details'
#
#     name = fields.Char("Name")
#     faculty_ids= fields.One2many('program.details','faculty_id','Faculty')

class OtherRequirement(models.Model):
    _name = 'other.requirement'

    name = fields.Char(string='Name')


class MultiProgramDetails(models.Model):
    _name = 'multi.program.details'

    # program_id = fields.Many2one('crm.lead',string="program")
    # program_ids=fields.Many2one('program.details',string="program")
    # checkbox=fields.Boolean(' ')
    # start_date = fields.Char('Start Date')
    # start_date_2 = fields.Char('Start Date 2')
    # start_date_3 = fields.Char('Start Date 3')


class crm(models.Model):
    _inherit = 'crm.lead'
    _rec_name = 'name'

    # total_program_cost = fields.Float(related='program.total', store=True)
    source_url = fields.Selection([('website', 'Website'),
                                  ('call', 'Call'),
                                  ('walk_in', 'Walk In')],
                                 string='source')
    form_filled = fields.Selection([('asked_question', 'Request Information'),
                                    ('requested_catalog', 'Requested Catelog'),
                                    ('book_a_tour', 'Book A Tour'),
                                    ('apply_now', 'Apply Now')],
                                   string='Form Filled')

    academic_requirements = fields.Boolean(string="academic requirements")
    assessment_test = fields.Boolean(string="assessment test")
    seat_deposit = fields.Boolean(string="seat deposit")
    support_academic_document = fields.Boolean(string="Support Academic Required")
    assessment_test_completed = fields.Boolean(string="Assessment Test Completed")
    seat_deposit_completed = fields.Boolean(string="Seat Deposit Completed")
    agreement_signed = fields.Boolean(string="Agreement Signed")
    other_requirements = fields.Many2one('other.requirement', 'Other Requirement')
    checkbox = fields.Boolean('Checkbox')
    upload_attachment_ids = fields.One2many('ir.attachment','upload_attachment_id', string='Upload Documents')
    disqualified = fields.Boolean('Disqualified')
    rating = fields.Selection([('hot','Hot'),
                               ('warm', 'Warm'),
                               ('cold', 'Cold')],
                              string="Rating")
    checked =fields.Boolean(string="Checked")
    # program_line_ids = fields.One2many('multi.program.details','program_id', string="Program")


# class Program_details(models.Model):
#     _name = 'program.details'
#
#     lead_by_diploma = fields.Boolean('Diploma')
#     lead_by_certification = fields.Boolean('Certification')
#     faculty_id = fields.Many2one('faculty.details','Faculty')