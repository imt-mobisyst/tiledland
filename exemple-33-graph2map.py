#!env python3
import signal, math

from src.tiledLand import Map, Tile, Coord2
import src.tiledLand.interface as tili

def main():
    # Set-up an IHM
    ihm= tili.Interface()

    nodes= [
        Coord2(-4.0, 1.0), Coord2(-4.0, 4.0), Coord2(-3.6, 7.0),
        Coord2(-1.4, 3.0), Coord2(-1.0, 0.8), Coord2(-0.8, 5.4)
    ]
    edges= [ (1,2), (2,3), (2,4), (3,6), (4,1), (4,5), (4,6) ]
    
    map1= Map( nodes, edges,
        tileModel= Tile().setRegular( 12, Coord2(0.0, 0.0), 1 )
    )

    nodes= [
        (n.scale(1.3)+Coord2(8, -0.2)).round(2)
        for n in nodes
    ]

    map2= Map( nodes, edges,
        tileModel= Tile().setRegular( 12, Coord2(0.0, 0.0), 1 )
    )
    map2.setEdgeAsPath(0.5)

    nodes= [ n+Coord2(10.0, 0.0) for n in nodes ]
    
    map3= Map( nodes, edges,
        tileModel= Tile().setRegular( 12, Coord2(0.0, 0.0), 1 )
    )

    game= Scenario( [map1, map2, map3] )

    # Start
    signal.signal(signal.SIGINT, ihm.signalHandler_stop)
    ihm.infiniteLoop( game.process )
    #process( ihm )

class Scenario :
    def __init__(self, maps):
        self._maps= maps
        
    def process( self, frame ):
        frame.drawFrameGrid()

        for map in self._maps :
            frame.drawMap( map )

        return True

if __name__ == "__main__":
    main()
