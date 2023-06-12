from django.urls import path
from .views import teamsView ,teamDetals
urlpatterns = [
    path('teams/', teamsView.as_view()),
    path('teams/<int:team_id>/', teamDetals.as_view()),
]
