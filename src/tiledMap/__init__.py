import math, shapely
from . import tile, joint, map

# Tiled Map Components:
Tile= tile.Tile
Joint= joint.Joint
Map= map.Map
#Body2= body.Body2

# Point tool box:
def roundPoint( aPoint, precision=1 ):
    x, y= aPoint
    return (
        round( x, precision ),
        round( y, precision )
    )

# Point list generators:
def pointlist_regularPolygon( center, nbFaces=4, radius=0.5 ):
    x, y= center
    points= []
    angle= math.pi - ((nbFaces-1)*math.pi/nbFaces)
    delta= math.pi/(nbFaces/2)
    for i in range(nbFaces) :
        points.append( (
            x+math.cos(angle)*radius,
            y+math.sin(angle)*radius
        ) )
        angle+= delta
    return points

def pointlist_hexagon( center, radius=0.5 ):
    return pointlist_regularPolygon( center, 6, radius )

#Line tools: 
def intersection( line1, line2 ):
    line= shapely.intersection( shapely.LineString(line1), shapely.LineString(line2) )
    coords= shapely.get_coordinates( line )
    if len(coords) == 0 :
        return False
    return tuple(coords[0])
