from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("random", views.random_entry, name="random"),
    path("wiki/not-found", views.not_found, name="404"),
    path("wiki/<str:name>", views.show, name="show"),
    path("wiki/<str:name>/edit", views.edit, name="edit")
]
