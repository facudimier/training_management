from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TrainingCourse(models.Model):
    _name = "training.course"
    _description = "Training Course"

    name = fields.Char(string="Course Name", required=True)
    description = fields.Text(string="Description")
    duration_hours = fields.Integer(string="Duration (hours)")
    active = fields.Boolean(default=True)

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    duration_days = fields.Integer(
        string="Duration (days)",
        compute="_compute_duration_days",
        store=True
    )

    student_count = fields.Integer(
    string="Cantidad de alumnos",
    compute="_compute_student_count",
    store=True,
    )

    color = fields.Integer(
    string="Color",
    compute="_compute_color_from_state",
    store=True
    )


    #otro modelo
    state = fields.Selection(
      selection=[
        ("draft", "Borrador"),
        ("active", "Activo"),
        ("archived", "Archivado"),
      ],
     string="Estado",
     default="draft",
     required=True,
    )

    def action_set_active(self):
        for record in self:
            record.state = "active"

    def action_set_draft(self):
        for record in self:
            record.state = "draft"

    def action_set_archived(self):
        for record in self:
            record.state = "archived"

#los siguiente es un One2many, para unir los estudiantes con los cursos.
    student_ids = fields.One2many(
        comodel_name="training.student",
        inverse_name="course_id",
        string="Alumnos",
    )



#APIs
    @api.depends("start_date", "end_date")
    def _compute_duration_days(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration_days = (
                    record.end_date - record.start_date
                ).days + 1
            else:
                record.duration_days = 0


    @api.depends("student_ids")
    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.student_ids)


    @api.depends('state')
    def _compute_color_from_state(self):
        for rec in self:
            if rec.state == 'draft':
                rec.color = 2   # gris
            elif rec.state == 'active':
                rec.color = 10  # verde
            else:
                rec.color = 1   # rojo

  # 🔴 VALIDACIÓN
    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for record in self:
            if (
                record.start_date
                and record.end_date
                and record.end_date < record.start_date
            ):
                raise ValidationError(
                    "La fecha de fin no puede ser anterior a la fecha de inicio."
                )
