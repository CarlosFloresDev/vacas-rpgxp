# === VACAS: FUENTE VIGENTE ===
# Script: Vacas_Lucy | posición en Scripts.rxdata: 97 (base 0)
# Función: Progreso, diálogos y pruebas del Acto III (Lucy).
# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.
# Switches simbólicos: ninguno
# Switches con ID literal: 34, 35, 36, 81, 90, 101
# Variables simbólicas: ninguna
# Variables con ID literal: 7, 8, 15, 19, 21
# Los índices calculados y rangos se describen en el código y en docs/sistemas/.
# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).
# === FIN CABECERA ===
# Vacas: Acto III. RGSS1 / Ruby 1.8.
module Vacas
  def self.empezar_acto3
    return unless $game_switches[34]
    $game_switches[81] = true
    for id in [9,10,11,15,16,23,24,25,26,27,29,30,31,40]
      $game_switches[id] = false
    end
    $game_variables[19] = 1 if $game_variables[19] < 1
    $game_system.save_disabled = true
    $game_system.menu_disabled = false
    $game_actors[1].set_graphic('vacas_steven',0,'steven_mente',0)
    $game_player.refresh
    $game_screen.weather(0,0,0)
    $game_temp.player_new_map_id = 12
    $game_temp.player_new_x = 12
    $game_temp.player_new_y = 17
    $game_temp.player_new_direction = 8
    $game_temp.player_transferring = true
    $game_temp.transition_processing = false
  end
  def self.prueba_acto3(resistir = false)
    prueba_acto2
    for id in [28,34,39,43,55]
      $game_switches[id] = true
    end
    $game_switches[35] = !resistir
    $game_switches[36] = resistir
    $game_variables[7] = 3
    $game_variables[8] = 9
    $game_variables[15] = resistir ? 25 : 35
    self.veneno = 40
    $game_party.gain_item(13,1)
    empezar_acto3
    $game_temp.player_transferring = false
    $game_map.setup(12)
    $game_player.moveto(12,17)
    $game_player.turn_up
    $game_map.autoplay
    $game_map.update
  end
  class << self
    alias lucy_tareas_anteriores tareas
    def tareas
      return lucy_tareas_anteriores unless $game_switches[81]
      s = $game_switches
      return [["Acto IV: el colector espera.",false]] if s[98]
      return [["Hablar con Lucy en el laboratorio.",false]] if s[88]
      return [["Comparar las dos muestras y el control.",false]] if s[86]
      return [["Hospital: pedir material a Elena.",false]] if s[85]
      return [["Depósito: riñón del lote sin etiqueta.",false]] if s[84]
      return [["Carnicería: hígado y sal para el control.",false]] if s[83]
      return [["Hablar con Lucy, junto a su mesa.",false]]
    end
  end
end
class Scene_Title
  alias lucy_nueva_partida command_new_game
  def command_new_game
    salto = Input.press?(Input::CTRL)
    resistencia = Input.press?(Input::A)
    lucy_nueva_partida
    Vacas.prueba_acto3(resistencia) if salto
  end
end
class Interpreter
  alias lucy_susto_anterior susto
  def susto(id)
    return lucy_susto_anterior(id) unless [8,9].include?(id)
    flag = id == 8 ? 99 : 100
    return true if $game_switches[flag]
    $game_switches[flag] = true
    $game_screen.vacas_susto(id)
    @wait_count = 24
    return true
  end
  def lucy_tension(n)
    # La investigación nunca impide continuar por acumular veneno.
    subir_veneno_tope(n,96)
    return true
  end
  def lucy_captura
    $game_variables[21] += 1
    lucy_tension(8)
    $game_switches[90] = false
    $game_switches[101] = false
    $game_system.timer_working = false
    $game_player.transparent = false
    $game_system.menu_disabled = false
    return true
  end
end
# Recargar mapas antiguos también si ya pasaron la migración del Acto II.
class Scene_Load
  alias lucy_read_save_data read_save_data
  def read_save_data(file)
    lucy_read_save_data(file)
    unless $game_system.instance_variable_get(:@lucy_mapas_v1)
      x,y = $game_player.x,$game_player.y
      $game_map.setup($game_map.map_id)
      $game_player.moveto(x,y)
      $game_player.refresh
      $game_system.instance_variable_set(:@lucy_mapas_v1,true)
    end
  end
end
