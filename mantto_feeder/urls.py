from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',RedirectView.as_view(url='/home/', permanent=False)),
    path('home/',views.home ,name='home'),
    path('analisis/',views.analisis ,name='analisis'),
    path('reparaciones/',views.reparaciones ,name='reparaciones'),
    path('reportes/',views.reportes ,name='reportes'),
    path('about/',views.about ,name='about'),
    path('registro/',views.registro ,name='registro'),
    path('inventario/',views.inventario ,name='inventario'),
    path('consultar/',views.consultar ,name='consultar'),
    path('iniciar_cronometro/', views.iniciar_cronometro, name='iniciar_cronometro'),
    path('detener_cronometro/<int:cronometro_id>/', views.detener_cronometro, name='detener_cronometro'),
    path('api/agregar_parte/',views.agregar_parte ,name='agregar_parte'),
    path('agregar_parte_form/',views.agregar_parte_form ,name='agregar_parte_form'),
    path('registrar_reparacion_form/', views.registrar_reparacion_form, name='registrar_reparacion_form'),
    path('agregar_parte_requerida_form/', views.agregar_parte_requerida_form, name='agregar_parte_requerida_form'),
]
