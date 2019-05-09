from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.index, name="index"),
    path('teaching/ECTS_rankings', views.ECTS_credits_rankings, name="ECTS_credits_rankings" ),
    path('teaching/ECTS_credits_details', views.ECTS_credits_details, name="ECTS_credits_details" ),
    path('teaching/teaching_hours_rankings', views.teaching_hours_rankings, name="teaching_hours_rankings"),
    path('finance/finances', views.finances, name="finances"),
    path('campus/space_used', views.space_used, name="space_used"),
]
