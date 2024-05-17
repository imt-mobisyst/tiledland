#!env python3
import pyConvexMap as cmap
from pyConvexMap.cairo import Frame

import sys, pygame

def main():
    # Define a world
    #world= mbm.World()
    #world.spoon( mbm.Body( mbm.Point(4.5, 2.2), mbm.Point(0.4, 0.2), 0.2 ) )

    # Set-up an IHM
    ihm= Frame()
    #ihm= loupe.Loupe( world )

    # Start
    process( ihm )

def process( frame, width=1200, height=800 ):
    pygame.init()
    pygame.display.set_mode((width, height))
    pygame.display.set_caption('ConvexCell-NavMap')
    screen = pygame.display.get_surface()

    body= cmap.Pose2( 4.5, 2.2, 0.2 )
    #transform= cmap.Pose2( mbm.Point(4.5, 2.2), mbm.Point(0.4, 0.2), 0.2 )
    #bod.speed= 1.0
    #bod.drift= 0.4
    #bod.rotate= 0.2

    while True:
        # Create PyGame surface from Cairo Surface
        frame.initializeSurface(width, height)
        frame.drawPose( body )
        frame.drawFrame()

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
        else:
            print(event)

if __name__ == "__main__":
    main()