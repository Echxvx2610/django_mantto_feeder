from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
import json
from .tools import crear_plantilla,search_feeder,progress,loggin,validar
from datetime import datetime


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
    # remplaza get_data() --> con json de registro
    if request.method == 'POST':
        try:
            # Cargar los datos JSON del cuerpo de la solicitud
            data = json.loads(request.body)
            print(data)  # Para verificar que los datos están llegando
            # Procesamiento de los datos
            feeder_value = data.get('id-feeder')
            print(int(feeder_value))  # Para verificar el tipo de dato de la variable feeder_value)
           
           
            return JsonResponse({'success': True, 'message': 'Datos procesados correctamente.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Error al procesar los datos.'}, status=400)

    # Para las solicitudes GET, puedes verificar si se accede a la vista correcta
    print("GET request to registro view")
    return render(request, 'registro.html')

def home(request):
    return render(request, 'home.html')

def analisis(request):
    return render(request, 'analisis.html')

def reparaciones(request):
    return render(request, 'reparaciones.html')

def reportes(request):
    return render(request, 'reportes.html')

def about(request):
    return render(request, 'about.html')
