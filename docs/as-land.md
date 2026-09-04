# Land and Actors - An introduction to Agent-Modeling

A _Land_ is a supper-object that integrate a model of an environnement (a tabletop with all thes tiles and entities its includes) linked to an agents collections. 

### Simple land with one simple actor: (agent + one body to control)

```python
import tiledland as tll

# Land defnition
land= tll.Land()
land.tabletop().initHexa(
    [[-1, 0, 0, 0], 
    [0, 0, 0, 0], 
    [-1, 0, 0, 0]], 1.4
)

# Population
land.popSimpleActor( tll.Agent(), 4 )
land.popSimpleActor( tll.Agent(), 7 )

# Draw the land's tabletop:
tll.draw( land.tabletop(), "shot-demo.png", 800, 600 )
print( f"You can open now the './shot-demo.png' file." )
```

### Bank of entiries: 

```python
# Land defnition
land= tll.Land()
land.tabletop().initHexa(
    [[-1, 0, 0, 0], 
    [0, 0, 0, 0], 
    [-1, 0, 0, 0]], 1.4
)

bank= [
    tll.Entity( 0, Convex().initArrowTip(0.6), orientation= 0.8,  name= "A" ),
    tll.Entity( 1, Convex().initSquare(0.8), orientation= 0.6,  name= "B" ),
    tll.Entity( 2, Convex().initRegular(0.1, 8), name= "C" )
]
land.setBankOfEntities(bank)

# Population

```
