# SVG and PNG Rendering

`Artist` transforms world coordinates into image coordinates and delegates drawing to a support. SVG allows vector display; PNG uses Cairo.

## Simple Export

```python
from tiledland import Tabletop, draw

plateau = Tabletop().initGrid([[0, 1], [2, 0]])
draw(plateau, "plateau.svg", 640, 480)
draw(plateau, "plateau.png", 640, 480)
```

Dimensions are in pixels. Explicitly choose a `.svg` or `.png` extension. The export writes the indicated file and can replace an existing file.

## Rendering Control

```python
from tiledland import Tabletop, createArtistSVG

plateau = Tabletop().initLine(3)
artist = createArtistSVG("detail.svg", 800, 300)
artist.fit(plateau)
plateau.renderOn(artist)
artist.flip()
```

`fit()` adapts the framing to the object. `renderOn()` draws the elements; `flip()` finalizes the support rendering. An empty tabletop is not a good starting point for calculating framing: add tiles first.

## Colors

`Brush(fill, stroke, width)` describes the fill, the outline, and its thickness. Foreground and background palettes assign colors to groups. To customize an entity, use `setBrush()` with a new brush rather than modifying a shared brush.

```python
from tiledland import Entity, Brush, draw

objet = Entity(name="Objet")
objet.setBrush(Brush(fill=0x44AA88, stroke=0x114433, width=2))
draw(objet, "objet.svg", 400, 400)
```

To integrate the result into an application, see the [web interface](ihm-web.md) and [desktop interface](ihm-gui.md) pages.
