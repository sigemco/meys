db=context.getParentDatabase()
url=db.absolute_url()
usuario=db.getCurrentUserId()
cache=db.getCache(usuario)
if not cache:
    db.cacheUsusario.runAgent() 
    cache=db.getCache(usuario)
    
tipo = context.REQUEST.get('tipo_docu')
est=context.REQUEST.get('estadoAcuse')
desde = context.REQUEST.get('desde')
hasta = context.REQUEST.get('hasta')
des_int=context.REQUEST.get('Sub_des')
docIds=context.REQUEST.get('docIds')
docIds=docIds.split('@')
docIds.remove('')
resultados=[db.getDocument(x) for x in docIds]


import StringIO
output = StringIO.StringIO()

from xlsxwriter.workbook import Workbook
output = StringIO.StringIO()
workbook = Workbook(output)
worksheet = workbook.add_worksheet()
#propiedades de pagina
worksheet.set_landscape()
worksheet.set_paper(9)
worksheet.center_horizontally()
#formato de celdas
bold = workbook.add_format({'bold': 1})
bold.set_font_color('white')
bold.set_font_name('Times New Roman')
bold.set_align('center')
bold.set_fg_color('#205C90')
bold.set_border(2)
bold.set_text_wrap()
texto=workbook.add_format()
texto.set_font_name('Times New Roman')
texto.set_border(1)
texto.set_align('vcenter')
texto.set_font_size(9)
texto.set_text_wrap()

texto1=workbook.add_format()
texto1.set_align('center')


asunto=workbook.add_format()
asunto.set_text_wrap()

titulo_pagina=workbook.add_format({'bold': 1})
fechaFuente= workbook.add_format({'bold': 1})
titulo_pagina.set_align('center')
fechaFuente.set_align('left')

worksheet.merge_range('A3:C3','Desde: '+desde, fechaFuente)
worksheet.merge_range('E3:H3','Hasta: '+hasta, fechaFuente)
        

titulo='Listado de documentos recibidos'
worksheet.merge_range('A1:H1',titulo, titulo_pagina)
worksheet.merge_range('A2:H2','Filtrado por: '+tipo, titulo_pagina)


cabezera=['Tipo','Nro','Asunto','Unidad origen','Fecha registro','Termino','Destino interno','Firma Rubrica']
worksheet.write_row('A5', cabezera,bold)

cabecera = '&CMEYS %s' % cache['unidad']
pie = '&LImpreso el &D a las &T&R Pagina &P de &N'
worksheet.set_header(cabecera)
worksheet.set_footer(pie)

worksheet.set_column(2,2, 30,asunto)
worksheet.set_column(3,3, 18,asunto)
worksheet.set_column(4,4, 6,texto1)
worksheet.set_column(1,1, 8,texto1)
worksheet.set_column(0,0, 7,texto1)
worksheet.set_column(5,5, 6,texto1)
worksheet.set_column(6,6, 11,texto1)
worksheet.set_column(7,7, 8,texto1)
n=6
def dep_internas(doc):
    dep=doc.getItem('destinosInternos')
    dep2=doc.getItem('destinosInternosNuevos')
    if dep:
        return dep
    elif  dep2 and cache['idUnidad'] in dep2.keys(): 
        return dep2[cache['idUnidad']]
    else:
        return []


def datos(doc):
    lista=[]
    lista.append(doc.getItem('tipoDoc'))
    lista.append(doc.getItem('nro_Expediente'))
    lista.append(doc.getItem('asunto'))
    if isinstance(doc.getItem('Unidad_origen'),unicode):
        lista.append(doc.getItem('Unidad_origen'))
    else:
        lista.append(('-').join(doc.getItem('Unidad_origen')))
    lista.append(DateToString(doc.getItem('fecha_Meys_Or'),format='%d/%m/%Y'))
    lista.append(doc.getItem('termino'))
    lista.append(('-').join(dep_internas(doc)))
    lista.append('')
    return lista
for x in resultados:
    doc=x    
    worksheet.write_row('A'+str(n), datos(doc),texto)
    n+=1



worksheet.repeat_rows(5)
workbook.close()
output.seek(0)
context.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename=listado-doc-recibidos.xlsx')
context.REQUEST.RESPONSE.setHeader('Content-type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8')
context.REQUEST.RESPONSE.setBody(output.read())