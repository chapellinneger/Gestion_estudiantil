# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GestionTipoEvaluacion(models.Model):
    _name = 'gestion.tipo.evaluacion'
    _description = 'Tipo de Evaluación'

    name = fields.Char(string='Nombre', required=True)
    seccion_id = fields.Many2one('gestion.seccion', string='Sección', required=True)

    porcentaje = fields.Float(string='Porcentaje (%)', required=True)
    periodo_id = fields.Many2one('gestion.periodo', string='Período Académico', required=True)

    #validacion de suma de porcentajes por sección no supera 100%
    @api.constrains('porcentaje', 'seccion_id')
    def _check_porcentaje_total(self):
        for record in self:
            tipos = self.search([
                ('seccion_id', '=', record.seccion_id.id),
                ('id', '!=', record.id)
            ])
            suma = record.porcentaje + sum(t.porcentaje for t in tipos)
            if suma > 100.0:
                raise ValidationError(
                    _("La suma de porcentajes para la sección '%s' supera el 100%% (%.2f%%)")
                    % (record.seccion_id.name, suma)
                )
            if record.porcentaje < 0:
                raise ValidationError(_("El porcentaje no puede ser negativo."))

    # Asignar período activo por defecto
    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        periodo_activo = self.env['gestion.periodo'].search([('activo', '=', True)], limit=1)
        if periodo_activo:
            defaults['periodo_id'] = periodo_activo.id
        return defaults

    # Validacion de que el período este activo
    @api.constrains('periodo_id')
    def _check_periodo_activo(self):
        for record in self:
            if record.periodo_id and not record.periodo_id.activo:
                raise ValidationError(_("Solo se puede asignar un período académico activo."))