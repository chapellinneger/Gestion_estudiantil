# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
# Importamos la clase base del portal para mantener el estilo de Odoo
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class EstudiantePortal(CustomerPortal):

    # 1. RUTA PARA CESAR (Materias y Profesores)
    @http.route(['/my/subjects'], type='http', auth="user", website=True)
    def portal_my_subjects(self, **kw):
        # Aquí Cesar buscará las materias
        values = self._prepare_portal_layout_values()
        # Ejemplo de búsqueda (ajustar según sus campos):
        materias = request.env['gestion.materia'].search([]) 
        
        return request.render("gestion_estudiantil.portal_my_subjects_template", {
            'materias': materias,
            'page_name': 'materias',
        })

    # 2. RUTA PARA TU LUZ (Actividades y Tareas)
    @http.route(['/my/activities'], type='http', auth="user", website=True)
    def portal_my_activities(self, **kw):
        # Aquí ella gestionará la vista de tareas
        values = self._prepare_portal_layout_values()
        actividades = request.env['gestion.activity'].search([])
        
        return request.render("gestion_estudiantil.portal_my_activities_template", {
            'actividades': actividades,
            'page_name': 'actividades',
        })

    # 3. RUTA PARA DAVID (Notas y Calificaciones)
    @http.route(['/my/grades'], type='http', auth="user", website=True)
    def portal_my_grades(self, **kw):
        # Aquí tú filtrarás las notas por el usuario actual
        values = self._prepare_portal_layout_values()
        # Filtro de seguridad: Solo las notas del estudiante logueado
        notas = request.env['gestion.calificacion'].search([
            ('student_id.user_id', '=', request.env.user.id)
        ])
        
        return request.render("gestion_estudiantil.portal_my_grades_template", {
            'notas': notas,
            'page_name': 'notas',
        })