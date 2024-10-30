#-*- coding: utf-8 -*-
import csv
import pandas as pd
import openpyxl
from openpyxl import workbook,load_workbook
from openpyxl.utils import get_column_letter
#from openpyxl.styles import Font, Alignment, Border, Side
from datetime import datetime,time
import asyncio
import tracemalloc
import PySimpleGUI as sg
"""
#testeo de memoria tracemalloc
tracemalloc.start()

snapshot1 = tracemalloc.take_snapshot()
"""
    
#*********************** Declarar fecha ************************
fecha_actual = datetime.now()
fecha_formateada = fecha_actual.strftime(f'{fecha_actual.month}/{fecha_actual.day}/{fecha_actual.year}')   


#*********************** Configuracion de dataframe(muestra todo el dataframe)********************
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

#***************************** Creacion de un dataframe ********************************
#data = pd.read_csv(r'C:\Users\CECHEVARRIAMENDOZA\OneDrive - Brunswick Corporation\Documents\Proyectos_Python\PysimpleGUI\Proyectos\mantto_feeder\data\plan feeders SEM.csv',encoding='ISO-8859-1',usecols=['serie','feeder'])
#data = pd.read_csv(r'H:\Ingenieria\Ensamble PCB\Documentacion ISO-9001\plan feeders SEM.csv',encoding='ISO-8859-1',usecols=['serie','feeder'],low_memory=False) #ruta oficial de documento
data = pd.read_csv(r'mantto_feeder\data\plan_feeders_SEM.csv',encoding='ISO-8859-1',usecols=['serie','feeder'],low_memory=False)
df = pd.DataFrame(data)

#**************************** Renombrar columnas ********************************
df.rename(columns={'serie':'ID_feeder'},inplace=True)
df.rename(columns={'feeder':'Feeder'},inplace=True)

#print(df)

# def search_id(ID_FEEDER):
#      '''
#      search_id(ID_FEEDER:int)
#          toma como parametro el id del feeder,mismo que sera proporcionado por la app feeder status
#          mediante el escaneo de los feeders.
#          retorna: un dataframe con todos los datos del feeder ( ID_feeder, Feeder )  
       
#          extra:
#              -Index ID_feeder: index de ID_feeder(posicion del dato en csv)
#              -Index fecha: index de fecha (posicion del dato en csv)
#      '''
#      #buscar feeder por id
#      if ID_FEEDER in df['ID_feeder'].values:
#          #valores de index feeder y fecha "erroneos" solo para guiarse en CSV
#          resultado = df.loc[df['ID_feeder'] == ID_FEEDER].to_string(index = False)
#          id_feeder = resultado.split()
#          descripcion = id_feeder[3]
#          return resultado
#adapata a web
def search_id(ID_FEEDER):
    '''
    search_id(ID_FEEDER: int)
        Busca un feeder por ID en el DataFrame.
        Retorna un diccionario con la descripción del feeder o None si no se encuentra.
    '''
    if ID_FEEDER in df['ID_feeder'].values:
        resultado = df.loc[df['ID_feeder'] == ID_FEEDER].to_string(index=False)
        id_feeder = resultado.split()
        descripcion = id_feeder[3:6]  # Extraemos la descripción
        # Convertimos la descripción en una cadena de texto
        descripcion = ' '.join(descripcion)
        return {
            "id_feeder": ID_FEEDER,
            "feeder": descripcion
        }
    return None  # Si no se encuentra el feeder, retornamos None 
  
     
#index feeder y fecha
def index_ff(ID_FEEDER):
    #Obtener index de feeder
    valor_feeder = ID_FEEDER
    indice_feeder = int(df['ID_feeder'].index[df['ID_feeder']==valor_feeder][0]) + 2
  
    with open(r'H:\Ingenieria\Ensamble PCB\Documentacion ISO-9001\plan feeders SEM.csv', 'r') as plan_semanal: #ruta oficial de documento
        # Crea un lector CSV
        lector_csv = csv.reader(plan_semanal)
        # Obtiene la primera fila del archivo CSV
        primera_fila = next(lector_csv)
        # Obtiene los valores del rango 
        valores_rango = primera_fila[0:1502]  # Índices de las columnas que tienen por nombre las fechas del año
        #Crear dataframe con los valores obtenidos del csv(columnas fechas)    
        data_fecha = pd.DataFrame(valores_rango)
        #Obtener index de fecha
        valor_fecha = fecha_formateada
  
    indice_fecha = int(data_fecha[0].index[data_fecha[0]==valor_fecha][0]) + 1
    return indice_feeder,indice_fecha
