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
    'depends': ['base', 'gestion_profesorado'],
    'data': [
       'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
