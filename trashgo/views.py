
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Hotspot, User, Team


class HotspotView(APIView):
    def get(self, request, formaat=None):
        return Response(Hotspot.objects.all())

    def post(self, request, format=None):
        pass


class UserView(APIView):
    def get(self, request, format=None):
        return Response(User.objects.all())

    def post(self, request, format=None):
        pass


class TeamView(APIView):
    def get(self, request, format=None):
        return Response(Team.objects.all())

    def post(self, request, format=None):
        pass