#************************** Analisis de datos (plan feeders SEM )********************************
def cell_value(ID_FEEDER:int):
    '''
    cell_value(ID_FEEDER:int)
        retorna una tupla con los valores de interseccion entre el id de un feeder respecto a la columna fecha,color y codigo
    '''
    #cargar archivo excel
    # Abre el archivo CSV en modo lectura
    with open(r'H:\Ingenieria\Ensamble PCB\Documentacion ISO-9001\plan feeders SEM.csv','r') as plan_semanal:#ruta oficial de documento
        # Crea un lector CSV
        lector_csv = csv.reader(plan_semanal)
        # Obtiene la primera fila del archivo CSV
        primera_fila = next(lector_csv)
        # Obtiene los valores del rango A1:H1
        valores_rango = primera_fila[0:1502]  # Índices de las columnas que tienen por nombre las fechas del año
  
        #Crear dataframe con los valores obtenidos del csv(columnas)    
        data_fecha = pd.DataFrame(valores_rango)
        try:
            #Valores de index feeder y fecha "Exactos" para analisis de CSV
            #Obtener index de feeder
            valor_feeder = ID_FEEDER
            indice_feeder = int(df['ID_feeder'].index[df['ID_feeder']==valor_feeder][0])
            #print("Indice feeder: ",indice_feeder + 2) # + 2 debido al index
            #Obtener index de fecha
            fecha_actual = datetime.now()
            fecha_formateada = fecha_actual.strftime(f'{fecha_actual.month}/{fecha_actual.day}/{fecha_actual.year}')
            valor_fecha = fecha_formateada
            indice_fecha = int(data_fecha[0].index[data_fecha[0]==valor_fecha][0])
            #print('Indice de fecha buscada: ',indice_fecha + 1) # + 1 debido al index
            #comprobar si hay un OK en una interseccion data por el index de un feeder y el index de una fecha(funcionando)
            csv_data  = list(lector_csv)
            fila = indice_feeder #al index deseado restarle 2 por conflicto con index
            columna_fecha = indice_fecha #igual a 3 por el 0 del index
            columna_color = 3
            columna_codigo = 2
            #Obtener valor de interseccion con columna fecha
            if fila < len(csv_data) and columna_fecha < len(csv_data[0]):
                #obtener valor de interseccion
                interseccion_fecha = csv_data[fila][columna_fecha]
            else:
                print("No se encontro valor interseccion")
            #Obtener valor de interseccion con columna color
            if fila < len(csv_data) and columna_color < len(csv_data[0]):
                #obtener valor de interseccion
                interseccion_color = csv_data[fila][columna_color]
            else:
                print("No se encontro valor interseccion")
            #Obtener valor de interseccion con columna codigo
            if fila < len(csv_data) and columna_codigo < len(csv_data[0]):
                #obtener valor de interseccion
                interseccion_codigo = csv_data[fila][columna_codigo]
            else:
                print("No se encontro valor interseccion")
            return interseccion_fecha, interseccion_color, interseccion_codigo
        except:
            return 0, 0, 0
        
def search_fecha(FECHA:str):
    '''
    search_id(ID_FEEDER:int)
        toma como parametro el id del feeder,mismo que sera proporcionado por la app feeder status
        mediante el escaneo de los feeders.
        retorna: un dataframe con todos los datos del feeder ( ID_feeder, Feeder )  
      
        extra:
            -Index ID_feeder: index de ID_feeder(posicion del dato en csv)
            -Index fecha: index de fecha (posicion del dato en csv)s
    '''
    #fecha en columna
    with open(r'H:\Ingenieria\Ensamble PCB\Documentacion ISO-9001\mantto seq.csv') as mantto_seq:#ruta oficial de documento
        #Crear un lector
        lectura_mantto = csv.reader(mantto_seq)
        data_mantto = pd.read_csv(r'H:\Ingenieria\Ensamble PCB\Documentacion ISO-9001\mantto seq.csv',encoding = "ISO-8859-1",usecols=['DIA','COLOR'],low_memory=False)#ruta oficial de documento
        df_mantto = pd.DataFrame(data_mantto)
        index_fecha = df_mantto.loc[df_mantto['DIA'] == FECHA].to_string(index = False)
        index_fecha = index_fecha.split()
        dia = index_fecha[2]
        color = index_fecha[3]
        return dia, color
    
