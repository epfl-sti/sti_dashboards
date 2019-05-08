from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('credits', views.ECTS_credits_by_teacher, name="ECTS_credits_by_teacher" ),
    path('icons/icons.svg', RedirectView.as_view(url="/static/epfl/elements/icons/icons.svg")),
]
