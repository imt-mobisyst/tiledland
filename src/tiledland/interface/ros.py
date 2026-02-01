#----------------------------------------------------------#
# 
# 
#----------------------------------------------------------#
from ..geometry import Point, Grid
import yaml, cairo

def loadGrid() :
    return Grid()

class GridMap :
    # Initialization
    def __init__(self, position= (0.0, 0.0), resolution=0.5):
        self._grid= [[0]]
        self._position= position
        self._resolution= resolution
        self._occupied= 0.8
        self._free= 0.2

    # Accessors
    def grid(self):
        return self._grid
    
    def dimention(self):
        return ( len(self._grid[0]), len(self._grid) )
    
    def position(self):
        return self._position

    def resolution(self):
        return self._resolution

    def occupiedTreshold(self):
        return self._occupied        
    
    def freeTreshold(self):
        return self._free

    # File managment
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
        self._grid= []
        for iLine in range(height) :
            self._grid.append( [] )
            for iCol in range(0, stride, 4) :
                i= iLine*stride+iCol
                pix= memoryview[i] + memoryview[i+1] + memoryview[i+2]
                pix/= 3
                status= round( (255.0 - pix) / 255.0, 3 )
                self._grid[iLine].append( status )
        # out
        return self
    
    def cellIsFree(self, x, y):
        return (self.cell(x, y) <= self._free)

    def cellIsOccupied(self, x, y):
        return (self.cell(x, y)  >= self._occupied)

    def cellIsUncertain(self, x, y):
        return (not self.cellIsFree(x, y) and not self.cellIsOccupied(x,y))
    
    # Morphing
    def asStatesGrid(self):
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
        return fouMap
    
    def asTllGrid(self):
        px, py= self.position()
        return Grid(
            self.asStatesGrid(),
            Point(px, py),
            self.resolution()
        )