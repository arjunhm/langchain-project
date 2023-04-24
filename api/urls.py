from django.urls import path
from api import views

urlpatterns = [
    path("linkedin/", views.LinkedInPostAPI.as_view()),
]
