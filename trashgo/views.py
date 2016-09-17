
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Hotspot


class HotspotView(APIView):
    def get(self, request, formaat=None):
        return Response(Hotspot.objects.all())
