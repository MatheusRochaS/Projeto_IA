from django.shortcuts import render, redirect

# Create your views here.
def welcome_view(request):
    # return render(request, template_name='welcome.html', status=200)
    return redirect('login')

def login(request):
    return render(request, template_name='Auth/login.html', status=200)

def register(request):
    return render(request, template_name='Auth/registro.html', status=200)

def main(request):
    return render(request, template_name='Videos/main.html', status=200)

def catalogo_geral(request):
    return render(request, template_name='Videos/catalogo.html', status=200)

def lista_geral(request):
    return render(request, template_name='Lista/lista.html', status=200)

def infos(request, video_id):
    return render(request, template_name='Videos/infos.html', status=200)