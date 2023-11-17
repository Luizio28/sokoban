class game:
    def __init__(game, playing, players,level,clock,gameover):
        game.playing:int = playing
        game.players:int = players
        game.level = level
        game.clock:int = clock
        game.gameover:bool = gameover
        
class level:
    def __init__(level,sizeI,sizeJ,ent,tile,board,entity,info,item):
        level.info = info
        level.sizeI:int = sizeI
        level.sizeJ:int = sizeJ
        level.ent = ent
        level.tile = tile
        level.board = board
        level.entity = entity
        level.item = item
        
class actor:
    def __init__(actor, typeid, name, glyph, hp, busy, fx, pos, attr, tags, stats, context, vision, items):
        actor.pos = pos
        actor.typeid = typeid
        actor.hp = hp
        actor.fx = fx
        actor.busy = busy
        actor.name = name
        actor.glyph = glyph
        actor.attr = attr
        actor.tags = tags
        actor.context = context
        actor.stats = stats
        actor.vision = vision
        actor.items = items
def_effects: list[int] = [0,0,0,0]
def_pos: list[int] = [0,0]
def_attr: list[int] = [12,12,12,12,12,12]
charstats = {"AC":10,"speed":5.0}

class itemclass:
    def __init__(itemclass, glyph, name, amount, weight, tags):
        itemclass.name = name
        itemclass.amount = amount
        itemclass.weight = weight
        itemclass.tags = tags
        itemclass.glyph = glyph
        
class tileclass:
    def __init__(tileclass, typeid, glyph, opaque, dark, tags):
        tileclass.typeid = typeid
        tileclass.glyph = glyph
        tileclass.tags = tags
        tileclass.opaque:bool = opaque
        tileclass.dark:bool = dark
def ftr_door(target):
    if "door_closed" in target.tags:
        target.tags.remove("door_closed")
        target.tags.append("door_open")
        target.glyph = 15
        target.opaque = False
        target.typeid = 0
        
class vector:
    def __init__(vector, I, J):
        vector.I: int = I
        vector.J: int = J
        
class quiz:
    def __init__(quiz, question):
        quiz.question = question

