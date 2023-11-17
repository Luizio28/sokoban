from data import objects as obj

id = {}

#list['example'] = obj.actor(typeid, name, glyph, [hp,max], busy, fx, pos, attr, tags, stats, context, vision,items)
id['player'] = obj.actor(1,'Adventurer',2,[1,1],0,obj.def_effects,obj.def_pos,obj.def_attr,[],obj.charstats,'',[],[])
id['npc'] = obj.actor(0,'NPC',28,[1,1],0,obj.def_effects,obj.def_pos,obj.def_attr,[],obj.charstats,'',[],[])
id['boulder'] = obj.actor(0,'the boulder',29,[9999,9999],0,obj.def_effects,obj.def_pos,obj.def_attr,[],obj.charstats,'',['boulder'],[])
id['null'] = 0
id['money'] = obj.actor(2,'mone',43,[1,1],0,obj.def_effects,obj.def_pos,obj.def_attr,['$100'],obj.charstats,'',[],[])