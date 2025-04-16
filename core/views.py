from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def app(request):
    return render(request, "app.html")

def registro(request):
    return render(request, "registro.html")

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form"  :form})
