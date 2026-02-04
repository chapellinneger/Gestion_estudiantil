{
    "name": "Gestion de Materias",
    "resumen": "modulo para la gestion de las materias",
    "description": "Este modulo permite gestionar las materias en un sistema de gestion estudiantil.",
    "version": "18.0.1.0.0",
    "author": "Kaazest",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/materia_views.xml",
        "data/materia_data.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}