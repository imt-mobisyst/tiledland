"""
# Simple Map rendering using streamlit.
"""
import streamlit as st
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

# Connect all close enough tiles: 
map.connectAllDistance( 1.2 )

# Add some objects on the map:
def newAgent( identifier, group ):
    return tll.Agent( identifier, group, shape=tll.Convex().initRegular(0.7, 6) )

map.setAgentFactory( newAgent )

bod= map.popAgentOn(9)
bod.setId(1).setMatter(13)

bod= map.popAgentOn(14)
bod.setId(2).setMatter(15)

bod= map.popAgentOn(26)
bod.setId(3).setMatter(13)

# Create an artist to render this map:
pablo= tll.createArtistSVG( filePath= "shot-web-rendering.svg" )
pablo.fitBox( map.box() )
map.draw(pablo)

# Rendering in a streamlit widget
widget= st.empty()
widget.write( pablo.render(), unsafe_allow_html=True )

pablo.flip()
