import math, shapely
from . import tile, joint, map
from .geometry import Coord2, Segment

# Tiled Map Components:
Tile= tile.Tile
Joint= joint.Joint
Map= map.Map
#Body2= body.Body2

#Line tools: 
def intersection( line1, line2 ):
    line= shapely.intersection( shapely.LineString( line1.list() ), shapely.LineString( line2.list() ) )
    coords= shapely.get_coordinates( line )
    if len(coords) == 0 :
        return False
    x, y= tuple(coords[0])
    return Coord2(x, y)
