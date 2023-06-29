from rest_framework.views import APIView, Request, Response, status
from django.forms.models import model_to_dict
from .models import Team
from datetime import datetime
from utils import data_processing
from teams.exceptions import (
    NegativeTitlesError,
    InvalidYearCupError,
    ImpossibleTitlesError,
)


class TeamsView(APIView):
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        teams_list = [model_to_dict(team) for team in teams]
        return Response(teams_list, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data_processing(request.data)
            team = Team.objects.create(**request.data)
            team_dict = model_to_dict(team)
        except NegativeTitlesError as e:
            return Response ({'error': e.message}, status.HTTP_400_BAD_REQUEST)
        except InvalidYearCupError as e:
            return Response ({'error':  e.message}, status.HTTP_400_BAD_REQUEST)
        except ImpossibleTitlesError as e:
            return Response ({'error':  e.message}, status.HTTP_400_BAD_REQUEST)
                

        return Response(team_dict, status=status.HTTP_201_CREATED)


class TeamDetals(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        team_dic = model_to_dict(team)
        return Response(team_dic, status.HTTP_200_OK)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        team_dic = model_to_dict(team)

        return Response(team_dic, status.HTTP_200_OK)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
