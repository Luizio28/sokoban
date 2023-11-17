from definitions import *
from draw import *

def spawn_pc():
    dungeon.level.entity.append(copy(monsters.id['player']))
    dungeon.level.entity[-1].name = pcName
    ent_displace(dungeon.level.entity[-1],dungeon.level.info['start'][0],dungeon.level.info['start'][1])
    genhp = 3
    dungeon.level.entity[-1].hp = [genhp,0]
    dungeon.level.entity[-1].busy = 100
    dungeon.players += 1

def spawn_npc():
    dungeon.level.entity.append(copy(monsters.id['npc']))
    ent_displace(dungeon.level.entity[-1],5,20)
    genhp = dice(1,8)+8
    dungeon.level.entity[-1].hp = [genhp,genhp]
    
def ent_checkfx():
    char = dungeon.level.entity[dungeon.playing]
    for i in range(0,3):
        if char.fx[i] != 0:
            char.fx[i] -= 1
            
    #EFFECT: Sleeping - the character is sleeping sound and cozy, in a dungeon filled with monsters.        
    if char.fx[0] != 0:
        char.busy += 1
    if char.fx[0] == 1:
        char.context += "You wake up. "

def ent_displace(target,i,j):
    oldI = target.pos[0] 
    oldJ = target.pos[1]
    
    target.pos = [i,j]
    dungeon.level.ent[oldI][oldJ] = 0
    dungeon.level.ent[i][j] = target
    board_update(i,j)
    board_update(oldI,oldJ)
    
def ent_remove(target):
    i = target.pos[0]
    j = target.pos[1]
    
    dungeon.level.ent[i][j] = 0
    try:
        dungeon.level.entity.remove(target)
    except: pass
    board_update(i,j)

def hurt(target,striker,a,mean):
    target.hp[0] -= a
    if target.hp[0] <= 0:
        kill(target,striker,mean)
    
def kill(target,striker,mean):
    if target.typeid == 1:
        dungeon.players -= 1
        if dungeon.players == 0:
            dungeon.gameover = True
        elif dungeon.players > 0:
            ent_remove(target)
    else:
        ent_remove(target)
    if dungeon.playing == len(dungeon.level.entity):
        dungeon.playing = 0
        
def ctxt_event(type,event,i,j,nohear):
    for i in range (0,len(dungeon.level.entity)):
        pass
        
def changelevel(a):
    global dungeon
    saved = dungeon.level.entity
    
    dir = open('levels/'+a+'.rog','rb')
    load = pickle.load(dir)
    dir.close()
    dungeon.level = load
    for i in saved:
        if i.typeid == 1:
            dungeon.level.entity.append(i)
            ent_displace(i,dungeon.level.info['start'][0],dungeon.level.info['start'][1])
    os.system(screenflush)
    visflush()
    refresh()