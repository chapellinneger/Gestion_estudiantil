{
    "name": "Gestión de Evaluaciones",
    "summary": "Módulo para la gestión de tipos de evaluación",
    "description": "Este módulo permite definir tipos de evaluación, porcentajes por sección y validaciones.",
    "version": "18.0.1.0.1",
    "author": "Christian y Marco - Subgrupo 1",
    "category": "Education",
    "depends": ["base", "gestion_activity", "asistencias"],
    "data": [
        "security/ir.model.access.csv",
        "views/tipo_evaluacion_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}