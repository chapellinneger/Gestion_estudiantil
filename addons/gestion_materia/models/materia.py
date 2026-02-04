from odoo import models, fields

class GestionMateria(models.Model):
    _name = "gestion.materia"
    _description = "Gestión de Materias Académicas"

    name = fields.Char(string="Nombre de la materia", required=True)
    codigo_materia = fields.Char(string="Código de la materia", required=True)

    teacher_id = fields.Many2one(
        comodel_name="res.partner",
        string="Profesor titular",
        domain=[("is_company", "=", False)]
    )

    type = fields.Selection(
        selection=[
            ("obligatoria", "Obligatoria"),
            ("electiva", "Electiva"),
        ],
        string="Tipo de materia",
        default="electiva",
    )

    active = fields.Boolean(string="Activo", default=True)
