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
    _rec_name = 'student_id'

    student_id = fields.Many2one(
        'gestion.student',
        string='Estudiante',
        required=True,
        help='Selecciona el estudiante.'
    )

    teacher_id = fields.Many2one('gestion.teacher', string='Docente')
    activity_id = fields.Many2one('gestion.activity', string='Actividad', required=True)
    file = fields.Binary(string='Archivo Entregado')
    file_name = fields.Char(string='Nombre del Archivo')
    score = fields.Float(string='Calificación')
    teacher_feedback = fields.Text(string='Comentarios del Profesor')

    @api.model_create_multi
    def create(self, vals_list):
        records = super(Grade, self).create(vals_list)
        for record in records:
            self.env['gestion.student.grade'].create({
                'student_id': record.student_id.id,
                'activity_id': record.activity_id.id,
                'score': record.score,
                'description': f'Nota registrada para {record.student_id.name}'
            })
        return records

    def write(self, vals):
        res = super(Grade, self).write(vals)
        if 'score' in vals or 'activity_id' in vals:
            for record in self:
                self.env['gestion.student.grade'].create({
                    'student_id': record.student_id.id,
                    'activity_id': record.activity_id.id,
                    'score': record.score,
                    'description': f'Actualización de nota para {record.student_id.name}'
                })
        return res
