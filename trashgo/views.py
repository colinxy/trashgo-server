
from rest_framework import status
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Bin, Hotspot, Team, User
from .serializers import (HotspotSerializer, TeamSerializer,
                          UserSerializer, BinSerializer)
from .utils import (updateHotspot, getNearbyHotspots, updateBin,
                    getNearbyBins, submitTrash, makePurchase)


# a public API? Yeah, we know, works for the demo
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class HotspotView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,
                              BasicAuthentication)

    def get(self, request, format=None):
        hotspots = Hotspot.objects.all()
        serializer = HotspotSerializer(hotspots, many=True)

        # print(serializer)
        return Response(serializer.data)

    def post(self, request, format=None):
        # data = JSONParser().parse(request)
        data = request.POST
        print(data)

        try:
            print(data["team"], data["longitude"], data["latitude"])
            facebook_id = data["team"]
            longitude = float(data["longitude"])
            latitude = float(data["latitude"])
            user = User.objects.get(facebook_id=facebook_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        updateHotspot(user, longitude, latitude)
        return Response(status=status.HTTP_201_CREATED)


class BinView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,
                              BasicAuthentication)

    def get(self, request, format=None):
        hotspots = Bin.objects.all()
        serializer = BinSerializer(hotspots, many=True)
        # print(serializer)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.POST
        try:
            print(data["team"], data["longitude"], data["latitude"])
            facebook_id = str(data["team"])
            longitude = float(data["longitude"])
            latitude = float(data["latitude"])
            user = User.objects.get(facebook_id=facebook_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        success = updateBin(user, longitude, latitude)
        return Response({'success': success}, status=status.HTTP_201_CREATED)


class RewardView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,
                              BasicAuthentication)

    def post(self, request, format=None):
        data = request.POST
        try:
            facebook_id = str(data["team"])
            user = User.objects.get(facebook_id=facebook_id)
            price = int(data["price"])
            description = str(data["description"])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        success = makePurchase(user, price, description)

        if success:
            print("{} has redeemed {} at {} successfully".format(user, price, description))
        else:
            print ("Transaction unapproved.")

        return Response({'success': success}, status=status.HTTP_201_CREATED)


class SubmitTrash(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,
                              BasicAuthentication)

    def post(self, request, format=None):
        data = request.POST
        try:
            facebook_id = str(data["team"])
            longitude = float(data["longitude"])
            latitude = float(data["latitude"])
            user = User.objects.get(facebook_id=facebook_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        success = submitTrash(user, longitude, latitude)
        return Response({'success': success}, status=status.HTTP_201_CREATED)


class HotspotWithinView(APIView):
    def get(self, request, ne_lat, ne_lng, sw_lat, sw_lng, format=None):
        print(ne_lat, ne_lng, sw_lat, sw_lng)

        try:
            ne_lat, ne_lng, sw_lat, sw_lng = \
                map(float, (ne_lat, ne_lng, sw_lat, sw_lng))
            if not (-90 < sw_lat < ne_lat < 90 and
                    -180 <= sw_lng < ne_lng <= 180):
                raise ValueError
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = HotspotSerializer(getNearbyHotspots(ne_lat, ne_lng,
                                                         sw_lat, sw_lng),
                                       many=True)
        return Response(serializer.data)


class BinWithinView(APIView):
    def get(self, request, ne_lat, ne_lng, sw_lat, sw_lng, format=None):
        print(ne_lat, ne_lng, sw_lat, sw_lng)

        try:
            ne_lat, ne_lng, sw_lat, sw_lng = \
                map(float, (ne_lat, ne_lng, sw_lat, sw_lng))
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # serializer = BinSerializer(getNearbyBins(ne_lat, ne_lng,
        #                                          sw_lat, sw_lng),
        #                            many=True)
        # return Response(serializer.data)
        return Response(getNearbyBins(ne_lat, ne_lng, sw_lat, sw_lng))


class UserWithId(APIView):
    def get(self, request, facebook_id):
        print (facebook_id)
        user = User.objects.get(facebook_id=str(facebook_id))
        serializer = UserSerializer(user)
        return Response(serializer.data)


class TeamView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,
                              BasicAuthentication)

    def get(self, request, format=None):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


class UserView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,
                              BasicAuthentication)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        print(data)

        user = User(user_name=data["user_name"],
                    team=data["team"],
                    facebook_id=data["facebook_id"],
                    points=0)
        user.save()

        return Response(status=status.HTTP_201_CREATED)
