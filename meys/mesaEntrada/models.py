from django.db import models
from django.utils import timezone
import datetime


#Definicion de metodos auxiliares
def crear_numero():
    ultimo_documento = documento.objects.all().order_by('id').last()
    if not ultimo_documento:
        return 'SG-' + str(datetime.date.today().year) + '/' + '0000'
    id_documento = ultimo_documento.Nro_sistema
    numero_entero = int(id_documento[9:12])
    nuevo = numero_entero + 1
    nuevo_numero = 'SG-' + str(str(datetime.date.today().year)) +'/' + str(nuevo).zfill(4)
    return nuevo_numero

#Fin metodos auxiliares

class unidades(models.Model):
    unidad= models.CharField(max_length=50)
    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"
    def __str__(self):
        return self.unidad

class dependenciasInternas(models.Model):
    dependencia = models.CharField(max_length=50, verbose_name="Nombre de la dependencia", help_text="Nombre de la dependencia a donse se entren los documentos")
    class Meta:
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"
    def __str__(self):
        return self.dependencia

class tipo(models.Model):
    tipo=models.CharField(max_length=20)
    class Meta:
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"
    def __str__(self):
        return self.tipo

class estado(models.Model):
    estado=models.CharField(max_length=50)
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return self.estado

class documento(models.Model):
    opciones_tramite = [
    ('RE', 'Recibido'),
    ('EM', 'Emitido'),]

    Tramite=models.CharField(max_length=2,choices=opciones_tramite,default='RE',)
    nro_documento=models.CharField(max_length=50,null=True,blank=False,verbose_name='Nro Documento',help_text='Ingrese el Número del documento, recuerde que este valor es utilizado para las busquedas')
    Nro_sistema= models.CharField(max_length = 20, default = crear_numero, editable=False)
    Tipo=models.ForeignKey(tipo,models.SET_NULL,null=True,)
    opciones = [
    ('PU', 'Público'),
    ('RE', 'Reservado'),
    ('CO', 'Confidencial'),
    ('SE', 'Secreto'),]

    Clasificacion=models.CharField(max_length=2,choices=opciones,default='PU',)
    Fecha_entrada=models.DateField(default=timezone.now,verbose_name='Fecha del documento',)
    Fecha_salida=models.DateField(auto_now=True, auto_now_add=False)
    Fecha_registro=models.DateField(auto_now=True, auto_now_add=False)
    asunto=models.TextField(max_length=200,help_text='Maximo de 200 caracteres')
    origen= models.ForeignKey(unidades,models.SET_NULL,verbose_name='Origen/Destino',null=True,)
    Estado= models.ForeignKey(estado,models.SET_NULL,null=True,)
    Termino=models.DateField(blank=True,null=True)
    Documento_relacionado=models.ManyToManyField('self',models.SET_NULL,verbose_name='Documentos relacionados',blank=True,)
    Obs=models.TextField(max_length=200,blank=True)
    archivo=models.FileField(blank=True,null=True,)
    Termino_interno=models.DateField(blank=True, null=True)
    pase=models.ManyToManyField(dependenciasInternas,related_name="pase", verbose_name="Pase a:", blank=True )
    entiende=models.ManyToManyField(dependenciasInternas,related_name="entiende", verbose_name="Entiende:", blank=True )
    participa=models.ManyToManyField(dependenciasInternas,related_name='participa', verbose_name='Participa:', blank=True,)
    interviene=models.ManyToManyField(dependenciasInternas,related_name='interviene', verbose_name='Interviene:',blank=True,)
    copia=models.ManyToManyField(dependenciasInternas,related_name='copia',verbose_name='Copia:',blank=True,)

    def filename(self):
        return os.path.basename(self.archivo.name)
    def __str__(self):
        return self.nro_documento

    def save(self, *args, **kwargs):
        self.nro_documento = (self.nro_documento).upper()
        return super(documento, self).save(*args, **kwargs)    
