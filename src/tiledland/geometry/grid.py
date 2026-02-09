import math
from ..pod import Podable, Pod
from .basic import Point, Line
from .convex import Point, Convex
from .mesh import Mesh
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
        minMatter= -1
        maxMatter= self.cell(1, 1)

        for ix in range(1, self.width()+1):
            for iy in range(1, self.height()+1):
                matter= self.cell(ix, iy)
                if minMatter == -1 :
                    minMatter= matter
                if matter >= 0 :
                    minMatter= min(minMatter, matter)
                    maxMatter= max(maxMatter, matter)
        return (minMatter, maxMatter)
    
    # Tests
    def isCell(self, x, y, state):
        return ( self.cell(x, y) == state )
    
    # Cleaning :
    def filter(self, value, modif):
        for i in range( self.height() ) :
            for j in range( self.width() ) :
                if self._grid[i][j] == value :
                    self._grid[i][j]= modif

    # Clustering :
    def clustering(self, matter, radius):
        means= self.clusterInit(matter, radius)
        minDistance= 1.0
        while minDistance > 0.001 :
            marks, newMeans= self.clusterIterate(matter, means, radius)
            for p, np in zip( means.points(), newMeans.points() ) :
                minDistance= min(minDistance, p.distance(np))
            means= newMeans
        return marks, means
    
    def clusterInit(self, matter, radius):
        cosPi6= 0.86602540378
        distance= radius*2
        pi6Distance= cosPi6*distance
        w, h= self.dimention()
        nbWidth= int(max(w//(distance), 1))
        nbHeight= int(max(h//(pi6Distance), 1))
        print( f"so: {nbWidth} x {nbHeight}" )
        means= []
        wMarge= w - nbWidth*distance + radius
        hMarge= h - nbHeight*pi6Distance + radius
        for i in range(nbHeight) :
            marge= wMarge
            lineSize= nbWidth
            if i % 2 ==1 :
                marge+= radius
                lineSize-= 1
            for j in range(lineSize):
                means.append( Point(marge+j*distance, hMarge+i*pi6Distance) )
            
        return Mesh( means )
    
    def localPointToCoordinate(self, aPoint):
        return (
            int( min( self.width(), max( 1, int(round(aPoint.x())) ))),
            int( min( self.height(), max( 1, int(round(aPoint.y())) )))
        )
    
    def clusterIterate(self, matter, proposedMeans, radius):
        w, h = self.dimention()

        # Initialize toVisit on mean-positions :
        toVisits= []
        myMeans= Mesh()
        count= 0
        for i in range(proposedMeans.size()) :
            x, y= self.localPointToCoordinate( proposedMeans.point(i+1) )
            x, y, dist= self.searchClosest(matter, x, y)
            if dist <= radius :
                toVisits.append( [(x, y)] )
                myMeans.append( proposedMeans.point(i+1) )
                count+= 1
        nbCluster= myMeans.size()

        # Initialize marks on 0 :
        marks= Grid(
            [ [ 0 for j in range(w)]  for i in range(h) ],
            self.position(), self.resolution()
        )

        # Initialize newMeans :
        clusterSum= [ Point() for i in range(nbCluster) ]
        clusterCount= [ 0 for i in range(nbCluster) ]

        while count > 0 :
            visited= []
            # Mark
            for i in range(nbCluster) :
                iCl= i+1
                for x, y in toVisits[i] :
                    p= Point(x, y)
                    cCl= marks.cell(x, y)
                    if cCl == 0 :
                        marks.setCell( x, y, iCl )
                        visited.append( (x, y) )
                    elif myMeans.point(iCl).distanceSquare(p) < myMeans.point(cCl).distanceSquare(p) :
                        marks.setCell( x, y, iCl )

            ## Enlarge :
            count= 0
            toVisits= [ [] for i in range(nbCluster) ]
            for x, y in visited :
                i= marks.cell(x, y)-1
                clusterSum[i].add( Point(x, y) )
                clusterCount[i]+= 1
                for cx, cy in [ (x+1, y), (x-1, y), (x, y+1), (x, y-1) ] :
                    if 0 < cx and cx <= w and 0 < cy and cy <= h and self.cell(cx, cy) == matter :
                        toVisits[i].append( (cx, cy) )
                        count+=1
        return marks, Mesh( [ Point( p.x()/c, p.y()/c ) for p, c in zip(clusterSum, clusterCount) ] )
    
    def clusterApplyBirdDistance(self, matter, means):
        w, h = self.dimention()
        clusterCenters= [ Point() for i in range( means.size() ) ]
        clusterCount= [ 0 for i in range( means.size() ) ]
        mask= Grid( [ [ 0 for j in range(w)]  for i in range(h) ] )
        for x in range( 1, w+1 ):
            for y in range( 1, h+1 ):
                if self.cell(x, y) == matter :
                    p= Point(x, y)
                    iCluster= means.searchClosestTo( p )
                    mask.setCell(x, y, iCluster)
                    clusterCenters[iCluster-1].add(p)
                    clusterCount[iCluster-1]+= 1
                    #cluster= 
        for i in range( means.size() ) :
            clusterCenters[i]._x/= clusterCount[i]
            clusterCenters[i]._y/= clusterCount[i]
        
        dists= [ clusterCenters[i].distance( means.point(i+1) ) for i in range(means.size()) ]
        return mask, Mesh( clusterCenters ), dists

    # Cuting :
    def cutingRectangles(self, state, expectedLenght):
        pos= self.searchLine(state)
        rectangles= []
        cellsSize= int( expectedLenght/self.resolution() )
        
        while pos :
            x, y= pos
            rect= self.maxRectangle(x, y, cellsSize)
            self.setRectangleOn( rect, -1 )
            rectangles.append( rect )
            pos= self.searchLine(state)
        
        for rect in rectangles :
            self.setRectangleOn(rect, state)
        return rectangles
    
    def maxRectangle(self, x, y, expectedCellsLenght):
        state= self.cell(x, y)
        width, height= self.dimention()
        x2= x+1
        y2= y+1
        xOk, yOk= True, True
        while xOk or yOk :
            xOk= xOk and x2 <= width and (x2-x) < expectedCellsLenght
            # Increase on x:
            iy= y
            while xOk and iy < y2 :
                xOk= xOk and (self.cell( x2, iy ) == state)
                iy+= 1
            if xOk :
                x2+= 1
            # Increase on y:
            yOk= yOk and y2 <= height and (y2-y) < expectedCellsLenght
            ix= x
            while yOk and ix < x2 :
                yOk= yOk and (self.cell( ix, y2 ) == state)
                ix+= 1
            if yOk :
                y2+= 1
        # Then return
        return [x, y, x2-1, y2-1]

    def searchClosest(self, matter, x, y):
        if self.cell(x, y) == matter :
            return (x, y, 0)
        w, h= self.dimention()
        for distance in range(1, max( w, h) ) :
            for d1 in range(distance):
                d2= distance-d1
                for cx, cy in [(x+d2, y+d1), (x-d1, y+d2), (x-d2, y-d1), (x+d1, y-d2) ] :
                    if 0 < cx and cx <= w and 0 < cy and cy <= h and self.cell(cx, cy) == matter :
                        return (cx, cy, distance)
        return False, False, max( w, h)

    def searchLine(self, state=0):
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

    def makeConvexes(self, state, expectedSize=1.0):
        rectangles= self.cutingRectangles(state, expectedSize)
        shapes= [ self.rectangleToConvex(rect) for rect in rectangles ]
        return shapes
    
    # to str
    def str(self, typeName="Grid"): 
        # Myself :
        let= ['·'] + [ str(i) for i in range(1, 10) ] + [ chr(65+i) for i in range(26) ]
        s= f"{typeName} {self.width()}x{self.height()}\n"
        for line in self._grid :
            s+= "| " + " ".join( [let[state] for state in line] ) +"\n"
        s+= "0 " + "-".join( ["-" for _ in range(self.width())] )
        return s
    
    def __str__(self):
        return self.str()