from . import float2, box, shape
import math

Float2= float2.Float2
Box= box.Box
Shape= shape.Shape

clockAngles= [ 0.0, 2.0*math.pi/6.0, math.pi/6.0, 0.0,
               math.pi/-6.0, -2.0*math.pi/6.0, math.pi/-2.0,
               -2.0*math.pi/3.0, -5.0*math.pi/6.0, math.pi,
               5.0*math.pi/6.0, 2.0*math.pi/3.0, math.pi/2.0
               ]
clockPositions= [
    Float2().fromTrigo(x) for x in clockAngles
]
clockLenght= 13
