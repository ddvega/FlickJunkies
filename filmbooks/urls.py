"""filmbooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include  # url()
from django.views.generic import TemplateView

from accounts.views import login_view, logout_view, register_view, account_view

from movies.views import (
    home_view,
    userLists_view,
    publicLists_view,
    searchTMDB_view,
    addList_view,
    addFromTMDB_view,
    searchDB_view,
    filmbooks_movies_view,
    update_ratings_view,
    search_movies_view,
    comments_view,
    addComment_view,
    plist_detail_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view),
    path("findmovies", search_movies_view),
    path("login/", login_view),
    path("logout/", logout_view),
    path("register/", register_view),
    path("account/", account_view),
    path("userlists/", userLists_view),
    path("lists/<slug:username>/<slug:listname>/", plist_detail_view),
    path("publiclists/", publicLists_view),
    path("searchTMDB/", searchTMDB_view),
    path("addList/", addList_view),
    path("addFromTMDB/", addFromTMDB_view),
    path("searchDB/", searchDB_view),
    path("filmbooks_main/", filmbooks_movies_view),
    path("update_rate/", update_ratings_view),
    path("comments/", comments_view),
    path("addComments/", addComment_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
