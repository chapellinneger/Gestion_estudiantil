# -*- coding: utf-8 -*-
{
    'name': "Gestion Calificaciones",
    'summary': """
        Módulo simple para registro de calificaciones estudiantiles""",
    'description': """
        Módulo independiente para gestionar calificaciones.
        Incluye modelos para Estudaintes, Actividades, Entregas y Calificaciones.
    """,
    'author': "Kaazest",
    'category': 'Education',
    'version': '0.1',
    'depends': ['base', 'gestion_estudiantil', 'gestion_materia'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_grade_views.xml',
        'views/views.xml',
    ],
}
