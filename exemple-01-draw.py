#!env python3
import shapely
import shapely.coordinates
import src.tiledMap.view.pygameView as timView
#import src.tiledMap.view.cairoView as timView

class Scenario :
    def __init__(self):
        self.point= ( 4.5, -2.2)
        self.seg= [( 7.5, -3.2), ( 22.5, 12.2) ]
        self.poly= shapely.Polygon( [(1, 2), (3, 4), (2, 6), (4, 8), (5, 5), (4, 0)] )

    def process( self, frame ):
        frame.drawPoint( (0, 0) )
        frame.drawPoint( self.point )
        frame.drawLine( (0, 0), self.point )
        frame.drawLine( self.seg[0], self.seg[1] )
        frame.drawCircle( self.point, 12.0 )
        frame.drawPolygon( shapely.get_coordinates(self.poly) )
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