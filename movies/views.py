from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.template import RequestContext
from django.shortcuts import render, redirect, render_to_response
from .models import *
from .db_functions import *
from django.core.exceptions import ObjectDoesNotExist
import os
from dotenv import load_dotenv

load_dotenv()

users = get_user_model()


def home_view(request, *args, **kwargs):
    return redirect(publicLists_view)


def search_movies_view(request, *args, **kwargs):
    return render(request, "movies/searchMovies.html", status=200)


def plist_detail_view(request, *args, **kwargs):
    if kwargs:
        u = users.objects.get(username=kwargs.get('username'))

        lists = List.objects.filter(listName=kwargs.get('listname'),
                                    user_id=u.id)

        if lists[0].private:
            return redirect(publicLists_view)

        is_user_list = None
        movs = []
        for l in List.objects.filter(id=lists[0].id):
            for m in l.movies.all():
                movs.append(m)

        data = clean_movie_objects(movs)
        data2 = []
        try:
            data2 = List.objects.filter(user=request.user)
        except:
            print("no lists")

        return render(
            request,
            "movies/tmdbResults.html",
            {
                "data": data,
                "data2": data2,
                "isMovie": True,
                "isLocal": True,
                "isUserList": is_user_list,
                "lname": lists[0].listName,
            },
        )

    else:
        return redirect(publicLists_view())


def userLists_view(request, *args, **kwargs):
    # get all the lists tied to user

    if request.method == "GET":
        # get lists tied only to user
        lists = List.objects.filter(user=request.user)

        # clean lists and add count
        data = cleanListObjects(lists, users)

        ulist = f"{request.user}'s Lists"

        return render(request, "movies/userLists.html", {"data": data,
                                                         "lname": ulist})

    elif request.method == "POST":
        data_field = request.POST
        if "deleteList" in data_field.keys():
            # delete list from user lists
            List.objects.filter(id=data_field["deleteList"]).delete()

            # get remaining lists
            lists = List.objects.filter(user=request.user)

            # clean objects and add count
            data = cleanListObjects(lists, users)

            return render(request, "movies/userLists.html", {"data": data})

        elif "viewList" in data_field.keys():
            is_user_list = data_field["viewList"]
            movs = []
            for l in List.objects.filter(id=data_field["viewList"]):
                for m in l.movies.all():
                    movs.append(m)

            data = clean_movie_objects(movs)
            data2 = []
            try:
                data2 = List.objects.filter(user=request.user)
            except:
                print("no lists")

            if "public" in data_field.keys():
                is_user_list = None

            return render(
                request,
                "movies/tmdbResults.html",
                {
                    "data": data,
                    "data2": data2,
                    "isMovie": True,
                    "isLocal": True,
                    "isUserList": is_user_list,
                    "lname": data_field["lname"],
                },
            )

        elif "deleteMovie" in data_field.keys():
            movs = []
            for l in List.objects.filter(id=data_field["listID"]):
                for m in l.movies.all():
                    print(m.id)
                    if m.id == int(data_field["deleteMovie"]):
                        # delete from M:M relationship table only
                        l.movies.remove(m)
                    else:
                        movs.append(m)
            data = clean_movie_objects(movs)
            data2 = []
            try:
                data2 = List.objects.filter(user=request.user)
            except:
                print("no lists")

            return render(
                request,
                "movies/tmdbResults.html",
                {
                    "data": data,
                    "data2": data2,
                    "isMovie": True,
                    "isLocal": True,
                    "isUserList": data_field["listID"],
                },
            )


def publicLists_view(request, *args, **kwargs):
    # get all lists

    lists = List.objects.all()
    data = cleanListObjects(lists, users)
    data = sorted(data, key=lambda x: x["count"], reverse=True)
    ulist = "Public Lists"

    return render(request, "movies/publicLists.html", {"data": data,
                                                       "lname": ulist})


def comments_view(request, *args, **kwargs):
    # get all lists
    movieID = request.POST.getlist("mid")[0]
    print(movieID)
    mov = Movie.objects.get(tmdbID=movieID)

    disc = Comment.objects.filter(movies=mov)
    disc = cleanCommentObject(disc, users)
    mov_obj = clean_movie_objects(Movie.objects.filter(tmdbID=movieID))

    # get lists tied only to user
    lists = List.objects.filter(user=request.user)

    # clean lists and add count
    list_obj = cleanListObjects(lists, users)

    return render(request, "movies/comments.html", {"comments": disc,
                                                    "movie": mov_obj[0],
                                                    "data2": list_obj,
                                                    "isComment": True})


def addComment_view(request, *args, **kwargs):
    comment = request.POST.getlist("comment")[0]
    movID = request.POST.getlist("mid")[0]

    mov = Movie.objects.get(id=movID)

    # list_name = list_name.replace(" ", "_")
    spoiler = False
    try:
        spoiler = request.POST.getlist("spoiler")[0]
    except:
        print("list will be public")

    com_object = Comment(body=comment, spoiler=spoiler,
                         user=request.user, movies=mov)
    com_object.save()

    disc = Comment.objects.filter(movies=mov)
    disc = cleanCommentObject(disc, users)

    print(disc)

    mov_obj = clean_movie_objects(Movie.objects.filter(id=movID))
    # print(data2)

    # get lists tied only to user
    lists = List.objects.filter(user=request.user)

    # clean lists and add count
    list_obj = cleanListObjects(lists, users)

    return render(request, "movies/comments.html", {"comments": disc,
                                                    "movie": mov_obj[0],
                                                    "data2": list_obj,
                                                    "isComment": True})


