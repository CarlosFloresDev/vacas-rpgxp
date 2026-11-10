"""Acto V «La matanza»: eventos de los mapas 22-27. Texto original en castellano."""

# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
from ev import *
from ev import _wrap
from contenido_sistemas import battle

KEYS = {'Steven': 'steven', 'La Guernsey': 'guernsey', 'Cripps': 'cripps', 'Muesca': 'muesca', 'Junco': 'junco',
        'El Rubio': 'rubio', 'El Chato': 'chato', 'Sierra': 'sierra', 'Benito': 'benito'}
def say(name, text, exp=None):
    exp = exp or ('susurro' if name == 'La Guernsey' else 'neutral')
    side = 'L' if name == 'Steven' else 'R'
    dim = 1 if name in ('Cripps', 'La Guernsey') else 0
    lines = _wrap(text); out = []
    for i in range(0, len(lines), 4):
        out.append(cmd(101, '\\P[%s_%s]\\%s\\D[%d]\\NOMBRE[%s]' % (KEYS[name], exp, side, dim, name) + lines[i]))
        out.extend(cmd(401, t) for t in lines[i + 1:i + 4])
    return ('L', out)

def snd(key): return SCRIPT('Vacas_Audio.play(:%s)' % key)
def alarma(n=1): return SCRIPT('matanza_alarma(%d)' % n)
def tension(n): return SCRIPT('matanza_tension(%d)' % n)
def dominio(n): return SCRIPT('matanza_inclinar(58,%d)' % n)
def piedad(n): return SCRIPT('matanza_inclinar(59,%d)' % n)
def rep(n): return SCRIPT('Vacas.reputacion(%d)' % n)
def inv(m, name, x, y, cmds, **kw): return m.add(name, x, y, [page(cmds, **kw)])
def una_vez(m, name, x, y, cmds, despues):
    return m.add(name, x, y, [page(cmds + [SS()]), page(despues, ss='A')])
def amb(m, r, g, b, gray):
    m.add('Noche de matanza', 0, 0, [page([TONE(r, g, b, gray, 0), ERASE], trigger=4)])
def entrada(m, cmds):
    m.add('Primera vez', 1, 0, [page(cmds + [SS()], sw1=140, trigger=3), page([], ss='A')])
def toque(m, name, x, y, cmds): m.add(name, x, y, [page(cmds, trigger=1)])
def descubierto(m, quien, frase, x, y, d):
    m.add('Descubierto', 0, 2, [page([], through=True), page([
        say(quien, frase), SCRIPT('matanza_descubierto'),
        T('Sueltas lo que llevas en las manos y corres agachado. La ALARMA sube un punto. No has perdido nada.'),
        TRANSFER(m.map_id, x, y, d)], sw1=142, trigger=3)])
def patrulla(n):
    return route(steps(RIGHT, n) + [mwait(40), turn(4), mwait(30)] + steps(LEFT, n) + [mwait(40), turn(6), mwait(30)], True, True)
def vaca(m, x, y, d, char='vacas_vaca', libre=True):
    pages = [page([], char=char, d=d, dirfix=True, walk=False)]
    if libre: pages.append(page([], sw1=145, sw2=151, through=True))
    m.add('Res en espera', x, y, pages)
def guardar(m, x, y, nombre='Radio de la garita'):
    inv(m, nombre, x, y, [T('Un transistor con la antena doblada. Entre la estática, el parte agrario de madrugada lee precios por kilo.'),
        CHOICE(['Guardar', 'Escuchar un momento', 'Dejarlo'], [[SAVE], [IF(c_ss('A', False), [T('Precios por kilo en canal. Nadie dice cuántas. Por alguna razón eso te calma: es una voz que no te pide nada.'), VEN(-6), SS()],
            [T('La misma voz repite los mismos precios.')])], []])])

