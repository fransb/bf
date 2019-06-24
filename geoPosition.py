from latlongType import *
from math import radians, cos, sin, asin, sqrt

class geoPosition:

    def __init__(self):
        self._lat = latType(PosType.Lat)
        self._long = latType(PosType.Long)
    
    def parseLat(self, line, refLat, file):
        parseDegree=int(line.split(".")[0])+refLat
        deci=int(line.split(".")[0]).ljust(8,"0")
        if parseDegree > 0:
            parseHemiSphere = Hemisphere.N
        else :
            parseHemiSphere = Hemisphere.S
            parseDegree = -parseDegree
        parseMinute = int(deci[0:1])
        parseSecond = int(deci[2:3])
        parseMillisecond = int(deci[4:6])
        
        self._lat.hemisphere = parseHemiSphere
        self._lat.degree = parseDegree
        self._lat.minute = parseMinute
        self._lat.second = parseSecond
        self._lat.millisecond = parseMillisecond
        

    def parseLong(self, line, refLong, file):
        parseDegree=int(line.split(".")[0])+refLong
        deci=line.split(".")[0].ljust(7,"0")
        if parseDegree > 0:
            parseHemiSphere = Hemisphere.E
        else :
            parseHemiSphere = Hemisphere.W
            parseDegree = -parseDegree
        parseMinute = int(deci[0:1])
        parseSecond = int(deci[2:3])
        parseMillisecond = int(deci[4:6])
        
        self._long.hemisphere = parseHemiSphere
        self._long.degree = parseDegree
        self._long.minute = parseMinute
        self._long.second = parseSecond
        self._long.millisecond = parseMillisecond

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
