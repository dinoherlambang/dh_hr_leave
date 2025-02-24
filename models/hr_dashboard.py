from datetime import timedelta
from odoo import models, fields, api

class HrDashboard(models.Model):
    _name = 'hr.dashboard'
    _description = 'HR Dashboard'

    total_employees = fields.Integer(string='Total Employees', compute='_compute_total_employees')
    employees_on_leave = fields.Integer(string='Employees on Leave', compute='_compute_employees_on_leave')
    total_leave_requests = fields.Integer(string='Total Leave Requests', compute='_compute_total_leave_requests')
    pending_approvals = fields.Integer(string='Pending Approvals', compute='_compute_pending_approvals')
    average_leave_duration = fields.Float(string='Average Leave Duration (days)', compute='_compute_average_leave_duration')
    employees_on_leave_tree = fields.One2many('hr.leave', 'dashboard_id', string='Employees on Leave This Month', compute='_compute_employees_on_leave_tree', store=True)
    leave_requests_tree = fields.One2many('hr.leave', 'dashboard_id', string='Leave Requests', compute='_compute_leave_requests_tree', store=True)

    # @api.depends()
    # def _compute_total_employees(self):
    #     self.total_employees = self.env['hr.employee'].search_count([])
    @api.depends('leave_requests_tree.employee_id')
    def _compute_total_employees(self):
        self.total_employees = self.env['hr.employee'].search_count([('active', '=', True)])


    # @api.depends()
    # def _compute_employees_on_leave(self):
    #     self.employees_on_leave = self.env['hr.leave'].search_count([('state', '=', 'approved')])
    # Add dependencies to trigger recomputation
    @api.depends('leave_requests_tree.state', 'leave_requests_tree.start_date', 'leave_requests_tree.end_date')
    def _compute_employees_on_leave(self):
        self.employees_on_leave = self.env['hr.leave'].search_count([('state', '=', 'approved')])


    # @api.depends()
    # def _compute_total_leave_requests(self):
    #     self.total_leave_requests = self.env['hr.leave'].search_count([])
    @api.depends('leave_requests_tree.state')
    def _compute_total_leave_requests(self):
        domain = [('state', 'not in', ['cancel'])]
        self.total_leave_requests = self.env['hr.leave'].search_count(domain)

    # @api.depends()
    # def _compute_pending_approvals(self):
    #     self.pending_approvals = self.env['hr.leave'].search_count([('state', 'in', ['confirm', 'in_review'])])
    @api.depends('leave_requests_tree.state')
    def _compute_pending_approvals(self):
        self.pending_approvals = self.env['hr.leave'].search_count([
            ('state', 'in', ['confirm', 'in_review']),
        ])

    # @api.depends()
    # def _compute_average_leave_duration(self):
    #     approved_leaves = self.env['hr.leave'].search([('state', '=', 'approved')])
    #     total_days = sum((leave.end_date - leave.start_date).days + 1 for leave in approved_leaves)
    #     self.average_leave_duration = total_days / len(approved_leaves) if approved_leaves else 0

    @api.depends('leave_requests_tree.state', 'leave_requests_tree.start_date', 'leave_requests_tree.end_date')
    def _compute_average_leave_duration(self):
        approved_leaves = self.env['hr.leave'].search([
            ('state', '=', 'approved'),
        ])
        if approved_leaves:
            total_days = sum((leave.end_date - leave.start_date).days + 1 for leave in approved_leaves)
            self.average_leave_duration = round(total_days / len(approved_leaves), 2)
        else:
            self.average_leave_duration = 0.0

    # @api.depends()
    # def _compute_employees_on_leave_tree(self):
    #     self.employees_on_leave_tree = self.env['hr.leave'].search([('state', '=', 'approved'), ('start_date', '<=', fields.Date.today()), ('end_date', '>=', fields.Date.today())])
    # @api.depends('leave_requests_tree.state', 'leave_requests_tree.start_date', 'leave_requests_tree.end_date')
    # def _compute_employees_on_leave_tree(self):
    #     today = fields.Date.today()
    #     self.employees_on_leave_tree = self.env['hr.leave'].search([
    #         ('state', '=', 'approved'),
    #         ('start_date', '<=', today),
    #         ('end_date', '>=', today)
    #     ])

    @api.depends('leave_requests_tree.state', 'leave_requests_tree.start_date', 'leave_requests_tree.end_date')
    def _compute_employees_on_leave_tree(self):
        for record in self:
            today = fields.Date.today()
            start_of_month = today.replace(day=1)
            # Get last day of current month
            if today.month == 12:
                end_of_month = today.replace(day=31)
            else:
                end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
                
            leaves = self.env['hr.leave'].search([
                ('state', '=', 'approved'),
                ('start_date', '<=', end_of_month),
                ('end_date', '>=', start_of_month)
            ])
            record.employees_on_leave_tree = [(6, 0, leaves.ids)]


    # @api.depends()
    # def _compute_leave_requests_tree(self):
    #     self.leave_requests_tree = self.env['hr.leave'].search([])
    @api.depends('leave_requests_tree.state')
    def _compute_leave_requests_tree(self):
        self.leave_requests_tree = self.env['hr.leave'].search([
            ('state', 'not in', ['cancel'])
        ])
