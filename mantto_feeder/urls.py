from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('home/',views.home ,name='home'),
    path('analisis/',views.analisis ,name='analisis'),
    path('reparaciones/',views.reparaciones ,name='reparaciones'),
    path('reportes/',views.reportes ,name='reportes'),
    path('about/',views.about ,name='about'),
    path('registro',views.registro ,name='registro'),
    path('consultar/',views.consultar ,name='consultar'),
]
