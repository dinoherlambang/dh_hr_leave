from odoo import models, fields

class HrLeaveApproval(models.Model):
    _name = 'hr.leave.approval'
    _description = 'HR Leave Approval'

    approval_manager_id = fields.Many2one('res.users', string='Reviewer')
    approval_head_id = fields.Many2one('res.users', string='Approver')
    employee_id = fields.Many2one('hr.employee', string='Employee')
