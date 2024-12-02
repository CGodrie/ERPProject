from odoo import models, fields

class Course(models.Model):
    _name = "openacademy.course"
    _description = "Course"

    name = fields.Char(required=True)
    description = fields.Text()
    session_ids = fields.One2many('openacademy.session', 'course_id')