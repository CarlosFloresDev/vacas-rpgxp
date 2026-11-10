"""Acto III. Eventos XP con ev.py, retratos VN y combate mental existente."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
from ev import *
from contenido_sistemas import battle

def say(name,text,exp='neutral'):
    if name=='Lucy' and ('Deja el vaso' in text or 'Eso no sale' in text):exp='calma'
    keys={'Steven':'steven','Lucy':'lucy','Madre':'madre','Molina':'molina','Elena':'elena','La Guernsey':'guernsey'}
    side='L' if name in ['Steven','Lucy'] else 'R'
    lines=_lines(text)
    out=[]
    for i in range(0,len(lines),4):
        box=lines[i:i+4]
        out += [cmd(101,f'\\P[{keys[name]}_{exp}]\\{side}\\D[1]\\NOMBRE[{name}]'+box[0])]
        out += [cmd(401,line) for line in box[1:]]
    return ('L',out)

def _lines(text):
    # Mismo ajuste tipográfico que ev.T, metadatos fuera del ancho.
    from ev import _wrap
    return _wrap(text)

def tension(n):return SCRIPT('lucy_tension(%d)'%n)
def objetos(m):
    slots={12:{'Dormitorio':0,'Taza sin usar':9},13:{},14:{'Riñón del lote borrado':5,'Cortina azul: refugio':1,'Tarro que atestigua':3},15:{'Camilla sin paciente':0,'Lavabo del personal':15},16:{'Preparación A: hígado':4,'Preparación B: riñón':5,'Control limpio':7,'Comparador y cuaderno':2}}
    for e in m.events:
        if e['name'] in slots[m.map_id]:
            n=slots[m.map_id][e['name']]
            for p in e['pages']:
                p['graphic'].update(tile_id=0,character_name='vacas_laboratorio',direction=2+2*(n//4),pattern=n%4)
                p.update(direction_fix=True,walk_anime=False,step_anime=False)
    props={12:[('Sofá de Lucy',4,12,8),('Armario de medicinas',21,13,14)],13:[('Tarros del mostrador',12,4,3)],14:[],15:[('Gotero sin bolsa',20,8,6)],16:[('Pinza sobre paño',8,12,11),('Lámpara de curas',21,12,10),('Bandeja de tarros',17,10,3)]}
    for name,x,y,n in props[m.map_id]:
        m.add(name,x,y,[page([T('Material usado, lavado demasiadas veces. Todavía sirve.')],char='vacas_laboratorio',d=2+2*(n//4),pat=n%4,dirfix=True,walk=False)])
    return m
def done(sw,items,text):
    return IF(c_sw(sw,False),[T(text)]+[ITEM(i) for i in items]+[SW(sw)], [T('Ya lo has recogido. No queda nada útil.')])

def ambience(m,cold=False):
    m.add('Ambiente A3',0,0,[page([TONE(-25,-30,-12,50,0) if cold else TONE(-12,-22,-35,35,0),BGS('016-Drips01',35,75),ERASE],trigger=4)])

def door(m,name,x,y,target,tx,ty,extra=None):
    m.add(name,x,y,[page((extra or [])+[TRANSFER(target,tx,ty,8)],trigger=1)])

def piso():
    m=MapEvents(12);ambience(m)
    m.add('Dos golpes',1,17,[page([
        T('Llamas dos veces. Al otro lado, alguien retira una silla de la puerta.'),
        say('Lucy','Has venido. He lavado un vaso para ti. Los otros son para las cosas que no sé decir.'),
        IF(c_sw(35),[say('Steven','Hoy hice lo que me mandaron. Mi mano seguía allí cuando yo ya quería irme.','miedo'),say('Lucy','Aquí puedes dejar de obedecer. Incluso a mí.')],
           [say('Steven','Intenté pararlo. No sirvió. Sigo oyendo el cajón.','miedo'),say('Lucy','Que no sirviera no borra que quisieras pararlo.')]),
        say('Lucy','Si el dolor deja algo dentro, debería poder verse. Necesito dos muestras de lotes distintos y algo limpio con que compararlas.'),
        T('La mesa tiene tres círculos: A, B y CONTROL. Primero, habla con Lucy junto a la mesa.'),SW(82),VAR(19,2)
    ],sw1=81,trigger=3),page([],sw1=82)])
    door(m,'Bajar al tercero',12,18,3,16,4)
    m.add('Lucy junto a la mesa',10,6,[page([
        IF(c_sw(83,False),[
            say('Lucy','Molina guarda hígado del lote de hoy. La otra carnicería cerró: su depósito está detrás del mostrador. No mezcles los tarros.'),
            say('Steven','¿Y si no encontramos veneno?'),say('Lucy','Entonces nos quedará el vaso limpio. Eso ya es algo.'),
            ITEM(14,2),ITEM(15),SW(83),VAR(20,1),
            T('Recibes dos tarros limpios y el protocolo de Lucy. Puedes releerlo desde Objetos. La carnicería se abre desde su mostrador en la calle.')
        ],[say('Lucy','Dos lotes y un control limpio. Elena guarda material en el hospital cerrado, al este de la calle. Yo prepararé el cuarto del fondo.')])
    ],char='vacas_lucy'),page([say('Lucy','Te espero dentro. No apagues la luz del pasillo.')],sw1=86,char='vacas_lucy'),page([],sw1=88)])
    m.add('Tele pequeña',5,13,[page([CHOICE(['Descansar','Guardar','Seguir'],[[T('Una pareja de cartón ríe por una tostada quemada. Por una vez no tienes que reírte con ellos.'),VEN(-15)],[SAVE],[]])],char='vacas_muebles',d=2,pat=1,dirfix=True)])
    m.add('Taza sin usar',7,8,[page([IF(c_sw(102,False),[say('Lucy','No la toques. La puse ahí para cuando viniera alguien. Hace meses.'),CHOICE(['Sentarte a su lado','Preguntar por los tarros'],[[say('Steven','Puedo quedarme un rato sin buscar nada.'),say('Lucy','Eso no sale en mis cuadernos.'),VAR(20,1,1),VEN(-6)],[say('Lucy','A veces una pregunta es una forma de no sentarse.')]]),SW(102)],[T('Dos tazas. Una tiene todavía la marca de tus dedos.')])],char='vacas_cosas',pat=0,d=2)])
    m.add('Cuaderno doméstico',18,5,[page([T('Entre listas de compra: «No confundir una persona con una tarea pendiente». La siguiente página está arrancada.')],tile=441)])
    m.add('Laboratorio tras la cortina',21,4,[page([IF(c_sw(86),[TRANSFER(16,12,17,8)],[T('Lucy: Primero las muestras. Y material del hospital; no pienso usar otra vez el colador.')])],tile=426)])
    m.add('Dormitorio',19,13,[page([T('La cama está hecha solo por un lado. Bajo la almohada hay un horario de autobuses. Todas las salidas están rodeadas.')])])
    return objetos(m)

def carniceria():
    m=MapEvents(13);ambience(m,True)
    door(m,'Salida al toldo',10,13,4,18,8)
    m.add('Molina',5,5,[page([
        IF(c_sw(83),[
            IF(c_sw(84,False),[say('Molina','¿Otra vez para la vecina? Me pidió que le pesara la tristeza. Le dije que la báscula no baja de cien gramos.'),
                say('Steven','Necesito hígado. Con la etiqueta del lote.'),
                say('Molina','Lote 17. Y sal sin abrir. Si vais a jugar a médicos, al menos no mintáis con las etiquetas.'),
                ITEM(14,-1),ITEM(16),ITEM(18),ITEM(23),SW(84),VAR(19,3),tension(4),
                T('Un tarro limpio contiene ahora hígado del lote 17. Conservas el otro tarro. La puerta del fondo lleva al depósito de la carnicería cerrada.')
            ],[say('Molina','La persiana del depósito se atasca. Si se pone a golpear, busca la cortina azul o vuelve aquí. Conserva el tarro, aunque tengas que correr.')])
        ],[say('Molina','Hoy tengo hígado, riñones y muy poca paciencia. Habla primero con tu vecina.')])
    ],char='vacas_carnicero')])
    m.add('Puerta del depósito vecino',16,3,[page([IF(c_sw(84),[TRANSFER(14,3,12,8)],[T('Molina: No es un atajo. Dime primero qué buscas.')])],tile=426)])
    m.add('Factura cosida',12,7,[page([T('La factura está sujeta al papel de envolver con hilo quirúrgico. El precio cambia cada vez que parpadeas.'),battle(11,93),T('Ahora solo dice: «No se admite devolver lo vivido».')],tile=441)])
    m.add('Mostrador de pedidos',7,8,[page([T('Dos sellos: APTO y NO APTO. Ninguno significa que al animal le doliera menos.')],tile=419)])
    return objetos(m)

def captura():
    return [SW(101,False),SCRIPT('lucy_captura'),T('La persiana cae detrás de ti. Has salido por debajo. El tarro sigue cerrado; nadie te lo quita.'),TRANSFER(13,15,4,2)]

def deposito():
    m=MapEvents(14);ambience(m,True)
    m.add('Persiana despierta',1,12,[page([
        IF(c_sw(91,False),[say('Steven','Ese golpe no viene de la calle.','miedo'),T('Tienes 35 segundos. Recoge el riñón al fondo y vuelve a la puerta, o refúgiate tras la cortina azul. Una captura conserva tus objetos y permite reintentar.'),SCRIPT('susto(8)'),SW(90),SW(101,False),TIMER(35),MENUACCESS(False)]),ERASE
    ],trigger=3)])
    m.add('Sombra de la persiana',5,11,[page([],through=True,opacity=0),page(captura(),sw1=90,char='vacas_cripps',trigger=2,move_type=2,speed=3,freq=5,opacity=150)])
    # El paralelo solo solicita captura. Su página desaparece al apagar 90;
    # diálogo y transferencia deben sobrevivir en el intérprete principal.
    m.add('Tiempo de la persiana',0,1,[page([IF(c_timer_le(0),[SW(101),SW(90,False)]),WAIT(2)],sw1=90,trigger=4)])
    m.add('Riñón del lote borrado',16,4,[page([
        IF(c_sw(85,False),[IF(c_item(14),[T('Un riñón oscuro en una bandeja. En su etiqueta han raspado el número. Lo cierras en el segundo tarro.'),ITEM(14,-1),ITEM(17),SW(85),VAR(19,4),tension(7)],[T('Necesitas el segundo tarro limpio de Lucy.')])],[T('La bandeja está vacía.')])
    ],tile=430)])
    escape=[SW(90,False),SW(91),SW(101,False),TIMERSTOP,MENUACCESS(True)]
    m.add('Cortina azul: refugio',9,9,[page([
        CHOICE(['Ocultarte','Seguir'],[[TRANSP(True),WAIT(80),TRANSP(False),
            IF(c_sw(85),escape+[T('El golpe se aleja. Ya puedes salir con la muestra.')],[SW(90,False),TIMERSTOP,MENUACCESS(True),T('La sombra pasa de largo. El riñón sigue al fondo. La puerta de salida también es segura.')])],[]])
    ],tile=438)])
    m.add('Salida del depósito',3,13,[page([SW(90,False),SW(101,False),TIMERSTOP,MENUACCESS(True),IF(c_sw(85),[SW(91)]),TRANSFER(13,16,4,2)],trigger=1)])
    m.add('Llamador de servicio',3,10,[page([IF(c_sw(91,False),[T('Vuelves a abrir el paso. La persiana responde.'),SW(90),SW(101,False),TIMER(35),MENUACCESS(False)],[T('La persiana ya no golpea.')])],tile=415)])
    m.add('Tarro que atestigua',14,7,[page([IF(c_sw(90,False),[T('En el vidrio hay una boca sin dueño. No pide salir: pide que lo mires.'),battle(10,92)],[T('Primero sal de la vista de la sombra.')])],tile=430)])
    m.add('Captura de la persiana',0,2,[page(captura(),sw1=101,trigger=3)])
    return objetos(m)

def hospital():
    m=MapEvents(15);ambience(m,True)
    door(m,'Salida del hospital',12,18,4,35,12)
    m.add('Elena',7,6,[page([
        IF(c_sw(85),[
            IF(c_sw(86,False),[say('Elena','Esto era una sala de curas. Ahora cuido las goteras. Lucy me ayudaba a doblar sábanas; luego empezó a buscar respuestas en ellas.'),
                say('Steven','Necesitamos saber qué tienen dos muestras. Dice que es veneno.'),
                say('Elena','Una mancha no es un diagnóstico. Usa suero como control y mira de dónde viene cada cosa. Si ella se asusta, quédate con ella antes que con la teoría.'),
                ITEM(19),ITEM(20),ITEM(21),ITEM(22),ITEM(24),SW(86),VAR(19,5),
                T('Recibes guantes, pinza, reactivo, suero y el protocolo de contraste. El cuarto del fondo del piso de Lucy está listo.')
            ],[say('Elena','Sal más muestra, luego reactivo. Repite con el otro lote y con suero solo. Los tres resultados van juntos. Si se tiñen los tres, mira el frasco, no a Lucy.')])
        ],[say('Elena','No llevo consultas. Trae los dos tarros de las carnicerías y veremos qué material puedo prestarte.')])
    ],char='vacas_elena')])
    m.add('Camilla sin paciente',18,7,[page([T('La sábana se hunde bajo el peso de alguien que no está. La almohada lleva tu nombre escrito al revés.'),battle(12,94),T('Das la vuelta a la almohada. Solo hay un número de lavandería.')],char='vacas_muebles',d=4,pat=2,dirfix=True)])
    m.add('Nota de existencias',5,12,[page([T('«Reactivo R-0: lote retirado. Se colorea en contacto con sal. No sirve para diagnóstico». Elena ha subrayado R-0 tres veces.'),SW(103)],tile=441)])
    m.add('Lavabo del personal',20,4,[page([CHOICE(['Lavarte las manos','Guardar','Volver'],[[T('Agua tibia. Puedes quedarte hasta distinguir el ruido del grifo de tu propia respiración.'),VEN(-12)],[SAVE],[]])],tile=435)])
    return objetos(m)

def ensayo(flag,raw,output,name):
    return IF(c_sw(flag),[T('La preparación '+name+' está sellada y rotulada.')],[
        IF(c_script('$game_party.item_number(%d)>0 && $game_party.item_number(19)>0 && $game_party.item_number(20)>0 && $game_party.item_number(21)>0 && $game_party.item_number(18)>0'%raw),[
            CHOICE(['Sal y reactivo','Solo reactivo','Volver'],[
                [T('Usas guantes y pinza, añades sal y una gota de R-0. La preparación '+name+' se vuelve azul oscuro.'),ITEM(raw,-1),ITEM(output),SW(flag),VAR(22,1,1),tension(3)],
                [T('Sin la misma preparación no puedes comparar resultados. El protocolo pide sal y reactivo para los tres. No desperdicias la muestra.')],[]])
        ],[T('Necesitas la muestra, guantes, pinza, sal y reactivo del hospital.')])])

def laboratorio():
    m=MapEvents(16);ambience(m,True)
    door(m,'Volver al piso',12,18,12,20,5)
    m.add('Preparación A: hígado',5,6,[page([ensayo(104,16,25,'A (hígado)')],tile=419)])
    m.add('Preparación B: riñón',11,6,[page([ensayo(105,17,26,'B (riñón)')],tile=419)])
    m.add('Control limpio',17,6,[page([ensayo(106,22,27,'CONTROL (suero limpio)')],tile=419)])
    m.add('Etiqueta del frasco',6,12,[page([T('R-0, diagnóstico visual. Debajo hay otra etiqueta pegada: «Retirado: reacciona a la sal». No habla de dolor. No habla de personas.'),SW(103)],tile=441)])
    m.add('Comparador y cuaderno',11,10,[page([
        IF(c_script('$game_switches[104] && $game_switches[105] && $game_switches[106]'),[
            IF(c_sw(88,False),[
                T('A: azul. B: azul. CONTROL: azul. Lucy aprieta su tarro vacío contra el pecho.'),
                CHOICE(['Es el reactivo','Es veneno en todo','No sé todavía'],[
                    [say('Steven','También cambia el suero limpio. Esto no demuestra que tengas algo malo dentro.'),VAR(20,1,1)],
                    [say('Lucy','Entonces ni siquiera el agua está a salvo.'),tension(7),say('Steven','Espera. El agua cambia cuando le ponemos el frasco. Eso también cuenta.')],
                    [say('Steven','No sé qué te está haciendo daño. Sé que este frasco no puede responderlo.'),VAR(20,1,1)]
                ]),ITEM(28),SW(88),VAR(19,6),
                say('Lucy','He tirado platos, ropa, cartas. Pensaba: si encuentro la parte mala, podré quedarme con el resto. ¿Y si no hay un resto limpio?','quiebre'),
                SCRIPT('susto(9)'),say('Steven','No eres una muestra. Mírame. Estoy aquí.','miedo'),
                T('Habla con Lucy, al fondo del laboratorio. Puedes volver a guardar antes.')
            ],[T('El cuaderno reúne tres resultados idénticos. Ninguno prueba la teoría del veneno.')])
        ],[T('Faltan preparaciones. El comparador exige A, B y CONTROL: tres tarros sellados, el mismo procedimiento.')])
    ],tile=422)])
    m.add('Lucy: diagnóstico',18,13,[page([
        say('Lucy','El tarro nunca se llena. Empiezo a pensar que esa era la trampa.'),
        IF(c_sw(88),[
            IF(c_sw(95,False),[
                say('Lucy','No quiero que me arregles. Quiero que la habitación deje de pedirme una prueba más.','quiebre'),
                T('Las etiquetas se levantan de la mesa como una jaula. La visión habla con tu voz: «Si la quieres, encuentra la pieza rota». No es Lucy. Es la orden.'),
                battle(13,95,True),VAR(19,7)
            ]),
            say('Lucy','Elena puede venir. Pero si vas a bajar con ese cuaderno, no me digas que lo haces por mí.','quiebre'),
            IF(c_var(20,2,1),[say('Lucy','Me gustó que te sentaras conmigo. No lo has medido y ha pasado igual.')]),
            IF(c_sw(38),[say('La Guernsey','Abajo hay sitio para lo que ellos desechan. Trae los nombres.','susurro')],[T('Desde la tubería llega un mugido. El plano del colector vuelve a crujir dentro de tu bolsillo.')]),
            CHOICE(['Quedarme con Lucy','Llevar las pruebas abajo','Todavía no'],[
                [SW(96),SW(97,False),VAR(23,1),say('Steven','Voy a llamar a Elena. Luego me quedo. No necesitas ganarte una silla aquí.'),say('Lucy','Deja el vaso en la mesa. Esta vez lo vamos a usar.'),VEN(-12),ITEM(29),SW(98),VAR(19,8),T('Elena sube. Por primera vez, Steven no recoge nada antes de sentarse. Más abajo, la ciudad sigue respirando.'),SAVE,SCRIPT('$scene = Scene_FinActo.new(3)')],
                [SW(97),SW(96,False),VAR(23,2),say('Steven','Le pediré a Elena que suba. Me llevo los lotes y las fechas. Alguien ha estado borrando nombres.'),say('Lucy','Vete por lo que tú quieras. A mí no me conviertas en otra etiqueta.','quiebre'),tension(8),ITEM(29),SW(98),VAR(19,8),T('Elena acepta quedarse con Lucy. Steven guarda el cuaderno y la llave del colector. No sabe si busca una respuesta o un sitio donde no le pregunten.'),SAVE,SCRIPT('$scene = Scene_FinActo.new(3)')],[]
            ])
        ],[say('Lucy','Faltan los tres resultados. Sin el control solo tendremos otra historia que nos hemos contado.')])
    ],char='vacas_lucy'),page([say('Lucy','Elena está aquí. El cuaderno ya no decide por nosotras.'),T('Fin del Acto III. La salida hacia el colector corresponde al Acto IV.'),CHOICE(['Guardar','Ver fin del acto','Volver'],[[SAVE],[SCRIPT('$scene = Scene_FinActo.new(3)')],[]])],sw1=98,char='vacas_lucy')])
    return objetos(m)

NOTES={15:'PROTOCOLO DE LUCY: dos tarros, dos lotes. Hígado de Molina; riñón del depósito vecino. Pedir material a Elena en el hospital, al este. Comparar A y B con suero limpio. No llamar veneno a una duda.',23:'MOLINA: hígado, lote 17, recibido hoy. Segundo lote: etiqueta raspada. Las muestras conservan su procedencia; no mezclar.',24:'CONTRASTE: guantes y pinza. Sal y una gota de R-0 en A, B y CONTROL de suero limpio. Si cambia el control, revisar el reactivo. Una reacción no demuestra una causa del sufrimiento.',28:'RESULTADOS: hígado azul; riñón azul; suero limpio azul. R-0 reacciona a la sal. No demuestra un veneno interno. Se conserva el registro de lotes sin convertirlo en diagnóstico.',29:'LLAVE DEL COLECTOR: Elena guardaba la llave del desagüe viejo del hospital. El camino bajo la ciudad continuará en el Acto IV. La decisión de Steven y los nombres del cuaderno permanecen.'}
def notas():return [IF(c_script('$vacas_ultimo_objeto == %d'%i),[T(text)]) for i,text in NOTES.items()]
