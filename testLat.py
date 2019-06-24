from latlongType import *

lat = latType(PosType.Lat)
lat.hemisphere = Hemisphere.N
print(lat.hemisphere.name)

lat.degree = 30
print(lat.degree)

lat.minute = 32
print(lat.minute)

lat.second = 33
print(lat.second)

lat.millisecond = 34
print(lat.millisecond)

print(lat)
print(lat.getDecimalDegree())
