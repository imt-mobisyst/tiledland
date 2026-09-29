# Desktop Interface

TiledLand provides the spatial model and rendering, but does not deliver a ready-to-use desktop window or event loop. Integration into an interface is the responsibility of the application.

## Recommended Organization

1. Keep a tabletop and simulation rules within the model.
2. Transform interface events into explicit commands.
3. Apply these commands to the model.
4. Regenerate a render after modification.

An SVG or PNG export is a first way to visually control the scene. For continuous interaction, provide a display component suited to the chosen toolkit. No Tkinter, Qt, or Pygame adapter is documented here as a feature provided by TiledLand.

## From Click to Action

Click coordinates are screen coordinates. They must be converted to world coordinates before selecting an area. The `Artist` framing introduces a scale and an offset: do not use pixels directly as simulation positions.

To avoid inconsistencies during movements, centralize tabletop modifications into a single loop. See [execution and concurrency](ihm-thread.md).
