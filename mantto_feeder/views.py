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
    if request.method == 'POST':
        try:
            # Cargar los datos JSON del cuerpo de la solicitud
            data = json.loads(request.body)
            feeder_id = int(data.get('id-feeder'))

            # fecha para plantilla
            fecha_actual = datetime.now()
            dia = fecha_actual.day
            mes = fecha_actual.strftime('%b')
            año = fecha_actual.year
            fecha_mantenimiento = "{}{}{}".format(dia,mes,año)
            tipo_feeder = ""
            # tipo de feeder sera igual a la key con valor OK
            for key, value in data.items():
                if value == "OK":
                    tipo_feeder = key
            # Procesar los datos del feeder
            try:
                index = search_feeder.index_ff(feeder_id)
                search_feeder.rellenar_rango_hasta_P(index[0], index[1])
                #print("Validado función index_ff y rellenar_rango_hasta_P")
            except (IOError, Exception) as e:
                return JsonResponse({'success': False, 'message': f'Error al procesar los datos: {e}'}, status=400)
            
            # Antes de generar el reporte, validar el número de técnico
            try:
                tecnico_valido = validar.user(data.get('tecnico'))
                
                if tecnico_valido is None:
                    return JsonResponse({'success': False, 'message': 'El No.Empleado no es válido.'}, status=400)

                print("Validado función validar_tecnico")
            except (IOError, Exception) as e:
                return JsonResponse({'success': False, 'message': f'Error al validar el No.Empleado: {e}'}, status=400)

            # Procesar los datos para generar la plantilla (reporte)
            try:
                crear_plantilla.create_template(tecnico_valido, feeder_id, tipo_feeder, fecha_mantenimiento, data.get('color-semana'), data.get('observaciones'))
            except (IOError, Exception) as e:
                return JsonResponse({'success': False, 'message': f'Error al procesar los datos: {e}'}, status=400)
            
            return JsonResponse({'success': True, 'message': 'Datos procesados correctamente.'})

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
    return render(request, 'analisis.html')

def reparaciones(request):
    return render(request, 'reparaciones.html')

def reportes(request):
    return render(request, 'reportes.html')

def about(request):
    return render(request, 'about.html')
