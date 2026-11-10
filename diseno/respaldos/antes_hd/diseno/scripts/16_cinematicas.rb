# === VACAS: FUENTE VIGENTE ===
# Script: Vacas_Cinematicas | posición en Scripts.rxdata: 104 (base 0)
# Función: Cinemáticas, transiciones y omisión de escenas.
# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.
# Switches simbólicos: ninguno
# Switches con ID literal: 22, 81, 113, 140, 176
# Variables simbólicas: ninguna
# Variables con ID literal: ninguna
# Los índices calculados y rangos se describen en el código y en docs/sistemas/.
# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).
# === FIN CABECERA ===
# Cinematicas. RGSS1 / Ruby 1.8. Texto original, violencia fuera de campo.
module Vacas_Cine
  # picture, retrato VN, titulo, frase, segundos, BGM, BGS, SE de entrada
  APERTURA = [
    ['cine_piso','steven_neutral','STEVEN',
      'Antes del turno, hay que aprender a levantarse.',13,
      :tema_tranquilo_seguro_tv,:reloj_tictac_piso,nil],
    ['cine_piso',nil,'EL PISO',
      'Cada puerta guarda una tarea pendiente.',14,
      :tema_tranquilo_seguro_tv,:reloj_tictac_piso,nil],
    ['cine_piso','madre_neutral','MADRE',
      'Su voz llega incluso cuando la casa calla.',12,
      :tema_tranquilo_seguro_tv,:reloj_tictac_piso,nil],
    ['cine_matadero',nil,'AL OTRO LADO DE LA CALLE',
      'A lo lejos, el matadero ya ha encendido sus luces.',15,
      :exploracion_matadero,:lluvia_exterior,nil]
  ]
  ACTOS = {
    2 => ['Acto II — La cadena','El reloj de la casa se convierte en sirena.',:cadenas_y_transportador],
    3 => ['Acto III — Lucy','Alguien pregunta por lo que no se ve.',:reloj_tictac_piso],
    4 => ['Acto IV — Bajo la ciudad','El agua conserva los nombres borrados.',:ambiente_hueco_alcantarilla_camara],
    5 => ['Acto V — La matanza','Esta noche, nadie quiere ocupar su puesto.',:cadenas_y_transportador],
    6 => ['Acto VI — Rey-dios','Todo camino de vuelta exige una respuesta.',:ambiente_hueco_alcantarilla_camara]
  }
  FINALES = {
    1 => [
      ['cine_altar','guernsey_susurro','EL ASIENTO',
        'Las voces esperan una orden. Steven tarda en respirar.',7,
        :alterna_camaras_drone,:ambiente_hueco_alcantarilla_camara,nil],
      ['cine_ciudad',nil,'REY DE LA MANADA',
        'La ciudad amanece bajo una nueva mirada.',6,
        :alterna_camaras_drone,:lluvia_exterior,nil]],
    2 => [
      ['cine_matadero',nil,'EL ÚLTIMO PUESTO',
        'Un gancho avanza. La puerta empieza a cerrarse.',7,
        :alterna_camaras_drone,:cadenas_y_transportador,:cadena_gancho],
      [nil,nil,'GANADO','La puerta se cierra. Solo queda el motor.',6,
        :alterna_camaras_drone,:cadenas_y_transportador,nil]],
    3 => [
      ['cine_ciudad','dog_neutral','EL HUECO',
        'Perro encuentra un paso entre las cosas caídas.',7,
        :tema_tranquilo_seguro_tv,:lluvia_exterior,nil],
      ['cine_ciudad',nil,'HUIDA','Steven da un paso. Después, otro.',6,
        :tema_tranquilo_seguro_tv,:lluvia_exterior,nil]]
  }
  def self.tarjeta(acto)
    row = ACTOS[acto]
    return [[nil,nil,row[0],row[1],6,:alterna_camaras_drone,row[2],nil]]
  end
  def self.atajo?
    return [Input::A,Input::SHIFT,Input::CTRL,Input::ALT,Input::L].any? { |k| Input.press?(k) }
  end
end

