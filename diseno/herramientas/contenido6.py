"""Acto VI: consecuencias y tres finales. Diálogos originales, sin citas."""
from ev import *
from ev import _wrap
from contenido_sistemas import battle,optional
from contenido5 import snd

KEYS={'Steven':'steven','Madre':'madre_envejecida','Lucy':'lucy','La Guernsey':'guernsey','Muesca':'muesca','El Rubio':'rubio'}
def say(name,text,exp=None):
    exp=exp or ('susurro' if name in ('Lucy','La Guernsey') else 'neutral')
    lines=_wrap(text);out=[]
    for i in range(0,len(lines),4):
        out.append(cmd(101,'\\P[%s_%s]\\%s\\D[1]\\NOMBRE[%s]'%(KEYS[name],exp,'L' if name=='Steven' else 'R',name)+lines[i]))
        out.extend(cmd(401,t) for t in lines[i+1:i+4])
    return ('L',out)
def inv(m,name,x,y,ls,**kw):return m.add(name,x,y,[page(ls,**kw)])
def once(m,name,x,y,ls,after=None,**kw):return m.add(name,x,y,[page(ls+[SS()],**kw),page(after or [],ss='A',**{k:v for k,v in kw.items() if k!='trigger'})])
def entry(m,flag,ls):m.add('Llegada A6',1,0,[page(ls+[SW(flag)],trigger=3),page([],sw1=flag)])
def amb(m):inv(m,'Ambiente A6',0,0,[TONE(-12,-10,-8,12,0),ERASE],trigger=4)
def save(m,x,y):inv(m,'Radio: guardar y respirar',x,y,[T('Una emisora sin locutor. Entre dos golpes de estática cabe una respiración.'),CHOICE(['Guardar','Descansar','Seguir'],[[SAVE],[SCRIPT('Vacas.preparar_mente(true)'),VEN(-8),T('Recuperas salud y aliento. La huella permanece.')],[]])])
def door(m,name,x,y,d,dx,dy,gate=None,text='Todavía no.'):
    ls=[TRANSFER(d,dx,dy,8)]
    if gate:ls=[IF(c_sw(gate),ls,[T(text)])]
    inv(m,name,x,y,ls,trigger=1)

def tunnels():
    m=MapEvents(28);amb(m)
    entry(m,177,[T('ACTO VI — REY-DIOS. Bajo el matadero, las raíces de la ciudad son tuberías. Cada casa bebe de una que huele a sangre.'),
        say('La Guernsey','Cripps ya no decide quién sale. Arriba están aprendiendo a vivir sin él.'),
        IF(c_sw(160),[say('La Guernsey','Te han guardado un asiento. Les diste un verdugo y creen que eso te convierte en rey.')],
        [IF(c_sw(161),[say('La Guernsey','Apretaste el perno tú solo. Ahora todas saben que puedes hacerlo.')],
        [say('La Guernsey','Abriste la mano. Algunas lo llaman traición. Lo que hagas con tus piernas ya será cosa tuya.')])]),
        say('Steven','Antes de sentarme en ninguna parte, voy a casa. Perro no sabe abrir la puerta.'),
        T('Objetivo: subir a la ciudad, volver al piso y regresar por la galería hasta el altar. Las radios permiten guardar.')])
    save(m,2,10)
    inv(m,'Tubería de los nombres',10,4,[IF(c_sw(178,False),[T('En la tubería suenan nombres domésticos: el de la leche, el del gas, el tuyo. Alguien pasa lista golpeando con los dientes.')]),battle(33,178),T('Ya no contestas a un nombre que no es el tuyo. Al este, la escalera vibra con pasos de pezuña.')])
    inv(m,'Nicho de los corrales',7,5,[IF(c_sw(145),[T('Las reses que soltaste duermen de pie en los nichos. Una te deja pasar sin pedirte que bajes la cabeza.')],[T('Hay candados colgados del techo. Nadie ha traído a las que dejaste en corrales. No preguntas si pudieron salir.')])])
    inv(m,'Muesca espera',15,10,[IF(c_var(51,2,1),[say('Muesca','Te vi dejar hueco para otras patas. Arriba aún queda gente que hará lo mismo por ti.'),ITEM(39),T('Muesca te da una ruta de tiza. La guardarás como recordatorio, no como permiso.')],
        [say('Muesca','Sube por donde no haya nadie. Tu nombre no abre tantas puertas como crees.')]),SS()],char='vacas_muesca',dirfix=True)
    # La entrega debe ser única incluso al volver a hablar.
    m.events[-1]['pages'].append(page([say('Muesca','Tu casa sigue en pie. Eso no significa que te esté esperando.')],ss='A',char='vacas_muesca',dirfix=True))
    inv(m,'Abrigo en el gancho',5,5,[T('Un abrigo de hombre sobre un gancho de carne. Alguien ha remendado el codo con hilo de atar canales. Las cosas útiles sobreviven a sus dueños.')])
    inv(m,'Carta húmeda',12,11,[IF(c_sw(96),[say('Lucy','Steven: Elena dice que estaré mejor lejos de los lotes. No sé si es verdad. Sé que te quedaste aquella noche. No lo he olvidado.','calma')],[IF(c_sw(97),[say('Lucy','Elena conserva una copia de lo que llevaste abajo. Que no se pierdan los nombres, aunque se pierdan las fábricas.','neutral')],[T('El agua ha borrado la firma. Queda un nombre: Lucy.')])]),SW(183),ITEM(40),T('Guardas la carta. No promete una curación ni una cita. Alguien sigue escribiendo al otro lado de la ciudad.')])
    m.events[-1]['pages'].append(page([T('La carta de Lucy sigue contigo.')],sw1=183))
    door(m,'Escalera a la ciudad',19,12,29,3,13,178,'Primero escucha la tubería del centro. Esa voz te seguirá si no le pones nombre.')
    return m

