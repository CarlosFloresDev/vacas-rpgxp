# === VACAS: FUENTE VIGENTE ===
# Script: Vacas_Matadero | posición en Scripts.rxdata: 93 (base 0)
# Función: Turnos, tareas y progreso del matadero.
# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.
# Switches simbólicos: SW_ESCONDIDO2, SW_PATRULLA_CAM, SW_PATRULLA_OFI, SW_PILLADO_CRIPPS
# Switches con ID literal: ninguno
# Variables simbólicas: VAR_RESULTADO
# Variables con ID literal: ninguna
# Los índices calculados y rangos se describen en el código y en docs/sistemas/.
# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).
# === FIN CABECERA ===
#==============================================================================
# ** Vacas - Matadero (Acto II)
#------------------------------------------------------------------------------
#  Minijuegos de trabajo (el corte y la cinta), vigilancia de Cripps y
#  escondites. Se llaman desde eventos con "Llamar script":
#    minijuego_corte(rondas)   -> resultado en la variable 12 (aciertos)
#    minijuego_cinta(piezas)   -> resultado en la variable 12 (aciertos)
#  Compatible con RGSS1 (Ruby 1.8).
#==============================================================================

#------------------------------------------------------------------------------
# Base comun: capa oscura encima del mapa, textos y espera
#------------------------------------------------------------------------------
class Vacas_Minijuego
  def initialize
    @vp = Viewport.new(0, 0, Vacas_HD.w, Vacas_HD.h)
    @vp.z = 6000
    @sprites = []
    @fondo = nuevo_sprite(Vacas_HD.w, Vacas_HD.h)
    @fondo.bitmap.fill_rect(0, 0, Vacas_HD.w, Vacas_HD.h, Color.new(6, 4, 4, 200))
  end
  def nuevo_sprite(w, h)
    s = Sprite.new(@vp)
    s.bitmap = Bitmap.new(w, h)
    @sprites.push(s)
    return s
  end
  def texto(s, y, tam, color, h = 32)
    sp = nuevo_sprite(Vacas_HD.w, h)
    sp.y = Vacas_HD.y(y)
    sp.bitmap.font.size = tam
    sp.bitmap.font.color = color
    sp.bitmap.draw_text(0, 0, Vacas_HD.w, h, s, 1)
    return sp
  end
  def rotulo(sp, s, color)
    sp.bitmap.clear
    sp.bitmap.font.color = color
    sp.bitmap.draw_text(0, 0, Vacas_HD.w, sp.bitmap.height, s, 1)
  end
  def esperar(n)
    n.times do
      tick
    end
  end
  def tick
    Graphics.update
    Input.update
    @vp.update
  end
  def se(nombre, vol = 80, tono = 100)
    $game_system.se_play(RPG::AudioFile.new(nombre, vol, tono))
  end
  def veneno
    return Vacas.veneno
  end
  def dispose
    for s in @sprites
      s.bitmap.dispose
      s.dispose
    end
    @vp.dispose
  end
  CLARO = Color.new(214, 204, 186)
  GRIS  = Color.new(140, 130, 118)
  ROJO  = Color.new(190, 36, 30)
  OSCURO = Color.new(60, 10, 10)
end

