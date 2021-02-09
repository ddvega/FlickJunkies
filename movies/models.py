from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Years(models.Model):
    yearDate = models.CharField(max_length=20, unique=True)

    def __repr__(self):
        return f"Years('{self.yearDate}'"


class Genres(models.Model):
    genreName = models.CharField(max_length=255, unique=True)

    def __repr__(self):
        return f"Genres('{self.genreName}')"


class Languages(models.Model):
    languageName = models.CharField(max_length=255, unique=True)

    def __repr__(self):
        return f"Languages('{self.languageName}')"


class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdbID = models.IntegerField(unique=True)
    poster = models.CharField(max_length=255)
    overview = models.TextField()
    rating = models.FloatField(null=True)
    title = models.CharField(max_length=255, unique=True)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    years = models.ForeignKey(Years, on_delete=models.CASCADE)
    lang = models.ForeignKey(Languages, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor, blank=True)

    class Meta:
        ordering = ['-rating']


class Comment(models.Model):
    body = models.TextField()
    spoiler = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    movies = models.ForeignKey(Movie, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __repr__(self):
        return f"Comment('{self.body}')"


class List(models.Model):
    listName = models.CharField(max_length=100)
    private = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return self.listName
