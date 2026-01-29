from odoo import models, fields, api

class Profesor(models.Model):
    _name = 'gestion_profesorado.profesor'
    _description = 'Profesor'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    active = fields.Boolean(string="Activo", default=True)
