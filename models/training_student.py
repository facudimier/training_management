from odoo import models, fields


class TrainingStudent(models.Model):
    _name = "training.student"
    _description = "Training Student"

    name = fields.Char(string="Nombre", required=True)
    email = fields.Char(string="Email")

    course_id = fields.Many2one(
        comodel_name="training.course",
        string="Curso",
        ondelete="cascade",
    )
