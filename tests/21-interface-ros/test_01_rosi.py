# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tll
from src.tiledland.interface import ros
import yaml, os.path, cairo

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
    image = cairo.ImageSurface.create_from_png( "tests/rsc/testmap.png" )
    width= image.get_width()
    height= image.get_height()
    stride= image.get_stride()
    assert (width, height) == (12, 10)
    assert stride == 48 # 12*4
    assert image.get_format() == cairo.Format.RGB24 # RGBA in applicative...

    assert type(image) == cairo.ImageSurface

    pixel_data_mv = image.get_data()  # MemoryView object
    assert len(pixel_data_mv) == stride * height

    print( pixel_data_mv )
    
    # ByteArray :
    pixels_as_bytes = pixel_data_mv.tobytes()
    for i in range(10) : 
        print( pixels_as_bytes[i:i+stride] )

    # As List :
    pixels_as_list = list(pixels_as_bytes)
    assert len(pixels_as_list) == stride*height
    for i in range(10) : 
        print( pixels_as_list[i:i+stride] )

    # build the map :
    gridmap= []
    for i in range(height) :
        gridmap.append([])
        for j in range(0, stride, 4) :
            pix= i*stride+j
            assert pixel_data_mv[pix] in [0, 255]
            assert pixel_data_mv[pix+1] == pixel_data_mv[pix]
            assert pixel_data_mv[pix+2] == pixel_data_mv[pix]
            assert pixel_data_mv[pix+3] == 255
            if pixel_data_mv[pix] == 0 :
                gridmap[i].append(1)
            else :
                gridmap[i].append(0)

    assert gridmap == [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    # Modification test :
    assert pixel_data_mv[26] == 255
    pixel_data_mv[26]= 104
    assert pixel_data_mv[26] == 104
    assert pixels_as_bytes[26] == 255

def test_load_map_with_rosi():
    gridmap= ros.GridMap()

    assert gridmap.dimention() == (1, 1)
    assert gridmap.grid() == [[0.0]]
    assert gridmap.position() == (0, 0.0)
    assert gridmap.resolution() == 0.5
    assert gridmap.occupiedTreshold() == 0.8
    assert gridmap.freeTreshold() == 0.2

    gridmap.load( "tests/rsc", "testmap.yaml" )
    
    assert gridmap.position() == (2.0, 3.0)
    assert gridmap.resolution() == 0.1
    assert gridmap.occupiedTreshold() == 0.65
    assert gridmap.freeTreshold() == 0.196

    print(gridmap.grid())

    assert gridmap.dimention() == (12, 10)
    assert gridmap.grid() == [
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
        [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ]

    assert gridmap.asStatesGrid() == [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

def test_load_partialmap():
    gridmap= ros.GridMap()
    gridmap.load( "tests/rsc", "testslammap.yaml" )
    
    assert gridmap.position() == (0.0, 0.0)
    assert gridmap.resolution() == 0.2
    assert gridmap.occupiedTreshold() == 0.6
    assert gridmap.freeTreshold() == 0.2

    assert gridmap.dimention() == (14, 12)

    print(gridmap.grid())

    assert gridmap.grid() == [
        [0.004, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.004, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.82, 0.82, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.004, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.816, 0.816, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.004, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.004, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.004, 0.039, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
        [0.063, 0.094, 0.118, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.263, 0.263, 0.263, 1.0, 0.0],
        [0.118, 0.118, 0.263, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.263, 0.263, 0.263, 1.0, 0.0],
        [0.118, 0.263, 0.263, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.263, 0.263, 0.263, 1.0, 0.0],
        [0.263, 0.263, 0.263, 0.263, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
        [0.263, 0.263, 0.263, 0.263, 0.263, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ]

    assert gridmap.asStatesGrid() == [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 2, 2, 2, 1, 0],
        [0, 0, 2, 1, 0, 0, 0, 0, 1, 2, 2, 2, 1, 0],
        [0, 2, 2, 1, 1, 0, 0, 0, 1, 2, 2, 2, 1, 0],
        [2, 2, 2, 2, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0],
        [2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

