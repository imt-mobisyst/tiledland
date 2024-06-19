#!env python3
import shapely
#import src.tiledMap.view.pygameView as timView
import src.tiledMap.view.cairoView as timView

class Scenario :
    def __init__(self):
        self.point= ( 2.5, -0.2)
        self.seg= [( 7.5, -3.2), ( 22.5, 12.2) ]

    def process( self, frame ):
        frame.drawPoint( (0, 0) )
        frame.drawPoint( self.point )
        frame.drawLine( (0, 0), self.point )
        frame.drawLine( self.seg[0], self.seg[1] )
        frame.drawCircle( self.point, 12.0 )
        frame.drawFrameAxes()
        
        return True

def main():
    # Set-up an IHM
    ihm= timView.Frame()
    game= Scenario()

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

if __name__ == "__main__":
    main()