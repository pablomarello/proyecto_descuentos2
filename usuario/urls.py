from django.urls import path

from usuario.views import Index
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [ 
    path('',Index.as_view(), name='index'),
    path('login/',views.login_user, name='login_user'),
    path('logout',views.logout_user, name='logout_user'),
    path('registrar_usuario/<int:persona_id>',views.registrar_usuario, name='registrar_usuario'),
    path('token_input',views.token_input, name='token_input'),
]
