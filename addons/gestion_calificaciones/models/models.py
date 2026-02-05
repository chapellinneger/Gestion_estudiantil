from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Activity(models.Model):
    _name = 'activity.activity'
    _description = 'Actividad'

    name = fields.Char(string='Nombre de la Actividad', required=True)
    
    @api.constrains('name')
    def checkname(self):
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError("El nombre de la actividad no puede estar vacío.")

class Grade(models.Model):
    _name = 'grade.grade'
    _description = 'Calificación'
    _rec_name = 'student_name'

    student_name = fields.Char(string='Nombre del Estudiante', required=True, help='Escribe el nombre del estudiante.')
    activity_id = fields.Many2one('activity.activity', string='Actividad', help='La actividad evaluada.', required=True)
    file = fields.Binary(string='Archivo Entregado', help='Este archivo vendrá del módulo de entregas en el futuro.')
    file_name = fields.Char(string='Nombre del Archivo')
    score = fields.Float(string='Calificación', help='Calificación numérica obtenida.')
    teacher_feedback = fields.Text(string='Comentarios del Profesor', help='Comentarios del profesor sobre el desempeño.')


    @api.constrains('student_name')
    def checknotemptyfields(self):
        for record in self:
            if not record.student_name or not record.student_name.strip():
                raise ValidationError("El nombre del estudiante no puede estar vacío.")

    @api.model_create_multi
    def create(self, vals_list):
        records = super(Grade, self).create(vals_list)
        for record in records:
            # Creamos el registro en el módulo original sin modificarlo
            self.env['gestion.estudiantil'].create({
                'name': record.activity_id.name or 'Nota', # Nombre de la actividad
                'value': int(record.score),               # Valor de la nota
                'description': f'Estudiante: {record.student_name}'
            })
        return records

    def write(self, vals):
        res = super(Grade, self).write(vals)
        if 'score' in vals or 'activity_id' in vals:
            for record in self:
                self.env['gestion.estudiantil'].create({
                    'name': record.activity_id.name or 'Nota Actualizada',
                    'value': int(record.score),
                    'description': f'Actualización - Estudiante: {record.student_name}'
                })
        return res
