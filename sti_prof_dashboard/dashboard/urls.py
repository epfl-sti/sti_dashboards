from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.index, name="index"),
    path('credits', views.ECTS_credits_by_teacher, name="ECTS_credits_by_teacher" ),
]
