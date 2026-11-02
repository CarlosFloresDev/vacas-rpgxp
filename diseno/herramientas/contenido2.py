# Contenido del Acto II de Vacas, «La cadena»: eventos del matadero.
# Texto original. Sin contenido sexual. La violencia se sugiere.
from ev import *
from contenido import (V_VENENO, PIENSA, FIN, AYUDA, MADRE, VOZ, COSAS, M_PISO, M_ESC)

# ---------------------------------------------------------------- ids
S_ACTO2, S_MATADERO, S_FICHADO, S_MONO, S_PATRULLA_CAM, S_NOCHE2, S_SUELDO = 22, 23, 24, 25, 26, 27, 28
S_PATRULLA_OFI, S_ESCONDIDO2, S_PILLADO_C, S_REGISTRO, S_PLANO = 29, 30, 31, 32, 33
S_PRIMERA, S_OBEDECIO, S_RESISTIO, S_GUARDO, S_PACTO, S_LUCY = 34, 35, 36, 37, 38, 39
S_PIEZA, S_VACA_FUERA, S_MADRE_PILLO, S_TURNO3, S_MANGUERA = 40, 41, 42, 43, 44
V_TURNO, V_FASE, V_SUELDO_HOY, V_SUELDO_TOTAL, V_GUERNSEY = 7, 8, 9, 10, 11
V_RESULT, V_PIEZAS, V_PIEZA, V_HUELLA, V_PILLADAS, V_PERRO = 12, 13, 14, 15, 16, 17
I_TARJETA, I_REGISTRO, I_PLANO, I_MANGUERA, I_NOTA_LUCY = 9, 10, 11, 12, 13
M_ENTRADA, M_VEST, M_CORR, M_CADENA, M_CAMARAS, M_OFICINA, M_PASILLO = 5, 6, 7, 8, 9, 10, 11

CRIPPS = "\\c[2]Cripps:\\c[0] "
CRIPPS_LEJOS = "\\c[2]Cripps (desde lejos):\\c[0] "
BENITO = "\\c[4]Benito:\\c[0] "
ENCARNA = "\\c[4]Encarna:\\c[0] "
RUBIO = "\\c[4]El Rubio:\\c[0] "
CHATO = "\\c[4]El Chato:\\c[0] "
REJILLA = "\\c[5]Voz en la rejilla:\\c[0] "
GUERN = "\\c[5]La Guernsey:\\c[0] "
LUCY = "\\c[3]Lucy:\\c[0] "
STEVEN = "\\c[6]Steven:\\c[0] "
OBJ = "vacas_matadero"

def FASE(n):
    return SCRIPT(f"fase({n})")
def COBRAR(expr):
    return SCRIPT(f"cobrar({expr})")
def si_turno(t, then, els=None):
    return IF(c_var(V_TURNO, t), then, els)
def si_fase(f, then, els=None):
    return IF(c_var(V_FASE, f), then, els)
def objeto(lst, d, pat, **kw):
    return page(lst, char=OBJ, d=d, pat=pat, dirfix=True, walk=False, **kw)
def puerta(dest_map, x, y, d, cond=None, negado=None, retro=None):
    """Lista de una puerta/hueco: si cond (switch) falta, texto y paso atras."""
    salir = [SE("024-Door01", 60, 80), TRANSFER(dest_map, x, y, d)]
    if cond is None:
        return salir
    return [IF(c_sw(cond), salir, [T(negado), MOVE(-1, [retro])] if retro else [T(negado)])]
def ambiente(tono, bgs, fog=("002-Clouds01", 30), extra=None):
    return [page([tono, BGS(*bgs), FOG(fog[0], fog[1], 0, 200, 1, 0)] + (extra or []) + [ERASE], trigger=4)]

TONO_CADENA = TONE(-14, -18, -20, 120)
TONO_FRIO = TONE(-50, -25, 12, 130)
TONO_PASILLO = TONE(-80, -78, -66, 110)
TONO_OFICINA = TONE(-20, -32, -55, 110)
TONO_CORRAL = TONE(-35, -38, -45, 110)
TONO_ALBA = TONE(-40, -40, -28, 105)
TONO_TARDE = TONE(-70, -62, -45, 120)
NEGRO = TONE(-255, -255, -255, 0, 30)

def mugido(v=55, p=55):
    return SE("070-Animal05", v, p)
def golpe_carne():
    return SE("093-Attack05", 70, 60)

def pillado_por_cripps(salida):
    """Autorun comun al sigilo: Cripps te ve. Veneno, pieza perdida, fuera."""
    mx, x, y, d = salida
    return page([
        SHAKE(8, 9, 20),
        VAR(V_PILLADAS, 1, 1),
        IF(c_var(V_PILLADAS, 1), [
            T(CRIPPS + "¿Qué haces tú aquí, escondiéndote como una rata entre la carne?"),
            T("Te agarra de la nuca con una mano que huele a hierro y a cebolla. Te aprieta hasta que oyes crujir algo."),
        ], [IF(c_var(V_PILLADAS, 2), [
            T(CRIPPS + "Otra vez. Te huelo, ¿sabes? Hueles a miedo nuevo. Aquí todo huele a miedo viejo."),
            T("Te empuja contra la pared helada. Se te queda pegada la mejilla al hielo, y al despegarla se queda allí un poco de ti."),
        ], [
            T(CRIPPS + "Una vez más y te cuelgo de un gancho para que aprendas cómo se ve esto desde arriba."),
            T("No es una broma. Él no hace bromas."),
        ])]),
        VEN(15),
        IF(c_script("veneno_al_maximo?"), [
            T("El frío entra y ya no sale. Algo en ti se queda colgado, quieto, en la oscuridad de la cámara."),
            WAIT(30), GAMEOVER,
        ]),
        IF(c_sw(S_PIEZA), [
            SW(S_PIEZA, False),
            T("La pieza se te ha caído al suelo. Tendrás que coger otra del final de la cinta."),
        ]),
        SW(S_PILLADO_C, False),
        TRANSFER(mx, x, y, d),
    ], sw1=S_PILLADO_C, trigger=3)

