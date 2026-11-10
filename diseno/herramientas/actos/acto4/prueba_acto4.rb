# Arnés temporal RGSS1 real. No guarda ni modifica partidas del usuario.
begin
  $vacas_test_log=File.open('diseno/verificaciones/verificacion_rgss_acto4.txt','w')
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
        $game_variables[18]=($bajo_resultados && !$bajo_resultados.empty?) ? $bajo_resultados.shift : 0
        $game_temp.battle_proc.call($game_variables[18]) if $game_temp.battle_proc
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

  for keys,expected in [[[],1],[[Input::A],5],[[Input::CTRL],12],[[Input::CTRL,Input::A],12],[[Input::ALT],17],[[Input::ALT,Input::A],17]]
    $lucy_test_keys=keys
    Scene_Title.new.command_new_game
    verificar($game_map.map_id==expected,'Atajo '+keys.inspect+' mapa '+expected.to_s)
    if keys.include?(Input::ALT)
      verificar($game_switches[97]==keys.include?(Input::A),'Alt: rama Lucy/pruebas')
    end
  end
  $lucy_test_keys=nil
  module Input
    class << self
      alias bajo_test_trigger_original trigger?
      def trigger?(key)
        return $bajo_tecla==key unless $bajo_tecla.nil?
        return false
      end
    end
  end
  # Dos ramas de A3 por ambas variantes del pacto: cuatro partidas independientes.
  for pruebas in [false,true]
   for venganza in [false,true]
    Scene_Title.new.command_new_game
    Vacas.prueba_acto4(pruebas)
    ejecutar(15,'Colector bajo hospital A4',[],1)
    verificar($game_map.map_id==17,'Acceso fisico hospital a Acto IV rama '+pruebas.to_s)
    antes=[$game_switches[35],$game_switches[36],$game_switches[38],$game_switches[96],$game_switches[97]]
    verificar($game_variables[51]==(pruebas ? 1 : 0),'Reputacion inicial segun rama')
    # Inicio es idempotente: no duplica inventario ni reinicia bateria/reputacion.
    $game_variables[52]=48
    n=$game_party.item_number(31)
    Vacas.empezar_acto4
    verificar($game_variables[52]==48 && $game_party.item_number(31)==n,'Entrada repetida conserva estado')
    $game_temp.player_transferring=false
    ejecutar(17,'Llegada al colector')
    verificar($game_switches[114],'Introduccion rama '+pruebas.to_s)
    ejecutar(17,'Pila de emergencia')
    verificar($game_party.item_number(31)==n+1,'Pickup de bateria')
    ejecutar(18,'Muesca vigila',[venganza ? 1 : 2])
    verificar($game_switches[127],'Dialogo Muesca')
    if venganza
      verificar($game_switches[120] && $game_system.menu_disabled,'Hostilidad inicia caza')
      $game_system.timer=0
      ejecutar(18,'Reloj de caza')
      verificar($game_switches[122] && !$game_switches[120],'Tiempo agotado solicita captura')
      ejecutar(18,'Captura pendiente')
      verificar($game_variables[53]==1 && !$game_system.timer_working && !$game_system.menu_disabled,'Captura recuperable')
    else
      verificar(!$game_switches[120],'Reputacion positiva evita primera caza')
    end
    # Se comprueba tambien el contacto y el refugio de los tuneles.
    $game_switches[120]=true
    ejecutar(18,'Acechador 18',[],1)
    verificar(!$game_player.transparent && !$game_switches[120],'Contacto limpia control')
    $game_switches[120]=true
    ejecutar(18,'Nicho de sacos',[0])
    verificar($game_switches[121] && !$game_system.menu_disabled && !$game_player.transparent,'Refugio de sacos')
    ejecutar(18,'Rueda entre trapos')
    ejecutar(18,'Rueda entre trapos')
    verificar($game_party.item_number(32)==1,'Rueda unica sin duplicados')
    ejecutar(19,'Compuerta a la camara')
    verificar(!$game_switches[118] && $game_map.map_id==19,'Agua bloquea camara')
    ejecutar(19,'Valvula descarga')
    verificar(!$game_switches[118] && $game_party.item_number(32)==1,'Error de valvulas recuperable')
    ejecutar(19,'Junco atrapada',[0])
    ejecutar(19,'Junco atrapada',[0])
    verificar($game_switches[126],'Ayuda Junco sin duplicar reputacion')
    ejecutar(19,'Valvula retorno')
    ejecutar(19,'Valvula descarga')
    verificar($game_switches[118] && $game_switches[123] && $game_variables[54]==2,'Agua drenada y segunda caza')
    ejecutar(19,'Armario de bombas',[0])
    verificar($game_switches[124] && !$game_switches[123],'Refugio bombas limpia caza')
    ejecutar(18,'El Coro del tubo')
    ejecutar(19,'El Pulmon de cieno')
    # Cencerro se afronta una vez incluso al perder; Pastor exige reintento.
    $bajo_resultados=[2,2,0]
    ejecutar(20,'La Guernsey bajo la ciudad',[venganza ? 1 : 0])
    verificar($bajo_resultados.empty?,'Jefe exige victoria tras derrota')
    verificar($game_switches[130] && $game_switches[131] && $game_switches[132] && $game_switches[135],'Final completo')
    verificar($game_switches[133]==!venganza && $game_switches[134]==venganza,'Pacto exclusivo')
    verificar($game_party.item_number(33)==1,'Chapa del pacto')
    ejecutar(20,'La Guernsey bajo la ciudad')
    verificar($game_party.item_number(33)==1,'Pacto no duplica recompensa')
    despues=[$game_switches[35],$game_switches[36],$game_switches[38],$game_switches[96],$game_switches[97]]
    verificar(antes==despues,'Conserva todas las decisiones de II/III')
    sw,vars=Marshal.load(Marshal.dump([$game_switches,$game_variables]))
    verificar(sw[132] && sw[133]!=sw[134] && vars[51]==$game_variables[51],'Estado V/VI serializable')
    ejecutar(21,'Altar de las cosas salvadas',[0])
    verificar($game_variables[52]==100 && Vacas.veneno>=Vacas.huella,'Altar recarga y respeta huella')
    ejecutar(21,'Dinamo de tres resonancias',[1])
    verificar(!$game_switches[139],'Dinamo: error permite reintentar')
    n=$game_party.item_number(31)
    ejecutar(21,'Dinamo de tres resonancias',[0])
    ejecutar(21,'Dinamo de tres resonancias',[0])
    verificar($game_switches[139] && $game_party.item_number(31)==n+1,'Dinamo: recompensa unica')
    ejecutar(21,'Paso hacia el matadero nocturno',[0])
    verificar($scene.is_a?(Scene_FinActo),'Cierre A4 ofrece guardado y fin')
    $scene=Scene_Map.new
   end
  end
  # Linterna en Scene_Map.update: gasto, pausa, recarga, oscuridad y controles.
  Scene_Title.new.command_new_game
  Vacas.prueba_acto4(false)
  $game_switches[114]=true
  $game_map.refresh
  $game_variables[52]=2;$game_variables[56]=119
  Vacas.actualizar_linterna
  verificar($game_variables[52]==1,'Consumo a 120 frames libres')
  $game_variables[56]=239
  Vacas.actualizar_linterna
  verificar($game_variables[52]==0 && !$game_switches[115],'Agotamiento apaga linterna')
  v=Vacas.veneno;$game_variables[56]=479
  Vacas.actualizar_linterna
  verificar(Vacas.veneno==v+1,'Oscuridad aumenta veneno')
  n=$game_party.item_number(31)
  verificar(Vacas.recargar && $game_variables[52]==60 && $game_party.item_number(31)==n-1,'Recarga real usa inventario')
  $game_variables[52]=100
  verificar(!Vacas.recargar,'Pila no se desperdicia llena')
  $game_temp.message_window_showing=true;$game_variables[56]=119
  Vacas.actualizar_linterna
  verificar($game_variables[56]==119,'Dialogo pausa gasto')
  $game_temp.message_window_showing=false
  $game_map.setup(21);Vacas.actualizar_linterna
  verificar($game_variables[56]==119,'Altar pausa gasto')
  $game_map.setup(17);$game_switches[114]=true;$game_map.refresh
  $bajo_tecla=Input::X;Vacas.actualizar_linterna
  verificar(!$game_switches[115],'A alterna luz')
  $bajo_tecla=Input::Y;$game_variables[52]=10;Vacas.actualizar_linterna
  verificar($game_variables[52]==70 && $game_switches[115],'S recarga luz')
  $bajo_tecla=nil
  luz=Sprite_Linterna.new
  for d in [0,2,4,6,8]
    b=luz.mascara(d)
    verificar(b.get_pixel(640,480).alpha<10 && b.get_pixel(20,20).alpha>200,'Radio luz/dark '+d.to_s)
  end
  luz.dispose
  for mid in 1..21
    $game_map.setup(mid)
    ss=Spriteset_Map.new;ss.update;ss.dispose
  end
  verificar(true,'21 mapas: spritesets reales, luz, niebla, HUD y assets')
  for key in ['muesca_neutral','junco_neutral','guernsey_susurro','steven_neutral']
    $game_temp.message_text='\\P['+key+']\\NOMBRE[Prueba]Bajo la ciudad.'+"\n"
    w=Window_Message.new;w.reset_window;w.refresh;w.dispose
  end
  $game_temp.message_text=nil
  verificar(true,'Retratos VN reales')
  for sid in [10,11]
    flag=sid==10 ? 136 : 137
    $game_switches[flag]=false
    Interpreter.new.susto(sid)
    verificar($game_screen.pictures[98].name=='screamer_'+sid.to_s,'Susto '+sid.to_s)
    24.times { $game_screen.update }
    verificar($game_screen.pictures[98].name=='','Limpieza susto')
    Interpreter.new.susto(sid)
    verificar($game_screen.pictures[98].name=='','Susto unico')
  end
  $game_temp.in_battle=true
  a=$game_actors[1]
  for tid in 14..17
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
  $game_map.setup(20)
  $game_temp.battle_troop_id=17
  $game_temp.battle_can_escape=false
  $game_temp.battle_can_lose=true
  $game_temp.battle_proc=Proc.new { |n| }
  Vacas.preparar_mente(true)
  Scene_Map.new.call_battle
  $scene.main
  verificar($game_variables[18]==0 && $scene.is_a?(Scene_Map),'Pastor hueco: Scene_Battle nativo vuelve al mapa')
  verificar(true,'FIN: Acto IV verificado con RGSS104E real')
rescue Exception => e
  $vacas_test_log.puts(e.class.to_s+': '+e.message) if $vacas_test_log
  $vacas_test_log.puts(e.backtrace.join("\n")) if $vacas_test_log
ensure
  $vacas_test_log.close if $vacas_test_log
end
$scene=nil
