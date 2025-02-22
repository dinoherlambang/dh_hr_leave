from odoo import models, fields, api
from odoo.exceptions import UserError

class HrLeave(models.Model):
    _name = 'hr.leave'
    _description = 'HR Leave'

    name = fields.Char(string='Description', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_approve(self):
        self._check_allowable_days()
        self.write({'state': 'approved'})
        self.send_notification()

    def action_refuse(self):
        self.write({'state': 'refused'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def send_notification(self):
        for leave in self:
            template = self.env.ref('dh_hr_leave.leave_approval_notification')
            self.env['mail.template'].browse(template.id).send_mail(leave.id, force_send=True)
            # Create an activity
            self.env['mail.activity'].create({
                'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.leave')], limit=1).id,
                'res_id': leave.id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': 'Leave Request Approved',
                'note': 'Your leave request from %s to %s has been approved.' % (leave.start_date, leave.end_date),
                'user_id': leave.employee_id.user_id.id,
                'date_deadline': fields.Date.today(),
            })

    def _check_allowable_days(self):
        leave_days = (self.end_date - self.start_date).days + 1
        rank = self.employee_id.job_id.name.lower()
        allowable_days = self.env['hr.leave.settings'].search([('rank', '=', rank)], limit=1).allowable_days
        if leave_days > allowable_days:
            raise UserError('You cannot request more than %s days of leave.' % allowable_days)
