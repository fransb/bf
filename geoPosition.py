from latlongType import *
from math import radians, cos, sin, asin, sqrt

class geoPosition:

    def __init__(self):
        self._lat = latType(PosType.Lat)
        self._long = latType(PosType.Long)

    def setLat(self,
               hemisphere: Hemisphere,
               degree: int,
               minute: int,
               second: int,
               millisecond: int):
        self._lat.hemisphere = hemisphere
        self._lat.degree = degree
        self._lat.minute = minute
        self._lat.second = second
        self._lat.millisecond = millisecond

    def setLong(self,
               hemisphere: Hemisphere,
               degree: int,
               minute: int,
               second: int,
               millisecond: int):
        
        self._long.hemisphere = hemisphere
        self._long.degree = degree
        self._long.minute = minute
        self._long.second = second
        self._long.millisecond = millisecond

    def __str__(self):
        return str(self._lat)+" "+str(self._long)

    def getDecimalDegreeLat(self):
        return self._lat.getDecimalDegree()

    def getDecimalDegreeLong(self):
        return self._long.getDecimalDegree()
 
    def calcDistance(self, refPoint):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [self.getDecimalDegreeLong(),
                                               self.getDecimalDegreeLat(),
                                               refPoint.getDecimalDegreeLong(),
                                               refPoint.getDecimalDegreeLat()])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r