def city():
    m=MapEvents(29);amb(m)
    entry(m,179,[T('El amanecer encuentra la ciudad ocupada. Los semáforos siguen cambiando para camiones sin conductor. Hay reses en las terrazas y mandiles blancos atados como banderas.'),
        IF(c_sw(133),[T('En una pared: NADIE ES GANADO. Debajo han puesto cubos de agua para quien pueda beber de ellos.')],[IF(c_sw(134),[T('En una pared: NOS TOCA COBRAR. Una persiana abollada se mueve. Nadie se acerca a levantarla.')],[T('Han borrado las palabras del pacto. La pared está todavía húmeda.')])]),
        T('La puerta del piso está al este. El paso sur vuelve al túnel; la galería del norte se abre tras volver a casa.')])
    save(m,16,11)
    m.add('Obreros: consecuencia visible',14,10,[page([T('Dos mandiles vacíos ocupan el banco.')]),
        page([say('El Rubio','El Chato está con los críos del portal. Nos avisaste. Hoy no llevamos cuchillo.'),say('Steven','No me debéis nada.'),say('El Rubio','Pues mejor. Las deudas ya han hecho bastante ruido.')],sw1=147,char='vacas_obrero3'),
        page([T('En el banco han dejado dos botas izquierdas. Dentro de una, la chapa del Rubio. La otra no lleva nombre. Alguien pintó encima un precio y luego lo tachó.')],sw1=171)])
    m.add('Ciudadanos tras la barricada',5,10,[page([T('Desde el refugio te miran por el hueco de una caja. Nadie reconoce en tu cara una garantía.')],char='vacas_obrero1'),
        page([T('Una vecina abre un palmo la puerta: «La escalera de tu madre está libre. El perro lleva horas llamando». Te alcanza un vaso de agua.'),VEN(-4),SS()],var=(51,2),char='vacas_obrero1'),
        page([T('La vecina sigue repartiendo agua, sin preguntar a quién pertenece la calle.')],ss='A',char='vacas_obrero1')])
    inv(m,'Manada en el semáforo',12,6,[IF(c_var(58,3,1),[say('La Guernsey','Te reconocen por lo que ordenaste. Ya han empezado a repetir tus órdenes sin que estés delante.')],[say('La Guernsey','No todas te siguen. Algunas solo querían dejar de estar encerradas. Tendrás que acostumbrarte.')])],char='vacas_guernsey4',dirfix=True)
    for x,y,d in [(2,4,6),(11,4,2),(17,9,4),(7,12,8)]:inv(m,'Manada ocupa la calle',x,y,[T('No se aparta como un animal asustado. Espera a que te apartes tú.')],char='vacas_vaca',d=d,dirfix=True,walk=False)
    inv(m,'Tablón de lotes',12,3,[IF(c_sw(97),[T('Las etiquetas de Lucy están clavadas entre los avisos de desaparecidos. El número de lote ya no tapa el nombre. Hay manos humanas copiándolos.')],[T('El tablón ofrece turnos de reparto. Alguien ha puesto una foto de familia donde iba el precio por kilo.')])])
    inv(m,'Portón de la galería',4,3,[IF(c_sw(181),[TRANSFER(31,3,13,8)],[T('Los golpes del otro lado te hacen pensar en una puerta de casa. Primero vuelve al piso. No puedes fingir que lo olvidaste.')])])
    door(m,'Portal del piso',19,12,30,3,13)
    door(m,'Volver a los túneles',3,14,28,18,12)
    return m