# ------------------------------------------------------------------ 22 Muelle de carga
def muelle():
    m = MapEvents(22); amb(m, -52, -48, -30, 30)
    m.add('Llegada al muelle', 1, 0, [page([
        T('La rejilla cede hacia arriba. Huele a gasóleo, a paja meada y a lejía. El matadero nunca había tenido todas las luces encendidas a esta hora.'),
        say('La Guernsey', 'Trescientas doce de las nuestras esperan en los corrales. Cripps quiere las cámaras llenas antes de que amanezca. La llaman la gran matanza.'),
        IF(c_sw(133), [say('La Guernsey', 'Abre las puertas. Corta la sirena. Los del turno de noche no son el capataz: que oigan las pezuñas a tiempo de apartarse.')],
           [say('La Guernsey', 'Abre las puertas y no avises a nadie. Lo que la manada encuentre en la nave, la manada lo cobra. Eso pactaste.')]),
        say('Steven', 'Primero las llaves. La garita del vigilante está al otro lado del muelle.', 'miedo'),
        T('INFILTRACIÓN. Los vigilantes ven en línea recta, cinco pasos, hacia donde miran, y también si los rozas. Si te descubren sube la ALARMA (máximo 3): con la alarma alta, Cripps estará más despierto. La radio de la garita permite guardar.'),
        SW(141)], sw1=140, trigger=3), page([], sw1=141)])
    descubierto(m, 'Benito', '¿Quién anda ahí? ¡El muelle está cerrado hasta el alba!', 3, 11, 8)
    m.add('Vigia A5', 2, 6, [page([], char='vacas_obrero1', d=6, move_type=3, speed=2, freq=6, mroute=patrulla(11)), page([], sw1=151, through=True)])
    guardar(m, 16, 5)
    una_vez(m, 'Tablero de llaves', 18, 4, [T('En el tablero quedan dos ganchos ocupados: la llave de servicio del muelle y una cizalla de precintar. Te llevas las dos. Has recibido LLAVE DEL MUELLE y CIZALLA.'), snd('llaves_tintineo'), ITEM(35), ITEM(36), VAR(61, 2)],
            [T('Ganchos vacíos y etiquetas escritas a mano: CORRALES, NORIA, CÁMARAS. La de OFICINA no ha estado nunca aquí.')])
    inv(m, 'Parte de turno', 18, 6, [T('Parte nocturno, pegado con cinta sobre la estufa: «Entran 312 cabezas. Portón cerrado hasta el alba. Sirena de corrales probada. Nadie sale sin que yo lo diga. —Cripps».')])
    inv(m, 'Puerta de servicio', 4, 2, [IF(c_item(35), [snd('puerta_metal_pesada_abrir'), TRANSFER(23, 12, 13, 8)], [T('Puerta de servicio a corrales. Cerrada. Por la rendija sale calor de animal y un mugido que alguien corta en seco.')])])
    inv(m, 'Cartel del muelle', 6, 2, [T('«MUELLE 2 — GANADO VIVO. Prohibido el paso a personal sin turno». Debajo, a boli: «y con turno también».')])
    inv(m, 'Camion vacio', 7, 9, [T('Las tablas del remolque aún están tibias. Entre dos listones, un mechón de pelo canela. El conductor dejó la radio encendida y las llaves no.')])
    una_vez(m, 'Camion de la res', 12, 11, [T('Dentro del segundo camión queda una. No pudo bajar la rampa. Respira deprisa, con los ojos muy abiertos, y te mira las manos antes que la cara.'), tension(3)],
            [T('La res del camión sigue respirando. No puedes moverla tú solo. Todavía.')])
    inv(m, 'Rejilla de la manada', 3, 12, [IF(c_sw(145), [say('La Guernsey', 'Oímos caer las cadenas. Ahora la nave. Para la noria y abre el camino del sangrado.')],
        [say('La Guernsey', 'Seguimos debajo. Cuando oigas el portón, aparta. No vamos a mirar por dónde pisamos hasta haber entrado.')])])
    una_vez(m, 'Contenedor', 17, 12, [T('Levantas la tapa. Cuernos serrados, pezuñas, un cubo de ojos que nadie compra. Lo que sobra de trescientas doce veces lo mismo.'), tension(2)], [T('No vuelves a levantar la tapa.')])
    inv(m, 'Sacos del muelle', 11, 3, [T('Sacos de sal gorda para las pieles. Uno está abierto: alguien ha metido la mano y se ha llevado un puñado.')])
    return m

# ------------------------------------------------------------------ 23 Corrales de espera
def corrales():
    m = MapEvents(23); amb(m, -44, -38, -36, 35)
    entrada(m, [T('Corrales de espera. Trescientas doce respiraciones en cinco corrales pensados para ochenta. El vapor sube de los lomos hasta las lámparas.'),
                say('Steven', 'El de la sierra hace la ronda por el pasillo central. La caseta del corralero está al fondo, a la derecha.', 'miedo')])
    descubierto(m, 'Sierra', '¡Eh! ¡Tú! ¡Aquí no entra nadie esta noche!', 12, 13, 8)
    m.add('Vigia A5', 2, 8, [page([], char='vacas_obrero2', d=6, move_type=3, speed=2, freq=6, mroute=patrulla(14)), page([], sw1=143, through=True), page([], sw1=151, through=True)])
    aliada = lambda quien, frase, frase2: [IF(c_sw(143), [say(quien, frase2)], [say(quien, frase),
        CHOICE(['Pedirle que aleje al vigilante', 'Mejor no'], [[SW(143), T('Un golpe de pezuña contra la chapa del fondo, luego otro, sin prisa. El hombre de la sierra deja la ronda y va a mirar una puerta que no deja de sonar.')], []])])]
    m.add('Aliada en el pasillo', 6, 11, [page([], through=True),
        page(aliada('Muesca', 'Has tardado. El de la sierra cuenta sus pasos; yo le cuento los descuidos. ¿Lo aparto?', 'Lo tengo mirando una puerta. Si vuelve, no respondo de mí.'), var=(51, 1), char='vacas_muesca', dirfix=True, walk=False),
        page(aliada('Junco', 'Me dejaste sacar la pata yo sola. Puedo hacer ruido donde no estés tú. ¿Quieres?', 'Sigue mirando la puerta. Los hombres siempre miran la puerta equivocada.'), sw1=126, var=(51, 1), char='vacas_junco', dirfix=True, walk=False),
        page([], sw1=151, through=True)])
    una_vez(m, 'Rejilla del corral', 6, 2, [say('La Guernsey', 'Esta rejilla la conoces. Por aquí te hablé la primera vez, cuando todavía creías que el miedo era tuyo.'), VEN(-4)],
            [say('La Guernsey', 'Las cadenas, Steven. Y la sirena, si no quieres que Cripps baje antes de tiempo.')])
    inv(m, 'Tablero de recuento', 12, 2, [T('Palotes de tiza en grupos de cinco. Sesenta y dos grupos y dos palotes sueltos. Alguien ha escrito debajo: «312 — ni una menos al alba».')])
    cadena = [IF(c_sw(145), [T('Sin cadena. Las reses no salen todavía: esperan una señal que no es la tuya.')], [IF(c_item(36), [
        IF(c_sw(153, False), [T('Apoyas la cizalla en el primer eslabón. Al fondo del corral una res empieza a contar en voz baja. Cuenta golpes. Cuenta cabezas. Te cuenta a ti.')]), battle(19, 153),
        CHOICE(['Cortar todas las cadenas', 'Dejarlas cerradas'], [
            [snd('cadena_gancho'), T('Cinco cadenas, cinco mordiscos secos. Las puertas quedan entornadas. Ninguna res sale: se apartan del hueco como si quemara y esperan.'), SW(145), piedad(2), rep(1), VAR(61, 3),
             IF(c_sw(134), [T('La chapa del pacto te pesa en el bolsillo. No las has soltado: has soltado trescientas doce razones más contra Cripps.')])],
            [T('Guardas la cizalla. Si la nave se llena de pezuñas, que sea solo con las que bajaron contigo.')]])],
        [T('Cadena y candado en cada puerta. Con las manos no. En la garita del muelle había herramienta.')])])]
    for i, (x, y) in enumerate([(3, 6), (9, 6), (15, 6), (3, 9), (9, 9)]): inv(m, 'Cadena del corral %d' % (i + 1), x, y, cadena)
    inv(m, 'Sirena de corrales', 16, 10, [IF(c_sw(144), [T('La sirena cuelga de un cable cortado. Si alguien pulsa la alarma, sonará un clic y nada más.')], [IF(c_item(36),
        [T('Sigues el cable de la sirena hasta la grapa y lo cortas. Queda colgando como una tripa seca. Has cortado la SIRENA: parar la cadena ya no despertará a nadie.'), snd('cuchilla_corte_de_carne'), SW(144)],
        [T('SIRENA DE CORRALES. Salta sola si la cadena de izado se detiene. El cable baja grapado por la pared; hace falta algo que corte.')])])])
    una_vez(m, 'Orden de matanza', 18, 10, [T('ORDEN DE MATANZA EXTRAORDINARIA. «Vaciar corrales en un solo turno. Lotes sin etiqueta a cámara 3. Sanidad no pasa hasta el lunes». Firmado: Cripps. Te la guardas.'), snd('papel_nota'), ITEM(38), SW(164)],
            [T('En el corcho queda la chincheta y la sombra clara del papel.')])
    for x, y, d in [(2, 3, 2), (4, 5, 4), (9, 3, 6), (8, 5, 2), (10, 4, 2), (15, 4, 4), (16, 5, 2), (3, 10, 2), (2, 12, 6), (9, 11, 4), (10, 12, 2)]:
        vaca(m, x, y, d, 'vacas_vaca_canela' if (x + y) % 3 == 0 else 'vacas_vaca')
    inv(m, 'Sacos de pienso', 18, 4, [T('Pienso de engorde. Nadie lo ha abierto: a las que van a morir de madrugada no se les echa de cenar.')])
    toque(m, 'Manga a la nave', 19, 7, [TRANSFER(24, 1, 7, 6)])
    toque(m, 'Vuelta al muelle', 12, 14, [TRANSFER(22, 4, 3, 2)])
    return m