#------------------------------------------------------------------------------
# El corte: una cuchilla va y viene por una barra. Hay que soltarla
# (Intro) cuando cruza la franja roja. La franja se estrecha.
#------------------------------------------------------------------------------
class Vacas_Corte < Vacas_Minijuego
  BX = 120
  BW = 400
  BY = Vacas_HD.y(330)
  def initialize(rondas)
    super()
    @rondas = rondas
    texto("EL CORTE", 26, 26, ROJO, 36)
    texto("Pulsa Intro cuando la cuchilla cruce la franja roja.", 62, 18, GRIS)
    @canal = nuevo_sprite(160, 220)
    @canal.zoom_x = @canal.zoom_y = Vacas_HD.h / 480.0
    @canal.x = 240
    @canal.y = Vacas_HD.y(92)
    dibujar_canal(0)
    @barra = nuevo_sprite(BW + 8, 32)
    @barra.x = BX - 4
    @barra.y = BY
    @cuchilla = nuevo_sprite(6, 44)
    @cuchilla.bitmap.fill_rect(0, 0, 6, 44, Color.new(230, 232, 236))
    @cuchilla.bitmap.fill_rect(2, 0, 2, 44, Color.new(120, 124, 130))
    @cuchilla.y = BY - 6
    @info = texto("", 380, 22, CLARO)
    @cuenta = texto("", 420, 18, GRIS)
  end
  def dibujar_canal(cortes)
    b = @canal.bitmap
    b.clear
    b.fill_rect(76, 0, 8, 20, Color.new(150, 156, 162))
    b.fill_rect(30, 20, 100, 190, Color.new(30, 6, 6))
    b.fill_rect(34, 24, 92, 182, Color.new(140, 48, 44))
    b.fill_rect(46, 30, 68, 170, Color.new(168, 74, 64))
    y = 40
    while y < 196
      b.fill_rect(48, y, 64, 3, Color.new(214, 196, 170))
      y += 14
    end
    b.fill_rect(78, 24, 4, 182, Color.new(96, 26, 24))
    for i in 0...cortes
      yy = 40 + i * 26
      b.fill_rect(20, yy, 120, 2, Color.new(20, 0, 0))
    end
  end
  def nueva_franja(r)
    ancho = 70 - r * 6
    ancho = 38 if ancho < 38
    @zona_w = ancho
    @zona_x = 20 + rand(BW - ancho - 40)
    b = @barra.bitmap
    b.clear
    b.fill_rect(0, 0, BW + 8, 32, Color.new(0, 0, 0))
    b.fill_rect(4, 4, BW, 24, Color.new(70, 66, 62))
    b.fill_rect(4 + @zona_x, 4, @zona_w, 24, Color.new(150, 24, 20))
    b.fill_rect(4 + @zona_x + @zona_w / 2 - 1, 4, 2, 24, Color.new(220, 120, 110))
  end
  def run
    aciertos = 0
    esperar(30)
    for r in 0...@rondas
      nueva_franja(r)
      rotulo(@cuenta, "Pieza " + (r + 1).to_s + " de " + @rondas.to_s, GRIS)
      rotulo(@info, "", CLARO)
      pos = 0.0
      vel = [4.0 + r * 0.6, 7.0].min
      dir = 1
      marco = 0
      soltado = false
      while marco < 360
        tick
        marco += 1
        pos += vel * dir
        if pos >= BW - 2
          pos = BW - 2
          dir = -1
        elsif pos <= 0
          pos = 0
          dir = 1
        end
        temblor = 0
        temblor = rand(5) - 2 if veneno >= 50 and rand(6) == 0
        @cuchilla.x = BX + pos.to_i - 3 + temblor
        # alucinacion: la canal respira
        if veneno >= 40 and marco % 90 < 10
          @canal.zoom_x = 1.0 + (marco % 90) * 0.004
        else
          @canal.zoom_x = 1.0
        end
        if Input.trigger?(Input::C)
          soltado = true
          break
        end
      end
      centro = pos - @zona_x
      if soltado and centro >= 0 and centro <= @zona_w
        aciertos += 1
        se("093-Attack05", 80, 70)
        @vp.flash(Color.new(120, 0, 0, 90), 6)
        rotulo(@info, "Limpio.", CLARO)
      else
        se("057-Wrong01", 70, 80)
        @vp.flash(Color.new(0, 0, 0, 200), 10)
        rotulo(@info, soltado ? "Torcido. Se ha astillado el hueso." : "Demasiado lento.", ROJO)
      end
      dibujar_canal(aciertos)
      esperar(40)
    end
    rotulo(@cuenta, "", GRIS)
    rotulo(@info, "Cortes limpios: " + aciertos.to_s + " de " + @rondas.to_s, CLARO)
    esperar(70)
    return aciertos
  end
end

