from django.contrib import admin
from .models import FeederRegistro,Cronometro

class FeederRegistroAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista del admin
    list_display = ('feeder_id', 'feeder_name', 'feeder_code', 'color_feeder', 'color_semana', 'tecnico', 'tiempo_captura', 'fecha_mantenimiento', 'fecha_creacion')
    
    # Campos por los que se puede buscar en el admin
    search_fields = ('feeder_id', 'feeder_name', 'feeder_code', 'color_feeder', 'color_semana', 'tecnico', 'fecha_mantenimiento')

    # Filtros laterales (barra lateral)
    list_filter = ('fecha_mantenimiento', 'fecha_creacion', 'CP', 'QP', 'HOVER', 'BFC')

    # Filtro personalizado para "fecha_mantenimiento"
    class FechaMantenimientoFilter(admin.SimpleListFilter):
        title = 'Fecha de Mantenimiento'
        parameter_name = 'fecha_mantenimiento'

        def lookups(self, request, model_admin):
            return (
                ('today', 'Hoy'),
                ('this_week', 'Esta semana'),
                ('this_month', 'Este mes'),
            )

        def queryset(self, request, queryset):
            from datetime import timedelta
            from django.utils import timezone

            if self.value() == 'today':
                return queryset.filter(fecha_mantenimiento=timezone.now().date())
            elif self.value() == 'this_week':
                start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
                return queryset.filter(fecha_mantenimiento__gte=start_of_week)
            elif self.value() == 'this_month':
                start_of_month = timezone.now().replace(day=1)
                return queryset.filter(fecha_mantenimiento__gte=start_of_month)
            return queryset

    # Registra el filtro personalizado
    list_filter = ('fecha_mantenimiento', 'fecha_creacion', 'CP', 'QP', 'HOVER', 'BFC', FechaMantenimientoFilter)

# Registra el modelo con su clase de administración personalizada
admin.site.register(FeederRegistro, FeederRegistroAdmin)

class CronometroAdmin(admin.ModelAdmin):
    list_display = ('feeder_id', 'tiempo_inicio', 'tiempo_fin', 'calcular_tiempo_captura')
    
    # Agregar los campos que deseas que sean buscables en el panel de admin
    search_fields = ('feeder_id', 'tiempo_inicio')

    # También puedes usar filtros laterales
    list_filter = ('tiempo_inicio', 'tiempo_fin')  # Puedes agregar más filtros si lo deseas

# Registra el modelo con su clase de administración personalizada
admin.site.register(Cronometro, CronometroAdmin)