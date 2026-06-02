from odoo import models, fields

class GestionTipoEvaluacion(models.Model):
    _name = 'gestion.tipo.evaluacion'
    _description = 'Tipo de Evaluación'

    name = fields.Char(string='Nombre', required=True)
    seccion_id = fields.Many2one('gestion.seccion', string='Sección', required=True)