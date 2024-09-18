#!env python3
import math
from tiledLand.tile import Tile
from tiledLand.geometry import Coord2, Segment
import tiledLand.interface as tili

def main():
    # Set-up an IHM
    ihm= tili.Interface()
    
    tile2= Tile().setFromCoordinates( [ Coord2(1, 2), Coord2(1.98, 5.9), Coord2(4.98, 4.9), Coord2(4, 0) ] )
    tile2.setSegementTags( [1, 2, 3, 0] )

    tiles= [
            Tile( Coord2(13.3, 2.8) ),
            tile2,
            Tile( tag=1 ).setFromCoordinates( [ Coord2(2, 6), Coord2(4, 8), Coord2(5, 5) ] ),
            Tile( tag=2 ).setFromCoordinates( [ Coord2(7,1), Coord2(9,1), Coord2(9,3), Coord2(7,3)] ),
            Tile().setFromCoordinates( [ Coord2(7,4), Coord2(9,5), Coord2(7,6)] ),
            Tile().setSquare( Coord2(11.8, 3.4), 1 ),
            Tile().setSquare( Coord2(10.8, 5.6), 2 ),
            Tile().setRegular( 3, Coord2(18.7, 0.8), 0.4 ),
            Tile().setRegular( 9, Coord2(16.7, 4.8), 1.8 ),
            tile2.copy().moveTo( Coord2(-2.7, 3.8) )
    ]

    tiles[8].setSegementTags(
        [1, 2, 2,
         2, 2, 3,
         3, 3, 0]
    )

    game= Scenario( tiles )

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

class Scenario :
    def __init__(self, tiles):
        self._tiles= tiles

    def process( self, frame ):
        frame.drawFrameGrid()
        for tile in self._tiles :
            frame.drawTile( tile )

        return True

if __name__ == "__main__":
    main()

    