import tiledland.game.pickndel as pnd

world= pnd.World().initializeGrid([
        [00, 00, 00, 00],  # 1  2  3  4
        [-1, 00, -1, -1],  #    5      
        [00, 00, 00, 00],  # 6  7  8  9
        [00, -1, -1, 00]   #10       13
    ])

master= pnd.GameMaster( world, tic=25 )
bot= pnd.player.ShellPlayer()

master.testPlayer( bot, 1 )