def filmbooks_movies_view(request, *args, **kwargs):
    movs = Movie.objects.all()

    data = clean_movie_objects(movs)
    data2 = []
    userDBase = "User's TOP 100"
    print("Added_By_Users")

    try:
        data2 = List.objects.filter(user=request.user)
        print(data2)
    except:
        print("user has no lists")

    return render(
        request,
        "movies/tmdbResults.html",
        {
            "data": data,
            "data2": data2,
            "isMovie": True,
            "isLocal": True,
            "lname": userDBase,
        },
    )


def searchDB_view(request, *args, **kwargs):
    return render(request, "movies/tmdbResults.html", {'apikey': str(os.getenv('API_KEY'))})


def searchTMDB_view(request, *args, **kwargs):
    actor = request.POST.getlist("actor")[0]
    title = request.POST.getlist("title")[0]
    genre = request.POST.getlist("genre")[0].lower()
    year = request.POST.getlist("year")[0]

    tmdbDBase = "TMDB Search Results"
    print("Added_By_Users")

    data = []
    for i in range(1, 5):
        data.extend(
            tmdb_discover(actor=actor,
                          title=title,
                          genre=genre,
                          year=year,
                          page=i))

    data2 = []

    try:
        data2 = List.objects.filter(user=request.user)
        print(data2)

    except:
        print("user not logged in or no lists to show")
    return render(
        request,
        "movies/tmdbResults.html",
        {
            "data": data,
            "data2": data2,
            "isMovie": True,
            "lname": tmdbDBase,
            "tmdb": True,
            "apikey": str(os.getenv('API_KEY'))
        },
    )


def update_ratings_view(request, *args, **kwargs):
    movs = Movie.objects.all()
    for m in movs:
        newRating = update_ratings(m.tmdbID)
        if newRating:
            print("updated rating for id " + str(m.tmdbID) + " to " +
                  str(newRating) + ".")
            m.rating = newRating
            m.save()
    return redirect(searchDB_view)


def addList_view(request, *args, **kwargs):
    list_name = request.POST.getlist("new")[0]
    list_name = list_name.replace(" ", "_")
    priv = False
    try:
        priv = request.POST.getlist("private")[0]
    except:
        print("list will be public")

    list_object = List(listName=list_name, private=priv, user=request.user)
    list_object.save()

    return redirect(userLists_view)


def addFromTMDB_view(request, *args, **kwargs):
    p = request.POST.getlist("poster")[0]
    t = request.POST.getlist("tmdbID")[0]
    o = request.POST.getlist("overview")[0]
    g = request.POST.getlist("genre")[0]
    l = request.POST.getlist("lang")[0]
    tit = request.POST.getlist("title")[0]
    d = request.POST.getlist("date")[0]
    r = request.POST.getlist("rating")[0]
    c = request.POST.getlist("cast")[0]
    ls = request.POST.getlist("listID")[0]
    rate = request.POST.getlist("rating")[0]

    try:
        gg = Genres.objects.get(genreName=g)
        print(gg.id)
    except:
        gen = Genres(genreName=g)
        gen.save()
        print("genre added")

    try:
        ll = Languages.objects.get(languageName=l)
        print(ll.id)
    except:
        lang = Languages(languageName=l)
        lang.save()
        print("language added")

    try:
        dd = Years.objects.get(yearDate=d)
        print(dd.id)
    except:
        date = Years(yearDate=d)
        date.save()
        print("date added")

    gg = Genres.objects.get(genreName=g)
    ll = Languages.objects.get(languageName=l)
    dd = Years.objects.get(yearDate=d)

    mov = Movie(
        tmdbID=t,
        poster=p,
        overview=o,
        title=tit,
        genre=gg,
        years=dd,
        lang=ll,
        rating=rate,
    )
    movieExists = False
    try:
        mov.save()
    except:
        print("movie already in database")
        movieExists = True

    # many to many tables
    try:
        list_name = List.objects.get(id=ls)
        list_name.movies.add(Movie.objects.get(tmdbID=t))
    except ObjectDoesNotExist:
        print("list doesn't exist")

    if not movieExists:
        test = c.split('\n')
        for i in range(0, len(test)):
            temp = test[i].lstrip()
            try:
                Actor.objects.get(name=temp)
                print("actor in database")

            except ObjectDoesNotExist:
                act = Actor(name=temp)
                act.save()

            try:
                actrel = Actor.objects.get(name=temp)
                mov.actors.add(actrel)
                print("new actor relationship created")
            except:
                print("actor relationship exists")

            if i > 40:
                break

    return redirect(searchDB_view)
