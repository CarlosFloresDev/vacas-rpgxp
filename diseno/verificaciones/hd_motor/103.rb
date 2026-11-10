# Acto VI y cierre. RGSS1 / Ruby 1.8. Texto original.
module Vacas
  FINALES_A6 = ['Rey de la manada', 'Ganado', 'Huida']
  def self.rama6
    return 1 if $game_switches[160]
    return 2 if $game_switches[161]
    return 3 if $game_switches[162]
    return 0
  end
  def self.empezar_acto6
    return unless $game_switches[163] && rama6 > 0
    $game_switches[176] = true
    for id in [26,29,30,31,120,122,142,150,185]
      $game_switches[id] = false
    end
    detener_caza
    $game_system.timer_working = false
    $game_system.menu_disabled = false
    $game_system.save_disabled = false
    $game_player.transparent = false
    $game_temp.player_new_map_id = 28
    $game_temp.player_new_x = 3
    $game_temp.player_new_y = 13
    $game_temp.player_new_direction = 8
    $game_temp.player_transferring = true
    $game_temp.transition_processing = false
  end
  def self.prueba_acto6(rama, cruel = false)
    prueba_acto5(cruel)
    for id in [145,147,151,156,159,163]
      $game_switches[id] = true
    end
    for id in 160..162
      $game_switches[id] = (id == 159 + rama)
    end
    $game_switches[96] = !cruel
    $game_switches[97] = cruel
    $game_switches[147] = !cruel
    $game_switches[171] = cruel
    $game_switches[145] = !cruel
    $game_variables[58] = cruel ? 5 : 1
    $game_variables[59] = cruel ? 0 : 4
    empezar_acto6
    $game_temp.player_transferring = false
    $game_map.setup(28)
    $game_player.moveto(3,13)
    $game_player.turn_up
    $game_map.autoplay
    $game_map.update
  end
  def self.finales_vistos
    return [] unless FileTest.exist?('Vacas_finales.dat')
    # Formato de texto acotado; nunca deserializa contenido externo.
    data = File.open('Vacas_finales.dat','rb') { |f| f.read(32) }
    return data.scan(/[123]/).collect { |n| n.to_i }.uniq.sort
  rescue
    return []
  end
  def self.registrar_final(rama)
    return unless (1..3).include?(rama)
    $game_switches[188] = true
    $game_switches[188 + rama] = true
    $game_variables[68] = rama
    begin
      seen = (finales_vistos + [rama]).uniq.sort
      File.open('Vacas_finales.tmp','wb') { |f| f.write(seen.join(',')) }
      File.delete('Vacas_finales.dat') if FileTest.exist?('Vacas_finales.dat')
      File.rename('Vacas_finales.tmp','Vacas_finales.dat')
    rescue
      # El final sigue disponible aunque el directorio sea de solo lectura.
    end
  end
  class << self
    alias reydios_tareas_antes tareas
    def tareas
      return reydios_tareas_antes unless $game_switches[176]
      s = $game_switches
      return [['La historia ha terminado.',true]] if s[188]
      return [['Altar: escuchar a la manada y afrontar el trono.',false]] if s[184]
      return [['Galeria: cerrar izquierda, centro y derecha.',false]] if s[181]
      return [['Ciudad: volver a casa. Madre y Perro siguen arriba.',false]] if s[179]
      return [['Tuneles: escuchar la tuberia y subir a la ciudad.',false]]
    end
  end
end

module Vacas_Audio
  MAP_AUDIO[28] = [:alcantarillas,:alcantarillas_bgm,:ambiente_hueco_alcantarilla_camara,:concreto]
  MAP_AUDIO[29] = [:matadero,:alterna_calle_de_noche_suspense,:lluvia_exterior,:concreto]
  MAP_AUDIO[30] = [:piso,:tema_tranquilo_seguro_tv,:reloj_tictac_piso,:madera]
  MAP_AUDIO[31] = [:alcantarillas,:alcantarillas_bgm,:cadenas_y_transportador,:metal]
  MAP_AUDIO[32] = [:manada,:alterna_camaras_drone,:ambiente_hueco_alcantarilla_camara,:concreto]
  class << self
    alias reydios_chasing_antes chasing?
    def chasing?
      return true if $game_switches[185]
      return reydios_chasing_antes
    end
  end