def home():
    m=MapEvents(30);amb(m)
    entry(m,180,[T('El piso huele a sopa fría. Han cambiado los ruidos de la ciudad, pero el reloj sigue perdiendo el mismo minuto. Perro golpea el suelo con la cola antes de verte.'),
        say('Madre','Por fin. He tenido que calentarla tres veces.'),say('Steven','Hay una manada en la calle.'),say('Madre','Pues que se limpie las patas. Esto no es una pensión.'),
        T('Por un segundo te ríes. Te duele más que lo que has visto en el matadero.')])
    save(m,7,4)
    m.add('Perro al volver',5,6,[page([T('Perro te pone el hocico en la mano. No mira la sangre. Busca el sitio exacto en el que siempre le rascabas.')],char='vacas_perro',dirfix=True),page([],sw1=182,through=True)])
    scene=[say('Madre','¿Qué traes en los zapatos? Vas a dejarlo todo perdido.'),
        say('Steven','No vengo a limpiar. Vengo a llevarme a Perro.'),
        say('Madre','Hasta el perro me quieres quitar. ¿Y quién se va a quedar conmigo?','ira'),
        T('El mantel parece una sábana de la cadena. Las manchas forman una boca que pide otra cena.'),battle(34,195),
        say('Steven','Yo también tenía miedo de quedarme solo. Por eso acepté tantas cosas.'),
        IF(c_sw(96),[say('Steven','Me quedé con Lucy una noche sin pedirle que estuviera bien a cambio. Quiero poder hacer eso sin pedir permiso.')],
          [IF(c_sw(97),[say('Steven','Saqué unos papeles de un laboratorio. Me resultó más fácil que decirte que no. Hoy voy a decirlo.')],[say('Steven','He encontrado otras puertas. Ya no sé volver a ser el que las tenía todas cerradas.')])]),
        CHOICE(['Poner un límite sin castigarla','Callar; no le debes una explicación'],[
          [say('Steven','Puedes venir al portal. Hay agua y gente. Pero no vas a hacerle daño a Perro para que yo vuelva.'),say('Madre','No sé estar ahí abajo.'),say('Steven','Yo tampoco. Puedes empezar por la escalera.'),SCRIPT('Vacas.inclinar(59,1)'),SW(192)],
          [T('No discutes. Desenganchas la correa. Ella espera una respuesta hasta que comprende que tampoco va a tener esa.'),SCRIPT('Vacas.inclinar(58,1)')]]),
        T('Perro se levanta antes de que tires de la correa. Tiene una pata dormida. Lo esperas. Por una vez nadie cuenta los segundos que tarda otro en levantarse.'),
        SW(182),SW(181),VEN(-10),
        IF(c_sw(192),[T('Tu madre guarda las llaves en un pañuelo. Cuando vuelves la cabeza, ya está mirando la escalera.')],[T('Tu madre sigue viva, sentada ante la sopa. Dejas la puerta sin echar la llave.')]),
        say('Steven','Vamos, Perro. Primero abajo. Después veremos cuánto mundo cabe delante.')]
    m.add('Madre: última cena',4,5,[page(scene,char='vacas_madre'),page([IF(c_sw(192),[say('Madre','No voy a correr. Si queréis que baje, tendréis que esperarme.')],[say('Madre','La sopa se va a enfriar.')])],sw1=181,char='vacas_madre')])
    inv(m,'Plato de la cocina',14,4,[T('Dos platos y un cuenco desconchado. Ninguno necesita que lo llenen para demostrar que existe.')])
    inv(m,'Armario doméstico',17,5,[T('Medicinas caducadas, recibos doblados, una correa de repuesto. No hay ningún secreto nuevo. Eso es lo que cuesta aceptar.')])
    inv(m,'Cama al fondo',13,10,[T('La colcha tiene la marca redonda de Perro. Te gustaría echarte un momento. Temes despertar y llamar a esto un sueño.')])
    door(m,'Bajar a la ciudad',3,14,29,18,12,181,'Perro espera en el salón. Habla con tu madre antes de salir.')
    door(m,'Puerta interior cerrada',19,12,29,18,12,181,'No vas a volver a marcharte sin Perro. Tu madre está junto al sofá.')
    return m

