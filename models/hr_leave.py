from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class HrLeave(models.Model):
    _name = 'hr.leave'
    _description = 'HR Leave'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, readonly=True, default='New', track_visibility='onchange')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, track_visibility='onchange')
    date_from = fields.Date(string='Start Date', required=True, track_visibility='onchange')
    date_to = fields.Date(string='End Date', required=True, track_visibility='onchange')
    description = fields.Text(string='Description', track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', track_visibility='onchange')
    approval_id = fields.Many2one('hr.leave.approval', string='Approval')
    dashboard_id = fields.Many2one('hr.dashboard', string='Dashboard', compute='_compute_dashboard_id', store=True, readonly=False)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.leave') or 'New'
        record = super(HrLeave, self).create(vals)
        if record.employee_id:
            approval = self.env['hr.leave.approval'].create({
                'reviewer_id': record.employee_id.reviewer_id.id,
                'approver_id': record.employee_id.approver_id.id,
            })
            record.approval_id = approval.id
        return record

    def write(self, vals):
        res = super(HrLeave, self).write(vals)
        for record in self:
            if record.employee_id and record.approval_id:
                record.approval_id.write({
                    'reviewer_id': record.employee_id.reviewer_id.id,
                    'approver_id': record.employee_id.approver_id.id,
                })
        return res

    def action_confirm(self):
        self.write({'state': 'confirm'})
        # Clear any existing activities
        self.activity_ids.unlink()
        # Create activity only for reviewer
        if self.approval_id and self.approval_id.reviewer_id:
            model_id = self.env['ir.model']._get('hr.leave').id
            self.env['mail.activity'].create({
                'res_model_id': model_id,
                'res_model': 'hr.leave',
                'res_id': self.id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': 'Leave Request needs Review',
                'note': 'A leave request from %s to %s has been confirmed.' % (self.date_from, self.date_to),
                'user_id': self.approval_id.reviewer_id.id,
                'date_deadline': fields.Date.today(),
            })

    def action_approve(self):
        self._check_allowable_days()
        self.write({'state': 'approved'})
        self.send_notification()

    def action_refuse(self):
        self.write({'state': 'refused'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_in_review(self):
        self.write({'state': 'in_review'})
        # Clear any existing activities
        self.activity_ids.unlink()
        # Create activity only for approver
        if self.approval_id and self.approval_id.approver_id:
            model_id = self.env['ir.model']._get('hr.leave').id
            self.env['mail.activity'].create({
                'res_model_id': model_id,
                'res_model': 'hr.leave',
                'res_id': self.id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': 'Leave Request needs Approval',
                'note': 'A leave request from %s to %s is in review.' % (self.date_from, self.date_to),
                'user_id': self.approval_id.approver_id.id,
                'date_deadline': fields.Date.today(),
            })

    def action_draft(self):
        self.write({'state': 'draft'})

    def send_notification(self):
        for leave in self:
            template = self.env.ref('dh_hr_leave.leave_approval_notification')
            self.env['mail.template'].browse(template.id).send_mail(leave.id, force_send=True)

    def _check_allowable_days(self):
        leave_days = (self.date_to - self.date_from).days + 1
        rank = self.employee_id.rank
        allowable_days = self.employee_id.allowable_days
        if leave_days > allowable_days:
            raise UserError('You cannot request more than %s days of leave.' % allowable_days)

    @api.constrains('employee_id', 'date_from', 'date_to')
    def _check_overlapping_leaves(self):
        for record in self:
            overlapping_leaves = self.env['hr.leave'].search([
                ('employee_id', '=', record.employee_id.id),
                ('id', '!=', record.id),
                ('state', 'not in', ['cancel', 'refused']),
                ('date_from', '<=', record.date_to),
                ('date_to', '>=', record.date_from),
            ])
            if overlapping_leaves:
                raise ValidationError('You cannot request leave during this period as it overlaps with another leave request.')

    # @api.depends('state')
    # def _compute_dashboard_id(self):
    #     for record in self:
    #         record.dashboard_id = self.env['hr.dashboard'].search([], limit=1).id

    @api.depends('state')
    def _compute_dashboard_id(self):
        dashboard = self.env['hr.dashboard'].search([], limit=1)
        for record in self:
            record.dashboard_id = dashboard.id if dashboard else False

