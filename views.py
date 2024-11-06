from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
import json
from .tools import crear_plantilla,search_feeder,progress,loggin,validar
from collections import defaultdict
from .models import FeederRegistro
import datetime
from datetime import date,datetime

def consultar(request):
    #remplaza funcion check_status() --> app mantto_feeder
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        feeder_id = request.GET.get('feeder_id')

        if not feeder_id:
            return JsonResponse({"error": "ID no proporcionado."}, status=400)

        try:
            feeder_id = int(feeder_id)  # Convertimos a entero
            #obteniene un diccionario de search_id
            resultado = search_feeder.search_id(feeder_id)
            #obteniene una lista de cell_value para determinar estado(OK,P,"")
            valor_celda = search_feeder.cell_value(feeder_id)[0]
            #codigo de feeder
            codigo = search_feeder.cell_value(feeder_id)[2]
            #color de feeder
            color_feeder = search_feeder.cell_value(feeder_id)[1]
            #color de semana
            fecha_actual = datetime.now()
            fecha_formateada = fecha_actual.strftime(f'{fecha_actual.month}/{fecha_actual.day}/{fecha_actual.year}')
            color_semana = search_feeder.search_fecha(fecha_formateada)[1]
            #diccionario para transmitir resultados en json
            resultados_dict = {
                'id_feeder': resultado['id_feeder'],
                'feeder': resultado['feeder'],
                'color_feeder': color_feeder,
                'codigo_feeder': codigo,
                'color_semana': color_semana,
                'valor_celda': valor_celda
            }
            if not resultado:
                return JsonResponse({"error": "Feeder no encontrado."}, status=404)

            return JsonResponse(resultados_dict)

        except ValueError:
            return JsonResponse({"error": "ID inválido. Debe ser un número."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno: {str(e)}"}, status=500)

    return render(request, 'registro.html')

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
            tiempo_captura = int(data.get('tiempo_captura'))
            observaciones = data.get('observaciones')
            tiempo = data.get('time')
            
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
                crear_plantilla.create_template(tecnico_valido, feeder_id, tipo_feeder, fecha_mantenimiento_plantilla, color_semana, observaciones)
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
                HOVER=data.get('HOVER', 'NG'),
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
    return render(request, 'home.html')

def analisis(request):
    # Extraer todos los registros de la base de datos
    consulta = FeederRegistro.objects.all()
    
    # Meta del Feeder (30 y 10 por defecto)
    meta_feeder = 30
    meta_usuario = 10
    print("Registros totales:", total := len(consulta))
    
    # Retornar el tipo de feeder de cada feeder
    tipo_feeder = []
    feeder_ids = []  # Para guardar los IDs de feeders
    for registro in consulta:
        if registro.CP == "OK":
            tipo_feeder.append("CP")
        elif registro.QP == "OK":
            tipo_feeder.append("QP")
        elif registro.HOVER == "OK":
            tipo_feeder.append("HOVER")
        elif registro.BFC == "OK":
            tipo_feeder.append("BFC")
        else:
            tipo_feeder.append("Desconocido")  # Si no es "OK", se puede considerar como un tipo desconocido

        feeder_ids.append(registro.feeder_id)  # Guardar el ID del feeder
    
    # Imprimir los tipos de feeder para depuración
    print("Tipos de feeder:", tipo_feeder)
    
    # Lista de tiempos de captura
    tiempos = []
    for registro in consulta:
        tiempos.append(registro.tiempo_captura)  # Guardar el tiempo de captura
    
    # Imprimir los tiempos de captura junto con el ID del feeder
    print("Tiempos de captura por feeder:")
    for feeder_id, tiempo, tipo in zip(feeder_ids, tiempos, tipo_feeder):
        print(f"Feeder ID {feeder_id}: {tiempo} segundos, Tipo: {tipo}")
    
    # Obtener el técnico desde la solicitud GET (si existe)
    tecnico = request.GET.get('tecnico', "00000")
    
    # Filtrar por técnico si se especifica
    if tecnico:
        consulta = FeederRegistro.objects.filter(tecnico=tecnico)
        if consulta.exists():
            print(f"Registros para el técnico {tecnico}:")
            for registro in consulta:
                print(f"Feeder ID: {registro.feeder_id}, Técnico: {registro.tecnico}")
        else:
            print(f"No se encontraron registros para el técnico: {tecnico}")
            consulta = FeederRegistro.objects.all()  # Vuelve a obtener todos los registros
    else:
        print("Mostrando todos los registros de feeders:")
        for registro in consulta:
            print(f"Feeder ID: {registro.feeder_id}, Técnico: {registro.tecnico}")
    
    # Obtener la semana actual del año
    fecha_actual = date.today()
    semana_actual = fecha_actual.isocalendar()[1]
    print("Semana actual:", semana_actual)

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

    # Pasar los datos a la plantilla
    context = {
        'feeders_por_semana': feeders_semana,
        'semanas': semanas,
        'feeders_por_tecnico': feeders_tecnico,
        'tecnicos': tecnicos,
        'meta_feeder': meta_feeder,
        'meta_usuario': meta_usuario,
        'tiempos': tiempos,
        'tipo_feeder': tipo_feeder,  # Agregar la lista de tipos de feeders a la plantilla
    }

    return render(request, 'analisis.html', context)

def reparaciones(request):
    return render(request, 'reparaciones.html')

def reportes(request):
    return render(request, 'reportes.html')

def about(request):
    return render(request, 'about.html')
