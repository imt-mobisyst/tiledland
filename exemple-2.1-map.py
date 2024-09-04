#!env python3
import math

import tiledLand as til
import tiledLand.interface as tili

def main():
    # Set-up an IHM
    ihm= tili.Interface()

    up_x= math.cos( math.pi/3 )
    up_y= math.sin( math.pi/3 )
    map1= til.Map()
    map1.addTile( til.Tile().setFromList( [(-1,7), (-3,7), (-3,9), (-1,9)] ) )        # 1
    map1.addTile( til.Tile().setRegular( 6, til.Coord2(8, 8), 1 ) )           # 2
    map1.addTile( til.Tile().setRegular( 6, til.Coord2(9, 8), 1 )  )          # 3
    map1.addTile( til.Tile().setRegular( 6, til.Coord2(8+up_x, 8+up_y), 1 ) ) # 4

    map2= til.Map()
    map2.addTile( til.Tile().setFromList( [(3,1), (5,1), (5,3), (3,3)] ) )
    map2.addTile( til.Tile().setRegular( 9, til.Coord2(12.5, 3.4), 1 ) )
    map2.addTile( til.Tile().setRegular( 3, til.Coord2(14.5, 2.4), 1 ) )

    map2.connect( 1, 2 )
    map2.connect( 2, 3 )

    game= Scenario( [map1, map2] )

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

class Scenario :
    def __init__(self, maps):
        self._maps= maps
        
    def process( self, frame ):
        frame.drawFrameGrid()

        for map in self._maps :
            frame.drawMap( map )

        return True

if __name__ == "__main__":
    main()

    