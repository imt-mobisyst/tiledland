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
        t1= tim.Tile( [(3,1), (5,1), (5,3), (3,3)] )
        t2= tim.Tile( [(3,4), (5,4), (4,6)] )
        self._joint= tim.Joint( t1, t2, 2, 0 )

    def process( self, frame ):
        frame.initBackground()
        frame.drawFrameGrid()
        
        frame.drawJoint( self._joint )
        frame.drawTile( self._joint.tileA() )
        frame.drawTile( self._joint.tileB() )

        return True

if __name__ == "__main__":
    main()

    