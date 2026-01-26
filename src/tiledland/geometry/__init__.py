import math

from .basic import Point, Line
from .box import Box
from .convex import Convex

clockAngles= [ 0.0, 2.0*math.pi/6.0, math.pi/6.0, 0.0,
               math.pi/-6.0, -2.0*math.pi/6.0, math.pi/-2.0,
               -2.0*math.pi/3.0, -5.0*math.pi/6.0, math.pi,
               5.0*math.pi/6.0, 2.0*math.pi/3.0, math.pi/2.0
               ]

clockPositions= [
    Point().fromTrigo(x) for x in clockAngles
]
clockLenght= 13
