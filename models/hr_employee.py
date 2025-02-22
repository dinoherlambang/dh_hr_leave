from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    leave_setting_ids = fields.One2many('hr.leave.settings', 'employee_id', string='Leave Settings')
    rank = fields.Selection([
        ('junior', 'Junior'),
        ('mid', 'Mid'),
        ('senior', 'Senior'),
        ('lead', 'Lead')
    ], string='Rank')
    allowable_days = fields.Integer(string='Allowable Leave Days', compute='_compute_allowable_days', store=True)

    @api.depends('rank')
    def _compute_allowable_days(self):
        for record in self:
            if record.rank:
                setting = self.env['hr.leave.settings'].search([('rank', '=', record.rank)], limit=1)
                record.allowable_days = setting.allowable_days if setting else 0