def sluice():
    m=MapEvents(31);amb(m)
    entry(m,196,[T('La galería conduce al altar. Detrás de las paredes, los depósitos del matadero descargan. El suelo salta una vez. Perro se te pega a la rodilla.'),
        IF(c_sw(147),[say('El Rubio','¡Tres cierres! Izquierda, centro, derecha. Los pinté yo. ¡No te quedes en medio!')],[T('Una instrucción pintada sobre los cuadros: CIERRE DE EMERGENCIA — IZQUIERDA, CENTRO, DERECHA.')]),
        T('TENSIÓN: tienes 35 segundos de movimiento para cerrar las tres compuertas. Z ante cada cuadro. El tiempo se pausa mientras lees. Un error cuesta tres segundos. Si llega el golpe vuelves al nicho de entrada; puedes reintentar siempre.'),
        SCRIPT('reydios_iniciar_tension')])
    for n,x in enumerate((4,10,16),1):inv(m,'Cierre %d'%n,x,4,[SCRIPT('reydios_valvula(%d)'%n)])
    inv(m,'Orden de cierre',2,6,[T('IZQUIERDA → CENTRO → DERECHA. El agua no sabe leer. Tú todavía sí.')])
    inv(m,'Nicho de entrada',2,11,[T('El nicho aguanta los golpes de agua. La salida del altar está al este. Los tres cuadros deben quedar cerrados.')])
    door(m,'Paso al altar',19,12,32,3,13,184,'El portón vibra. Faltan cierres: izquierda, centro, derecha.')
    # Salir detiene y reinicia limpiamente; nunca permite guardar un reloj activo.
    inv(m,'Retirada a la ciudad',3,14,[SCRIPT('$game_switches[185] = false\n$game_system.menu_disabled = false\n$game_system.save_disabled = false'),TRANSFER(29,4,4,2)],trigger=1)
    # Reentrada: el interruptor local ya fue visto, pero hay que volver a arrancar.
    inv(m,'Reactivar cierres al regresar',1,1,[IF(c_sw(184,False),[IF(c_sw(185,False),[SCRIPT('reydios_iniciar_tension')])]),WAIT(8)],trigger=4)
    return m

