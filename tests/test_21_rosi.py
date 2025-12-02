# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import rosi
import yaml, os.path

# ------------------------------------------------------------------------ #
#         T E S T   R O S I :   R O S 2   I N T E R F A C E
# ------------------------------------------------------------------------ #

def test_load_map_metadata():
    rscPath= "tests/rsc/"
    mapName= "testmap"
    # Open map meta data file
    with open( rscPath+mapName+".yaml", 'r' ) as file:
        mapFile= file.read()
    print( f"---\n{mapFile}." )
    
    assert mapFile == """image: "testmap.png"
resolution: 0.1
origin: [2.0, 3.0, 1.0]
occupied_thresh: 0.65
free_thresh: 0.196
negate: 0
mode: "trinary"
"""
    # Read map meta data YAML file
    with open( rscPath+mapName+".yaml", 'r' ) as file:
        data = yaml.safe_load(file)

    print(data)
    assert data == {
        'image': "testmap.png",
        'resolution': 0.1,
        'origin': [2.0, 3.0, 1.0],
        'occupied_thresh': 0.65,
        'free_thresh': 0.196,
        'negate': 0,
        'mode': "trinary"
    }
    
    assert data["image"] == mapName+".png"
    assert os.path.isfile( rscPath+data["image"] )

def test_load_map_data():
    assert False