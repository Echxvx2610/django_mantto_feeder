from django.db import models

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
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Feeder {self.feeder_name} - ID {self.feeder_id}"