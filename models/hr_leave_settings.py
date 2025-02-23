from odoo import models, fields, api

class HrLeaveSettings(models.Model):
    _name = 'hr.leave.settings'
    _description = 'HR Leave Settings'

    rank = fields.Selection([
        ('junior', 'Junior'),
        ('mid', 'Mid'),
        ('senior', 'Senior'),
        ('lead', 'Lead')
    ], string='Rank', required=True)
    allowable_days = fields.Integer(string='Allowable Leave Days')
