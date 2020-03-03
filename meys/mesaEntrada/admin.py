from django.contrib import admin
from .models import documento, estado, tipo, unidades, dependenciasInternas
from django import forms
from django.forms import TextInput, Textarea
from django.db import models
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import datetime

import io
from django.http import HttpResponse
import xlsxwriter

from fpdf import FPDF, HTMLMixin
from django.template.response import TemplateResponse

# clases y/o metodos auxiliares


class MYFPDF(FPDF, HTMLMixin):
    pass
# fin de cales y/o metodos auxiliares


@admin.register(documento)
class DocumentoAdmin(admin.ModelAdmin):
    radio_fields = {"Tramite": admin.HORIZONTAL}
    list_display = ('nro_documento', 'Tipo', 'asunto',
                    'origen', 'destino', 'Nro_sistema', 'Fecha_registro')
    list_filter = ['Tramite', 'Tipo']
    search_fields = ['nro_documento', 'Nro_sistema', 'asunto', 'Tipo__tipo']
    list_per_page = 25
    autocomplete_fields = ['Documento_relacionado', 'pase',
                           'entiende', 'participa', 'interviene', 'copia']
    date_hierarchy = 'Fecha_registro'
    actions = ['exportar_a_excel_recibidos',
               'exportar_a_excel_emitidos', 'exportar_hoja_ruta']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '50'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 50})},
    }

    """
    #Estas opciones comentadas son para agregar botones
    change_list_template = "exportar/exportar.html"
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('exportarExcel/', self.exportar_a_excel),
            #path('exportarPdf/', self.exportar_a_pdf),

        ]
        return my_urls + urls

    def exportar_a_excel(self, request):
        #self.message_user(request, "Exportado a Excel con éxito")
        #messages.error(request, 'Debe seleccionar almenos un registro para exportar a Excel')
        return HttpResponseRedirect("../")
    """

    # https://xlsxwriter.readthedocs.io/example_django_simple.html
    def exportar_a_excel_recibidos(self, request, queryset):
        unidad = 'Secr Ayte JEMCFFAA'
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        # propiedades de pagina
        worksheet.set_landscape()
        worksheet.set_paper(9)
        worksheet.center_horizontally()
        # formato de celdas
        bold = workbook.add_format({'bold': 1})
        bold.set_font_color('white')
        bold.set_font_name('Times New Roman')
        bold.set_align('center')
        bold.set_fg_color('#205C90')
        bold.set_border(2)
        bold.set_text_wrap()
        texto = workbook.add_format()
        texto.set_font_name('Times New Roman')
        texto.set_border(1)
        texto.set_align('vcenter')
        texto.set_font_size(9)
        texto.set_text_wrap()

        texto1 = workbook.add_format()
        texto1.set_align('center')

        asunto = workbook.add_format()
        asunto.set_text_wrap()

        titulo_pagina = workbook.add_format({'bold': 1})
        fechaFuente = workbook.add_format({'bold': 1})
        titulo_pagina.set_align('center')
        fechaFuente.set_align('left')

        titulo = 'Listado de documentos recibidos'
        worksheet.merge_range('A1:G1', titulo, titulo_pagina)
        #worksheet.merge_range('A2:H2','Filtrado por: '+tipo, titulo_pagina)

        #list_display = ('Tipo','nro_documento','asunto','origen','Nro_sistema','Fecha_registro')
        cabezera = ['Tipo', 'Nro Doc', 'Asunto',
                    'Origen', 'Nro sis', 'Fecha reg', 'Obs']
        worksheet.write_row('A5', cabezera, bold)

        cabecera = '&CMEYS %s' % unidad
        pie = '&LImpreso el &D a las &T&R Pagina &P de &N'
        worksheet.set_header(cabecera)
        worksheet.set_footer(pie)

        worksheet.set_column(2, 2, 30, asunto)
        worksheet.set_column(3, 3, 11, asunto)
        worksheet.set_column(4, 4, 11, texto1)
        worksheet.set_column(1, 1, 8, texto1)
        worksheet.set_column(0, 0, 9, texto1)
        worksheet.set_column(5, 5, 8, texto1)
        worksheet.set_column(6, 6, 11, texto1)
        worksheet.set_column(7, 7, 8, texto1)

        def datos(obj):
            lista = []
            lista.append(str(getattr(obj, 'Tipo')))
            lista.append(getattr(obj, 'nro_documento'))
            lista.append(getattr(obj, 'asunto'))
            lista.append(str(getattr(obj, 'origen')))
            lista.append(getattr(obj, 'Nro_sistema'))
            f = getattr(obj, 'Fecha_registro')
            g = f.strftime('%d/%m/%Y')
            lista.append(g)
            lista.append('')
            return lista
        n = 6
        for obj in queryset:
            # for x in resultados:
            if (getattr(obj, 'Tramite') == 'RE'):
                worksheet.write_row('A'+str(n), datos(obj), texto)
            n += 1

        worksheet.repeat_rows(5)
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = 'Documentos recibidos-{0}.xlsx'.format(
            datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            filename)
        return response

        #self.message_user(request, "Exportado a Excel con éxito")

    def exportar_a_excel_emitidos(self, request, queryset):
        unidad = 'Secr Ayte JEMCFFAA'
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        # propiedades de pagina
        worksheet.set_landscape()
        worksheet.set_paper(9)
        worksheet.center_horizontally()
        # formato de celdas
        bold = workbook.add_format({'bold': 1})
        bold.set_font_color('white')
        bold.set_font_name('Times New Roman')
        bold.set_align('center')
        bold.set_fg_color('#205C90')
        bold.set_border(2)
        bold.set_text_wrap()
        texto = workbook.add_format()
        texto.set_font_name('Times New Roman')
        texto.set_border(1)
        texto.set_align('vcenter')
        texto.set_font_size(9)
        texto.set_text_wrap()

        texto1 = workbook.add_format()
        texto1.set_align('center')

        asunto = workbook.add_format()
        asunto.set_text_wrap()

        titulo_pagina = workbook.add_format({'bold': 1})
        fechaFuente = workbook.add_format({'bold': 1})
        titulo_pagina.set_align('center')
        fechaFuente.set_align('left')

        titulo = 'Listado de documentos emitidos'
        worksheet.merge_range('A1:G1', titulo, titulo_pagina)

        cabezera = ['Tipo', 'Nro doc', 'Asunto',
                    'Destino', 'Nro sis', 'Fecha reg', 'Obs']
        worksheet.write_row('A5', cabezera, bold)

        cabecera = '&CMEYS %s' % unidad
        pie = '&LImpreso el &D a las &T&R Pagina &P de &N'
        worksheet.set_header(cabecera)
        worksheet.set_footer(pie)

        worksheet.set_column(2, 2, 30, asunto)
        worksheet.set_column(3, 3, 11, asunto)
        worksheet.set_column(4, 4, 11, texto1)
        worksheet.set_column(1, 1, 8, texto1)
        worksheet.set_column(0, 0, 9, texto1)
        worksheet.set_column(5, 5, 8, texto1)
        worksheet.set_column(6, 6, 11, texto1)
        worksheet.set_column(7, 7, 8, texto1)

        def datos(obj):
            lista = []
            lista.append(str(getattr(obj, 'Tipo')))
            lista.append(getattr(obj, 'nro_documento'))
            lista.append(getattr(obj, 'asunto'))
            lista.append(str(getattr(obj, 'origen')))
            lista.append(getattr(obj, 'Nro_sistema'))
            f = getattr(obj, 'Fecha_registro')
            g = f.strftime('%d/%m/%Y')
            lista.append(g)
            lista.append('')
            return lista
        n = 6
        for obj in queryset:
            if (getattr(obj, 'Tramite') == 'EM'):
                worksheet.write_row('A'+str(n), datos(obj), texto)
            n += 1

        worksheet.repeat_rows(5)
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = 'Documentos emitidos-{0}.xlsx'.format(
            datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            filename)
        return response

    def exportar_hoja_ruta(self, request, queryset):
        pdf = MYFPDF()
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        for obj in queryset:
            pdf.add_page()
            pdf.set_font('Arial', 'BI', 10)
            nroSistema = getattr(obj, 'Nro_sistema')
            tipo = str(getattr(obj, 'Tipo'))
            nro = getattr(obj, 'nro_documento')
            fecha_doc = getattr(obj, 'Fecha_entrada')
            fecha_reg = getattr(obj, 'Fecha_registro')
            if (getattr(obj, 'Termino')):
                termino = getattr(obj, 'Termino')
            else:
                termino = 'No posee'
            origen = str(getattr(obj, 'origen'))
            asunto = getattr(obj, 'asunto')
            texto = len(asunto)
            if texto < 75:
                alto = 6
            elif texto >= 75 and texto < 150:
                alto = 12
            else:
                alto = 18
            pdf.cell(35, 5, 'EMCOFFAA', 0, 0, 'C')
            pdf.cell(0, 5, 'Nro de Sistema: '+nroSistema, 0, 1, 'R')
            pdf.set_font('Arial', '', 10)
            pdf.cell(100, 5, 'Secretaria Ayudante', 0, 1, 'L')
            pdf.set_font('Arial', 'U', 15)
            pdf.cell(90, 15, 'HOJA DE RUTA:', 0, 0, 'R')
            pdf.set_font('Arial', '', 15)
            pdf.cell(100, 15, tipo + ' ' + nro, 0, 1, 'L')
            pdf.set_font('Arial', '', 10)
            #pdf.cell(50,8,'%s Nro: %s'% (tipo, nro),1,0,'L')

            pdf.cell(190, 8, 'Origen: %s' % origen, 1, 1, 'L')

            pdf.cell(50, 8, 'Fecha Doc: %s' % fecha_doc, 1, 0, 'C')
            pdf.cell(70, 8, 'Fecha Reg: %s' % fecha_reg, 1, 0, 'C')
            pdf.cell(70, 8, u'T\u00E9rmino: %s' % termino, 1, 1, 'C')
            pdf.cell(20, alto, 'Asunto:', 'TBL', 0, 'J')
            pdf.multi_cell(0, 6, asunto, 'TBR', 1, 'J')
            pdf.cell(38, 8, 'Entiende: ', 1, 0, 'C')
            pdf.cell(38, 8, 'Participa: ', 1, 0, 'C')
            pdf.cell(38, 8, 'Interviene: ', 1, 0, 'C')
            pdf.cell(38, 8, 'Copia: ', 1, 0, 'C')
            pdf.cell(38, 8, u'T\u00E9rmino interno: ', 1, 1, 'C')
            pdf.cell(38, 40, '', 1, 0, 'C')
            pdf.cell(38, 40, '', 1, 0, 'C')
            pdf.cell(38, 40, '', 1, 0, 'C')
            pdf.cell(38, 40, '', 1, 0, 'C')
            pdf.cell(38, 40, '', 1, 1, 'C')

            pdf.set_font('Arial', 'BI', 10)
            pdf.cell(100, 20, 'OBSERVACIONES / ORDENES', 0, 1, 'L')

            pdf.set_font('Arial', '', 10)
            pdf.cell(38, 18, '', 1, 0, 'C')
            pdf.cell(114, 18, '', 1, 0, 'C')
            pdf.cell(38, 18, '', 1, 1, 'C')
            pdf.cell(38, 18, '', 1, 0, 'C')
            pdf.cell(114, 18, '', 1, 0, 'C')
            pdf.cell(38, 18, '', 1, 1, 'C')
            pdf.cell(38, 18, '', 1, 0, 'C')
            pdf.cell(114, 18, '', 1, 0, 'C')
            pdf.cell(38, 18, '', 1, 1, 'C')
            pdf.cell(38, 18, '', 1, 0, 'C')
            pdf.cell(114, 18, '', 1, 0, 'C')
            pdf.cell(38, 18, '', 1, 1, 'C')
            pdf.cell(38, 18, '', 1, 0, 'C')
            pdf.cell(114, 18, '', 1, 0, 'C')
            pdf.cell(38, 18, '', 1, 1, 'C')
            pdf.cell(38, 18, '', 1, 0, 'C')
            pdf.cell(114, 18, '', 1, 0, 'C')
            pdf.cell(38, 18, '', 1, 1, 'C')
            pdf.cell(0, 12, '', 0, 1, 'R')
            pdf.cell(
                0, 6, '.......................................................', 0, 1, 'R')
            pdf.cell(0, 8, '', 0, 1, 'R')
            pdf.set_font('Arial', 'BI', 8)
            pdf.cell(0, 4, datetime.now().strftime(
                '%d/%m/%Y %H:%M'), 0, 1, 'C')
            pdf.set_title('Docuemnto Nro '+nro)
        filename = 'Hoja de ruta-{0}.pdf'.format(
            datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))
        response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            filename)
        response['Content-Type'] = 'application/pdf'
        return response

    exportar_a_excel_recibidos.short_description = "Exportar a Excel lista Doc(s) recibidos"
    exportar_a_excel_emitidos.short_description = "Exportar a Excel lista Doc(s) emitidos"
    exportar_hoja_ruta.short_description = "Generar hoja de ruta"


@admin.register(dependenciasInternas)
class DependenciasInternasAdmin(admin.ModelAdmin):
    list_display = ('dependencia',)
    search_fields = ['dependencia', 'pase1']
    list_per_page = 10


@admin.register(tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ('tipo',)
    search_fields = ['tipo']
    list_per_page = 10


@admin.register(unidades)
class UnidadesAdmin(admin.ModelAdmin):
    list_display = ('unidad',)
    search_fields = ['unidad']
    list_per_page = 10


@admin.register(estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('estado',)
    search_fields = ['estado']
    list_per_page = 10