# ======================================================================
# MAPA 5: ENTRADA Y FICHAJE
# ======================================================================
def entrada():
    m = MapEvents(M_ENTRADA)
    m.add("Ambiente", 0, 0, [page([
        IF(c_var(V_FASE, 9, 0), [TONO_TARDE], [IF(c_var(V_FASE, 0, 0), [], [TONO_ALBA])]),
        WEATHER(1, 3, 0), BGS("005-Rain01", 45, 80), STOPBGM(1),
        FOG("002-Clouds01", 30, 0, 200, 2, 1), ERASE,
    ], trigger=4)])

    llegada = [
        TONE(-255, -255, -255, 0, 0), WAIT(30),
        si_turno(1, [
            T("La furgoneta frena en un patio de asfalto mojado. El motor se queda temblando un rato, como un perro después de mear."),
            TONE(-40, -40, -28, 105, 60), WAIT(50),
            T("El matadero municipal. Un edificio de ladrillo, ancho y bajo, con las ventanas pintadas de blanco por dentro para que nadie mire."),
            mugido(70, 50), WAIT(20),
            T("De algún sitio, detrás, llega un mugido. Luego otro, encima del primero. No suenan a vaca. Suenan a pregunta."),
            T(PIENSA + "(Huele a lejía. Y debajo de la lejía, a lo que la lejía intenta tapar. Conozco ese olor. Es el olor de la nevera de casa, pero de una nevera del tamaño de una iglesia.)" + FIN),
        ]),
        si_turno(2, [
            TONE(-40, -40, -28, 105, 50), WAIT(40),
            T("Segundo día. La furgoneta te escupe en el mismo charco que ayer."),
            T(PIENSA + "(Anoche soñé con ganchos. Esta mañana, al afeitarme, me temblaba la mano igual que tiembla la cinta.)" + FIN),
        ]),
        si_turno(3, [
            TONE(-48, -48, -34, 115, 70), WAIT(50),
            T("Tercer día. Llueve más fuerte. El camión de ganado ya está vacío y alguien lo baldea con una manguera. El agua sale rosa."),
            mugido(80, 45), WAIT(10),
            T(PIENSA + "(Hoy. La voz dijo que sería hoy.)" + FIN),
        ]),
        T(AYUDA + "(Ficha en la máquina del vestíbulo. El vestíbulo está subiendo, por la puerta del edificio.)" + FIN),
        FASE(1),
    ]
    m.add("Llegada", 0, 1, [
        page(llegada, sw1=S_MATADERO, trigger=3),
        page([], var=(V_FASE, 1)),
    ])

    # ---------------- furgoneta y camion de ganado
    m.add("Furgoneta", 12, 19, [page([
        T("La furgoneta blanca del matadero. En la puerta trasera alguien ha escrito con el dedo en la mugre: VUELVE."),
    ], char="vacas_furgoneta", dirfix=True, walk=False)])
    for x in (11, 13):
        m.add("Bloqueo furgoneta", x, 19, [page([], char="vacas_vacio", dirfix=True, walk=False)])
    m.add("Camion de ganado", 3, 16, [page([
        T("Un camión de ganado con las tablas rajadas. Dentro no queda nada. En el suelo de la caja hay marcas de pezuñas que parecen escritura."),
        IF(c_ss("A", False), [SE("041-Knock02", 60, 60), WAIT(20),
            T("Algo da un golpe dentro. Te asomas. Está vacío."), VEN(2), SS("A")]),
    ], char="vacas_furgoneta", dirfix=True, walk=False, hue=0)])
    for x in (2, 4):
        m.add("Bloqueo camion", x, 16, [page([], char="vacas_vacio", dirfix=True, walk=False)])
    m.add("Verja", 14, 21, [page([
        T("No te vas a ir andando. La furgoneta te ha traído y la furgoneta te llevará."),
        MOVE(-1, [UP])], trigger=1)])
    m.add("Verja 2", 15, 21, [page([
        T("No te vas a ir andando. La furgoneta te ha traído y la furgoneta te llevará."),
        MOVE(-1, [UP])], trigger=1)])

    # ---------------- Benito en el patio
    m.add("Benito patio", 17, 16, [
        page([
            si_turno(1, [
                T(BENITO + "¿El nuevo? Benito. Treinta y un años en la cadena. Fíjate bien en mis manos, que el primer día es lo único que vas a querer mirar."),
                T("Tiene las manos limpias. Demasiado limpias. Rosadas de tanto frotar."),
                T(BENITO + "Lo primero, fichar. La máquina del vestíbulo. Si no fichas, no existes. Y si no existes, Cripps te puede hacer lo que quiera, que no consta."),
            ]),
            si_turno(2, [T(BENITO + "Ah, volviste. La mitad no vuelve el segundo día. La otra mitad no vuelve el tercero.")]),
            si_turno(3, [
                T(BENITO + "Hoy te ha mirado raro, Cripps. Al pasar. Como mira a las que van a ir al cajón."),
                T(BENITO + "No es nada. Ficha y no pienses."),
            ]),
        ], sw1=S_MATADERO, char="vacas_obrero1", d=4),
        page([], var=(V_FASE, 2)),
    ])

    # ---------------- vestibulo
    fichar_entrada = [
        SE("032-Switch01", 90, 60), WAIT(6), SE("040-Knock01", 80, 120),
        T("Metes la tarjeta. La máquina la muerde con un ruido de dientes y la escupe marcada."),
        si_turno(1, [
            ITEM(I_TARJETA), SE("046-Book01"),
            T("Es tu tarjeta. Pone STEPHEN, con PH. Nadie va a corregirlo."),
            T(AYUDA + "(Tienes la Tarjeta de fichar. Puedes leerla desde el menú.)" + FIN),
        ]),
        SW(S_FICHADO), FASE(2),
        None,   # presentacion de Cripps (se rellena abajo)
    ]
    CRIPPS_V = m.reserve("Cripps vestibulo")
    # la presentacion de Cripps (solo el primer dia)
    presentacion = [
        EVLOC(CRIPPS_V, 24, 3, 2),
        MOVE(CRIPPS_V, steps(DOWN, 1) + steps(LEFT, 8) + [turn(4)]), WAITMOVE,
        T(CRIPPS + "Tú."),
        T("Es grande de una forma que no tiene que ver con la altura. Ocupa el aire. El delantal le llega a las botas y no tiene ni una mancha: las manchas las lleva en los antebrazos, secas, como tatuajes."),
        T(CRIPPS + "Steven. Stephen. Me da igual. Aquí os llamo a todos igual: «chaval», hasta que os ganáis otro nombre o hasta que os vais."),
        T(CRIPPS + "Soy Cripps. Esto es mío. No el edificio: el edificio es del ayuntamiento. Lo que pasa dentro es mío."),
        T("Se acerca. Te huele el cuello, despacio, como se huele un melón en el mercado."),
        T(CRIPPS + "Hueles a casa. A madre. Eso se quita en una semana."),
        CHOICE(["Bajar la mirada", "Sostenerle la mirada"], [[
            T(CRIPPS + "Bien. Las que bajan la cabeza dan menos trabajo."),
            VEN(3),
        ], [
            T("Le aguantas la mirada un segundo. Dos. Él sonríe con la boca y con nada más."),
            T(CRIPPS + "Ah. Uno con ojos. Me gustan los que tienen ojos. Se les nota todo."),
            VEN(5),
        ]], 0),
        T(CRIPPS + "Vestuario. Taquilla trece. Te pones el mono y te vienes a la cadena. La cinta. No me hagas buscarte."),
        MOVE(CRIPPS_V, [turn(6)] + steps(RIGHT, 8) + steps(UP, 1)), WAITMOVE,
        SE("026-Door03", 70, 70),
        T(AYUDA + "(El vestuario está por la puerta de la izquierda del vestíbulo.)" + FIN),
    ]
    fichar_entrada[-1] = si_turno(1, [WAIT(20), SE("026-Door03", 80, 70),
                                      T("La puerta de la cadena se abre de una patada."), presentacion])
    fichar_salida = [
        SE("032-Switch01", 90, 60), WAIT(6), SE("040-Knock01", 80, 120),
        T("La máquina muerde la tarjeta otra vez. Ya está. Hoy has existido de las seis a las seis."),
        IF(c_sw(S_MONO), [SCRIPT("poner_mono(false)"),
                          T("Te arrancas el mono aquí mismo y lo dejas en el banco. Debajo, tu ropa huele igual.")]),
        T("Hoy has ganado \\v[9] monedas."),
        SW(S_MATADERO, False), SW(S_NOCHE2), SW(S_SUELDO, False),
        TONE(-255, -255, -255, 0, 40), STOPBGS(3), WEATHER(0, 0, 0), WAIT(40),
        T("La furgoneta de vuelta va llena de hombres callados. Nadie habla de lo que ha hecho. Alguien silba algo y se calla a mitad."),
        si_turno(1, [T("Te miras las uñas todo el camino. Debajo de cada una hay una media luna oscura que no es tierra.")]),
        si_turno(2, [T("Por la ventanilla pasa la ciudad. En cada alcantarilla te parece ver unos ojos. Uno de los hombres dice: «Esta noche mugen fuerte, ¿eh?», y nadie le contesta.")]),
        si_turno(3, [T("No sientes las manos. Ni el dedo. Sobre todo el dedo."),
                     T("Benito, a tu lado, te da una palmada en la rodilla. No dice nada. Es la palmada que se le da a alguien en un entierro.")]),
        T("La furgoneta te deja en la esquina de tu calle. Subes la escalera a oscuras."),
        TRANSFER(M_ESC, 4, 11, 8),
        TONE(-70, -70, -50, 110, 40), WAIT(20),
        T(AYUDA + "(Es de noche. Entra en casa: madre espera su sueldo.)" + FIN),
    ]
    fichadora = [
        IF(c_var(V_FASE, 1, 0), fichar_entrada, [
            IF(c_var(V_FASE, 9, 0), fichar_salida, [
                T("La fichadora hace tic-tac por dentro, más fuerte que un reloj. Tu tarjeta ya está marcada. Hasta que suene la sirena, eres del matadero."),
            ]),
        ]),
    ]
    m.add("Fichadora", 14, 3, [objeto([IF(c_sw(S_MATADERO), fichadora, [])], 6, 0)])
    cripps_hablar = [
        si_turno(1, [T(CRIPPS + "¿Todavía aquí? Taquilla trece. El mono. Muévete.")]),
        si_turno(2, [T(CRIPPS + "Llegas a la hora. Qué decepción. Me gustaba imaginar qué te iba a hacer."),
                     T(CRIPPS + "Hoy cortas. Mono, y a la cadena.")]),
        si_turno(3, [T(CRIPPS + "Hoy es un día bonito, chaval."),
                     T("No dice por qué. Se limpia las uñas con una navaja pequeña, mirándote, y se ríe solo.")]),
    ]
    m.set("Cripps vestibulo", 24, 3, [
        page([]),
        page(cripps_hablar, sw1=S_MATADERO, var=(V_FASE, 2), char="vacas_cripps", d=4),
        page([], var=(V_FASE, 3)),
    ])
    m.add("Puerta vestuario", 5, 2, [page(puerta(M_VEST, 9, 12, 8), trigger=1)])
    m.add("Puerta cadena", 24, 2, [page([
        T("Un cartel en la puerta: \\c[6]PROHIBIDO PASAR SIN MONO. ENTRADA POR EL VESTUARIO.\\c[0]"),
        T("Del otro lado llega un zumbido grande y continuo, como si el edificio entero tuviera fiebre."),
        MOVE(-1, [DOWN])], trigger=1)])
    m.add("Tablon normas", 8, 2, [page([
        T("Un tablón con las normas, escritas a máquina hace mucho:"),
        T("\\c[6]1. SE FICHA AL ENTRAR Y AL SALIR.\n2. NADIE ENTRA EN LA CADENA SIN MONO.\n3. LO QUE SE CAE AL SUELO, NO SE RECOGE.\\c[0]"),
        T("\\c[6]4. EL CAPATAZ DECIDE.\\c[0]"),
        T("Alguien añadió a boli, abajo, con letra temblona: \\c[6]5. NO ESCUCHES A LAS PAREDES.\\c[0]"),
    ], char="vacas_tablon", d=2, pat=1, dirfix=True, walk=False)])
    m.add("Banco vestibulo", 10, 7, [page([T("Un banco largo. Aquí se sientan a fumar antes del turno. Las colillas están todas pisadas en el mismo punto, como si apagarlas fuera también un trabajo.")])])
    m.add("Reloj vestibulo", 17, 2, [page([T("El reloj del vestíbulo marca la hora de verdad. Es el único reloj de tu vida que no va tarde.")])])
    m.add("Cubo vestibulo", 27, 3, [page([T("Un cubo con agua roja y una fregona dentro. La fregona tiene pelo. No es de fregona.")])])
    m.add("Cartel fachada", 11, 10, [page([T("\\c[6]MATADERO MUNICIPAL\\c[0]. Debajo, en letras más pequeñas, borradas por la lluvia: \\c[6]«CARNE PARA LA CIUDAD»\\c[0].")])])
    m.add("Cartel fachada 2", 18, 10, [page([T("Alguien tachó «CARNE» y escribió encima, con pintura roja: \\c[6]«NOSOTROS»\\c[0]. Lo han intentado borrar varias veces.")])])
    return m

# ======================================================================
# MAPA 6: VESTUARIO
# ======================================================================
def vestuario():
    m = MapEvents(M_VEST)
    m.add("Ambiente", 0, 0, ambiente(TONE(-20, -24, -30, 115), ("016-Drips01", 45, 90), extra=[STOPBGM(1)]))
    m.add("Salida vestibulo", 9, 13, [page(puerta(M_ENTRADA, 5, 3, 2), trigger=1)])
    m.add("Salida vestibulo 2", 10, 13, [page(puerta(M_ENTRADA, 5, 3, 2), trigger=1)])
    m.add("Salida cadena", 19, 7, [page(puerta(M_CADENA, 5, 21, 8, S_MONO,
        "Sin el mono no pasas. Lo dice el cartel. Lo diría Cripps, con la mano.", LEFT), trigger=1)])
    ponerse = [
        si_turno(1, [
            T("Taquilla trece. Dentro hay un mono blanco con otro nombre bordado en el pecho: \\c[6]R. MATA\\c[0]."),
            T("Huele a lejía y al sudor de un desconocido. En la rodilla izquierda, una mancha que la lejía ha vuelto marrón."),
            T(PIENSA + "(¿Dónde está R. Mata? ¿Por qué ya no necesita su mono?)" + FIN),
        ]),
        si_turno(2, [
            T("El mono te espera colgado, todavía húmedo de ayer. Te queda un poco mejor. Como si se estuviera acostumbrando a ti."),
            T("En el bolsillo encuentras un papel doblado que ayer no estaba. Letra de lápiz, apretada:"),
            T("\\c[6]«NO LE CONTESTES A LA REJILLA. YO LE CONTESTÉ. — R.M.»\\c[0]"),
            VEN(3),
        ]),
        si_turno(3, [
            T("Te pones el mono. Hoy pesa. Como si alguien lo hubiera llenado de agua por dentro."),
        ]),
        SE("045-Push01", 70, 90), SCRIPT("poner_mono(true)"), FASE(3),
        T(AYUDA + "(Ya llevas el mono. La cadena está por la puerta de la derecha del vestuario.)" + FIN),
    ]
    taquilla = [
        IF(c_var(V_FASE, 2, 0), ponerse, [
            IF(c_sw(S_MONO), [T("Tu ropa de calle cuelga dentro como un hombre que se ha ido.")],
               [T("La taquilla trece. Un candado sin cerrar: aquí nadie roba nada. No hay nada que robar.")]),
        ]),
    ]
    m.add("Taquilla 13", 7, 3, [page([IF(c_sw(S_MATADERO), taquilla, [])])])
    m.add("Taquilla forzada", 3, 3, [page([
        T("Una taquilla con la puerta doblada hacia fuera. Desde dentro."),
        T("En el fondo hay paja. Paja fresca, amarilla, como la de los corrales."),
    ])])
    m.add("Taquilla Benito", 5, 3, [page([
        T("La taquilla de Benito. Hay fotos pegadas por dentro: una niña en una comunión, la misma niña más mayor, y luego ninguna más."),
    ])])
    m.add("Taquilla vacia", 10, 3, [page([
        T("Vacía. Huele a desinfectante muy fuerte. Alguien ha limpiado aquí algo con mucho cuidado."),
    ])])
    m.add("Fregaderos", 15, 3, [page([
        T("Te lavas las manos. El agua sale tibia y rosada al principio, luego clara, luego otra vez rosada sin que sepas de dónde."),
        IF(c_sw(S_PRIMERA), [T(PIENSA + "(Me froto el dedo índice hasta que duele. Sigue siendo el mismo dedo.)" + FIN)]),
    ])])
    m.add("Desague vestuario", 15, 9, [page([
        T("Un sumidero en el suelo. Por él sube un sonido muy lejano, como si debajo de la ciudad algo grande masticara despacio."),
        IF(c_ss("A", False), [VEN(2), SS("A")]),
    ], through=True)])
    m.add("Encarna", 13, 8, [page([
        si_turno(1, [
            T(ENCARNA + "Encarna. Vísceras. Lo que tú tiras, yo lo separo: lo que se vende, lo que se pica y lo que no se nombra."),
            T(ENCARNA + "Un consejo, guapo: respira por la boca los tres primeros días. Luego ya da igual, porque ya no hueles nada."),
        ]),
        si_turno(2, [
            T(ENCARNA + "¿Has oído la rejilla? No me mires así. Todos la hemos oído alguna vez. Unos la oyen más que otros."),
            T(ENCARNA + "El chico de antes la oía muchísimo. Mata. Ramón Mata. Un día dejó de venir."),
        ]),
        si_turno(3, [
            IF(c_var(V_FASE, 6, 1), [
                IF(c_sw(S_OBEDECIO), [
                    T(ENCARNA + "Ya está, ¿eh? Ya pasó. A todos nos pasó un día. Luego se te olvida la cara."),
                    T(ENCARNA + "Mentira. No se te olvida. Pero se te olvida que te acuerdas."),
                ], [
                    T(ENCARNA + "Te he visto bajar la pistola. Desde la mesa de vísceras se ve todo."),
                    T(ENCARNA + "Nadie le había dicho que no a Cripps en años. Ten cuidado. Ahora te mira a ti como miraba a la vaca."),
                ]),
            ], [
                T(ENCARNA + "Hoy no hables mucho. Hay días en que la cadena escucha."),
            ]),
        ]),
    ], sw1=S_MATADERO, char="vacas_obrero3", d=4)])
    m.add("El Chato", 4, 8, [page([
        T("El Chato está sentado en el banco, comiendo algo de un papel de periódico. No levanta la vista."),
        si_turno(1, [T(CHATO + "...")]),
        si_turno(2, [T(CHATO + "Está buena cruda. Más buena que cocida. Cocida ya no te dice nada.")]),
        si_turno(3, [T(CHATO + "La de hoy era lechera. Se nota en la ubre. Lo he notado en el cubo."), VEN(2)]),
    ], sw1=S_MATADERO, char="vacas_obrero4", d=8)])
    return m

