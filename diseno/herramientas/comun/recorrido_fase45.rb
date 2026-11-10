# Se evalua dentro del arnes existente del VI. No modifica datos en disco.
def jugar(mid,name,choices=[])
  $game_map.setup(mid)
  ev=$game_map.events.values.find { |e| e.instance_variable_get(:@event).name==name }
  raise 'Falta '+name unless ev
  pages=ev.instance_variable_get(:@event).pages
  page=ev.instance_variable_get(:@page)
  raise 'Sin pagina activa '+name unless page
  ejecutar(mid,name,choices,pages.index(page))
end
def transferir_prueba
  if $game_temp.player_transferring
    $game_temp.player_transferring=false
    $game_map.setup($game_temp.player_new_map_id)
    $game_player.moveto($game_temp.player_new_x,$game_temp.player_new_y)
  end
  $game_temp.transition_processing=false
end
def pasar_tarjeta(n,mid,switch)
  $scene=Scene_FinActo.new(n-1);$scene.main
  verificar($game_switches[switch] && $game_temp.player_new_map_id==mid,'Contrato '+(n-1).to_s+' > '+n.to_s)
  transferir_prueba
end
class Interpreter
  # Aislar destreza manual; los minijuegos reales se construyen mas abajo.
  def minijuego_cinta(n); $game_variables[12]=n;return true;end
  def minijuego_corte(n); $game_variables[12]=n;return true;end
  def minijuego_noria(n); $game_variables[12]=n;return true;end
end
def recorrer_hasta_seis
  $a6_keys=[];Scene_Title.new.command_new_game
  verificar($scene.is_a?(Scene_VacasCine),'Nueva partida abre cinematica')
  f=Graphics.frame_count;$scene.main
  verificar(Graphics.frame_count-f==54*Graphics.frame_rate,'Apertura completa dura 54 s')
  verificar($scene.is_a?(Scene_Map) && $game_map.map_id==1,'Apertura conserva prologo y partida')
  jugar(1,'Prologo');jugar(2,'Despertar');jugar(2,'Madre')
  jugar(2,'Comoda madre');jugar(2,'Alacena');jugar(2,'Perro')
  jugar(2,'Lavabo');jugar(2,'Madre')
  jugar(4,'Mostrador');jugar(4,'Tablon');jugar(2,'Madre');jugar(2,'Madre')
  verificar($game_switches[8] && $game_party.item_number(7)==1,'I: tareas y llave sin inyectar switches')
  jugar(2,'Cama Steven',[0]);jugar(2,'Armario',[0,0])
  verificar($game_switches[13],'I: noche recuperable da salida')
  jugar(4,'Hombre del matadero',[0,0,0]);pasar_tarjeta(2,5,22)
  for turno in 1..3
    jugar(5,'Llegada');jugar(5,'Fichadora',[0]);jugar(6,'Taquilla 13')
    verificar($game_variables[7]==turno && $game_variables[8]==3,'II: turno y mono '+turno.to_s)
    if turno==1
      jugar(8,'Puesto de la cinta');jugar(11,'Manguera');jugar(11,'Rejilla',[0]);jugar(8,'Cripps',[0])
    elsif turno==2
      jugar(8,'Puesto de corte')
      3.times do
        jugar(8,'Final de la cinta')
        jugar(9,'Camara '+$game_variables[14].to_s)
      end
      jugar(11,'Rejilla',[0]);jugar(10,'Escritorio');jugar(10,'Archivador');jugar(11,'Rejilla',[0])
    else
      jugar(8,'Cripps');jugar(7,'Puerta corral 3',[0]);jugar(8,'El cajon (escena)',[1]);jugar(11,'Despues del cajon')
    end
    verificar($game_variables[8]==9,'II: tareas completas turno '+turno.to_s)
    jugar(5,'Fichadora')
    jugar(3,'Lucy') if turno==3
    jugar(2,'Madre',[0]);jugar(2,'Perro');jugar(2,'Tele',[0]);jugar(2,'Cama Steven',[0])
  end
  verificar($game_switches[34] && $game_switches[36] && $game_party.item_number(13)==1,'II: decision y nota conservadas')
  pasar_tarjeta(3,12,81)
  jugar(12,'Dos golpes');jugar(12,'Lucy junto a la mesa');jugar(13,'Molina')
  jugar(14,'Persiana despierta');jugar(14,'Riñón del lote borrado');jugar(14,'Cortina azul: refugio',[0])
  jugar(15,'Elena');jugar(16,'Preparación A: hígado',[0]);jugar(16,'Preparación B: riñón',[0]);jugar(16,'Control limpio',[0])
  jugar(16,'Comparador y cuaderno',[0]);jugar(16,'Lucy: diagnóstico',[0])
  verificar($game_switches[98] && $game_switches[96] && $game_party.item_number(29)==1,'III: muestras, decision y llave')
  pasar_tarjeta(4,17,113)
  verificar($game_party.item_number(30)==1 && $game_party.item_number(31)==2 && $game_variables[52]==100,'IV: equipo inicial entregado')
  jugar(17,'Llegada al colector');jugar(18,'Muesca vigila',[2]);jugar(18,'Rueda entre trapos')
  jugar(19,'Junco atrapada',[0]);jugar(19,'Valvula retorno');jugar(19,'Valvula descarga');jugar(19,'Armario de bombas',[0])
  jugar(20,'La Guernsey bajo la ciudad',[0]);jugar(21,'Paso hacia el matadero nocturno',[0])
  verificar($game_switches[132] && $game_switches[133] && $game_party.item_number(33)==1,'IV: pacto y chapa')
  pasar_tarjeta(5,22,140)
  jugar(22,'Llegada al muelle');jugar(22,'Tablero de llaves');jugar(22,'Puerta de servicio')
  jugar(23,'Primera vez');jugar(23,'Sirena de corrales')
  for i in 1..5;jugar(23,'Cadena del corral '+i.to_s);end
  jugar(24,'Primera vez');jugar(24,'El Rubio',[0]);jugar(24,'Cuadro de la noria',[0]);jugar(24,'Puerta del rail')
  jugar(25,'Primera vez');$game_player.moveto(3,5);jugar(25,'Empieza la caza')
  # Refugio y salida reales; no resolver la persecucion asignando 151 a mano.
  jugar(25,'Canal vaciada',[0]);$game_system.timer=0;jugar(25,'Reloj de caza');jugar(25,'Puerta de la escalera')
  jugar(26,'Primera vez');$game_player.moveto(10,8);jugar(26,'Umbral de la oficina')
  jugar(26,'Cripps en su mesa',[0]);jugar(26,'Escalera de incendios')
  jugar(27,'Primera vez');jugar(27,'La Guernsey en el patio');jugar(27,'Cancela abierta',[0])
  verificar($game_switches[163] && $game_switches[160] && $game_switches[176] && $game_map.map_id==28,'V > VI: cancela fisica y rama Rey')
  verificar($game_temp.vacas_tarjeta==6,'Puerta fisica solicita tarjeta VI')
  Scene_VacasCine.new(Vacas_Cine.tarjeta(6)).main;$game_temp.vacas_tarjeta=nil
