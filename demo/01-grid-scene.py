#!env python3
import tiledland as tll

# Create a new TiledMap as a grid:
map= tll.Map()
map.initGrid(
    [[0, 1, 1, -1, 0, 0, 0, 0],              #  -1 : means no cell at this location
    [5, -1, 0, 2, 0, -1, 5, 0],              #  0 - n : give the group identifier of the cell to create.
    [0, 0, 0, -1, 0, 1, 1, 0],               #  
    [0, 4, 0, -1, 0, 2, 1, 6],               #  
    [-1, -1, 0, 0, 0, -1, -1, -1]]           #  
)

# Agent 1
agent= map.popAgentOn(9)

# Agent 2
agent= map.popAgentOn(26)
agent.setMatter(13)

# Agent 3
agent= map.popAgentOn(14)
agent.setMatter(15)

# Create an artist to render this map:
anArtist= tll.createArtistPNG( "shot-demo.png", 800, 600 )
anArtist.fitBox( map.box() )
map.renderOn(anArtist)
anArtist.flip() # Uptate the support and return to a blanc page.

print( f"You can open now the './{anArtist.support().filePath()}' file." )