end

class Scene_Title
  alias reydios_nueva_antes command_new_game
  def command_new_game
    salto = Input.press?(Input::CTRL) && Input.press?(Input::R)
    cruel = Input.press?(Input::SHIFT)
    reydios_nueva_antes
    $scene = Scene_PruebaActo6.new(cruel) if salto
  end
  alias reydios_title_update_antes update
  def update
    unless @reydios_badge
      seen = Vacas.finales_vistos
      labels = seen.collect { |i| Vacas::FINALES_A6[i-1] }
      Vacas_UI.text(@logo.bitmap,42,177,570,'Finales: '+seen.size.to_s+'/3',18,Vacas_UI::MINT)
      Vacas_UI.text(@logo.bitmap,42,202,570,labels.join(' / '),15)
      @reydios_badge = true
    end
    reydios_title_update_antes
  end
end

class Scene_PruebaActo6
  def initialize(cruel = false); @cruel = cruel; end
  def main
    @background = Vacas_UI.background('titulo')
    @window = Window_VacasCommand.new(100,170,440,
      ['VI: Rey de la manada','VI: Ganado','VI: Huida'])
    Vacas_UI.loop_scene(self)
    @window.dispose
    @background.dispose
  end
  def update
    @background.update
    @window.update
    if Input.trigger?(Input::B)
      $scene = Scene_Title.new
    elsif Input.trigger?(Input::C)
      Vacas.prueba_acto6(@window.index+1,@cruel)
      $scene = Scene_Map.new
    end
  end
end

class Interpreter
  def reydios_iniciar_tension
    return true if $game_switches[184]
    $game_switches[185] = true
    $game_variables[65] = 0
    $game_variables[66] = 40 * 35
    $game_system.menu_disabled = true
    $game_system.save_disabled = true
    return true
  end
  def reydios_valvula(n)
    return true unless $game_switches[185]
    if $game_variables[65] == n-1
      $game_variables[65] = n
      Vacas_Audio.play(:cadena_gancho)
      if n == 3
        $game_switches[184] = true
        $game_switches[185] = false
        $game_system.menu_disabled = false
        $game_system.save_disabled = false
        $game_map.need_refresh = true
      end
    else
      $game_variables[66] = [$game_variables[66]-120,40].max
      Vacas_Audio.play(:cadena_gancho)
    end
    return true
  end
  def reydios_jefe
    id = 34 + Vacas.rama6
    # La piedad facilita resistir; el dominio da más cuerpo a la visión.
    hp = 780 + $game_variables[58]*35 - $game_variables[59]*25
    $data_enemies[id].maxhp = [[hp,650].max,990].min
    return true
  end
  def reydios_terminar
    Vacas.registrar_final(Vacas.rama6)
    $scene = Scene_FinalVacas.new(Vacas.rama6)
    return true
  end
end

class Scene_Map
  alias reydios_map_update_antes update
  def update
    reydios_map_update_antes
    return unless $scene == self && $game_switches[185] && $game_map.map_id == 31
    return if $game_system.map_interpreter.running? || $game_temp.message_window_showing
    $game_variables[66] -= 1
    if $game_variables[66] <= 0
      $game_variables[67] += 1
      Vacas.veneno = [96,Vacas.veneno+4].min
      $game_variables[65] = 0
      $game_variables[66] = 40*35
      $game_player.moveto(3,12)
      $game_screen.start_flash(Color.new(180,40,20,90),12)
      Vacas_Audio.play(:cadena_gancho)
    end
  end
end

class Sprite_TensionA6 < Sprite
  def initialize
    super()
    self.bitmap = Bitmap.new(600,38)
    self.x = 20; self.y = 102; self.z = 2800
  end
  def update
    self.visible = $game_switches[185] && $game_map.map_id == 31
    return unless self.visible
    bitmap.clear
    bitmap.fill_rect(0,0,600,38,Color.new(8,10,12,220))
    seconds = ($game_variables[66]+39)/40
    Vacas_UI.text(bitmap,8,2,582,'COMPUERTAS '+$game_variables[65].to_s+'/3  |  '+seconds.to_s+' s  |  izquierda > centro > derecha',17)
  end
  def dispose
    bitmap.dispose
    super
  end