# ======================================================================
# MAPA 7: CORRALES
# ======================================================================
def corrales():
    m = MapEvents(M_CORR)
    m.add("Ambiente", 0, 0, ambiente(TONO_CORRAL, ("002-Wind02", 35, 60), extra=[STOPBGM(1)]))
    m.add("Mugidos", 0, 1, [page([WAIT(200), mugido(50, 50), WAIT(260), mugido(40, 62)], trigger=4)])
    for y in (3, 4):
        m.add("Manga a la cadena", 29, y, [page(puerta(M_CADENA, 1, 7, 6), trigger=1)])
    frases = [
        "Te mira con un ojo, luego con el otro, como si con uno solo no se creyera lo que ve.",
        "Tiene una etiqueta amarilla en la oreja con un número. El número es más largo que tu nombre.",
        "Te huele la mano a través de la valla. Su aliento es caliente y huele a hierba. Es lo único vivo que huele a hierba en kilómetros.",
        "Está temblando. No hace frío.",
    ]
    VACA = []
    for i, (x, y) in enumerate([(4, 10), (6, 13), (13, 9), (15, 12), (21, 14), (26, 9)]):
        VACA.append(m.add("Vaca", x, y, [page([
            T(frases[i % len(frases)]),
            IF(c_ss("A", False), [VEN(1), SS("A")]),
        ], char="vacas_vaca", d=2, move_type=1, speed=2, freq=2)]))
    VFONDO = m.add("Vaca del fondo", 24, 12, [
        page([
            T("Esta es distinta. Más pequeña, de un color de leche con canela. Tiene las pestañas claras."),
            T("No se mueve. No te mira. Mira la puerta del corral como quien espera el autobús."),
            IF(c_sw(S_TURNO3), [T(PIENSA + "(La del fondo. Me ha mandado traer a la del fondo.)" + FIN)]),
        ], char="vacas_vaca_canela", d=8, move_type=0, speed=2),
        page([], sw1=S_VACA_FUERA),
    ])
    traer = [
        T("Abres la puerta del corral. Los goznes chillan. La vaca del fondo levanta la cabeza."),
        CHOICE(["Llamarla en voz baja", "Usar la picana"], [[
            T("Le hablas bajito, como a Perro cuando tiene pesadillas. Ella viene hacia ti, confiada, sin prisa."),
            T(PIENSA + "(Viene porque la llamo. Viene porque confía. Eso es peor que todo lo demás.)" + FIN),
            VEN(5),
        ], [
            SE("123-Thunder01", 60, 120), FLASH(200, 200, 255, 120, 6),
            T("La picana chasquea. La vaca da un respingo, muge y sale trotando, con la piel temblándole a trozos."),
            T(PIENSA + "(Me ha salido muy fácil. Eso me da más miedo que el ruido.)" + FIN),
            VEN(7),
        ]], 0),
        MOVE(-1, [LEFT, turn(6)]), WAITMOVE,
        MOVE(VFONDO, [mv(37)] + steps(LEFT, 1) + steps(UP, 8) + steps(RIGHT, 4) + [mv(42, 0), mv(38)]),
        mugido(70, 50), WAITMOVE,
        SW(S_VACA_FUERA), FASE(5),
        T("La vaca entra en la manga y sigue sola, hacia el zumbido. Las vacas siempre van hacia el zumbido."),
        T(AYUDA + "(Vuelve a la cadena. Al cajón.)" + FIN),
    ]
    puerta_txt = "Una puerta de corral, de barras de hierro. El cerrojo está pegajoso."
    m.add("Puerta corral 1", 4, 7, [page([T(puerta_txt)])])
    m.add("Puerta corral 2", 13, 7, [page([T(puerta_txt)])])
    m.add("Puerta corral 3", 23, 7, [page([
        IF(c_sw(S_TURNO3), [IF(c_var(V_FASE, 4, 0), traer, [T(puerta_txt)])], [T(puerta_txt)]),
    ])])
    m.add("El Rubio", 6, 5, [page([
        si_turno(1, [
            T(RUBIO + "Yo soy el de los corrales. Las traigo, las cuento, las mando a la manga. Nunca entro en la cadena. Nunca."),
            T(RUBIO + "Así puedo decir en casa que yo trabajo con animales. Vivos."),
        ]),
        si_turno(2, [
            T(RUBIO + "Anoche se escapó una. Bueno, se escapó hace años. Pero anoche la volví a soñar."),
            T(RUBIO + "Una Guernsey. Color canela. Se metió por el desagüe grande y ya no salió. Cripps hizo como que no había pasado."),
        ]),
        si_turno(3, [
            IF(c_var(V_FASE, 5, 1), [
                T(RUBIO + "...")], [
                T(RUBIO + "¿Vienes a por una? La del fondo. Cripps la ha elegido él. Siempre elige las que miran."),
            ]),
        ]),
    ], sw1=S_MATADERO, char="vacas_obrero2", d=8)])
    m.add("Picana", 26, 2, [page([
        T("En la pared, junto a la manguera, cuelga una picana eléctrica. Tiene la empuñadura gastada en la forma exacta de una mano grande."),
    ])])
    m.add("Cubo corrales", 2, 17, [page([T("Un cubo con pienso mojado. Nadie lo ha tocado. No vale la pena alimentar lo que va a la manga.")])])
    return m

