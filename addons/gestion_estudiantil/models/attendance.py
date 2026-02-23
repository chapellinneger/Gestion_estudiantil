from odoo import models, fields, api

class GestionAttendance(models.Model):
    _name = 'gestion.attendance'
    _description = 'Asistencia'
    _rec_name = 'date'

    date = fields.Date(string='Fecha', default=fields.Date.context_today, required=True)
    section_id = fields.Many2one('gestion.seccion', string='Sección', required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado')
    ], string='Estado', default='draft', required=True)
    
    attendance_line_ids = fields.One2many('gestion.attendance.line', 'attendance_id', string='Líneas de Asistencia')

    def action_confirm(self):
        self.ensure_one()
        self.state = 'confirmed'

class GestionAttendanceLine(models.Model):
    _name = 'gestion.attendance.line'
    _description = 'Línea de Asistencia'

    attendance_id = fields.Many2one('gestion.attendance', string='Asistencia', ondelete='cascade', required=True)
    student_id = fields.Many2one('gestion.student', string='Estudiante', required=True)
    present = fields.Boolean(string='Presente', default=False)
