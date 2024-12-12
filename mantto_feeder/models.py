from django.db import models
from django.utils import timezone

class FeederRegistro(models.Model):
    # Campos correspondientes al JSON
    feeder_id = models.IntegerField()  # 'id-feeder'
    feeder_name = models.CharField(max_length=255)  # 'feeder' (nombre del feeder)
    feeder_code = models.CharField(max_length=50)  # 'codigo-feeder'
    color_feeder = models.CharField(max_length=50)  # 'color-feeder'
    color_semana = models.CharField(max_length=50)  # 'color-semana'
    tecnico = models.CharField(max_length=50)  # 'tecnico'
    tiempo_captura = models.IntegerField()  # 'tiempo_captura'
    observaciones = models.TextField()  # 'observaciones'
    tiempo = models.CharField(max_length=20)  # 'time'
    
    # Feeder estados
    CP = models.CharField(max_length=10, default="NG")  # 'CP'
    QP = models.CharField(max_length=10, default="NG")  # 'QP'
    HOVER = models.CharField(max_length=10, default="NG")  # 'HOVER'
    BFC = models.CharField(max_length=10, default="NG")  # 'BFC'
    
    # Fecha y hora de mantenimiento
    fecha_mantenimiento = models.DateField(max_length=10)  # 'fecha_mantenimiento'

    # Timestamp de creación
    fecha_creacion = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Feeder {self.feeder_name} - ID {self.feeder_id}"
    

class Cronometro(models.Model):
    # Si 'feeder_id' es un campo que no permite valores nulos, debes dar un valor por defecto
    feeder_id = models.CharField(max_length=255)  # Definir un valor por defecto
    tiempo_inicio = models.DateTimeField(default=timezone.now)
    tiempo_fin = models.DateTimeField(null=True, blank=True)

    def calcular_tiempo_captura(self):
        if self.tiempo_fin:
            diferencia = self.tiempo_fin - self.tiempo_inicio
            return diferencia.total_seconds()  # Devuelve el tiempo en segundos
        return 0  # Si no se ha detenido el cronómetro, retorna 0

    def __str__(self):
        return f"Cronómetro para Feeder {self.feeder_id}"