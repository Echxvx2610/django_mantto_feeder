import pandas as pd

# Ruta del archivo CSV
csv_path = r'H:\Ingenieria\Ensamble PCB\Documentacion ISO-9001\plan feeders SEM.csv'

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv(csv_path , encoding='latin-1')

# Verifica el tipo de la columna 'ID_feeder' para asegurarte de que se convierta correctamente
# Asegúrate de que 'ID_feeder' esté presente en el archivo CSV
if 'serie' in df.columns:
    # Convierte la columna 'ID_feeder' a entero (usando pd.to_numeric, con errores='coerce' para manejar valores no numéricos)
    df['serie'] = pd.to_numeric(df['serie'], errors='coerce')

    # Ahora guardamos el DataFrame de nuevo en el archivo CSV
    df.to_csv(csv_path, index=False)

    print(f"Archivo CSV actualizado y guardado correctamente en {csv_path}.")
else:
    print("La columna 'ID_feeder' no se encuentra en el archivo CSV.")
