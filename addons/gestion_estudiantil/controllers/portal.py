# -*- coding: utf-8 -*-
import base64 
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class EstudiantePortal(CustomerPortal):

    # 1. RUTA PARA MATERIAS (Desde Secciones)
    @http.route(['/my/subjects'], type='http', auth="user", website=True)
    def portal_my_subjects(self, **kw):
        values = self._prepare_portal_layout_values()
        partner_id = request.env.user.partner_id.id
        
        # Buscamos el estudiante y lo usamos en el domain
        student = request.env['gestion.student'].sudo().search([('partner_id', '=', partner_id)], limit=1)
        
        secciones = request.env['gestion.seccion'].sudo().search([
            ('student_ids', 'in', student.id if student else 0)
        ])
        
        return request.render("gestion_estudiantil.portal_my_subjects_template", {
            'secciones': secciones, 
            'page_name': 'materias',
        })

    # 2. RUTA PARA ACTIVIDADES
    @http.route(['/my/activities'], type='http', auth="user", website=True)
    def portal_my_activities(self, **kw):
        values = self._prepare_portal_layout_values()
        
        actividades = request.env['gestion.activity'].sudo().search([])
        
        return request.render("gestion_estudiantil.portal_my_activities_template", {
            'actividades': actividades,
            'page_name': 'actividades',
        })

    @http.route(['/my/activities/<int:activity_id>'], type='http', auth="user", website=True)
    def portal_activity_detail(self, activity_id, **kw):
        activity = request.env['gestion.activity'].sudo().browse(activity_id)
        
        if not activity.exists():
            return request.not_found()

        return request.render("gestion_estudiantil.portal_actividad_page", {
            'activity': activity,
            'page_name': 'actividad_detalle',
        })
    
    @http.route(['/gestion/actividad/subir'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def portal_submit_activity(self, **post):
        activity_id = int(post.get('activity_id'))
        archivo = post.get('archivo_tarea')
        
        partner_id = request.env.user.partner_id.id
        # Buscamos al estudiante real para asignarle la tarea
        student = request.env['gestion.student'].sudo().search([('partner_id', '=', partner_id)], limit=1)

        if archivo and student:
            file_content = base64.b64encode(archivo.read())
            file_name = archivo.filename

            # Usamos student.id en la creación
            request.env['gestion.submission'].sudo().create({
                'activity_id': activity_id,
                'student_id': student.id,
                'file_data': file_content,
                'file_name': file_name,
            })

        return request.redirect(f'/my/activities/{activity_id}?success=1')

    # 3. RUTA PARA NOTAS (Modelo grade.grade)
    @http.route(['/my/grades'], type='http', auth="user", website=True)
    def portal_my_grades(self, **kw):
        values = self._prepare_portal_layout_values()
        user_name = request.env.user.name
        
        # Dejado igual, asumiendo que el ilike por nombre sigue funcionando con la herencia
        notas = request.env['grade.grade'].sudo().search([
            ('student_id.name', 'ilike', user_name)
        ])
        
        return request.render("gestion_estudiantil.portal_my_grades_template", {
            'notas': notas,
            'page_name': 'notas',
        })

    # 4. RUTA PARA AUSENCIAS (Asistencias)
    @http.route(['/my/absences'], type='http', auth="user", website=True)
    def portal_my_absences(self, **kw):
        values = self._prepare_portal_layout_values()
        partner_id = request.env.user.partner_id.id
        
        student = request.env['gestion.student'].sudo().search([('partner_id', '=', partner_id)], limit=1)
        
        asistencias = request.env['gestion.attendance_line'].sudo().search([
            ('student_id', '=', student.id if student else 0)
        ])
        
        return request.render("gestion_estudiantil.portal_my_absences_template", {
            'asistencias': asistencias,
            'page_name': 'ausencias',
        })

    # 5. RUTA PARA SECCIONES
    @http.route(['/my/sections'], type='http', auth="user", website=True)
    def portal_my_sections(self, **kw):
        values = self._prepare_portal_layout_values()
        partner_id = request.env.user.partner_id.id
        
        student = request.env['gestion.student'].sudo().search([('partner_id', '=', partner_id)], limit=1)
        
        secciones = request.env['gestion.seccion'].sudo().search([
            ('student_ids', 'in', student.id if student else 0)
        ])
        
        return request.render("gestion_estudiantil.portal_my_sections_template", {
            'secciones': secciones,
            'page_name': 'secciones',
        })

    # 6. RUTA PARA PROFESORES
    @http.route(['/my/teachers'], type='http', auth="user", website=True)
    def portal_my_teachers(self, **kw):
        values = self._prepare_portal_layout_values()
        partner_id = request.env.user.partner_id.id
        
        student = request.env['gestion.student'].sudo().search([('partner_id', '=', partner_id)], limit=1)
        
        secciones = request.env['gestion.seccion'].sudo().search([
            ('student_ids', 'in', student.id if student else 0)
        ])
        profesores = secciones.mapped('teacher_id')
        
        return request.render("gestion_estudiantil.portal_my_teachers_template", {
            'profesores': profesores,
            'page_name': 'profesores',
        })