from odoo import models, fields

class GestionSeccion(models.Model):
    _name = "gestion.seccion"
    _description = "Secciones de Materias"

    name = fields.Char(required=True)
    subject_id = fields.Many2one("gestion.materia", string="Materia", required=True)
    teacher_id = fields.Many2one("res.partner", string="Profesor", domain=[("is_teacher", "=", True)])
    student_ids = fields.Many2many("res.partner", string="Estudiantes")
    state = fields.Selection(
        [
            ("abierto", "Abierto"),
            ("en progreso", "En Progreso"),
            ("finalizado", "Finalizado"),
        ],
        default="abierto",
    )
