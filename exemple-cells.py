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

    points=[
        cmap.Point2(1, 2), cmap.Point2(2, 6),
        cmap.Point2(5, 5), cmap.Point2(4, 0),
        cmap.Point2(4, 8)
    ]
    cells= [
        cmap.Cell( [ points[0], points[1], points[2], points[3] ] ),
        cmap.Cell( [ points[1], points[4], points[2] ] )
    ]
    
    cells[1].setTags( [0, 0, 1] )

    while True:
        # Create PyGame surface from Cairo Surface
        width= screen.get_width()
        height= screen.get_height()
        frame.initializeSurface(width, height)
        frame.drawFrameGrid()
        for c in cells :
            frame.drawCell(c)

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