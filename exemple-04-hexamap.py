#!env python3
import math

#import src.tiledMap as tim
import tiledMap as tim

#import src.tiledMap.view.pygameView as timView
#import tiledMap.view.pygameView as timView
#import src.tiledMap.view.cairoView as timView
import tiledMap.view.cairoView as timView

import shapely

def main():
    # Set-up an IHM
    ihm= timView.Frame()
    game= Scenario()

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

class Scenario :
    def __init__(self):
        self._map= tim.Map()
        up_x= math.cos( math.pi/3 )
        up_y= math.sin( math.pi/3 )
        assert( self._map.addTile( tim.Tile([(3,1), (5,1), (5,3), (3,3)]) ) == 0 )
        assert( self._map.addNewTile( (12, 2) ) == 1 )
        assert( self._map.addNewTile( (13, 2) ) == 2 )
        assert( self._map.addNewTile( (12+up_x, 2+up_y) ) == 3 )
        
    def process( self, frame ):
        frame.initBackground()
        frame.drawFrameGrid()

        for tile in self._map.tiles() :
            frame.drawTile( tile )
        
        return True

if __name__ == "__main__":
    main()

    