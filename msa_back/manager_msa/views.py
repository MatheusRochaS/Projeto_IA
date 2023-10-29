from django.shortcuts import render

# Create your views here.
def welcome_view(request):
    return render(request, template_name='welcome.html', status=200)