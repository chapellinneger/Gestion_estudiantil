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
        
        # Agregamos .sudo() para evitar bloqueos al leer las materias de otros módulos
        secciones = request.env['gestion.seccion'].sudo().search([
            ('student_ids', 'in', partner_id)
        ])
        
        return request.render("gestion_estudiantil.portal_my_subjects_template", {
            'secciones': secciones, 
            'page_name': 'materias',
        })

    # 2. RUTA PARA ACTIVIDADES
    @http.route(['/my/activities'], type='http', auth="user", website=True)
    def portal_my_activities(self, **kw):
        values = self._prepare_portal_layout_values()
        
        # El .sudo() aquí es CRUCIAL para que act.teacher_id.name no de error 403
        actividades = request.env['gestion.activity'].sudo().search([])
        
        return request.render("gestion_estudiantil.portal_my_activities_template", {
            'actividades': actividades,
            'page_name': 'actividades',
        })

    @http.route(['/my/activities/<int:activity_id>'], type='http', auth="user", website=True)
    def portal_activity_detail(self, activity_id, **kw):
        # Buscamos la actividad por su ID
        activity = request.env['gestion.activity'].sudo().browse(activity_id)
        
        # Si la actividad no existe, devolvemos un error 404
        if not activity.exists():
            return request.not_found()

        return request.render("gestion_estudiantil.portal_actividad_page", {
            'activity': activity,
            'page_name': 'actividad_detalle',
        })
    
    @http.route(['/gestion/actividad/subir'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def portal_submit_activity(self, **post):
        # 1. Obtenemos los datos del formulario
        activity_id = int(post.get('activity_id'))
        archivo = post.get('archivo_tarea')
        
        # 2. Identificamos al estudiante (el partner del usuario logueado)
        student_id = request.env.user.partner_id.id

        # 3. Verificamos que se haya subido un archivo
        if archivo:
            # Leemos el archivo y lo codificamos en base64 para guardarlo en Odoo
            file_content = base64.b64encode(archivo.read())
            file_name = archivo.filename

            # 4. Creamos el registro en gestion.submission usando sudo()
            request.env['gestion.submission'].sudo().create({
                'activity_id': activity_id,
                'student_id': student_id,
                'file_data': file_content,
                'file_name': file_name,
            })

        # 5. Redirigimos de vuelta a la página de la actividad con un mensaje de éxito
        return request.redirect(f'/my/activities/{activity_id}?success=1')


    # 3. RUTA PARA NOTAS (Modelo grade.grade)
    @http.route(['/my/grades'], type='http', auth="user", website=True)
    def portal_my_grades(self, **kw):
        values = self._prepare_portal_layout_values()
        user_name = request.env.user.name
        
        # Usamos .sudo() por si el modelo grade.grade tiene restricciones de lectura
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
        
        asistencias = request.env['gestion.attendance_line'].sudo().search([
            ('student_id', '=', partner_id)
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
        
        secciones = request.env['gestion.seccion'].sudo().search([
            ('student_ids', 'in', partner_id)
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
        
        # Obtenemos las secciones con sudo para poder mapear los profesores sin error de acceso
        secciones = request.env['gestion.seccion'].sudo().search([
            ('student_ids', 'in', partner_id)
        ])
        profesores = secciones.mapped('teacher_id')
        
        return request.render("gestion_estudiantil.portal_my_teachers_template", {
            'profesores': profesores,
            'page_name': 'profesores',
        })
