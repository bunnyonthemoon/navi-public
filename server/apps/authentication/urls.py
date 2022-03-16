from django.urls import include, path

from . import views

urlpatterns = [
    path("offer/", views.offer),
]
