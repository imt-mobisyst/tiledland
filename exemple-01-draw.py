#!env python3
from src.tiledMap import Point2, Segment
#import src.tiledMap.view.pmPygame as pmView
import src.tiledMap.view.pmCairo as pmView

class Scenario :
    def __init__(self):
        self.point= Point2( 2.5, -0.2)
        self.seg= Segment( Point2( 7.5, -3.2), Point2( 22.5, 12.2) )

    def process( self, frame ):
        zero= Point2()
        frame.drawPoint( zero )
        frame.drawPoint( self.point )
        frame.drawLine( zero, self.point )
        frame.drawLine( self.seg.pointA(), self.seg.pointB() )
        frame.drawCircle( self.point, 12.0 )
        frame.drawFrameAxes() 
        
        return True

def main():
    # Set-up an IHM
    ihm= pmView.Frame()
    game= Scenario()

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

if __name__ == "__main__":
    main()