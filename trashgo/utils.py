from math import radians, cos, sin, asin, sqrt
from .models import Team, Hotspot, Bin
from .capitalone import rewardCustomer

HOTSPOT_RADIUS = 20
BIN_RADIUS = 10


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    m = 6367000 * c
    return m


def updateHotspot(lon1, lat1):
    hotspots = Hotspot.objects.all()
    mindist = 1000
    target = None

    for hotspot in hotspots:
        dist = haversine(lon1, lat1, hotspot.longitude, hotspot.latitude)
        if dist < HOTSPOT_RADIUS and dist < mindist:
            mindist = dist
            target = hotspot

    if target is not None:
        target.frequency += 1
        target.save()

    else:
        newHotspot = Hotspot(longitude=lon1,
                             latitude=lat1,
                             frequency=1)
        newHotspot.save()


def updateBin(user, lon1, lat1):
    # Merge location with hotspot, or create one in position
    print ("Updatebin running...")
    hotspots = Bin.objects.filter(team=user.team)
    mindist = 1000
    target = None
    pointsUp = 0

    for hotspot in hotspots:
        dist = haversine(lon1, lat1, hotspot.longitude, hotspot.latitude)
        if dist < BIN_RADIUS and dist < mindist:
            mindist = dist
            target = hotspot

    if target is not None:
        target.frequency += 1
        # Old site, team gets one point
        target.save()
        pointsUp = 0

    else:
        for team_ref in Team.objects.all():
            newBin = Bin(longitude=lon1,
                         latitude=lat1,
                         frequency=0,
                         team=team_ref)
            if team_ref == user.team:
                newBin.frequency += 1
            newBin.save()

        # New site discovered. 3 points.
        pointsUp = 1

    user.points += pointsUp
    user.save()
    rewardCustomer(user.user_name, pointsUp)
    user.team.points += pointsUp
    user.team.save()

"""
Get related points according to the current bounds

http://stackoverflow.com/questions/14285963/google-maps-get-viewport-latitude-and-longitude

bounds is a 4-tuple containing NE Lat, NE Lng, SW Lat, SW Lng
"""


def getNearbyHotspots(ne_lat, ne_lng, sw_lat, sw_lng):
    delta_lng = ne_lng - sw_lng
    delta_lat = ne_lat - sw_lat

    if delta_lng < 1:
        ne_lng += delta_lng
        sw_lng -= delta_lng
    if delta_lat < 1:
        ne_lat += delta_lat
        sw_lat -= delta_lat

    q = Hotspot.objects.filter(longitude__lte=ne_lng,
                               longitude__gte=sw_lng,
                               latitude__lte=ne_lat,
                               latitude__gte=sw_lat)

    return q


def getNearbyBins(ne_lat, ne_lng, sw_lat, sw_lng):
    delta_lng = ne_lng - sw_lng
    delta_lat = ne_lat - sw_lat

    if delta_lng < 1:
        ne_lng += delta_lng
        sw_lng -= delta_lng
    if delta_lat < 1:
        ne_lat += delta_lat
        sw_lat -= delta_lat

    q = Bin.objects.filter(team=Team.objects.all()[0]).\
        filter(longitude__lte=ne_lng,
               longitude__gte=sw_lng,
               latitude__lte=ne_lat,
               latitude__gte=sw_lat)

    return q



