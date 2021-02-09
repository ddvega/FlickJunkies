from django.contrib import admin

# Register your models here.
from .models import List, Movie, Comment


class ListAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['listName', 'user__username', 'user__email']

    class Meta:
        model = List


class MoviesAdmin(admin.ModelAdmin):
    list_display = ['title', 'rating']
    search_fields = ['title']

    class Meta:
        model = Movie


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body']
    search_fields = ['user', 'body']

    class Meta:
        model = Comment


admin.site.register(List, ListAdmin)
admin.site.register(Movie, MoviesAdmin)
admin.site.register(Comment, CommentAdmin)
