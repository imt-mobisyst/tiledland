#!env python3
from src.pyPolyMap import Point2, Segment
import src.pyPolyMap.pygame as pmGame

class Scenario :
    def __init__(self):
        self.point= Point2( 2.5, -0.2)
        self.seg= Segment( Point2( 7.5, -3.2), Point2( 22.5, 12.2) )

    def process( self, frame ):
        frame.initBackground()
        #frame.drawFrameGrid()
        #frame.drawFrameAxes()
        #frame.drawBody( body )
        #frame.drawCell( cell )

        zero= Point2()
        frame.drawPoint( zero )
        frame.drawPoint( self.point )
        frame.drawSegment( zero, self.point )
        frame.drawSegment( self.seg.pointA(), self.seg.pointB() )
        frame.drawCircle( self.point, 12.0 )
        
        frame.drawFrameAxes() 
        
        return True

def main():
    # Set-up an IHM
    ihm= pmGame.Frame()
    game= Scenario()

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

if __name__ == "__main__":
    main()