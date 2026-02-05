from odoo import models, fields
from odoo.exceptions import ValidationError

class GestionMateria(models.Model):
    _name = "gestion.materia"
    _description = "Gestión de Materias Académicas"

    name = fields.Char(string="Nombre de la materia", required=True)
    codigo_materia = fields.Char(string="Código de la materia", required=True)

    teacher_id = fields.Many2one(
        comodel_name="gestion.teacher",
        string="Profesor titular",
        domain=[("is_teacher", "=", True)]
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
    
@api.constrains('name', 'codigo_materia')
    def checknotemptyfields(self):
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError("El nombre de la materia no puede estar vacío.")
            if not record.codigomateria or not record.codigomateria.strip():
                raise ValidationError("El código de la materia no puede estar vacío.")
