# Arnés temporal RGSS1 real del Acto V. No guarda ni modifica partidas.
begin
  $vacas_test_log=File.open('diseno/verificacion_rgss_acto5.txt','w')
  def verificar(ok,label)
    $vacas_test_log.puts((ok ? 'OK ' : 'FALLO ')+label)
    $vacas_test_log.flush
    raise label unless ok
  end
  nombres={'Actors'=>'actors','Classes'=>'classes','Skills'=>'skills','Items'=>'items','Weapons'=>'weapons','Armors'=>'armors','Enemies'=>'enemies','Troops'=>'troops','States'=>'states','Animations'=>'animations','Tilesets'=>'tilesets','CommonEvents'=>'common_events','System'=>'system'}
  for name in nombres.keys
    eval('$data_'+nombres[name]+' = load_data("Data/'+name+'.rxdata")')
  end
  Vacas.ajustar_sistema
  $game_system=Game_System.new
  def Graphics.update
    self.frame_count+=1
  end
  for path in Dir.glob('Data/*.rxdata')
    d=load_data(path)
    verificar(d!=nil,'carga '+path)
  end
  module Input
    class << self
      alias a5_press_original press?
      def press?(key)
        return $a5_keys.include?(key) unless $a5_keys.nil?
        return a5_press_original(key)
      end
    end
  end
  for venganza in [false,true]
    $a5_keys = venganza ? [Input::L,Input::R] : [Input::L]
    Scene_Title.new.command_new_game
    $a5_keys = nil
    verificar($game_map.map_id==22 && $game_player.x==3 && $game_player.y==11,'atajo Q llega al muelle')
    verificar($game_switches[140] && $game_switches[132] && $game_switches[venganza ? 134 : 133] && !$game_switches[venganza ? 133 : 134],'pacto del atajo')
    verificar(Vacas.tareas.size>0,'tareas')
    for mid in 22..27
      $game_map.setup(mid)
      $game_player.moveto(10,7)
      $game_switches[150]=(mid==25)
      $game_map.need_refresh=true
      ss=Spriteset_Map.new
      8.times { $game_map.update; ss.update }
      verificar(Vacas_Audio.zone!=nil,'zona audio '+mid.to_s)
      ss.dispose
      if mid==25
        ev=nil
        for e in $game_map.events.values
          ev=e if e.matanza_ruta!=nil && e.instance_variable_get(:@event).name=='Cripps caza'
        end
        verificar(ev!=nil && ev.character_name=='vacas_cripps','Cripps activo en caza')
        verificar([2,4,6,8].include?(ev.matanza_ruta),'ruta de Cripps')
        x0=ev.x; y0=ev.y
        60.times { $game_map.update }
        verificar(ev.x!=x0 || ev.y!=y0,'Cripps se mueve')
      end
      $game_switches[150]=false
    end
    i=Interpreter.new
    i.matanza_alarma(5); verificar($game_variables[57]==3,'tope alarma')
    i.matanza_inclinar(58,9); verificar($game_variables[58]==6,'tope dominio')
    i.matanza_jefe; verificar($data_enemies[21].maxhp==1070,'jefe escalado')
    i.matanza_fin_caza; verificar($game_switches[151],'fin de caza')
    $game_switches[157]=true; i.susto(12)
  end
  m=Vacas_Noria.new(3)
  m.nueva_pieza
  m.dispose
  verificar(true,'minijuego noria construido')
  for id in [12,13]
    b=RPG::Cache.picture('screamer_'+id.to_s); verificar(b.width==640,'susto '+id.to_s)
  end
  for id in 18..21
    b=RPG::Cache.battler($data_enemies[id].battler_name,$data_enemies[id].battler_hue); verificar(b.width>0,'battler '+id.to_s)
    verificar($data_troops[id].members[0].enemy_id==id,'tropa '+id.to_s)
  end
  $vacas_test_log.puts('OK FIN: Acto V verificado con RGSS real')
rescue Exception => e
  $vacas_test_log.puts('FALLO '+e.class.to_s+': '+e.message+' | '+(e.backtrace || [])[0,4].join(' | ')) if $vacas_test_log
ensure
  $vacas_test_log.close if $vacas_test_log
end
