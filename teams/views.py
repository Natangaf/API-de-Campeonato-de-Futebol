from rest_framework.views import APIView, Request, Response, status
from django.forms.models import model_to_dict
from .models import Team
from datetime import datetime


class teamsView(APIView):
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        teams_list = [model_to_dict(team) for team in teams]
        return Response(teams_list, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        data = request.data
        if int(data.get("titles", 0)) < 0:
            return Response(
                {"error": "titles cannot be negative"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        first_cup_date = datetime.strptime(data.get("first_cup"), "%Y-%m-%d")
        print(first_cup_date)

        if first_cup_date.year < 1930 or (first_cup_date.year - 1930) % 4 != 0:
            return Response(
                {"error": "there was no world cup this year"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        expected_years = (datetime.now().year - first_cup_date.year) // 4 + 1
        if data.get("titles") is not None and data.get("titles") > expected_years:
            return Response(
                {"error": "impossible to have more titles than disputed cups"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        team = Team.objects.create(**data)
        team_dict = model_to_dict(team)

        return Response(team_dict, status=status.HTTP_201_CREATED)


class teamDetals(APIView):
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
