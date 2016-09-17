
from rest_framework.serializers import ModelSerializer

from .models import Hotspot, Team, User


class HotspotSerializer(ModelSerializer):
    class Meta:
        model = Hotspot
        fields = ("longitude", "latitude", "team", "frequency")


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ("name", "points")


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("user_name", "facebook_id", "team", "points")