# ------------------------------------------------------------------ 24 Sala de matanza
def sala():
    m = MapEvents(24); amb(m, -30, -34, -30, 30)
    entrada(m, [T('La sala de matanza. La noria iza sola, el cajón golpea solo y la cinta se lleva las cajas de vísceras a ninguna parte. Dos hombres del turno de noche siguen el ritmo sin mirarlo.')])
    obreros = [IF(c_sw(146), [say('El Rubio', 'Tú a lo tuyo, chaval. Nosotros no hemos visto a nadie.')], [
        say('El Rubio', '¿Steven? Tú no tienes turno. Nadie con dos dedos de frente tiene turno hoy.'),
        say('El Chato', 'Doble jornal por no hacer preguntas. Trescientas doce antes del alba. El capataz está arriba, contando.'),
        CHOICE(['Avisarles: «Marchaos ya»', 'Mentir: «Me manda Cripps»', 'Callar y seguir'], [
            [say('Steven', 'Dejad los cuchillos. Dentro de un rato esta nave no va a ser de los que matan.'), say('El Rubio', 'Lo dices como quien ya lo ha visto.'),
             say('El Chato', 'A mí no me pagan para morirme. Vámonos por el vestuario, Rubio.'), SW(146), SW(147), piedad(1),
             T('Los dos cuelgan los mandiles y se van sin correr. Nadie te verá tocar el cuadro.')],
            [say('Steven', 'Me manda Cripps. Revisión del cuadro de la noria.', 'miedo'), say('El Rubio', 'Pues revisa. Y dile que el perno del dos pierde aire.'), SW(146), dominio(1),
             T('Te han creído. Se quedan en su puesto: cuando entre la manada, seguirán aquí.')],
            [say('El Chato', 'Raro fuiste siempre.'), T('No dices nada. Te siguen con la vista.')]], 3)])]
    m.add('El Rubio', 8, 8, [page(obreros, char='vacas_obrero3', d=8, dirfix=True), page([], sw1=147, through=True), page([], sw1=151, through=True)])
    m.add('El Chato', 16, 6, [page(obreros, char='vacas_obrero4', d=4, dirfix=True), page([], sw1=147, through=True), page([], sw1=151, through=True)])
    exito = [SW(148), snd('cadena_gancho'), T('La noria se queja, se para y empieza a girar al revés. Las reses que subían colgadas de una pata bajan despacio hasta el suelo. La puerta del raíl se desenclava.'), VAR(61, 4),
             IF(c_sw(144), [T('La sirena de corrales hace clic y nada más. El cable cortado cuelga en su caseta.')],
                [snd('susto'), T('La sirena de corrales salta: un aullido largo por toda la nave. Arriba se enciende una luz. La ALARMA sube un punto.'), alarma(1)])]
    fallo = [T('La cadena se traba, escupe grasa y vuelve a su sentido. Demasiados cables cruzados mal. Puedes intentarlo otra vez: la próxima bastará con ocho.'), SW(169), tension(3)]
    m.add('Cuadro de la noria', 15, 8, [page([IF(c_sw(148), [T('La noria gira al revés. En el cuadro, la luz verde parpadea como un ojo con sueño.')], [
        IF(c_sw(146, False), [IF(c_ss('A', False), [T('El Chato levanta la vista del cuchillo al oír la puerta del cuarto de control. No dice nada. Lo apunta. La ALARMA sube un punto.'), alarma(1), SS()])]),
        T('CUADRO DE LA NORIA. La cadena de izado sube las reses al raíl de sangrado. Invertirla baja lo que está colgado y desbloquea la puerta del raíl. Piezas ROJAS: pulsa su flecha. Piezas AZULES, cables cruzados: pulsa la CONTRARIA. Hacen falta diez de dieciséis.'),
        CHOICE(['Invertir la cadena', 'Todavía no'], [[SCRIPT('minijuego_noria(16)'),
            IF(c_var(12, 10, 1), exito, [IF(c_sw(169), [IF(c_var(12, 8, 1), exito, fallo)], fallo)])], []])])])])
    m.add('Armero del aturdido', 15, 12, [page([IF(c_sw(149), [T('El armero está vacío. Queda la silueta de la pistola pintada en el fondo, para que nadie olvide dónde se devuelve.')], [
        T('El armero del aturdido. Dentro, la pistola de perno cautivo, limpia, engrasada. Al tocarla notas en la muñeca todas las veces que alguien te sujetó la mano.'), battle(18, 154),
        T('Te llevas la PISTOLA DE PERNO. Un solo cartucho. No sabes todavía para quién.'), snd('recoger_objeto'), ITEM(37), SW(149), dominio(1)])])])
    inv(m, 'Cajon de aturdir', 7, 7, [T('El cajón de aturdir. La compuerta sube y baja sola cada nueve segundos. Dentro no hay nadie. El suelo de dentro está más gastado que el de fuera.')])
    inv(m, 'Noria de izado', 8, 7, [IF(c_sw(148), [T('La noria baja lo que antes subía. Una cadena suelta golpea el poste a cada vuelta.')], [T('La noria de izado. Un gancho pasa, se lleva lo que encuentra y vuelve vacío. No distingue.')])])
    inv(m, 'Puerta del rail', 17, 2, [IF(c_sw(148), [snd('puerta_metal_pesada_abrir'), TRANSFER(25, 17, 13, 8)], [T('Enclavamiento de seguridad: la puerta del sangrado solo abre con la noria parada o invertida. El cuadro está en el cuarto de control, al este.')])])
    una_vez(m, 'Fregadero', 1, 3, [T('Te lavas las manos con agua casi hirviendo. El jabón huele a sebo. Durante unos segundos solo existe el agua.'), VEN(-5)], [T('El agua sale ya fría.')])
    inv(m, 'Cuadro de fusibles', 17, 8, [T('Fusibles etiquetados con esparadrapo: «NORIA», «CINTA», «SIRENA CORRALES — salta si para la noria». El cable de la sirena sale hacia los corrales.')])
    inv(m, 'Canal recien colgada', 13, 4, [T('Todavía gotea. En la paletilla, el sello azul de sanidad está puesto antes de que nadie haya mirado nada.')])
    inv(m, 'Mesa de triperia', 2, 13, [T('Cuchillos ordenados por tamaño. Alguien ha dibujado con sangre seca una casita con humo en el acero. El turno de noche es largo.')])
    inv(m, 'Almanaque', 13, 8, [T('Un almanaque de piensos compuestos. La fecha de hoy está rodeada tres veces. Debajo: «312».')])
    toque(m, 'Manga a corrales', 0, 7, [TRANSFER(23, 18, 7, 4)])
    return m

