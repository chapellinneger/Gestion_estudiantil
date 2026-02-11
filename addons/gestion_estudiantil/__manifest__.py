{
    'name': "Gestion Estudiantil",
    'summary': "Módulo para la gestión de estudiantes",
    'description': """
        Módulo básico para la gestión estudiantil en Odoo 18.
    """,
    'author': "Kaazest",
    'website': "https://www.yourcompany.com",
    'category': 'Education',
    'version': '18.0.1.0.0',
    'depends': ['base', 'gestion_profesorado', 'gestion_secciones'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/asistencia_view.xml',  # mi  archivo XML
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}