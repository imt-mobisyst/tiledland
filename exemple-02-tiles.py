#!env python3
import tiledMap as tim
#import src.tiledMap.view.pygameView as timView
import src.tiledMap.view.cairoView as timView
def main():
    # Set-up an IHM
    ihm= timView.Frame()
    game= Scenario()

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

class Scenario :
    def __init__(self):
        points=[ (1, 2), (2, 6), (5, 5), (4, 0), (4, 8) ]
        self.tiles= [
            tim.Tile( [ points[0], points[1], points[2], points[3] ] ),
            tim.Tile( [ points[1], points[4], points[2] ] )
        ]
        self.tiles[1].setTags( [0, 0, 1] )
        #self.body= Body2( 7.5, 5.2, 2.2 )

    def process( self, frame ):
        frame.initBackground()
        frame.drawFrameGrid()
        for tile in self.tiles :
            frame.drawTile( tile )
        #frame.drawBody( self.body )

        return True

if __name__ == "__main__":
    main()