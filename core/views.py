from django.shortcuts import render

# Create your views here.

def app(request):
    return render(request, "app.html")

def registro(request):
    return render(request, "registro.html")
