"""Extensiones de historia aplicadas por build_events; IDs existentes estables."""
from ev import *

def battle(troop,flag,boss=False):
    tutorial=IF(c_sw(54,False),[T('\\c[6]Las imágenes no son cuerpos: son recuerdos. Golpear y Poner nombre las debilitan. Respirar cura, devuelve aliento y limpia Pánico, Asco y Culpa. El veneno crece al luchar.\\c[0]'),SW(54)])
    play=[SCRIPT('preparar_mente'),cmd(301,troop,False,True)]
    if boss:
        play=[LOOP(play+[IF(c_var(18,0),[BREAK],[T('Te despiertas dentro del mismo sueño. Todavía puedes respirar. Vuelve a ponerle nombre.')])])]
    return IF(c_sw(flag,False),[tutorial]+play+[SW(flag)])

def optional(troop,flag):
    return IF(c_sw(flag,False),[CHOICE(['Afrontar la imagen','Apartarte'],[[battle(troop,flag)],[]],2)])

def after_text(commands,needle,extra):
    """Inserta al acabar una caja 101/401, conservando su indentacion."""
    i=0
    while i<len(commands):
        if commands[i]['code']==101:
            j=i+1
            while j<len(commands) and commands[j]['code']==401:j+=1
            text=' '.join(c['parameters'][0] for c in commands[i:j])
            if needle in text:
                commands[j:j]=flatten(extra,commands[i]['indent']);return True
            i=j
        else:i+=1
    return False

def enriquecer(m):
    for e in m.events:
        name=e['name']
        for p in e['pages']:
            cs=p['list']
            if m.map_id==2:
                if name=='Lavabo':after_text(cs,'Detrás del espejo',[SCRIPT('susto(1)')])
                if name=='Tele':after_text(cs,'Dentro de la nieve',[SCRIPT('susto(2)'),optional(8,45)])
                if name in ['Cama Steven','Cama Steven 2']:
                    after_text(cs,'Debajo del suelo',[battle(2,51)])
                    after_text(cs,'Sueñas con la cinta',[battle(7,47)])
                    after_text(cs,'Sueñas que bajas',[battle(3,49)])
                    # El jefe se afronta tras Lucy y el sueldo de la tercera noche.
                    for i,c in enumerate(cs):
                        if c['code']==355 and c['parameters'][0]=='fin_del_acto2':
                            cs[i:i]=flatten([T('En el techo, el cajón se abre hacia dentro. Tu reflejo lleva una corona de ganchos. No vas a darle tu nombre.'),SCRIPT('susto(7)'),battle(9,55,True),T('No eres el cajón. No eres su rey. Al otro lado de la pared, Perro respira contigo.')],c['indent']);break
                if name=='Libro':
                    cs.extend(flatten([IF(c_sw(53,False),[T('Entre dos hojas hay un dibujo de un perro junto a una puerta abierta. Alguien escribió: TODAVÍA.'),SW(53),VEN(-5)])]))
            if m.map_id==5 and name=='Camion de ganado':after_text(cs,'Algo da un golpe dentro',[SCRIPT('susto(3)')])
            if m.map_id==6 and 'Desague' in name:
                cs.extend(flatten([IF(c_sw(25),[SCRIPT('susto(4)'),optional(5,46)])]))
            if m.map_id==7 and ('Vaca' in name or 'vaca' in name) and name!='Vaca decorado':
                # Solo una aparición de la voz; el interruptor persiste entre páginas.
                cs.extend(flatten([IF(c_var(1,35,1),[optional(1,50)])]))
            if m.map_id==8 and name=='Canal':
                cs.extend(flatten([IF(c_var(1,35,1),[optional(7,47)])]))
            if m.map_id==9 and ('escarcha' in name.lower() or 'mensaje' in name.lower()):
                cs.extend(flatten([SCRIPT('susto(6)')]))
            if m.map_id==10 and name=='Foto':
                cs.extend(flatten([SCRIPT('susto(6)'),optional(4,48)]))
            if m.map_id==11 and name=='Rejilla':
                after_text(cs,'Te acercas a la rejilla',[SCRIPT('susto(5)')])
            if m.map_id==11 and name=='Trampilla':
                cs.extend(flatten([IF(c_sw(38),[T('En el hierro aparece tu cara con ojos de vaca. Sabes que la voz de abajo no está aquí: esto lo has traído tú.'),optional(6,52)])]))
    return m
