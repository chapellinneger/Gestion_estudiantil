from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GestionActivity(models.Model):
    _name = 'gestion.activity'
    _description = 'Actividad Académica'

    name = fields.Char(string='Título de la Tarea', required=True)
    description = fields.Html(string='Instrucciones')
    date_deadline = fields.Date(string='Fecha de Entrega')
    
    teacher_id = fields.Many2one('gestion.teacher', string='Profesor Responsable', required=True)
    
    
    submission_ids = fields.One2many('gestion.submission', 'activity_id', string='Entregas')

    @api.constrains('name')
    def checknotemptyfields(self):
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError("El título de la actividad no puede estar vacío.")

class GestionSubmission(models.Model):
    _name = 'gestion.submission'
    _description = 'Entrega de Alumno'

    activity_id = fields.Many2one('gestion.activity', string='Tarea', required=True)
    student_id = fields.Many2one('res.partner', string='Estudiante', required=True)
    
    
    file_data = fields.Binary(string='Archivo de Tarea')
    file_name = fields.Char(string='Nombre del Archivo')
    
    submission_date = fields.Date(string='Fecha de Envío', default=fields.Date.today)
    score = fields.Float(string='Calificación')
    notes = fields.Text(string='Observaciones del Profesor')
