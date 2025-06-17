from django.urls import path
from .views import interview_api
from .views import index, interview_api,personal_login,interview_dashboard,save_summary,show_summary

urlpatterns = [ 
    # path("", index),
    path('personal_login/',personal_login, name='personal_login'),
    path("interview/", interview_api),
    path('interview_dashboard/', interview_dashboard, name='interview_dashboard'),
    path('save-summary/',save_summary),       # <-- new route to save results
    path('summary/', show_summary, name="summary"),
]