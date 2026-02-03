from odoo import models, fields

class TeacherUser(models.Model):
    _inherit = "res.users"

    # Campos de la tabla técnica
    is_teacher = fields.Boolean(
        string="Es Profesor", 
        default=True,
        help="Flag para filtrar usuarios en campos relacionales y reglas de seguridad."
    )
    
    # Cambiamos el string a uno genérico para que no diga "Docente" por defecto
    signature = fields.Binary(
        string="Firma Digital",
        help="Firma digital para la generación de actas oficiales y reportes."
    )

    # Estos campos se dejan comentados para evitar errores de relación 
    # hasta que los modelos de Materias y Secciones existan en el sistema.
    
    # subject_ids = fields.One2many(
    #     'gestion.subject', 
    #     'teacher_id', 
    #     string="Materias",
    #     help="Materias de las cuales es el titular responsable."
    # )

    # section_ids = fields.One2many(
    #     'gestion.section', 
    #     'teacher_id', 
    #     string="Secciones",
    #     help="Secciones específicas que tiene asignadas actualmente."
    # )

    # Nota: 'user_id' y 'name' ya vienen heredados de res.users