end

class Spriteset_Map
  alias reydios_ss_update_antes update
  alias reydios_ss_dispose_antes dispose
  def update
    reydios_ss_update_antes
    mid = $game_map.map_id
    if (28..32).include?(mid)
      if @reydios_mid != mid
        @reydios_luz.dispose if @reydios_luz
        @reydios_luz = Sprite.new(@viewport1)
        @reydios_luz.bitmap = RPG::Cache.picture(sprintf('acto6_luz%02d',mid))
        @reydios_luz.z = 2500
        @reydios_mid = mid
      end
      @reydios_luz.x = -$game_map.display_x/4
      @reydios_luz.y = -$game_map.display_y/4
      @reydios_tension = Sprite_TensionA6.new unless @reydios_tension
    elsif @reydios_luz
      @reydios_luz.dispose; @reydios_luz = nil; @reydios_mid = nil
    end
    @reydios_tension.update if @reydios_tension
  end
  def dispose
    @reydios_luz.dispose if @reydios_luz
    @reydios_tension.dispose if @reydios_tension
    reydios_ss_dispose_antes
  end
end

class Scene_FinalVacas
  def initialize(rama); @rama = rama; end
  def main
    Vacas_Audio.play(:tema_tranquilo_seguro_tv)
    @background = Vacas_UI.background('titulo')
    @text = Sprite.new
    @text.bitmap = Bitmap.new(640,480)
    b = @text.bitmap
    Vacas_UI.text(b,40,128,560,'FIN',56,Vacas_UI::MINT)
    Vacas_UI.text(b,40,204,560,Vacas::FINALES_A6[@rama-1],30)
    lines = [
      ['La ciudad aprende a bajar la cabeza.','Un rey también tiene que dormir.'],
      ['La cadena conserva todos los puestos.','Ahora uno lleva tu nombre.'],
      ['Al otro lado no hay una vida prometida.','Hay un camino. Empiezas por él.']][@rama-1]
    lines.each_with_index { |line,i| Vacas_UI.text(b,40,270+i*32,560,line,21) }
    Vacas_UI.text(b,40,412,560,'Z / Intro: créditos del juego',18)
    @frames = 0
    Vacas_UI.loop_scene(self)
    @text.bitmap.dispose; @text.dispose; @background.dispose
  end
  def update
    @background.update; @frames += 1
    if @frames >= 480 || (@frames > 40 && Input.trigger?(Input::C))
      $scene = Scene_CreditosJuego.new
    end
  end
end

class Scene_CreditosJuego
  TEAM = ['FEKA STUDIOS','VACAS','',
    'Carlos - dirección, arte, diseño','Alexandre - historia',
    'Ithalo "Ander" - sonido','',
    'Adaptación libre. Diálogos originales.','Gracias por llegar hasta aquí.','',
    'CRÉDITOS DE AUDIO Y LICENCIAS','Listado íntegro; también accesible desde el título.','']
  def main
    @background = Vacas_UI.background('titulo')
    @viewport = Viewport.new(20,30,600,390)
    @viewport.z = 100
    @text = Sprite.new(@viewport)
    @text.bitmap = Bitmap.new(600,440)
    @footer = Vacas.sprite_texto(['Créditos: mantener Z acelera / Esc vuelve al título'],438,26,16)
    @lines = TEAM + Vacas_Audio::CREDITS_LINES + ['', 'FEKA STUDIOS', 'FIN']
    @offset = -340
    Vacas_Audio.play(:tema_tranquilo_seguro_tv)
    Vacas_UI.loop_scene(self)
    @text.bitmap.dispose; @text.dispose; @viewport.dispose
    @footer.bitmap.dispose; @footer.dispose; @background.dispose
  end
  def update
    @background.update
    @offset += Input.press?(Input::C) ? 16 : 2
    b = @text.bitmap; b.clear
    b.font.name = 'Courier New'; b.font.size = 16; b.font.color = Vacas_UI::INK
    first = [@offset / 26,0].max
    (first..[first+17,@lines.size-1].min).each do |i|
      b.draw_text(8,i*26-@offset,584,26,@lines[i],1)
    end
    if Input.trigger?(Input::B) || @offset > @lines.size*26+40
      $scene = Scene_Title.new
    end
  end
end