def finale_lines(rama):
    common=[IF(c_sw(182),[T('Perro tira de la correa hacia donde entra aire. No entiende de coronas. Es el único presente que no espera una orden.')])]
    if rama==1:
        return common+[say('La Guernsey','Siéntate. Alguien tiene que decirnos qué viene después.'),say('Steven','¿Y si un día digo que no?'),say('La Guernsey','Ese día sabremos para qué queríamos un rey.'),
          IF(c_script('$game_variables[59] > $game_variables[58]'),[say('Steven','Empiezo por algo pequeño: ninguna cadena para los que no quieran seguirnos.'),T('La Guernsey no se arrodilla. Varias reses se marchan antes de la ceremonia. Las dejas pasar. El trono pierde súbditos y gana sitio para respirar.')],[T('Te sientas. La primera fila baja la cabeza y la segunda imita a la primera. Desde arriba, todas las nucas se parecen. Te sorprendes contando.')]),
          IF(c_sw(133),[T('El pacto de no convertir a nadie en ganado queda clavado junto al asiento. Cada mañana alguien lo lee en voz alta.')],[T('El pacto de venganza se convierte en ley. El matadero pierde el nombre de Cripps, pero sus puertas siguen cerrándose desde fuera.')]),
          IF(c_sw(171),[T('En el reparto de cargos quedan dos huecos sin nombre. El Rubio y el Chato no podrán decirte si esto se parece demasiado a lo de antes.')],[IF(c_sw(147),[T('El Rubio organiza agua para humanos y reses. Rechaza el cargo de capataz. Por ahora, te ríes con él.')],[T('Los obreros que se encerraron en el matadero salen al mediodía. Mantienen la distancia cuando ven tu asiento.')])]),
          IF(c_sw(192),[T('Tu madre baja al reparto con su pañuelo. Se queja de la cola y hace la cola. Perro duerme bajo el asiento, donde tu mano todavía puede alcanzarlo.')],[T('Llevas a Perro contigo. Mandas comida al piso. El mensajero vuelve siempre con la misma respuesta: «Que venga él».')]),
          T('REY DE LA MANADA. Esa noche la ciudad duerme con un ojo abierto. Tú también. Al menos ya sabes a quién pertenece ese miedo.')]
    if rama==2:
        return common+[say('La Guernsey','Aquí no hay asiento. Hay un turno que cubrir.'),say('Steven','Yo os abrí la nave.'),say('La Guernsey','Y luego decidiste que una mano bastaba para juzgar. La máquina también sabe trabajar con una sola mano.'),
          T('El altar gira. Debajo del mantel hay una cinta transportadora. Has reconocido cada pieza demasiado tarde.'),
          IF(c_script('$game_variables[59] > $game_variables[58]'),[T('No tiras de Perro contigo. Aflojas la correa y lo empujas hacia Muesca. Esa última orden no lleva castigo.'),say('Muesca','A este no lo contamos.')],[T('Buscas el perno que ya no llevas. Perro retrocede al oír el metal; Muesca lo saca por la abertura. No vuelve la cabeza hasta estar fuera.')]),
          IF(c_sw(147),[T('Desde el pasillo, el Rubio golpea el portón. No logra abrirlo, pero obliga a detener la cinta una vez. Ese minuto es suyo, no del capataz.')],[IF(c_sw(171),[T('En la etiqueta hay un número reciclado del turno del Rubio. La tinta vieja traspasa la nueva.')],[T('Al otro lado del muro se oyen obreros. Nadie sabe que el siguiente lote tiene nombre.')])]),
          IF(c_sw(96),[T('Recuerdas a Lucy pidiéndote que te quedaras, sin sujetarte. La diferencia llega entera cuando ya no puedes salir.')],[T('Piensas en las etiquetas del laboratorio. Ahora sabes cuánto espacio cabe entre una cifra y una persona.')]),
          IF(c_sw(192),[T('Tu madre recibe a Perro en el portal. Le pone un cuenco. No pregunta cuándo volverás hasta el tercer día.')],[T('Perro vuelve al piso acompañado por Muesca. Tu madre deja la puerta abierta durante toda la noche.')]),
          T('GANADO. La puerta se cierra antes del golpe. Fuera de plano, la cadena arranca. El registro del turno añade una cabeza; la ciudad no añade una tumba.')]
    return common+[say('Steven','No hay sitio para mí en ese asiento. Ni quiero aprender a hacerlo.'),say('La Guernsey','Después de todo lo que hemos cobrado, ¿te vas a marchar?'),say('Steven','Sí. Y no voy a llamar libertad a lo que os deje hacer detrás.'),
       IF(c_var(51,2,1),[say('Muesca','El desagüe del este sale a las vías. Nadie ha dicho que tengamos que seguirte. Nadie ha dicho que tengamos que pararte.')],[T('Nadie abre paso. Perro encuentra el hueco entre dos cajas y te obliga a agacharte. Sales con las manos sucias, sin despedida.')]),
       IF(c_sw(133),[T('Dejas la chapa del pacto en el suelo: nadie es ganado. Algunas reses la leen como una promesa. Otras, como una acusación.')],[T('La chapa de venganza cae al agua. La oyes chocar con el fondo antes de seguir. Lo que hiciste no se hunde con ella.')]),
       IF(c_sw(183),[T('Llevas la carta de Lucy doblada dentro del zapato. No sabes si la dirección seguirá existiendo; sí sabes que no será una deuda.')],[T('Al llegar a las vías, decides buscar noticias de Lucy y Elena. Caminar no te devuelve a nadie, pero permite preguntar.')]),
       IF(c_sw(147),[T('El Rubio y el Chato te alcanzan con una carretilla. No han venido a seguirte: van al mismo lado. Podéis turnaros empujando.')],[IF(c_sw(171),[T('En la vía cuentas dos durmientes, luego otros dos. Dejas de contar. No hay distancia que convierta esas muertes en una buena decisión.')],[T('Los obreros salen después por su cuenta. Nunca sabrás qué nombre le pusieron a tu marcha.')])]),
       IF(c_sw(192),[T('Tu madre espera en el cruce, sin maleta. Dice que Perro bebe demasiado. Le das la botella. Empiezas a andar despacio para que pueda seguir.')],[T('Dejas a tu madre agua y el camino del refugio escrito en la mesa. No te perdonas ni te condenas en su nombre. Perro te espera al otro lado de la vía.')]),
       IF(c_script('$game_variables[59] > $game_variables[58]'),[T('Cuando Perro se para, tú también. La mañana no mejora por eso. Pero por primera vez el ritmo lo decide el que va más cansado.')],[T('Te descubres tirando demasiado fuerte de la correa. Paras, la aflojas y vuelves a empezar. No basta con salir una vez.')]),
       T('HUIDA. La ciudad queda detrás. Perro huele una cuneta, estornuda y sigue. El mundo continúa sin pedirte que seas su rey.')]