# ------------------------------------------------------------------ 25 Camara de sangrado
def sangrado():
    m = MapEvents(25); amb(m, -54, -30, 4, 45)
    m.add('Primera vez', 1, 0, [page([T('La cámara de sangrado. Tres raíles, tres canales rojos en el suelo, y las reses de la noche colgadas tan juntas que hay que pasar de lado. Hace un frío que huele a hierro.'),
        say('Steven', 'La escalera de la oficina está al fondo, a la izquierda. Tengo que cruzar entre ellas.', 'miedo'), SW(152)], sw1=140, trigger=3), page([], sw1=152)])
    cripps = m.reserve('Cripps caza')
    m.add('Empieza la caza', 0, 3, [page([], through=True), page([IF(c_script('$game_player.y <= 7'), [
        EVLOC(cripps, 2, 3, 2), snd('puerta_de_hierro'), say('Cripps', 'Sabía que eras tú. Las ratas vuelven siempre por donde huele a ellas.', 'ira'),
        say('Cripps', 'Ven aquí, Steven. Te voy a colgar entre dos buenas piezas, que aprendas.', 'ira'), SCRIPT('susto(12)'),
        IF(c_var(51, 2, 1), [T('PERSECUCIÓN. Aguanta 30 segundos: la manada ya está en la manga. Cripps conoce el camino entre las canales. Hay dos canales vaciadas donde esconderte una vez cada una.'), TIMER(30)],
           [T('PERSECUCIÓN. Aguanta 40 segundos, hasta que la manada rompa el portón. Cripps conoce el camino entre las canales. Hay dos canales vaciadas donde esconderte una vez cada una.'), TIMER(40)]),
        MENUACCESS(False), SW(150), SCRIPT('Vacas_Audio.map_audio')]), WAIT(4)], sw1=152, trigger=4), page([], sw1=150, through=True), page([], sw1=151, through=True)])
    captura = [SCRIPT('matanza_captura'), FLASH(180, 20, 20, 200, 12), say('Cripps', '¡Te tengo, rata!', 'ira'),
               T('El gancho te abre el mono, no la carne. Te revuelves, resbalas en la sangre y ruedas bajo las canales hasta la puerta. La ALARMA sube. El reloj sigue corriendo.'),
               EVLOC(cripps, 2, 3, 2), TRANSFER(25, 17, 13, 8)]
    m.set('Cripps caza', 2, 3, [page([], through=True), page(captura, sw1=150, char='vacas_cripps', trigger=2, speed=3, freq=6),
                                 page(captura, sw1=150, var=(57, 2), char='vacas_cripps', trigger=2, speed=4, freq=6), page([], sw1=151, through=True)])
    m.add('Reloj de caza', 0, 1, [page([], through=True), page([IF(c_timer_le(0), [
        SCRIPT('matanza_fin_caza'), SHAKE(7, 6, 40), snd('mugido_grave_distorsionado'), T('Algo golpea el portón de corrales. Una vez. Otra. A la tercera, el portón ya no está.'),
        IF(c_sw(145), [T('Trescientas doce reses sin cadena empujan desde dentro mientras la manada empuja desde fuera. La nave entera se llena de lomos.')],
           [T('La manada entra sola por la manga. En los corrales, las encerradas mugen detrás de sus cadenas sin poder seguirla.')]),
        IF(c_sw(134), [T('No esquivan nada. Lo que hay en medio —mesas, cubos, cristal— cruje y queda atrás. Huele a pelo mojado y a algo recién abierto.')],
           [T('Pasan como pasa el agua: rodeando. Tumban mesas, no pisan a nadie que se haya quedado quieto.')]),
        say('Cripps', '¡Cerrad la nave! ¡CERRAD LA NAVE!', 'ira'),
        T('Nadie le contesta. Cripps suelta el gancho, te mira una sola vez y corre a la escalera de la oficina. Deja la puerta abierta detrás.'),
        IF(c_sw(147, False), [IF(c_sw(134), [T('Desde la sala de matanza llegan dos gritos, uno encima del otro, y luego solo pezuñas. El Rubio y el Chato no alcanzaron el vestuario.'), SW(171), dominio(1), tension(6)],
            [T('En la sala de matanza, el Rubio y el Chato se encierran en el cuarto de control con la espalda contra la puerta. Vivirán para contarlo mal.')])]),
        VAR(61, 5), SCRIPT('Vacas_Audio.map_audio')]), WAIT(4)], sw1=150, trigger=4), page([], sw1=151, through=True)])
    def escondite(nombre, x, y, flag, cx, cy):
        inv(m, nombre, x, y, [IF(c_sw(150), [IF(c_sw(flag), [T('Dentro ya no cabe el miedo de nadie más. ¡Corre!')], [
            CHOICE(['Meterte dentro', 'Seguir corriendo'], [[TRANSP(True), snd('sonido_viscoso'), SCRIPT('susto(13)'),
                T('Te encoges dentro de la canal abierta. Está tibia. Las costillas te quedan a la altura de los ojos, como una persiana.'), tension(4), EVLOC(cripps, cx, cy, 2), WAIT(140),
                T('El gancho de Cripps pasa golpeando las canales, una por una, y se aleja hacia el otro lado.'), TRANSP(False), SW(flag)], []])])],
            [T('Una canal abierta de arriba abajo y vaciada. Cabría un hombre encogido.')])])
    escondite('Canal vaciada', 13, 5, 165, 2, 13)
    escondite('Canal vaciada del centro', 7, 8, 166, 17, 3)
    inv(m, 'Ganchos de repuesto', 9, 2, [IF(c_sw(150), [T('¡Ahora no!')], [IF(c_sw(155), [T('Los ganchos cuelgan quietos. Uno tiene todavía tu aliento empañándolo.')],
        [T('Una barra de ganchos limpios. Uno se mueve solo, despacio, como un pecho que sube y baja.'), battle(20, 155)])])])
    inv(m, 'Puerta de la escalera', 2, 2, [IF(c_sw(151), [snd('puerta_metal_pesada_abrir'), TRANSFER(26, 3, 13, 8)], [IF(c_sw(150), [T('¡Cerrada! ¡Corre!')],
        [T('Cerrada por dentro. Al otro lado alguien baja la escalera despacio, arrastrando algo de metal por los peldaños.')])])])
    inv(m, 'Rejilla del sangrado', 12, 2, [IF(c_sw(151), [say('La Guernsey', 'Sube. Nosotras tardamos más con las escaleras.')], [say('La Guernsey', 'Estamos en la manga. Aguanta de pie. De pie se cuenta mejor.')])])
    inv(m, 'Termometro', 14, 2, [T('Dos grados. Debajo, escrito con rotulador: «la carne no se queja, el frío sí».')])
    inv(m, 'Carro de despojos', 18, 6, [T('Un carro lleno hasta arriba. Encima de todo, una lengua, entera, apuntando a la puerta.')])
    m.add('Vuelta a la sala', 17, 14, [page([IF(c_sw(150), [T('La puerta del raíl se ha enclavado detrás de ti.'), MOVE(-1, [UP]), WAITMOVE], [TRANSFER(24, 17, 3, 2)])], trigger=1)])
    return m

