import os
import sys
import json

from colored import fg, bg, attr
import keyboard

import math
from copy import deepcopy as copy
from random import randint, choice
import pickle

from data import tiles, monsters, items, objects


if sys.platform == 'linux':
    screenflush = 'clear'
if sys.platform == 'win32':
    screenflush = 'cls'

distance:int = lambda a,b: abs(b-a) 
dice = lambda a,b: randint(a,b*a)
bonus = lambda a : (a//2)-5

flairend = "GAME OVER (Perdeu todas as vidas)"
flairtop = attr('reverse')+"pyRogue v0.0.5d"+(" "*5)+"Dungeon Rogue Episode VI: The Maze of Doom"+(" "*19)+attr('res_reverse')

#load glyphs
glyph = open("data/glyphs.txt", "r",encoding="UTF-8").read().rsplit("\n")
for i in range (0, len(glyph)):
    glyph[i] = glyph[i].rsplit(" ")
    color = fg(glyph[i][1]) + bg(glyph[i][2])
    glyph[i] = [color+glyph[i][0]+attr('reset')]
    glyph[i] = glyph[i][0]

#load bindings
bindings = {}
load_bindings = open("data/bindings.txt", "r",encoding="UTF-8").read().rsplit("\n")
for i in range (0,len(load_bindings)):
    load_bindings[i] = load_bindings[i].rsplit(" ")
    bindings[load_bindings[i][0]] = load_bindings[i][1] 

levels = {}

x = 81
y = 21

boundsI = [y,-1]
boundsJ = [x,-1]

visScreen = []

board_updates = []


vision = [0]*(y)
for i in range(0,len(vision)):
    vision[i] = [0]*x

for i in range(0,len(vision)):
    for j in range (0,len(vision[i])):
        vision[i][j] = objects.vector(i,j)

dir = open('levels/start.rog','rb')
load = pickle.load(dir)
dir.close()

dungeon = objects.game(0,0,load,-1,False)

pcName = input('Quem é você?\n>')

regist = ['keep','dungeon','cell','station1','trial','seeker']
def randomlevel():
    global regist
    global flairend
    try:
        pick = choice(regist)
        regist.remove(pick)
        
        return pick
    except:
        flairend = 'Todas as fases completadas!'
        dungeon.gameover = True

os.system(screenflush)

#quiz questions
quiz1 = json.loads(open("quiz/questions_manut.json", "r",encoding="UTF-8").read())
quiz2 = json.loads(open("quiz/questions_algor.json", "r",encoding="UTF-8").read())
quiz1 = quiz1['questions']
quiz2 = quiz2['questions']

quizstart = objects.quiz(quiz1+quiz2)