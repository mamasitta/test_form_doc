
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.admin_index, name='admin_index'),
    path('form_details/<id>/', views.form_details, name='form_details'),
    path('user_registration', views.user_registration, name='user_registration'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('create_form/', views.create_form, name='create_form'),
    path('application/', views.user_application, name='user_application'),
    path('sign_confirmation/?P<aid>[0-9A-Za-z_\-]/', views.sign_confirmation, name='sign_confirmation'),
    path('sign/?P<aid>[0-9A-Za-z_\-]/', views.sign, name='sign'),
    path('final_preview/<aid>/', views.final_preview, name='final_preview'),
    path('download_application/<id>/', views.download_application, name='download_application')
]
