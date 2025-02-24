from odoo import models, fields, api
from datetime import date, timedelta

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    dashboard_id = fields.Many2one('hr.dashboard', string='Dashboard')
    leave_date = fields.Date(string='Leave Date')
    total_leave_requests = fields.Integer(string='Total Leave Requests', compute='_compute_leave_counts')
    approved_leaves = fields.Integer(string='Approved Leaves', compute='_compute_leave_counts')
    pending_leaves = fields.Integer(string='Pending Leaves', compute='_compute_leave_counts')
    
    @api.depends('member_ids')
    def _compute_leave_counts(self):
        for department in self:
            employees = department.member_ids
            start_of_month = date.today().replace(day=1)
            end_of_month = date.today().replace(day=1).replace(month=date.today().month + 1) - timedelta(days=1)
            leaves = self.env['hr.leave'].search([
                ('employee_id', 'in', employees.ids),
                ('start_date', '>=', start_of_month),
                ('end_date', '<=', end_of_month),
                ('state', 'in', ['confirm', 'in_review', 'approved'])
            ])
            
            department.total_leave_requests = len(leaves)
            department.approved_leaves = len(leaves.filtered(lambda l: l.state == 'approved'))
            department.pending_leaves = len(leaves.filtered(lambda l: l.state in ['confirm', 'in_review']))
