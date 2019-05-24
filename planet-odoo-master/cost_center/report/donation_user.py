from odoo import tools
from odoo import models, fields,api
import xlwt
import StringIO
import unicodecsv as csv
class donation_report(models.TransientModel):
    _name = 'donation.report.user'

    Header = ['']
    @api.multi
    def download_my_donation_report_xlsx(self):
        csvfile = StringIO.StringIO()
        recordcount = 0
        w = csv.writer(csvfile)
        w.writerow(self.Header)

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet 1')
        borders = xlwt.Borders()
        donation = self.env['donation.donation'].search([('create_uid','=',self.env.uid)])
        if donation:
            for don_id in donation:
                recordcount += 1
                modified_row = []
                modified_row.append (don_id.partner_id.name or '')
        return

