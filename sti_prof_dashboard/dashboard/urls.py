from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('icons/icons.svg', RedirectView.as_view(url="/static/epfl/elements/icons/icons.svg")),
]
