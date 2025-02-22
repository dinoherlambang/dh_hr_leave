from odoo import models, fields

class HrLeaveApproval(models.Model):
    _name = 'hr.leave.approval'
    _description = 'HR Leave Approval'

    approval_manager_id = fields.Many2one('res.users', string='Approval Manager')
    approval_head_id = fields.Many2one('res.users', string='Approval Head')
    employee_id = fields.Many2one('hr.employee', string='Employee')
