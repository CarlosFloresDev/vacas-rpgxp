# Arnés temporal RGSS1 real. No guarda ni modifica partidas del usuario.
begin
  $vacas_test_log=File.open('diseno/verificaciones/verificacion_rgss_acto3.txt','w')
  def verificar(ok,label)
    $vacas_test_log.puts((ok ? 'OK ' : 'FALLO ')+label)
    $vacas_test_log.flush
    raise label unless ok
  end
  for name in ['Actors','Classes','Skills','Items','Weapons','Armors','Enemies','Troops','States','Animations','Tilesets','CommonEvents','System']
    eval('$data_'+{'Actors'=>'actors','Classes'=>'classes','Skills'=>'skills','Items'=>'items','Weapons'=>'weapons','Armors'=>'armors','Enemies'=>'enemies','Troops'=>'troops','States'=>'states','Animations'=>'animations','Tilesets'=>'tilesets','CommonEvents'=>'common_events','System'=>'system'}[name]+' = load_data("Data/'+name+'.rxdata")')
  end
  Vacas.ajustar_sistema
  $game_system=Game_System.new
  Scene_Title.new.command_new_game
  def Graphics.update
    self.frame_count+=1
    Graphics.frame_reset
    if self.frame_count%100==0 && respond_to?(:ui_original_update)
      hwnd=Win32API.new('user32','FindWindow','pp','l').call('RGSS Player',nil)
      Win32API.new('user32','ShowWindow','li','i').call(hwnd,5)
      Win32API.new('user32','SetForegroundWindow','l','i').call(hwnd)
      ui_original_update
    end
  end
  for path in Dir.glob('Data/*.rxdata')
    d=load_data(path)
    verificar(Marshal.load(Marshal.dump(d)).class==d.class,'Marshal '+path)
  end
  module Input
    class << self
      alias lucy_test_press_original press?
      def press?(key)
        return $lucy_test_keys.include?(key) unless $lucy_test_keys.nil?
        return lucy_test_press_original(key)
      end
    end
  end
  for keys,expected in [[[],1],[[Input::A],5],[[Input::CTRL],12],[[Input::CTRL,Input::A],12]]
    $lucy_test_keys=keys
    Scene_Title.new.command_new_game
    verificar($game_map.map_id==expected,'Nueva partida: teclas '+keys.inspect+' mapa '+expected.to_s)
    if keys.include?(Input::CTRL)
      verificar($game_switches[36]==keys.include?(Input::A),'Atajo conserva rama seleccionada')
    end
  end
  $lucy_test_keys=nil
  def ejecutar(mid,name,choices=[],page_index=0)
    $game_map.setup(mid)
    map=load_data(sprintf('Data/Map%03d.rxdata',mid))
    ev=map.events.values.find { |e| e.name==name }
    raise 'No existe '+name unless ev
    it=Interpreter.new
    it.setup(ev.pages[page_index].list,ev.id)
    frames=0
    while it.running? && frames<4000
      frames+=1
      it.update
      if $game_temp.message_text!=nil
        if $game_temp.choice_max>0
          choice=choices.empty? ? 0 : choices.shift
          $game_temp.choice_proc.call(choice)
        end
        $game_temp.message_text=nil
        $game_temp.choice_max=0
        $game_temp.message_proc.call if $game_temp.message_proc
        $game_temp.message_proc=nil
      end
      if $game_temp.battle_calling
        # Prueba de ramas del intérprete. El combate se verifica aparte abajo.
        $game_temp.battle_calling=false
        $game_variables[18]=0
        $game_temp.battle_proc.call(0) if $game_temp.battle_proc
        $game_temp.battle_proc=nil
      end
      if $game_temp.player_transferring
        $game_temp.player_transferring=false
        $game_temp.transition_processing=false
        $game_map.setup($game_temp.player_new_map_id)
        $game_player.moveto($game_temp.player_new_x,$game_temp.player_new_y)
      end
      $game_temp.save_calling=false
      $game_map.refresh if $game_map.need_refresh
      $game_screen.update
    end
    verificar(!it.running?,'Evento '+mid.to_s+' '+name)
  end
  # Progresión completa desde los dos resultados del cajón.
  for resistir in [false,true]
    Scene_Title.new.command_new_game
    Vacas.prueba_acto3(resistir)
    verificar($game_switches[34] && $game_switches[35]!=resistir && $game_switches[36]==resistir,'Atajo rama '+resistir.to_s)
    ejecutar(12,'Dos golpes')
    ejecutar(12,'Lucy junto a la mesa')
    verificar($game_party.item_number(14)==2,'Dos tarros iniciales')
    ejecutar(13,'Molina')
    verificar($game_party.item_number(14)==1 && $game_party.item_number(16)==1,'Hígado consume un solo tarro')
    ejecutar(14,'Persiana despierta')
    verificar($game_switches[90] && $game_system.timer_working,'Persecución activa')
    ejecutar(14,'Riñón del lote borrado')
    verificar($game_party.item_number(14)==0 && $game_party.item_number(17)==1,'Segundo tarro usado para riñón')
    $game_system.timer=0
    ejecutar(14,'Tiempo de la persiana')
    verificar($game_switches[101] && !$game_switches[90],'Paralelo solicita captura sin bloquear mensaje/transferencia')
    ejecutar(14,'Captura de la persiana')
    verificar(!$game_switches[90] && !$game_system.timer_working && $game_party.item_number(17)==1,'Captura conserva muestra y limpia temporizador')
    $game_switches[90]=true
    ejecutar(14,'Sombra de la persiana',[],1)
    verificar($game_variables[21]==2 && !$game_switches[90] && $game_party.item_number(17)==1,'Contacto y tiempo agotado permiten reintentar')
    ejecutar(14,'Cortina azul: refugio',[0])
    verificar($game_switches[91] && !$game_system.menu_disabled && !$game_player.transparent,'Refugio restaura control')
    ejecutar(15,'Elena')
    verificar($game_switches[86] && $game_party.item_number(22)==1,'Material y suero')
    ejecutar(16,'Preparación A: hígado',[1])
    verificar(!$game_switches[104] && $game_party.item_number(16)==1,'Procedimiento incorrecto no gasta muestra')
    ejecutar(16,'Comparador y cuaderno')
    verificar(!$game_switches[88],'Comparador bloquea sin control')
    ejecutar(16,'Preparación A: hígado',[0])
    ejecutar(16,'Preparación B: riñón',[0])
    ejecutar(16,'Control limpio',[0])
    ejecutar(16,'Preparación A: hígado',[0])
    verificar($game_variables[22]==3 && $game_party.item_number(25)==1,'Tres preparaciones sin duplicar')
    ejecutar(16,'Comparador y cuaderno',[resistir ? 2 : 0])
    verificar($game_switches[88] && $game_switches[100] && $game_party.item_number(28)==1,'Quiebre, susto y cuaderno')
    ejecutar(16,'Lucy: diagnóstico',[resistir ? 1 : 0])
    verificar($game_switches[95] && $game_switches[98],'Jefe y fin registrados')
    verificar($game_switches[96]==!resistir && $game_switches[97]==resistir,'Elecciones mutuamente excluyentes')
    verificar($game_variables[23]==(resistir ? 2 : 1) && $game_party.item_number(29)==1,'Continuidad para Acto IV')
    flags,vars=Marshal.load(Marshal.dump([$game_switches,$game_variables]))
    verificar(flags[98] && flags[96]!=flags[97] && vars[23]==$game_variables[23],'Decisión se serializa en formato de guardado')
  end
  # Carga de bitmaps, VN y spritesets reales para todos los mapas.
  for mid in 1..16
    $game_map.setup(mid)
    ss=Spriteset_Map.new;ss.update;ss.dispose
  end
  verificar(true,'16 mapas: spritesets reales')
  for key in ['lucy_quiebre','lucy_calma','elena_neutral']
    $game_temp.message_text='\\P['+key+']\\NOMBRE[Prueba]Una voz detrás del vidrio.'+"\n"
    w=Window_Message.new;w.reset_window;w.refresh;w.dispose
  end
  $game_temp.message_text=nil
  verificar(true,'Retratos nuevos en ventana VN real')
  for sid in [8,9]
    flag=sid==8 ? 99 : 100
    $game_switches[flag]=false
    Interpreter.new.susto(sid)
    verificar($game_screen.pictures[98].name=='screamer_'+sid.to_s,'Susto '+sid.to_s+' visible')
    24.times { $game_screen.update }
    verificar($game_screen.pictures[98].name=='','Susto limpiado')
    Interpreter.new.susto(sid)
    verificar($game_screen.pictures[98].name=='','Susto no se repite')
  end
  $game_temp.in_battle=true
  a=$game_actors[1]
  for tid in 10..13
    30.times do |seed|
      srand(seed);a.recover_all;Vacas.veneno=65;$game_troop.setup(tid)
      enemy=$game_troop.enemies[0];turn=0
      while enemy.hp>0 && a.hp>0 && turn<100
        turn+=1
        if a.hp<200 || a.sp<8 || [2,3,4].any? { |id| a.state?(id) }
          a.skill_effect(a,$data_skills[61])
        else
          a.sp-=8;enemy.skill_effect(a,$data_skills[62])
        end
        if enemy.hp>0
          if rand(2)==0
            a.attack_effect(enemy)
          else
            a.skill_effect(enemy,$data_skills[$data_enemies[tid].actions[1].skill_id])
          end
        end
        a.remove_states_auto;enemy.remove_states_auto
      end
      verificar(a.hp>0 && enemy.hp==0,'Balance '+tid.to_s+' semilla '+seed.to_s+' turnos '+turn.to_s)
    end
  end
  module Input
    def self.trigger?(key); return key==Input::C; end
  end
  module Graphics
    def self.transition(*args); end
    def self.freeze; end
  end
  class Scene_Battle
    alias lucy_test_phase3 start_phase3
    def start_phase3
      lucy_test_phase3
      a=$game_actors[1]
      a.current_action.kind=1
      a.current_action.skill_id=(a.hp<200 || a.sp<8) ? 61 : 62
      a.current_action.target_index=0
      start_phase4
    end
  end
  $game_map.setup(16)
  $game_temp.battle_troop_id=13
  $game_temp.battle_can_escape=false
  $game_temp.battle_can_lose=true
  $game_temp.battle_proc=Proc.new { |n| }
  Vacas.preparar_mente(true)
  Scene_Map.new.call_battle
  $scene.main
  verificar($game_variables[18]==0 && $scene.is_a?(Scene_Map),'Diagnóstico: Scene_Battle nativo vuelve al mapa')
  verificar(true,'FIN: Acto III verificado con RGSS104E real')
rescue Exception => e
  $vacas_test_log.puts(e.class.to_s+': '+e.message) if $vacas_test_log
  $vacas_test_log.puts(e.backtrace.join("\n")) if $vacas_test_log
ensure
  $vacas_test_log.close if $vacas_test_log
end
$scene=nil
