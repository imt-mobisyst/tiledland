#!env python3
import tiledland as tll

# Create a new TiledTabletop as a grid:
tabletop= tll.Tabletop()
tabletop.initGrid(
    [[0, 1, 1, -1, 0, 0, 0, 0],              #  -1 : means no cell at this location
    [5, -1, 0, 2, 0, -1, 5, 0],              #  0 - n : give the group identifier of the cell to create.
    [0, 0, 0, -1, 0, 1, 1, 0],               #  
    [0, 4, 0, -1, 0, 2, 1, 6],               #  
    [-1, -1, 0, 0, 0, -1, -1, -1]]           #  
)

# Agent 1
agent= tabletop.popAgentOn(9)

# Agent 2
agent= tabletop.popAgentOn(26)
agent.setMatter(13)

# Agent 3
agent= tabletop.popAgentOn(14)
agent.setMatter(15)

# Create an artist to render this tabletop:
anArtist= tll.createArtistPNG( "shot-demo.png", 800, 600 )
anArtist.fitBox( tabletop.box() )
tabletop.renderOn(anArtist)
anArtist.flip() # Uptate the support and return to a blanc page.

print( f"You can open now the './{anArtist.support().filePath()}' file." )
