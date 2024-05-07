from django.urls import path

from usuario.views import Index
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [ 
    path('',Index.as_view(), name='index'),
    path('login/',views.login_user, name='login_user'),
    path('logout',views.logout_user, name='logout_user'),
    path('registrar',views.registrar, name='registrar'),
]
