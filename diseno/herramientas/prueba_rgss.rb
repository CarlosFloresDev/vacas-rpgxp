# Arnes temporal ejecutado como Main con RGSS104E real. Nunca guarda partidas.
begin
  $vacas_test_log = File.open('diseno/verificacion_rgss.txt', 'w')
  def verificar(ok, mensaje)
    $vacas_test_log.puts((ok ? 'OK ' : 'FALLO ') + mensaje)
    $vacas_test_log.flush
    raise mensaje unless ok
  end
  $vacas_test_log.puts('Inicio RGSS1 real')
  $data_actors = load_data('Data/Actors.rxdata')
  $data_classes = load_data('Data/Classes.rxdata')
  $data_skills = load_data('Data/Skills.rxdata')
  $data_items = load_data('Data/Items.rxdata')
  $data_weapons = load_data('Data/Weapons.rxdata')
  $data_armors = load_data('Data/Armors.rxdata')
  $data_enemies = load_data('Data/Enemies.rxdata')
  $data_troops = load_data('Data/Troops.rxdata')
  $data_states = load_data('Data/States.rxdata')
  $data_animations = load_data('Data/Animations.rxdata')
  $data_tilesets = load_data('Data/Tilesets.rxdata')
  $data_common_events = load_data('Data/CommonEvents.rxdata')
  $data_system = load_data('Data/System.rxdata')
  Vacas.ajustar_sistema
  $game_system = Game_System.new
  Scene_Title.new.command_new_game
  verificar($game_party.actors.size == 1, 'Partida nueva: solo Steven')
  a=$game_actors[1]
  verificar(a.maxhp == 360 && a.skill_learn?(61), 'Salud y recursos iniciales')
  # En modo oculto Graphics.update espera foco de Windows. El arnes prueba
  # objetos/bitmaps sin ese bloqueo; el bucle del juego no se modifica.
  def Graphics.update; Graphics.frame_reset; end
  for path in Dir.glob('Data/*.rxdata')
    data=load_data(path)
    verificar(Marshal.load(Marshal.dump(data)).class==data.class, 'Marshal RGSS: '+path)
  end
  # Todos los mapas se construyen con las clases del motor real.
  for mid in 1..11
    $game_map.setup(mid)
    ss=Spriteset_Map.new
    ss.update
    ss.dispose
    Graphics.update
  end
  verificar(true,'Mapas 1..11 y spritesets cargados')
  # Renderiza todas las cajas reales, incluidas opciones y expresiones.
  count=0
  vistos={}
  for mid in 1..11
    map=load_data(sprintf('Data/Map%03d.rxdata',mid))
    for event in map.events.values
      for page in event.pages
        i=0
        while i<page.list.size
          if page.list[i].code==101
            text=page.list[i].parameters[0]+"\n"
            i+=1
            while i<page.list.size && page.list[i].code==401
              text+=page.list[i].parameters[0]+"\n"
              i+=1
            end
            key = text[/\\P\[[^\]]+\]/] || 'sin_retrato'
            next if vistos[key]
            vistos[key]=true
            $game_temp.message_text=text
            w=Window_Message.new
            w.reset_window
            w.refresh
            w.dispose
            count+=1
            Graphics.update if count%8==0
          else
            i+=1
          end
        end
      end
    end
  end
  verificar(true,'Cajas VN renderizadas: '+count.to_s)
  $game_temp.message_text='Escoge'+"\n"+'Quedarte'+"\n"+'Salir'+"\n"
  $game_temp.choice_start=1
  $game_temp.choice_max=2
  $game_temp.choice_proc=Proc.new { |n| }
  w=Window_Message.new
  w.refresh
  verificar(w.index==0 && w.instance_variable_get(:@vn_choice_active),'Opciones nativas conservadas')
  w.dispose
  # Dos pulsaciones separadas: revelar nunca cierra ni elige una opcion.
  module Input
    class << self
      alias prueba_trigger_original trigger?
      def trigger?(key)
        return $vacas_tecla_prueba == key if $vacas_prueba_input
        return prueba_trigger_original(key)
      end
    end
  end
  $vacas_prueba_input=true
  $vacas_tecla_prueba=nil
  $game_temp.message_text='\\P[steven_neutral]\\NOMBRE[Steven]Una palabra tras otra.'+"\n"
  w=Window_Message.new
  13.times { w.update }
  verificar(w.instance_variable_get(:@vn_units).size>0,'Texto se revela progresivamente')
  $vacas_tecla_prueba=Input::C
  w.update
  verificar($game_temp.message_text!=nil,'Primera confirmacion solo revela')
  $vacas_tecla_prueba=nil
  w.update
  $vacas_tecla_prueba=Input::C
  w.update
  verificar($game_temp.message_text==nil,'Segunda confirmacion avanza')
  w.dispose
  $vacas_tecla_prueba=nil
  $game_temp.message_text='Quedarte'+"\n"+'Salir'+"\n"
  $game_temp.choice_start=0
  $game_temp.choice_max=2
  $game_temp.choice_cancel_type=2
  $vacas_opcion_elegida=nil
  $game_temp.choice_proc=Proc.new { |n| $vacas_opcion_elegida=n }
  w=Window_Message.new
  13.times { w.update }
  $vacas_tecla_prueba=Input::C
  w.update
  verificar($vacas_opcion_elegida==nil,'Revelar opciones no selecciona')
  $vacas_tecla_prueba=nil
  w.update
  $vacas_tecla_prueba=Input::B
  w.update
  verificar($vacas_opcion_elegida==1,'Cancelar respeta la opcion configurada')
  w.dispose
  $vacas_prueba_input=false
  # Acceso de Perro: el corredor debe alcanzar el salon.
  $game_map.setup(2)
  $game_player.moveto(6,16)
  verificar($game_player.passable?(6,16,2),'Hueco del salon (6,16)->(6,17) libre')
  $game_player.moveto(6,17)
  verificar($game_player.passable?(6,17,4),'Del umbral hacia Perro')
  # Sustos: una sola vez, imagen borrada, sin esperas bloqueantes.
  it=Interpreter.new
  it.susto(1)
  verificar($game_screen.pictures[98].name=='screamer_1','Susto muestra imagen')
  24.times { $game_screen.update; Graphics.update }
  verificar($game_screen.pictures[98].name=='','Susto borra imagen al terminar')
  # Recursos, estados y veneno en el motor de combate real.
  $game_temp.in_battle=true
  Vacas.preparar_mente(true)
  a.hp=100
  a.sp=0
  a.add_state(2)
  Vacas.veneno=60
  a.skill_effect(a,$data_skills[61])
  $vacas_test_log.puts('RESPIRAR '+[a.hp,a.sp,a.state?(2),Vacas.veneno,$data_skills[61].id].inspect)
  verificar(a.hp>100 && a.sp==18 && !a.state?(2) && Vacas.veneno==54,'Respirar cura, recupera SP, limpia y baja veneno')
  # Simula combates con una estrategia estable, 30 semillas por enemigo.
  for tid in 1..9
    maxturn=0
    30.times do |seed|
      srand(seed)
      a.recover_all
      Vacas.veneno=65
      $game_troop.setup(tid)
      enemy=$game_troop.enemies[0]
      turn=0
      while enemy.hp>0 && a.hp>0 && turn<80
        turn+=1
        if a.hp<200 || a.sp<8 || a.state?(2) || a.state?(3) || a.state?(4)
          a.skill_effect(a,$data_skills[61])
        else
          a.sp-=8
          enemy.skill_effect(a,$data_skills[62])
        end
        if enemy.hp>0
          if rand(2)==0
            a.attack_effect(enemy)
          else
            sid=$data_enemies[tid].actions[1].skill_id
            a.skill_effect(enemy,$data_skills[sid])
          end
        end
        a.remove_states_auto
        enemy.remove_states_auto
        Graphics.update if turn%10==0
      end
      verificar(a.hp>0 && enemy.hp==0,'Balance enemigo '+tid.to_s+' semilla '+seed.to_s+' turnos '+turn.to_s)
      maxturn=[maxturn,turn].max
    end
    $vacas_test_log.puts('MAXTURN '+tid.to_s+' '+maxturn.to_s)
  end
  $game_map.setup(8)
  $game_temp.battle_troop_id=9
  $game_temp.battle_can_escape=false
  $game_temp.battle_can_lose=true
  $game_temp.battle_event_flags={}
  $game_temp.map_bgm=nil
  $game_map.battleback_name='mente_matadero'
  $game_troop.setup(9)
  ss=Spriteset_Battle.new
  ss.update
  ss.dispose
  w=Window_PartyCommand.new
  w.dispose
  w=Window_BattleResult.new(0,0,[])
  w.dispose
  verificar(true,'Spriteset de batalla, comandos y resultado')
  # Recorre el Scene_Battle nativo, automatizando solo las decisiones.
  module Input
    def self.trigger?(key)
      return key == Input::C
    end
  end
  module Graphics
    def self.transition(*args); end
    def self.freeze; end
  end
  class Scene_Battle
    alias prueba_start_phase3 start_phase3
    def start_phase3
      prueba_start_phase3
      a=$game_actors[1]
      a.current_action.kind=1
      a.current_action.skill_id=(a.hp<200 || a.sp<8) ? 61 : 62
      a.current_action.target_index=0
      start_phase4
    end
  end
  $game_temp.battle_proc=nil
  $game_temp.battle_abort=false
  $game_temp.battle_troop_id=9
  Vacas.preparar_mente(true)
  $scene=Scene_Battle.new
  $scene.main
  verificar($game_variables[18]==0 && $scene.is_a?(Scene_Map),'Jefe: Scene_Battle nativo termina en victoria')
  if FileTest.exist?('Save1.rxdata')
    File.open('Save1.rxdata','rb') { |file| Scene_Load.allocate.read_save_data(file) }
    verificar($game_system.vacas_version_sistemas==1,'Partida anterior migrada en memoria')
    if $game_map.map_id==2
      tele=$game_map.events.values.find { |ev| ev.instance_variable_get(:@event).name=='Tele' }
      verificar(tele.x==8 && tele.y==17,'Partida anterior: tele fuera del umbral')
    end
    verificar($game_actors[1].skill_learn?(61),'Partida anterior: recursos en castellano')
  end
  verificar(true,'FIN: comprobaciones completadas')
rescue Exception => e
  if $vacas_test_log
    $vacas_test_log.puts(e.class.to_s+': '+e.message)
    $vacas_test_log.puts(e.backtrace.join("\n"))
  end
ensure
  $vacas_test_log.close if $vacas_test_log
end
$scene=nil
