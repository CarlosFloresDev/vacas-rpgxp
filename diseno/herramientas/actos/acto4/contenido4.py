"""Acto IV, eventos XP. Texto original; comandos y VN del juego existente."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
from ev import *
from contenido_sistemas import battle
from contenido3 import say as say3

def say(name,text,exp='neutral'):
    if name not in ('Muesca','Junco'):return say3(name,text,exp)
    from ev import _wrap
    lines=_wrap(text);out=[]
    for i in range(0,len(lines),4):
        out.append(cmd(101,'\\P[%s_neutral]\\R\\D[1]\\NOMBRE[%s]'%(name.lower(),name)+lines[i]))
        out.extend(cmd(401,t) for t in lines[i+1:i+4])
    return ('L',out)

def bajar():
    # El salto de escena conserva la cola RGSS; los eventos usan 201 explicito.
    return [SCRIPT('Vacas.empezar_acto4\n$game_temp.player_transferring = false'),TRANSFER(17,4,11,8)]

def rep(n):return SCRIPT('Vacas.reputacion(%d)'%n)
def tension(n):return SCRIPT('bajo_tension(%d)'%n)
def prop(n,commands=None,**kw):
    return page(commands or [],char='vacas_alcantarilla',d=2+2*(n//4),pat=n%4,dirfix=True,walk=False,**kw)
def amb(m):
    m.add('Respiracion bajo la ciudad',0,0,[page([TONE(-16,-6,-20,28,0),BGS('016-Drips01',48,65),ERASE],trigger=4)])
def puerta(m,name,x,y,mid,tx,ty,extra=None):
    m.add(name,x,y,[prop(11,(extra or [])+[TRANSFER(mid,tx,ty,8)])])
def pila(m,x,y,name='Pila de emergencia'):
    m.add(name,x,y,[prop(0,[T('Una pila seca dentro de una bolsa encerada. +1 repuesto; S recarga sesenta puntos.'),ITEM(31),SS()]),page([],ss='A',through=True)])
def captura(dest,x,y):
    return [SCRIPT('bajo_captura'),T('Te metes entre dos tubos. El golpe pasa de largo. Conservas todos tus objetos; puedes continuar.'),TRANSFER(dest,x,y,8)]
def caza(m,active,done,pending,seconds,rx,ry,dx,dy,refugio):
    m.add('Acechador '+str(m.map_id),rx,ry,[page([],through=True),page(captura(21,4,10),sw1=active,char='vacas_muesca',speed=3,freq=5,move_type=2,trigger=2,opacity=175)])
    m.add('Reloj de caza',0,1,[page([IF(c_timer_le(0),[SW(pending),SW(active,False)]),WAIT(2)],sw1=active,trigger=4)])
    m.add('Captura pendiente',0,2,[page(captura(21,4,10),sw1=pending,trigger=3)])
    m.add(refugio,dx,dy,[prop(6,[CHOICE(['Esconderte','Seguir'],[[TRANSP(True),WAIT(65),SCRIPT('Vacas.detener_caza'),SW(done),T('Cuentas cuatro pezuñas. Después, ninguna. Ya puedes seguir.')],[]])])])

def entrada():
    m=MapEvents(17);amb(m)
    m.add('Llegada al colector',1,1,[page([IF(c_sw(96),[
        say('Steven','Esperé a que Lucy se durmiera. Elena ha dejado la luz del pasillo encendida.','miedo'),say('La Guernsey','Has tardado. Aquí abajo confundimos esperar con tener hambre.','susurro')],[say('Steven','Traigo los lotes. No dicen qué le pasa a Lucy. Sí dicen quién borró los nombres.'),say('La Guernsey','Las pruebas no te hacen inocente. Pero pueden abrir una puerta.','susurro')]),
        T('La llave del colector gira. Has recibido una linterna y dos pilas. A enciende/apaga; S recarga. La luz se agota solo al explorar. En la oscuridad queda un radio mínimo, pero sube el veneno. El altar no gasta batería.'),SW(114),VAR(55,2)
    ],sw1=113,trigger=3),page([],sw1=114)])
    puerta(m,'Escalera al hospital',4,12,15,20,5,[SCRIPT('Vacas.detener_caza')])
    puerta(m,'Tuneles de servicio',16,5,18,3,11)
    pila(m,7,10)
    m.add('Plano rayado del colector',10,6,[prop(9,[T('Un plano tallado: túneles al norte, agua al este; un altar en el ramal seco. Junto a las válvulas: CERRAR EL RETORNO antes de ABRIR LA DESCARGA. No empujes el agua hacia los que duermen.'),ITEM(34),SS()]),prop(9,[T('Retorno cerrado, después descarga abierta. El altar queda al este de los túneles.')],ss='A')])
    m.add('Botas sin dueño',12,9,[prop(8,[T('Tres pares de botas ordenados por tamaño. En cada suela, la misma grasa del matadero. Nadie ordenó salir a sus dueños.')])])
    m.add('Marcas de la dinamo',14,5,[prop(1,[T('Tres trazos bajo la grasa: primero el tubo; luego el aire en la bolsa; al final, la campana. La dinamo del altar escucha en ese orden.')])])
    return m

def tuneles():
    m=MapEvents(18);amb(m)
    puerta(m,'Regreso al colector',3,12,17,15,6,[SCRIPT('Vacas.detener_caza')])
    puerta(m,'Ramal del altar',17,10,21,4,10,[SW(121),SCRIPT('Vacas.detener_caza')])
    puerta(m,'Boca inundada',17,4,19,3,11,[SW(121),SCRIPT('Vacas.detener_caza')])
    m.add('Muesca vigila',9,6,[page([
        IF(c_sw(127,False),[say('Muesca','No me llames ganado. Ese nombre lleva una puerta detrás.'),
            CHOICE(['Bajar la linterna','Exigir paso','Escuchar'],[
                [say('Steven','No te voy a alumbrar los ojos.'),rep(1),SW(138)],
                [say('Steven','Aparta. He bajado para hablar con la Guernsey.'),rep(-2)],
                [say('Muesca','Cripps nos contaba por el golpe que hacían nuestras cabezas. Aprende a contar de otra manera.'),rep(1),SW(138)]]),SW(127),
            IF(c_var(51,0,2),[say('Muesca','Entonces corre. Quiero ver si sabes encontrar un hueco sin pisar a nadie.'),T('Persecución: 32 segundos. El nicho de sacos y las salidas son seguros. Una captura conserva objetos y te lleva al altar.'),SW(120),TIMER(32),MENUACCESS(False),SCRIPT('susto(10)')],[say('Muesca','Junco está junto al agua. Si la ayudas, escucharé tu nombre.')])
        ],[IF(c_var(51,1,1),[say('Muesca','Puedes pasar. No significa que vaya a dejar de mirarte.')],[say('Muesca','El nicho de sacos está al sur. Las pezuñas también saben esperar.')])])
    ],char='vacas_muesca',dirfix=True,walk=False)])
    caza(m,120,121,122,32,6,10,10,10,'Nicho de sacos')
    m.add('Rueda entre trapos',14,7,[prop(2,[IF(c_sw(119,False),[T('Una rueda de válvula entre trapos con el sello de Cripps. Aún encaja en el vástago del colector.'),ITEM(32),SW(119),VAR(55,3)],[T('Ya guardas la rueda.')])])])
    pila(m,4,7)
    m.add('El Coro del tubo',5,4,[prop(10,[T('El tubo devuelve todas las voces que has obedecido. Ninguna tiene pulmones.'),battle(14,128)])])
    return m

def inundada():
    m=MapEvents(19);amb(m)
    puerta(m,'Volver a los tuneles',3,12,18,16,5,[SCRIPT('Vacas.detener_caza')])
    m.add('Compuerta a la camara',17,5,[prop(11,[IF(c_sw(118),[SW(124),SCRIPT('Vacas.detener_caza'),TRANSFER(20,4,11,8)],[T('El agua empuja desde el otro lado. Dos válvulas: primero cerrar retorno; después abrir descarga. La rueda está en los túneles.')])])])
    m.add('Junco atrapada',7,9,[page([
        IF(c_sw(126,False),[say('Junco','La rejilla me muerde la pata. No tires de mí. Levanta el hierro.'),CHOICE(['Levantar la rejilla','Pasar de largo'],[
            [T('Metes el tubo bajo el borde. Junco saca la pata por su propio peso.'),say('Junco','Has esperado a que yo pudiera. Eso se recuerda.'),rep(2),SW(126),VEN(-5)],
            [say('Junco','El agua subirá antes de que te acostumbres al ruido.')]])],[say('Junco','Retorno, luego descarga. Si no, las camas del altar reciben toda el agua.')])
    ],char='vacas_junco',dirfix=True,walk=False)])
    m.add('Valvula retorno',5,5,[prop(3,[IF(c_item(32),[
        IF(c_sw(116,False),[T('Ajustas la rueda y cierras RETORNO. El tubo que lleva al altar deja de vibrar.'),SW(116),VAR(54,1)],[T('El retorno ya está cerrado.')])
    ],[T('Falta una rueda. La vieron entre los trapos de los túneles.')])])])
    m.add('Valvula descarga',13,5,[prop(3,[IF(c_sw(118),[T('La descarga está abierta. Puedes entrar en la cámara.')],[
        IF(c_sw(116),[T('Abres DESCARGA con el retorno cerrado. La corriente se retira del umbral. Las pasarelas siguen siendo la ruta segura.'),SW(117),SW(118),VAR(54,2),VAR(55,4),
            IF(c_sw(126),[rep(1)]),SCRIPT('susto(11)'),T('Algo viene con el último golpe del agua. 28 segundos. El armario de bombas o cualquiera de las salidas cortan la persecución.'),SW(123),TIMER(28),MENUACCESS(False)
        ],[T('El agua revienta contra el tubo del altar. Cierras antes de inundarlo. La rueda no se pierde: cierra primero RETORNO.'),tension(4)])])])])
    caza(m,123,124,125,28,10,11,15,9,'Armario de bombas')
    m.add('El Pulmon de cieno',15,7,[prop(12,[IF(c_sw(123,False),[T('Una bolsa respira bajo el limo. Cada burbuja pronuncia la palabra limpio.'),battle(15,129)],[T('Primero encuentra refugio.')])])])
    pila(m,11,10)
    return m

def camara():
    m=MapEvents(20);amb(m)
    puerta(m,'Regreso al agua',4,12,19,16,6,[SCRIPT('Vacas.detener_caza')])
    puerta(m,'Paso al altar',17,11,21,15,5)
    m.add('La Guernsey bajo la ciudad',11,5,[page([
        IF(c_sw(131,False),[
            say('La Guernsey','Cripps cierra una mano y cien cuerpos avanzan. Necesitamos su puerta abierta, no otro hombre aprendiendo el gesto.','susurro'),
            IF(c_sw(96),[say('La Guernsey','Te quedaste con la mujer cuando dejó de servirte de respuesta. Eso ha llegado antes que tú.','susurro')],[say('La Guernsey','Has traído los lotes. No vamos a comer papel. Dinos a quién protegían los números.','susurro')]),
            IF(c_var(51,1,1),[say('Junco','Yo respondo por el hueco que dejó para mi pata.')],[say('Muesca','No confío en él. Oiré el trato; vigilaré la salida.')]),
            T('El hueco del techo toma forma de campana. Dentro no hay una vaca: hay una orden que nunca deja de sonar.'),battle(16,130),battle(17,131,True),VAR(55,5)
        ]),
        IF(c_sw(132,False),[
            say('La Guernsey','Contra Cripps. El resto tendrás que elegirlo cuando deje de haber una puerta cerrada.','susurro'),
            CHOICE(['Pacto: nadie es ganado','Pacto: Cripps pagará','Volver al altar'],[
                [SW(133),SW(134,False),rep(1),say('Steven','Abriré el matadero. Nadie lleva un collar con mi nombre. Ni vosotros ni los de arriba.'),say('La Guernsey','Te lo repetiré cuando te guste mandar.','susurro'),SW(132),SW(135),ITEM(33),VAR(55,6),T('Pacto sellado. El altar permite guardar antes del cierre. El paso al matadero de noche queda marcado para el Acto V.')],
                [SW(134),SW(133,False),rep(-1),say('Steven','Os daré a Cripps. Quiero que sepa quién abrió la puerta.'),say('La Guernsey','Procura no necesitar su puesto para reconocer su cara.','susurro'),SW(132),SW(135),ITEM(33),VAR(55,6),tension(5),T('Pacto sellado. El altar permite guardar antes del cierre. La venganza queda registrada para los Actos V y VI.')],[]])
        ],[say('La Guernsey','El pacto está hecho. El camino sigue al otro lado del altar.','susurro')])
    ],char='vacas_guernsey4',dirfix=True,walk=False)])
    m.add('Muesca en consejo',6,6,[page([IF(c_var(51,1,1),[say('Muesca','Te hemos dejado sitio. No es un trono.')],[say('Muesca','Una promesa no llena un estómago. No cruces detrás de mí.')])],char='vacas_muesca',dirfix=True,walk=False)])
    m.add('Junco en consejo',15,7,[page([IF(c_sw(126),[say('Junco','La pata duele. Camina. Pueden ser ciertas las dos cosas.')],[say('Junco','No confundiré un pacto con una mano tendida.')])],char='vacas_junco',dirfix=True,walk=False)])
    m.add('Camas de la manada',7,10,[prop(6,[T('Los sacos están separados por tubos tibios. Los cubos tienen marcas para repartir agua, no nombres de propietarios.')])])
    return m

def altar():
    m=MapEvents(21);amb(m)
    puerta(m,'Tuneles desde altar',3,11,18,16,10)
    puerta(m,'Camara desde altar',16,5,20,16,11,[IF(c_sw(118,False),[T('Un conducto seco permite llegar al umbral, pero el agua aún bloquea la cámara.'),EXIT])])
    m.add('Altar de las cosas salvadas',10,5,[prop(7,[T('Una lámpara sobre una puerta arrancada. Debajo: chapas, una taza sin asa y un saco doblado para alguien que todavía no ha llegado.'),
        CHOICE(['Descansar y cargar','Guardar','Seguir'],[
            [VEN(-18),SCRIPT('$game_variables[52] = 100'),SW(115),SCRIPT('$game_actors[1].recover_all'),T('La dinamo del altar recarga la linterna. La huella permanece. Puedes volver tantas veces como necesites.')],[SAVE],[]])])])
    m.add('Caja de repuestos del altar',7,7,[prop(0,[IF(c_script('$game_party.item_number(31)<2'),[ITEM(31),T('Tomas una pila del cargador. El altar mantiene hasta dos repuestos: una red de seguridad para explorar.')],[T('Ya llevas dos o más repuestos. Deja los demás para quien vuelva.')])])])
    m.add('Paso hacia el matadero nocturno',15,10,[prop(11,[IF(c_sw(132),[CHOICE(['Guardar y ver fin del acto','Seguir explorando'],[[SAVE,SCRIPT('$scene = Scene_FinActo.new(4)')],[]])],[T('La puerta de arriba lleva al matadero. Primero habla con la Guernsey, al otro lado del agua.')])])])
    m.add('Cucharas contadas',5,5,[prop(9,[T('Cada cuchara tiene una muesca. Hay una más que camas. No sabes si es hospitalidad o una deuda.')])])
    m.add('Dinamo de tres resonancias',12,8,[prop(15,[IF(c_sw(139,False),[T('Tres mandos sin letras: tubo, bolsa de aire y campana. Las marcas del colector recuerdan el orden.'),CHOICE(['Tubo, aire, campana','Campana, tubo, aire','Aire, campana, tubo','Dejarlo'],[[T('El tubo calla. La bolsa toma aire. La campana deja de ordenar. La carga vuelve a circular; encuentras una pila.'),SW(139),ITEM(31),rep(1),VEN(-8)],[T('La campana devuelve una orden seca. Puedes volver a intentar.'),tension(2)],[T('La bolsa se vacia antes de recibir aire. Puedes volver a intentar.'),tension(2)],[]])],[T('La dinamo mantiene el orden. La pila ya fue recogida.')])])])
    return m

SWITCHES={113:'Acto IV activo',114:'Llegada vista',115:'Linterna encendida',116:'Retorno cerrado',117:'Descarga abierta',118:'Umbral drenado',119:'Rueda recogida',120:'Caza tuneles',121:'Caza tuneles resuelta',122:'Captura tuneles pendiente',123:'Caza agua',124:'Caza agua resuelta',125:'Captura agua pendiente',126:'Junco liberada',127:'Muesca escuchada',128:'Coro afrontado',129:'Pulmon afrontado',130:'Cencerro afrontado',131:'Pastor hueco vencido',132:'PACTO contra Cripps',133:'PACTO nadie es ganado',134:'PACTO venganza',135:'Ruta V desbloqueada',136:'Susto10 visto',137:'Susto11 visto',138:'Bajo la luz ante Muesca',139:'Dinamo afinada'}
VARIABLES={51:'Reputacion manada (-3..5)',52:'Bateria (0..100)',53:'Capturas',54:'Estado valvulas (0..2)',55:'Etapa (1..6)',56:'Reloj exploracion'}
ITEMS=[(30,'Linterna del colector','A: encender/apagar. S: recargar con una pila.'),(31,'Pila seca','Recarga 60 puntos. S en exploracion o usar aqui.'),(32,'Rueda de valvula','Encaja en el retorno del tramo inundado.'),(33,'Chapa del pacto','Contra Cripps. El limite elegido permanece.'),(34,'Croquis del colector','Cerrar retorno antes de abrir descarga. Altar al este.')]
NOTAS={30:'LINTERNA: A alterna la luz; S usa una pila seca (+60). Solo consume al explorar. En la oscuridad sube el veneno hasta 96. Altar: recarga completa gratuita.',31:'PILA SECA: solo se gasta si falta carga. Recarga hasta sesenta puntos; no puedes desperdiciarla con bateria llena.',32:'RUEDA: se monta en RETORNO. Primero cerrar retorno, despues abrir descarga. No inundar el altar.',33:'PACTO: abrir el matadero contra Cripps. La eleccion de Steven sobre el control y la venganza queda registrada para los actos V y VI.',34:'CROQUIS: entrada -> tuneles -> agua -> camara. Ramal seco de tuneles -> altar. RETORNO cerrado antes que DESCARGA abierta. Nicho de sacos y armario de bombas son escondites.'}
def notas():
    return [IF(c_script('$vacas_ultimo_objeto == %d'%i),[T(text)]+([IF(c_script('Vacas.bajo_ciudad?'),[IF(c_script('Vacas.recargar'),[T('Pila instalada. La linterna vuelve a encenderse.')],[T('No necesitas gastar una pila ahora.')])])] if i==31 else [])) for i,text in NOTAS.items()]
