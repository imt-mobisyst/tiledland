# TiledLand: Polygon-based simulation engine.

The main idea is to model a plan world (a land) as a collection of convex-polygons objects : tiles.
Then, the land is mainly composed of an environnement - interconnected tiles - and agents distributed inside it.

To notice that, _TiledLand_ is more a sandbox project to test approaches than an optimized, ready-to-use and well documented toolbox.

- On github: [imt-mobisyst/tiledland](https://github.com/imt-mobisyst/tiledland)
- On PyPip: [projct tiledland](https://pypi.org/project/tiledland/)
- Documentation : []()

## Install

The project is a `Python` program reling on [Cairo](https://pypi.org/project/pycairo/) library for rendering example, [pyyaml](https://pypi.org/project/PyYAML) to read _yaml_ configuration files and [hacka](https://github.com/ktorz-net/hacka-py) for distributed game programming.

The project and its dependancies can be installed with pip

```sh
pip install tiledland
```


## Getting started


Then, as an exemple, the following code will generate a grid land with 3 square agents in position _9_, _14_ and _26_.
The land is then rendered as a _png_ graphic.

```python
#!env python3
import tiledland as tll

# Create a new TiledMap as a grid:
scene= tll.Sence()
scene.initializeGrid(
    [[0, 1, 1, -1, 0, 0, 0, 0],  #  -1 : means no cell at this location
    [5, -1, 0, 2, 0, -1, 5, 0],  #  0 - n : give the group identifier
    [0, 0, 0, -1, 0, 1, 1, 0],   #           of the cell to create.  
    [0, 4, 0, -1, 0, 2, 1, 6],     
    [-1, -1, 0, 0, 0, -1, -1, -1]]  
)

# Agent 1
agent= scene.popAgentOn(9)

# Agent 2
agent= scene.popAgentOn(26)
agent.setMatter(13)

# Agent 3
agent= scene.popAgentOn(14)
agent.setMatter(15)

# Create an artist to render this scene:
artist= tll.Artist().initializePNG( "shot-demo.png", 800, 600 )
artist.fitBox( scene.box() )
artist.drawScene(scene)
artist.flip() # Uptate the support and return to a blanc page.

print( f"You can open now the './{artist.support().filePath()}' file." )
```
