from odoo import models, fields, api

class HrDashboard(models.Model):
    _name = 'hr.dashboard'
    _description = 'HR Dashboard'

    total_employees = fields.Integer(string='Total Employees', compute='_compute_total_employees')
    employees_on_leave = fields.Integer(string='Employees on Leave', compute='_compute_employees_on_leave')

    @api.depends()
    def _compute_total_employees(self):
        self.total_employees = self.env['hr.employee'].search_count([])

    @api.depends()
    def _compute_employees_on_leave(self):
        self.employees_on_leave = self.env['hr.leave'].search_count([('state', '=', 'approved')])
