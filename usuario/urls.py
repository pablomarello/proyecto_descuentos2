from django.urls import path

from usuario.views import Index
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

urlpatterns = [ 
    path('',views.index, name='index'),
    #path('login/',views.login_user, name='login_user'),
    #path('logout',views.logout_user, name='logout_user'),
    path('registrar_usuario/<int:persona_id>',views.registrar_usuario, name='registrar_usuario'),
    path('token_input',views.token_input, name='token_input'),
    #inicio y cierre de sesion 
    path('login/',views.iniciar_sesion,name='login'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    #CAMBIO DE CONTRASEÑA
    path('reset_password/', PasswordResetView.as_view(),{'template_name':'registration/password_reset_form.html','email_template':'registration/password_reset_email.html'}, name='reset_password'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',views.CustomPasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('mapa/',views.mapa,name='mapa')

]
