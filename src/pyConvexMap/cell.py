import math
from .point import Point2


class Cell:

    # Initialization Destruction:
    def __init__( self, vertices= []):
        self._vertices= vertices
        self._tags= [0 for i in range( len(vertices) )]
        self.updateCenter()

    # Construction:
    def makeConvex(self):
        return self._vertices
    
    def updateCenter(self):
        self._center= Point2(0.0, 0.0)
        weights= 0.0
        for v1, v2, t in self.segments() :
            v= v1+v2
            dist= v1.distance(v2)
            v.scale(0.5)
            self._center.x+= v.x*dist
            self._center.y+= v.y*dist
            weights+= dist
        if weights > 0.0 :
            self._center.x/= weights
            self._center.y/= weights

    def add( self, aPoint, aTag ):
        self._vertices.append( aPoint )
        self._tags.append( aTag )
    
    def setVertice( self, i, aPoint ):
        self._vertices[i]= aPoint
    
    def setVertices( self, vertices ):
        self._vertices= vertices
    
    def setTags( self, tags ):
        self._tags= tags

    def setTag( self, i, tag ):
        self._tags[i]= tag
        
    def setTag( self, i, tag ):
        self._tags[i]= tag
    
    # Accessors:
    def size(self):
        return len( self._vertices )
    
    def center(self):
        return self._center
    
    def vertices(self):
        return self._vertices
    
    def tags(self):
        return self._tags
    
    def segments(self):
        if self.size() > 0 :
            vertices2= self._vertices[1:] + [self._vertices[0]]
            return zip( self._vertices, vertices2, self._tags )
        return zip( [], [], [] )