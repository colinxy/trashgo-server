
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Hotspot, Team, User
from .serializers import HotspotSerializer, TeamSerializer, UserSerializer


class HotspotView(APIView):
    def get(self, request, formaat=None):
        hotspots = Hotspot.objects.all()
        serializer = HotspotSerializer(hotspots, many=True)

        # print(serializer)
        return Response(serializer.data)

    def post(self, request, format=None):
        pass


class TeamView(APIView):
    def get(self, request, format=None):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        pass


class UserView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        pass
