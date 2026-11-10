# Prueba de la intro Feka en RGSS104E real (sustituye a Main solo durante la prueba).
# PENDIENTE: colgo dos veces antes de anadir ShowWindow; sin validar aun en motor.
# Uso: node diseno/herramientas/comun/probar_interfaz.mjs prueba_intro_feka.rb
begin
  $ui_log=File.open('diseno/verificaciones/verificacion_intro_feka.txt','w')
  def ui_check(ok,label)
    $ui_log.puts((ok ? 'OK ' : 'FALLO ')+label); $ui_log.flush
    raise label unless ok
  end
  module Graphics
    class << self
      alias ui_test_native_update ui_original_update
      def ui_original_update
        $ui_frame=($ui_frame || 0)+1
        if $ui_frame%10==0
          frame_reset; ui_test_native_update
        else
          self.frame_count+=1; frame_reset
        end
      end
      # Como en prueba_ui_vn.rb: con la ventana oculta la transicion nativa no avanza.
      def transition(*args); end
      def freeze; end
    end
  end
  module Input
    def self.update
      $ui_tick=($ui_tick || 0)+1
      raise 'La intro no termina' if $ui_tick>2000
      $ui_keys=$ui_action ? $ui_action.call($ui_tick) : []
      $ui_keys ||= []
    end
    def self.trigger?(key); ($ui_keys || []).include?(key); end
    def self.repeat?(key); trigger?(key); end
    def self.press?(key); false; end
  end
  module Audio
    class << self
      alias intro_test_se vacas_original_se_play
      def vacas_original_se_play(name,volume=100,pitch=100)
        ($intro_se ||= []).push([name,volume]); intro_test_se(name,volume,pitch)
      end
    end
  end
  # Con la ventana oculta (windowsHide del lanzador) Graphics.update nativo no vuelve.
  hwnd=Win32API.new('user32','FindWindow','pp','l').call('RGSS Player',nil)
  Win32API.new('user32','ShowWindow','li','i').call(hwnd,5) if hwnd!=0
  def intro_run(label,action)
    $ui_tick=0; $ui_action=action; $intro_se=[]
    Graphics.freeze
    $scene=Scene_FekaIntro.new
    $scene.main
    ui_check($scene.is_a?(Scene_Aviso),label+': cede el paso a Scene_Aviso (aviso -> titulo)')
    $ui_tick
  end
  %w(feka_logo feka_gota feka_halo feka_linea feka_presenta).each do |n|
    b=RPG::Cache.picture(n)
    ui_check(b.width>0 && b.height>0,"Grafico #{n} #{b.width}x#{b.height}")
  end
  n=intro_run('Completa',nil)
  ui_check(n==Scene_FekaIntro::T_FIN,"Intro completa dura #{n} fotogramas (#{n/40.0} s a 40 fps)")
  ui_check(n>=200 && n<=280,'Duracion entre 5 y 7 s')
  vol=Vacas_Config.get(:se)
  ui_check($intro_se.size==2,'Dos efectos: '+$intro_se.map { |s| File.basename(s[0]) }.join(', '))
  ui_check($intro_se[0][1]==80*vol/100 && $intro_se[1][1]==70*vol/100,"Volumen escalado por ajuste SE=#{vol}")
  n=intro_run('Salto con C',proc { |t| t==60 ? [Input::C] : [] })
  ui_check(n==70,"C/Intro salta: termina en el fotograma #{n}")
  n=intro_run('Salto con B',proc { |t| t==5 ? [Input::B] : [] })
  ui_check(n==15 && $intro_se.empty?,"Esc salta: termina en el fotograma #{n}, sin efectos")
  viejo=Vacas_Config.get(:intensidad); Vacas_Config.set(:intensidad,0)
  n=intro_run('Intensidad 0',nil)
  Vacas_Config.set(:intensidad,viejo)
  ui_check(n==Scene_FekaIntro::T_FIN,'Intensidad 0: sin parpadeo, misma duracion')
  ui_check(Scene_Title.method_defined?(:command_new_game),'Scene_Title conserva command_new_game (atajos Mayus/Ctrl/Alt)')
  $ui_log.puts('OK FIN INTRO FEKA'); $ui_log.close
rescue Exception => e
  File.open('diseno/verificaciones/verificacion_intro_feka.txt','a') { |f| f.puts('FALLO '+e.class.to_s+': '+e.message); f.puts(e.backtrace) }
end
