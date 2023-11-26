from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from .request import request as api
from .models import Movie
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

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
    movies_now = api.get(url="https://api.themoviedb.org/3/movie/now_playing?language=pt-BR&page=1")

    context = {
        'videos':resp_api, 
        'movies': movies, 
        'series': series,
        'movies_now': movies_now
    }

    return render(request, template_name='Videos/main.html', status=200, context=context)

@login_required(login_url='/login')
def catalogo_geral(request):
    return render(request, template_name='Videos/catalogo.html', status=200)

@login_required(login_url='/login')
def lista_geral(request, user_id):
    list_movie = Movie.objects.all().filter(user=user_id)
    page_num = request.GET.get('page', 1)

    paginator = Paginator(list_movie, 10)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    lista_filmes = []
    for l in list_movie:
        movie = api.get(url=f"https://api.themoviedb.org/3/movie/{l.movie}?language=pt-BR")
        # movie['release_date'] = movie.release_date.strftime("%d/%m/%y")
        movie['status_watch'] = l.watch
        movie['id_bd'] = l.id
        movie['rating_personal'] = l.rating
        lista_filmes.append(movie)

        context = {
            'list': lista_filmes,
            'page_obj': page_obj,
        }
    
    return render(request, template_name='Lista/lista.html', context=context)

@login_required(login_url='/login')
def infos(request, video_id, type):

    if type == 'movie':
        video_detail = api.get(url=f"https://api.themoviedb.org/3/movie/{video_id}?language=pt-BR")
        video_detail['type_video'] = 'movie'
        video_credits = api.get(url=f"https://api.themoviedb.org/3/movie/{video_id}/credits?language=pt-BR")
        video_images = api.get(url=f"https://api.themoviedb.org/3/movie/{video_id}/images")
        
    else:
        video_detail = api.get(url=f"https://api.themoviedb.org/3/tv/{video_id}?language=pt-BR")
        video_detail['type_video'] = 'serie'
        video_credits = api.get(url=f"https://api.themoviedb.org/3/tv/{video_id}/credits?language=pt-BR")
        video_images = api.get(url=f"https://api.themoviedb.org/3/tv/{video_id}/images?language=pt-BR")

    message = {
                'msg': '',
                'type': ''
            }
    movie = Movie(user_id=request.user.pk ,movie=video_id, watch=0)
    if request.method == "POST":
        movie.save()
        
        message = {
            'msg': f"Filme {video_detail['title']} adicionado com sucesso na sua lista de filmes!",
            'type': 'success'
        }
    
    context = {
        'details': video_detail,
        'alert': message,
        'credits': video_credits,
        'images': video_images,
    }
        
    return render(request, template_name='Videos/infos.html', context=context)

@login_required(login_url='/login')
def rating_movie(request, rating, video_id):
    # movie = Movie.objects.get(id=video_id)
    movie_detail = api.get(url=f"https://api.themoviedb.org/3/movie/{video_id}?language=pt-BR")
    movie = Movie.objects.filter(movie=video_id).update(rating=rating)
    # message = {
    #     'msg': f'Filme {movie_detail[0].title} deletado com sucesso!',
    #     'type': 'success'
    # }

    # context = {'alert': message}
    messages.success(request, f"Filme {movie_detail['title']} avaliado com sucesso!")
    return HttpResponseRedirect(reverse('lista', kwargs={'user_id':request.user.id}))

@login_required(login_url='/login')
def delete_movie(request, video_id):
    movie = Movie.objects.get(id=video_id)
    movie_detail = api.get(url=f"https://api.themoviedb.org/3/movie/{movie.movie}?language=pt-BR")
    movie.delete()
    # message = {
    #     'msg': f'Filme {movie_detail[0].title} deletado com sucesso!',
    #     'type': 'success'
    # }

    # context = {'alert': message}
    messages.success(request, f"Filme {movie_detail['title']} deletado com sucesso!")
    return HttpResponseRedirect(reverse('lista', kwargs={'user_id':request.user.id}))

@login_required(login_url='/login')
def search(request):
    resp_api = api.get(url="https://api.themoviedb.org/3/trending/all/week?language=pt-Br")

    search_videos = request.GET.get('search')

    if search_videos:
        Q(search_videos)
        videos = api.get(url=f"https://api.themoviedb.org/3/search/multi?query={search_videos}&include_adult=false&language=pt-BR&page=1")
    else:
        videos = 'Não encontrado'
    
    context = {
        'keywords': resp_api,
        'search': videos,
        'search_video': search_videos,
    }

    return render(request, template_name='search.html', context=context)