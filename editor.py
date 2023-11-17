#level editor

from definitions import *
from draw import *
import pickle
from func_ent import *

x = 81
y = 21

boundsI = [y,-1]
boundsJ = [x,-1]

pos = [0,0]

category = 1
selected = tiles.id['floor']

def new_level(x,y):
    
    board = [0]*(y)
    for i in range(0,len(board)):
        board[i] = [""]*x   

    level_board = [0]*(y)
    for i in range(0,len(level_board)):
        level_board[i] = [copy(tiles.id['nothing'])]*x

    ent_board = [0]*(y)
    for i in range(0,len(ent_board)):
        ent_board[i] = [0]*x
    
    item_board = [0]*(y)
    for i in range(0,len(item_board)):
        item_board[i] = [[0]]*x

    visScreen=[]
    board_updates = []
    vision = [0]*(y)
    for i in range(0,len(vision)):
        vision[i] = [0]*x

    for i in range(0,len(vision)):
        for j in range (0,len(vision[i])):
            vision[i][j] = objects.vector(i,j)


    #load level graphics  
    for i in range (0,len(board)):
        for j in range (0,len(board[i])):
            board[i][j] = glyph[level_board[i][j].glyph]

    return objects.level(y,x,ent_board,level_board,board,[],{},item_board)

def keys(a):
    global pos
    global category
    
    if a == "up":
        pos[0] -= 1
    if a == 'down':
        pos[0] += 1
    if a == "left":
        pos[1] -= 1
    if a == 'right':
        pos[1] += 1
        
    if a == 's':
        save()
    if a == 'c':
        change()
    if a == 'p':
        place()
        
    if a == '1':
        category = 1
    if a == '2':
        category = 2
    if a == '3':
        category = 3
        
def change():
    global selected
    chc = input('tile name: ')
    if category == 1:
        try:
            selected = tiles.id[chc]
        except: pass
    if category == 2:
        try:
            selected = monsters.id[chc]
        except: print('ERR')
    if category == 3:
        try:
            selected = items.id[chc]
        except: print('ERR')
def place():
    if category == 1:
    
    #dealing with bars
        if selected == tiles.id['nothing'] and dungeon.level.tile[pos[0]][pos[1]] == tiles.id['bars']:
            dungeon.level.info['bars'].remove([pos[0],pos[1]])
        if selected == tiles.id['bars']:
            dungeon.level.info['bars'].append([pos[0],pos[1]])
    #dealig with sokoban
        if selected == tiles.id['nothing'] and dungeon.level.tile[pos[0]][pos[1]] == tiles.id['sokoban']:
            dungeon.level.info['soko'] -= 1
        if selected == tiles.id['sokoban']:
            dungeon.level.info['soko'] += 1
            
        dungeon.level.tile[pos[0]][pos[1]] = copy(selected)
        ed_update(pos[0],pos[1])
    try:
        if category == 2:
            dungeon.level.ent[pos[0]][pos[1]] = copy(selected)
            if selected != monsters.id['null']:
                ent_displace(dungeon.level.ent[pos[0]][pos[1]],pos[0],pos[1])
            ed_update(pos[0],pos[1])
    except: print('ERR')   
    if category == 3:
        if selected == items.id['null']:
            if dungeon.level.item[pos[0]][pos[1]][-1] != 0: del dungeon.level.item[pos[0]][pos[1]][-1]
        else:
            dungeon.level.item[pos[0]][pos[1]].append(copy(selected))
        ed_update(pos[0],pos[1])
    
def save():
    os.system(screenflush)
    a = input('level name: ')
    b = input('StartI: ')
    c = input('StartJ: ')
    dungeon.level.info['start'] = [int(b),int(c)]
    dir = open('levels/'+a+'.rog','wb')
    pickle.dump(dungeon.level,dir)
    dir.close()
    
def loadlev(a):
    dir = open('levels/'+a+'.rog','rb')
    load = pickle.load(dir)
    dir.close()
    return load

def ed_update(i,j):
    board[i][j] = glyph[level_board[i][j].glyph]
    if item_board[i][j][-1] != 0: board[i][j]: char = glyph[item_board[i][j][-1].glyph]
    if ent_board[i][j] != 0: board[i][j]: char = glyph[ent_board[i][j].glyph]
    
def draw_ed():    
    render.console_cursor("hide")
    for i in range(0,y):
        for j in range(0,x):
            render.drawglyph(i,j,board[i][j])

dungeon = objects.game(0,0,'',-1,False)

while True:
    choice = input("n) New level\nl) Load level from file\n\n> ")
    os.system(screenflush)
    if choice == 'n':
        dungeon.level = new_level(81,24)
        dungeon.level.info['start'] = [0,0]
        dungeon.level.info['soko'] = 0
        dungeon.level.info['bars'] = []
        break
    if choice == 'l':
        name = input('level name: ')
        dungeon.level = loadlev(name)
        break
        
board = dungeon.level.board
level_board = dungeon.level.tile
ent_board = dungeon.level.ent
item_board = dungeon.level.item
draw_ed()



bindingsED = ['up','down','left','right','p','1','2','3','4','r','s','c']

pos = dungeon.level.info['start']
render.setcursor(pos[0],pos[1])
render.console_cursor('show')
while True:
    keypress = keyboard.read_event(suppress=True)
    if keypress.name in bindingsED and keypress.event_type == keyboard.KEY_DOWN:
        keys(keypress.name)
        draw_ed()
        render.console_cursor('show')
        print(pos,category,selected,dungeon.level.board[pos[0]][pos[1]][-1])
        render.setcursor(pos[0],pos[1])