# ======================================================================
# MAPA 8: LA CADENA
# ======================================================================
def cadena():
    m = MapEvents(M_CADENA)
    CR = m.reserve("Cripps")
    VACA_C = m.reserve("Vaca del cajon")
    m.add("Ambiente", 0, 0, ambiente(TONO_CADENA, ("015-Quake01", 32, 50), extra=[STOPBGM(1)]))
    m.add("Ruido de la cadena", 0, 1, [page([
        WAIT(150), SE("044-Chest01", 45, 50), WAIT(90), golpe_carne(), WAIT(220), mugido(35, 45),
    ], sw1=S_MATADERO, trigger=4)])
    # ---------------- salidas
    m.add("A los corrales", 0, 7, [page(puerta(M_CORR, 28, 4, 4), trigger=1)])
    m.add("A las camaras", 39, 9, [page(puerta(M_CAMARAS, 1, 17, 6), trigger=1)])
    m.add("Al vestuario", 5, 22, [page(puerta(M_VEST, 18, 7, 4), trigger=1)])
    m.add("Al pasillo", 32, 22, [page(puerta(M_PASILLO, 1, 7, 6), trigger=1)])
    m.add("Puerta oficina", 35, 2, [
        page([T("Una puerta metálica. Detrás, unas escaleras suben a la oficina de Cripps. Cerrada con llave."),
              MOVE(-1, [DOWN])], trigger=1),
        page([IF(c_var(V_FASE, 6, 0), [
            T("La puerta de la oficina está entornada. Cripps ha bajado. Se le oye en algún sitio, lejos, silbando."),
            SE("024-Door01", 50, 70), TRANSFER(M_OFICINA, 9, 12, 8),
        ], [T("Cerrada con llave."), MOVE(-1, [DOWN])])], sw1=S_PATRULLA_OFI, trigger=1),
    ])

    # ---------------- canales colgadas (decorado: bloquean y tapan)
    canal_txt = [
        "Una canal colgada del gancho. Vacía por dentro, abierta como un libro que alguien ha terminado de leer.",
        "Gotea. Cada gota tarda lo mismo en caer. Es el único reloj de la cadena.",
        "Todavía está tibia. El calor se le va saliendo por el corte, en un vaho que sube hacia las luces.",
        "Tiene un sello morado en la grupa: APTO. Alguien ha decidido que esto es apto.",
    ]
    i = 0
    for y in (6, 12):
        for x in range(6, 38, 3):
            if (x, y) == (21, 12):
                continue
            pat = (i % 3)
            m.add("Canal", x, y, [page([
                T(canal_txt[i % len(canal_txt)]),
                IF(c_var(V_VENENO, 55, 1), [IF(c_ss("A", False), [
                    T("La canal se gira despacio en el gancho, sin que nadie la toque, hasta quedar de frente a ti."), VEN(2), SS("A")])]),
            ], char=OBJ, d=4, pat=pat if pat < 2 else 0, dirfix=True, walk=False)])
            i += 1

    # ---------------- la cinta (animada) y el puesto de la cinta
    puesto_cinta = [
        IF(c_var(V_TURNO, 1, 0), [IF(c_var(V_FASE, 3, 0), [
            T("Tu puesto en la cinta. Las piezas llegan desde la sierra, una detrás de otra, sin principio ni final."),
            T(BENITO + "Cada pieza lleva marcada la flecha del corte. Tú la giras hacia donde marca, antes de que pase. Si se te escapa una, se atasca todo. Y si se atasca todo, viene él."),
            T(AYUDA + "(Pulsa la flecha de cada pieza cuando entre en el recuadro.)" + FIN),
            SCRIPT("minijuego_cinta(12)"),
            COBRAR("3 + $game_variables[12] / 2"), VEN(6),
            IF(c_var(V_RESULT, 7, 4), [
                SE("092-Attack04", 80, 70), SHAKE(5, 8, 10),
                T(CRIPPS_LEJOS + "¡Nuevo! ¡Que se te amontonan! ¿Quieres que te ponga a ti en la cinta, a ver si así aprendes a qué velocidad va?"),
                VEN(4),
            ], [
                T(BENITO + "No está mal. Ten cuidado, que si se te da bien, te sube de puesto. Y los puestos de arriba están más cerca del cajón."),
            ]),
            T(CRIPPS_LEJOS + "¡Tú! La manguera grande se ha quedado en el pasillo de mantenimiento, junto a la rejilla. Tráemela. Y no te entretengas: ahí abajo no hay nada que ver."),
            FASE(4),
            T(AYUDA + "(El pasillo de mantenimiento está por la puerta de abajo a la derecha.)" + FIN),
        ], [T("La cinta corre. Las piezas pasan. Las manos de los demás se mueven solas, como si la cinta tirara de ellas.")])],
           [T("La cinta corre. Las piezas pasan. Las manos de los demás se mueven solas, como si la cinta tirara de ellas.")]),
    ]
    for x in range(9, 30):
        if x == 19:
            m.add("Puesto de la cinta", x, 15, [page(puesto_cinta, char=OBJ, d=2, pat=0, dirfix=True, walk=False, step=True)])
        else:
            m.add("Cinta", x, 15, [page([], char=OBJ, d=2, pat=0, dirfix=True, walk=False, step=True, through=True)])

    # ---------------- el puesto de corte
    corte = [
        T("Una canal entera, recién bajada de la sierra. Encima, la línea de tiza por donde hay que abrirla."),
        T(BENITO + "Despacio no, que se enfría y se agarrota. Deprisa tampoco, que el hueso se astilla. Suelta la cuchilla justo encima de la marca."),
        T(AYUDA + "(Pulsa Intro cuando la cuchilla cruce la franja roja.)" + FIN),
        SCRIPT("minijuego_corte(6)"),
        COBRAR("4 + $game_variables[12]"), VEN(8),
        IF(c_var(V_RESULT, 3, 4), [
            T("Una mano enorme te agarra la muñeca desde atrás. Cripps. No le has oído llegar."),
            T(CRIPPS + "Así no. Así."),
            T("Guía tu mano con la suya. La cuchilla entra sola. Te suelta y se limpia la mano en tu mono, a la altura del corazón."),
            VEN(6),
        ], [
            T(CRIPPS_LEJOS + "Mira tú. Tiene pulso el nuevo."),
        ]),
        T(CRIPPS + "Ahora cargas. Lo que sale por el final de la cinta va a las cámaras frías: los cuartos a la primera, las vísceras a la segunda, las cabezas a la tercera."),
        T(CRIPPS + "Tres viajes. Yo estaré allí dentro, contando. Si te veo parado, o escondido, o mirando lo que no es, lo sabré."),
        SW(S_PATRULLA_CAM), FASE(4), VAR(V_PIEZAS, 0),
        T(AYUDA + "(Coge una pieza al final de la cinta y llévala a su cámara. Cripps vigila: no dejes que te vea de frente. Puedes esconderte entre las canales y detrás de las cajas.)" + FIN),
    ]
    m.add("Puesto de corte", 21, 12, [page([
        IF(c_var(V_TURNO, 2, 0), [IF(c_var(V_FASE, 3, 0), corte, [T("La canal que abriste. Ya no parece nada que haya caminado.")])],
           [T("Una canal en espera, con una línea de tiza por el lomo. Hoy no te toca cortar.")]),
    ], char=OBJ, d=4, pat=0, dirfix=True, walk=False)])

    # ---------------- final de la cinta: coger piezas
    piezas = [
        IF(c_sw(S_PIEZA), [T("Ya llevas una pieza. Primero suéltala en su cámara.")], [
            VARRAND(V_PIEZA, 1, 3), SW(S_PIEZA), SE("045-Push01", 70, 70),
            IF(c_var(V_PIEZA, 1), [T("Te cae en los brazos un \\c[6]cuarto trasero\\c[0]. Pesa como un niño dormido y está igual de tibio.")]),
            IF(c_var(V_PIEZA, 2), [T("Coges un cubo de \\c[6]vísceras\\c[0]. Todavía humean. Algo dentro hace un ruido suave, de burbuja.")]),
            IF(c_var(V_PIEZA, 3), [
                T("Te dan una \\c[6]cabeza\\c[0], sin piel. Los ojos siguen puestos."),
                IF(c_var(V_VENENO, 50, 1), [T("Uno de los ojos se mueve para seguirte. Seguramente."), VEN(2)]),
            ]),
            T(PIENSA + "(Cuartos a la primera cámara, vísceras a la segunda, cabezas a la tercera.)" + FIN),
        ]),
    ]
    m.add("Final de la cinta", 30, 15, [page([
        IF(c_sw(S_PATRULLA_CAM), piezas,
           [T("Aquí acaba la cinta. Las piezas caen en una bandeja de acero con un ruido blando, como de aplauso.")]),
    ])])

    # ---------------- Cripps en la cadena
    cripps = [
        si_turno(1, [
            IF(c_var(V_FASE, 3, 0), [T(CRIPPS + "La cinta. Puesto del medio. ¿Necesitas que te lleve de la mano?")]),
            IF(c_var(V_FASE, 4, 0), [T(CRIPPS + "¿Y mi manguera? ¿Te la has comido por el camino?")]),
            IF(c_var(V_FASE, 5, 0), [
                ITEM(I_MANGUERA, -1),
                T("Le das la manguera. La enrolla en el brazo sin dejar de mirarte."),
                T(CRIPPS + "Has tardado. ¿Te ha contado algo la rejilla?"),
                CHOICE(["No.", "¿Qué rejilla?"], [[
                    T(CRIPPS + "No. Claro que no. Las paredes no hablan."),
                ], [
                    T(CRIPPS + "Ninguna. Ninguna rejilla. Buen chico."),
                ]], 0),
                T("Se acerca tanto que ves los pelos negros dentro de su nariz."),
                T(CRIPPS + "Aquí había un chaval que oía cosas. Ramón. Le dejé de oír yo a él."),
                COBRAR(2), VEN(5),
                T(CRIPPS + "Por hoy, basta. Ve a fichar. Y mañana vienes con hambre: mañana cortas."),
                FASE(9),
                T(AYUDA + "(El turno ha terminado. Ficha la salida en el vestíbulo, pasando por el vestuario.)" + FIN),
            ]),
            IF(c_var(V_FASE, 9, 0), [T(CRIPPS + "¿Sigues aquí? Fuera. Que te vea mañana.")]),
        ]),
        si_turno(2, [
            IF(c_var(V_FASE, 3, 0), [T(CRIPPS + "El puesto de corte. Esa canal de ahí, la que tiene la tiza. Te espera.")]),
            IF(c_var(V_FASE, 5, 0), [
                T(CRIPPS + "Descanso. Diez minutos. Ni uno más."),
                T(CRIPPS + "Y no bajes al pasillo de mantenimiento. Ahí no se te ha perdido nada. Nada."),
            ]),
            IF(c_var(V_FASE, 7, 1), [
                T(CRIPPS + "Hueles a papel. ¿Has estado leyendo, chaval?"),
                T("No espera respuesta. Te mira las manos."),
                IF(c_var(V_FASE, 9, 0), [
                    T(CRIPPS + "Vete a casa. Duerme bien."),
                    T(CRIPPS + "Mañana te toca el cajón."),
                    VEN(6),
                ]),
            ]),
        ]),
        si_turno(3, [
            IF(c_var(V_FASE, 3, 0), [
                T(CRIPPS + "Por fin. Hoy es tu día, chaval."),
                T("Señala con la barbilla el cajón de aturdimiento, al fondo, junto a la entrada de la manga. Un cajón de acero del tamaño de una vaca. Exactamente."),
                T(CRIPPS + "Vas a los corrales y me traes la del fondo, la del tercer corral. La de color canela. Luego vienes aquí y haces lo que hace un hombre."),
                T(CRIPPS + "El Rubio te abre si no sabes. Pero sabrás."),
                FASE(4), VEN(6),
                T(AYUDA + "(Los corrales están por el hueco de la izquierda, por la manga.)" + FIN),
            ]),
            IF(c_var(V_FASE, 4, 0), [T(CRIPPS + "¿A qué esperas? ¿A que venga ella sola? Vendría, ¿eh? Vienen solas. Eso es lo bonito.")]),
            IF(c_var(V_FASE, 9, 0), [
                IF(c_sw(S_OBEDECIO), [T(CRIPPS + "Mañana, otra. Y pasado, otra. Hasta que ya no las cuentes.")],
                   [T(CRIPPS + "Mañana lo harás solo. Y si no, te meto a ti en el cajón para que veas lo pequeño que es.")]),
            ]),
        ]),
    ]
    m.set("Cripps", 16, 9, [
        page([]),
        page(cripps, sw1=S_MATADERO, char="vacas_cripps", d=2, move_type=3, speed=2, freq=3,
             mroute=route([mwait(120), turn(4), mwait(80), turn(6), mwait(100), turn(2)], True, True)),
        page([], sw1=S_PATRULLA_CAM),
        page([], sw1=S_PATRULLA_OFI),
    ])
    for nombre, x, y, char, d, lineas in [
        ("Benito", 14, 16, "vacas_obrero1", 8, {
            1: ["No mires a los ojos de las cabezas. Las cabezas no hacen nada, pero mejor no."],
            2: ["¿Ya has oído lo del pasillo? Ni caso. Hay corrientes de aire. Las corrientes de aire hacen ruidos."],
            3: ["Hoy no me hables. Hoy te toca a ti. No me hables, que luego me acuerdo."]}),
        ("Obrero de la sierra", 24, 16, "vacas_obrero2", 8, {
            1: ["Yo estoy en la sierra. No oigo nada. Hace años que no oigo nada. Es una suerte."],
            2: ["¿Qué? ¡No te oigo! ¡La sierra!"],
            3: ["Dicen que hoy entras al cajón. Al principio tiemblan las manos. Luego, el resto."]}),
    ]:
        m.add(nombre, x, y, [page([
            si_turno(t, [T(f"\\c[4]{nombre}:\\c[0] " + l) for l in ls]) for t, ls in lineas.items()
        ], sw1=S_MATADERO, char=char, d=d, dirfix=True)])
    m.add("Encarna cadena", 26, 19, [page([
        T(ENCARNA + "No mires mis cubos. Lo de dentro de un animal se parece demasiado a lo de dentro de una persona. Por eso no se mira."),
    ], sw1=S_MATADERO, char="vacas_obrero3", d=8, dirfix=True)])

    # ---------------- el cajon, la pistola, la vaca
    m.add("Cajon", 2, 4, [page([
        T("El cajón de aturdimiento. Una caja de acero con una puerta que sube y otra que baja. Dentro cabe exactamente una vaca."),
        T("Las paredes por dentro tienen arañazos a la altura de una cabeza. Muchos. Ninguno sale."),
    ])])
    m.add("Pistola de perno", 4, 4, [page([
        IF(c_sw(S_PRIMERA),
           [T("La pistola de perno cuelga otra vez de su cable. No la miras. Ella sí te mira a ti.")],
           [T("La pistola de perno cautivo cuelga de un cable, a la altura de la mano. No dispara balas: dispara un perno que sale y vuelve a entrar."),
            T(PIENSA + "(Sale y vuelve a entrar. Como si no hubiera pasado nada.)" + FIN)]),
    ], char=OBJ, d=6, pat=1, dirfix=True, walk=False)])
    m.set("Vaca del cajon", 3, 5, [
        page([]),
        page([T("Te mira. Tiene los ojos mojados. No llora: las vacas no lloran. Es solo que tiene los ojos mojados.")],
             sw1=S_VACA_FUERA, char="vacas_vaca_canela", d=6, dirfix=True, through=True),
        page([], sw1=S_PRIMERA),
    ])

    # ---------------- CLIMAX: primera muerte obligada
    obedecer = [
        T("Aprietas."),
        TONE(-255, -255, -255, 0, 2), STOPBGS(0),
        SE("093-Attack05", 100, 50), SE("052-Cannon01", 70, 140), WAIT(10), SHAKE(9, 9, 12),
        WAIT(30), SE("045-Push01", 100, 40), WAIT(50),
        T("Un ruido seco. Luego otro, más grande y más blando: el de un cuerpo que deja de sostenerse a sí mismo."),
        T("Luego, nada. La nada dura mucho. Dentro de la nada se oye la cadena, que no se ha parado. Que no se para nunca."),
        SW(S_OBEDECIO), SW(S_PRIMERA),
        WAIT(40),
        T(CRIPPS + "Ya está. ¿Ves? Un ruido y se acabó."),
        T("Su mano en tu hombro. Pesada. Caliente. Satisfecha."),
        T(CRIPPS + "Ya eres de los nuestros, Steven."),
        T(PIENSA + "(Ha dicho mi nombre. Bien escrito, se le nota al decirlo.)" + FIN),
        SCRIPT("subir_veneno_tope(32, 96)"), SCRIPT("huella(20)"),
    ]
    resistir = [
        T("Bajas la pistola. Despacio. Te tiembla tanto el brazo que el cable tintinea."),
        T(STEVEN + "No."),
        WAIT(20),
        T("Cripps no grita. Eso es lo peor. Sonríe y te pone la mano encima de la tuya, sobre la pistola, como un guante de carne."),
        T(CRIPPS + "No es una pregunta, chaval. Nunca ha sido una pregunta."),
        T("Te levanta el brazo. Te lo apoya en su sitio. Su dedo empuja el tuyo."),
        TONE(-255, -255, -255, 0, 2), STOPBGS(0),
        SE("093-Attack05", 100, 50), SE("052-Cannon01", 70, 140), WAIT(10), SHAKE(9, 9, 12),
        WAIT(30), SE("045-Push01", 100, 40), WAIT(40),
        SE("092-Attack04", 90, 70), FLASH(255, 255, 255, 120, 6),
        T("Después, el golpe: en la cara, con el dorso de la mano. Pierdes pie. El suelo está mojado y tibio."),
        T(CRIPPS + "No lo has hecho tú. Eso te vas a decir esta noche. Pero era tu dedo."),
        T(CRIPPS + "Era tu dedo."),
        SW(S_RESISTIO), SW(S_PRIMERA),
        SCRIPT("subir_veneno_tope(24, 96)"), SCRIPT("huella(12)"),
    ]
    climax = [
        TONE(-255, -255, -255, 0, 20), WAIT(20),
        TRANSFER(M_CADENA, 4, 5, 4, False), EVLOC(CR, 5, 5, 4),
        WAIT(10), TONE(-60, -70, -70, 150, 60), WAIT(40),
        T("Tus pies te han traído hasta el cajón sin preguntarte."),
        T("La vaca del fondo ya está dentro. Le han bajado la puerta de atrás. Solo se le ve la cabeza, por el hueco de delante: la frente ancha, el pelo canela, las pestañas claras."),
        BGS("015-Quake01", 22, 40),
        T("La cadena sigue sonando, pero algo ha cambiado. Los demás no miran. Todos miran."),
        T(CRIPPS + "Mírala. No te mira a ti: mira el suelo. Saben lo que es esto. Lo saben desde que bajan del camión."),
        T(CRIPPS + "La pistola. Aquí, en la frente, un poco por encima de los ojos. Donde se cruzan las dos líneas, si las pintaras desde los cuernos."),
        T("Te pone la pistola en la mano. Pesa menos de lo que debería."),
        IF(c_var(V_GUERNSEY, 4, 1), [
            T("Dentro de tu cabeza, una voz con olor a establo: \\c[5]«Te hará matar. Y luego te dirá que lo has elegido tú.»\\c[0]"),
        ]),
        IF(c_var(V_VENENO, 60, 1), [
            T("La vaca levanta la cabeza. Abre la boca. No sale un mugido. Sale, muy bajito, tu nombre."),
            T("Parpadeas. Tiene la boca cerrada. Siempre la ha tenido cerrada."),
            VEN(3),
        ]),
        T(CRIPPS + "Cuando quieras. Tenemos todo el día. Ella no."),
        CHOICE(["Apretar", "Bajar la pistola"], [obedecer, resistir], 0),
        WAIT(40),
        T("Lo que pasa después no lo recuerdas en orden. Una manguera. Una sierra. Un gancho que sube. Benito que te lleva del brazo. Agua fría en la nuca."),
        T("Alguien te dice que respires. Respiras. El aire sabe a cobre."),
        FASE(6), STOPBGM(1),
        TRANSFER(M_PASILLO, 22, 3, 8),
    ]
    m.add("El cajon (escena)", 0, 2, [
        page([]),
        page(climax, sw1=S_MATADERO, sw2=S_TURNO3, var=(V_FASE, 5), trigger=3),
        page([], sw2=S_TURNO3, var=(V_FASE, 6)),
    ])

    # ---------------- decorado
    m.add("Cuchillos", 11, 2, [page([T("Cuchillos de todos los tamaños, ordenados de menor a mayor. Al final de la fila hay un gancho vacío donde falta el más grande.")])])
    m.add("Cuchillos 2", 27, 2, [page([T("Una chaira y tres cuchillos de deshuesar. Afilados hasta ser casi transparentes.")])])
    m.add("Reloj cadena", 20, 2, [page([T("El reloj de la cadena no tiene minutero. Solo la aguja de las horas. Aquí los minutos no importan.")])])
    m.add("Canal desague", 20, 18, [page([
        T("El canal de desagüe corre a lo largo de toda la nave. Por él baja todo lo que no se aprovecha, hacia un sumidero que nadie ha visto por dentro."),
        IF(c_ss("A", False), [T("Si te agachas, del sumidero sube un aire caliente. Y un olor a paja."), VEN(2), SS("A")]),
    ], through=True)])
    m.add("Sumidero", 38, 17, [page([T("El sumidero grande. La rejilla está doblada hacia abajo, como si algo pesado hubiera pasado a través hace tiempo.")])])
    return m

