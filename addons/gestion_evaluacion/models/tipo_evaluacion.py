from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GestionTipoEvaluacion(models.Model):
    _name = 'gestion.tipo.evaluacion'
    _description = 'Tipos de Evaluacion'

    name = fields.Char(string='Nombre', required=True)
    seccion_id = fields.Many2one('gestion.seccion', string='Sección', required=True)
    porcentaje = fields.Float(string='Porcentaje', default=0.0)
    periodo_id = fields.Many2one('gestion.periodo', string='Período Académico', default=lambda self: self.env['gestion.periodo'].search([('activo', '=', True)], limit=1))

    @api.constrains('porcentaje', 'seccion_id')
    def _check_porcentaje_total(self):
        for rec in self:
            if rec.seccion_id:
                evaluaciones = self.search([('seccion_id', '=', rec.seccion_id.id)])
                total_porcentaje = sum(evaluaciones.mapped('porcentaje'))
                if total_porcentaje > 1.0:
                    raise ValidationError('El porcentaje total para esta sección no puede exceder el 100% (1.0).')

