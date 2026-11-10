
# Rutas compartidas de herramientas; no ejecuta módulos de otros actos.
import sys as _sys
from pathlib import Path as _Path
_tools = next(p for p in _Path(__file__).resolve().parents if p.name == 'herramientas')
_sys.path.insert(0, str(_tools / 'comun'))
from rutas import ROOT as _ROOT, preparar_imports
preparar_imports()
# Contenido del Acto I de Vacas: todos los eventos. Texto original.
from ev import *

# ---------------------------------------------------------------- ids
S_INTRO, S_ORDENES, S_PERRO, S_JARABE, S_CARNE_C, S_CARNE_D, S_ANUNCIO, S_CENA = 1, 2, 3, 4, 5, 6, 7, 8
S_NOCHE, S_BUSQ, S_ESCONDIDO, S_BUSQ_FIN, S_MANANA, S_CONTRATADO = 9, 10, 11, 12, 13, 14
S_HUD_OFF, S_SIN_EFECTOS, S_PILLADO, S_PUERTA, S_ABRELATAS, S_LATA, S_TIEMPO = 15, 16, 17, 18, 19, 20, 21
V_VENENO, V_ETAPA, V_CANAL, V_VECES, V_AUX, V_INSULTO = 1, 2, 3, 4, 5, 6
I_LATA, I_ABRE, I_JARABE, I_LISTA, I_CARNE, I_ANUNCIO, I_LLAVE, I_FOTO = 1, 2, 3, 4, 5, 6, 7, 8
M_PROLOGO, M_PISO, M_ESC, M_CALLE = 1, 2, 3, 4

MADRE = "\\c[2]Madre:\\c[0] "
VOZ = "\\c[2]Voz de madre:\\c[0] "
PIENSA = "\\c[7]"
FIN = "\\c[0]"
AYUDA = "\\c[6]"

MUEBLES = "vacas_muebles"
COSAS = "vacas_cosas"

# tonos
def tono_dia(f=0): return TONE(18, 4, -38, 70, f)
def tono_noche(f=0): return TONE(-95, -85, -40, 90, f)
def tono_busqueda(f=0): return TONE(-50, -95, -95, 110, f)
def tono_manana(f=0): return TONE(-5, -12, -30, 95, f)
NEGRO = TONE(-255, -255, -255, 0, 30)

def mueble(lst, x, y, name, d, pat, ev=None, **kw):
    """Pagina de un mueble con grafico de vacas_muebles."""
    return page(lst, char=MUEBLES, d=d, pat=pat, dirfix=True, walk=False, **kw)

# ======================================================================
# MAPA 1: PROLOGO
# ======================================================================
def prologo():
    m = MapEvents(M_PROLOGO)
    m.add("Prologo", 9, 7, [page([
        TRANSP(True), MENUACCESS(False), SAVEACCESS(False),
        SW(S_HUD_OFF), SW(S_SIN_EFECTOS),
        PARTY_OUT(2), PARTY_OUT(7), PARTY_OUT(8),
        WAIT(60),
        BGS("001-Wind01", 45, 60),
        T("Hay un piso en la tercera planta de un bloque que\nnadie ha vuelto a pintar desde hace años."),
        T("Huele a grasa fría, a perro mojado y a algo más\ndulce, algo que nadie en el edificio nombra."),
        T("Ahí vive Steven. Tiene veinticinco años.\nNunca ha tenido una llave que fuera suya."),
        T("Ahí vive también ella. Steven la llama «madre»\nen voz alta. Por dentro la llama la Bestia."),
        T("Y ahí vive Perro, que ya no puede andar,\npero que todavía mueve la cola cuando le ven."),
        T("En el salón hay una tele vieja, de madera, de\nantes de que naciera nadie de la casa."),
        T("Cuando la tele está encendida, el mundo se\ncalla un poco. Solo un poco."),
        WAIT(30), STOPBGS(3), WAIT(40),
        SW(S_INTRO), VAR(V_ETAPA, 1), VAR(V_VENENO, 15),
        TRANSFER(M_PISO, 2, 4, 2),
        SS("A"),
    ], trigger=3), page([], ss="A")])
    return m

