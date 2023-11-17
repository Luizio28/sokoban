from func_ent import *

def action_walk(a,b):
    char = dungeon.level.entity[dungeon.playing]
    char_posI = char.pos[0]
    char_posJ = char.pos[1]
    
    move = [char.pos[0]+a,char.pos[1]+b]
    
    if move[0] < 0 or move[1] < 0 or move[0] > y-1 or move[1] > x-1:
        char.context += "Você não pode seguir esse caminho... "
    else:
        if dungeon.level.tile[move[0]][move[1]].typeid == 1:
            char.context += "Você bate a cara na parede. "
        
        #entity      
        elif dungeon.level.ent[move[0]][move[1]] != 0:
            if dungeon.level.ent[move[0]][move[1]].typeid != 2:
                action_push(char,a,b)
            elif dungeon.level.ent[move[0]][move[1]].typeid == 2:
                ent_displace(char,move[0],move[1])
                char.hp[1] += 100
                char.context += "Você achou um tesouro! "
                
        #getting to a closed door
        elif dungeon.level.tile[move[0]][move[1]].typeid == 2 and "door_closed" in dungeon.level.tile[move[0]][move[1]].tags:
            action_open(move[0],move[1])
            char.context += "A porta se abre. "
            
        #getting to a quiz
        elif dungeon.level.tile[move[0]][move[1]].typeid == 2 and "solve" in dungeon.level.tile[move[0]][move[1]].tags:
            quiz_solve(move[0],move[1],char)
                
        #getting to the exit       
        elif dungeon.level.tile[move[0]][move[1]].typeid == 2 and "exit" in dungeon.level.tile[move[0]][move[1]].tags:
            changelevel(randomlevel())
            char.context += 'changed level'
            char.hp[1] += 1000
        #getting to a hole      
        elif dungeon.level.tile[move[0]][move[1]].typeid == 2 and "hole" in dungeon.level.tile[move[0]][move[1]].tags:
            char.context += "Um buraco obstrue seu caminho! "
        #getting to a secret door       
        elif dungeon.level.tile[move[0]][move[1]].typeid == 2 and "secret" in dungeon.level.tile[move[0]][move[1]].tags:
            dungeon.level.tile[move[0]][move[1]] = copy(tiles.id['door'])
            board_update(move[0],move[1])
            char.context += 'Um segredo é revelado! '
            char.hp[1] += 500

        else:
            ent_displace(char,move[0],move[1])

def action_open(i,j):
    objects.ftr_door(dungeon.level.tile[i][j])
    board_update(i,j)

def action_push(striker,i,j):
    hasTarget = False
    direction = [striker.pos[0]+i,striker.pos[1]+j]
    
    if direction[0] > -1 and direction[0] < y-1 and  direction[1] > -1 and direction[1] < x-1:
        if dungeon.level.ent[direction[0]][direction[1]] != 0:
            hasTarget = True
            target = dungeon.level.ent[direction[0]][direction[1]]
            dir_push = [target.pos[0]+i,target.pos[1]+j]
    if hasTarget == True:    
        #check the direction where the target will be sent
        tileIsSolid = False
        tileIsDoor = False
        tileIsOut = False
        tileIsSoko = False
        tileIsHole = False
        
        #checking the tile the target will be sent
        if dir_push[0] < 0 or dir_push[0] > y-1 or dir_push[1] < 0 or dir_push[1] > x-1:
            tileIsOut = True
        else:
            dir_tile = dungeon.level.tile[dir_push[0]][dir_push[1]]
            dir_ent = dungeon.level.ent[dir_push[0]][dir_push[1]]
            if dir_tile.typeid == 1:
                tileIsSolid = True
            if dir_tile.typeid == 2 and "door_closed" in dir_tile.tags:
                tileIsDoor = True
            if dir_tile.typeid == 2 and "soko-solve" in dir_tile.tags:
                tileIsSoko = True
            if dir_tile.typeid == 2 and "hole" in dir_tile.tags:
                tileIsHole = True
            if dir_ent != 0:
                tileIsSolid=True
        
        #now actually pushing
        #SOLID WALL
        if tileIsSolid or tileIsOut or tileIsDoor:
            pass
        #SOKOBAN
        elif tileIsSoko:
            striker.context += "Você empurra a pedra, CLICK! "
            ent_displace(striker,direction[0],direction[1])
            dir_tile.tags.remove('soko-solve')
            dir_tile.glyph = 35
            board_update(dir_push[0],dir_push[1])
            soko_solve(striker)
            striker.hp[1] += 200
        elif tileIsHole:
            striker.context += "A pedra preenche o buraco! "
            ent_displace(striker,direction[0],direction[1])
            dungeon.level.tile[dir_push[0]][dir_push[1]] = copy(tiles.id['hole_fill'])
            board_update(dir_push[0],dir_push[1])
            striker.hp[1] += 100
        #NOTHING
        else:
            striker.context += "Você empurra a pedra. "
            target.context += striker.name+" just pushed you. "
            ent_displace(target,dir_push[0],dir_push[1])
            ent_displace(striker,direction[0],direction[1])
    else:
        striker.context += "You push thin air. "

