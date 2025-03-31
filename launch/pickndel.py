#!env python3 
import sys, json, tiledland.game.pickndel as pnd

# bot to test :
bot= pnd.player.ShellPlayer()
numberOfGames= 1

# Game Configutration :
conf= {
    "conf": "default",
    "grid": [
        [ 0,  0],  # 1  2  
        [ 0,  0]   # 3  4
    ],
    "tileSize": 1.0,
    "encumbers": [
        [ 3 ],
        [0.6]
    ],
    "tic": 12
}

# Load Configutration given as command argumnent :
if len( sys.argv ) > 1 :
    fileDsc= open( f"./{sys.argv[1]}" )
    conf= json.load(fileDsc)
    fileDsc.close()

for k in conf: 
    valueStr= str( conf[k] )
    if len( valueStr ) > 42 :
        valueStr= valueStr[:38] + "..."
    print( f"- {k}: {valueStr}" )

# Create game nstance :
world= pnd.World( conf["conf"] ).initializeGrid( conf["grid"], conf["tileSize"], encumbers=conf["encumbers"] )
master= pnd.GameMaster( world, tic=conf["tic"] )

# Start the numberOfGames games :
master.testPlayer( bot, numberOfGames )
