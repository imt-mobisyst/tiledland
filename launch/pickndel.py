import tiledland.game.pickndel as pnd


world= pnd.World().initializeGrid([[0, 0], [0, 0]])
master= pnd.GameMaster( world )
bot= pnd.player.ShellPlayer()

master.testPlayer( bot, 1 )
