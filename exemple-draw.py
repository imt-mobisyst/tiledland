#!env python3
import pyPolyMap as cmap
from pyPolyMap.cairo import Color, Frame

import sys, pygame

def main():
    # Set-up an IHM
    ihm= Frame()

    # Start
    process( ihm )

def process( frame, width=1200, height=800 ):
    pygame.init()
    screen= pygame.display.set_mode( (width, height), pygame.RESIZABLE )
    pygame.display.set_caption('ConvexCell-NavMap')

    point= cmap.Point2( 2.5, -0.2)
    seg= cmap.Segment( cmap.Point2( 7.5, -3.2), cmap.Point2( 22.5, 12.2) )
    cell= cmap.Cell( [cmap.Point2(1, 2), cmap.Point2(2, 6), cmap.Point2(5, 5), cmap.Point2(4, 0)] )
    cell.setTags( [0, 1, 0, 2] )
    body= cmap.Body2( 7.5, 5.2, 2.2 )

    #transform= cmap.Pose2( mbm.Point(4.5, 2.2), mbm.Point(0.4, 0.2), 0.2 )
    #bod.speed= 1.0
    #bod.drift= 0.4
    #bod.rotate= 0.2

    while True:
        # Create PyGame surface from Cairo Surface
        width= screen.get_width()
        height= screen.get_height()
        frame.initializeSurface(width, height)
        frame.drawFrameGrid()
        frame.drawFrameAxes()
        frame.drawBody( body )
        frame.drawPoint( point, Color() )
        frame.drawCircle(point, 12 )
        frame.drawSegment( seg )
        print( type(cell) )
        frame.drawCell( cell )

        #self._surface.write_to_png("MyImage.png")
        # Create PyGame surface from Cairo Surface
        image = pygame.image.frombuffer(
            frame._surface.get_data(), # Cairo seems to works on a BGRA suface...
            (width, height), "BGRA"
        )

        # Tranfer to Screen
        screen.blit(image, (0, 0))
        pygame.display.flip()

        input( pygame.event.get() )

        #body.process()

def input(events):
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)
        #else:
        #    print(event)

if __name__ == "__main__":
    main()