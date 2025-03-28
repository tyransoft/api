import math
from decimal import Decimal


def haversine(lat1,long1,lat2,long2):

    R = 6371

    lat1, long1, lat2, long2 = map(lambda x: float(x), [lat1, long1, lat2, long2])

    lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])

    dlat = lat2 - lat1
    dlong = long2 - long1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return Decimal(distance)