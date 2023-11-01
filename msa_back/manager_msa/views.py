from django.shortcuts import render

# Create your views here.
def welcome_view(request):
    return render(request, template_name='welcome.html', status=200)

def login(request):
    return render(request, template_name='Auth/login.html', status=200)

def register(request):
    return render(request, template_name='Auth/registro.html', status=200)