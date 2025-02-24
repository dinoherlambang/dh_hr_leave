from datetime import timedelta
from odoo import models, fields, api

class HrEmployeeLeaves(models.Model):
    _name = 'hr.employee.leaves'
    _description = 'Employee Leaves Summary'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    total_leave_days = fields.Integer(string='Total Leave Days')
    dashboard_id = fields.Many2one('hr.dashboard', string='Dashboard')

class HrDashboard(models.Model):
    _name = 'hr.dashboard'
    _description = 'HR Dashboard'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    total_leave_days = fields.Integer(string='Total Leave Days')

    total_employees = fields.Integer(string='Total Employees', compute='_compute_total_employees')
    employees_on_leave = fields.Integer(string='Employees on Leave', compute='_compute_employees_on_leave')
    total_leave_requests = fields.Integer(string='Total Leave Requests', compute='_compute_total_leave_requests')
    pending_approvals = fields.Integer(string='Pending Approvals', compute='_compute_pending_approvals')
    average_leave_duration = fields.Float(string='Average Leave Duration (days)', compute='_compute_average_leave_duration')
    employees_on_leave_tree = fields.One2many('hr.leave', 'dashboard_id', string='Employees on Leave This Month', compute='_compute_employees_on_leave_tree', store=True)
    leave_requests_tree = fields.One2many('hr.leave', 'dashboard_id', string='Leave Requests', compute='_compute_leave_requests_tree', store=True)
    departments_tree = fields.One2many('hr.department', 'dashboard_id', string='Leaves this day', compute='_compute_departments_tree', store=True)
    # departments_tree = fields.One2many('hr.department', 'dashboard_id', string='Departments')
    employee_leaves_tree = fields.One2many('hr.employee', 'dashboard_id', string='Total Leaves Taken', compute='_compute_employee_leaves_tree', store=True)

 
    @api.depends('leave_requests_tree.employee_id')
    def _compute_total_employees(self):
        self.total_employees = self.env['hr.employee'].search_count([('active', '=', True)])

    @api.depends('leave_requests_tree.state', 'leave_requests_tree.start_date', 'leave_requests_tree.end_date')
    def _compute_employees_on_leave(self):
        self.employees_on_leave = self.env['hr.leave'].search_count([('state', '=', 'approved')])

    @api.depends('leave_requests_tree.state')
    def _compute_total_leave_requests(self):
        domain = [('state', 'not in', ['cancel'])]
        self.total_leave_requests = self.env['hr.leave'].search_count(domain)

    @api.depends('leave_requests_tree.state')
    def _compute_pending_approvals(self):
        self.pending_approvals = self.env['hr.leave'].search_count([
            ('state', 'in', ['confirm', 'in_review']),
        ])

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

    @api.depends('leave_requests_tree.state')
    def _compute_leave_requests_tree(self):
        self.leave_requests_tree = self.env['hr.leave'].search([
            ('state', 'not in', ['cancel'])
        ])

    @api.depends('leave_requests_tree.state', 'leave_requests_tree.start_date', 'leave_requests_tree.end_date')
    def _compute_departments_tree(self):
        for record in self:
            today = fields.Date.today()
            departments = self.env['hr.department'].search([
                ('leave_date', '=', today)
            ])
            record.departments_tree = [(6, 0, departments.ids)]

    @api.depends('leave_requests_tree.state', 'leave_requests_tree.start_date', 'leave_requests_tree.end_date')
    def _compute_employee_leaves_tree(self):
        for record in self:
            employees = self.env['hr.employee'].search([])
            employee_leaves = []
            for employee in employees:
                total_leave_days = sum((leave.end_date - leave.start_date).days + 1 for leave in employee.leave_ids if leave.state == 'approved')
                employee_leaves.append((0, 0, {'employee_id': employee.id, 'total_leave_days': total_leave_days}))
            record.employee_leaves_tree = employee_leaves
