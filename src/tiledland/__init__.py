from .geometry import Point, Polygon, Box
from .shaped import Shaped
from .tile import Tile
from .agent import Agent
from .scene import Scene
from . import artist

# Artist:
SupportVoid= artist.support.SupportVoid
SupportSVG= artist.support.SupportSVG
SupportPNG= artist.supportCairo.SupportPNG
Artist= artist.Artist