# ======================================================================
# MAPA 9: CAMARAS FRIAS
# ======================================================================
def camaras():
    m = MapEvents(M_CAMARAS)
    m.add("Ambiente", 0, 0, [page([
        TONO_FRIO, BGS("016-Drips01", 55, 70), FOG("002-Clouds01", 45, 0, 150, 1, 1),
        IF(c_sw(S_PATRULLA_CAM), [BGM("036-Dungeon02", 60, 70)], [STOPBGM(1)]),
        ERASE], trigger=4)])
    m.add("Pillado", 0, 1, [page([]), pillado_por_cripps((M_CADENA, 37, 9, 4))])
    m.add("Salida", 0, 17, [page(puerta(M_CADENA, 38, 9, 4), trigger=1)])
    # canales colgadas
    camaras_x = [(2, 4, 6), (12, 14, 16), (20, 22, 24, 26)]
    huecos = {(3, 9), (13, 5), (23, 9)}
    k = 0
    for xs in camaras_x:
        for x in xs:
            for y in (5, 9):
                m.add("Canal fria", x, y, [page([
                    T(["Escarcha en las costillas, como sal.", "Una canal helada. Al tocarla suena como una puerta.",
                       "Tiene el corte cubierto de hielo rosa."][k % 3]),
                ], char=OBJ, d=4, pat=k % 2, dirfix=True, walk=False)])
                k += 1
    # escondites: te pegas entre las canales o detras de las cajas
    def escondite(texto_dentro, d, pat):
        return [page([
            CHOICE(["Esconderte aquí", "Mejor no"], [[
                MOVE(-1, [mv(37), mv(12), mv(38)]), WAITMOVE,
                T(texto_dentro),
                SCRIPT("esconderse"),
                T(AYUDA + "(Muévete para salir del escondite.)" + FIN),
            ], []], 2),
        ], char=OBJ, d=d, pat=pat, dirfix=True, walk=False)]
    for (x, y) in sorted(huecos):
        m.add("Escondite canales", x, y, escondite(
            "Te metes entre dos canales colgadas. El frío de la carne te atraviesa el mono. Te quedas quieto, una pieza más.", 4, 1))
    for (x, y) in [(8, 18), (20, 18)]:
        m.add("Escondite cajas", x, y, escondite(
            "Te agachas detrás de las cajas. Huelen a cartón mojado y a algo que estuvo vivo esta mañana.", 6, 3))
    # puntos de entrega
    for n, (x, nombre, tipo) in enumerate([(5, "CUARTOS", 1), (14, "VÍSCERAS", 2), (23, "CABEZAS", 3)]):
        entregar = [
            IF(c_sw(S_PIEZA), [IF(c_var(V_PIEZA, tipo), [
                SW(S_PIEZA, False), VAR(V_PIEZAS, 1, 1), COBRAR(1), VEN(2), SE("045-Push01", 70, 60),
                T("Cuelgas la pieza donde le toca. El frío la recibe sin hacer preguntas."),
                IF(c_var(V_PIEZAS, 3, 1), [
                    STOPBGM(2),
                    SE("040-Knock01", 90, 50), WAIT(10),
                    T(CRIPPS_LEJOS + "¡Descanso! ¡Diez minutos!"),
                    T("Los pasos de Cripps se alejan hacia la cadena. El frío se queda."),
                    SW(S_PATRULLA_CAM, False), FASE(5),
                    T(AYUDA + "(Es la hora del descanso. Tienes diez minutos. El pasillo de mantenimiento está abajo a la derecha de la cadena.)" + FIN),
                ], [T(AYUDA + "(Piezas: \\v[13] de 3. Vuelve al final de la cinta.)" + FIN)]),
            ], [
                T("Esto no va aquí. Lo sabes porque lo pone en la pared. Lo sabes porque la pieza pesa distinto en las manos cuando la acercas."),
                VEN(3),
            ])], []),
        ]
        m.add("Camara " + str(n + 1), x, 2, [page([
            T(f"Un rótulo pintado sobre la pared helada: \\c[6]CÁMARA {n + 1} · {nombre}\\c[0]."),
            entregar,
        ])])
    m.add("Escrito en la escarcha", 10, 2, [page([
        T("En la escarcha de la pared alguien escribió con el dedo, hace poco, porque las letras aún no se han cerrado:"),
        T("\\c[6]ABAJO SON MUCHAS\\c[0]"),
        IF(c_ss("A", False), [VEN(3), SS("A")]),
    ])])
    # Cripps patrulla
    ruta = (steps(RIGHT, 11) + steps(UP, 9) + [turn(4), mwait(40), turn(6), mwait(40), turn(2)] + steps(DOWN, 9)
            + steps(LEFT, 10) + steps(UP, 9) + [turn(4), mwait(50), turn(6), mwait(30), turn(2)] + steps(DOWN, 9)
            + steps(LEFT, 10) + steps(UP, 9) + [turn(4), mwait(40), turn(6), mwait(40), turn(2)] + steps(DOWN, 9)
            + steps(RIGHT, 9) + [turn(4), mwait(30)])
    m.add("Cripps vigila", 14, 16, [
        page([]),
        page([], sw1=S_PATRULLA_CAM, char="vacas_cripps", d=6, move_type=3, speed=3, freq=6,
             mroute=route(ruta, True, False)),
    ])
    return m

