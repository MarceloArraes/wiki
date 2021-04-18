from django.urls import path

from . import views

urlpatterns = [
    path("wiki", views.index, name="index"),
    path("search",views.search, name="search"),
    path("wiki/newPage", views.newPage, name="newPage"),
    path("wiki/<str:title>", views.titles, name="titles"),
    path("wiki/errorpage",views.newPage, name="errorpage")

]