# ======================================================================
# MAPA 2: EL PISO
# ======================================================================
def piso():
    m = MapEvents(M_PISO)
    CAZA = m.reserve("Madre cazadora")      # id 1, referencia cruzada

    # ---------------- secuencias reutilizables
    def amanecer():
        return [
            SW(S_BUSQ, False), SW(S_ESCONDIDO, False), SW(S_NOCHE, False),
            SW(S_BUSQ_FIN), SW(S_MANANA), VAR(V_ETAPA, 6), TIMERSTOP,
            STOPBGM(3), STOPBGS(2), EVLOC(CAZA, 22, 7, 2),
            TONE(-255, -255, -255, 0, 20), WAIT(60),
            T("Amanece. La luz entra sucia por las ventanas,\ncomo si también hubiera tenido que pedir\npermiso."),
            IF(c_sw(S_PILLADO), [
                TRANSFER(M_PISO, 6, 12, 2),
                TRANSP(False), WAIT(10), tono_manana(60), WAIT(30),
                T("Te despiertas en el suelo del pasillo. Te duele\nel costado al respirar."),
                T("Perro se ha arrastrado hasta ti durante la noche.\nTiene la cabeza apoyada en tu mano."),
            ], [
                TRANSFER(M_PISO, 6, 5, 2),
                TRANSP(False), WAIT(10), tono_manana(60), WAIT(30),
                T("Sales del escondite con las piernas dormidas.\nLa casa está en silencio. Ella ronca en la\ncocina, sentada a la mesa."),
            ]),
            BGS("001-Wind01", 35, 60),
            T(VOZ + "Son las cinco y media. El camión del\nmatadero sale a las seis."),
            T(VOZ + "Si lo pierdes, no vuelvas. Ni a por el perro."),
            T(AYUDA + "(Baja a la calle y busca el camión del matadero.\nAntes puedes guardar en la tele.)" + FIN),
        ]

    def pillado():
        return [
            TIMERSTOP, STOPBGM(1), SW(S_ESCONDIDO, False),
            FLASH(255, 0, 0, 220, 20), SHAKE(9, 9, 30), SE("092-Attack04", 90, 70),
            T(MADRE + "¡AHÍ ESTÁS!"),
            TONE(-255, -255, -255, 0, 10), WAIT(20),
            SE("091-Attack03", 80, 60), WAIT(25), SE("092-Attack04", 80, 50), WAIT(40),
            T("Te saca a rastras, del pelo, por el pasillo.\nLo demás pasa a oscuras. Tu cuerpo lo\nrecuerda mejor que tú."),
            T(MADRE + "Mi dinero. MI dinero. En mi casa se\nrespeta lo mío."),
            VEN(35), SW(S_PILLADO),
            IF(c_script("veneno_al_maximo?"), [
                WAIT(30),
                T("Algo dentro de ti se llena hasta el borde.\nY se derrama."),
                WAIT(40), GAMEOVER,
            ]),
            amanecer(),
        ]

    def esconderse(tipo):
        if tipo == "armario":
            entrar = [TRANSFER(M_PISO, 7, 3, 8, False)]
            dentro = T("Te encierras dentro. Huele a naftalina y a un\nhombre que ya no existe. Por la rendija entra\nuna línea de luz amarilla.")
            ida = [EVLOC(CAZA, 5, 10, 8),
                   MOVE(CAZA, steps(UP, 4) + steps(RIGHT, 2) + steps(UP, 2) + [turn(8)])]
            vuelta = MOVE(CAZA, [turn(2)] + steps(DOWN, 2) + steps(LEFT, 2) + steps(DOWN, 4))
            cerca = T("Sus pasos se paran justo delante del armario.\nSu aliento entra por la rendija: jerez y carne.")
            mirar = "Mirar por la rendija"
            ojo = T("Acercas un ojo a la rendija.\nAl otro lado hay otro ojo. Enorme. Amarillo.\nTe estaba mirando desde el principio.")
            salida = (6, 5)
        else:
            entrar = [TRANSFER(M_PISO, 10, 5, 8, False)]
            dentro = T("Te metes en la bañera y te tumbas en el agua\nfría. Te empapa la espalda. No respiras.")
            ida = [EVLOC(CAZA, 12, 10, 8),
                   MOVE(CAZA, steps(UP, 5) + steps(LEFT, 1) + [turn(4)])]
            vuelta = MOVE(CAZA, [turn(6)] + steps(RIGHT, 1) + steps(DOWN, 5))
            cerca = T("Se para junto a la bañera. Ves su sombra sobre\nel agua sucia. Ves cómo se inclina.")
            mirar = "Asomar la cabeza"
            ojo = T("Levantas la cabeza del agua.\nElla está ahí, inclinada, con la boca abierta.\nComo si fuera a beber.")
            salida = (11, 6)
        return [CHOICE(["Esconderte aquí", "Mejor no"], [[
            SW(S_ESCONDIDO), TIMERSTOP, SE("024-Door01", 70, 80),
            TONE(-255, -255, -255, 0, 15), WAIT(15),
            entrar, TRANSP(True), WAIT(10), tono_busqueda(15),
            dentro,
            WAIT(30), SE("040-Knock01", 60, 50), WAIT(20),
            ida, WAITMOVE,
            T(MADRE + "Steeeeven..."),
            cerca,
            CHOICE(["Contener la respiración", mirar], [[
                T("Te muerdes la lengua para no hacer ruido.\nNotas el sabor de la sangre. Cuentas.\nUno. Dos. Tres..."),
                WAIT(60),
                T("Una uña rasca la madera, de arriba abajo,\nmuy despacio. Luego se detiene."),
                T(MADRE + "Ya saldrás. Siempre sales. Y yo siempre\nestoy aquí."),
                vuelta, WAITMOVE, EVLOC(CAZA, 22, 7, 2),
                SE("026-Door03", 60, 70),
                T("Los pasos se alejan hacia la cocina. Una silla\ncruje bajo su peso. Luego, nada."),
                VEN(8),
                TRANSFER(M_PISO, salida[0], salida[1], 2, False),
                amanecer(),
            ], [
                ojo, pillado(),
            ]], 0),
        ], []], 2)]

    def bajo_la_cama():
        return [CHOICE(["Meterte debajo de la cama", "Mejor no"], [[
            SW(S_ESCONDIDO), TIMERSTOP,
            TONE(-255, -255, -255, 0, 15), WAIT(15),
            TRANSFER(M_PISO, 1, 4, 8, False), TRANSP(True), WAIT(10), tono_busqueda(15),
            T("Te arrastras debajo de la cama. Polvo, pelos de\nperro, un calcetín que creías perdido."),
            EVLOC(CAZA, 5, 10, 8),
            MOVE(CAZA, steps(UP, 4) + steps(LEFT, 3) + steps(UP, 2) + [turn(4)]), WAITMOVE,
            T(MADRE + "Debajo de la cama. Siempre debajo de la\ncama. Como cuando tenías seis años."),
            T("Una mano entra bajo el somier y te encuentra\nel tobillo a la primera."),
            pillado(),
        ], []], 2)]

    def empezar_busqueda():
        return [CHOICE(["Dormir", "Todavía no"], [[
            TONE(-255, -255, -255, 0, 60), STOPBGS(2), WAIT(70),
            T("Duermes. O algo que se le parece."),
            T("Sueñas con un pasillo de azulejos blancos que\nno termina nunca. Al fondo, algo muy grande\nrespira."),
            T("Debajo del suelo, algo muge. Un mugido largo,\nhúmedo. Casi suena a tu nombre."),
            VEN(8),
            SE("026-Door03", 100, 60), SHAKE(7, 8, 20),
            T("Un portazo te despierta. La nevera."),
            T(VOZ + "¡Me falta dinero del monedero! ¡STEVEN!"),
            T(VOZ + "Sé que has sido tú. Siempre eres tú."),
            tono_busqueda(30), WAIT(20),
            T(PIENSA + "(Viene hacia aquí. Tengo que esconderme. Ya.)" + FIN),
            T(AYUDA + "(Tienes poco tiempo. Busca un buen escondite:\nno todos lo son.)" + FIN),
            SW(S_BUSQ), VAR(V_ETAPA, 5),
            EVLOC(CAZA, 22, 12, 4),
            BGM("036-Dungeon02", 75, 80),
            TIMER(30),
        ], []], 2)]

    # ---------------- 1: la madre cazadora
    m.set("Madre cazadora", 22, 7, [
        page([]),
        page([pillado()], sw1=S_BUSQ, char="vacas_madre", d=4, trigger=2,
             move_type=2, speed=3, freq=5),
        page([], sw1=S_ESCONDIDO, char="vacas_madre", d=8, move_type=0, speed=3),
        page([], sw1=S_BUSQ_FIN),
    ])

    # ---------------- 2: ambiente
    m.add("Ambiente", 0, 0, [page([
        IF(c_sw(S_BUSQ), [tono_busqueda(), BGS("018-Darkness01", 55, 70)], [
            IF(c_sw(S_NOCHE), [tono_noche(), BGS("018-Darkness01", 45, 80)], [
                IF(c_sw(S_MANANA), [tono_manana(), BGS("001-Wind01", 35, 60)],
                   [tono_dia(), BGS("001-Wind01", 30, 55)])])]),
        FOG("002-Clouds01", 28, 0, 200, 1, 0),
        ERASE,
    ], trigger=4)])

    # ---------------- 3: despertar
    m.add("Despertar", 0, 1, [page([
        SW(S_HUD_OFF, False), SW(S_SIN_EFECTOS, False), TRANSP(False), MENUACCESS(True),
        WAIT(40),
        T(PIENSA + "(El techo otra vez. La mancha de humedad tiene\nforma de un país que no existe. Ha crecido.)" + FIN),
        SE("040-Knock01", 90, 60), SHAKE(6, 8, 15),
        T(VOZ + "¡STEVEN!"),
        T(VOZ + "¡Ven aquí antes de que tenga que levantarme\nyo!"),
        VEN(5),
        T(PIENSA + "(Su voz atraviesa las paredes como el olor.\nNo hay puerta en esta casa que la pare.)" + FIN),
        T(AYUDA + "(Abajo a la izquierda ves tu veneno: lo que\nla casa te va metiendo dentro. La tele lo baja.\nEsc abre el menú: objetos y tareas.)" + FIN),
        SS("A"),
    ], sw1=S_INTRO, trigger=3), page([], ss="A")])

    # ---------------- cama de Steven (dos casillas)
    cama = [
        page([T("Las sábanas tienen la forma exacta de tu cuerpo.\nComo un molde. Como una bandeja.")]),
        page([empezar_busqueda()], sw1=S_NOCHE),
        page([bajo_la_cama()], sw1=S_BUSQ),
        page([T("No vuelves a acostarte. Hoy no.")], sw1=S_MANANA),
    ]
    m.add("Cama Steven", 1, 3, cama)
    m.add("Cama Steven 2", 1, 4, cama)

    # ---------------- armario
    m.add("Armario", 7, 3, [
        mueble([T("Tres camisas y un abrigo que huele a naftalina.\nTodo era de tu padre. Nada te queda bien.\nNada te ha quedado bien nunca.")], 7, 3, "", 6, 0),
        mueble([esconderse("armario")], 7, 3, "", 6, 0, sw1=S_BUSQ),
        mueble([T("El armario se ha quedado entreabierto. Dentro\nhuele todavía a tu miedo.")], 7, 3, "", 6, 1, sw1=S_BUSQ_FIN),
    ])

    # ---------------- cajonera, libro, ventana
    m.add("Cajonera", 5, 3, [
        page([T("En el cajón de abajo, debajo de calcetines con\nagujeros, hay una foto boca abajo."),
              ITEM(I_FOTO), SE("046-Book01"),
              T(AYUDA + "(Has cogido la Foto rascada. Úsala desde el\nmenú para mirarla.)" + FIN), SS("A")]),
        page([T("Calcetines. Una caja de cerillas vacía. Un diente\nde leche en una bolsita: no sabes de quién.")], ss="A"),
    ])
    m.add("Libro", 6, 3, [page([T("Un libro infantil: «La granja contenta».\nAlguien tachó con boli todas las sonrisas de\nlos animales."),
                                T(PIENSA + "(Fui yo. Tenía ocho años. No recuerdo por qué,\nsolo que tenía que hacerse.)" + FIN)])])
    m.add("Ventana Steven", 3, 2, [page([T("Da a un patio de luces. Abajo, alguien tendió\nropa hace semanas y nunca la recogió. Se ha\nvuelto del color del agua sucia.")])])

    # ---------------- bano
    m.add("Vater", 11, 3, [mueble([T("No tires de la cadena por la noche. Ella lo oye\ntodo. Y luego te lo cobra.")], 0, 0, "", 8, 0)])
    m.add("Lavabo", 13, 3, [
        mueble([
            IF(c_sw(S_ORDENES), [
                T("Detrás del espejo, entre cuchillas oxidadas y\nalgodones amarillos, está el jarabe de madre."),
                ITEM(I_JARABE), SE("046-Book01"), SS("A"),
            ], [T("El espejo está partido en diagonal. Te corta la\ncara en dos mitades que no se parecen.")]),
        ], 0, 0, "", 8, 1),
        mueble([
            IF(c_var(V_VENENO, 40, 1), [
                T("Te miras. Tu reflejo parpadea un segundo\ndespués que tú."), VEN(3),
            ], [T("El espejo está partido en diagonal. Te corta la\ncara en dos mitades que no se parecen.")]),
        ], 0, 0, "", 8, 1, ss="A"),
    ])
    m.add("Banera", 10, 5, [
        mueble([T("La bañera tiene un cerco marrón a la altura\nexacta de su cuerpo. Nunca la vacía del todo.")], 0, 0, "", 6, 3),
        mueble([esconderse("banera")], 0, 0, "", 6, 3, sw1=S_BUSQ),
    ])

    # ---------------- la madre (en su sillon)
    m.add("Sillon madre", 24, 4, [mueble([], 0, 0, "", 8, 2)])
    insultos = [
        IF(c_var(V_INSULTO, 1), [T(MADRE + "¿Qué haces ahí plantado? Pareces una vaca\nmirando pasar un tren.")]),
        IF(c_var(V_INSULTO, 2), [T(MADRE + "Si tu padre te viera... No. Mejor que no te\nvea nadie.")]),
        IF(c_var(V_INSULTO, 3), [T(MADRE + "Está todo en la lista. ¿O ya no sabes leer?")]),
        IF(c_var(V_INSULTO, 4), [T(MADRE + "Te huelo desde aquí. Hueles a miedo. Es un\nolor muy barato, Steven.")]),
    ]
    ordenes = [
        T(MADRE + "Por fin. Cada mañana tardas más en levantarte.\nCada mañana pesas más de nada."),
        T(PIENSA + "(Ocupa el sillón entero. El sillón ya no tiene\nforma de sillón: tiene forma de ella.)" + FIN),
        T(MADRE + "Escucha, que no lo voy a repetir."),
        T(MADRE + "Uno. Mi jarabe. Está en el baño, detrás del\nespejo. Me duele el pecho de tanto aguantarte."),
        T(MADRE + "Dos. Ese perro apesta a hambre. Dale algo\nantes de que se muera y tenga que bajarlo yo."),
        T(MADRE + "Tres. Baja a la carnicería de Molina. Medio\nkilo de picada. De la roja, no de la gris."),
        GOLD(3), SE("006-System06", 70, 80),
        T("Te tira tres monedas. Caen al suelo. Las recoges\nde rodillas, como siempre."),
        ITEM(I_LISTA), ITEM(I_LLAVE),
        T(MADRE + "Y la llave. Me la devuelves. Si la pierdes, te\ncambio a ti por una cerradura."),
        T(MADRE + "Y mira el tablón del portal. Un hombre que no\ntrae dinero a casa no es un hombre. Es un\nmueble."),
        T(MADRE + "Y muebles ya tengo bastantes."),
        SW(S_ORDENES), SW(S_PUERTA), VAR(V_ETAPA, 2), VEN(5),
        T(AYUDA + "(Tienes la Lista de madre y la Llave del piso.\nEn el menú verás lo que queda pendiente.)" + FIN),
    ]
    cena = [
        T(MADRE + "Lo has hecho todo. Mírate. Casi pareces útil."),
        T(MADRE + "Siéntate. Hoy cenamos juntos."),
        NEGRO, WAIT(40), STOPBGS(2),
        T("En la cocina, la bombilla zumba como una mosca\natrapada dentro del cristal."),
        T("Madre no cocina la carne. La amasa con las\nmanos, le echa sal y se la come así, cruda, a\npuñados, sin dejar de mirarte."),
        T(MADRE + "Come."),
        T("Te pone un puñado en el plato. Está fría.\nTiene la temperatura exacta de la nevera."),
        CHOICE(["Comer", "Negarte"], [[
            T("Masticas. No sabe a nada y a la vez sabe a todo:\na hierro, a cobre, a moneda chupada."),
            T(MADRE + "¿Ves? No era tan difícil. Tragar. Es lo único\nque se te ha dado bien siempre."),
            VEN(12),
        ], [
            SE("092-Attack04", 80, 80), SHAKE(8, 9, 15), FLASH(255, 255, 255, 120, 6),
            T("La mano llega antes que la palabra. Te arde la\nmejilla. La carne cae al suelo."),
            T(MADRE + "Recógela. Ahora te la comes del suelo, como\nel perro. Ya que no quieres ser persona."),
            VEN(18),
        ]], 0),
        T(MADRE + "¿Y el tablón? ¿Has mirado el tablón?"),
        T("Le enseñas el anuncio del matadero.\nLo lee moviendo los labios."),
        T("Se ríe. Se ríe tanto que tose, y tose tanto que\nescupe algo rosa en la servilleta."),
        T(MADRE + "¿Tú? ¿En el matadero? Si no fuiste capaz ni de\nahogar los gatitos de la vecina."),
        T(MADRE + "... Bueno. Por lo menos olerás a algo.\nMañana a las seis estás en ese camión.\nY ahora, a la cama."),
        SW(S_CENA), SW(S_NOCHE), VAR(V_ETAPA, 4),
        TRANSFER(M_PISO, 2, 5, 2), WAIT(10), tono_noche(40),
        BGS("018-Darkness01", 45, 80), WAIT(30),
        T(PIENSA + "(La casa se queda callada. Solo se oye la\nnevera. Y debajo de la nevera, otra cosa.)" + FIN),
        T(AYUDA + "(Cuando quieras, acuéstate en tu cama. Antes\npuedes guardar en la tele del salón.)" + FIN),
    ]
    entrega = [
        IF(c_item(I_JARABE), [
            ITEM(I_JARABE, -1), SW(S_JARABE),
            T(MADRE + "Trae."),
            T("Bebe directamente del frasco. Un hilo marrón le\nbaja por la barbilla y se pierde en los\npliegues del cuello."),
            T(MADRE + "Está caliente. Lo has tenido en la mano, ¿eh?\nLo has calentado con tus manos sucias."),
            VEN(4), EXIT,
        ]),
        IF(c_item(I_CARNE), [
            ITEM(I_CARNE, -1), SW(S_CARNE_D),
            T("Le das el paquete. Lo abre allí mismo, sobre las\nrodillas, y huele la carne como quien huele\nflores."),
            T(MADRE + "Roja. Bien. Por una vez."),
            T(MADRE + "¿Y el cambio?"),
            IF(c_gold(1), [GOLD(-1), T("Le das la moneda que sobró. La muerde para\ncomprobar que es de verdad.")]),
            VEN(3), EXIT,
        ]),
        VARRAND(V_INSULTO, 1, 4), insultos, VEN(2),
    ]
    madre_dia = [
        IF(c_sw(S_ORDENES), [
            IF(c_sw(S_PERRO), [IF(c_sw(S_JARABE), [IF(c_sw(S_CARNE_D), [IF(c_sw(S_ANUNCIO), [
                cena, EXIT])])])]),
            entrega,
        ], ordenes),
    ]
    m.add("Madre", 24, 5, [
        page(madre_dia, char="vacas_madre", d=2, speed=2),
        page([T("Se ha dormido sentada, con la boca abierta.\nRonca como un motor que no termina de\narrancar. No la despiertes.")],
             sw1=S_NOCHE, char="vacas_madre", d=2, dirfix=True),
        page([], sw1=S_BUSQ),
        page([], sw1=S_MANANA),
    ])
    abrelatas = [
        T("Abres el primer cajón. Ella deja de respirar un\nmomento. Notas sus ojos en la nuca."),
        T(MADRE + "¿Qué buscas en mis cajones?"),
        T(PIENSA + "(El abrelatas. Para Perro.)" + FIN),
        T(MADRE + "El abrelatas. Claro. Lo que se abre en esta casa\nlo abro yo. Pídemelo bien."),
        CHOICE(["Pedírselo de rodillas", "Cogerlo sin más"], [[
            T("Te arrodillas en la alfombra. Huele a pies y a\njerez. Dices «por favor». Lo dices dos veces,\nporque la primera hace como que no lo oye."),
            T(MADRE + "Así me gusta. Cógelo. Y me lo devuelves limpio."),
            VEN(6),
        ], [
            SE("042-Knock03", 90, 80), SHAKE(6, 9, 12),
            T("Le das la espalda y lo coges. Algo te golpea en\nla nuca: un zapato, o el mando de la tele.\nNo te vuelves a mirar."),
            T(MADRE + "Ladrón. Igual que tu padre. Igualito."),
            VEN(10),
        ]], 0),
        ITEM(I_ABRE), SW(S_ABRELATAS), SE("046-Book01"),
    ]
    m.add("Comoda madre", 21, 3, [
        page([T("No abras sus cajones. Nunca. Es la primera regla\nque aprendiste en esta casa.")]),
        page([IF(c_sw(S_ABRELATAS),
                 [T("Medias enrolladas como tripas secas. Recibos.\nUn rosario sin cruz.")],
                 abrelatas)], sw1=S_ORDENES),
    ])
    m.add("Tarro", 22, 3, [page([T("Encima de la cómoda, un tarro con dientes de\nleche. Muchos. Más de los que tiene un niño.")])])
    m.add("Reloj de cuco", 23, 2, [page([T("El reloj de cuco lleva parado desde antes de\nque tú nacieras. El cuco se quedó fuera,\na medio salir, con el pico abierto.")])])
    m.add("Cama madre", 17, 4, [page([T("La cama huele a ella: a grasa, a polvos de\ntalco, a carne que se ha quedado fuera de\nla nevera.")])])
    m.add("Botellas", 26, 6, [page([T("Botellas de jerez barato. Las vacías también las\nguarda. Dice que algún día valdrán algo.")],
                                    char=COSAS, d=4, pat=1, dirfix=True, walk=False)])
    m.add("Cenicero", 22, 6, [page([T("Colillas con carmín, aplastadas hasta el filtro.\nUna todavía humea.")],
                                    char=COSAS, d=4, pat=2, dirfix=True, walk=False)])
    m.add("Cajas", 27, 4, [page([T("Cajas de cartón con tu nombre escrito. Dentro,\nropa de bebé. Muchísima ropa de bebé, toda sin\nestrenar.")])])

    # ---------------- pasillo
    m.add("Perchero", 2, 11, [page([T("Un abrigo de hombre. En el bolsillo, un billete\nde autobús de hace veinte años, con destino al\nmatadero municipal.")])])
    m.add("Reloj pasillo", 17, 11, [page([T("Este reloj sí funciona. Va siete minutos tarde,\ncomo todo en esta casa.")])])
    m.add("Cuadro pasillo", 9, 11, [page([T("Un cuadro de flores. Alrededor, la pared está\nmás oscura: aquí hubo colgado otro cuadro más\ngrande durante muchos años.")])])
    m.add("Tetera", 27, 12, [page([T("Una tetera fría sobre un taburete. Nadie sabe\nqué hace aquí. Nadie se atreve a moverla.")])])
    for (x, y) in [(8, 13), (21, 19), (13, 7)]:
        m.add("Mancha", x, y, [page([], char=COSAS, d=2, pat=3, dirfix=True, walk=False, through=True)])

    # ---------------- puerta del piso
    salir = [SE("024-Door01", 80, 90), TRANSFER(M_ESC, 9, 3, 2)]
    atras = MOVE(-1, [UP])
    puerta = [
        page([T("La puerta está cerrada con llave. La llave la\ntiene ella."), atras], trigger=1),
        page(salir, sw1=S_PUERTA, trigger=1),
        page([T("De noche no se sale. Es la única norma de esta\ncasa que nunca hizo falta escribir."), atras], sw1=S_NOCHE, trigger=1),
        page(salir, sw1=S_MANANA, trigger=1),
    ]
    m.add("Puerta del piso", 14, 21, puerta)
    m.add("Puerta del piso 2", 15, 21, puerta)

    # ---------------- salon: la tele
    def programa(n, txt, graf=(2, 0, True)):
        d, p, anim = graf
        return IF(c_var(V_CANAL, n), [
            MOVE(0, [mgraphic(MUEBLES, d, p), STEP_ANIME_ON if anim else STEP_ANIME_OFF]), WAIT(4),
            T(txt)])
    ver = [
        SE("032-Switch01", 80, 70), WAIT(10),
        VAR(V_CANAL, 1, 1), IF(c_var(V_CANAL, 5, 3), [VAR(V_CANAL, 1)]),
        VAR(V_VECES, 1, 1),
        IF(c_script("$game_switches[9] or $game_switches[27]"), [
            MOVE(0, [mgraphic(MUEBLES, 2, 0), STEP_ANIME_ON]), WAIT(40),
            T("Ya no emiten nada. Solo nieve."),
            MOVE(0, [mgraphic(MUEBLES, 4, 2), STEP_ANIME_OFF]), WAIT(4),
            T("Dentro de la nieve, una forma oscura se acerca\na la pantalla. Tiene cuernos. Te mira como si\nla tele fuera una ventana y tú, el programa."),
            VEN(-8),
        ], [
            programa(1, "Un concurso. Un presentador con brillantina\npregunta a una señora cuánto pesa su marido.\nElla acierta. El público aplaude demasiado."),
            programa(2, "Un western en blanco y negro. Un vaquero guía\nreses por un desfiladero. Ninguna vaca mira a\nla cámara. Casi ninguna."),
            programa(3, "Un programa de cocina. Una mujer con delantal\nenseña a hacer lengua estofada. Sonríe mucho.\nLa lengua, en el plato, parece querer hablar."),
            programa(4, "La carta de ajuste y un pitido largo, limpio.\nEs lo más parecido al silencio que conoces.", (4, 1, False)),
            programa(5, "Un muñeco de trapo con forma de vaca canta una\ncanción sobre ir al mercado. Los niños del plató\nno cantan. Solo miran."),
            VEN(-15),
        ]),
        T(PIENSA + "(Mientras mira, nadie le habla. El mundo se\nqueda al otro lado del cristal.)" + FIN),
        IF(c_var(V_VECES, 3), [
            SE("040-Knock01", 90, 60), SHAKE(4, 8, 10),
            T(VOZ + "¡Apaga eso, que la luz cuesta dinero! ¡La\npagas tú, mueble!"),
            VEN(4),
        ]),
        MOVE(0, [mgraphic(MUEBLES, 4, 0), STEP_ANIME_OFF]),
        SE("032-Switch01", 60, 50),
    ]
    guardar = [
        MOVE(0, [mgraphic(MUEBLES, 2, 0), STEP_ANIME_ON]), WAIT(10),
        T("Dejas la tele encendida, sin volumen. Su luz\nazul te vigila mientras guardas."),
        SAVE,
        MOVE(0, [mgraphic(MUEBLES, 4, 0), STEP_ANIME_OFF]),
    ]
    tele = [IF(c_sw(S_BUSQ), [T("No hay tiempo para la tele. Ya viene.")], [
        T("La tele. Madera oscura, patas de alambre, una\npantalla curva como un ojo de pez."),
        CHOICE(["Ver la tele", "Guardar partida", "Dejarla"], [ver, guardar, []], 3),
    ])]
    m.add("Tele", 8, 17, [mueble(tele, 0, 0, "", 4, 0)])
    m.add("Sofa", 6, 19, [page([T("El sofá. Un muelle se te clava siempre en el\nmismo sitio, como si te conociera.")])])
    m.add("Piano", 10, 17, [
        mueble([T("El piano está tapado con una sábana. Nadie lo\ntoca desde que él se fue.")], 0, 0, "", 8, 3),
        mueble([T("Bajo la sábana suena una tecla. Sola. Una nota\ngrave, larga. Luego nada."), VEN(4), SS("A")],
               0, 0, "", 8, 3, sw1=S_NOCHE),
        mueble([T("La sábana está quieta. Muy quieta.")], 0, 0, "", 8, 3, sw1=S_NOCHE, ss="A"),
    ])
    perro_hablar = [
        IF(c_sw(S_PERRO), [
            IF(c_sw(S_MANANA), [
                T("Perro arrastra su cuerpo hasta tus pies y apoya\nla cabeza en tu zapato. Te promete algo con\nlos ojos. No sabes qué."),
                IF(c_ss("B", False), [VEN(-6), SS("B")]),
            ], [
                T("Le rascas detrás de las orejas. Perro cierra\nlos ojos. Por un momento, en esta casa, alguien\nestá bien."),
                IF(c_ss("A", False), [VEN(-4), SS("A")]),
            ]),
        ], [
            IF(c_item(I_LATA), [
                IF(c_item(I_ABRE), [
                    SE("044-Chest01", 70, 120),
                    T("Abres la lata. El olor llena el salón: gelatina,\nharina, algo que fue un animal."),
                    T("Perro come tumbado de lado, porque es la única\nforma que tiene. Las patas de atrás no se\nenteran de nada."),
                    ITEM(I_LATA, -1), SW(S_PERRO), VEN(-10),
                    T(PIENSA + "(Cuando termina, te lame los dedos uno por uno.\nComo si te diera las gracias por cada uno.)" + FIN),
                ], [
                    T("Tienes la lata, pero nada con qué abrirla. Perro\nla huele y gime."),
                    T(PIENSA + "(El abrelatas. En el cajón de la cocina no está.\nLo tendrá ella.)" + FIN),
                ]),
            ], [
                T("Perro te mira desde el suelo. Las patas de atrás\nle cuelgan como dos calcetines vacíos."),
                T("Tiene hambre. Siempre tiene hambre. Arrastra el\ncuerpo un palmo hacia ti, y otro."),
            ]),
        ]),
    ]
    m.add("Perro", 3, 19, [
        page(perro_hablar, char="vacas_perro", d=4, move_type=3, speed=1, freq=1,
             mroute=route([mwait(160), LEFT, mwait(200), RIGHT, mwait(80), turn(2)], True, True)),
        page([T("Perro gime muy bajito, con el hocico contra el\nsuelo. Sabe lo que viene. Siempre lo sabe.")],
             sw1=S_BUSQ, char="vacas_perro", d=2),
        page(perro_hablar, sw1=S_MANANA, char="vacas_perro", d=4),
    ])
    m.add("Cesta Perro", 2, 20, [page([T("La cesta de Perro. Huele a orina vieja y a\nperro mojado. Huele a la única cosa de esta casa\nque te quiere.")],
                                       char=COSAS, d=4, pat=3, dirfix=True, walk=False)])
    m.add("Cuenco", 4, 20, [
        page([T("El cuenco de Perro. Vacío. Lleva días vacío.")], char=COSAS, d=2, pat=0, dirfix=True, walk=False),
        page([T("Perro ha dejado el cuenco limpio, brillante.")], sw1=S_PERRO, char=COSAS, d=2, pat=1, dirfix=True, walk=False),
    ])
    m.add("Ventana salon", 3, 16, [page([T("Desde aquí se ve la calle. Allí abajo la gente\nanda deprisa, como si tuviera a dónde ir.")])])
    m.add("Estante salon", 11, 16, [page([T("Figuritas de porcelana: pastoras, perritos, una\nvaca con un lazo. A la vaca le falta la cabeza.")])])

    # ---------------- cocina
    m.add("Alacena", 17, 18, [
        page([T("Platos desparejados, tazas sin asa, un tarro de\nmonedas extranjeras que nadie va a gastar.")]),
        page([IF(c_sw(S_LATA), [T("Platos desparejados. Sal. Azúcar con hormigas.")], [
            T("Detrás de los botes de sal y de una bolsa de\nazúcar con hormigas, encuentras una lata\npara perro."),
            ITEM(I_LATA), SW(S_LATA), SE("046-Book01"),
            T(PIENSA + "(Para abrirla hace falta el abrelatas.)" + FIN),
        ])], sw1=S_ORDENES),
    ])
    m.add("Cajon cubiertos", 18, 18, [
        page([T("El cajón de los cubiertos. Cuchillos sin punta,\ntenedores torcidos.")]),
        page([IF(c_sw(S_ABRELATAS), [T("Cuchillos sin punta. Tenedores torcidos.")], [
            T("En el cajón de los cubiertos, en lugar del\nabrelatas, hay una nota con su letra:"),
            T("\\c[6]«EL ABRELATAS LO TENGO YO.»\\c[0]"),
        ])], sw1=S_ORDENES),
    ])
    m.add("Fogon", 20, 17, [page([T("El fogón de carbón. Ella cocina aquí la carne\nhasta que deja de parecer carne. Casi nunca.")])])
    m.add("Nevera", 28, 17, [
        mueble([T("Dentro: un cuarto de cerdo envuelto en film,\nnumerado con rotulador. Tres huevos. Un frasco\ncon algo que flota y que no es un pepinillo.")], 0, 0, "", 6, 2),
        mueble([T("La puerta de la nevera está abierta. La luz de\ndentro tiembla. Algo gotea en el suelo.")], 0, 0, "", 6, 2, sw1=S_BUSQ),
    ])
    m.add("Mesa cocina", 25, 20, [page([T("Hule pegajoso. Migas. Una mosca que no se va\naunque la espantes.")])])
    m.add("Carne en la mesa", 24, 19, [
        page([]),
        page([], sw1=S_CARNE_D, char=COSAS, d=2, pat=2, dirfix=True, walk=False),
    ])
    m.add("Barreno", 27, 20, [page([T("Agua gris con platos dentro. Algo se mueve en\nel fondo. Es solo un tenedor. Seguramente.")])])
    m.add("Madre por la manana", 23, 19, [
        page([]),
        page([IF(c_sw(S_PILLADO),
                 [T("No te mira. Moja pan en el café y lo chupa."),
                  T(MADRE + "Trae el sueldo entero. Entero, Steven.")],
                 [T(MADRE + "¿Todavía aquí? Vete. Y trae el sueldo entero.\nEntero, Steven."),
                  T(MADRE + "Y anoche... anoche no me hagas pensar en\nanoche.")])],
             sw1=S_MANANA, char="vacas_madre", d=6),
    ])

    # ---------------- control de la busqueda (paralelo)
    m.add("Control busqueda", 0, 2, [
        page([]),
        page([
            IF(c_sw(S_ESCONDIDO, False), [
                IF(c_timer_le(0), [TIMERSTOP, SW(S_TIEMPO)]),
            ]),
            SE("040-Knock01", 35, 40), WAIT(45),
        ], sw1=S_BUSQ, trigger=4),
    ])

    m.add("Fin del tiempo", 0, 3, [
        page([]),
        page([SW(S_TIEMPO, False),
              SE("026-Door03", 100, 50),
              T("Una puerta se abre de golpe en algún sitio de la casa. Ya no hay donde esconderse."),
              pillado()], sw1=S_TIEMPO, trigger=3),
    ])

    # ---------------- bloqueadores invisibles (graficos vacios)
    m.add("Bloqueo banera", 10, 4, [page([], char="vacas_vacio", dirfix=True, walk=False)])
    return m

