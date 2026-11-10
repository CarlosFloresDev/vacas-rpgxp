# Integracion en RGSS104E real; entradas simuladas, capturas GDI del cliente.
begin
  $ui_log=File.open('diseno/verificacion_vn_interfaz.txt','w')
  def ui_check(ok,label)
    $ui_log.puts((ok ? 'OK ' : 'FALLO ')+label); $ui_log.flush
    raise label unless ok
  end
  module Graphics
    class << self
      alias ui_test_native_update ui_original_update
      def ui_original_update
        $ui_frame=($ui_frame || 0)+1
        if $ui_render || $ui_frame%100==0
          frame_reset
          ui_test_native_update
        else
          self.frame_count+=1
          frame_reset
        end
      end
      def transition(*args); end
      def freeze; end
    end
  end
  module Input
    def self.update
      $ui_tick=($ui_tick || 0)+1
      $ui_keys=$ui_action ? $ui_action.call($ui_tick) : []
      $ui_keys ||= []
    end
    def self.trigger?(key); ($ui_keys || []).include?(key); end
    def self.repeat?(key); trigger?(key); end
    def self.press?(key); ($ui_held || []).include?(key); end
  end
  def ui_capture(name)
    $ui_log.puts('CAPTURA '+name); $ui_log.flush
    hwnd=Win32API.new('user32','FindWindow','pp','l').call('RGSS Player',nil)
    ui_check(hwnd!=0,'Ventana RGSS para '+name)
    Win32API.new('user32','ShowWindow','li','i').call(hwnd,5)
    Win32API.new('user32','SetForegroundWindow','l','i').call(hwnd)
    $ui_render=true
    Graphics.frame_reset
    8.times { Graphics.update }
    $ui_render=false
    dc=Win32API.new('user32','GetDC','l','l').call(hwnd)
    create=Win32API.new('gdi32','CreateCompatibleDC','l','l')
    mem=create.call(dc)
    bmp=Win32API.new('gdi32','CreateCompatibleBitmap','lii','l').call(dc,640,480)
    select=Win32API.new('gdi32','SelectObject','ll','l')
    old=select.call(mem,bmp)
    Win32API.new('gdi32','BitBlt','liii liii l'.delete(' '),'i').call(mem,0,0,640,480,dc,0,0,0x00CC0020)
    select.call(mem,old)
    header=[40,640,480,1,32,0,640*480*4,0,0,0,0].pack('LllSSLLLLLL')
    pixels="\0"*(640*480*4)
    n=Win32API.new('gdi32','GetDIBits','llii ppi'.delete(' '),'i').call(dc,bmp,0,480,pixels,header,0)
    File.open('diseno/capturas/ui_'+name+'.bmp','wb') do |f|
      f.write('BM'+[54+pixels.size,0,54].pack('LLL')+header+pixels)
    end
    Win32API.new('gdi32','DeleteObject','l','i').call(bmp)
    Win32API.new('gdi32','DeleteDC','l','i').call(mem)
    Win32API.new('user32','ReleaseDC','ll','i').call(hwnd,dc)
    ui_check(n==480,'Captura GDI '+name)
  end
  def ui_scene(scene,name,exitkey=Input::B)
    $ui_tick=0
    $ui_action=Proc.new do |n|
      ui_capture(name) if n==12
      n>=16 ? [exitkey] : []
    end
    $scene=scene; scene.main
    $ui_action=nil; $ui_keys=[]
    ui_check(true,'Escena '+name)
  end

  # Titulo real carga la BD y sale por Nueva partida sin cambiar el metodo.
  ui_scene(Scene_Title.new,'titulo',Input::C)
  ui_check($scene.is_a?(Scene_Map),'Nueva partida original')
  for keys,mid in [[[],1],[[Input::A],5],[[Input::CTRL],12],[[Input::ALT],17]]
    $ui_held=keys; Scene_Title.new.command_new_game
    ui_check($game_map.map_id==mid,'Atajo mapa '+mid.to_s)
  end
  $ui_held=[]
  $game_switches[114]=true
  ui_scene(Scene_Menu.new,'menu')
  ui_scene(Scene_VacasJournal.new(:estado),'estado')
  ui_scene(Scene_VacasJournal.new(:notas),'notas')
  ui_scene(Scene_Item.new,'objetos')
  ui_scene(Scene_Save.new,'guardar')
  original=Vacas_Config.values.clone
  $ui_tick=0
  $ui_action=Proc.new do |n|
    ui_capture('ajustes') if n==12
    n==2 ? [Input::RIGHT] : (n>=16 ? [Input::B] : [])
  end
  $scene=Scene_VacasSettings.new;$scene.main
  $ui_action=nil;$ui_keys=[]
  ui_check(Vacas_Config.get(:bgm)==[original[:bgm]+5,100].min,'Ajuste mediante flecha real de escena')
  Vacas_Config.set(:bgm,35);Vacas_Config.set(:bgs,40)
  Vacas_Config.set(:se,45);Vacas_Config.set(:me,50)
  ui_check(Vacas_Config.save,'Config persistente escrita')
  Vacas_Config.instance_variable_set(:@values,nil)
  ui_check(Vacas_Config.get(:bgm)==35 && Vacas_Config.get(:me)==50,'Config recargada separada')
  original.each { |k,v| Vacas_Config.set(k,v) }; Vacas_Config.save

  # Espia el ultimo salto al motor: cuatro canales, volumen global y silencio.
  module Audio
    class << self
      alias ui_test_bgm vacas_original_bgm_play
      alias ui_test_bgs vacas_original_bgs_play
      alias ui_test_se vacas_original_se_play
      alias ui_test_me vacas_original_me_play
      def vacas_original_bgm_play(*a); $ui_audio=[:bgm,a]; end
      def vacas_original_bgs_play(*a); $ui_audio=[:bgs,a]; end
      def vacas_original_se_play(*a); $ui_audio=[:se,a]; end
      def vacas_original_me_play(*a); $ui_audio=[:me,a]; end
    end
  end
  File.open('Audio/SE/ui_prueba.wav','wb') { |f| f.write('prueba de ruta, no reproducir') }
  [:bgm,:bgs,:se,:me].each do |kind|
    Vacas_Config.set(kind,40)
    Audio.send(kind.to_s+'_play','Audio/SE/ui_prueba',75,100)
    ui_check($ui_audio==[kind,['Audio/SE/ui_prueba',30,100]],'Volumen global '+kind.to_s)
    $ui_audio=nil
    Audio.send(kind.to_s+'_play','Audio/SE/no_existe_ui',100,100)
    ui_check($ui_audio.nil?,'Fallback silencioso '+kind.to_s)
    Vacas_Config.set(kind,original[kind])
  end
  File.delete('Audio/SE/ui_prueba.wav')
  module Audio
    class << self
      alias vacas_original_bgm_play ui_test_bgm
      alias vacas_original_bgs_play ui_test_bgs
      alias vacas_original_se_play ui_test_se
      alias vacas_original_me_play ui_test_me
    end
  end
  $game_map.setup(21);$game_player.moveto(5,10)
  ui_check(Vacas_UI.save_allowed?,'Guardado en altar')
  $game_map.setup(18)
  ui_check(!Vacas_UI.save_allowed?,'Guardado bloqueado fuera de punto')
  $game_map.setup(2);$game_player.moveto(8,16)
  ui_check(Vacas_UI.save_allowed?,'Guardado frente a tele')
  $game_player.moveto(2,2)
  ui_check(!Vacas_UI.save_allowed?,'Guardado bloqueado lejos de tele')
  $game_map.setup(17);$game_switches[15]=false
  $game_player.moveto(4,11)
  $game_screen.start_tone_change(Tone.new(-16,-6,-20,28),0)
  $scene=Scene_Map.new
  ss=Spriteset_Map.new;ss.update;ui_capture('hud');ss.dispose
  $game_temp.message_text='\\P[steven_miedo]\\NOMBRE[Steven]La luz sigue encendida.'+"\n"
  $game_temp.message_window_showing=true
  ss=Spriteset_Map.new;w=Window_Message.new
  16.times { w.update }
  $ui_keys=[Input::C];w.update;$ui_keys=[];w.update
  ss.update;ui_capture('vn');w.terminate_message;w.dispose;ss.dispose
  $game_temp.message_text=nil;$game_temp.message_window_showing=false
  selected=nil
  $game_temp.message_text="Elegir.\nSeguir\nVolver\n"
  $game_temp.choice_start=1;$game_temp.choice_max=2
  $game_temp.choice_cancel_type=2
  $game_temp.choice_proc=Proc.new { |n| selected=n }
  w=Window_Message.new
  16.times { w.update }
  $ui_keys=[Input::C];w.update
  ui_check(selected.nil?,'VN revelar no confirma decision')
  $ui_keys=[];w.update
  $ui_keys=[Input::C];w.update
  ui_check(selected==0,'VN segunda pulsacion confirma rama original')
  $ui_keys=[];w.dispose
  $game_temp.choice_max=0;$game_temp.choice_proc=nil
  $game_temp.message_text=nil;$game_temp.message_window_showing=false
  ui_check(true,'FIN VN REAL')
rescue Exception => e
  $ui_log.puts('FALLO '+e.message)
  $ui_log.puts(e.backtrace)
ensure
  $ui_log.close if $ui_log
end
$scene=nil
