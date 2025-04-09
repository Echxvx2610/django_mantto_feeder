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
    HOVER = models.CharField(max_length=10, default="NG")  # 'HOOVER'
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

class PartesFeeder(models.Model):
    numero_parte = models.CharField(max_length=50, unique=True)  # Número de parte
    nombre = models.CharField(max_length=255)  # Nombre de la parte
    costo = models.DecimalField(max_digits=10, decimal_places=2)  # Costo de la parte
    stock_minimo = models.IntegerField(default=0)  # Stock mínimo requerido
    cantidad = models.IntegerField()  # Cantidad en inventario
    estado = models.CharField(max_length=50, default="Disponible")  # Estado de la parte (ej. Disponible, En uso, etc.)
    fecha_registro = models.DateTimeField(auto_now_add=True)  # Fecha de registro
    
    def __str__(self):
        return f"No.part: {self.numero_parte} - nombre: {self.nombre} - costo: {self.costo} - stock_minimo: {self.stock_minimo} - cantidad: {self.cantidad} - estado: {self.estado} - fecha_registro: {self.fecha_registro}"
    
class FeederParaReparar(models.Model):
    feeder_id = models.IntegerField()  # id-feeder
    tamano = models.CharField(max_length=5)  # tamaño ejemplo 12x04 , 08x04, 12x02, 08x02
    color = models.CharField(max_length=20)  # color ejemplo rojo, azul, verde, etc.
    falla = models.CharField(max_length=255)  # falla ejemplo: no avanza, traga tape
    parte = models.ForeignKey(PartesFeeder, on_delete=models.CASCADE)  # Relación con PartesFeeder
    cantidad_refaccion = models.IntegerField()  # cantidad de refacciones ejemplo: 2, 3, 4, etc.
    tecnico = models.CharField(max_length=50)  # tecnico ejemplo: Juan, Pedro, etc.
    fecha_registro = models.DateTimeField(auto_now_add=True)  # Fecha de registro
    
    def __str__(self):
        return f"Feeder ID: {self.feeder_id} - Tamaño: {self.tamano} - Falla: {self.falla} - Refacción: {self.parte.nombre} - Cantidad: {self.cantidad_refaccion}"
    

class PartesRequeridas(models.Model):
    feeder_id = models.ForeignKey(FeederParaReparar, on_delete=models.CASCADE)  # Relación con FeederParaReparar
    numero_parte = models.ForeignKey(PartesFeeder, on_delete=models.CASCADE,default=None)  # Relación con PartesFeeder
    nombre = models.CharField(max_length=255) # Nombre de la parte
    costo = models.DecimalField(max_digits=10, decimal_places=2)  # Costo de la parte
    cantidad = models.IntegerField()  # Cantidad requerida
    
    def __setr__(self):
        return f"Feeder ID: {self.feeder_id} - No. Parte: {self.numero_parte} - Nombre: {self.nombre} - Costo: {self.costo} - Cantidad: {self.cantidad}"
    
