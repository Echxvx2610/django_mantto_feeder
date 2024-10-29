from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'home.html')

def analisis(request):
    return render(request, 'analisis.html')

def registro(request):
    return render(request, 'registro.html')

def reparaciones(request):
    return render(request, 'reparaciones.html')

def reportes(request):
    return render(request, 'reportes.html')

def about(request):
    return render(request, 'about.html')
