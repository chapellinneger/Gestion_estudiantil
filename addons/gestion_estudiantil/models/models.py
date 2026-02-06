from odoo import models, fields, api

class Student(models.Model):
    _name = 'gestion.student'
    _description = 'Student'
    _inherits = {'res.partner': 'partner_id'}
    
    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    
    # Optional: Link to a system user if they need to login
    user_id = fields.Many2one('res.users', string='Related User')

    enrollment_number = fields.Char(string="Número de Matrícula")
    academic_history = fields.Text(string="Historial Académico")
    
    @api.model_create_multi
    def create(self, vals_list):
        records = super(Student, self).create(vals_list)
        for record in records:
            if not record.user_id:
                # Create user automatically
                # Use email as login if available, otherwise name (or handle error)
                login = record.email or record.name or 'student_%s' % record.id
                
                user_vals = {
                    'name': record.name,
                    'login': login,
                    'partner_id': record.partner_id.id,
                    'groups_id': [(4, self.env.ref('gestion_estudiantil.group_estudiante').id)],
                }
                user = self.env['res.users'].create(user_vals)
                record.user_id = user
        return records
    
    # Relaciones que dan problemas (Commented out as in original)
    # section_ids = fields.Many2many('gestion.seccion', string="Secciones")
    # grade_ids = fields.One2many('gestion.nota', 'student_id', string="Notas")