def action_attack(striker,i,j):
    hasTarget = False
    didMiss = False
    
    direction = [striker.pos[0]+i,striker.pos[1]+j]
    
    if direction[0] > -1 and direction[0] < y and  direction[1] > -1 and direction[1] < x:
        if dungeon.level.ent[direction[0]][direction[1]] != 0:
            hasTarget = True
            target = dungeon.level.ent[direction[0]][direction[1]]
    if hasTarget == True:   
        damage = dice(1,4)+bonus(striker.attr[0])
        hitdice = dice(1,20)
        if hitdice == 20:
            damage *= 2
        if hitdice < target.stats['AC']:
            didMiss = True
        if didMiss == False:
            hurt(target,striker,damage,'punch')
        else:
            striker.context += "You miss your attack! "
            target.context += striker.name+" misses! "
    else:
        striker.context += "You attack thin air. "
        
def action_pick(striker,i,j):
    target = dungeon.level.item[i][j][-1]
    
    if target != 0:
        striker.items.append(target)
        striker.context += 'You pick up a'+target.name+". "
        del dungeon.level.item[i][j][-1]
    else: striker.context += 'Theres nothing here to pickup'

def quiz():
    isCorrect = False
    question = quizstart.question[randint(0,len(quizstart.question)-1)]
    picks = [0,1,2,3]
    pckd = []
    possible = ['a','b','c','d']
    for i in possible:
        roll = choice(picks)
        if roll == 3:
            correct = i
            pckd.append(question['right_answer'])
            picks.remove(roll)
        try:
            if roll in picks:
                picks.remove(roll)
                pckd.append(question['other_alternatives'][roll])
        except: break
            
    qtext = question['text']+"\n\nA)"+pckd[0]+"\nB)"+pckd[1]+"\nC)"+pckd[2]+"\nD)"+pckd[3]+"\nSua resposta: "
    answer = input(qtext).lower()
    if answer == correct: 
        isCorrect = True
        quizstart.question.remove(question)
    
    return isCorrect
    
def quiz_solve(i,j,target):
    tile = dungeon.level.tile[i][j]
    if 'tier1' in tile.tags:
        os.system(screenflush)
        if quiz() == True:
            tile.tags.remove('solve')
            tile.opaque = False
            tile.glyph = 30
            board_update(i,j)
            target.hp[1] += 450
            target.context += "Você acertou! "
        else:
            target.context += "Você errou... "
            hurt(target,target,1,'fail')
    if 'tier2' in tile.tags:
        os.system(screenflush)
        if quiz() == True:
            tile.tags.remove('solve')
            tile.opaque = False
            tile.glyph = 30
            board_update(i,j)
            target.hp[1] += 800
            target.context += "Você acertou! "
        else:
           target.context += "Você errou... "
           hurt(target,target,1,'fail')
    if 'tier3' in tile.tags:
        os.system(screenflush)
        if quiz():
            tile.tags.remove('solve')
            tile.opaque = False
            tile.glyph = 30
            board_update(i,j)
            target.context += "Você acertou! "
            target.hp[1] += 1000
        else:
            target.context += "Você errou... "
            hurt(target,target,1,'fail')
    os.system(screenflush)
    visflush()
    refresh()

def soko_solve(target):
    dungeon.level.info['soko'] -= 1
    if dungeon.level.info['soko'] != 0:
        target.context += str(dungeon.level.info['soko'])+" faltando... "
    elif dungeon.level.info['soko'] == 0:
        for i in dungeon.level.info['bars']:
            dungeon.level.tile[i[0]][i[1]] = tiles.id['bars_open']
            board_update(i[0],i[1])
        target.context += 'Sequência completa! '
        target.hp[1] += 600