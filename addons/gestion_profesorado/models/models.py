from odoo import models, fields

class TeacherUser(models.Model):
    _inherit = "res.users"

    # Campos de la tabla técnica que nos pasaste
    is_teacher = fields.Boolean(
        string="Es Profesor", 
        default=True,
        help="Flag para filtrar usuarios en campos relacionales y reglas de seguridad."
    )
    
    signature = fields.Binary(
        string="Firma Digital",
        help="Firma digital para la generación de actas oficiales y reportes."
    )

    # Nota: 'user_id' y 'name' ya vienen heredados de res.users, 
    # no hace falta declararlos de nuevo o darán error de duplicidad.