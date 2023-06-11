from django.urls import path
from .views import teamsView
urlpatterns = [
    path('teams/', teamsView.as_view()),
]
