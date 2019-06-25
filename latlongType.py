from enum import Enum
from localTypes import Hemisphere

class PosType(Enum):
    Long = 0
    Lat = 1
    undeclared = 2

class latType:

    def __init__(self,posType : PosType):
        self._hemisphere = Hemisphere.undeclared
        self._degree = 0.0
        self._type = posType

    @property
    def hemisphere(self):
        return self._hemisphere

    @hemisphere.setter
    def hemisphere(self, hemisphere):
        if ((hemisphere == Hemisphere.N or
            hemisphere == Hemisphere.S) and
            self._type == PosType.Lat):
            self._hemisphere=hemisphere
        elif ((hemisphere == Hemisphere.E or
              hemisphere == Hemisphere.W) and
              (self._type == PosType.Long)):
            self._hemisphere=hemisphere
        else :
            raise ValueError("Sorry hemisphere shall be North, South, East or West")


    @property
    def type(self):
        return self._type

    @property
    def degree(self):
        return self._degree

    @degree.setter
    def degree(self, degree):
        if (degree > 90 or degree < 0) and (self._type == PosType.Lat):
            raise ValueError("Sorry degree shall be 0-90")
        elif (degree > 180 or degree < 0) and (self._type == PosType.Long):
            raise ValueError("Sorry degree shall be 0-180")
        self._degree=degree

  
    def __str__(self):
        d = int(self._degree)
        m = int((self._degree - d) * 60)
        s = int((self._degree - d - m/60) * 3600)
        ms = int((self._degree - d - m/60 - s/3600)*360000)
        mms = int((self._degree - d - m/60- s/3600- ms/360000)*36000000)

        #print("degree: " + str(self._degree))
        #print("minute: " + str(self._degree - d))
        #print("second: " + str(self._degree - d - m/60))
        #print("millisecond: " + str((self._degree - d - m/60 - s/3600)*360000))

        if (self._type == PosType.Lat):
            posString = self._hemisphere.name + " " + str(d).zfill(2)
        elif (self._type == PosType.Long):
            posString = self._hemisphere.name + " " + str(d).zfill(3)
        else:
            raise ValueError("Sorry error")

        
        return posString+ "º "+ str(m).zfill(2)+ "' "+ str(s).zfill(2) + '" ' + str(ms).zfill(2) + " " +str(mms).zfill(2)

#    def getDecimalDegree(self):
#        return float(self._degree)+float(self._minute)/float(60)+float(self._second)/float(3600)+float(self._millisecond)/float(3600000)

#    def getRaw(self):
#        return str(self._degree)+"."+str(self._minute)+str(self._second)+str(self._millisecond)

    def __eq__(self, other):
        return not self.degree < other.degree and not other.degree < self.degree
    def __ne__(self, other):
        return self.degree < other.degree or other.degree < self.degree
    def __gt__(self, other):
        return other.degree < self.degree
    def __ge__(self, other):
        return not self.degree < other.degree
    def __le__(self, other):
        return not other.degree < self.degree
        
    
