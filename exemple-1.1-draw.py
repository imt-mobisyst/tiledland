#!env python3
import shapely
import shapely.coordinates
from tiledLand.geometry import Coord2
import tiledLand.cutout.pygameView as timView
#import tiledLand.cutout.cairoView as timView

class Scenario :
    def __init__(self):
        self.point= Coord2(4.5, -2.2)
        self.seg= [ Coord2(7.5, -3.2), Coord2(22.5, 12.2) ]
        self.poly= shapely.Polygon( [(1, 2), (3, 4), (2, 6), (4, 8), (5, 5), (4, 0)] )

    def process( self, frame ):
        frame.drawPoint( Coord2(0, 0) )
        frame.drawPoint( self.point )
        frame.drawLine( Coord2(0, 0), self.point )
        frame.drawLine( self.seg[0], self.seg[1] )
        frame.drawCircle( self.point, 12.0 )
        frame.drawShapelyPolygon( self.poly )
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