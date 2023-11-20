from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from .request import request as api
from .models import Movie

# Create your views here.
def welcome_view(request):
    # return render(request, template_name='welcome.html', status=200)
    return redirect('login')

def login(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            auth_login(request, usuario)
            return redirect('main')
        else:
            form_login = AuthenticationForm
    else:
        form_login = AuthenticationForm
    return render(request, template_name='Auth/login.html', context={'form_login': form_login})

def logout(request):
    auth_logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == "POST":
        form_usuario = CustomUserForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('main')
    else:
        form_usuario = CustomUserForm()
    return render(request, template_name='Auth/registro.html', context={'form_usuario': form_usuario})

@login_required(login_url='/login')
def main(request):
    resp_api = api.get(url="https://api.themoviedb.org/3/trending/all/day?language=pt-Br")
    movies = api.get(url="https://api.themoviedb.org/3/movie/popular?language=pt-BR&page=1")
    series = api.get(url="https://api.themoviedb.org/3/tv/popular?language=pt-BR&page=1")
    return render(request, template_name='Videos/main.html', status=200, context={'videos':resp_api, 'movies': movies, 'series': series})

@login_required(login_url='/login')
def catalogo_geral(request):
    return render(request, template_name='Videos/catalogo.html', status=200)

@login_required(login_url='/login')
def lista_geral(request, user_id):
    list_movie = Movie.objects.all().filter(user=user_id)

    lista_filmes = []
    for l in list_movie:
        movie = api.get(url=f"https://api.themoviedb.org/3/movie/{l.movie}?language=pt-BR")
        # movie['release_date'] = movie.release_date.strftime("%d/%m/%y")
        movie['status_watch'] = l.watch
        lista_filmes.append(movie)
    
    return render(request, template_name='Lista/lista.html', context={'list': lista_filmes})

@login_required(login_url='/login')
def infos(request, video_id):
    movie_detail = api.get(url=f"https://api.themoviedb.org/3/movie/{video_id}?language=pt-BR")
    message = {
            'msg': '',
            'type': ''
        }
    if request.method == "POST":
        movie = Movie(user_id= request.user.pk ,movie=video_id, watch=0)
        movie.save()
        
        message = {
            'msg': 'Filme adicionado com sucesso',
            'type': 'success'
        }
        
    return render(request, template_name='Videos/infos.html', context={'details': movie_detail, 'alert': message})