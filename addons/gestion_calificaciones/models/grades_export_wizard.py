from odoo import models, fields, api
import io
import xlsxwriter
import base64

class GestionExportCalificaciones(models.TransientModel):
    _inherit = 'gestion.export'

    # Extiende la selección del tipo de reporte en el wizard
    export_type = fields.Selection(
        selection_add=[('grades', 'Calificaciones')],
        ondelete={'grades': 'cascade'}
    )

    # Campo para filtrar por materia específica (opcional)
    subject_id = fields.Many2one(
        'gestion.materia',
        string="Materia"
    )

    def get_grade_lines(self):
        """Busca y retorna las calificaciones que coinciden con los filtros del wizard."""
        self.ensure_one()
        domain = []
        
        # Filtro por estudiante
        if self.filter_type == 'single' and self.student_id:
            domain.append(('student_id', '=', self.student_id.id))
            
        # Filtro por sección
        elif self.filter_type == 'section' and self.section_id:
            domain.append(('student_id', 'in', self.section_id.student_ids.ids))
            
        # Filtro por materia
        if self.subject_id:
            domain.append(('activity_id.subject_id', '=', self.subject_id.id))
            
        # Filtro por rango de fechas
        if self.date_from:
            domain.append(('date', '>=', self.date_from))
        if self.date_to:
            domain.append(('date', '<=', self.date_to))
            
        return self.env['grade.grade'].search(domain, order='student_id, date desc, activity_id')

    def action_export(self):
        self.ensure_one()
        if self.export_type == 'grades':
            if self.export_format == 'pdf':
                return self.env.ref('gestion_calificaciones.action_report_grades_pdf').report_action(self)
            elif self.export_format == 'xlsx':
                return self._export_grades_xlsx()
        return super(GestionExportCalificaciones, self).action_export()

    def _export_grades_xlsx(self):
        self.ensure_one()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # Formatos de celdas
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 11,
            'align': 'center',
            'bg_color': '#2C3E50', 
            'font_color': '#FFFFFF',
            'border': 1
        })
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'font_color': '#2980B9'
        })
        info_bold = workbook.add_format({'bold': True, 'font_size': 10})
        info_normal = workbook.add_format({'font_size': 10})
        
        cell_format = workbook.add_format({'font_size': 10, 'align': 'center', 'border': 1})
        cell_left = workbook.add_format({'font_size': 10, 'align': 'left', 'border': 1})
        
        # Formato especial para nota aprobada (verde) y reprobada (rojo)
        passing_format = workbook.add_format({
            'font_size': 10,
            'align': 'center',
            'border': 1,
            'bg_color': '#D4EDDA',
            'font_color': '#155724',
            'num_format': '0.00'
        })
        failing_format = workbook.add_format({
            'font_size': 10,
            'align': 'center',
            'border': 1,
            'bg_color': '#F8D7DA',
            'font_color': '#721C24',
            'num_format': '0.00'
        })
        score_format = workbook.add_format({
            'font_size': 10,
            'align': 'center',
            'border': 1,
            'num_format': '0.00'
        })

        lines = self.get_grade_lines()
        students = lines.mapped('student_id')

        # HOJA 1: RESUMEN DE NOTAS
        sheet_resumen = workbook.add_worksheet('Resumen de Notas')
        sheet_resumen.set_column('A:A', 30)  
        sheet_resumen.set_column('B:B', 15)  
        sheet_resumen.set_column('C:C', 20)  
        sheet_resumen.set_column('D:D', 20)  

        sheet_resumen.merge_range('A1:D1', 'Resumen de Calificaciones de Estudiantes', title_format)
        
        # Información de los filtros
        sheet_resumen.write('A3', 'Filtro utilizado:', info_bold)
        filter_text = "Todos los estudiantes"
        if self.filter_type == 'single' and self.student_id:
            filter_text = f"Estudiante: {self.student_id.name}"
        elif self.filter_type == 'section' and self.section_id:
            filter_text = f"Sección: {self.section_id.name}"
        sheet_resumen.write('B3', filter_text, info_normal)
        
        sheet_resumen.write('A4', 'Materia filtrada:', info_bold)
        subject_text = self.subject_id.name if self.subject_id else "Todas las materias"
        sheet_resumen.write('B4', subject_text, info_normal)
        
        sheet_resumen.write('A5', 'Rango de fechas:', info_bold)
        date_text = f"Desde {self.date_from or 'Inicio'} hasta {self.date_to or 'Fin'}"
        sheet_resumen.write('B5', date_text, info_normal)

        headers_resumen = ['Estudiante', 'Matrícula', 'Promedio de Notas', 'Actividades Evaluadas']
        for col_idx, header in enumerate(headers_resumen):
            sheet_resumen.write(7, col_idx, header, header_format)

        row_idx = 8
        for student in students:
            student_lines = lines.filtered(lambda l: l.student_id == student)
            scores = student_lines.mapped('score')
            avg_score = sum(scores) / len(scores) if scores else 0.0
            total_act = len(scores)

            sheet_resumen.write(row_idx, 0, student.name or '', cell_left)
            sheet_resumen.write(row_idx, 1, student.enrollment_number or '', cell_format)
            
            # Formato condicional para el promedio (suponiendo aprobación >= 10 o >= 5)
            # En la escala de 20 (aprobación >= 10) o de 10 (aprobación >= 5)
            if avg_score >= 10:
                sheet_resumen.write(row_idx, 2, avg_score, passing_format)
            elif avg_score < 10 and avg_score > 0:
                sheet_resumen.write(row_idx, 2, avg_score, failing_format)
            else:
                sheet_resumen.write(row_idx, 2, avg_score, score_format)
                
            sheet_resumen.write(row_idx, 3, total_act, cell_format)
            row_idx += 1

        # HOJA 2: DETALLE DE NOTAS
        sheet_detalle = workbook.add_worksheet('Detalle de Notas')
        sheet_detalle.set_column('A:A', 30)  
        sheet_detalle.set_column('B:B', 15)  
        sheet_detalle.set_column('C:C', 25)  
        sheet_detalle.set_column('D:D', 25)  
        sheet_detalle.set_column('E:E', 15)  
        sheet_detalle.set_column('F:F', 15)  
        sheet_detalle.set_column('G:G', 35)  

        sheet_detalle.merge_range('A1:G1', 'Detalle de Calificaciones Estudiantiles', title_format)

        headers_detalle = ['Estudiante', 'Matrícula', 'Materia', 'Actividad', 'Nota', 'Fecha', 'Observaciones']
        for col_idx, header in enumerate(headers_detalle):
            sheet_detalle.write(3, col_idx, header, header_format)

        row_idx_det = 4
        for line in lines:
            sheet_detalle.write(row_idx_det, 0, line.student_id.name or '', cell_left)
            sheet_detalle.write(row_idx_det, 1, line.student_id.enrollment_number or '', cell_format)
            sheet_detalle.write(row_idx_det, 2, line.activity_id.subject_id.name or '', cell_format)
            sheet_detalle.write(row_idx_det, 3, line.activity_id.name or '', cell_left)
            
            # Formato de celda condicional para cada nota
            if line.score >= 10:
                sheet_detalle.write(row_idx_det, 4, line.score, passing_format)
            else:
                sheet_detalle.write(row_idx_det, 4, line.score, failing_format)
                
            sheet_detalle.write(row_idx_det, 5, str(line.date) if line.date else '', cell_format)
            sheet_detalle.write(row_idx_det, 6, line.teacher_feedback or '', cell_left)
            row_idx_det += 1

        if not lines:
            sheet_detalle.merge_range(4, 0, 4, 6, 'No hay detalles de calificaciones que mostrar.', cell_format)

        workbook.close()
        output.seek(0)

        self.write({
            'file_data': base64.b64encode(output.read()),
            'file_name': f'Reporte_Calificaciones_{fields.Date.today()}.xlsx',
            'state': 'get'
        })
        output.close()

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