# ------------------------------------------------------------------ 26 Oficina alta
def oficina():
    m = MapEvents(26); amb(m, -34, -38, -46, 30)
    entrada(m, [T('La escalera de hierro acaba en una pasarela sobre la nave. Abajo, lomos. Arriba, una antesala con olor a papel húmedo y, al fondo, la luz de un flexo.'),
                T('La radio de la antesala permite guardar. Después de esa puerta no habrá otra ocasión.')])
    guardar(m, 1, 8, 'Radio de la antesala')
    inv(m, 'Cajas de etiquetas', 1, 5, [IF(c_sw(97), [T('Cajas de etiquetas de lote sin usar. Los mismos números que llevas doblados en el bolsillo, en limpio, esperando una canal a la que mentir.')],
        [T('Cajas de etiquetas de lote sin usar. Rollos enteros de números que todavía no se han pegado a nadie.')])])
    inv(m, 'Archivo de bajas', 1, 3, [T('Partes de baja ordenados por año. «Dedo». «Mano». «No volvió». La letra es siempre la de Cripps; la firma del trabajador, casi nunca.')])
    inv(m, 'Reloj de fichar', 3, 2, [T('El reloj de fichar del turno de noche. Tu tarjeta sigue ahí, en la ranura de los que no volvieron, entre dos nombres tachados.')])
    inv(m, 'Banco de espera', 5, 5, [T('El banco donde se espera a que el capataz diga tu nombre. Encima, una carta de sanidad sin abrir, con fecha del mes pasado.')])
    m.add('Umbral de la oficina', 0, 4, [page([IF(c_script('$game_player.x >= 9 && $game_player.y <= 9'), [SW(167)]), WAIT(4)], sw1=140, trigger=4), page([], sw1=167, through=True)])
    escena = [
        say('Cripps', 'Cierra la puerta, Steven. Hay corriente y se me vuelan los papeles.'),
        IF(c_var(57, 2, 1), [say('Cripps', 'Te he oído venir desde el muelle. Haces más ruido que una res con tres patas.')],
           [say('Cripps', 'No te he oído subir. Eso te lo enseñé yo: se entra despacio y se sale con las manos limpias.')]),
        IF(c_sw(97), [say('Cripps', 'Los lotes. ¿Crees que esos números me señalan a mí? Señalan a todos los que comieron sin preguntar.')],
           [say('Cripps', 'Dicen que cuidas a una enferma. Yo cuido a una ciudad entera: come porque yo no hago preguntas.')]),
        say('Steven', 'Trescientas doce en una noche. ¿Para tapar qué?', 'miedo'),
        say('Cripps', 'Para tapar nada. Para vaciar los corrales antes de que tus amigas de abajo aprendieran a abrir puertas. Tarde. Ya las oigo.'),
        say('Cripps', 'Tú y yo hacemos lo mismo, chico. Yo cobro por ello. Tú necesitas que te lo pidan por favor.', 'ira'),
        T('Cripps levanta el gancho. La oficina se alarga como una manga de conducción y al fondo solo queda un cajón con la compuerta abierta.'),
        SCRIPT('matanza_jefe'), battle(21, 156, True),
        T('Cripps está sentado en el suelo, contra la caja fuerte, con el gancho lejos de la mano. Respira por la boca. Fuera, las pezuñas suben la escalera de hierro de una en una.'),
        IF(c_sw(133), [say('La Guernsey', 'Está hecho, Steven. Dijiste que nadie es ganado. Él también cuenta, aunque nos pese. Decide de quién es.')],
           [say('La Guernsey', 'Está hecho, Steven. Prometiste que pagaría. Falta decidir quién cobra.')]),
        CHOICE(['Abrir la puerta a la manada', 'Apretar tú el perno', 'Dejarle la escalera de incendios'], [
            [SW(160), say('Steven', 'No es mío. Nunca fue mío.'), TONE(-255, -255, -255, 0, 30), WAIT(30),
             T('Abres la puerta de la oficina y te apartas contra la pared. No miras. Oyes entrar a la primera, despacio, y a Cripps decir un nombre que no es el de nadie.'), snd('mugido_grave_distorsionado'),
             T('Luego oyes lo demás. Dura menos de lo que duraba un turno.'), rep(1), IF(c_sw(134), [dominio(1), T('Cuando vuelve el silencio, todas te miran a ti. Esperan la orden siguiente.')]), TONE(-34, -38, -46, 30, 40)],
            [SW(161), IF(c_item(37), [T('La pistola de perno pesa lo mismo que el primer día. La apoyas donde él te enseñó: dos dedos por encima de la línea de los ojos.')],
                [T('No tienes la pistola. El gancho está a tu alcance y sabes usarlo: él te enseñó.')]), TONE(-255, -255, -255, 0, 20), WAIT(20), snd('hueso_quebrado'),
             T('Un golpe seco. El mismo sonido de siempre. Lo único nuevo es que esta vez nadie te sujetaba la mano.'), dominio(2), tension(8), rep(-1),
             say('La Guernsey', 'Lo has hecho bien. Como él. Eso es lo que voy a recordar.'), TONE(-34, -38, -46, 30, 40)],
            [SW(162), say('Steven', 'La escalera de incendios. Vete. Corre lo que sepas.'), say('Cripps', 'Eso no es piedad, chico. Eso es no querer mancharte.'),
             T('Cripps sale cojeando por la pasarela. Lo oyes bajar los peldaños de dos en dos. Lo oyes llegar al patio. Luego oyes que el patio no estaba vacío.'), snd('mugido_angustiado'),
             piedad(2), rep(-2), say('La Guernsey', 'Teníamos un pacto. Lo has cumplido con las patas de otras. Ya hablaremos de lo que eso te hace.')]], 0),
        SW(159), VAR(61, 6), T('La puerta de la escalera de incendios queda abierta al fondo de la pasarela. Por el ventanal entra una luz gris: amanece.')]
    m.add('Cripps en su mesa', 13, 4, [page([say('Cripps', 'Pasa, hombre. No muerdo.')], char='vacas_cripps', d=2, dirfix=True, walk=False),
                                        page(escena, sw1=167, char='vacas_cripps', d=2, dirfix=True, walk=False, trigger=3), page([], sw1=159, through=True)])
    m.add('La Guernsey en la oficina', 9, 6, [page([], through=True), page([IF(c_sw(160), [say('La Guernsey', 'No pediste su carne ni su silla. Abajo ya hay quien te llama de otra manera.')],
        [IF(c_sw(161), [say('La Guernsey', 'Límpiate las manos antes de bajar. Las pequeñas se fijan en todo.')], [say('La Guernsey', 'Baja al patio. Lo que queda de él está junto a la cancela.')])])], sw1=159, char='vacas_guernsey4', d=6, dirfix=True, walk=False)])
    una_vez(m, 'Caja de cencerros', 18, 7, [T('Una caja de cencerros con muescas hechas a navaja. Uno por cada res que habló antes de callar. El de arriba tiene una muesca reciente y un nombre: GUERNSEY, con interrogación.'), tension(2)],
            [T('Los cencerros no suenan aunque muevas la caja. Alguien les quitó el badajo a todos.')])
    inv(m, 'Caja fuerte', 18, 9, [IF(c_sw(159), [T('La caja fuerte está abierta. Sobres con membrete de sanidad, billetes sujetos con gomas y una foto de un niño con un ternero. Por detrás: «el primero».')],
        [T('La caja fuerte de Cripps. Nadie que tú conozcas ha visto nunca la combinación.')])])
    inv(m, 'Ventanal de la nave', 10, 2, [IF(c_sw(159), [T('Abajo, la nave es un río lento de lomos. Ninguna corre ya. Alguien ha parado la cinta.')], [T('El ventanal da a la nave. Desde aquí arriba los hombres y las reses tienen el mismo tamaño.')])])
    inv(m, 'Trofeos', 12, 2, [T('Cráneos barnizados con la fecha en la frente. El más pequeño no es de vaca adulta.')])
    inv(m, 'Sofa de escay', 9, 9, [T('Un sofá de escay con la forma de un solo cuerpo. Entre los cojines, una petaca y una lista de nombres del turno. El tuyo está subrayado.')])
    m.add('Escalera de incendios', 19, 12, [page([IF(c_sw(159), [TRANSFER(27, 3, 3, 2)], [T('La escalera de incendios baja al patio. Todavía no. Cripps está en su oficina.'), MOVE(-1, [LEFT]), WAITMOVE])], trigger=1)])
    toque(m, 'Bajada al sangrado', 3, 14, [TRANSFER(25, 2, 3, 2)])
    return m

