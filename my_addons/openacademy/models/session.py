from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Session(models.Model):
    _name = "openacademy.session"
    _description = "Session"

    name = fields.Char()
    date_start = fields.Date(required=True)
    date_stop = fields.Date(required=True)
    teacher_id = fields.Many2one('openacademy.person')
    student_ids = fields.Many2many('openacademy.person')
    rate = fields.Integer()
    course_id = fields.Many2one('openacademy.course')

    len_student = fields.Integer(compute='_compute_len_students', store=True)

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')], default='draft')

    # _sql_constraints = [
    #     ('name_unique', 'UNIQUE(name)', 'The session name must be unique!')
    # ]

    @api.constrains('name')
    def _constrains_name(self):
        for session in self:
            if self.search_count([('name', '=', session.name)]) > 1:
                raise ValidationError("Session name must be unique")

    @api.constrains('date_start', 'date_stop')
    def _check_dates(self):
        for session in self:
            if session.date_start > session.date_stop:
                raise ValidationError("The start date cannot be after the stop date.")

    @api.depends('student_ids')
    def _compute_len_students(self):  
        for session in self:
            session.len_student = len(session.student_ids)

    @api.depends('course_id', 'date_start')
    def _compute_name(self):
        for session in self:
            if session.course_id and session.date_start:
                session.name = f"Session {session.course_id.name} - {session.date_start.strftime('%d/%m/%Y')}"

    
    def copy(self, default=None):
        default = dict(default or {})
        if self.search_count([('name', '=', self.name)]) > 0:
            default['name'] = 'NEW %s' % (self.name)
        return super().copy(default)

    def action_confirm(self):
        for session in self:
            session.state = 'confirm'

    def action_done(self):
        for session in self:
            session.state = 'done'

    def action_cancel(self):
        for session in self:
            session.state = 'cancel'

    def action_draft(self):
        for session in self:
            session.state = 'draft'