#!env python3
import tiledland as tild

# Create a new Land:
land= tild.Land()
land.tabletop().initHexa(
    [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
    [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
    [0, 0, 0, -1, 0, 0, 0, 0],      #  
    [0, 0, 0, -1, 0, 0, 0, 0],      #  
    [-1, -1, 0, 0, 0, -1, -1, -1]]  #
)

land.initializeArrowTipBankOfEntities( range(1, 6),
    [0.4, 0.4, 0.2, 0.8, 0.6],
    [0.0, 3.14, -1.57, 0.8, -2.6],
    ["A", "B", "C", "D", "E"] )

land.popSimpleActor( tild.Agent(), 3 )
land.popSimpleActor( tild.Agent(), 10 )
land.popSimpleActor( tild.Agent(), 12 )
land.popSimpleActor( tild.Agent(), 26 )

# Create an artist to render this tabletop:
anArtist= tild.artist.openPNG( "shot-demo.png", 800, 600 )
anArtist.fit(land)
land.renderOn(anArtist)
anArtist.flip() # Uptate the support and return to a blanc page.

print( f"You can open now the './{anArtist.support().filePath()}' file." )
