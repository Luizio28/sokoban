from actions import *

keys_directions = {"1":"1;-1","2":"1;0","3":"1;1","4":"0;-1","6":"0;1","7":"-1;-1","8":"-1;0","9":"-1;1","up":"-1;0","down":"1;0","left":"0;-1","right":"0;1"}

def pc_listen():
    while True:
        keypress = keyboard.read_event(suppress=True)
        if keypress.name in bindings and keypress.event_type == keyboard.KEY_DOWN:
            dungeon.level.entity[dungeon.playing].context = ""
            impulse(bindings[keypress.name])
            refresh()
            break

def verbose():
    render.print_line(y+2,0,"# ",81)
    render.setcursor(y+2,2)
    vrb_cmd = input()
    impulse(str(vrb_cmd))
    
def impulse(a):
    char = dungeon.level.entity[dungeon.playing]
    
    if a == "north":
        action_walk(-1,0)
    if a == "east":
        action_walk(0,-1)
    if a == "south":
        action_walk(1,0)
    if a == "west":
        action_walk(0,1)
    if a == "southwest":
        action_walk(1,1)
    if a == "northwest":
        action_walk(-1,1)
    if a == "southeast":
        action_walk(1,-1)
    if a == "northeast":
        action_walk(-1,-1)
        
    if a == "wait":
        char.context += "Time passess... "
    if a == "rest":
        char.fx[0] += 100+dice(2,100)
        char.context += "You fall asleep... "
    if a == "push":
        drct = listen_direction()
        if drct[2] == True:
            action_push(char,drct[0],drct[1])
    if a == "pick":
        action_pick(char,char.pos[0],char.pos[1])
    if a == "hurt":
        hurt(char,char,dice(1,4),'suicide')
    if a == "bindings":
        char.context += "Bound keys: " + str(bindings) + " "
        refresh()
    if a == "dungeon.gameover":
        dungeon.gameover = True
    if a == "menu_verbose":
        verbose()
        refresh()
    if a == "die":
        hurt(char,char,100,'suicide')
    if a == "add_pc":
        spawn_pc()
    if a == "add_npc":
        spawn_npc()
        
def listen_direction():
    ok = True
    
    i = 0
    j = 0
    render.print_line(y+2,0,"What direction?",81)
    render.setcursor(dungeon.level.entity[dungeon.playing].pos[0]+1,dungeon.level.entity[dungeon.playing].pos[1])
    while True:
        keypress = keyboard.read_event(suppress=True)
        if keypress.event_type == keyboard.KEY_DOWN and keypress.name in keys_directions:
            break
    drct = keys_directions[keypress.name].rsplit(";")
    i = int(drct[0])
    j = int(drct[1])
    return [i,j,ok]

