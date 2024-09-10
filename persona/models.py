from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
#from usuario.models import Usuario

validacion = RegexValidator(
    regex=r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]{2,25}( [a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]{2,25})*$',
    message='Ingrese un dato válido. Sólo se permiten letras, espacios, guiones y apóstrofes'
)

validacion_dni=RegexValidator(
    regex=r'^[0-9]{8}$',
    message='Ingrese un numero de DNI válido. Solo se permiten 8 digitos númericos.'
)

class Persona(models.Model):
    GENERO=[('M','Masculino'),
            ('F','Femenino'),
            ('N','No Binario')]
    
    identificacion= models.IntegerField(primary_key=True, verbose_name='D.N.I.', help_text='Ingrese el nro de dni sin puntos')#, validators=[validacion_dni])
    nombres=models.CharField(max_length=50, help_text='Si posee mas de un nombre ingrese los mismos con un espacio entre cada nombre. Ej: Juan Carlos')#,null=True,blank=True, validators=[validacion])
    apellidos=models.CharField(max_length=25, help_text='Si posee mas de un apellido ingrese los mismos con un espacio entre cada apellido. Ej: Rodriguez Perez',null=True,blank=True)#,validators=[validacion])
    genero=models.CharField(max_length=15,choices=GENERO,null=True,blank=True)
    fecha_creacion= models.DateTimeField(auto_now_add=True,null=True,blank=True)
    foto=models.ImageField(upload_to='personas/',default='avatar_default.png',null=True,blank=True)
    usuario_creacion= models.PositiveIntegerField(null=True,blank=True)
    habilitado = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion= models.DateTimeField(null=True,blank=True)
    usuario_eliminacion= models.PositiveIntegerField(null=True,blank=True)

    #usuario_id = models.OneToOneField(Usuario, on_delete=models.CASCADE, blank=True,null=True)
    
    

    class Meta:
        verbose_name='Persona'
        verbose_name_plural= 'Personas'
        db_table= 'persona'


class TablaPais(models.Model):
    cod_pais = models.CharField(primary_key=True)
    nom_pais = models.CharField(blank=True, null=True)
    
    def __str__(self):
        return self.nom_pais
    

    class Meta:
        managed = False
        db_table = 'tabla_pais'

class TablaProvincia(models.Model):
    cod_pcia = models.CharField(primary_key=True)
    nom_pcia = models.CharField(blank=True, null=True)
    pais_id_id = models.CharField(blank=True, null=True)
    
    def __str__(self):
        return self.nom_pcia

    class Meta:
        managed = False
        db_table = 'tabla_provincia'
               
class TablaDepartamento(models.Model):
    cod_depto = models.CharField(primary_key=True)
    nom_depto = models.CharField(blank=True, null=True)
    provincia_id_id = models.CharField(blank=True, null=True)
    
    def __str__(self):
        return self.nom_depto

    class Meta:
        managed = False
        db_table = 'tabla_departamento'


class TablaMunicipio(models.Model):
    cod_agl = models.CharField(primary_key=True)
    nom_agl = models.CharField(blank=True, null=True)
    departamento_id_id = models.CharField(blank=True, null=True)
    
    def __str__(self):
        return self.nom_agl
    

    class Meta:
        managed = False
        db_table = 'tabla_municipio'

class TablaLocalidad(models.Model):
    cod_ase = models.CharField(primary_key=True)
    nombre = models.CharField(blank=True, null=True)
    tipo = models.CharField(blank=True, null=True)
    lat_gd = models.CharField(blank=True, null=True)
    long_gd = models.CharField(blank=True, null=True)
    fuente = models.CharField(blank=True, null=True)
    municipio_id_id = models.CharField(blank=True, null=True)
    lat_gs = models.CharField(blank=True, null=True)
    long_gs = models.CharField(blank=True, null=True)

    
    def __str__(self):
        return self.nombre
    
    class Meta:
        managed = False
        db_table = 'tabla_localidad'

class ubicaciones(models.Model):
    persona_id=models.OneToOneField(Persona,blank=True,null=True,on_delete=models.CASCADE,related_name='ubicacion',db_column="identificacion")
    pais=models.ForeignKey(TablaPais,blank=False,null=False,on_delete=models.CASCADE,db_column="cod_pais")
    provincia=models.ForeignKey(TablaProvincia,blank=False,null=False,on_delete=models.CASCADE,db_column="cod_pcia")
    departamento=models.ForeignKey(TablaDepartamento, blank=False,null=False ,on_delete=models.CASCADE,db_column="cod_depto")
    municipio=models.ForeignKey(TablaMunicipio,blank=False,null=False,on_delete=models.CASCADE,db_column="cod_agl")
    localidad=models.ForeignKey(TablaLocalidad,blank=False,null=False,on_delete=models.CASCADE,db_column="cod_ase")
    barrio=models.CharField(max_length=100,blank=False,null=False)
    calle=models.CharField(max_length=50,blank=True,null=True)
    altura=models.CharField(max_length=20,blank=True,null=True)
    latitud = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    #lat
    #long
    class Meta:
        verbose_name='Ubicacion'
        verbose_name_plural= 'Ubicaciones'
        db_table= 'ubicacion'


