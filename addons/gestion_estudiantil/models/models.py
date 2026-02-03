from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    enrollment_number = fields.Char(string="Número de Matrícula")
    academic_history = fields.Text(string="Historial Académico")
    
    # Relaciones que dan problemas
    # section_ids = fields.Many2many('gestion.seccion', string="Secciones")
    # grade_ids = fields.One2many('gestion.nota', 'student_id', string="Notas")