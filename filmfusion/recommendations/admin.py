from django.contrib import admin
from .models import Movie, Genre


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_date', 'popularity', 'vote_average')
    search_fields = ('title', 'tmdb_id', 'imdb_id')
    list_filter = ('release_date', 'popularity', 'vote_average', 'genres')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)