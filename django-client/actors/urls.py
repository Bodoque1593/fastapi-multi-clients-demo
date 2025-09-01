from django.urls import path
from . import views

app_name = "actors"

urlpatterns = [
    path("", views.actor_list, name="list"),
    path("<int:id>/", views.actor_detail, name="detail"),
    path("create/", views.actor_create, name="create"),
    path("<int:id>/edit/", views.actor_update, name="update"),
    path("<int:id>/delete/", views.actor_delete, name="delete"),
]
