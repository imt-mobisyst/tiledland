#----------------------------------------------------------#
# 
# 
#----------------------------------------------------------#
from .geometry import Shape

import yaml, cairo

class GridMap :
    # Initialization
    def __init__(self, states= ['Free', 'Occupied', 'Unknown'], position=(0.0, 0.0), resolution=0.5):
        self._states= states
        self.setGrid( [[0]] )
        self._position= position
        self._resolution= resolution

    # Accessors
    def grid(self):
        return self._grid
    
    def dimention(self):
        return ( len(self._grid[0]), self._height )
    
    def cell(self, x, y):
        dy= self._height-1-y
        return self._grid[dy][x]

    def position(self):
        return self._position

    def resolution(self):
        return self._resolution

    # Tests
    def isCell(self, x, y, state):
        return ( self.cell(x, y) == state )
    
    # Construction
    def setGrid(self, aGrid): 
        self._grid= aGrid
        self._height= len(self._grid)
        return self

    def setCell( self, x, y, state ):
        dy= self._height-1-y
        self._grid[dy][x]= state
        return self

    # Boxing
    def box(self, x, y):
        state= self.cell(x, y)
        width, height= self.dimention()
        x2= x+1
        y2= y+1
        xOk, yOk= True, True
        while xOk or yOk :
            xOk= xOk and x2 < width
            for iy in range( y, y2 ) :
                xOk= xOk and (self.cell( x2, iy ) == state)
            if xOk :
                x2+= 1
            yOk= yOk and y2 < height
            for ix in range( x, x2 ) :
                yOk= yOk and (self.cell( ix, y2 ) == state)
            if yOk :
                y2+= 1
        return [x, y, x2, y2]

    def search(self, state=0):
        x, y= 0, 0
        width, height= self.dimention()
        while y < height and self.cell(x, y) != state :
            x+= 1
            if x == width :
                x=0
                y+=1
        if y == height :
            return False
        return (x, y)
    
    def setBoxOn(self, box, state ):
        bx1, by1, bx2, by2= tuple(box)
        for ix in range( bx1, bx2 ):
            for iy in range( by1, by2 ):
                self.setCell(ix, iy, state)
        return self

    def makeBoxes(self, state=0):
        pos= self.search(state)
        boxes= []
        while pos :
            x, y= pos
            box= self.box(x, y)
            self.setBoxOn( box, -1 )
            boxes.append( box )
            pos= self.search(state)
        
        for box in boxes :
            self.setBoxOn(box, state)
        return boxes

    # Shaping
    def boxToShape(self, box):
        r= self.resolution()
        epsilon= r/4.0
        ox, oy= self.position()
        bx1, by1, bx2, by2= tuple(box)
        sx1= ox + bx1*r + epsilon
        sy1= oy + by1*r + epsilon
        sx2= ox + bx2*r - epsilon
        sy2= oy + by2*r - epsilon
        print( f"vars:{(ox, oy, r)} - {box} - {(sx1, sy1)} {(sx2, sy2)}" )
        return Shape().fromZipped( [(sx1, sy1), (sx1, sy2), (sx2, sy2), (sx2, sy1)] )

    def makeShapes(self, state=0):
        boxes= self.makeBoxes(state)
        shapes= [ self.boxToShape(box) for box in boxes ]
        return shapes

class GridMapStat(GridMap) :

    def __init__(self, states= ['Free', 'Occupied', 'Unknown'], position=(0.0, 0.0), resolution=0.5):
        super().__init__(states, position, resolution)
        self._occupied= 0.8
        self._free= 0.2
   
    def occupiedTreshold(self):
        return self._occupied        
    
    def freeTreshold(self):
        return self._free
    
    def load( self, path, file ):
        config= {}
        with open( path+"/"+file, "r") as file:
            # Charger le contenu du fichier en tant que dictionnaire Python
            config = yaml.safe_load( file )

        assert config['mode'] == "trinary"
        assert config['negate'] in [0, False]

        image = cairo.ImageSurface.create_from_png( path+"/"+ config['image'] )
        
        origin= config['origin']
        self._position= (origin[0], origin[1])
        self._resolution= config['resolution']
        self._occupied= config['occupied_thresh']
        self._free= config['free_thresh']
    
        # build the grid :
        assert image.get_format() == cairo.Format.RGB24
        height= image.get_height()
        stride= image.get_stride()
        memoryview = image.get_data()

        # build the grid
        newGrid= []
        for iLine in range(height) :
            newGrid.append( [] )
            for iCol in range(0, stride, 4) :
                i= iLine*stride+iCol
                pix= memoryview[i] + memoryview[i+1] + memoryview[i+2]
                pix/= 3
                status= round( (255.0 - pix) / 255.0, 3 )
                newGrid[iLine].append( status )
        
        # Update self grid
        self.setGrid(newGrid)
        return self
    
    def cellIsFree(self, x, y):
        return (self.cell(x, y) <= self._free)

    def cellIsOccupied(self, x, y):
        return (self.cell(x, y)  >= self._occupied)

    def cellIsUncertain(self, x, y):
        return (not self.cellIsFree(x, y) and not self.cellIsOccupied(x,y))
    
    # Morphing
    def asGridMap(self):
        # Build a [Free(0), Occupied(1), Unknown(2)] map
        width, height = self.dimention()
        fouMap= []
        for iLine in range(height) :
            fouMap.append( [] )
            for iCol in range(width) :
                status= self._grid[iLine][iCol]
                if status >= self._occupied :
                    fouMap[iLine].append( 1 )
                elif status <= self._free :
                    fouMap[iLine].append( 0 )
                else :
                    fouMap[iLine].append( 2 )
        
        gm= GridMap(['Free', 'Occupied', 'Unknown'], self._position, self._resolution)
        gm.setGrid( fouMap )

        return gm