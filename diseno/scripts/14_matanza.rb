# === VACAS: FUENTE VIGENTE ===
# Script: Vacas_Matanza | posición en Scripts.rxdata: 102 (base 0)
# Función: Progreso y pruebas del Acto V (La matanza).
# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.
# Switches simbólicos: SW_HUD_OCULTO
# Switches con ID literal: 132, 133, 134, 140, 142, 150, 151, 159
# Variables simbólicas: VAR_RESULTADO
# Variables con ID literal: 51, 54, 55, 57, 58, 59, 60, 61
# Los índices calculados y rangos se describen en el código y en docs/sistemas/.
# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).
# === FIN CABECERA ===
# Acto V: La matanza. RGSS1 / Ruby 1.8.
#   Mapas 22-27, interruptores 140-171, variables 57-61, objetos 35-38,
#   enemigos/tropas 18-21, sustos 12/13. Atajo: Q + Nueva partida (W: venganza).
module Vacas
  def self.matanza?
    return $game_switches[140] && (22..27).include?($game_map.map_id)
  end
  def self.empezar_acto5
    return unless $game_switches[132]
    unless $game_switches[140]
      $game_switches[140] = true
      $game_variables[57] = 0
      $game_variables[58] = $game_switches[134] ? 1 : 0
      $game_variables[59] = $game_switches[133] ? 1 : 0
      $game_variables[60] = 0
      $game_variables[61] = 1
    end
    detener_caza
    for id in [26,29,30,31,142,150]
      $game_switches[id] = false
    end
    $game_system.timer_working = false
    $game_system.menu_disabled = false
    $game_system.save_disabled = true
    $game_player.transparent = false
    $game_temp.player_new_map_id = 22
    $game_temp.player_new_x = 3
    $game_temp.player_new_y = 11
    $game_temp.player_new_direction = 8
    $game_temp.player_transferring = true
    $game_temp.transition_processing = false
  end
  def self.prueba_acto5(venganza = false)
    prueba_acto4(false)
    for id in [114,116,117,118,119,121,124,126,127,128,129,130,131,132,135,138,139]
      $game_switches[id] = true
    end
    $game_switches[133] = !venganza
    $game_switches[134] = venganza
    $game_variables[51] = venganza ? 0 : 3
    $game_variables[54] = 2
    $game_variables[55] = 6
    $game_party.gain_item(33,1)
    empezar_acto5
    $game_temp.player_transferring = false
    $game_map.setup(22)
    $game_player.moveto(3,11)
    $game_player.turn_up
    $game_map.autoplay
    $game_map.update
  end
  def self.alarma(n)
    $game_variables[57] = [[0,$game_variables[57]+n].max,3].min
  end
  def self.inclinar(var, n)
    $game_variables[var] = [[0,$game_variables[var]+n].max,6].min
  end
  class << self
    alias matanza_tareas_antes tareas
    def tareas
      return matanza_tareas_antes unless $game_switches[140]
      s = $game_switches
      return [["Acto VI: abajo te esperan.",false]] if s[163]
      return [["Patio: hablar con la Guernsey. Amanece.",false]] if s[159]
      return [["Oficina alta: Cripps.",false]] if s[151]
      return [["Sangrado: cruzar hasta la escalera.",false]] if s[148]
      return [["Sala de matanza: invertir la noria.",false]] if $game_map.map_id >= 24
      return [["Corrales: cadenas y sirena. Luego, la nave.",false]] if $game_party.item_number(35) > 0
      return [["Muelle: las llaves estan en la garita.",false]]
    end
  end
end

module Vacas_Audio
  MAP_AUDIO[22] = [:matadero,:alterna_calle_de_noche_suspense,:lluvia_exterior,:concreto]
  MAP_AUDIO[23] = [:matadero,:exploracion_matadero,:corral_de_ganado_mugidos_y_arrastre,:concreto]
  MAP_AUDIO[24] = [:matadero,:exploracion_matadero,:cadenas_y_transportador,:baldosa]
  MAP_AUDIO[25] = [:camaras,:camaras_frias,:compresor_de_camara_fria,:baldosa]
  MAP_AUDIO[26] = [:matadero,:alterna_camaras_drone,:reloj_tictac_piso,:madera]
  MAP_AUDIO[27] = [:matadero,:tema_tranquilo_seguro_tv,:lluvia_exterior,:concreto]
  class << self
    alias matanza_chasing chasing?
    def chasing?
      return true if $game_switches[150]
      return matanza_chasing
    end
  end
