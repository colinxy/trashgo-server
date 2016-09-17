from math import radians, cos, sin, asin, sqrt
from .models import User, Location, Hotspot

HOTSPOT_RADIUS = 20


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
    # Merge location with hotspot, or create one in position
    hotspots = Hotspot.objects.all()
    mindist = 1000
    target = None

    for hotspot in hotspots:
        dist = haversine(lon1, lat1, hotspot.longitude, hotspot.latitude)
        if dist < HOTSPOT_RADIUS and dist < mindist:
            mindist = dist
            target = hotspot

    if target is not None :
        target.frequency += 1
        target.save()

    else :
        newHotspot = Hotspot(longitude = lon1, latitude = lat1, frequency = 0);
        newHotspot.save()


"""
Get related points according to the current bounds

http://stackoverflow.com/questions/14285963/google-maps-get-viewport-latitude-and-longitude

bounds is a 4-tuple containing NE Lat, NE Lng, SW Lat, SW Lng
"""

def getNearbyHotspots(bounds, scale = 1.0):
    delta_lng = bounds[1] - bounds[3]
    delta_lat = bounds[0] - bounds[2]
    bounds[1] += delta_lng
    bounds[3] -= delta_lng
    bounds[0] += delta_lat
    bounds[2] -= delta_lat

    q = Hotspot.objects.filter(longitude__lte=bounds[1],
                           longitude__gte=bounds[3],
                           latitude__lte = bounds[0],
                           latitude__gte=bounds[2])

    return q.objects.all()



