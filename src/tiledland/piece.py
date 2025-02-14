from .shape import Shape

class Piece(Shape):

    # Initialization Destruction:
    def __init__( self, name= "AA", type= 0, center= (0.0, 0.0), size= 0.5 ):
        self._name= name
        super().__init__(type, center, size)
        self.setShapeRegular( self.center(), size, 8 )

    # Accessor: 
    def name(self):
        return self._name
    
    # Construction:
    def setName(self, name):
        self._name= name
        return self