end

class Scene_Title
  alias matanza_nueva_partida command_new_game
  def command_new_game
    salto = Vacas_HD.key?(:q)
    venganza = Vacas_HD.key?(:w)
    matanza_nueva_partida
    Vacas.prueba_acto5(venganza) if salto
  end
end

# La noria: variacion dura de la cinta. Las piezas azules piden la flecha contraria.
class Vacas_Noria < Vacas_Cinta
  OPUESTA = {2=>8, 8=>2, 4=>6, 6=>4}
  def initialize(piezas)
    super(piezas)
    rotulo(@sprites[1], "LA NORIA", ROJO)
    rotulo(@sprites[2], "Roja: pulsa su flecha.  AZUL: pulsa la CONTRARIA.", GRIS)
  end
  def nueva_pieza
    s = nuevo_sprite(48, 48)
    d = DIRS[rand(4)]
    cruzada = rand(100) < 40
    b = s.bitmap
    b.fill_rect(2, 6, 44, 36, Color.new(8, 8, 14))
    if cruzada
      b.fill_rect(4, 8, 40, 32, Color.new(48, 82, 150))
    else
      b.fill_rect(4, 8, 40, 32, Color.new(150, 52, 46))
    end
    b.fill_rect(6, 12, 36, 4, Color.new(214, 196, 170))
    flecha(b, d, 24, 26, Color.new(240, 236, 226))
    s.x = Vacas_HD.w
    s.y = CY
    @piezas.push([s, cruzada ? OPUESTA[d] : d, false])
  end
end

class Interpreter
  alias matanza_susto_antes susto
  def susto(id)
    return matanza_susto_antes(id) unless [12,13].include?(id)
    flag = id == 12 ? 157 : 158
    return true if $game_switches[flag]
    $game_switches[flag] = true
    $game_screen.vacas_susto(id)
    @wait_count = 24
    return true
  end
  def minijuego_noria(piezas)
    m = Vacas_Noria.new(piezas)
    r = m.run
    m.dispose
    $game_variables[Vacas::VAR_RESULTADO] = r
    Input.update
    return true
  end
  def matanza_alarma(n)
    Vacas.alarma(n)
    return true
  end
  def matanza_inclinar(var, n)
    Vacas.inclinar(var, n)
    return true
  end
  def matanza_tension(n)
    subir_veneno_tope(n,96)
    return true
  end
  def matanza_descubierto
    Vacas.alarma(1)
    subir_veneno_tope(4,96)
    $game_switches[142] = false
    return true
  end
  def matanza_captura
    $game_variables[60] += 1
    subir_veneno_tope(8,96)
    Vacas.alarma(1)
    return true
  end
  def matanza_fin_caza
    $game_switches[150] = false
    $game_switches[151] = true
    $game_system.timer_working = false
    $game_system.menu_disabled = false
    $game_player.transparent = false
    $game_map.need_refresh = true
    return true
  end
  # La alarma acumulada endurece al jefe; nunca lo hace imposible.
  def matanza_jefe
    $data_enemies[21].maxhp = 860 + 70 * $game_variables[57]
    return true
  end
end

