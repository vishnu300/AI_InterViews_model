from django.urls import path
from .views import interview_api
from .views import index, interview_api

urlpatterns = [
    path("", index),
    path("interview/", interview_api),
]