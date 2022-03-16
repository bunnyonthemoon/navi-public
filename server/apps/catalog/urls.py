from django.urls import include, path

from . import views

urlpatterns = [
    path("complex/<str:complex_key>/", views.complex),
    path("lot/<str:lot_id>/", views.lot),
    path("selection/<str:selection_key>/", views.selection),
    path("filter/", views.filter),
    path("options/", views.options),
    path("favorites/", views.favorites),
]
