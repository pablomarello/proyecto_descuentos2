
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#from persona.models import Persona


class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    rol = models.CharField('Rol', max_length=50, unique=True)

    class Meta:
        verbose_name= 'Rol'
        verbose_name_plural = 'Roles'
    
    def __str__ (self):
        return self.rol

class UsuarioManager(BaseUserManager):
    
    def _create_user(self,username,email,password,is_staff,is_superuser,**extra_fields):
        if not email:
            raise ValueError('El usuario deber tener un correo electrónico!')
        
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            is_staff= is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    #crear usuario basico
    def create_user(self, username, email,is_staff, password=None, **extra_fields):
        return self._create_user(username, email, password,is_staff, False, **extra_fields)
    #crear usuario administrador
    def create_superuser(self,username,email,password = None, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)
        


class Usuario(AbstractBaseUser,PermissionsMixin):
    username = models.CharField('Nombre de usuario',unique=True,max_length=50)
    email = models.EmailField('Correo Electrónico',max_length=100,unique=True)
    # usuario_administrador = models.BooleanField(default=False)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default=False)
    token= models.CharField(max_length=30,null=True,blank=True)
    fecha_creacion_token= models.DateTimeField(null=True,blank=True)
    actividad_inicio= models.DateTimeField(null=True,blank=True)
    actividad_fin = models.DateTimeField(null=True,blank=True)
    fecha_creacion= models.DateTimeField(auto_now_add=True,null=True,blank=True)
    usuario_creacion= models.PositiveIntegerField(null=True,blank=True)
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion= models.DateTimeField(null=True,blank=True)
    usuario_eliminacion= models.PositiveIntegerField(null=True,blank=True)
    #campos c/ clave foranea
    rol_id = models.OneToOneField(Rol, on_delete=models.CASCADE, blank=True,null=True) #depues sacar blank y null
    #persona_id = models.OneToOneField(Persona, on_delete=models.CASCADE, blank=True,null=True)  #depues sacar blank y null
    objects = UsuarioManager()
    

    #hace referencia a cual es el parametro unico (requerido) del usuario
    USERNAME_FIELD = 'username'
    #campos requeridos
    REQUIRED_FIELDS = ['email']

    def __str__ (self):
        return f'Usuario: {self.username}'
    
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
    

# Create your models here.
