{
    "name": "Gestion de secciones",
    "summary": "modulo para la gestion de secciones",
    "description": "Este modulo permite gestionar las secciones en un sistema de gestion estudiantil.",
    "version": "18.0.1.0.0",
    "author": "Kaazest",
    "category": "Education",
    "depends": ["base", "gestion_materia"],
    "data": [
        "security/ir.model.access.csv",
        "views/gestion_seccion_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
