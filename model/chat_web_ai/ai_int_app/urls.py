# from django.urls import path
# from .views import chatbot_api, home

# urlpatterns = [
#     path('', home),
#     path('chat/', chatbot_api),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.interview_page, name='interview_home'),
    path('chat/', views.interview_chat, name='interview_chat'),
]
