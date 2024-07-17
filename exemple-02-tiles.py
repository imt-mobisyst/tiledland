#!env python3
import math, tiledMap as tim
#import src.tiledMap.view.pygameView as timView
import src.tiledMap.view.cairoView as timView

def regular1( center, nbFaces=4, ran=1):
    x, y= center
    return [
        (center[0]-ran, center[1]-ran),
        (x+ran, y-ran),
        (x+ran, y+ran),
        (x-ran, y+ran)
    ]

def regular2( center, nbFaces=4, ran=1):
    x, y= center
    points= []
    angle= math.pi - ((nbFaces-1)*math.pi/nbFaces)
    for i in range(nbFaces) :
        points.append( ( x+math.cos(angle)*ran, y+math.sin(angle)*ran ) )
        angle+= math.pi/(nbFaces/2)
    return points

def main():
    # Set-up an IHM
    ihm= timView.Frame()
    shapes= [
            [ (1, 2), (1.98, 5.9), (4.98, 4.9), (4, 0) ],
            [ (2, 6), (4, 8), (5, 5) ],
            [(7,1), (9,1), (9,3), (7,3)],
            [(7,4), (9,5), (7,6)],
            tim.generatePointlist_circumscribe( ( 12.5, 4.6) ),
            tim.generatePointlist_circumscribe( ( 14.5, 0), 9, 2 )
    ]
    game= Scenario( shapes )

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

class Scenario :
    def __init__(self, shapes):
        self.tiles= [
            tim.Tile( points  )
            for points in shapes
        ]
        self.tiles[1].setTags( [1, 0, 0] )
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

    