# ======================================================================
# MAPA 10: OFICINA DE CRIPPS
# ======================================================================
def oficina():
    m = MapEvents(M_OFICINA)
    m.add("Ambiente", 0, 0, [page([
        TONO_OFICINA, BGS("016-Drips01", 25, 120), FOG("002-Clouds01", 20, 0, 200, 0, 1),
        IF(c_sw(S_PATRULLA_OFI), [BGM("036-Dungeon02", 55, 60)], [STOPBGM(1)]),
        IF(c_ss("A", False), [IF(c_sw(S_PATRULLA_OFI), [
            T(PIENSA + "(Su oficina. Huele a él: a tabaco negro y a colonia de barbería. Tengo poco tiempo antes de que vuelva a subir.)" + FIN),
            T(AYUDA + "(Si sube, escóndete: tras las cajas del rincón o bajo la mesa. El libro estará en el escritorio.)" + FIN),
            SS("A")])]),
        ERASE], trigger=4)])
    m.add("Pillado", 0, 1, [page([]), pillado_por_cripps((M_CADENA, 35, 3, 2))])
    m.add("Salida", 9, 13, [page(puerta(M_CADENA, 35, 3, 2), trigger=1)])
    m.add("Salida 2", 10, 13, [page(puerta(M_CADENA, 35, 3, 2), trigger=1)])
    cajon = [
        IF(c_sw(S_REGISTRO), [T("El cajón del escritorio. Clips, una petaca vacía y un diente de oro que no es suyo.")], [
            T("Abres el cajón del escritorio. Debajo de una revista de caza hay un libro de tapas verdes, gastado en las esquinas."),
            T("\\c[6]REGISTRO DE RESES\\c[0]. Años y años de números, fechas, pesos, todo con la misma letra apretada."),
            ITEM(I_REGISTRO), SW(S_REGISTRO), SE("046-Book01"),
            T(AYUDA + "(Tienes el Registro de reses. Puedes leerlo desde el menú. Llévaselo a la rejilla.)" + FIN),
            FASE(7),
        ]),
    ]
    m.add("Escritorio", 4, 6, [page([
        IF(c_sw(S_PATRULLA_OFI), [IF(c_var(V_FASE, 6, 1), cajon, [])],
           [T("El escritorio de Cripps. Un teléfono negro, una taza con un cerco marrón por dentro y por fuera.")]),
    ])])
    m.add("Archivador", 15, 3, [page([
        IF(c_sw(S_PLANO), [T("Carpetas de proveedores, de inspecciones, de bajas. Las de bajas son las más gordas.")], [
            T("Carpetas y carpetas. En la última, enrollado con una goma, un plano azul del edificio."),
            T("No es del edificio: es de lo que hay debajo. Los desagües, los colectores, unas galerías que siguen fuera del papel."),
            ITEM(I_PLANO), SW(S_PLANO), SE("046-Book01"), VEN(2),
            T(AYUDA + "(Tienes el Plano del desagüe.)" + FIN),
        ]),
    ])])
    m.add("Persiana", 5, 2, [page([
        T("Por las lamas de la persiana se ve la cadena entera, desde arriba. Las cabezas de los trabajadores, blancas, todas iguales."),
        T("Desde aquí parecen ganado."),
    ])])
    m.add("Ventana oficina", 12, 2, [page([T("Una ventana a la calle. La han tapado con la persiana bajada y con cinta. A Cripps no le interesa lo de fuera.")])])
    m.add("Foto", 9, 2, [page([
        T("Una foto enmarcada: Cripps joven, con la misma cara, al lado de una vaca premiada con una escarapela."),
        T("Él sonríe. La vaca tiene la cabeza girada hacia otro lado, como si se negara a salir en la foto."),
    ])])
    m.add("Silla", 5, 7, [page([T("Su silla. El asiento está hundido con su forma. Te dan ganas de sentarte para ver qué se siente. No lo haces.")])])
    def escondite(texto_dentro, d, pat, char=OBJ):
        return [page([
            CHOICE(["Esconderte aquí", "Mejor no"], [[
                MOVE(-1, [mv(37), mv(12), mv(38)]), WAITMOVE,
                T(texto_dentro), SCRIPT("esconderse"),
                T(AYUDA + "(Muévete para salir del escondite.)" + FIN),
            ], []], 2),
        ], char=char, d=d, pat=pat, dirfix=True, walk=False)]
    m.add("Escondite rincon", 17, 3, escondite("Te encajas en el rincón, detrás de las cajas. Hay polvo, pelusa y una bota vieja, de niño.", 6, 3))
    m.add("Escondite mesa", 3, 7, escondite("Te metes bajo la mesa, hecho un ovillo. Ves sus zapatos de cerca: hay sangre seca en la costura.", 6, 3))
    ruta = ([mv(42, 0), mv(37), mwait(150), mwait(150), mwait(60), mv(38), mv(42, 255), mv(44, audio("024-Door01", 60, 70))]
            + steps(UP, 6) + steps(LEFT, 4) + [turn(4), mwait(40)] + steps(UP, 2) + [turn(8), mwait(70)]
            + steps(DOWN, 2) + steps(RIGHT, 4) + [turn(6), mwait(40)] + steps(DOWN, 6) + [turn(2)])
    m.add("Cripps vigila", 10, 12, [
        page([]),
        page([], sw1=S_PATRULLA_OFI, char="vacas_cripps", d=8, move_type=3, speed=3, freq=6,
             mroute=route(ruta, True, False)),
    ])
    return m