# ------------------------------------------------------------------ 27 Patio del alba
def patio():
    m = MapEvents(27); amb(m, -26, -28, -14, 20)
    entrada(m, [T('Amanece sobre el patio de camiones. La cancela está abierta de par en par y nadie la vigila. La manada ocupa el asfalto sin formar filas.'),
                IF(c_sw(162), [T('Junto al barro de la cancela hay una gorra verde pisoteada y una mancha que va oscureciéndose. Nadie la rodea ya.')]),
                IF(c_sw(171), [T('Dos mandiles cuelgan de la alambrada. Alguien, o algo, los ha dejado ahí a la vista.')])])
    final = [IF(c_sw(160), [say('La Guernsey', 'No pediste su carne ni su silla. Abajo ya te llaman de otra manera. No corrijas a nadie todavía.')]),
             IF(c_sw(161), [say('La Guernsey', 'Has matado bien. Eso es lo que me preocupa. Abajo te seguirán. Procura mirar atrás de vez en cuando.')]),
             IF(c_sw(162), [say('La Guernsey', 'Nos abriste y te apartaste. La manada no sabe si eso es respeto o asco. Yo tampoco.')]),
             IF(c_sw(133), [say('La Guernsey', 'Dijiste que nadie es ganado. Hoy hay trescientas bocas más que van a preguntarte qué son entonces.')],
                [say('La Guernsey', 'Querías que pagara y ha pagado. La manada ha probado algo esta noche. No va a querer volver al pienso.')]),
             say('Steven', 'La ciudad se va a despertar sin carne.', 'miedo'),
             say('La Guernsey', 'La ciudad se va a despertar. Tu madre también. Baja con nosotras o vuelve a tu piso: las dos escaleras siguen ahí. Pero no tardes.'), SW(168)]
    m.add('La Guernsey en el patio', 10, 8, [page(final, char='vacas_guernsey4', d=2, dirfix=True, walk=False), page([say('La Guernsey', 'La cancela está abierta. Cuando quieras.')], sw1=168, char='vacas_guernsey4', d=2, dirfix=True, walk=False)])
    m.add('Muesca en el patio', 7, 9, [page([IF(c_sw(134), [say('Muesca', 'Ha sabido a poco. Hay más puertas como esta en la ciudad.')], [say('Muesca', 'Ningún collar. Ninguna fila. No sé qué hacer con las patas cuando nadie empuja.')])], char='vacas_muesca', d=6, dirfix=True, walk=False)])
    m.add('Junco en el patio', 13, 9, [page([], through=True), page([say('Junco', 'La pata duele. He subido una escalera con ella. Pueden ser ciertas las dos cosas.')], sw1=126, char='vacas_junco', d=4, dirfix=True, walk=False)])
    for (x, y, d, c), t in zip([(4, 9, 6, 'vacas_vaca'), (16, 9, 4, 'vacas_vaca_canela'), (12, 11, 2, 'vacas_vaca'), (6, 12, 8, 'vacas_vaca_canela'), (16, 12, 2, 'vacas_vaca')],
                               ['Tiene todavía la marca de tiza del recuento en el lomo. Te huele la manga y no se aparta.', 'Mastica algo que no es pienso. Prefieres no mirar qué.',
                                'Mira el cielo como quien mira un techo demasiado alto.', 'Tiembla de pie. No es frío.', 'Se ha tumbado en el barro, por primera vez con sitio para hacerlo.']):
        m.add('Res en el patio', x, y, [page([T(t)], char=c, d=d, dirfix=True, walk=False)])
    m.add('El Rubio en la cancela', 17, 11, [page([], through=True), page([say('El Rubio', 'No sé qué eres ahora, Steven. Pero avisaste. Eso no se me olvida.')], sw1=147, char='vacas_obrero3', d=4, dirfix=True)])
    m.add('El Chato en la cancela', 18, 11, [page([], through=True), page([say('El Chato', 'Yo no vuelvo. Que mate otro. O que no mate nadie, me da igual.')], sw1=147, char='vacas_obrero4', d=4, dirfix=True)])
    inv(m, 'Camion abierto', 15, 6, [T('La rampa del camión está bajada. Dentro no queda nadie. En la chapa, por dentro, cientos de marcas de pezuña a la misma altura.')])
    inv(m, 'Puerta de incendios', 3, 2, [TRANSFER(26, 18, 12, 4)])
    cierre = [IF(c_sw(168), [CHOICE(['Guardar y cerrar el acto', 'Quedarme un momento'], [[SAVEACCESS(True), SAVE, SW(163), SCRIPT('$scene = Scene_FinActo.new(5)')], [MOVE(-1, [UP]), WAITMOVE]])],
                 [T('La Guernsey te espera en mitad del patio. No se sale de una noche así sin hablar.'), MOVE(-1, [UP]), WAITMOVE])]
    m.add('Cancela abierta', 9, 13, [page(cierre, trigger=1)])
    m.add('Cancela abierta', 10, 13, [page(cierre, trigger=1)])
    return m

