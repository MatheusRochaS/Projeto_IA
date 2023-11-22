from django.contrib import admin
from .models import Movie, Serie, Season, Episode

# Register your models here.
admin.site.register(Movie)
admin.site.register(Serie)
admin.site.register(Season)
admin.site.register(Episode)