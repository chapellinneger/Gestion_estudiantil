# -*- coding: utf-8 -*-
from odoo import http

# class GestionProfesorado(http.Controller):
#     @http.route('/gestion_profesorado/gestion_profesorado', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_profesorado/gestion_profesorado/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_profesorado.listing', {
#             'root': '/gestion_profesorado/gestion_profesorado',
#             'objects': http.request.env['gestion_profesorado.profesor'].search([]),
#         })

#     @http.route('/gestion_profesorado/gestion_profesorado/objects/<model("gestion_profesorado.profesor"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_profesorado.object', {
#             'object': obj
#         })