# ======================================================================
# MAPA 3: LA ESCALERA
# ======================================================================
def escalera():
    m = MapEvents(M_ESC)
    m.add("Ambiente", 0, 0, [page([
        TONE(-25, -30, -45, 100, 0), BGS("016-Drips01", 55, 80),
        FOG("002-Clouds01", 40, 0, 200, 0, 1), ERASE], trigger=4)])
    m.add("Puerta 3B", 9, 2, [page([
        T("3ºB. Tu puerta. La mirilla está tapada con\ncinta aislante desde dentro."),
        CHOICE(["Entrar", "Quedarte fuera"], [[SE("024-Door01", 80, 90), TRANSFER(M_PISO, 14, 20, 8)], []], 2),
    ], char="vacas_puerta", d=2, pat=0, dirfix=True, walk=False)])
    m.add("Puerta 3A", 4, 2, [page([T("3ºA. Un felpudo que dice BIENVENIDOS. Nadie ha\nsido bienvenido aquí nunca.")],
                                   char="vacas_puerta", d=2, pat=0, dirfix=True, walk=False)])
    m.add("Puerta 3C", 15, 2, [page([
        T("3ºC. Aquí vive el señor Ortega. Hace un mes que\nnadie le ve, pero la radio sigue encendida."),
        T("Detrás de la puerta, la radio reza una misa.\nSiempre la misma. Día y noche."),
    ], char="vacas_puerta", d=2, pat=0, dirfix=True, walk=False)])
    REM = "\\c[4]Doña Remedios:\\c[0] "
    m.add("Dona Remedios", 4, 4, [
        page([
            IF(c_ss("A", False), [
                T(REM + "Ay, Steven, hijo. Anoche otra vez los gritos.\nYo no digo nada, ¿eh? Yo no me meto."),
                T(REM + "Pero si un día necesitas... bueno. Nada.\nQue tu madre me debe un táper desde Semana\nSanta, díselo."),
                SS("A"),
            ], [
                T(REM + "Tienes cara de no comer. Bueno, comer comes.\nTienes cara de que no te sienta bien."),
            ]),
        ], char="vacas_remedios", d=2),
        page([
            T(REM + "¿Al matadero? Dicen que allí la gente se vuelve\nrara. Como el del cuarto. Como esa chica."),
            T(REM + "La rubia de arriba, la que pide tripas en las\ncarnicerías. Para estudiarlas, dice. Estudiar\ntripas. Dios mío."),
        ], sw1=S_MANANA, char="vacas_remedios", d=2),
    ])
    ANS = "\\c[4]Señor Anselmo:\\c[0] "
    m.add("Senor Anselmo", 13, 6, [
        page([
            IF(c_ss("A", False), [
                T(ANS + "Mi hermano trabajó treinta años en el matadero\nmunicipal. Treinta años."),
                T(ANS + "Al final mugía en sueños. Mi cuñada no podía\ndormir. Decía que él tenía la boca llena de\nhierba."),
                SS("A"),
            ], [
                T(ANS + "Las vacas lo saben, ¿sabes? Saben cuándo les\ntoca. Se quedan mirando al suelo."),
                IF(c_ss("B", False), [VEN(2), SS("B")]),
            ]),
        ], char="vacas_anselmo", d=2),
        page([
            T(ANS + "Así que vas. Bueno. Lávate las manos con limón\nal llegar a casa. La sangre se va con limón."),
            T(ANS + "El olor no. El olor no se va con nada."),
        ], sw1=S_MANANA, char="vacas_anselmo", d=2),
    ])
    m.add("Escalera arriba", 17, 3, [page([
        T("La escalera sube al cuarto piso. Allí vive una\nchica, Lucy. Dicen que va a las carnicerías a\npedir vísceras. Dicen muchas cosas."),
        T(PIENSA + "(Hoy no subes.)" + FIN),
        MOVE(-1, [DOWN]),
    ], trigger=1)])
    m.add("Bajada a la calle", 2, 12, [page([SE("013-Move01", 60, 80), TRANSFER(M_CALLE, 7, 6, 2)], trigger=1)])
    m.add("Cajas mudanza", 7, 8, [page([T("Cajas de una mudanza que nunca terminó. Una dice\nFRÁGIL. Otra dice MAMÁ, con letra de niño.")])])
    m.add("Ventana escalera", 12, 2, [page([T("Una ventana tan sucia que la luz entra ya\ncansada.")])])
    m.add("Bombilla", 9, 6, [page([], char="185-Light02", blend=1, opacity=160, through=True, top=True,
                                  dirfix=True, step=True)])
    for (x, y) in [(6, 9), (15, 5), (11, 11)]:
        m.add("Mancha", x, y, [page([], char=COSAS, d=2, pat=3, dirfix=True, walk=False, through=True)])
    return m