def altar():
    m=MapEvents(32);amb(m)
    entry(m,186,[T('El altar huele a comedor después de una fiesta. Han arrastrado un sofá hasta la cabecera y lo han coronado con cuernos serrados. Reconoces una quemadura del salón de tu madre.'),
        say('La Guernsey','No hicimos un mundo nuevo. Trajimos las cosas que sabíamos usar.'),say('Steven','Eso es lo que me da miedo.'),
        IF(c_sw(135),[T('La chapa del pacto roza la madera. Has llegado por el camino que pactaste debajo de la ciudad.')]),
        T('La radio permite guardar. Habla con la Guernsey, junto al trono, cuando quieras afrontar el final. La decisión de Cripps ya ha elegido la rama; aquí verás lo que cuesta.')])
    save(m,3,10)
    inv(m,'Perro ante el trono',5,10,[T('Perro bosteza. Después te apoya todo su peso en el tobillo. Un cuerpo pequeño, tibio y absolutamente real.')],char='vacas_perro')
    inv(m,'Lugar para Lucy',16,6,[IF(c_sw(96),[T('Hay una taza limpia en un asiento vacío. No has reservado a Lucy como se reserva una propiedad. La taza puede quedarse vacía.')],[T('Sobre la mesa: etiquetas con nombres copiados del laboratorio. Ningún lote vuelve a ser anónimo porque cierres los ojos.')])])
    inv(m,'Pacto al pie del altar',8,7,[IF(c_sw(132),[IF(c_sw(133),[T('NADIE ES GANADO. Lo escribiste cuando todavía parecía una frase fácil.')],[T('VENGANZA. Una sola palabra ocupa más que el sofá entero.')])],[T('La madera tiene marcas de uñas antiguas.')])])
    branches=[]
    for rama in (1,2,3):
        branches.append([SCRIPT('reydios_jefe'),T(['El asiento te devuelve tu cara con una boca que solo sabe ordenar.','Una etiqueta con tu nombre abre los ojos sobre la cinta.','La salida tiene tu altura. También tiene tus dientes.'][rama-1]),
            battle(34+rama,187,True)]+finale_lines(rama)+[SCRIPT('reydios_terminar')])
    ending=[CHOICE(['Afrontar el trono','Todavía no'],[[IF(c_sw(160),branches[0],[IF(c_sw(161),branches[1],[IF(c_sw(162),branches[2],[T('Falta la decisión del Acto V. Vuelve a cargar una partida después de Cripps.')])])])],[]])]
    inv(m,'Guernsey: desenlace',10,6,ending,char='vacas_guernsey4',dirfix=True)
    door(m,'Volver a la galería',3,14,31,18,12)
    return m

MAPAS=[tunnels,city,home,sluice,altar]
SEEDS={28:(3,13),29:(3,13),30:(3,13),31:(3,13),32:(3,13)}
SWITCHES={176:'Acto VI activo',177:'Llegada túneles',178:'Censo afrontado',179:'Ciudad vista',180:'Regreso al piso',181:'Última cena terminada',182:'Perro acompaña',183:'Carta de Lucy',184:'Compuertas cerradas',185:'Tensión activa',186:'Altar visto',187:'Jefe final vencido',188:'Juego completado',189:'Final Rey visto',190:'Final Ganado visto',191:'Final Huida visto',192:'Límite sin castigo',195:'Mesa afrontada',196:'Galería vista'}
VARIABLES={65:'Cierres 0-3',66:'Tensión: frames restantes',67:'Golpes de agua',68:'Final 1-3',69:'Reservada A6'}
ITEMS=[(39,'Ruta de tiza','El paso que Muesca te dibujó. Recuerdo sin consumo.'),(40,'Carta de Lucy','Una voz al otro lado de la ciudad. Recuerdo sin consumo.')]
ENEMIGOS=[(33,'censo_bocas',0,'El Censo de las bocas',340,29,65),(34,'mesa_exige',0,'La Mesa que exige',390,31,66),(35,'rey_sin_rostro',0,'El Rey sin rostro',860,35,70),(36,'numero_cadena',0,'Tu Número en la cadena',860,35,67),(37,'puerta_muerde',0,'La Puerta que muerde',860,35,70)]
