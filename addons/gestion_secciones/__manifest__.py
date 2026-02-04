{
    'name': "Gestion de secciones",
    'summary': "Módulo para la gestión de secciones",
    'description': """
        Módulo básico para la gestión de secciones en Odoo 18.
    """,
    'author': "Kaazest",
    'category': 'Education',
    'version': '18.0.1.0.0',
    'depends': ['base'],
    "data": [
        "security/ir.model.access.csv",
        "views/gestion_seccion_views.xml",
        "views/menu_views.xml",
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
