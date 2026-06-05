# pyrefly: ignore [missing-import]
from odoo import models, fields, api
import io
# pyrefly: ignore [missing-import]
import xlsxwriter
import base64
class GestionExport(models.TransientModel):
    _name = 'gestion.export'
    _description = 'Exportacion de asistencias'

    # Campo de selección para elegir el formato de salida: Excel o PDF
    export_format = fields.Selection([
        ('xlsx', 'Excel (.xlsx)'),
        ('pdf', 'Pdf (.pdf)')
    ], string="Tipo de exportacion", default='xlsx', required=True)

    # Campo de selección para definir el criterio de filtrado
    filter_type = fields.Selection([
        ('all', 'Todos'),
        ('section', 'Por Sección'),
        ('single', 'Un estudiante')
    ], string="Filtrar por", default="all", required=True)

    # Relación con el estudiante, requerida si se filtra por un solo estudiante
    student_id = fields.Many2one(
        'gestion.student', 
        string="Estudiante"
    )

    # Relación con la sección, requerida si se filtra por una sección específica
    section_id = fields.Many2one(
        'gestion.seccion', 
        string="Sección"
    )

    # Rango de fechas para el reporte (opcionales)
    date_from = fields.Date(string="Fecha Desde")
    date_to = fields.Date(string="Fecha Hasta")

    # Almacena los datos binarios del archivo Excel generado
    file_data = fields.Binary(string="Archivo", readonly=True)
    
    # Almacena el nombre del archivo Excel generado
    file_name = fields.Char(string="Nombre de Archivo", readonly=True)
    

    # 'choose' muestra el formulario de filtros; 'get' muestra la pantalla de descarga
    state = fields.Selection([
        ('choose', 'Elegir Parámetros'),
        ('get', 'Descargar')
    ], string="Estado", default='choose')

    # Método para buscar las líneas de asistencia en base a los filtros configurados
    def get_attendance_lines(self):
        """Busca y retorna las líneas de asistencia que coinciden con los filtros del wizard."""
        self.ensure_one()

        # Solo se incluyen registros de asistencia que ya han sido confirmados
        domain = [('attendance_id.state', '=', 'confirmed')]
        
        # Filtra por un estudiante específico
        if self.filter_type == 'single' and self.student_id:
            domain.append(('student_id', '=', self.student_id.id))

        # Filtra por una sección específica
        elif self.filter_type == 'section' and self.section_id:
            domain.append(('attendance_id.section_id', '=', self.section_id.id))
            
        # Filtra por rango de fechas 
        if self.date_from:
            domain.append(('attendance_id.date', '>=', self.date_from))
        if self.date_to:
            domain.append(('attendance_id.date', '<=', self.date_to))
            
        # Retorna el conjunto de líneas de asistencia que coinciden con la búsqueda,
        return self.env['gestion.attendance_line'].search(domain, order='student_id, attendance_id desc')
    
    # Método que ejecuta la exportación del reporte cuando el usuario presiona el botón
    def action_export(self):
        self.ensure_one()
        
        # Generación del reporte en formato PDF usando la plantilla QWeb
        if self.export_format == 'pdf':
            # Llama a la acción de reporte registrada en el sistema de Odoo y la retorna al cliente web
            return self.env.ref('gestion_estudiantil.action_report_attendance_pdf').report_action(self)
            
        # Generación del reporte en formato Excel (.xlsx)
        elif self.export_format == 'xlsx':
            # Crea un flujo de bytes en memoria para escribir el archivo
            output = io.BytesIO()
            # Inicializa el libro de trabajo Excel con xlsxwriter
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            
            # Formatos de celdas para el diseño y estética del reporte Excel
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
            
            # Formato de celda especial para asistencia (Verde)
            present_format = workbook.add_format({
                'font_size': 10,
                'align': 'center',
                'border': 1,
                'bg_color': '#D4EDDA',
                'font_color': '#155724'
            })

            # Formato de celda especial para inasistencia (Rojo)
            absent_format = workbook.add_format({
                'font_size': 10,
                'align': 'center',
                'border': 1,
                'bg_color': '#F8D7DA',
                'font_color': '#721C24'
            })

            # Obtiene las líneas filtradas y los estudiantes asociados a ellas
            lines = self.get_attendance_lines()
            students = lines.mapped('student_id')

            # HOJA 1: RESUMEN DE ASISTENCIA
            sheet_resumen = workbook.add_worksheet('Resumen de Asistencia')
            # Establece los anchos de las columnas en la hoja
            sheet_resumen.set_column('A:A', 30)  
            sheet_resumen.set_column('B:B', 15)  
            sheet_resumen.set_column('C:C', 25)  
            sheet_resumen.set_column('D:D', 15)  
            sheet_resumen.set_column('E:G', 15)  

            # Título principal del reporte
            sheet_resumen.merge_range('A1:G1', 'Resumen de Asistencia de Estudiantes', title_format)
            
            # Información de los filtros aplicados en el encabezado
            sheet_resumen.write('A3', 'Filtro utilizado:', info_bold)
            filter_text = "Todos los estudiantes"
            if self.filter_type == 'single' and self.student_id:
                filter_text = f"Estudiante: {self.student_id.name}"
            elif self.filter_type == 'section' and self.section_id:
                filter_text = f"Sección: {self.section_id.name}"
            sheet_resumen.write('B3', filter_text, info_normal)
            sheet_resumen.write('A4', 'Rango de fechas:', info_bold)
            date_text = f"Desde {self.date_from or 'Inicio'} hasta {self.date_to or 'Fin'}"
            sheet_resumen.write('B4', date_text, info_normal)

            # Escribe las cabeceras de la tabla resumen
            headers_resumen = ['Estudiante', 'Matrícula', 'Clase(s) / Sección', 'Clases Totales', 'Asistencias', 'Inasistencias', '% Asistencia']
            for col_idx, header in enumerate(headers_resumen):
                sheet_resumen.write(6, col_idx, header, header_format)

            # Escribe los registros del resumen de asistencia por estudiante
            row_idx = 7
            for student in students:
                student_lines = lines.filtered(lambda l: l.student_id == student)
                total_classes = len(student_lines)
                presents = len(student_lines.filtered(lambda l: l.present))
                absents = total_classes - presents
                ratio = (presents / total_classes * 100) if total_classes > 0 else 0.0

                # CLASE DEL ESTUDIANTE: Obtiene el identificador/nombre de la clase 
                sections = self.env['gestion.seccion'].search([('student_ids', 'in', student.id)])
                sections_name = ", ".join(sections.mapped('name')) or "Ninguna"

                sheet_resumen.write(row_idx, 0, student.name or '', cell_left)
                sheet_resumen.write(row_idx, 1, student.enrollment_number or '', cell_format)
                sheet_resumen.write(row_idx, 2, sections_name, cell_format)
                sheet_resumen.write(row_idx, 3, total_classes, cell_format)
                sheet_resumen.write(row_idx, 4, presents, cell_format)
                sheet_resumen.write(row_idx, 5, absents, cell_format)
                sheet_resumen.write(row_idx, 6, f"{ratio:.2f}%", cell_format)
                row_idx += 1

            # HOJA 2: DETALLE DE ASISTENCIAS
            sheet_detalle = workbook.add_worksheet('Detalle de Asistencias')
            sheet_detalle.set_column('A:A', 30)  
            sheet_detalle.set_column('B:B', 15)  
            sheet_detalle.set_column('C:C', 20)  
            sheet_detalle.set_column('D:D', 20)  
            sheet_detalle.set_column('E:E', 20)  

            # Título principal del reporte detalle
            sheet_detalle.merge_range('A1:E1', 'Detalle de Asistencias de Estudiantes', title_format)

            # Escribe las cabeceras de la tabla detalle
            headers_detalle = ['Estudiante', 'Fecha', 'Sección', 'Materia', 'Estado']
            for col_idx, header in enumerate(headers_detalle):
                sheet_detalle.write(3, col_idx, header, header_format)

            row_idx_det = 4
            for line in lines:
                sheet_detalle.write(row_idx_det, 0, line.student_id.name or '', cell_left)
                sheet_detalle.write(row_idx_det, 1, str(line.attendance_id.date) if line.attendance_id.date else '', cell_format)
                sheet_detalle.write(row_idx_det, 2, line.attendance_id.section_id.name or '', cell_format)
                sheet_detalle.write(row_idx_det, 3, line.attendance_id.subject_id.name or '', cell_format)

                # Colorea la celda del estado de asistencia de manera condicional (presente/ausente)
                if line.present:
                    sheet_detalle.write(row_idx_det, 4, 'Asistió (True)', present_format)
                else:
                    sheet_detalle.write(row_idx_det, 4, 'Inasistió (False)', absent_format)
                row_idx_det += 1

            # Mensaje en caso de que no existan líneas de detalles
            if not lines:
                sheet_detalle.merge_range(4, 0, 4, 4, 'No hay detalles de asistencias que mostrar.', cell_format)

            # Cierra el archivo del libro de trabajo
            workbook.close()
            output.seek(0)

            # Guarda los datos binarios base64 y el nombre del archivo en el registro del wizard,
            self.write({
                'file_data': base64.b64encode(output.read()),
                'file_name': f'Reporte_Asistencias_{fields.Date.today()}.xlsx',
                'state': 'get'
            })

            # Cierra el flujo de memoria BytesIO
            output.close()

            # Retorna una acción que recarga la vista formulario actual para reflejar los cambios
            return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'new',
            }
        
    # Regresa al paso de parámetros desde la pantalla de descarga
    def action_back(self):
        """Limpia los archivos y regresa el wizard al estado de selección."""
        self.ensure_one()
        # Limpia los datos guardados y restablece el estado del asistente a 'choose'
        self.write({
            'state': 'choose',
            'file_data': False,
            'file_name': False
        })
        # Retorna la acción para recargar la vista formulario actual
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }