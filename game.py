from commands import *



def turn_pass(): 
    turnTaken = 0
    
    while True:
        char = dungeon.level.entity[dungeon.playing]
        dungeon.clock += 1
        while True:
            #this marks the end of the round
            if dungeon.playing > len(dungeon.level.entity)-1:
                dungeon.playing = 0
                break
            char = dungeon.level.entity[dungeon.playing]
            #check effects    
            ent_checkfx()
            
            
            if char.typeid == 1:
                char.busy -= 1
                if turnTaken != dungeon.playing and dungeon.players > 1:
                    render.print_line(y+2,0,attr('reverse')+"* It is now "+glyph[char.glyph]+char.name+"'s turn."+attr('res_reverse'),81)
                    input()
                refresh()
                pc_listen()
                turnTaken = dungeon.playing
                #refresh in multiplayer, to see the action
                if dungeon.players > 1:
                    refresh()
            else:
                pass
            dungeon.playing += 1
            if quizstart.question == []: 
                dungeon.gameover = True
                flairend = "Todas as questões feitas! "
        if dungeon.gameover == True:
            break


spawn_pc()
  
while True:
		#refresh()
		if dungeon.gameover == True:
			input(flairend)
			break
		turn_pass()
