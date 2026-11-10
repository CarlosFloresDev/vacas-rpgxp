# Arnés temporal RGSS104E. No conserva guardados ni finales de prueba.
begin
  $vacas_test_log=File.open('diseno/verificacion_rgss_fase45.txt','w')
  def verificar(ok,label)
    $vacas_test_log.puts((ok ? 'OK ' : 'FALLO ')+label)
    $vacas_test_log.flush
    raise label unless ok
  end
  names={'Actors'=>'actors','Classes'=>'classes','Skills'=>'skills','Items'=>'items','Weapons'=>'weapons','Armors'=>'armors','Enemies'=>'enemies','Troops'=>'troops','States'=>'states','Animations'=>'animations','Tilesets'=>'tilesets','CommonEvents'=>'common_events','System'=>'system'}
  names.each { |name,key| eval('$data_'+key+' = load_data("Data/'+name+'.rxdata")') }
  Vacas.ajustar_sistema
  $game_system=Game_System.new
  def Graphics.update
    self.frame_count+=1
    Graphics.frame_reset
  end
  def Graphics.transition(*args); end
  def Graphics.freeze; end
  module Input
    def self.press?(key); return ($a6_keys || []).include?(key); end
    def self.trigger?(key)
      return true if $a6_confirm && key==Input::C
      return true if $a6_back && key==Input::B
      return false
    end
  end
  # Muestrea inicio y final del scroll sin dibujar miles de frames sin
  # renderer: el watchdog RGSS interrumpe bucles CPU de más de diez segundos.
  class Scene_CreditosJuego
    alias a6_test_credit_update update
    def update
      a6_test_credit_update
      if $a6_fast_credits && @offset > -300
        @offset = @lines.size*26+41
      end
    end
  end
  def ejecutar(mid,name,choices=[],page_index=0)
    $game_map.setup(mid)
    map=load_data(sprintf('Data/Map%03d.rxdata',mid))
    ev=map.events.values.find { |e| e.name==name }
    raise 'Falta '+name unless ev
    it=Interpreter.new
    it.setup(ev.pages[page_index].list,ev.id)
    frames=0
    while it.running? && frames<4000
      frames+=1;it.update
      if $game_temp.message_text!=nil
        if $game_temp.choice_max>0
          $game_temp.choice_proc.call(choices.empty? ? 0 : choices.shift)
        end
        $game_temp.message_text=nil;$game_temp.choice_max=0
        $game_temp.message_proc.call if $game_temp.message_proc
        $game_temp.message_proc=nil
      end
      if $game_temp.battle_calling
        $game_temp.battle_calling=false
        $game_variables[18]=($a6_results && !$a6_results.empty?) ? $a6_results.shift : 0
        $game_temp.battle_proc.call($game_variables[18]) if $game_temp.battle_proc
        $game_temp.battle_proc=nil
      end
      if $game_temp.player_transferring
        $game_temp.player_transferring=false;$game_temp.transition_processing=false
        $game_map.setup($game_temp.player_new_map_id)
        $game_player.moveto($game_temp.player_new_x,$game_temp.player_new_y)
      end
      $game_temp.save_calling=false
      $game_map.refresh if $game_map.need_refresh
      $game_screen.update
      # Las rutas forzadas de los escondites necesitan avanzar personajes.
      $game_player.update
      $game_map.events.each_value { |event| event.update }
    end
    verificar(!it.running?,'Intérprete '+mid.to_s+'/'+name)
  end
  eval(File.open('diseno/herramientas/recorrido_fase45.rb','rb') { |f| f.read })
  Dir.glob('Data/*.rxdata').each do |path|
    d=load_data(path)
    verificar(Marshal.load(Marshal.dump(d)).class==d.class,'Marshal '+path)
  end
  for cruel in [false,true]
    for rama in 1..3
      $a6_keys=[Input::CTRL,Input::R]
      $a6_keys.push(Input::SHIFT) if cruel
      Scene_Title.new.command_new_game
      verificar($scene.is_a?(Scene_PruebaActo6),'Ctrl+W abre selector')
      if rama==1 && !cruel
        recorrer_hasta_seis
      else
        Vacas.prueba_acto6(rama,cruel)
      end
      $game_temp.vacas_tarjeta=nil
      $a6_keys=[]
      verificar($game_map.map_id==28 && Vacas.rama6==rama,'Inicio A6 rama '+rama.to_s)
      verificar($game_switches[cruel ? 171 : 147] && $game_switches[cruel ? 97 : 96],'Matices de prueba')
      ejecutar(28,'Llegada A6')
      ejecutar(28,'Carta húmeda')
      ejecutar(28,'Muesca espera')
      n=$game_party.item_number(39)
      ejecutar(28,'Muesca espera',[],1)
      verificar($game_party.item_number(39)==n,'Ruta única')
      ejecutar(28,'Tubería de los nombres')
      ejecutar(28,'Escalera a la ciudad')
      verificar($game_map.map_id==29,'Transfer túneles-ciudad')
      ejecutar(29,'Llegada A6')
      ejecutar(29,'Portón de la galería')
      verificar($game_map.map_id==29,'No se omite a madre y Perro')
      ejecutar(29,'Portal del piso')
      verificar($game_map.map_id==30,'Entrada al piso')
      ejecutar(30,'Llegada A6')
      ejecutar(30,'Madre: última cena',[cruel ? 1 : 0])
      verificar($game_switches[181] && $game_switches[182],'Madre resuelta y Perro acompaña')
      verificar($game_switches[192]==!cruel,'Elección emocional')
      ejecutar(30,'Bajar a la ciudad')
      ejecutar(29,'Portón de la galería')
      verificar($game_map.map_id==31,'Transfer ciudad-galería')
      ejecutar(31,'Llegada A6')
      verificar($game_switches[185] && $game_variables[66]==1400,'Comienza tensión 35s')
      i=Interpreter.new;i.reydios_valvula(2)
      verificar($game_variables[65]==0 && $game_variables[66]==1280,'Error de orden cuesta 3s')
      # No usar el update completo aquí: probar la cuenta con dependencias
      # de Scene_Map construidas, y ocultar el autorun ya recorrido.
      $game_map.refresh
      $game_variables[66]=1
      scene=Scene_Map.new
      ss=Spriteset_Map.new
      scene.instance_variable_set(:@spriteset,ss)
      scene.instance_variable_set(:@message_window,Window_Message.new)
      $scene=scene
      scene.update
      verificar($game_variables[67]>0 && $game_variables[66]==1400 && $game_player.x==3,'Golpe de agua recuperable')
      scene.instance_variable_get(:@message_window).dispose;ss.dispose
      i.reydios_valvula(1);i.reydios_valvula(2);i.reydios_valvula(3)
      verificar($game_switches[184] && !$game_switches[185] && !$game_system.menu_disabled,'Cierres terminan tensión')
      ejecutar(31,'Paso al altar')
      verificar($game_map.map_id==32,'Transfer al altar')
      ejecutar(32,'Llegada A6')
      $a6_results=[2,0]
      ejecutar(32,'Guernsey: desenlace')
      verificar($a6_results.empty? && $game_switches[187],'Jefe exige victoria tras derrota')
      verificar($game_switches[188] && $game_switches[188+rama] && $game_variables[68]==rama,'Final correcto completado')
      verificar(Vacas.finales_vistos.include?(rama),'Final persistente')
      verificar($scene.is_a?(Scene_FinalVacas),'Escena FIN')
      $a6_confirm=true
      $scene.main
      $a6_confirm=false
      verificar($scene.is_a?(Scene_CreditosJuego),'FIN enlaza créditos')
      # Recorre la secuencia completa una vez; las demás prueban Esc.
      if rama==3 && cruel
        $a6_keys=[Input::C]
        $a6_fast_credits=true
      else
        $a6_back=true
      end
      $scene.main
      $a6_keys=[];$a6_back=false;$a6_fast_credits=false
      verificar($scene.is_a?(Scene_Title),'Créditos vuelven al título')
    end
  end
  verificar(Vacas.finales_vistos==[1,2,3],'Tres finales vistos sin duplicados')
  verificar(Scene_CreditosJuego::TEAM.any? { |line| line.include?('Ander') },'Créditos Feka')
  verificar(Vacas_Audio::CREDITS_LINES.size>1200,'Créditos CC íntegros')
  # Spritesets y audio reales para todos los mapas nuevos.
  for mid in 28..32
    $game_map.setup(mid);$game_player.moveto(3,13)
    ss=Spriteset_Map.new;ss.update;ss.dispose
    row=Vacas_Audio::MAP_AUDIO[mid]
    verificar(row[1..2].all? { |k| Vacas_Audio::TABLE[k]!=nil },'Claves audio '+mid.to_s)
    verificar(FileTest.exist?('Graphics/Battlebacks/ui_'+row[0].to_s+'.png'),'Battleback '+mid.to_s)
    $game_map.autoplay
  end
  # VN: se construyen ventanas reales con todas las expresiones usadas.
  for key in ['steven_neutral','steven_miedo','madre_neutral','madre_ira','lucy_calma','lucy_neutral','lucy_susurro','guernsey_susurro','muesca_neutral','rubio_neutral']
    $game_temp.message_text='\\P['+key+']\\NOMBRE[Prueba]La carne recuerda.'+"\n"
    w=Window_Message.new;w.reset_window;w.refresh;w.dispose
  end
  $game_temp.message_text=nil
  verificar(true,'Ventanas VN nativas')
  # Balance reproducible con las mismas fórmulas y estados del combate real.
  $game_temp.in_battle=true
  a=$game_actors[1]
  for tid in 33..37
    20.times do |seed|
      srand(seed);a.recover_all;Vacas.veneno=50;$game_troop.setup(tid)
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
      verificar(a.hp>0 && enemy.hp==0,'Balance '+tid.to_s+'/'+seed.to_s+' turnos '+turn.to_s)
    end
  end
  # Arranque y salida del Scene_Battle nativo por variante. La victoria se
  # fuerza tras 24 frames: el balance por turnos se comprobó arriba; así el
  # renderer sin foco no bloquea ni activa el watchdog del motor.
  $a6_confirm=true
  class Scene_Battle
    alias a6_test_update update
    def update
      @a6_ticks = (@a6_ticks || 0)+1
      if @a6_ticks == 24
        $game_troop.enemies.each { |enemy| enemy.hp=0 }
        battle_end(0)
        return
      end
      a6_test_update
    end
    alias a6_test_phase3 start_phase3
    def start_phase3
      a6_test_phase3
      a=$game_actors[1]
      a.current_action.kind=1
      a.current_action.skill_id=(a.hp<200 || a.sp<8) ? 61 : 62
      a.current_action.target_index=0
      start_phase4
    end
  end
  for tid in 35..37
    $game_temp.in_battle=false
    $game_map.setup(32)
    $game_temp.battle_troop_id=tid
    $game_temp.battle_can_escape=false;$game_temp.battle_can_lose=true
    $game_temp.battle_proc=Proc.new { |n| }
    Vacas.preparar_mente(true)
    Scene_Map.new.call_battle
    $scene.main
    verificar($game_variables[18]==0 && $scene.is_a?(Scene_Map),'Entrada/salida jefe nativo '+tid.to_s+' (victoria forzada)')
  end
  $a6_confirm=false
  eval(File.open('diseno/herramientas/balance_fase45.rb','rb') { |f| f.read })
  $vacas_test_log.puts('OK FIN: fases 4 y 5 verificadas con RGSS real')
rescue Exception => e
  $vacas_test_log.puts('FALLO '+e.class.to_s+': '+e.message+' | '+(e.backtrace || [])[0,8].join(' | ')) if $vacas_test_log
ensure
  $vacas_test_log.close if $vacas_test_log
end
$scene=nil
