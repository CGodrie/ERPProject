from odoo import models, fields, api
from datetime import datetime

class Person(models.Model):
    _name = "openacademy.person"
    _description = "Person"

    name = fields.Char(required=True)
    birthday_date = fields.Date()
    age = fields.Integer(compute='_compute_age', store=True)

    @api.depends("birthday_date")
    def _compute_age(self):
        for person in self:
            if person.birthday_date:
                birth_date = fields.Date.from_string(person.birthday_date)
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                person.age = str(age)
            else:
                person.age = 0