from geoPosition import *
from types import *
import json

class tacticalObject:

    def __init__(self):
        self._geoPosition = geoPosition()
        self._name = ""
        self._color = ""
        self._coalition = ""
        self._country = ""
        self._group = ""
        self._id = ""
        self._status = ""
        self._towrite = True

    @property
    def geoPosition(self):
        return self._geoPosition

    @geoPosition.setter
    def geoPosition(self, geoPosition):
        self._geoPosition
        
    @property
    def towrite(self):
        return self._towrite

    @towrite.setter
    def towrite(self, towrite):
        self._towrite = towrite

    @property
    def objectTypes(self):
        return self._objectTypes

    @objectTypes.setter
    def objectTypes(self, objectTypes):
        self._objectTypes

    @property
    def fileName(self):
        return self._fileName

    @fileName.setter
    def fileName(self, fileName):
        self._fileName
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id
   
    @property
    def altitude(self):
        return self._altitude

    @altitude.setter
    def altitude(self, altitude):
        self._altitude
        
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color

    @property
    def coalition(self):
        return self._coalition

    @coalition.setter
    def coalition(self, coalition):
        self._coalition

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        self._country

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, group):
        self._group

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status

    @property
    def distance(self):
        return self._distance

    def parseLine(self, line, refLat, refLong, file):
        for part in line.rstrip().split(","):
            #print(line)
            if "T=" in part:
                long = part.split("|")[0].replace("T=","")
                #print(long)
                lat = part.split("|")[1]
                #print(lat)
                alt = part.split("|")[2]
                if not long == "":
                    self._geoPosition.parseLong(long, refLong, file)
                if not lat == "":
                    self._geoPosition.parseLat(lat, refLat, file)
                if not alt == "":
                    self._altitude = alt
            elif "Type=" in part:
                self._objectType=part.replace("Type=","")
            elif "Name=" in part:
                self._name = part.replace("Name=","")
            elif "Color=" in part:
                self._color = part.replace("Color=","")
            elif "Coalition=" in part:
                self._coalition = part.replace("Coalition=","")
            elif "Country=" in part:
                self._country = part.replace("Country=","")
            elif "Group=" in part:
                self._group = part.replace("Group=","")
            elif not "=" in part :
                self._id = part.rstrip()+file
        self._status="Alive"

    def setDistance(self, refPos):
        self._distance = self._geoPosition.calcDistance(refPos)
        

    def __str__(self):
        #print(self._distance)
        return str(self._geoPosition) +"    Distance: " + \
                format(self._distance*1000, '.3f') + " km  " + \
                str(self._geoPosition.getDecimalDegreeLat())+", "+str(self._geoPosition.getDecimalDegreeLong()) + \
                " altitude:" + self._altitude + \
                " Type: " + self._objectType + \
                " Name: " + self._name + \
                " Color: " + self._color + \
                " Coalition: " + self._coalition + \
                " Country: " + self._country + \
                " Group: " + self._group + \
                " id: " + self._id + \
                " status: " + self._status

    def __lt__(self, other):
        if self.towrite and other.towrite:
            #print("self:  " + self._name + str(self.print))
            #print("other: " + other.name + str(other.print))
            return (self.distance < other.distance)
        elif not self.towrite:
            return False
        else:

            return True
