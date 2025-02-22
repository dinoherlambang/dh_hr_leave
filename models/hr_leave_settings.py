from odoo import models, fields, api

class HrLeaveSettings(models.Model):
    _name = 'hr.leave.settings'
    _description = 'HR Leave Settings'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    rank = fields.Selection([
        ('junior', 'Junior'),
        ('mid', 'Mid'),
        ('senior', 'Senior'),
        ('lead', 'Lead')
    ], string='Rank', required=True)
    allowable_days = fields.Integer(string='Allowable Leave Days', compute='_compute_allowable_days', store=True)

    @api.depends('rank')
    def _compute_allowable_days(self):
        for record in self:
            if record.rank:
                setting = self.env['hr.leave.settings'].search([('rank', '=', record.rank)], limit=1)
                record.allowable_days = setting.allowable_days if setting else 0
