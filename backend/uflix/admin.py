from django.contrib import admin

from .models import UserData
from .models import Movie
from .models import Genre
from .models import Comment

# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "poster", "genre_id", "score", "url")


class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "movie_id", "text")


# we will need to register the
# model class and the Admin model class
# using the register() method
# of admin.site class
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserData)
