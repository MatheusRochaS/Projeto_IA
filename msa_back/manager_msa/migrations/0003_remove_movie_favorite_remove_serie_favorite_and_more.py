# Generated by Django 4.2.6 on 2023-11-25 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_msa', '0002_movie_favorite_serie_favorite_alter_movie_watch_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='favorite',
        ),
        migrations.RemoveField(
            model_name='serie',
            name='favorite',
        ),
        migrations.AddField(
            model_name='movie',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='serie',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
