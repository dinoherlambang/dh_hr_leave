from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    rank = fields.Selection([
        ('junior', 'Junior'),
        ('mid', 'Mid'),
        ('senior', 'Senior'),
        ('lead', 'Lead')
    ], string='Rank')
    allowable_days = fields.Integer(string='Allowable Leave Days', compute='_compute_allowable_days', store=True)
    reviewer_id = fields.Many2one('res.users', string='Review by', domain=lambda self: self._get_reviewer_domain())
    approver_id = fields.Many2one('res.users', string='Approval By', domain=lambda self: self._get_approver_domain())

    @api.depends('rank')
    def _compute_allowable_days(self):
        for record in self:
            if record.rank:
                setting = self.env['hr.leave.settings'].search([('rank', '=', record.rank)], limit=1)
                record.allowable_days = setting.allowable_days if setting else 0

    def _get_reviewer_domain(self):
        reviewer_group = self.env.ref('dh_hr_leave.group_hr_leave_reviewer')
        return [('groups_id', 'in', reviewer_group.id)]

    def _get_approver_domain(self):
        approver_group = self.env.ref('dh_hr_leave.group_hr_leave_approver')
        return [('groups_id', 'in', approver_group.id)]