def rellenar_rango_hasta_P(fila, columna_inicio):
    '''
    rellenar_rango_hasta_P(fila, columna_inicio):
        rellena con 'OK' un rango de columnas hasta que encuentra una P
      
        parametros:
            -fila: es el index del feeder
            -columna_inicio: es el index de la columna de la fecha actual
          
        condiciones:
            -Verificar si la fila existe en el rango de filas del archivo CSV
            -Verificar si la columna de inicio está dentro del rango de la fila
            -Verificar si la columna de fin está dentro del rango de la fila
            -Rellena un rango de columnas con OK apartir de la interseccion de la fecha y el id del feeder
            -Al iniciar a rellenar si detecta varias P de manera consecutiva, las cuenta y si son iguales o menores a 15, las sobreescribe y se detiene en la próxima P
    '''
    try:
        # Abrir el archivo CSV en modo lectura
        with open(r'H:\Ingenieria\Ensamble PCB\Documentacion ISO-9001\plan feeders SEM.csv', 'r') as archivo_csv:
            # Leer el archivo CSV
            filas = list(csv.reader(archivo_csv))

        # Obtener la fila deseada
        fila_deseada = filas[fila - 1]

        # Declarar la columna final
        columna_fin = len(fila_deseada)

        # Contar celdas consecutivas con valor "P" hasta un máximo de 15
        p_consecutivas = 0
        for i in range(columna_inicio - 1, columna_fin):
            if fila_deseada[i] == 'P':
                p_consecutivas += 1
                if p_consecutivas <= 15:
                    fila_deseada[i] = "OK"
            else:
                break

        # Rellenar celdas consecutivas con valor "OK" hasta la próxima celda con valor "P"
        for i in range(columna_inicio - 1, columna_fin):
            # Verificar si el valor de la celda es igual a 'P'
            if fila_deseada[i] == 'P':
                break  # Si encuentra 'P', se detiene el bucle

            # Rellenar la celda con el valor deseado
            fila_deseada[i] = "OK"

        # Guardar los cambios en el archivo CSV
        try:
            with open(r'H:\Ingenieria\Ensamble PCB\Documentacion ISO-9001\plan feeders SEM.csv', 'w', newline='') as archivo_csv:
                escritor = csv.writer(archivo_csv)
                escritor.writerows(filas)
        except IOError:
            sg.popup_error("Error al abrir el archivo CSV en modo escritura.")
            raise IOError("El Archivo CSV se encuentra abierto!")
    except Exception as e:
        raise e

#Quitar comentarios para testear
#print("resultado search_id:\n",search_id(105372618)) #probar funcionamiento de funcion
#descripcion = ""
#for i in search_id(105372953).split()[3:]:
#    descripcion += i + " "

#print("\nresultado descripcion:",descripcion)
#print("\nresultado cell_value:",cell_value("104575035")) #probar funcionamiento de funcion
#print("resultado search_fecha",search_fecha(fecha_formateada)[1]) #probando funcion para buscar fecha
###rellenar_rango_hasta_P(5,182,300)
###rellenar_rango_hasta_P( 5, 8)
#print(index_ff(104575035)[0], index_ff(104575035)[1])
#rellenar_rango_hasta_P(index_ff(104575032)[0], index_ff(104575032)[1])


"""
snapshot2 = tracemalloc.take_snapshot()
differences = snapshot2.compare_to(snapshot1,'filename')

for stat in differences[:10]:
    print(stat)
    
#obtener la traza de un objeto especifico
#remplana el objeto que deseas rastrear
your_object = ...
object_trace = tracemalloc.get_object_traceback(your_object)
print(object_trace)
"""
