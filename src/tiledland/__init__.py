from .geometry import Point, Polygon, Box
from .oldgeometry import Shape
from . import agent, tile, scene, artist
from .shaped import Shaped

# Geometry:
#Point= Point
Float2= Point
#Shape= Polygon

Shape= Shape

# Geometry:
Tile= tile.Tile
Scene= scene.Scene
Agent= agent.Agent

# Artist:
SupportVoid= artist.support.SupportVoid
SupportSVG= artist.support.SupportSVG
SupportPNG= artist.supportCairo.SupportPNG
Artist= artist.Artist