# Escena aislada: no consume Pictures del mapa (98 pertenece a los sustos),
# no avanza interpretes ni persecuciones, ni modifica tono/inventario/switches.
class Scene_VacasCine
  attr_reader :terminada, :omitida
  def initialize(planos, destino = nil, restaurar = false)
    @planos = planos; @destino = destino; @restaurar = restaurar
  end
  def main
    @fps = Graphics.frame_rate
    @indice = -1; @hold = 0; @listo = false
    @terminada = false; @omitida = false
    @fondo = Sprite.new
    @fondo.bitmap = Bitmap.new(640,480)
    @fondo.bitmap.fill_rect(0,0,640,480,Color.new(0,0,0))
    @fondo.z = 4000
    @plano = Sprite.new; @plano.z = 4001
    @retrato = Sprite.new; @retrato.z = 4002
    @texto = Sprite.new; @texto.z = 4003
    @texto.bitmap = Bitmap.new(640,480)
    siguiente
    Graphics.transition(12)
    until @terminada
      Graphics.update; Input.update; update
    end
    if @omitida
      12.times do
        for s in [@plano,@retrato,@texto]; s.opacity -= 22; end
        Graphics.update; Input.update
      end
    end
    Graphics.freeze
  ensure
    @menu.dispose if @menu
    for s in [@fondo,@plano,@retrato,@texto]
      next unless s
      # Cache posee las capturas y los retratos: nunca liberarlos aqui.
      s.bitmap.dispose if s.bitmap && (s == @fondo || s == @texto)
      s.dispose
    end
    Audio.bgm_fade(500); Audio.bgs_fade(500)
    if @restaurar && $game_map
      Audio.bgm_stop; Audio.bgs_stop
      $game_map.autoplay
    end
    Input.update
    $scene = @destino if @destino
  end
  def siguiente
    @indice += 1
    if @indice >= @planos.size
      @terminada = true
      return
    end
    row = @planos[@indice]; @frame = 0
    @duracion = (@fps * row[4]).to_i
    @plano.bitmap = row[0] ? RPG::Cache.picture(row[0]) : nil
    @plano.tone = Tone.new(-45,-52,-58,30)
    @plano.zoom_x = @plano.zoom_y = 1.08
    @retrato.bitmap = row[1] ? RPG::Cache.picture('retrato_'+row[1]) : nil
    @retrato.x = 32; @retrato.y = 42
    @retrato.zoom_x = @retrato.zoom_y = 0.70
    Vacas_Audio.play(row[5]) if row[5]
    Vacas_Audio.play(row[6]) if row[6]
    Vacas_Audio.play(row[7]) if row[7]
    b = @texto.bitmap; b.clear
    b.fill_rect(0,338,640,142,Color.new(0,0,0,235))
    b.font.name = 'Arial'; b.font.size = 26
    b.font.color = Color.new(210,220,204)
    b.draw_text(24,350,592,36,row[2],1)
    b.font.size = 19
    b.draw_text(16,392,608,32,row[3],1)
    b.font.size = 15; b.font.color = Color.new(160,164,152)
    b.draw_text(16,445,608,24,'Mantén Z / Intro 1 s para saltar · Esc: menú',1)
    animar
  end
  def animar
    fade = [@frame,@duracion-@frame,@fps].min * 255 / @fps
    @plano.opacity = fade; @texto.opacity = fade; @retrato.opacity = fade
    if @plano.bitmap
      t = @frame.to_f / @duracion
      dx = [@plano.bitmap.width*1.08-640,0].max
      dy = [@plano.bitmap.height*1.08-480,0].max
      @plano.x = -dx * (0.35 + t*0.25)
      @plano.y = -dy * (0.55 - t*0.20)
    end
  end
  def update
    if @menu
      @menu.update
      if Input.trigger?(Input::B) || Input.trigger?(Input::C)
        salir = Input.trigger?(Input::C) && @menu.index == 1
        @menu.dispose; @menu = nil; @listo = false; @hold = 0
        @terminada = @omitida = true if salir
      end
      return
    end
    # Exige soltar la confirmacion que abrio Nueva partida / el fin del acto.
    @listo = true unless Input.press?(Input::C)
    @hold = (@listo && Input.press?(Input::C)) ? @hold+1 : 0
    if @hold >= @fps
      @terminada = @omitida = true
      return
    end
    if Input.trigger?(Input::B)
      @menu = Window_Command.new(280,['Continuar cinemática','Saltar cinemática'])
      @menu.x = 180; @menu.y = 170; @menu.z = 4100
      return
    end
    @frame += 1; animar
    siguiente if @frame >= @duracion
  end
end

class Scene_Title
  alias cine_nueva_antes command_new_game
  def command_new_game
    salto = Vacas_Cine.atajo?
    cine_nueva_antes
    $game_temp.vacas_tarjeta = nil
    if !salto && $scene.is_a?(Scene_Map)
      $scene = Scene_VacasCine.new(Vacas_Cine::APERTURA,$scene,true)
    end
  end
end

class Scene_FinActo
  def main
    siguiente = @acto + 1
    unless Vacas_Cine::ACTOS[siguiente]
      $scene = Scene_Title.new
      return
    end
    Scene_VacasCine.new(Vacas_Cine.tarjeta(siguiente)).main
    Vacas.send('empezar_acto'+siguiente.to_s)
    $game_temp.vacas_tarjeta = nil
    $scene = Scene_Map.new
  end
end

# Las puertas fisicas tambien pueden iniciar actos sin Scene_FinActo.
class Game_Temp
  attr_accessor :vacas_tarjeta
end
module Vacas
  class << self
    alias cine_acto2 empezar_acto2
    alias cine_acto3 empezar_acto3
    alias cine_acto4 empezar_acto4
    alias cine_acto5 empezar_acto5
    alias cine_acto6 empezar_acto6
    def empezar_acto2
      nuevo = !$game_switches[22]; cine_acto2
      $game_temp.vacas_tarjeta = 2 if nuevo && $game_switches[22]
    end
    def empezar_acto3
      nuevo = !$game_switches[81]; cine_acto3
      $game_temp.vacas_tarjeta = 3 if nuevo && $game_switches[81]
    end
    def empezar_acto4
      nuevo = !$game_switches[113]; cine_acto4
      $game_temp.vacas_tarjeta = 4 if nuevo && $game_switches[113]
    end
    def empezar_acto5
      nuevo = !$game_switches[140]; cine_acto5
      $game_temp.vacas_tarjeta = 5 if nuevo && $game_switches[140]
    end
    def empezar_acto6
      nuevo = !$game_switches[176]; cine_acto6
      $game_temp.vacas_tarjeta = 6 if nuevo && $game_switches[176]
    end
  end
end
class Scene_Map
  alias cine_map_update update
  def update
    cine_map_update
    if $scene == self && $game_temp.vacas_tarjeta &&
        !$game_system.map_interpreter.running? && !$game_temp.player_transferring &&
        !$game_temp.message_window_showing
      acto = $game_temp.vacas_tarjeta; $game_temp.vacas_tarjeta = nil
      $scene = Scene_VacasCine.new(Vacas_Cine.tarjeta(acto),Scene_Map.new,true)
    end
  end
end

class Scene_FinalVacas
  alias cine_final_antes main
  def main
    Scene_VacasCine.new(Vacas_Cine::FINALES[@rama]).main
    cine_final_antes
  end
end
