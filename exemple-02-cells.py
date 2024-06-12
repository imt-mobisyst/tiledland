#!env python3
from src.pyPolyMap import Point2, Cell, Body2
import src.pyPolyMap.view.pmCairo as pmView

def main():
    # Set-up an IHM
    ihm= pmView.Frame()
    game= Scenario()

    # Start
    ihm.infiniteLoop( game.process )
    #process( ihm )

class Scenario :
    def __init__(self):
        points=[ Point2(1, 2), Point2(2, 6), Point2(5, 5), Point2(4, 0), Point2(4, 8) ]
        self.cells= [
            Cell( [ points[0], points[1], points[2], points[3] ] ),
            Cell( [ points[1], points[4], points[2] ] )
        ]
        self.cells[1].setTags( [0, 0, 1] )
        self.body= Body2( 7.5, 5.2, 2.2 )

    def process( self, frame ):
        frame.initBackground()
        frame.drawFrameGrid()
        for cell in self.cells :
            frame.drawCell( cell )
        frame.drawBody( self.body )

        return True

if __name__ == "__main__":
    main()