#-*- coding:utf-8 -*-

from odoo import fields,models,api,_
from odoo.tools.translate import _


class hr_employee(models.Model):

    """Simplified Employee Record Interface."""


    _inherit = 'hr.employee'
    @api.one
    def _default_country(self):
        cid = self.env['res.country'].search([('code', '=', 'ET')])
        if cid:
            return cid[0]

    #         for last contract in hr.
    @api.multi
    def _get_latest_contract(self):
        res = {}
        obj_contract = self.env['hr.contract']
        for emp in self:
            contract_ids = obj_contract.search([('employee_id', '=', emp.id), ], order='date_start')
            if contract_ids:
                res[emp.id] = contract_ids[-1:][0]
            else:
                res[emp.id] = False
        return res

    @api.multi
    def _get_id_from_contract(self):
        res = []
        for contract in self.env['hr.contract'].browse(self._ids):
            res.append(contract.employee_id.id)

        return res


    contract_id = fields.Many2one('hr.contract',compute='_get_latest_contract', string='Contract',
                                  help='Latest contract of the employee')
    job_id = fields.Many2one('hr.job',related='contract_id.job_id',string="Job",
                             method=True, readonly=True, )

    _sql_constraints = [
        ('unique_identification_id', 'unique(identification_id)',
         _('Official Identifications must be unique!')),
    ]



hr_employee()


class hr_contract(models.Model):

    _inherit = 'hr.contract'

    @api.multi
    def _default_employee(self):
        context = self._context
        if context != None:
            e_ids = context.get('search_default_employee_id', False)
            if e_ids:

                return e_ids[0]
    employee_dept_id = fields.Many2one('hr.department',related='employee_id.department_id',
                                       string="Default Dept Id")




    @api.multi
    @api.onchange('employee_id')
    def onchange_employee_id(self):

        dom = {
            'job_id': [],
        }
        val = {
            'employee_dept_id': [],
        }
        if self.employee_id:
            dept_id = self.employee_id.department_id.id
            dom['job_id'] = [('department_id', '=', dept_id)]
            val['employee_dept_id'] = dept_id
        return {'value': val, 'domain': dom}


class hr_job(models.Model):

    # for search and count the contract which all are done.
    @api.multi
    def _no_of_contracts(self):
        res = {}
        for job in self:
            contract_ids = self.env['hr.contract'].search([('job_id', '=', job.id),('state', '!=', 'done')])
            nb = len(contract_ids or [])
            res[job.id] = {
                'no_of_employee': nb,
                'expected_employees': nb + job.no_of_recruitment,
            }
        return res

    @api.multi
    def _get_job_position(self):
        res = []
        for contract in self.contract_id:
            if contract.job_id:
                res.append(contract.job_id.id)
        return res


    _inherit = 'hr.job'


    no_of_employee = fields.Integer(compute='_no_of_contracts', string="Current Number of Employees",
                                    help='Number of employees currently occupying this job position.',
                                    store={'hr.contract': (_get_job_position, ['job_id'], 10),
                                           }, multi='no_of_employee')
    expected_employees = fields.Integer(compute='_no_of_contracts', string='Total Forecasted Employees',
                                        help='Expected number of employees for this job position after new recruitment.',
                                        store={
                                            'hr.job': (lambda self, cr, uid, ids, c=None: ids, ['no_of_recruitment'], 10),
                                            'hr.contract': (_get_job_position, ['job_id'], 10),
                                        },multi='no_of_employee')

