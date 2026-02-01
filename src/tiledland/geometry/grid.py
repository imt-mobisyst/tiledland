import math
from ..pod import Podable, Pod
from .basic import Point, Line
from .convex import Point, Convex
#from .box import Box

class Grid() : # ToDo: Podable
    # Initialization
    def __init__(self, values= [[0]], position= Point(0.0, 0.0), resolution=0.1):
        self.initialize(values)
        self._position= position
        self._resolution= resolution

    # Construction
    def initialize(self, aGrid):
        self._grid= aGrid
        self._height= len(self._grid)
        self._width= len(self._grid[0])
        return self

    def setCell( self, x, y, state ):
        i, j= self.inTable(x, y)
        self._grid[i][j]= state
        return self
    
    # Accessors
    def values(self):
        return self._grid
    
    def height(self):
        return self._height

    def width(self):
        return self._width

    def dimention(self):
        return ( self._width, self._height )
    
    def inTable(self, x, y):
        return self._height-y, x-1

    def cell(self, x, y):
        assert 0 < x and x <= self.width() and 0 < y and y <= self.height()
        i, j = self.inTable(x, y)
        return self._grid[i][j]

    def position(self):
        return self._position

    def resolution(self):
        return self._resolution

    def valueMinMax(self):
        if self.height() == 0 :
            return (0, 0)
        minMatter= self.cell(1, 1)
        maxMatter= minMatter

        for ix in range(1, self.width()+1):
            for iy in range(1, self.height()+1):
                matter= self.cell(ix, iy)
                minMatter= min(minMatter, matter)
                maxMatter= max(maxMatter, matter) 
        return (minMatter, maxMatter)
    # Tests
    def isCell(self, x, y, state):
        return ( self.cell(x, y) == state )
    
    # Clustering :
    def clusterRectangles(self, state=0):
        pos= self.search(state)
        rectangles= []
        while pos :
            x, y= pos
            rect= self.maxRectangle(x, y)
            self.setRectangleOn( rect, -1 )
            rectangles.append( rect )
            pos= self.search(state)
        
        for rect in rectangles :
            self.setRectangleOn(rect, state)
        return rectangles
    
    def maxRectangle(self, x, y):
        state= self.cell(x, y)
        width, height= self.dimention()
        x2= x+1
        y2= y+1
        xOk, yOk= True, True
        while xOk or yOk :
            xOk= xOk and x2 <= width
            # Increase on x:
            iy= y
            while xOk and iy < y2 :
                xOk= xOk and (self.cell( x2, iy ) == state)
                iy+= 1
            if xOk :
                x2+= 1
            # Increase on y:
            yOk= yOk and y2 <= height
            ix= x
            while yOk and ix < x2 :
                yOk= yOk and (self.cell( ix, y2 ) == state)
                ix+= 1
            if yOk :
                y2+= 1
        # Then return
        return [x, y, x2-1, y2-1]

    def search(self, state=0):
        x, y= 1, 1
        width, height= self.dimention()
        while y <= height and self.cell(x, y) != state :
            x+= 1
            if x > width :
                x=1
                y+=1
        if y > height :
            return False
        return (x, y)
    
    def setRectangleOn(self, rect, state ):
        bx1, by1, bx2, by2= tuple(rect)
        for ix in range( bx1, bx2+1 ):
            for iy in range( by1, by2+1 ):
                self.setCell(ix, iy, state)
        return self

    # Shaping
    def rectangleToConvex(self, rect):
        r= self.resolution()
        e= r*0.1
        ox, oy= self.position().asTuple()
        bx1, by1, bx2, by2= tuple(rect)
        sx1= ox + (bx1-1)*r + e
        sy1= oy + (by1-1)*r + e
        sx2= ox + bx2*r - e
        sy2= oy + by2*r - e
        return Convex().fromZipped( [(sx1, sy1), (sx1, sy2), (sx2, sy2), (sx2, sy1)] )

    def makeConvexes(self, state=0):
        rectangles= self.clusterRectangles(state)
        shapes= [ self.rectangleToConvex(rect) for rect in rectangles ]
        return shapes
    
    # to str
    def str(self, typeName="Grid"): 
        # Myself :
        s= f"{typeName} {self.width()}x{self.height()}\n"
        for line in self._grid :
            s+= "| " + " ".join( [str(state) for state in line] ) +"\n"
        s+= "0 " + "-".join( ["-" for _ in range(self.width())] )
        return s
    
    def __str__(self): 
        return self.str()