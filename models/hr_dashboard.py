from datetime import timedelta
from odoo import models, fields, api

class HrDashboard(models.Model):
    _name = 'hr.dashboard'
    _description = 'HR Dashboard'

    total_employees = fields.Integer(string='Total Employees', compute='_compute_dashboard_data')
    employees_on_leave = fields.Integer(string='Employees on Leave', compute='_compute_dashboard_data')
    total_leave_requests = fields.Integer(string='Total Leave Requests', compute='_compute_dashboard_data')
    pending_approvals = fields.Integer(string='Pending Approvals', compute='_compute_dashboard_data')
    average_leave_duration = fields.Float(string='Average Leave Duration (days)', compute='_compute_dashboard_data')
    employees_on_leave_ids = fields.Many2many('hr.leave', string='Employees on Leave This Month', compute='_compute_dashboard_data')
    leave_request_ids = fields.Many2many('hr.leave', string='Leave Requests', compute='_compute_dashboard_data')
    employee_leaves_ids = fields.Many2many(
        'hr.employee',
        string='Employee Leaves Summary',
        compute='_compute_dashboard_data'
    )

    @api.depends()
    def _compute_dashboard_data(self):
        for record in self:
            # Total Employees
            record.total_employees = self.env['hr.employee'].search_count([('active', '=', True)])

            # Leave data
            today = fields.Date.today()
            start_of_month = today.replace(day=1)
            if today.month == 12:
                end_of_month = today.replace(day=31)
            else:
                end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

            # Current leaves
            current_leaves = self.env['hr.leave'].search([
                ('state', '=', 'approved'),
                ('date_from', '<=', end_of_month),
                ('date_to', '>=', start_of_month)
            ])
            record.employees_on_leave_ids = current_leaves

            # All valid leave requests
            leave_requests = self.env['hr.leave'].search([
                ('state', 'not in', ['cancel'])
            ])
            record.leave_request_ids = leave_requests

            # Compute statistics
            record.employees_on_leave = len(current_leaves)
            record.total_leave_requests = len(leave_requests)
            record.pending_approvals = self.env['hr.leave'].search_count([
                ('state', 'in', ['confirm', 'in_review'])
            ])

            # Average duration
            approved_leaves = self.env['hr.leave'].search([
                ('state', '=', 'approved')
            ])
            if approved_leaves:
                total_days = sum((leave.date_to - leave.date_from).days + 1 for leave in approved_leaves)
                record.average_leave_duration = round(total_days / len(approved_leaves), 2)
            else:
                record.average_leave_duration = 0.0

            # Get all employees including those with zero leaves
            employees = self.env['hr.employee'].search([('active', '=', True)])
            record.employee_leaves_ids = employees
