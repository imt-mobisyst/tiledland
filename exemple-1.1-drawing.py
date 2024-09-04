#!env python3
from tiledLand.geometry import Coord2
import tiledLand.interface as tili

class Scenario :
    def __init__(self):
        self.p0= Coord2()
        self.p1= Coord2(4.5, -2.2)
        self.p2= Coord2(14.5, 5.2)
        self.p3= Coord2(-2.5, 6.2)
        self.seg= [ Coord2(7.5, -3.2), Coord2(22.5, 12.2) ]
        self.poly1= [ 
            Coord2(1, 2), Coord2(3, 4), Coord2(2, 6),
            Coord2(4, 8), Coord2(5, 5), Coord2(4, 0)
        ]
        self.poly2= [ 
            Coord2(5, 2), Coord2(6, 3), Coord2(7.5, 4),
            Coord2(7, 8), Coord2(8, 5), Coord2(7, 0)
        ]
        self.poly3= [ 
            Coord2(-1, 2), Coord2(-2, -3),
            Coord2(-5, -2), Coord2(-4, 0)
        ]
    def process( self, frame ):
        frame.tracePoint( self.p0 )
        frame.tracePoint( self.p1 )
        frame.traceLine( self.p1, self.p0 )
        frame.traceLine( self.seg[0], self.seg[1] )
        frame.traceCircle( self.p1, 12.0 )

        frame.fillCircle( self.p2, 2.0 )
        frame.drawCircle( self.p3, 1.4 )

        frame.tracePolygon( self.poly1 )
        frame.fillPolygon( self.poly2 )
        frame.drawPolygon(
            self.poly3,
            tili.Rgb(1.0, 0.5, 0.3),
            tili.Rgb(0.8, 0.1, 0.1)
        )

        frame.drawFrameAxes()
        
        return True

def main():
    # Set-up an IHM
    ihm= tili.Interface()
    game= Scenario()

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

if __name__ == "__main__":
    main()