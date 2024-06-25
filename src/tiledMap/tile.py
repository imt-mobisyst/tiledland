import math, shapely

class Tile:

    # Initialization Destruction:
    def __init__( self, points= []):
        self._size= len(points)
        self._shape= shapely.Polygon( points )
        self._tags= [ 0 for i in range( self._size ) ]
        self._connexions= []
        self._connexionMirors= []
        self._connexionGates= []

    def setTags( self, tags ):
        self._tags= tags
    
    # Accessors:
    def size(self):
        return self._size
    
    def center(self):
        point= shapely.centroid(self._shape)
        return (point.x, point.y)
    
    def segments(self):
        coords= shapely.get_coordinates(self._shape)
        assert( len(coords)-1 == self._size )
        return [
            ( tuple(coords[i]), tuple(coords[i+1]) )
            for i in range(self._size)
        ]
    
    def segment(self, i):
        coords= shapely.get_coordinates(self._shape)
        return ( tuple(coords[i]), tuple(coords[i+1]) )
    
    def segmentTags(self):
        return self._tags