# ======================================================================
# MAPA 4: LA CALLE
# ======================================================================
def calle():
    m = MapEvents(M_CALLE)
    m.add("Ambiente", 0, 0, [page([
        IF(c_sw(S_MANANA),
           [TONE(-20, -28, -35, 100, 0), WEATHER(1, 3, 0)],
           [TONE(-40, -38, -22, 120, 0), WEATHER(1, 6, 0)]),
        BGS("005-Rain01", 65, 90), FOG("002-Clouds01", 35, 0, 200, 2, 1), ERASE], trigger=4)])
    m.add("Portal", 7, 5, [page([
        CHOICE(["Volver a subir", "Seguir en la calle"], [[SE("024-Door01", 80, 90), TRANSFER(M_ESC, 2, 9, 8)], []], 2),
    ], char="vacas_puerta", d=2, pat=0, dirfix=True, walk=False)])
    anuncio_txt = [
        T("\\c[6]MATADERO MUNICIPAL. SE NECESITAN BRAZOS.\nTurnos de mañana y de noche. No se pide\nexperiencia. Se pide estómago.\\c[0]"),
        T("\\c[6]Presentarse junto al camión del matadero, en\nesta misma calle, a las seis de la mañana.\\c[0]"),
    ]
    m.add("Tablon", 9, 6, [page([
        T("Entre anuncios de pisos que nadie quiere y de\ngatos que nadie busca, hay uno escrito a\nmáquina:"),
        anuncio_txt,
        T(PIENSA + "(Brazos. No piden personas. Piden brazos.)" + FIN),
        IF(c_sw(S_ANUNCIO, False), [
            ITEM(I_ANUNCIO), SW(S_ANUNCIO), SE("046-Book01"),
            T("Arrancas el anuncio y te lo guardas en el\nbolsillo. Está húmedo, blando, como piel."),
        ]),
    ], char="vacas_tablon", d=2, pat=1, dirfix=True, walk=False)])
    MOL = "\\c[4]Molina:\\c[0] "
    m.add("Mostrador", 18, 7, [page([
        IF(c_sw(S_MANANA), [
            T(MOL + "¿Al matadero, eh? Pues ya nos veremos. Lo que\ntú cortes allí, lo vendo yo aquí."),
            T(MOL + "Así funciona el mundo, chaval. Unos cortan,\notros venden y otros comen."),
        ], [
            IF(c_sw(S_ORDENES), [
                IF(c_sw(S_CARNE_C), [
                    T(MOL + "Corre, que a tu madre no le gusta esperar.\nY a la carne tampoco."),
                ], [
                    T(MOL + "Hombre, Steven. Lo de siempre para tu madre,\n¿no? Medio de picada. De la roja."),
                    T("Molina hunde la mano en la bandeja y saca un\npuñado rojo, brillante. Lo pesa sin mirar\nla balanza."),
                    IF(c_gold(2), [
                        GOLD(-2), ITEM(I_CARNE), SW(S_CARNE_C), SE("006-System06", 70, 80),
                        T(MOL + "Dos monedas. Y dile que el hígado del jueves\nno tenía nada. Que lo de los gusanos fue\ncosa suya."),
                        T(MOL + "Oye. En el matadero están cogiendo gente.\nMira el tablón de tu portal. Tú tienes\nbrazos, ¿no? Pues eso."),
                    ], [T(MOL + "No te llega, chaval. Vuelve con dinero.")]),
                ]),
            ], [
                T(MOL + "Hombre, Steven. ¿Hoy no te manda la jefa?"),
            ]),
        ]),
    ], char=COSAS, d=2, pat=2, dirfix=True, walk=False)])
    m.add("Molina", 18, 6, [page([], char="vacas_carnicero", d=2)])
    m.add("Escaparate", 15, 5, [page([T("En el escaparate, cabezas de cerdo sobre hojas\nde lechuga de plástico. Todas sonríen igual.\nComo si supieran el mismo chiste.")])])
    BOR = "\\c[4]Borracho:\\c[0] "
    m.add("Borracho", 31, 16, [
        page([
            IF(c_ss("A", False), [
                T(BOR + "Eh. Eh, tú. El del piso de la Bestia."),
                T(BOR + "Las oigo por las alcantarillas, ¿sabes? Por las\nnoches. Mugen ahí abajo."),
                T(BOR + "No me mires así. Tú también las vas a oír.\nTodos los del matadero las oyen."),
                VEN(3), SS("A"),
            ], [T(BOR + "Mmmuuu. Mmmuuuuu. Je.")]),
        ], char="vacas_borracho", d=2, pat=1, walk=False, dirfix=True),
        page([T("Duerme encima de un charco. Respira, eso sí.")],
             sw1=S_MANANA, char="vacas_borracho", d=2, pat=1, walk=False, dirfix=True),
    ])
    m.add("Transeunte", 20, 12, [page([T("Pasa a tu lado sin mirarte. Nadie te mira en esta\ncalle. Es lo único bueno que tiene.")],
                                      char="vacas_transeunte", d=2, move_type=1, speed=3, freq=3)])
    m.add("Alcantarilla", 23, 12, [page([
        T("Una rejilla de alcantarilla. De abajo sube aire\ncaliente y un olor dulce, a establo."),
        T("Y algo más. Muy lejos. Muy abajo. Como un\nrebaño respirando a la vez."),
        IF(c_ss("A", False), [VEN(3), SS("A")]),
    ], char=COSAS, d=2, pat=3, dirfix=True, walk=False, through=True)])
    m.add("Furgoneta", 31, 11, [
        page([]),
        page([T("Una furgoneta blanca con letras rojas. Huele a\nlejía. Por debajo de la puerta trasera gotea\nalgo oscuro.")],
             sw1=S_MANANA, char="vacas_furgoneta", dirfix=True, walk=False),
    ])
    for x in (30, 32):
        m.add("Bloqueo furgoneta", x, 11, [page([]), page([], sw1=S_MANANA, char="vacas_vacio", dirfix=True, walk=False)])
    for (x, y) in [(4, 11), (13, 10), (16, 13), (27, 14), (36, 10), (34, 15)]:
        m.add("Charco", x, y, [page([], char=COSAS, d=2, pat=3, dirfix=True, walk=False, through=True, opacity=200)])
    HOM = "\\c[4]Hombre del matadero:\\c[0] "
    entrevista = [
        T(HOM + "¿Vienes por el anuncio? Llegas justo. Los otros\nya están dentro."),
        T("Lleva un mono blanco con manchas que no son de\npintura. Tiene las uñas negras hasta la raíz."),
        T(HOM + "Tres preguntas. La primera: ¿te mareas con la\nsangre?"),
        CHOICE(["No.", "No lo sé."], [
            [T(HOM + "Ya. Todos dicen que no.")],
            [T(HOM + "Al menos eres sincero. Eso se pierde el primer\ndía, ya verás.")],
        ], 0),
        T(HOM + "Segunda: ¿por qué quieres este trabajo?"),
        CHOICE(["Por el dinero.", "Para salir de casa.", "No lo quiero."], [
            [T(HOM + "Buena respuesta. La única buena, de hecho.")],
            [T("Se ríe sin abrir la boca."), T(HOM + "De casa no se sale, chaval. Se cambia de casa.\nY la nuestra huele peor.")],
            [T(HOM + "Nadie lo quiere. Por eso se paga.")],
        ], 0),
        T(HOM + "Tercera. Mírame las manos."),
        T("Le falta medio dedo índice. El corte es limpio,\nviejo, rosado como una goma de borrar."),
        T(HOM + "¿Te da asco?"),
        CHOICE(["Sí.", "No."], [
            [T(HOM + "Mejor. El asco te mantiene despierto. Cuando\nse te pase, ten cuidado.")],
            [T(HOM + "Mientes bien. Eso a Cripps le va a gustar.\nCripps es el capataz. Ya le conocerás.")],
        ], 0),
        T(HOM + "Vale. Valdrás. Sube atrás, con los demás.\nEmpiezas hoy."),
        SW(S_CONTRATADO), VAR(V_ETAPA, 7), SW(S_HUD_OFF), SW(S_SIN_EFECTOS),
        SE("024-Door01", 80, 70), TONE(-255, -255, -255, 0, 60), WAIT(60),
        STOPBGS(3), WEATHER(0, 0, 0),
        T("La furgoneta huele a lejía y, debajo de la\nlejía, a algo que la lejía no consigue tapar."),
        T("Por la ventanilla trasera ves el bloque hacerse\npequeño entre la lluvia."),
        T("Arriba, en la tercera planta, se mueve una\ncortina. Puede que sea ella. Puede que sea Perro\nintentando llegar a la ventana."),
        T("Por primera vez en años, Steven va a alguna\nparte."),
        T("Todavía no sabe que todos los caminos de esa\nfurgoneta terminan en el mismo sitio."),
        WAIT(40),
        SCRIPT("fin_del_acto"),
    ]
    m.add("Hombre del matadero", 28, 11, [
        page([]),
        page(entrevista, sw1=S_MANANA, char="vacas_reclutador", d=6),
    ])
    return m

