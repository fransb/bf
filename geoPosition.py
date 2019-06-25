from latlongType import *
from math import radians, cos, sin, asin, sqrt

class geoPosition:

    def __init__(self):
        self._lat = latType(PosType.Lat)
        self._long = latType(PosType.Long)
    
    @property
    def lat(self):
        return self._lat
        
    @property
    def long(self):
        return self._long


    def parseGeoLat(self, data):
        parseDegree=float(int(data.split(".")[0]))
        deci=data.split(".")[1].ljust(8,"0")

        if parseDegree > 0:
            parseHemiSphere = Hemisphere.N
        else :
            parseHemiSphere = Hemisphere.S
            parseDegree = -parseDegree

        parseDegree = parseDegree + int(deci[0:2])/60
        parseDegree = parseDegree + int(deci[2:4])/3600
        parseDegree = parseDegree + int(deci[4:6])/360000
        print(parseDegree)
        #parseMillisecond = int(deci[4:6])
        
        
        self._lat.hemisphere = parseHemiSphere
        self._lat.degree = parseDegree
        print(str(self._lat))
        

    def parseGeoLong(self, data):
        parseDegree=float(data.split(".")[0])
        deci=data.split(".")[1].ljust(8,"0")
        if parseDegree > 0:
            parseHemiSphere = Hemisphere.E
        else :
            parseHemiSphere = Hemisphere.W
            parseDegree = -parseDegree
        parseDegree = parseDegree + int(deci[0:2])/60
        parseDegree = parseDegree + int(deci[2:4])/3600
        parseDegree = parseDegree + int(deci[4:6])/360000
        print(parseDegree)
        #parseMillisecond = int(deci[4:6])
        
        
        self._long.hemisphere = parseHemiSphere
        self._long.degree = parseDegree
        print(str(self._long))
    
    def parseLat(self, line, refLat, file):
        parseDegree=float(line)+float(refLat)
        #print("Latitude: "+format(parseDegree, '.7f')+'\n')
        
        if parseDegree > 0:
            parseHemiSphere = Hemisphere.N
        else :
            parseHemiSphere = Hemisphere.S
            parseDegree = -parseDegree
        
        self._lat.hemisphere = parseHemiSphere
        self._lat.degree = parseDegree

        
        

    def parseLong(self, line, refLong, file):
        parseDegree=float(line)+float(refLong)
        #print("Longitude: "+format(parseDegree, '.7f')+'\n')
        if parseDegree > 0.0:
            parseHemiSphere = Hemisphere.E
        else :
            parseHemiSphere = Hemisphere.W
            parseDegree = -parseDegree

        
        self._long.hemisphere = parseHemiSphere
        self._long.degree = parseDegree

        #print(self._long)

    def __str__(self):
        return str(self._lat)+" "+str(self._long)

    def getDecimalDegreeLat(self):
        return self._lat.degree

    def getDecimalDegreeLong(self):
        return self._long.degree
        
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
