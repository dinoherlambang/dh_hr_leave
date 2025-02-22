from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    leave_setting_ids = fields.One2many('hr.leave.settings', 'employee_id', string='Leave Settings')
