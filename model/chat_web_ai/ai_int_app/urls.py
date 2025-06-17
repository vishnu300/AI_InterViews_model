from django.urls import path
from .views import interview_api
from .views import index, interview_api,personal_login,interview_dashboard

urlpatterns = [ 
    # path("", index),
    path('personal_login/',personal_login, name='personal_login'),
    path("interview/", interview_api),
    path('interview_dashboard/', interview_dashboard, name='interview_dashboard'),
]