# ======================================================================
# EVENTO COMUN 1: leer notas desde el menu
# ======================================================================
def evento_comun_notas():
    lst = flatten([
        IF(c_script("$vacas_ultimo_objeto == 4"), [
            T("La lista, escrita a lápiz, apretando tanto que\nel papel se ha roto en dos sitios:"),
            T("\\c[6]1. MI JARABE.\n2. EL PERRO, QUE SE CALLE.\n3. CARNE PICADA. MEDIO KILO. LA ROJA.\\c[0]"),
            T("Y al final, más pequeño:\n\\c[6]«Y búscate un trabajo, mueble.»\\c[0]"),
        ]),
        IF(c_script("$vacas_ultimo_objeto == 6"), [
            T("\\c[6]MATADERO MUNICIPAL. SE NECESITAN BRAZOS.\nTurnos de mañana y de noche. No se pide\nexperiencia. Se pide estómago.\\c[0]"),
            T("\\c[6]Presentarse junto al camión del matadero, en\nesta misma calle, a las seis de la mañana.\\c[0]"),
        ]),
        IF(c_script("$vacas_ultimo_objeto == 8"), [
            T("Un hombre joven delante de una furgoneta blanca.\nLa cara está rascada con una uña hasta el cartón."),
            T("En el dorso, a lápiz: \\c[6]«Matadero, primer día.»\\c[0]"),
            T(PIENSA + "(Nunca te dijo dónde trabajaba. Nunca nadie\nte dijo nada.)" + FIN),
        ]),
    ])
    lst.append({"code": 0, "indent": 0, "parameters": []})
    return ["update_database_entry", {"kind": "common_events", "id": 1, "updates": {
        "name": "Leer notas (objetos)", "trigger": 0, "switch_id": 1,
        "list": [{"_class": "RPG::EventCommand", **c} for c in lst]}}]
