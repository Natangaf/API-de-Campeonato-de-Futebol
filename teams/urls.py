from django.urls import path
from .views import TeamsView ,TeamDetals
urlpatterns = [
    path('teams/', TeamsView.as_view()),
    path('teams/<int:team_id>/', TeamDetals.as_view()),
]
