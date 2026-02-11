# -*- coding: utf-8 -*-
from odoo import models, fields, api

class GestionAttendance(models.Model):
    _name = 'gestion.attendance'
    _description = 'Registro de Asistencia'

    date = fields.Date(string="Fecha", default=fields.Date.today, required=True)
    # Cambia 'gestion.seccion' por el nombre técnico REAL del modelo de secciones
    section_id = fields.Many2one('gestion.seccion', string="Sección", required=True) 
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado')
    ], string="Estado", default='draft')
    
    # Este es el campo que falta y causa el error
    confirmed = fields.Boolean(string="Confirmado", compute="_compute_confirmed", store=True)

    attendance_line_ids = fields.One2many(
        'gestion.attendance_line', 
        'attendance_id', 
        string="Lista de Estudiantes"
    )

    @api.depends('state')
    def _compute_confirmed(self):
        for record in self:
            record.confirmed = (record.state == 'confirmed')

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

class GestionAttendanceLine(models.Model):
    _name = 'gestion.attendance_line'
    _description = 'Línea de Asistencia'

    attendance_id = fields.Many2one('gestion.attendance', string="Registro de Asistencia", ondelete='cascade')
    student_id = fields.Many2one('res.partner', string="Estudiante", required=True) 
    present = fields.Boolean(string="Presente", default=True)