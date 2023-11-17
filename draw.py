import os
from definitions import *

if sys.platform == 'win32': 
    import r_win32 as render
if sys.platform == 'linux': 
    import r_linux as render

angles = []
anglesteps = 0.05
flag = -1
while True:
    flag += anglesteps
    if flag >= 1:
        break
    else: angles.append(flag)

circle = [0,1,2,3]
maxvis = 5

def refresh():
    char = dungeon.level.entity[dungeon.playing]
    draw_vision(char)
    statusbar = char.name+" Vida:"+str(char.hp[0])+" Pontos: "+str(char.hp[1])
    #draw sbar
    render.print_line(y+1,0,statusbar,81)
    #draw flair
    render.print_line(y+2,0,char.context,81)
    #draw flairtop
    viscount= str(len(visScreen))
    #place cursor on main characer
    render.console_cursor("show")
    render.setcursor(char.pos[0]+1,char.pos[1])
    
def draw_board():    
    render.console_cursor("hide")
    for i in range(0,y):
        for j in range(0,x):
            render.drawglyph(i,j,board[i][j])

def cell_update(i,j):
    render.console_cursor("hide")
    render.drawglyph(i+1,j,dungeon.level.board[i][j])
    
def board_update(i,j):
    dungeon.level.board[i][j] = glyph[dungeon.level.tile[i][j].glyph]
    #if dungeon.level.item[i][j][-1] != 0: dungeon.level.board[i][j]: char = glyph[dungeon.level.item[i][j][-1].glyph]
    if dungeon.level.ent[i][j] != 0: dungeon.level.board[i][j]: char = glyph[dungeon.level.ent[i][j].glyph]
    board_updates.append(vision[i][j])
    
def draw_vision(char):
    getVis = []
    upVis = []
    noVis = []
    remVis = []
    remUps = []
    vis = 3
    selfvis = 1
    global board_updates
    
    #you can aways see yourself and around you
    for i in range (char.pos[0]-selfvis,char.pos[0]+selfvis+1):
        for j in range (char.pos[1]-selfvis,char.pos[1]+selfvis+1):  
            if i not in boundsI and j not in boundsJ:
                getVis.append(vision[i][j])
                if vision[i][j] not in visScreen:
                    visScreen.append(vision[i][j])
                    upVis.append(vision[i][j])
    #ray tracing
    for k in circle:
        for l in angles:
            x = 1
            while True:
                if k == 0:
                    i  = round(x*l+char.pos[0])
                    j  = round(x+char.pos[1])
                if k == 2:
                    i  = round(-x*l+char.pos[0])
                    j  = round(-x+char.pos[1])
                if k == 1:
                    i  = round(x+char.pos[0])
                    j  = round(x*l+char.pos[1])
                if k == 3:
                    i  = round(-x+char.pos[0])
                    j  = round(-x*l+char.pos[1])
                if i not in boundsI and j not in boundsJ:
                    if not dungeon.level.tile[i][j].opaque or not dungeon.level.tile[i][j].dark:
                        getVis.append(vision[i][j])
                        if vision[i][j] not in visScreen:
                            visScreen.append(vision[i][j])
                            upVis.append(vision[i][j])
                        if dungeon.level.tile[i][j].opaque or x == maxvis:
                            break
                    else: break
                    x+=1
                else: break
    #old ones
    for i in visScreen:
        if i not in getVis: 
            noVis.append(i)
            remVis.append(i) 
    #board updates
    for i in board_updates:
        if i in getVis:
            upVis.append(i)
    #flush
    for i in remVis:
        visScreen.remove(i)
    board_updates = []
    #finally, draw
    for i in upVis:
        cell_update(i.I,i.J)
    for i in noVis:
        cell_blank(i.I,i.J)
 
def get_vision(char):
    getVis = []
    selfvis = 1
    
    #you can aways see yourself and around you
    for i in range (char.pos[0]-selfvis,char.pos[0]+selfvis+1):
        for j in range (char.pos[1]-selfvis,char.pos[1]+selfvis+1):  
            if i > -1 and i < 21 and j > -1 and j < 81:
                getVis.append(vision[i][j])
    #ray tracing
    l = 1
    k = 1
    #part 1
    for m in circle:
        for l in angles:
            x = 1
            while True:
                i  = round(x*k)*m+(char.pos[0])
                j  = round(x*l)*m+(char.pos[1])
                if i not in boundsI and j not in boundsJ:
                    if level_board[i][j].typeid != -1:
                        getVis.append(vision[i][j])
                        if level_board[i][j].typeid == 1 or "closed_door" in level_board[i][j].tags:
                            break
                    x+=1
                else:
                    break
        for k in angles:
            x = 1
            while True:
                i  = round(x*k)*m+(char.pos[0])
                j  = round(x*l)*m+(char.pos[1])
                if i not in boundsI and j not in boundsJ:
                    if level_board[i][j].typeid != -1:
                        getVis.append(vision[i][j])
                        if level_board[i][j].typeid == 1 or "closed_door" in level_board[i][j].tags:
                            break
                    x+=1
                else:
                    break 
    return getVis
    
def cell_blank(i,j):
    render.console_cursor("hide")
    render.drawglyph(i+1,j," ")
    
def visflush():
    global visScreen
    visScreen = []