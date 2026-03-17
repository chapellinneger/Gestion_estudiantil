from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Activity(models.Model):
    _inherit = 'gestion.activity'
    
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

# Estos campos no tiene utilidad, las tareas se registran y del modulo de profesorado
#-------------------------------------------------------------------------------
    file = fields.Binary(string='Archivo Entregado')
    file_name = fields.Char(string='Nombre del Archivo')
#------------------------------------------------------------------------------

    score = fields.Float(string='Calificación', help='Calificación numérica obtenida.')
    teacher_feedback = fields.Text(string='Comentarios del Profesor', help='Comentarios del profesor sobre el desempeño.')


    
    # Fields from Luz_rama
    date = fields.Date(string="Fecha", default=fields.Date.context_today)
    description = fields.Text(string='Descripción de la Nota')

    # Logic from develop (Unique Constraints)
    @api.constrains('student_id', 'activity_id')
    def _check_unique_grade(self):
        for record in self:
            existing = self.search([
                ('student_id', '=', record.student_id.id),
                ('activity_id', '=', record.activity_id.id),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError(
                    f"El estudiante {record.student_id.name} ya tiene una calificación registrada para la actividad '{record.activity_id.name}'."
                )

    # Logic from develop (History Tracking)
    @api.model_create_multi
    def create(self, vals_list):
        records = super(Grade, self).create(vals_list)
        for record in records:
            self.env['gestion.student.grade'].sudo().create({
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
                self.env['gestion.student.grade'].sudo().create({
                    'student_id': record.student_id.id,
                    'activity_id': record.activity_id.id,
                    'score': record.score,
                    'description': f'Actualización de nota para {record.student_id.name}'
                })
        return res

class GestionSubmissionInherit(models.Model):
    # Heredamos el modelo del módulo de profesorado
    _inherit = 'gestion.submission'

    def write(self, vals):
        # 1. Guardamos la nota normalmente en la entrega
        res = super(GestionSubmissionInherit, self).write(vals)
        
        # 2. Si el profesor modificó la calificación o las observaciones...
        if 'score' in vals or 'notes' in vals:
            for record in self:
               
                estudiante_perfil = self.env['gestion.student'].search([
                    ('partner_id', '=', record.student_id.id)
                ], limit=1)

                if estudiante_perfil:
                    grade_env = self.env['grade.grade'].sudo()
                    
                    # Buscamos si ya existe una nota para no romper tu _check_unique_grade
                    nota_oficial = grade_env.search([
                        ('student_id', '=', estudiante_perfil.id),
                        ('activity_id', '=', record.activity_id.id)
                    ], limit=1)
                    
                    valores_nota = {
                        'student_id': estudiante_perfil.id,
                        'teacher_id': record.activity_id.teacher_id.id,
                        'activity_id': record.activity_id.id,
                        'score': record.score,
                        'teacher_feedback': record.notes,
                        'description': f"Nota sincronizada desde la entrega web para {estudiante_perfil.name}",
                    }
                    
                    if nota_oficial:
                        nota_oficial.write(valores_nota)
                    else:
                        grade_env.create(valores_nota)
                        
        return res

