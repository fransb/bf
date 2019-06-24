from geoPosition import *
from latlongType import Hemisphere

position = geoPosition()

position.setLat(Hemisphere.N, 60, 0, 0, 0)
position.setLong(Hemisphere.E, 9, 50, 40, 1)

print(position)

refposition = geoPosition()

refposition.setLat(Hemisphere.N, 60, 0, 0, 0)
refposition.setLong(Hemisphere.E, 9, 51, 40, 1)

print(refposition)

print(position.calcDistance(refposition))