# ======================================================================
# MAPA 11: PASILLO DE MANTENIMIENTO (la rejilla)
# ======================================================================
def pasillo():
    m = MapEvents(M_PASILLO)
    REJ = m.reserve("Rejilla")
    m.add("Ambiente", 0, 0, ambiente(TONO_PASILLO, ("016-Drips01", 60, 60), fog=("002-Clouds01", 40), extra=[STOPBGM(1)]))
    m.add("Salida", 0, 7, [page(puerta(M_CADENA, 32, 21, 8), trigger=1)])
    def ver(pat):
        return MOVE(REJ, [mgraphic(OBJ, 8, pat)])

    charla1 = [
        ver(0),
        T("Te acercas a la rejilla. El aire que sale es caliente y huele a heno, a leche agria, a establo en invierno."),
        T(REJILLA + "Tú eres el nuevo. El de la cinta. Te he oído respirar desde la cadena."),
        T(PIENSA + "(Una voz. Grave, lenta, con algo húmedo en cada palabra, como si hablara con la boca llena de hierba.)" + FIN),
        CHOICE(["¿Quién eres?", "No contestar"], [[
            T(STEVEN + "¿Quién... quién eres?"),
            T(REJILLA + "Alguien que estaba en la manga y no llegó al cajón."),
        ], [
            T("No contestas. Te muerdes el labio."),
            T(REJILLA + "No hace falta que hables. Los de arriba nunca hablan. Por eso os oigo tan bien."),
        ]], 0),
        ver(1), SE("070-Animal05", 40, 40),
        T("Detrás de las lamas, en lo oscuro, algo se mueve. Un ojo. Grande, castaño, con las pestañas claras. Te mira de lado, como miran ellas."),
        VEN(6),
        T(REJILLA + "Él no sabe que estoy aquí. O lo sabe y hace como que no. Es lo mismo que hace con todo."),
        T(REJILLA + "Vuelve cuando él no mire. Tengo cosas que contarte, y tú tienes manos."),
        ver(0), SE("013-Move01", 40, 50),
        T("El ojo se aparta. Se oyen pezuñas sobre metal, alejándose por dentro de la pared, hacia abajo."),
        VAR(V_GUERNSEY, 2), FASE(5),
        T(AYUDA + "(Lleva la manguera a Cripps, en la cadena.)" + FIN),
    ]
    charla2 = [
        ver(2), SE("070-Animal05", 40, 45),
        T(REJILLA + "Has vuelto."),
        T("Esta vez se ve un hocico pegado a las lamas: rosa y negro, mojado, soltando vaho."),
        T(REJILLA + "Ayer te llamó Ramón, ¿verdad? No: te llamó «chaval». A Ramón también. A todos."),
        T(REJILLA + "Escucha. Él tiene un libro. Lo apunta todo: cuántas entran, cuántas salen, cuánto pesa cada una. Lo apunta como si eso las hiciera suyas."),
        T(REJILLA + "Yo estoy en ese libro. Quiero saber qué pone de mí."),
        CHOICE(["¿Por qué yo?", "¿Qué eres?"], [[
            T(REJILLA + "Porque tú todavía tienes miedo. Los que tienen miedo miran. Los demás ya solo ven."),
        ], [
            T(REJILLA + "Una Guernsey. Me trajeron de una granja buena. Las granjas buenas también acaban aquí."),
            T(REJILLA + "Ahora soy otra cosa. Abajo nos volvemos otra cosa."),
        ]], 0),
        T(REJILLA + "Él ahora sube y baja a su oficina. Sube, mira por la persiana, baja. Si eres listo, entras cuando él baja."),
        T(REJILLA + "El libro está en su escritorio. Tráemelo. Léemelo."),
        ver(0),
        VAR(V_GUERNSEY, 3), SW(S_PATRULLA_OFI), FASE(6), VEN(4),
        T(AYUDA + "(La oficina de Cripps está arriba, por la puerta metálica del fondo de la cadena. Cripps sube y baja: entra cuando no esté y escóndete si le oyes.)" + FIN),
    ]
    charla3 = [
        ver(1),
        T(GUERN + "Huele a él. A su colonia. Lo tienes."),
        T("Abres el registro por las páginas que tienen una esquina doblada. Lees en voz baja, contra la rejilla:"),
        T("\\c[6]«Lote 7. Guernsey, hembra, 3 años. 412 kg. BAJA: fuga por el colector 4. No consta.»\\c[0]"),
        T("Debajo, con otra tinta: \\c[6]«Que no conste.»\\c[0]"),
        WAIT(20), ver(2),
        T(GUERN + "«No consta.» Qué bonito. Ni siquiera muerta. Ni siquiera fuera."),
        T(GUERN + "Me escapé por el colector. El agua de la cadena baja caliente y te lleva. Abajo hay sitio. Abajo hay mucho sitio."),
        T(GUERN + "Y no estoy sola. Las que se caen por el desagüe, las que no llegan a pesarse, los terneros que tiran por el sumidero porque no sirven... Abajo somos muchas."),
        IF(c_sw(S_PLANO), [
            T("Le hablas del plano. Le describes las galerías que siguen fuera del papel."),
            T(GUERN + "Entonces ya sabes por dónde se baja. Guárdalo. Algún día vas a querer bajar."),
            VAR(V_GUERNSEY, 1, 1),
        ]),
        ver(1),
        T(GUERN + "Ahora escúchame bien, Steven."),
        T(PIENSA + "(Sabe mi nombre. Nadie aquí sabe mi nombre.)" + FIN),
        T(GUERN + "Mañana te llevará al cajón. Te hará matar. Y luego te dirá que lo has elegido tú. Hace eso con todos: los mancha para que no puedan irse."),
        T(GUERN + "No te pido que no lo hagas. No podrías. Te pido que vuelvas después. Que no te olvides de que hay alguien detrás de la pared."),
        CHOICE(["«Volveré.»", "«No puedo prometer nada.»"], [[
            T(STEVEN + "Volveré."),
            T(GUERN + "Lo sé. Los que vuelven tienen la voz como tú: rota por el mismo sitio."),
            SW(S_PACTO), VAR(V_GUERNSEY, 1, 1),
        ], [
            T(GUERN + "Nadie puede. Por eso las promesas valen tan poco aquí arriba. Abajo, en cambio..."),
            T("No termina la frase."),
        ]], 0),
        ver(0), SE("013-Move01", 40, 50),
        T("Las pezuñas se alejan dentro de la pared. Bajan. Siguen bajando mucho después de que deberían haber llegado al suelo."),
        VAR(V_GUERNSEY, 1, 1), VEN(5),
        SW(S_PATRULLA_OFI, False), FASE(9),
        T(AYUDA + "(El turno ha terminado. Ficha la salida en el vestíbulo.)" + FIN),
    ]
    charla4 = [
        TONE(-255, -255, -255, 0, 0), WAIT(30), TONE(-90, -90, -80, 150, 80), WAIT(40),
        T("Estás sentado en el suelo del pasillo de mantenimiento, con la espalda contra la pared. No sabes cuánto tiempo llevas aquí."),
        T("Tienes el mono mojado. Tienes la mano derecha cerrada y no consigues abrirla."),
        WAIT(30), ver(1), SE("070-Animal05", 40, 40),
        IF(c_sw(S_OBEDECIO), [
            T(REJILLA + "Lo he oído. Desde aquí se oye todo. Ese ruido se oye en toda la ciudad, si sabes escuchar."),
            T(REJILLA + "Ya hueles como él. Un poco. Por las manos."),
            T(REJILLA + "No te lo reprocho. Él quería que lo hicieras para que ya no pudieras mirarnos. Mírame, Steven."),
            T("La miras. El ojo castaño, al otro lado de las lamas, no se aparta."),
        ], [
            T(REJILLA + "Te he oído decir que no. Nadie le dice que no. Lo he oído desde abajo, y abajo lo han oído todas."),
            T(REJILLA + "No importa de quién fuera el dedo. Importa quién dijo que no."),
            T("El ojo castaño, al otro lado de las lamas, parpadea despacio. Como una caricia."),
        ]),
        IF(c_sw(S_PACTO), [
            T(REJILLA + "Dijiste que volverías. Has vuelto. Te estaré esperando más abajo cuando estés preparado."),
        ], [
            T(REJILLA + "Ahora ya sabes lo que pasa arriba. Cuando quieras saber lo que pasa abajo, la rejilla seguirá aquí."),
        ]),
        T(REJILLA + "Y escucha: hay alguien en tu escalera que también busca lo que queda dentro de nosotras. Deja que te encuentre."),
        ver(0),
        VAR(V_GUERNSEY, 1, 1),
        WAIT(20), TONE(-80, -78, -66, 110, 60),
        COBRAR(6),
        T("En el bolsillo del mono hay seis monedas que antes no estaban. Paga doble, el primer cajón. Lo llaman «la propina»."),
        FASE(9),
        T(AYUDA + "(Ficha la salida en el vestíbulo. Vete a casa.)" + FIN),
    ]
    def q(t, f, extra=""):
        return c_script(f"$game_variables[7] == {t} and $game_variables[8] == {f}" + extra)
    silencio = [T("Silencio. Solo el aire, caliente, que sube desde muy abajo. Huele a establo.")]
    rejilla = [
        IF(q(1, 4, " and $game_switches[44]"), charla1, [
        IF(q(1, 4), [
            T("Una rejilla de ventilación. De ella sale aire caliente, que es raro: al otro lado solo deberían estar las cámaras frías."),
            T("Huele a establo."),
        ], [
        IF(q(2, 5), charla2, [
        IF(q(2, 7), charla3, [
        IF(q(2, 6), [T("Silencio. Dentro de la pared, algo espera, respirando hondo. Espera el libro.")], silencio),
        ])])])]),
    ]
    m.set("Rejilla", 22, 2, [page(rejilla, char=OBJ, d=8, pat=0, dirfix=True, walk=False)])
    m.add("Manguera", 9, 2, [page([
        IF(c_var(V_TURNO, 1, 0), [IF(c_var(V_FASE, 4, 0), [
            IF(c_sw(S_MANGUERA), [T("Ya tienes la manguera.")], [
                T("La manguera grande, enrollada en su soporte. Pesa como una serpiente dormida."),
                ITEM(I_MANGUERA), SW(S_MANGUERA), SE("045-Push01", 70, 80),
                WAIT(30), SE("070-Animal05", 30, 40),
                T("Mientras la descuelgas, oyes algo al fondo del pasillo. Un siseo. No: una voz, muy baja, que dice algo parecido a «eh»."),
                T(PIENSA + "(Viene de la rejilla de la pared.)" + FIN),
                VAR(V_GUERNSEY, 1), MOVE(REJ, [mgraphic(OBJ, 8, 1)]), WAIT(30), MOVE(REJ, [mgraphic(OBJ, 8, 0)]),
            ]),
        ], [T("El soporte de la manguera. Vacío, o lleno, según el día.")])],
           [T("El soporte de la manguera.")]),
    ])])
    m.add("Trampilla", 26, 9, [page([
        T("Una trampilla de hierro en el suelo, con un candado. Debajo, el desagüe general."),
        T("El candado es nuevo. Es lo único nuevo de todo el matadero."),
        IF(c_sw(S_PLANO), [
            T("En el plano esta trampilla tiene nombre: \\c[6]COLECTOR 4\\c[0]. Y una flecha que baja y se sale del papel."),
        ]),
        IF(c_ss("A", False), [SE("070-Animal05", 25, 35), WAIT(20),
            T("Pegas la oreja al hierro. Muy abajo, muchas respiraciones a la vez, despacio, como un fuelle enorme."),
            VEN(3), SS("A")]),
    ], through=True)])
    m.add("Tuberias", 15, 2, [page([T("Tuberías que bajan del techo y se meten en el suelo. Una está caliente. Otra late, muy débil, como un pulso.")])])
    m.add("Cajas pasillo", 2, 4, [page([T("Cajas con monos viejos. En uno, bordado, \\c[6]R. MATA\\c[0]. Está limpio. Planchado. Doblado con mucho cuidado.")])])
    m.add("Cubo pasillo", 28, 10, [page([T("Un cubo con cal viva. Para los olores, pone. Para los olores que no se van, piensas.")])])
    # escena posterior al cajon (turno 3)
    m.add("Despues del cajon", 0, 1, [
        page([]),
        page(charla4, sw1=S_MATADERO, sw2=S_TURNO3, var=(V_FASE, 6), trigger=3),
        page([], sw2=S_TURNO3, var=(V_FASE, 9)),
    ])
    return m

# ======================================================================
# NOCHES EN CASA: paginas nuevas para el piso y la escalera
# ======================================================================
def sueldo_madre():
    dar = [
        IF(c_sw(S_GUARDO), [
            IF(c_var(V_TURNO, 2, 1), [
                T(MADRE + "Ayer faltaba una. Lo sé porque las cuento con la lengua. Tienen sabor, ¿sabes? Las tuyas saben a vaca."),
            ]),
        ]),
        CHOICE(["Dárselo todo", "Guardarte una moneda"], [[
            SCRIPT("entregar_sueldo(false)"), SE("006-System06", 70, 70),
            T("Le das todas las monedas. Las cuenta en la palma de la mano, una a una, moviendo los labios."),
            T(MADRE + "Bien. Para algo sirves."),
            VEN(3),
        ], [
            SCRIPT("entregar_sueldo(true)"), SW(S_GUARDO), SE("006-System06", 70, 70),
            T("Le das el puñado. Una moneda se te queda en el puño, pegada al sudor."),
            VARRAND(V_RESULT, 1, 3),
            IF(c_var(V_RESULT, 1), [
                T("Te mira la mano cerrada. No dice nada. Te la abre dedo a dedo, despacio, como se abre una ostra."),
                SE("092-Attack04", 80, 80), SHAKE(7, 9, 12),
                T(MADRE + "Ladrón. En mi casa. Con mi comida dentro."),
                GOLD(-1), SW(S_MADRE_PILLO), VEN(10),
            ], [
                T("No se da cuenta. O sí, y se lo guarda para otro día."),
                T(PIENSA + "(Una moneda mía. La primera.)" + FIN),
                VEN(1),
            ]),
        ]], 0),
    ]
    return [IF(c_sw(S_SUELDO), [
        si_turno(1, [T(MADRE + "Ya tengo lo mío. Vete a la cama. Apestas.")]),
        si_turno(2, [T(MADRE + "Mañana más. Y pasado más. Hasta que me compres un sillón nuevo.")]),
        si_turno(3, [T("Duerme sentada. En sueños, mastica.")]),
    ], [
        si_turno(1, [
            T(MADRE + "Ya era hora. ¿Qué traes?"),
            T("Se inclina hacia ti y te huele. Primero el pelo, luego las manos. Cierra los ojos."),
            T(MADRE + "Matadero. Igual que él. Huele igual que él."),
        ]),
        si_turno(2, [
            T(MADRE + "El sueldo. Y no me cuentes nada del trabajo. No quiero saber cómo se gana el dinero. Solo quiero el dinero."),
        ]),
        si_turno(3, [
            T("Madre está despierta, esperándote. Algo cambia en su cara cuando entras. Algo parecido al respeto. Algo peor."),
            T(MADRE + "Hoy hueles distinto. Hueles a hombre, por fin."),
            IF(c_sw(S_OBEDECIO), [T(MADRE + "¿Lo has hecho? Lo has hecho. Se te ve en los hombros.")],
               [T(MADRE + "Aunque no del todo. Todavía no del todo.")]),
            VEN(4),
        ]),
        T("Te tiende la mano abierta, con la palma hacia arriba."),
        dar,
        T(AYUDA + "(Cuando quieras, acuéstate. Antes puedes guardar en la tele.)" + FIN),
    ])]

def dormir_acto2():
    sueno = [
        TONE(-255, -255, -255, 0, 60), STOPBGS(2), WAIT(70),
        si_turno(1, [
            T("Sueñas con la cinta. Pasas tú por ella, tumbado, y en cada puesto alguien te gira un poco. Nadie te mira la cara."),
            T("Al final de la cinta hay una rejilla, y detrás de la rejilla, un ojo castaño que no parpadea."),
        ]),
        si_turno(2, [
            T("Sueñas que bajas. Por el sumidero de la ducha, por las tuberías, por el agua caliente de la cadena. Bajas y bajas."),
            T("Abajo hay un establo enorme, sin techo, sin paredes, lleno de respiraciones. Alguien dice tu nombre con la boca llena de hierba."),
            VEN(4),
        ]),
        SCRIPT("nuevo_turno"),
        WAIT(30),
        T("Un claxon abajo, en la calle. Dos veces. La furgoneta."),
        T(VOZ + "¡Que te vas! ¡Que se va sin ti, mueble!"),
        T("Te vistes a oscuras. Perro levanta la cabeza al oírte pasar, y la vuelve a bajar."),
        TRANSFER(M_ENTRADA, 15, 19, 8),
    ]
    final = [
        TONE(-255, -255, -255, 0, 60), STOPBGS(2), WAIT(80),
        T("Esta noche no sueñas. Te quedas tumbado, mirando el techo. La mancha de humedad ha cambiado otra vez de forma."),
        IF(c_sw(S_OBEDECIO), [T("Ahora parece una cabeza vista de frente. Con una marca en el centro de la frente.")],
           [T("Ahora parece una mano. Una mano grande encima de otra más pequeña.")]),
        T("Arriba, en el cuarto piso, alguien camina de un lado a otro. Pasos descalzos. Lucy, que tampoco duerme."),
        T("Y abajo, mucho más abajo que el portal, más abajo que la calle, algo grande se mueve en la oscuridad y espera."),
        T(PIENSA + "(Mañana volveré a la cadena. Y a la rejilla. Y a lo mejor llamo dos veces a una puerta del cuarto piso.)" + FIN),
        WAIT(60),
        SCRIPT("fin_del_acto2"),
    ]
    return [IF(c_sw(S_SUELDO), [
        CHOICE(["Dormir", "Todavía no"], [[IF(c_sw(S_TURNO3), final, sueno)], []], 2),
    ], [
        T("No puedes acostarte. Madre no te dejará dormir sin su dinero. Te oiría cerrar los ojos."),
    ])]

