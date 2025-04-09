import json
import pandas as pd
import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .tools import crear_plantilla,search_feeder,validar
from collections import defaultdict
from .forms import FeederParaRepararForm,PartesFeederForm,PartesRequeridasForm
from .models import FeederRegistro,Cronometro,PartesFeeder,FeederParaReparar,PartesRequeridas
import datetime
from datetime import date,datetime
from django.utils import timezone




def consultar(request):
    #remplaza funcion check_status() --> app mantto_feeder
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        feeder_id = request.GET.get('feeder_id')

        if not feeder_id:
            return JsonResponse({"error": "ID no proporcionado."}, status=400)

        try:
            feeder_id = int(feeder_id)  # Convertimos a entero
            #print(feeder_id,type(feeder_id))
            
            #obteniene un diccionario de search_id
            resultado = search_feeder.search_id(feeder_id)
            #print(resultado)
            
            #obteniene una lista de cell_value para determinar estado(OK,P,"")
            valor_celda = search_feeder.cell_value(feeder_id)[0]
            #print("valor_celda:",valor_celda)
            
            #codigo de feeder
            codigo = search_feeder.cell_value(feeder_id)[2]
            #print("codigo:",codigo)
            
            #color de feeder
            color_feeder = search_feeder.cell_value(feeder_id)[1]
            #print("color_feeder:",color_feeder)
            
            #color de semana
            fecha_actual = datetime.now()
            fecha_formateada = fecha_actual.strftime(f'{fecha_actual.month}/{fecha_actual.day}/{fecha_actual.year}')
            #print("fecha_formateada:",fecha_formateada)
            
            color_semana = search_feeder.search_fecha(fecha_formateada)[1]
            #print("color_semana:",color_semana)
            #diccionario para transmitir resultados en json
            resultados_dict = {
                'id_feeder': resultado['id_feeder'],
                'feeder': resultado['feeder'],
                'color_feeder': color_feeder,
                'codigo_feeder': codigo,
                'color_semana': color_semana,
                'valor_celda': valor_celda
            }
            #print(resultados_dict)
            if not resultado:
                return JsonResponse({"error": "Feeder no encontrado."}, status=404)

            return JsonResponse(resultados_dict)

        except ValueError:
            return JsonResponse({"error": "ID inválido. Debe ser un número."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno: {str(e)}"}, status=500)

    return render(request, 'registro.html')

def iniciar_cronometro(request):
    if request.method == 'POST':
        try:
            # Extraer datos del JSON
            data = json.loads(request.body)
            print("Datos recibidos en iniciar_cronometro:", data)

            # Obtener feeder_id
            feeder_id = data.get('id-feeder')
            print("Feeder ID:", feeder_id)
            # Obtener el tiempo de inicio, asegurándonos de que sea un timestamp válido
            tiempo_inicio = data.get('tiempo_inicio')
            if tiempo_inicio:
                # Convertir timestamp a datetime aware
                tiempo_inicio = datetime.fromtimestamp(tiempo_inicio)
                tiempo_inicio = timezone.make_aware(tiempo_inicio)  # Hace la fecha aware con la zona horaria actual
                print("Tiempo inicio:", tiempo_inicio)
            else:
                return JsonResponse({'success': False, 'message': 'tiempo_inicio es requerido.'}, status=400)
            
            # Crear el objeto Cronometro con tiempo_fin como None
            cronometro = Cronometro(tiempo_inicio=tiempo_inicio, tiempo_fin=None ,feeder_id=feeder_id)
            cronometro.save()  # Guarda en la base de datos
            print("Cronómetro guardado:", cronometro)
            
            return JsonResponse({'success': True, 'message': 'Cronómetro guardado correctamente.', 'id': cronometro.id})
        except Exception as e:
            print("Error al guardar cronómetro:", str(e))
            return JsonResponse({'success': False, 'message': f'Error al guardar cronómetro: {str(e)}'}, status=400)
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

def detener_cronometro(request, cronometro_id):
    """Detiene el cronómetro y devuelve el tiempo de captura."""
    if request.method == 'POST':
        try:
            cronometro = Cronometro.objects.get(id=cronometro_id)
            if cronometro.tiempo_fin is not None:
                return JsonResponse({'success': False, 'error': 'El cronómetro ya fue detenido'}, status=400)
            
            cronometro.tiempo_fin = timezone.now()
            print("Tiempo fin:", cronometro.tiempo_fin)
            cronometro.save()

            tiempo_captura = cronometro.calcular_tiempo_captura()
            return JsonResponse({'success': True, 'tiempo_captura': tiempo_captura})
        except Cronometro.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cronómetro no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error al detener el cronómetro: {str(e)}'}, status=500)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

def tiempo_a_segundos(tiempo_str):
    h, m, s = map(int, tiempo_str.split(':'))
    return h * 3600 + m * 60 + s

def registro(request):
    if request.method == 'POST':
        try:
            # Cargar los datos JSON del cuerpo de la solicitud
            data = json.loads(request.body)
            print("Datos del JSON:", data)
            
            feeder_id = int(data.get('id-feeder'))
            feeder_name = data.get('feeder')
            feeder_code = data.get('codigo-feeder')
            color_feeder = data.get('color-feeder')
            color_semana = data.get('color-semana')
            tecnico = data.get('tecnico')
            # convertir el tiempo de captura a segundos
            tiempo_captura = tiempo_a_segundos(data.get('tiempo_captura'))
            observaciones = data.get('observaciones')
            tiempo = data.get('tiempo_captura')
            
            # fecha para plantilla
            fecha_actual = datetime.now()
            dia = fecha_actual.day
            mes = fecha_actual.strftime('%b')
            año = fecha_actual.year
            fecha_mantenimiento_plantilla = "{}{}{}".format(dia,mes,año)
            
            # Fecha de mantenimiento (formato DD/MM/YYYY)
            try:
                fecha_mantenimiento = datetime.now().strftime('%Y-%m-%d')
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Fecha de mantenimiento con formato incorrecto.'}, status=400)
            
            # Tipo de feeder será igual a la key con valor "OK"
            tipo_feeder = ""
            for key, value in data.items():
                if value == "OK":
                    tipo_feeder = key
            
            # Procesar los datos del feeder
            try:
                index = search_feeder.index_ff(feeder_id)
                search_feeder.rellenar_rango_hasta_P(index[0], index[1])
            except (IOError, Exception) as e:
                return JsonResponse({'success': False, 'message': f'Error al procesar los datos: {e}'}, status=400)
            
            # Validar el número de técnico
            try:
                tecnico_valido = validar.user(tecnico)
                if tecnico_valido is None:
                    return JsonResponse({'success': False, 'message': 'El No.Empleado no es válido.'}, status=400)
            except (IOError, Exception) as e:
                return JsonResponse({'success': False, 'message': f'Error al validar el No.Empleado: {e}'}, status=400)
            
            # Crear la plantilla
            try:
                crear_plantilla.create_template(tecnico_valido, feeder_id, tipo_feeder, fecha_mantenimiento_plantilla, color_feeder, observaciones)
            except (IOError, Exception) as e:
                return JsonResponse({'success': False, 'message': f'Error al procesar los datos: {e}'}, status=400)
            
            # Guardar en la base de datos
            feeder_registro = FeederRegistro(
                feeder_id=feeder_id,
                feeder_name=feeder_name,
                feeder_code=feeder_code,
                color_feeder=color_feeder,
                color_semana=color_semana,
                tecnico=tecnico,
                tiempo_captura=tiempo_captura,
                observaciones=observaciones,
                tiempo=tiempo,
                CP=data.get('CP', 'NG'),
                QP=data.get('QP', 'NG'),
                HOVER=data.get('HOOVER', 'NG'),
                BFC=data.get('BFC', 'NG'),
                fecha_mantenimiento=fecha_mantenimiento
            )
            feeder_registro.save()
            print("Datos guardados en la base de datos.")
            return JsonResponse({'success': True, 'message': 'Datos procesados y guardados correctamente.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Error al procesar los datos: JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error inesperado: {e}'}, status=500)

    # Manejo de solicitudes GET
    print("GET request to registro view")
    return render(request, 'registro.html')

def home(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        data = pd.read_csv(
            r"H:\Ingenieria\Ensamble PCB\Documentacion ISO-9001\mantto seq 2025.csv",
            encoding="ISO-8859-1",
            usecols=["DIA", "COLOR"],
            engine="python"
        )
        # Reemplazar todos los NaN en todas las columnas
        data = data.fillna("GHOSTWHITE")
        # Convertir todas las columnas a cadenas para evitar problemas con objetos no serializables
        data["DIA"] = data["DIA"].astype(str)
        data["COLOR"] = data["COLOR"].astype(str)
        # Convertir a lista de diccionarios
        data_dict = data.to_dict(orient="records")
        #print(data_dict)  # Validar JSON generado
        return JsonResponse({"color_semana": data_dict})
    return render(request, "home.html")


def analisis(request):
    # Extraer todos los registros de la base de datos
    consulta = FeederRegistro.objects.all()
    
    # Obtener la semana actual del año
    fecha_actual = date.today()
    semana_actual = fecha_actual.isocalendar()[1]
    
    # Meta del Feeder
    meta_feeder = 80
    meta_usuario = 200
    
    # Crear el diccionario para guardar tipo_feeder y su respectivo tiempo
    feeder_tipo_tiempo = {
        "CP": [],
        "QP": [],
        "HOVER": [],
        "BFC": [],
    }

    feeder_tipo_tiempo_semana_actual = {
        "CP": [],
        "QP": [],
        "HOVER": [],
        "BFC": [],
    }

    # Llenar el diccionario con los datos de feeder_id, tipo_feeder y tiempo_captura
    for resultado in consulta:
        tipo = ""  # Valor por defecto si no se encuentra un tipo válido
        fecha_mantenimiento = resultado.fecha_mantenimiento
        semana_mantenimiento = fecha_mantenimiento.isocalendar()[1]  # Semana de la fecha de mantenimiento
        
        # Identificar el tipo de feeder basado en los valores de los campos
        if resultado.CP == "OK":
            tipo = "CP"
        elif resultado.QP == "OK":
            tipo = "QP"
        elif resultado.HOVER == "OK":
            tipo = "HOVER"
        elif resultado.BFC == "OK":
            tipo = "BFC"

        # Añadir al diccionario el (feeder_id, tiempo_captura) solo si la semana de mantenimiento es la actual
        if semana_mantenimiento == semana_actual:
            feeder_tipo_tiempo[tipo].append((resultado.feeder_id, resultado.tiempo_captura))
            feeder_tipo_tiempo_semana_actual[tipo].append((resultado.feeder_id, resultado.tiempo_captura, resultado.fecha_mantenimiento))
    
    # Sumatoria de tiempo para los tipos de feeder en la semana actual
    sumatoria_tipo_semana_actual = {}
    for tipo in ["CP", "QP", "HOVER", "BFC"]:
        # Calcular la suma de tiempos para cada tipo de feeder solo para la semana actual
        sumatoria_tipo_semana_actual[tipo] = sum(tiempo_captura for _, tiempo_captura, _ in feeder_tipo_tiempo_semana_actual[tipo])
    
    # Imprimir la sumatoria de cada tipo de feeder para la semana actual
    #print(sumatoria_tipo_semana_actual)

    # Obtener el técnico desde la solicitud GET (si existe)
    tecnico = request.GET.get('tecnico', "00000")
    
    # Filtrar por técnico si se especifica
    if tecnico:
        consulta = FeederRegistro.objects.filter(tecnico=tecnico)
        if consulta.exists():
            #print(f"Registros para el técnico {tecnico}:") # para depuración
            for registro in consulta:
                pass
                #print(f"Feeder ID: {registro.feeder_id}, Técnico: {registro.tecnico}") # para depuración
        else:
            #print(f"No se encontraron registros para el técnico: {tecnico}") # para depuración
            consulta = FeederRegistro.objects.all()  # Vuelve a obtener todos los registros
    else:
        #print("Mostrando todos los registros de feeders:")
        for registro in consulta:
            pass
            #print(f"Feeder ID: {registro.feeder_id}, Técnico: {registro.tecnico}")

    # Contar los feeders por semana del año
    feeders_por_semana = defaultdict(int)
    for registro in consulta:
        semana = registro.fecha_mantenimiento.isocalendar()[1]  # Obtener la semana
        feeders_por_semana[semana] += 1
    
    # Contar los feeders por técnico
    feeders_por_tecnico = defaultdict(int)
    for registro in consulta:
        feeders_por_tecnico[registro.tecnico] += 1
    
    # Prepara los datos para los gráficos
    semanas = list(feeders_por_semana.keys())
    feeders_semana = [feeders_por_semana.get(semana, 0) for semana in semanas]
    tecnicos = list(feeders_por_tecnico.keys())
    feeders_tecnico = [feeders_por_tecnico.get(tecnico, 0) for tecnico in tecnicos]

    # Contar los feeders por semana y por técnico
    feeders_por_semana_tecnico = defaultdict(lambda: defaultdict(int))  # Semana -> Técnico -> Contador de feeders
    for registro in consulta:
        semana = registro.fecha_mantenimiento.isocalendar()[1]  # Obtener la semana
        feeders_por_semana_tecnico[semana][registro.tecnico] += 1

    # Preparar los datos para las semanas (categorías del gráfico)
    #semanas = sorted(feeders_por_semana_tecnico.keys())  # semanas ordenadas

    # Obtener los tecnicos
    tecnicos = list(set(tecnico for semana in feeders_por_semana_tecnico.values() for tecnico in semana.keys())) 
    tecnicos.sort()  # Ordenar los tecnicos alfabéticamente

    # Preparar los datos para el grafico apilado (por cada tecnico, por cada semana)
    feeders_por_tecnico_semanal = {tecnico: [] for tecnico in tecnicos}
    for semana in semanas:
        for tecnico in tecnicos:
            feeders_por_tecnico_semanal[tecnico].append(feeders_por_semana_tecnico[semana].get(tecnico, 0))

    # Obtener los tecnicos unicos y reemplazar IDs con nombres
    tecnicos_nombres = {tecnico: validar.user(tecnico) or tecnico for tecnico in tecnicos}

    # Preparar los datos para el gráfico apilado con nombres en lugar de IDs
    feeders_por_tecnico_semanal_nombres = {
        tecnicos_nombres[tecnico]: data
        for tecnico, data in feeders_por_tecnico_semanal.items()
    }
    
    # Pasar los datos a la plantilla
    context = {
        'feeders_por_semana': feeders_semana,
        'semanas': semanas,
        'feeders_por_tecnico': feeders_tecnico,
        'feeders_por_tecnico_semanal': feeders_por_tecnico_semanal_nombres,
        'tecnicos': list(tecnicos_nombres.values()),
        'meta_feeder': meta_feeder, 
        'meta_usuario': meta_usuario, 
        #'tiempos': tiempos,
        #'tipo_feeder': tipo_feeder,  
        'feeder_tipo_tiempo': feeder_tipo_tiempo,
        'sumatoria_tipo_semana_actual': sumatoria_tipo_semana_actual,
        'semana_actual': semana_actual
    }

    return render(request, 'analisis.html', context)

def reparaciones(request):
    return render(request, 'reparaciones.html')

def agregar_parte(request):
    #http://localhost:8000/registro/?numero_parte=12345&nombre=Resistencia&costo=150.50&cantidad=100
    try:    
        if request.method == 'POST':
            data = json.loads(request.body)
            print("Datos recibidos POST:", data)
            #{'partNumber','partName','partCost','partStock','partStatus','partDate'}
            # crear el objeto PartesFeeder
            parte = PartesFeeder(
                numero_parte= data.get('partNumber'),
                nombre=data.get('partName'),
                costo=data.get('partCost'),
                stock_minimo=data.get('partStock'),
                cantidad=data.get('partQty'),
                estado=data.get('partStatus'),
                fecha_registro=data.get('partDate')
            )
            parte.save()
            print("Parte guardada:", parte)
            return JsonResponse({'success': True, 'message': 'Datos procesados correctamente.'})
        else:
            data = request.GET
            print("Datos recibidos GET:", data)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Error al procesar los datos: JSON inválido.'}, status=400)
    
def inventario(request):
    partes = PartesFeeder.objects.all()  # Obtener todos los registros de PartesFeeder
    reparaciones = FeederParaReparar.objects.all()  # Obtener todas las reparaciones
    partes_requeridas = PartesRequeridas.objects.all()  # Obtener todas las partes requeridas
    for parte in partes_requeridas:
        parte.costo = parte.costo * parte.cantidad
    #print("Partes Requeridas:", partes_requeridas.count())
    
    # for parte in partes_requeridas:
    #     print(f"Feeder ID:{parte.feeder_id.feeder_id} | {parte.cantidad}" )
    #     if parte.feeder_id.feeder_id == 1045623:
    #         parte.cantidad = 60
    #         parte.save()
    #         print("Parte actualizada")
    
    return render(request, 'inventario.html', {
        'partes': partes,
        'reparaciones': reparaciones,
        'partes_requeridas': partes_requeridas,
    })

def registrar_reparacion_form(request):
    if request.method == 'POST':
        form = FeederParaRepararForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el registro de la reparación en la base de datos
            return redirect('inventario')  # Redirige a la vista de inventario
    else:
        form = FeederParaRepararForm()
    
    return render(request, 'forms/registrar_reparacion.html', {'form': form})

def agregar_parte_form(request):
    if request.method == "POST":
        form = PartesFeederForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = PartesFeederForm()
    return render(request, 'forms/agregar_parte.html', {'form': form})
  
def agregar_parte_requerida_form(request):
    if request.method == "POST":
        form = PartesRequeridasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = PartesRequeridasForm()
    return render(request, 'forms/agregar_parte_requerida.html', {'form': form})

  
def reportes(request):
    return render(request, 'reportes.html')

def about(request):
    return render(request, 'about.html')
