from odoo import models, fields, api

class HrDashboard(models.Model):
    _name = 'hr.dashboard'
    _description = 'HR Dashboard'

    total_employees = fields.Integer(string='Total Employees', compute='_compute_total_employees')
    employees_on_leave = fields.Integer(string='Employees on Leave', compute='_compute_employees_on_leave')
    total_leave_requests = fields.Integer(string='Total Leave Requests', compute='_compute_total_leave_requests')
    pending_approvals = fields.Integer(string='Pending Approvals', compute='_compute_pending_approvals')
    average_leave_duration = fields.Float(string='Average Leave Duration (days)', compute='_compute_average_leave_duration')
    employees_on_leave_tree = fields.One2many('hr.leave', compute='_compute_employees_on_leave_tree')
    leave_requests_tree = fields.One2many('hr.leave', compute='_compute_leave_requests_tree')

    @api.depends()
    def _compute_total_employees(self):
        self.total_employees = self.env['hr.employee'].search_count([])

    @api.depends()
    def _compute_employees_on_leave(self):
        self.employees_on_leave = self.env['hr.leave'].search_count([('state', '=', 'approved')])

    @api.depends()
    def _compute_total_leave_requests(self):
        self.total_leave_requests = self.env['hr.leave'].search_count([])

    @api.depends()
    def _compute_pending_approvals(self):
        self.pending_approvals = self.env['hr.leave'].search_count([('state', 'in', ['confirm', 'in_review'])])

    @api.depends()
    def _compute_average_leave_duration(self):
        approved_leaves = self.env['hr.leave'].search([('state', '=', 'approved')])
        total_days = sum((leave.end_date - leave.start_date).days + 1 for leave in approved_leaves)
        self.average_leave_duration = total_days / len(approved_leaves) if approved_leaves else 0

    @api.depends()
    def _compute_employees_on_leave_tree(self):
        self.employees_on_leave_tree = self.env['hr.leave'].search([('state', '=', 'approved'), ('start_date', '<=', fields.Date.today()), ('end_date', '>=', fields.Date.today())])

    @api.depends()
    def _compute_leave_requests_tree(self):
        self.leave_requests_tree = self.env['hr.leave'].search([])
