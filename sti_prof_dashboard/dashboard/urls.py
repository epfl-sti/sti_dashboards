from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.index, name="index"),
    path('ECTS_rankings', views.ECTS_credits_rankings, name="ECTS_credits_rankings" ),
]
