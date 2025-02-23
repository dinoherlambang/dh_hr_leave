from odoo import models, fields

class HrLeaveApproval(models.Model):
    _name = 'hr.leave.approval'
    _description = 'HR Leave Approval'

    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    approver_id = fields.Many2one('res.users', string='Approver')
    employee_id = fields.Many2one('hr.employee', string='Employee')