end

# Cada atajo se comprueba por la entrada publica del titulo.
for keys,mid in [[[Input::A],5],[[Input::CTRL],12],[[Input::ALT],17],[[Input::L],22],[[Input::L,Input::R],22]]
  $a6_keys=keys;Scene_Title.new.command_new_game
  verificar($scene.is_a?(Scene_Map) && $game_map.map_id==mid && !$game_temp.vacas_tarjeta,'Atajo sin cinematica '+keys.inspect)
end
$a6_keys=[]
# Audio y bitmaps de la tabla completa de zonas, incluidos los 32 mapas.
Scene_Title.new.command_new_game
for mid in 1..32
  row=Vacas_Audio::MAP_AUDIO[mid]
  verificar(row && row[1..2].all? { |key| Vacas_Audio::TABLE[key] },'BGM/BGS zone '+mid.to_s)
end
verificar(Vacas_Audio::CREDITS_LINES[0,30].join(' ').include?('Ander'),'Equipo Feka en creditos del titulo')

# Mantener una confirmacion de entrada no debe omitir la escena.
class Scene_VacasCine
  alias fase45_test_update update
  def update
    $cine_menu_ticks=($cine_menu_ticks || 0)+1 if $cine_menu
    if $cine_prueba
      $cine_ticks=($cine_ticks || 0)+1
      $a6_keys=($cine_ticks<=60 || $cine_ticks>=65) ? [Input::C] : []
    end
    fase45_test_update
  end
end
$cine_prueba=true;$cine_ticks=0
movie=Scene_VacasCine.new(Vacas_Cine::APERTURA);movie.main
verificar(movie.omitida && $cine_ticks==64+Graphics.frame_rate,'Salto exige liberar y mantener 1 s')
$cine_prueba=false;$a6_keys=[]
module Input
  class << self
    alias cine_test_trigger trigger?
    alias cine_test_repeat repeat?
    def trigger?(key)
      if $cine_menu
        return [2,6,8,10].include?($cine_menu_ticks) if key==Input::B
        return [4,14].include?($cine_menu_ticks) if key==Input::C
        return false
      end
      return cine_test_trigger(key)
    end
    def repeat?(key)
      return key==Input::DOWN && $cine_menu_ticks==12 if $cine_menu
      return cine_test_repeat(key)
    end
  end
end
$cine_menu=true;$cine_menu_ticks=0
movie=Scene_VacasCine.new(Vacas_Cine::APERTURA);movie.main
verificar(movie.omitida && $cine_menu_ticks==14,'Menu: continuar, cancelar y saltar con teclas')
$cine_menu=false
verificar(!RPG::Cache.picture('cine_piso').disposed?,'Cache de capturas sigue disponible')
