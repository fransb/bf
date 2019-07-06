from geoPosition import *
from types import *
import json

class tacticalObject:

    def __init__(self):
        self._geoPosition = []
        self._name = ""
        self._color = ""
        self._coalition = ""
        self._country = ""
        self._group = ""
        self._id = ""
        self._status = ""
        self._towrite = True
        self._objectTypes = ""
        self._altitude = []


    @property
    def geoPosition(self):
        return self._geoPosition[-1]

    #@geoPosition.setter
    #def geoPosition(self, geoPosition):
        #self._geoPosition
        
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
        self._objectTypes = objectTypes

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
        return self._altitude[-1]

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
        self._color = color

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
                self._geoPosition.append(geoPosition())
                self._altitude.append(0.0)
                long = part.split("|")[0].replace("T=","")
                #print(long)
                lat = part.split("|")[1]
                #print(lat)
                alt = part.split("|")[2]
                if not long == "":
                    self._geoPosition[-1].parseLong(long, refLong, file)
                else:
                    self._geoPosition[-1].long = self._geoPosition[-2].long

                if not lat == "":
                    self._geoPosition[-1].parseLat(lat, refLat, file)
                else:
                    self._geoPosition[-1].lat = self._geoPosition[-2].lat

                if not alt == "":
                    self._altitude[-1] = float(alt)
                elif len(self._altitude) > 1:
                    self._altitude[-1] = self._altitude[-2]
                    

            elif "Type=" in part:
                self._objectTypes=part.replace("Type=","")
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
        self._distance = self._geoPosition[-1].calcDistance(refPos)
        

    def __str__(self):
        #print(self._distance)
        return str(self._geoPosition[-1]) + " altitude: " \
                + str(int(round(self._altitude[-1]/0.3048))) + " feet" \
                +" Distance: " + format(self._distance*1000, '.3f') + " km  " \
                + " Type: " + self._objectTypes \
                + " Name: " + self._name \
                + " Group: " + self._group \
                + " status: " + self._status \
                + " movements " + str(len(self._geoPosition))
                #+ str(self._geoPosition[-1].getDecimalDegreeLat())+", "+str(self._geoPosition[-1].getDecimalDegreeLong()) + \
                #" altitude:" + self._altitude[-1] + \
                #" Color: " + self._color + \
   
#" Coalition: " + self._coalition + 
#" Country: " + self._country + 
#str(self._geoPosition.getDecimalDegreeLat())+", "+str(self._geoPosition.getDecimalDegreeLong()) + 
#" id: " + self._id + 

    def __lt__(self, other):
        if self.towrite and other.towrite:
            #print("self:  " + self._name + str(self.print))
            #print("other: " + other.name + str(other.print))
            return (self.distance < other.distance)
        elif not self.towrite:
            return False
        else:

            return True
