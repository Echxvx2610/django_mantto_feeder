import os
import django

# Configura el entorno de Django y carga la configuración
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_feeder.settings")
django.setup()

from mantto_feeder.models import FeederRegistro  # Ahora puedes importar el modelo
from faker import Faker
import random

# Configuración de Faker y generación de datos
fake = Faker()

def generate_random_feeder():
    feeder_id = random.randint(100000000, 999999999)
    feeder_name = random.choice(["CP6 8X2 PAPER","CP6 8X4 PAPER"])
    feeder_code = f"FEEDER-{feeder_id}"
    color_feeder = random.choice(["ROJO", "VERDE", "AZUL", "NEGRO","NARANJA"])
    color_semana = random.choice(["VERDE", "AZUL", "NEGRO","CAFE","NARANJA"])
    tecnico = random.choice(["002652A","015310A","014685A"])
    tiempo_captura = random.randint(5, 120)
    observaciones = random.choice(["N/A","Tape lift dañado"])
    tiempo = fake.time()
    CP = "OK"
    QP = "NG"
    HOVER = "NG"
    BFC = "NG"
    fecha_mantenimiento = fake.date_between(start_date='-90d', end_date='today')

    FeederRegistro.objects.create(
        feeder_id=feeder_id,
        feeder_name=feeder_name,
        feeder_code=feeder_code,
        color_feeder=color_feeder,
        color_semana=color_semana,
        tecnico=tecnico,
        tiempo_captura=tiempo_captura,
        observaciones=observaciones,
        tiempo=tiempo,
        CP=CP,
        QP=QP,
        HOVER=HOVER,
        BFC=BFC,
        fecha_mantenimiento=fecha_mantenimiento
    )

# Crear registros aleatorios
for _ in range(500):
    generate_random_feeder()
