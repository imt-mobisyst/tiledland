# Land and Actors - An introduction to Agent-Modeling

A _Land_ is a supper-object that integrate a model of an environnement (a tabletop with all thes tiles and entities its includes) linked to an agents collections. 

### Simple land with one simple actor: (agent + one body to control)

```python
import tiledland as tild

# Land defnition
land= tild.Land()
land.tabletop().initHexa(
    [[-1, 0, 0, 0], 
    [0, 0, 0, 0], 
    [-1, 0, 0, 0]], 1.4
)

# Population
land.popSimpleActor( tild.Agent(), 4 )
land.popSimpleActor( tild.Agent(), 7 )

# Draw the land's tabletop:
tild.draw( land.tabletop(), "shot-demo.png", 800, 600 )
print( f"You can open now the './shot-demo.png' file." )
```

### Bank of entiries: 

```python
import tiledland as tild

# Land defnition
land= tild.Land()
land.tabletop().initHexa(
    [[-1, 0, 0, 0], 
    [0, 0, 0, 0], 
    [-1, 0, 0, 0]], 1.4
)

bank= [
    tild.Entity( 0, tild.Convex().initArrowTip(0.6), orientation= 0.8,  name= "x" ),
    tild.Entity( 1, tild.Convex().initSquare(0.8), orientation= 0.6,  name= "A" ),
    tild.Entity( 2, tild.Convex().initRegular(0.4, 8), name= "B" )
]
land.setBankOfEntities(bank)

# Population
land.appendActor( tild.Agent(), [4, 8], [1, 1] )

ia= land.appendActor( tild.Agent())
land.popActorBody( ia, 3, 2 )
land.popActorBody( ia, 7, 2 )

land.popActorBody( 0, 5, 0 )
land.popActorBody( 0, 6, 0 )


# Draw the land's tabletop:
tild.draw( land.tabletop(), "shot-demo.png", 800, 600 )
print( f"You can open now the './shot-demo.png' file." )
```