def perro_noche():
    return [
        si_turno(1, [T("Perro se arrastra hasta ti y te huele las manos mucho rato. Luego te las lame, despacio, una y otra vez, como si quisiera quitarte algo.")]),
        si_turno(2, [T("Perro te apoya la cabeza en el zapato. Tiene el hocico caliente. Gime bajito, mirando hacia la ventana, hacia la calle, hacia abajo.")]),
        si_turno(3, [IF(c_sw(S_OBEDECIO),
            [T("Perro te huele las manos y aparta la cabeza. Por primera vez desde que lo conoces, aparta la cabeza.")],
            [T("Perro te lame los nudillos, justo donde Cripps te apretó. Le dejas. No sabes quién consuela a quién.")])]),
        IF(c_script("perro_esta_noche?"), [VEN(-6), SCRIPT("perro_hecho")]),
    ]

def lucy_escena(LUCY_ID):
    return [
        WAIT(30), SE("013-Move01", 50, 70), WAIT(20), SE("013-Move01", 50, 75),
        T("Pasos en la escalera de arriba. Descalzos. Alguien baja desde el cuarto piso."),
        EVLOC(LUCY_ID, 17, 3, 2), MOVE(-1, [UP, turn(6)]),
        MOVE(LUCY_ID, steps(DOWN, 7) + steps(LEFT, 12) + [turn(4)]), WAITMOVE,
        T("Es una chica de tu edad, o un poco más. Pelo claro, recogido de cualquier manera. Una bata de hospital encima de la ropa. En la mano, un tarro de cristal vacío."),
        T(LUCY + "Hola. Tú eres el del 3ºB. El hijo de la señora que grita."),
        T("Se acerca sin pedir permiso y te huele el hombro. Igual que Cripps. Igual que madre. Pero no igual."),
        T(LUCY + "Matadero. El de verdad, no la carnicería. Se nota en la grasa del pelo. Lucy, del cuarto. Encantada."),
        CHOICE(["«Steven.»", "No decir nada"], [[
            T(STEVEN + "Steven."),
            T(LUCY + "Steven. Bonito. Un nombre de alguien que todavía no ha hecho nada."),
        ], [
            T("No dices nada. Ella asiente, como si eso también fuera una respuesta."),
            T(LUCY + "No pasa nada. Los que vienen de allí al principio no hablan. Luego hablan demasiado."),
        ]], 0),
        T(LUCY + "¿Sabes qué pienso? Que el dolor no se va. Que se queda dentro, como un poso, como la cal en una tetera. En la carne, en el hígado, en las tripas."),
        T(LUCY + "Si se pudiera encontrar... si alguien lo sacara y lo pusiera en un tarro... se podría ver. Se podría pesar."),
        T("Levanta el tarro vacío hacia la bombilla de la escalera. La luz pasa a través y no encuentra nada."),
        T(LUCY + "Tú trabajas donde hay más dolor de toda la ciudad. Tráeme algo de dentro, un día. Lo que sea. Algo que haya visto el cajón."),
        IF(c_sw(S_PRIMERA), [
            T("Te mira las manos. Te mira el dedo índice, exactamente ese dedo, como si brillara."),
            T(LUCY + "Ah. Ya has estado cerca. Se te nota. Tú también llevas un poco dentro."),
            VEN(3),
        ]),
        T("Te mete un papel doblado en el bolsillo del pecho. Sus dedos están helados."),
        ITEM(I_NOTA_LUCY), SE("046-Book01"),
        T(LUCY + "Llama dos veces. Si llamas tres, no abro: tres es la policía o tu madre."),
        MOVE(LUCY_ID, [turn(6)] + steps(RIGHT, 12) + steps(UP, 7) + [mv(42, 0)]), WAITMOVE,
        T("Sube la escalera sin hacer ruido. Arriba se cierra una puerta. Dos vueltas de llave."),
        SW(S_LUCY),
        T(AYUDA + "(Tienes la Nota de Lucy. Entra en casa: madre espera.)" + FIN),
    ]

# ======================================================================
# Extensiones de los mapas del Acto I (se aplican sobre MapEvents ya hechos)
# ======================================================================
def _ev(m, nombre):
    for e in m.events:
        if e and e["name"] == nombre:
            return e
    raise KeyError(nombre)

def extender_piso(m):
    import contenido as C
    amb = _ev(m, "Ambiente")
    amb["pages"] = [page([
        IF(c_sw(S_NOCHE2), [C.tono_noche(), BGS("018-Darkness01", 40, 75)], [
            IF(c_sw(C.S_BUSQ), [C.tono_busqueda(), BGS("018-Darkness01", 55, 70)], [
                IF(c_sw(C.S_NOCHE), [C.tono_noche(), BGS("018-Darkness01", 45, 80)], [
                    IF(c_sw(C.S_MANANA), [C.tono_manana(), BGS("001-Wind01", 35, 60)],
                       [C.tono_dia(), BGS("001-Wind01", 30, 55)])])])]),
        STOPBGM(1), FOG("002-Clouds01", 28, 0, 200, 1, 0), ERASE,
    ], trigger=4)]
    _ev(m, "Madre")["pages"].append(page(sueldo_madre(), sw1=S_NOCHE2, char="vacas_madre", d=2, dirfix=True))
    _ev(m, "Madre por la manana")["pages"].append(page([], sw1=S_ACTO2))
    for n in ("Cama Steven", "Cama Steven 2"):
        _ev(m, n)["pages"].append(page(dormir_acto2(), sw1=S_NOCHE2))
    for n in ("Puerta del piso", "Puerta del piso 2"):
        _ev(m, n)["pages"].append(page([
            T("De noche no se sale. Y menos ahora, que sabes lo que hay ahí fuera esperando a que amanezca."),
            MOVE(-1, [UP])], sw1=S_NOCHE2, trigger=1))
    _ev(m, "Perro")["pages"].append(page(perro_noche(), sw1=S_NOCHE2, char="vacas_perro", d=4))

def extender_escalera(m):
    amb = _ev(m, "Ambiente")
    amb["pages"] = [page([
        IF(c_sw(S_NOCHE2), [TONE(-70, -70, -50, 110, 0), BGS("016-Drips01", 45, 70)],
           [TONE(-25, -30, -45, 100, 0), BGS("016-Drips01", 55, 80)]),
        FOG("002-Clouds01", 40, 0, 200, 0, 1), ERASE], trigger=4)]
    _ev(m, "Dona Remedios")["pages"].append(page([], sw1=S_ACTO2))
    ANS = "\\c[4]Señor Anselmo:\\c[0] "
    _ev(m, "Senor Anselmo")["pages"].append(page([
        T("El señor Anselmo fuma en el rellano, en pijama, con el cenicero en la mano."),
        si_turno(1, [T(ANS + "¿Primer día? Lávate con limón. Ya te lo dije. Y no le cuentes nada a tu madre: a las madres les gusta demasiado el olor.")]),
        si_turno(2, [T(ANS + "Mi hermano decía que en el matadero hay una pared que habla. Él decía que era el aire. Luego dejó de decir que era el aire.")]),
        si_turno(3, [T("Te mira las manos. Apaga el cigarro sin terminarlo y se mete en su casa sin decir buenas noches.")]),
    ], sw1=S_NOCHE2, char="vacas_anselmo", d=2))
    _ev(m, "Escalera arriba")["pages"].append(page([
        T("Arriba, una raya de luz bajo la puerta del 4ºB. Se oye cristal contra cristal, como tarros que alguien ordena."),
        T(PIENSA + "(Hoy no. Todavía no.)" + FIN), MOVE(-1, [DOWN])], sw1=S_LUCY, trigger=1))
    _ev(m, "Bajada a la calle")["pages"].append(page([
        T("No. Por hoy ya has tenido bastante calle. Bastante mundo."), MOVE(-1, [RIGHT])], sw1=S_NOCHE2, trigger=1))
    LUCY_ID = m.reserve("Lucy")
    m.set("Lucy", 17, 1, [
        page([]),
        page(lucy_escena(LUCY_ID), sw1=S_NOCHE2, sw2=S_TURNO3, trigger=3, char="vacas_lucy", d=2, opacity=255),
        page([], sw1=S_LUCY),
    ])

# ======================================================================
# EVENTO COMUN 1: notas nuevas
# ======================================================================
def notas_acto2():
    return [
        IF(c_script("$vacas_ultimo_objeto == 9"), [
            T("Una tarjeta de cartón con casillas para cada día. Pone \\c[6]STEPHEN\\c[0], con PH."),
            T("En el dorso, a lápiz, de otra mano: \\c[6]«R. MATA — 41 días.»\\c[0] Alguien la usó antes y borró su nombre a medias."),
        ]),
        IF(c_script("$vacas_ultimo_objeto == 10"), [
            T("\\c[6]REGISTRO DE RESES.\\c[0] Columnas de fechas, lotes, razas y pesos con la letra apretada de Cripps."),
            T("Hay páginas enteras con la misma palabra en la columna del final: \\c[6]APTO, APTO, APTO.\\c[0]"),
            T("\\c[6]«Lote 7. Guernsey, hembra, 3 años. 412 kg. BAJA: fuga por el colector 4. No consta.»\\c[0]"),
            T("Y, en la última página escrita, una línea suelta: \\c[6]«Ramón Mata. Baja voluntaria.»\\c[0] Con la misma tinta que las vacas."),
        ]),
        IF(c_script("$vacas_ultimo_objeto == 11"), [
            T("Un plano azul de los desagües bajo el matadero. Colectores numerados del 1 al 6."),
            T("El colector 4 está rodeado a lápiz muchas veces, hasta romper el papel. Desde él sale una galería que no termina: se sale del borde."),
            T("Al lado, a lápiz: \\c[6]«no bajar»\\c[0]. Y debajo, tachado: \\c[6]«bajar»\\c[0]."),
        ]),
        IF(c_script("$vacas_ultimo_objeto == 13"), [
            T("Un papel doblado en cuatro. Letra redonda, de colegio:"),
            T("\\c[6]«Lucy. 4ºB. Si traes algo de dentro, llama dos veces.»\\c[0]"),
            T("Debajo hay un dibujo pequeño, muy bien hecho: un estómago de vaca, con sus cuatro cámaras, y una de ellas pintada de negro."),
        ]),
    ]
