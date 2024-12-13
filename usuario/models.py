from django.db import models
from crum import get_current_user
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
from persona.models import Persona
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings


# Create your models here.

#validacion_usuario=RegexValidator(
 #   regex=r'^[a-zA-Z0-9]{4,15}*$',
  #  message='Introduzca un nombre de usuario valido. Este solo puede incluir letras y numeros'
#)

class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    rol = models.CharField('Rol', max_length=50, unique=True)

    class Meta:
        verbose_name= 'Rol'
        verbose_name_plural = 'Roles'
    
    def __str__ (self):
        return self.rol

class UsuarioManager(BaseUserManager):
    
    def _create_user(self,username,email,password,is_staff,is_superuser,is_active,**extra_fields):
        if not email:
            raise ValueError('El usuario deber tener un correo electrónico!')
        
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            is_staff= is_staff,
            is_superuser = is_superuser,
            is_active= is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
   
    #crear usuario administrador
     # Crear superusuario
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Aseguramos que el superusuario esté activo
        return self._create_user(username, email, password, **extra_fields)
        



#SE CAMBIÓ EL is_active a False! y la fecha de creacion del token
class Usuario(AbstractBaseUser,PermissionsMixin):
    metodo_verificacion = models.CharField(max_length=80, default='email')
    username = models.CharField('Nombre de usuario',unique=True,max_length=50)
    email = models.EmailField('Correo Electrónico',max_length=100, null=True)
    telefono=models.CharField('SU TELEFONO: ',max_length=40, null=True)
    # usuario_administrador = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    token= models.CharField(max_length=30,null=True,blank=True)
    fecha_creacion_token= models.DateTimeField(auto_now_add=True, null=True)
    actividad_inicio= models.DateTimeField(null=True,blank=True)
    actividad_fin = models.DateTimeField(null=True,blank=True)
    fecha_creacion= models.DateTimeField(auto_now_add=True,null=True,blank=True)
    usuario_creacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         null=True, blank=True, related_name='usuarios_creados')
    usuario_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                             null=True, blank=True, related_name='usuarios_modificados')
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    eliminado = models.BooleanField(default=False)
    usuario_eliminacion = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                                            null=True, blank=True, related_name='usuarios_eliminados')
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)
    #campos c/ clave foranea
    rol_id = models.OneToOneField(Rol, on_delete=models.CASCADE, blank=True,null=True) #depues sacar blank y null
    persona_id = models.OneToOneField(Persona, on_delete=models.CASCADE,related_name='usuario', blank=True,null=True)  #depues sacar blank y null
    objects = UsuarioManager()
    

    #hace referencia a cual es el parametro unico (requerido) del usuario
    USERNAME_FIELD = 'username'
    #campos requeridos
    REQUIRED_FIELDS = ['email']

    def __str__ (self):
        return f'Usuario: {self.username}'
    
    def save(self, force_insert = False, force_update = False, using = None,
              update_fields = None):
        user = get_current_user()
        # Evitar bucles y usuarios no válidos
        if user and user.is_authenticated:
            if not self.pk:  # Usuario nuevo
                self.usuario_creacion = user
            else:  # Actualización de usuario existente
                self.usuario_modificacion = user
        super(Usuario, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        user = get_current_user()
        if user is not None:
            self.usuario_eliminacion = user
        self.fecha_eliminacion = timezone.now()
        self.eliminado = True
        self.save()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
        
#AUIDITORIAS
    # Señal para registrar el usuario que crea la cuenta
@receiver(pre_save, sender=Usuario)
def set_usuario_creacion(sender, instance, **kwargs):
    if not instance.pk and hasattr(instance, '_current_user'):
        instance.usuario_creacion = instance._current_user.id
class ActividadUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    actividadinicio = models.DateTimeField(null=True, blank=True)
    actividadfin = models.DateTimeField(null=True, blank=True)

    # Método para registrar el inicio de sesión
    def registrar_inicio_sesion(self):
        self.actividadinicio = timezone.now()
        self.save()

    # Método para registrar el cierre de sesión
    def registrar_cierre_sesion(self):
        self.actividadfin = timezone.now()
        self.save()

    def __str__(self):
        return f'Sesión de {self.usuario} desde {self.actividadinicio} hasta {self.actividadfin}'

    #para que se pueda utilizar el modelo Usuario en el admin de django
    """ def has_perm(self,perm,obj= None):
        return True """
    #tmb para el admin de django, recibe la etiqueta de la app en la cual esta el modelo
    """ def has_module_perms(self,app_label):
        return True """
    
    #valida si un usuario es administrador o no
    """ @property
    def is_staff(self):
        return self.usuario_administrador
 """