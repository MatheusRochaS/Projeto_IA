from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    movie = models.BigIntegerField(null=False)
    watch = models.BooleanField(default='False')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Serie(models.Model):
    serie = models.BigIntegerField(null=False)
    complete = models.BooleanField(default='False')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Season(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, verbose_name='Serie_ID')
    season = models.IntegerField(null=False)
    title = models.CharField(max_length=150, null=True, blank=True)

class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name='Season_ID')
    episode = models.IntegerField(null=False)
    watch = models.BooleanField(default='False')
    title = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ListUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, verbose_name='User_ID')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Movie_ID')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, verbose_name='Serie_ID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)