# Vigilantes del Acto V: eventos llamados "Vigia A5". Ven cinco casillas en linea recta.
class Game_Event
  def matanza_vigia?
    return false if @erased || @character_name == ""
    return @event.name == "Vigia A5"
  end
  alias matanza_ev_update update
  def update
    matanza_ev_update
    return unless $game_switches[150] && @event.name == "Cripps caza"
    return if @erased || @character_name == "" || moving? || jumping?
    return if $game_system.map_interpreter.running? || $game_temp.message_window_showing
    d = matanza_ruta
    case d
    when 2 then move_down
    when 4 then move_left
    when 6 then move_right
    when 8 then move_up
    end
  end
  # Busqueda en anchura desde el jugador: Cripps conoce su camara.
  def matanza_ruta
    w = $game_map.width
    h = $game_map.height
    px = $game_player.x
    py = $game_player.y
    dist = {}
    dist[px + py * w] = 0
    cola = [[px, py]]
    i = 0
    while i < cola.size
      x = cola[i][0]
      y = cola[i][1]
      i += 1
      d0 = dist[x + y * w]
      for paso in [[0,1],[-1,0],[1,0],[0,-1]]
        nx = x + paso[0]
        ny = y + paso[1]
        next if nx < 0 || ny < 0 || nx >= w || ny >= h
        next if dist[nx + ny * w]
        next unless $game_map.passable?(nx, ny, 0)
        dist[nx + ny * w] = d0 + 1
        cola.push([nx, ny])
      end
    end
    mejor = 0
    valor = 9999
    for paso in [[2,0,1],[4,-1,0],[6,1,0],[8,0,-1]]
      v = dist[(@x + paso[1]) + (@y + paso[2]) * w]
      next unless v
      if v < valor
        valor = v
        mejor = paso[0]
      end
    end
    return mejor
  end
end

class Game_Map
  alias matanza_gm_update update
  def update
    matanza_gm_update
    return unless Vacas.matanza?
    return if $game_switches[142] || $game_switches[150]
    return if $game_system.map_interpreter.running? || $game_temp.message_window_showing
    for ev in @events.values
      next unless ev.matanza_vigia?
      if ev.vacas_ve_al_jugador?
        $game_switches[142] = true
        @need_refresh = true
        $game_screen.start_flash(Color.new(255, 0, 0, 150), 10)
        Vacas_Audio.play(:cordura_baja_stinger)
        return
      end
    end
  end
end

# Luz nocturna anclada al mapa (como Vacas_Revision_Luces) y marcador de alarma.
class Sprite_Alarma < Sprite
  def initialize
    super(nil)
    self.bitmap = Bitmap.new(200, 22)
    self.x = 124
    self.y = Vacas_HD.bottom(40)
    self.z = 4000
    @estado = nil
  end
  def update
    super
    self.visible = Vacas.matanza? && !$game_switches[Vacas::SW_HUD_OCULTO] && !$game_switches[159]
    return unless self.visible
    a = $game_variables[57]
    return if a == @estado
    @estado = a
    b = self.bitmap
    b.clear
    b.font.size = 13
    b.font.color = Color.new(206, 198, 176)
    b.draw_text(0, 0, 60, 16, "alarma")
    for i in 0...3
      c = i < a ? Color.new(190, 36, 30) : Color.new(40, 36, 32, 220)
      b.fill_rect(54 + i * 16, 4, 12, 9, Color.new(12, 10, 10))
      b.fill_rect(55 + i * 16, 5, 10, 7, c)
    end
  end
  def dispose
    self.bitmap.dispose
    super
  end
end
class Spriteset_Map
  alias matanza_ss_update update
  alias matanza_ss_dispose dispose
  def update
    matanza_ss_update
    mid = $game_map.map_id
    if mid >= 22 && mid <= 27
      if @matanza_mid != mid
        @matanza_luz.dispose if @matanza_luz
        @matanza_luz = Sprite.new(@viewport1)
        @matanza_luz.bitmap = RPG::Cache.picture(sprintf('acto5_luz%02d', mid))
        @matanza_luz.z = 2500
        @matanza_mid = mid
      end
      @matanza_luz.x = -$game_map.display_x / 4
      @matanza_luz.y = -$game_map.display_y / 4
      @matanza_alarma = Sprite_Alarma.new unless @matanza_alarma
    elsif @matanza_luz
      @matanza_luz.dispose
      @matanza_luz = nil
      @matanza_mid = nil
    end
    @matanza_alarma.update if @matanza_alarma
  end
  def dispose
    @matanza_luz.dispose if @matanza_luz
    @matanza_alarma.dispose if @matanza_alarma
    matanza_ss_dispose
  end
end