MAPAS = [muelle, corrales, sala, sangrado, oficina, patio]
SEEDS = {22: (3, 11), 23: (12, 13), 24: (1, 7), 25: (17, 13), 26: (3, 13), 27: (3, 3)}
SWITCHES = {140: 'Acto V activo', 141: 'Llegada al muelle vista', 142: 'Descubierto pendiente', 143: 'Vigia corrales distraido', 144: 'Sirena cortada', 145: 'Corrales abiertos',
            146: 'Obreros convencidos', 147: 'Obreros avisados', 148: 'Noria invertida', 149: 'Pistola de perno recogida', 150: 'Caza sangrado', 151: 'Manada dentro',
            152: 'Sangrado visto', 153: 'Res que cuenta afrontada', 154: 'Turno de noche afrontado', 155: 'Gancho afrontado', 156: 'Matarife vencido', 157: 'Susto12 visto',
            158: 'Susto13 visto', 159: 'DECISION tomada', 160: 'FINAL Cripps a la manada', 161: 'FINAL Steven aprieta el perno', 162: 'FINAL Cripps soltado', 163: 'Acto V completo',
            164: 'Orden de matanza leida', 165: 'Escondite 1 usado', 166: 'Escondite 2 usado', 167: 'Escena oficina', 168: 'Guernsey patio hablada', 169: 'Noria fallada', 171: 'Obreros muertos'}
