import sys, json, tiledland.game.pickndel as pnd

# Game Configutration :
conf= {
    "conf": "default",
    "grid": [
        [ 0,  0],  # 1  2  
        [ 0,  0]   # 3  4
    ],
    "encumbers": [
        [ 3 ],
        [0.6]
    ],
    "tic": 12
}

if len( sys.argv ) > 1 :
    fileDsc= open( f"./{sys.argv[1]}" )
    conf= json.load(fileDsc)
    fileDsc.close()

for k in conf: 
    valueStr= str( conf[k] )
    if len( valueStr ) > 42 :
        valueStr= valueStr[:38] + "..."
    print( f"- {k}: {valueStr}" )

world= pnd.World( conf["conf"] ).initializeGrid( conf["grid"], encumbers=conf["encumbers"] )

master= pnd.GameMaster( world, tic=conf["tic"] )
bot= pnd.player.ShellPlayer()

master.testPlayer( bot, 1 )
