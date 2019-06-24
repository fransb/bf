from enum import Enum
from localTypes import Hemisphere

class PosType(Enum):
    Long = 0
    Lat = 1
    undeclared = 2

class latType:

    def __init__(self,posType : PosType):
        self._hemisphere = Hemisphere.undeclared
        self._degree = 0
        self._minute = 0
        self._second = 0
        self._millisecond = 0
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
        return self._degree

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

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, minute):
        if (minute > 59 or minute < 0):
            raise ValueError("Sorry minute shall be 0-59")
        self._minute=minute
        

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, second):
        if (self.second > 59 or self.second < 0):
            raise ValueError("Sorry second shall be 0-59")
        self._second=second

    @property
    def millisecond(self):
        return self._millisecond

    @millisecond.setter
    def millisecond(self, millisecond):
        if (millisecond > 999 or millisecond < 0):
            raise ValueError("Sorry millisecond shall be 0-999")
        self._millisecond=millisecond

    def __str__(self):
        if (self._type == PosType.Lat):
            posString = self._hemisphere.name+str(self._degree).zfill(2)
        elif (self._type == PosType.Long):
            posString = self._hemisphere.name+str(self._degree).zfill(3)
        else:
            raise ValueError("Sorry error")
        return posString+"°"+str(self._minute).zfill(2)+"\'"+str(self._second).zfill(2)+"\""+str(self._millisecond).zfill(3)

    def getDecimalDegree(self):
        return float(self._degree)+float(self._minute)/float(60)+float(self._second)/float(3600)+float(self._millisecond)/float(3600000)
            
