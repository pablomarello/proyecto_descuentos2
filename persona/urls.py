

from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('registrar',views.registrar_persona, name='registrar_persona'),
]
