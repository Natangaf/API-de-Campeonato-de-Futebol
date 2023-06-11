from rest_framework.views import APIView, Request, Response, status
from django.forms.models import model_to_dict
from .models import Team
from .exceptions import NegativeTitlesError


class teamsView(APIView):
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()

        teams_list = []

        for team in teams:
            team_dict = model_to_dict(team)
            teams_list.append(team_dict)

        return Response(teams_list, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        print(request.data)
        if request.data.get("titles", 0) < 0:
            raise NegativeTitlesError()

        team = Team.objects.create(**request.data)

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_201_CREATED)


class TeamDetals(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        team_dic = model_to_dict(team)
        return Response(team_dic, status.HTTP_200_OK)

    def pach(self, request: Request, team_id: int) -> Response:
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
