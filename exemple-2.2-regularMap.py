#!env python3
import math

#import src.tiledLand as tim
import src.tiledLand as til
import tiledLand.cutout.cairoView as timView

import shapely

def main():
    # Set-up an IHM
    ihm= timView.Frame()
    
    map1= til.Map().setSquareGrid(
        [
            [1,1,1,1,1,0,1,1,0,0],
            [1,0,1,1,1,0,1,1,1,1],
            [1,0,0,0,1,1,1,1,0,0],
            [1,1,1,1,1,1,1,1,0,0],
            [1,1,0,0,0,1,0,1,0,0]
        ],
        til.Coord2(0.8, 1.0), 1.0
    )

    map2= til.Map().setHexaGrid(
        [
            [1,1,1,1,1,0,1,1,0,0],
             [1,0,1,1,1,0,1,1,1,1],
            [1,0,0,0,1,1,1,1,0,0],
             [1,1,1,1,1,1,1,1,0,0],
            [1,1,0,0,0,1,0,1,0,0]
        ],
        til.Coord2(12.8, 1.0), 1.0
    )

    game= Scenario( [map1, map2] )

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

class Scenario :
    def __init__(self, maps):
        self._maps= maps
        
    def process( self, frame ):
        frame.initBackground()
        frame.drawFrameGrid()

        for map in self._maps :
            frame.drawMap( map )

        return True

if __name__ == "__main__":
    main()

    