#------------------------------------------------------------------------------
# La cinta: piezas que llegan por la derecha con una flecha. Pulsa esa
# direccion cuando la pieza esta dentro del recuadro. La cinta acelera.
#------------------------------------------------------------------------------
class Vacas_Cinta < Vacas_Minijuego
  ZX = 90
  ZW = 70
  CY = Vacas_HD.y(250)
  DIRS = [2, 4, 6, 8]
  def initialize(piezas)
    super()
    @total = piezas
    texto("LA CINTA", 26, 26, ROJO, 36)
    texto("Pulsa la flecha de cada pieza cuando entre en el recuadro.", 62, 18, GRIS)
    @cinta = nuevo_sprite(Vacas_HD.w, 80)
    @cinta.y = CY - 10
    @cinta_off = 0
    @zona = nuevo_sprite(ZW, 76)
    @zona.x = ZX
    @zona.y = CY - 8
    pintar_zona(Color.new(200, 190, 170))
    @info = texto("", 360, 22, CLARO)
    @cuenta = texto("", 400, 18, GRIS)
    @piezas = []
  end
  def pintar_zona(c)
    b = @zona.bitmap
    b.clear
    b.fill_rect(0, 0, ZW, 3, c)
    b.fill_rect(0, 73, ZW, 3, c)
    b.fill_rect(0, 0, 3, 76, c)
    b.fill_rect(ZW - 3, 0, 3, 76, c)
  end
  def pintar_cinta
    b = @cinta.bitmap
    b.clear
    b.fill_rect(0, 0, Vacas_HD.w, 60, Color.new(20, 20, 22))
    b.fill_rect(0, 4, Vacas_HD.w, 52, Color.new(52, 52, 54))
    x = -(@cinta_off % 24)
    while x < Vacas_HD.w
      b.fill_rect(x, 4, 2, 52, Color.new(82, 82, 84))
      x += 24
    end
  end
  def flecha(b, d, cx, cy, c)
    for i in 0...10
      case d
      when 8 then b.fill_rect(cx - i, cy - 8 + i, i * 2 + 1, 1, c)
      when 2 then b.fill_rect(cx - i, cy + 8 - i, i * 2 + 1, 1, c)
      when 4 then b.fill_rect(cx - 8 + i, cy - i, 1, i * 2 + 1, c)
      when 6 then b.fill_rect(cx + 8 - i, cy - i, 1, i * 2 + 1, c)
      end
    end
  end
  def nueva_pieza
    s = nuevo_sprite(48, 48)
    d = DIRS[rand(4)]
    b = s.bitmap
    b.fill_rect(2, 6, 44, 36, Color.new(30, 6, 6))
    b.fill_rect(4, 8, 40, 32, Color.new(150, 52, 46))
    b.fill_rect(6, 12, 36, 4, Color.new(214, 196, 170))
    flecha(b, d, 24, 26, Color.new(240, 236, 226))
    s.x = Vacas_HD.w
    s.y = CY
    @piezas.push([s, d, false])
  end
  def run
    aciertos = 0
    lanzadas = 0
    espera = 0
    vel = 3.0
    esperar(30)
    loop do
      tick
      @cinta_off += vel.to_i
      pintar_cinta
      espera -= 1
      if lanzadas < @total and espera <= 0
        nueva_pieza
        lanzadas += 1
        espera = 70 - lanzadas * 3
        espera = 34 if espera < 34
        vel += 0.25
      end
      pulsada = Input.dir4
      pulsada = 0 unless Input.trigger?(Input::DOWN) or Input.trigger?(Input::LEFT) or
                         Input.trigger?(Input::RIGHT) or Input.trigger?(Input::UP)
      # pieza mas adelantada todavia viva
      primera = nil
      for p in @piezas
        next if p[2]
        primera = p
        break
      end
      if pulsada != 0 and primera != nil
        dentro = primera[0].x + 24 >= ZX and primera[0].x + 24 <= ZX + ZW
        if dentro and pulsada == primera[1]
          aciertos += 1
          primera[2] = true
          primera[0].visible = false
          se("093-Attack05", 70, 90)
          pintar_zona(Color.new(220, 60, 50))
          rotulo(@info, "Bien.", CLARO)
        else
          se("057-Wrong01", 60, 80)
          @vp.flash(Color.new(120, 0, 0, 80), 6)
          primera[2] = true
          primera[0].opacity = 90
          rotulo(@info, "¡Esa no!", ROJO)
        end
      end
      for p in @piezas
        p[0].x -= vel.to_i
        if !p[2] and p[0].x + 24 < ZX
          p[2] = true
          p[0].opacity = 90
          se("057-Wrong01", 50, 70)
          rotulo(@info, "Se te ha escapado una.", ROJO)
        end
        if p[0].x < -48 and p[0].visible
          p[0].visible = false
        end
      end
      pintar_zona(Color.new(200, 190, 170)) if Graphics.frame_count % 12 == 0
      if veneno >= 45 and rand(240) == 0
        @vp.flash(Color.new(0, 0, 0, 160), 8)
      end
      rotulo(@cuenta, "Piezas: " + aciertos.to_s + " / " + @total.to_s, GRIS) if Graphics.frame_count % 10 == 0
      terminado = (lanzadas >= @total)
      for p in @piezas
        terminado = false if p[0].x > -48 and p[0].visible
      end
      break if terminado
    end
    rotulo(@info, "La cinta se para. Piezas a tiempo: " + aciertos.to_s + " de " + @total.to_s, CLARO)
    esperar(70)
    return aciertos
  end
