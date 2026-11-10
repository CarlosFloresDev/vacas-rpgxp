# Prueba de integracion en RGSS1 real. Main temporal; runner restaura Scripts.
begin
  log=File.open('diseno/verificacion_audio_motor.txt','w')
  log.sync=true
  log.puts('INICIO AUDIO')
  def audio_check(ok,label)
    $audio_log.puts((ok ? 'OK ' : 'FALLO ')+label); $audio_log.flush
    raise label unless ok
  end
  $audio_log=log
  module Graphics
    class << self
      alias audio_test_native_update ui_original_update
      def ui_original_update
        $audio_frame=($audio_frame || 0)+1
        frame_reset
        # Sin capturas: se comprueban clases/Audio nativos sin esperar al foco
        # de la ventana. El renderer de RGSS pausa cuando no tiene ventana activa.
        self.frame_count+=1
      end
      def transition(*args); end
      def freeze; end
    end
  end
  module Audio
    class << self
      def install_audio_probe(kind)
        original='vacas_original_'+kind.to_s+'_play'
        singleton=class << self; self; end
        singleton.send(:alias_method,'test_'+original,original)
        singleton.send(:define_method,original) do |*args|
          $audio_calls ||= []
          $audio_calls.push([kind,args])
          $audio_log.puts('PLAY '+kind.to_s+' '+args[0].to_s)
          send('test_'+original,*args)
        end
      end
    end
  end
  [:bgm,:bgs,:me,:se].each { |kind| Audio.install_audio_probe(kind) }
  module Input
    def self.update
      $audio_tick=($audio_tick || 0)+1
      $audio_keys=$audio_action ? $audio_action.call($audio_tick) : []
    end
    def self.trigger?(k); ($audio_keys || []).include?(k); end
    def self.repeat?(k); trigger?(k); end
    def self.press?(k); false; end
  end
  # Abrir creditos mediante la opcion real del titulo.
  $audio_tick=0
  $audio_action=proc do |tick|
    if tick==2
      $scene.instance_variable_get(:@command_window).index=3
      [Input::C]
    else; []; end
  end
  log.puts('ABRIR TITULO')
  $scene=Scene_Title.new; $scene.main
  audio_check($scene.is_a?(Scene_VacasCredits),'Acceso a Creditos desde titulo')
  credits=$scene; $audio_tick=0
  $audio_action=proc do |tick|
    case tick
    when 2; [Input::RIGHT]
    when 3
      audio_check(credits.instance_variable_get(:@page)==1,'Pagina siguiente de creditos')
      credits.instance_variable_set(:@page,credits.instance_variable_get(:@pages)-1)
      credits.draw
      [Input::LEFT]
    when 4
      audio_check(credits.instance_variable_get(:@page)==credits.instance_variable_get(:@pages)-2,'Ultimas atribuciones accesibles')
      [Input::B]
    else; []; end
  end
  credits.main
  audio_check($scene.is_a?(Scene_Title),'Volver de Creditos al titulo')
  $audio_action=nil; $audio_keys=[]
  # Inicializar juego sin atajos ni interpretes narrativos en marcha.
  $game_temp=Game_Temp.new; $game_system=Game_System.new
  $game_switches=Game_Switches.new; $game_variables=Game_Variables.new
  $game_self_switches=Game_SelfSwitches.new; $game_screen=Game_Screen.new
  $game_actors=Game_Actors.new; $game_party=Game_Party.new
  $game_troop=Game_Troop.new; $game_map=Game_Map.new; $game_player=Game_Player.new
  $game_party.setup_starting_members
  $scene=Scene_Map.new
  Vacas_Audio::TABLE.each do |key,row|
    $audio_calls=[]; Vacas_Audio.play(key)
    audio_check($audio_calls.size==1,'Reproduccion nativa '+key.to_s)
    Graphics.frame_reset; Graphics.update
  end
  Vacas_Audio::MAP_AUDIO.keys.sort.each do |id|
    $game_map.setup(id); $game_map.autoplay
    row=Vacas_Audio::MAP_AUDIO[id]
    audio_check(Audio.vacas_tracks[:bgm][0].include?(Vacas_Audio::TABLE[row[1]][1]),'BGM mapa '+id.to_s)
    audio_check(Audio.vacas_tracks[:bgs][0].include?(Vacas_Audio::TABLE[row[2]][1]),'BGS mapa '+id.to_s)
    # El ambiente de un evento antiguo debe mantener la seleccion del mapa.
    Audio.bgs_play('Audio/BGS/016-Drips01',80,60)
    audio_check(Audio.vacas_tracks[:bgs][0].include?(Vacas_Audio::TABLE[row[2]][1]),'BGS evento conserva mapa '+id.to_s)
    Graphics.frame_reset; Graphics.update
  end
  $game_map.setup(19); $game_map.autoplay
  [10,90,120,122].each do |id|
    $game_switches[id]=true; Vacas_Audio.map_audio
    audio_check(Audio.vacas_tracks[:bgm][0].include?('vacas_persecucion'),'Persecucion '+id.to_s)
    $game_switches[id]=false; Vacas_Audio.map_audio
    audio_check(Audio.vacas_tracks[:bgm][0].include?('bgm_alcantarillas'),'Restauracion tras persecucion '+id.to_s)
  end
  Vacas_Audio.play(:menu); Vacas_Audio.map_audio
  audio_check(Audio.vacas_tracks[:bgs][0].include?('bgs_agua_corriente'),'Restauracion tras pausa')
  $game_map.setup(2); $game_player.moveto(8,17)
  $audio_calls=[]
  9.times { Graphics.frame_count+=12; $game_player.increase_steps }
  audio_check($audio_calls.size==3,'Pasos cada tres movimientos')
  audio_check($audio_calls.map { |v| v[1][0] }.uniq.size==3,'Tres variantes de pasos')
  $audio_calls=[]; $game_party.gain_item(1,1)
  audio_check($audio_calls.size==1,'Recoger objeto en exploracion')
  Audio.se_play('Audio/SE/006-System06',80,100)
  audio_check($audio_calls.size==1,'Recogida evita duplicar SE antiguo del evento')
  [Vacas_Corte,Vacas_Cinta].each do |klass|
    $audio_calls=[]; klass.allocate.se('093-Attack05',80,70)
    expected=klass==Vacas_Corte ? 'se_cuchillada_1' : 'se_gancho_metal'
    audio_check($audio_calls.size==1 && $audio_calls[0][1][0].include?(expected),'SE de '+klass.to_s)
  end
  # Ejecutar la entrada real de Scene_Battle; omitir solo el bucle de turnos.
  class Scene_Battle
    alias audio_test_battle_main ui_battle_main
    def ui_battle_main
      $audio_battle_track=Audio.vacas_tracks[:bgm][0]
    end
  end
  [2,9,13,17].each do |troop|
    $game_temp.battle_troop_id=troop; Scene_Battle.new.main
    expected=troop==2 ? 'vacas_combate' : 'vacas_jefe'
    audio_check($audio_battle_track.include?(expected),'Musica de entrada tropa '+troop.to_s)
  end
  class Scene_Battle
    alias ui_battle_main audio_test_battle_main
  end
  $audio_calls=[]; $game_screen.vacas_susto(8)
  audio_check($audio_calls.size==1 && $audio_calls[0][1][0].include?('se_screamer_2'),'Screamer sin duplicar impacto')
  Vacas_Config.set(:intensidad,0); $audio_calls=[]; $game_screen.vacas_susto(9)
  audio_check($audio_calls[0][1][1]==0,'Intensidad cero silencia screamer')
  Vacas_Config.set(:intensidad,70)
  $game_switches[113]=true; $game_map.setup(17); $game_variables[52]=50
  $game_switches[115]=true; $audio_keys=[Input::X]; $audio_calls=[]
  Vacas.actualizar_linterna
  audio_check($audio_calls.size==1,'Clic al apagar linterna')
  $audio_keys=[]; $game_party.gain_item(31,1); $audio_calls=[]
  Vacas.recargar
  audio_check($audio_calls.size==1,'Clic al recargar linterna')
  [:bgm,:bgs,:se,:me].each { |k| Vacas_Config.set(k,50) }
  $audio_calls=[]; Vacas_Audio.play(:confirmar)
  audio_check($audio_calls[0][1][1]==Vacas_Audio::TABLE[:confirmar][2]/2,'Volumen global aplicado una vez')
  log.puts('OK FIN AUDIO RGSS104E'); log.close
rescue Exception => e
  if log
    log.puts('FALLO '+e.class.to_s+': '+e.message); log.puts(e.backtrace); log.close
  end
end
Audio.bgm_stop; Audio.bgs_stop; Audio.me_stop; Audio.se_stop
exit