VARIABLES = {57: 'Alarma (0..3)', 58: 'Dominio (0..6)', 59: 'Piedad (0..6)', 60: 'Capturas', 61: 'Etapa (1..6)'}
ITEMS = [(35, 'Llave del muelle', 'Abre la puerta de servicio a los corrales.'), (36, 'Cizalla de precintar', 'Corta cadenas de corral y el cable de la sirena.'),
         (37, 'Pistola de perno', 'Un cartucho. Dos dedos sobre la linea de los ojos.'), (38, 'Orden de matanza', '312 cabezas en un turno. Firmada por Cripps.')]
NOTAS = {35: 'LLAVE DEL MUELLE: puerta de servicio, en la pared norte del muelle. Los corrales quedan justo detras.',
         36: 'CIZALLA: corta las cadenas de los corrales (cualquier puerta sirve para todas) y el cable de la sirena en la caseta del corralero.',
         37: 'PISTOLA DE PERNO: un solo cartucho. Cripps te sujeto la mano la primera vez. Esta noche nadie te la sujeta.',
         38: 'ORDEN DE MATANZA: vaciar corrales en un turno, lotes sin etiqueta a camara 3, sanidad no pasa hasta el lunes. Es la letra de Cripps.'}
def notas():
    return [IF(c_script('$vacas_ultimo_objeto == %d' % i), [T(text)]) for i, text in NOTAS.items()]
ENEMIGOS = [(18,'turno_noche',0,'El Turno de noche', 340, 35, 68, 'Nadie me sujeta la mano. Es mía.'),
            (19,'res_cuenta',0,'La Res que cuenta', 330, 34, 65, 'Cuenta lo que quieras. Yo no soy un número.'),
            (20,'gancho_respira',0,'El Gancho que respira', 360, 36, 67, 'Es hierro. El hierro no respira. Respiro yo.'),
            (21,'cripps_matarife',0,'Cripps, el matarife', 860, 43, 70, None)]