end

class Interpreter
  def minijuego_corte(rondas)
    m = Vacas_Corte.new(rondas)
    r = m.run
    m.dispose
    $game_variables[Vacas::VAR_RESULTADO] = r
    Input.update
    return true
  end
  def minijuego_cinta(piezas)
    m = Vacas_Cinta.new(piezas)
    r = m.run
    m.dispose
    $game_variables[Vacas::VAR_RESULTADO] = r
    Input.update
    return true
  end
end

#==============================================================================
# ** Vigilancia de Cripps
#   Los eventos llamados "Cripps vigila" ven en linea recta hacia donde
#   miran (5 casillas) y notan al jugador pegado a ellos. Las paredes y las
#   canales colgadas tapan la vista. Escondido, no te ven.
#==============================================================================
class Game_Event
  def vacas_vigia?
    return false if @erased or @character_name == "" or @transparent or @opacity == 0
    return @event.name == "Cripps vigila"
  end
  def vacas_tapa?(x, y)
    for ev in $game_map.events.values
      next if ev == self or ev.through
      next if ev.character_name == ""
      return true if ev.x == x and ev.y == y
    end
    return false
  end
  def vacas_ve_al_jugador?
    px = $game_player.x
    py = $game_player.y
    dx = px - @x
    dy = py - @y
    return true if dx.abs + dy.abs <= 1
    rango = 5
    case @direction
    when 2 then return false unless dx == 0 and dy > 0 and dy <= rango
    when 8 then return false unless dx == 0 and dy < 0 and -dy <= rango
    when 6 then return false unless dy == 0 and dx > 0 and dx <= rango
    when 4 then return false unless dy == 0 and dx < 0 and -dx <= rango
    else return false
    end
    sx = (dx <=> 0)
    sy = (dy <=> 0)
    x = @x + sx
    y = @y + sy
    while x != px or y != py
      return false unless $game_map.passable?(x, y, 0)
      return false if vacas_tapa?(x, y)
      x += sx
      y += sy
    end
    return true
  end
end

class Game_Map
  alias vacas_gm_update update
  def update
    vacas_gm_update
    vacas_vigilar
  end
  def vacas_vigilar
    return unless $game_switches[Vacas::SW_PATRULLA_CAM] or $game_switches[Vacas::SW_PATRULLA_OFI]
    return if $game_switches[Vacas::SW_ESCONDIDO2] or $game_switches[Vacas::SW_PILLADO_CRIPPS]
    return if $game_system.map_interpreter.running? or $game_temp.message_window_showing
    for ev in @events.values
      next unless ev.vacas_vigia?
      if ev.vacas_ve_al_jugador?
        $game_switches[Vacas::SW_PILLADO_CRIPPS] = true
        @need_refresh = true
        $game_screen.start_flash(Color.new(255, 0, 0, 160), 10)
        $game_system.se_play(RPG::AudioFile.new("092-Attack04", 90, 60))
        return
      end
    end
  end
end

#==============================================================================
# ** Escondites: mientras el interruptor 30 esta activo, Steven no se mueve;
#    cualquier direccion o Intro le hace salir del escondite.
#==============================================================================
class Game_Player
  alias vacas_gp_update update
  def update
    if $game_switches[Vacas::SW_ESCONDIDO2] and !moving? and
       !$game_system.map_interpreter.running? and !$game_temp.message_window_showing and
       !@move_route_forcing
      if Input.dir4 != 0 or Input.trigger?(Input::C)
        $game_switches[Vacas::SW_ESCONDIDO2] = false
        @opacity = 255
        $game_map.need_refresh = true
        $game_system.se_play(RPG::AudioFile.new("045-Push01", 50, 120))
      end
      return
    end
    vacas_gp_update
  end
  def vacas_esconder
    $game_switches[Vacas::SW_ESCONDIDO2] = true
    @opacity = 90
    $game_map.need_refresh = true
  end
end

class Interpreter
  def esconderse
    $game_player.vacas_esconder
    return true
  end
end
