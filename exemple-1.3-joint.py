#!env python3

import src.tiledLand as til
from tiledLand.geometry import Coord2, Segment
import tiledLand.interface as tili


import shapely

def main():
    # Set-up an IHM
    ihm= tili.Interface()
    game= Scenario()

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

class Scenario :
    def __init__(self):
        t1= til.Tile().setFromCoordinates( [ Coord2(3, 1), Coord2(5,1), Coord2(5,3), Coord2(3,3) ] )
        t2= til.Tile().setFromCoordinates( [ Coord2(3,4), Coord2(5,4), Coord2(4,6)] )
        self._joint1= til.Joint(t1, t2)
        self._joint1.updateGates()

        t1= til.Tile().setFromCoordinates( [ Coord2(13,1), Coord2(15,1), Coord2(15,3), Coord2(13,3)] )
        t2= til.Tile().setFromCoordinates( [ Coord2(13,4), Coord2(15,4), Coord2(14,6)] )
        self._joint2= til.Joint(t1, t2)
        self._joint2.updateGates()

    def process( self, frame ):
        frame.drawFrameGrid()
        
        frame.drawJointShape( self._joint1 )
        frame.drawTile( self._joint1.tileA() )
        frame.drawTile( self._joint1.tileB() )

        front= self._joint1.frontiere()
        inter= til.intersection( front, Segment( self._joint1.tileA().center(), self._joint1.tileB().center() ) )
        if( inter ):
            frame.tracePoint( inter )

        frame.drawJoint( self._joint2 )
        frame.drawTile( self._joint2.tileA() )
        frame.drawTile( self._joint2.tileB() )

        return True

if __name__ == "__main__":
    main()

    