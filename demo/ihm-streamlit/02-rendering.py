"""
# Simple Tabletop rendering using streamlit.
"""
import streamlit as st
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

# Connect all close enough tiles: 
tabletop.connectAllDistance( 1.2 )

# Add some objects on the tabletop:
def newAgent( identifier, group ):
    return tll.Agent( identifier, group, shape=tll.Convex().initRegular(0.7, 6) )

tabletop.setAgentFactory( newAgent )

bod= tabletop.popAgentOn(9)
bod.setId(1).setMatter(13)

bod= tabletop.popAgentOn(14)
bod.setId(2).setMatter(15)

bod= tabletop.popAgentOn(26)
bod.setId(3).setMatter(13)

# Create an artist to render this tabletop:
pablo= tll.createArtistSVG( filePath= "shot-web-rendering.svg" )
pablo.fitBox( tabletop.box() )
tabletop.renderOn(pablo)

# Rendering in a streamlit widget
widget= st.empty()
widget.write( pablo.render(), unsafe_allow_html=True )

pablo.flip()
