from enum import Enum

class ObjectType(Enum):
    unknown         = 0
    Ground          =  1
    Static          =  2
    Aerodrome       =  3
    Sea             =  4
    Watercraft      =  5
    Warship         =  6
    Building        =  7
    Heavy           =  8
    Armor           =  9
    Vehicle         = 10
    Tank            = 11
    AntiAircraft    = 12
    Light           = 13
    Human           = 14
    Infantry        = 15
    AircraftCarrier = 16
    Air             = 17
    FixedWing       = 18
    Rotorcraft      = 19
    
class Hemisphere(Enum):
    N = 0
    S = 1
    E = 2
    W = 3
    undeclared = 4
    
    