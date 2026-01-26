from odoo import models, fields, api

class Student(models.Model):
    _name = 'gestion_estudiantil.student'
    _description = 'Estudiante'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    active = fields.Boolean(string="Activo", default=True)
