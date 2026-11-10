# === VACAS: FUENTE VIGENTE ===
# Script: Vacas_Nucleo | posición en Scripts.rxdata: 89 (base 0)
# Función: Constantes, estado y comandos de eventos del juego.
# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.
# Switches simbólicos: SW_ACTO2, SW_ESCONDIDO2, SW_FICHADO, SW_HUD_OCULTO, SW_MATADERO, SW_MONO, SW_NOCHE2, SW_PATRULLA_CAM, SW_PATRULLA_OFI, SW_PIEZA, SW_PILLADO_CRIPPS, SW_SIN_EFECTOS, SW_SUELDO_DADO, SW_TURNO3
# Switches con ID literal: 9
# Variables simbólicas: VAR_AUX, VAR_CANAL, VAR_ETAPA, VAR_FASE, VAR_GUERNSEY, VAR_HUELLA, VAR_PIEZA, VAR_PIEZAS, VAR_RESULTADO, VAR_SUELDO_HOY, VAR_SUELDO_TOTAL, VAR_TURNO, VAR_VECES_TELE, VAR_VENENO
# Variables con ID literal: 2, 17
# Los índices calculados y rangos se describen en el código y en docs/sistemas/.
# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).
# === FIN CABECERA ===
#==============================================================================
# ** Vacas - Nucleo
#------------------------------------------------------------------------------
#  Constantes del juego, ajustes del sistema en tiempo de ejecucion y
#  comandos de ayuda para los eventos (subir_veneno, bajar_veneno...).
#  Compatible con RGSS1 (Ruby 1.8).
#==============================================================================

module Vacas
  # --- Variables ---
  VAR_VENENO     = 1   # 0..100
  VAR_ETAPA      = 2
  VAR_CANAL      = 3
  VAR_VECES_TELE = 4
  VAR_AUX        = 5
  # --- Interruptores ---
  SW_HUD_OCULTO  = 15
  SW_SIN_EFECTOS = 16
  # --- Acto II ---
  SW_ACTO2       = 22
  SW_MATADERO    = 23
  SW_FICHADO     = 24
  SW_MONO        = 25
  SW_PATRULLA_CAM = 26
  SW_NOCHE2      = 27
  SW_SUELDO_DADO = 28
  SW_PATRULLA_OFI = 29
  SW_ESCONDIDO2  = 30
  SW_PILLADO_CRIPPS = 31
  SW_PIEZA       = 40
  SW_TURNO3      = 43
  VAR_TURNO      = 7
  VAR_FASE       = 8
  VAR_SUELDO_HOY = 9
  VAR_SUELDO_TOTAL = 10
  VAR_GUERNSEY   = 11
  VAR_RESULTADO  = 12
  VAR_PIEZAS     = 13
  VAR_PIEZA      = 14
  VAR_HUELLA     = 15
  VENENO_MAX     = 100
  # --- Graficos propios ---
  WINDOWSKIN = "vacas_ventana"
  TITULO     = "vacas_titulo"
  GAMEOVER   = "vacas_gameover"
  #--------------------------------------------------------------------------
  # Ajusta datos de System.rxdata que el MCP no puede editar
  #--------------------------------------------------------------------------
  def self.ajustar_sistema
    return if $data_system == nil
    $data_system.party_members = [1]
    $data_system.title_name    = TITULO
    $data_system.gameover_name = GAMEOVER
    $data_system.windowskin_name = WINDOWSKIN
    $data_system.title_bgm = RPG::AudioFile.new("058-Slow01", 80, 80)
    $data_system.gameover_me = RPG::AudioFile.new("016-Shock01", 90, 70)
    w = $data_system.words
    w.gold = "monedas"
    w.item = "Objetos"
    w.hp = "Salud"
    w.sp = "Aliento"
  end
  #--------------------------------------------------------------------------
  def self.veneno
    return 0 if $game_variables == nil
    return $game_variables[VAR_VENENO]
  end
  # La huella (variable 15) es un suelo: lo que has hecho ya no baja.
  def self.huella
    return 0 if $game_variables == nil
    return $game_variables[VAR_HUELLA]
  end
  def self.veneno=(v)
    v = 0 if v < 0
    v = huella if v < huella
    v = VENENO_MAX if v > VENENO_MAX
    $game_variables[VAR_VENENO] = v
    $game_map.need_refresh = true if $game_map != nil
  end
end

#==============================================================================
# ** Game_System - ventana oscura siempre
#==============================================================================
class Game_System
  alias vacas_gs_initialize initialize
  def initialize
    vacas_gs_initialize
    @windowskin_name = Vacas::WINDOWSKIN
  end
end

#==============================================================================
# ** Interpreter - comandos para usar en "Llamar script"
#   Todos devuelven true para que el interprete no repita el comando.
#==============================================================================
class Interpreter
  def subir_veneno(n)
    Vacas.veneno = Vacas.veneno + n
    fuerza = 40 + n * 6
    fuerza = 200 if fuerza > 200
    $game_screen.start_flash(Color.new(150, 0, 0, fuerza), 12)
    $game_screen.start_shake(2 + n / 10, 8, 10 + n)
    $game_system.se_play(RPG::AudioFile.new("140-Darkness03", 70, 60))
    $vacas_hud_pulso = 40
    return true
  end
  def bajar_veneno(n)
    Vacas.veneno = Vacas.veneno - n
    $game_screen.start_flash(Color.new(200, 220, 255, 50), 20)
    $vacas_hud_pulso = 20
    return true
  end
  def veneno_al_maximo?
    return Vacas.veneno >= Vacas::VENENO_MAX
  end
  # Sube el veneno sin pasar de un tope (para escenas que no deben matar)
  def subir_veneno_tope(n, tope)
    n = tope - Vacas.veneno if Vacas.veneno + n > tope
    n = 0 if n < 0
    subir_veneno(n)
    return true
  end
  # Marca permanente: el veneno ya no baja de aqui
  def huella(n)
    $game_variables[Vacas::VAR_HUELLA] = n if $game_variables[Vacas::VAR_HUELLA] < n
    Vacas.veneno = Vacas.veneno
    return true
  end
  def poner_mono(si)
    nombre = si ? "vacas_steven_mono" : "vacas_steven"
    $game_actors[1].set_graphic(nombre, 0, "", 0)
    $game_player.refresh
    $game_switches[Vacas::SW_MONO] = si
    $game_map.need_refresh = true
    return true
  end
  # Paga el sueldo: monedas visibles y variables de sueldo
  def cobrar(n)
    $game_party.gain_gold(n)
    $game_variables[Vacas::VAR_SUELDO_HOY] += n
    $game_variables[Vacas::VAR_SUELDO_TOTAL] += n
    return true
  end
  # Madre se lleva el sueldo. Si guardar es true, Steven esconde una moneda.
  def entregar_sueldo(guardar)
    g = $game_party.gold
    g -= 1 if guardar and g > 0
    $game_party.lose_gold(g)
    $game_switches[Vacas::SW_SUELDO_DADO] = true
    $game_map.need_refresh = true
    return true
  end
  # Prepara el siguiente turno (al dormir)
  def nuevo_turno
    for i in [Vacas::SW_FICHADO, Vacas::SW_MONO, Vacas::SW_PATRULLA_CAM, Vacas::SW_NOCHE2,
              Vacas::SW_SUELDO_DADO, Vacas::SW_PATRULLA_OFI, Vacas::SW_ESCONDIDO2,
              Vacas::SW_PILLADO_CRIPPS, Vacas::SW_PIEZA]
      $game_switches[i] = false
    end
    $game_variables[Vacas::VAR_TURNO] += 1
    $game_variables[Vacas::VAR_FASE] = 0
    $game_variables[Vacas::VAR_SUELDO_HOY] = 0
    $game_variables[Vacas::VAR_PIEZAS] = 0
    $game_variables[Vacas::VAR_PIEZA] = 0
    $game_switches[Vacas::SW_MATADERO] = true
    $game_switches[Vacas::SW_TURNO3] = ($game_variables[Vacas::VAR_TURNO] == 3)
    $game_map.need_refresh = true
    return true
  end
  # Perro: una caricia que cura, una vez por noche
  def perro_esta_noche?
    return $game_variables[17] < $game_variables[Vacas::VAR_TURNO]
  end
  def perro_hecho
    $game_variables[17] = $game_variables[Vacas::VAR_TURNO]
    return true
  end
  def fase(n)
    $game_variables[Vacas::VAR_FASE] = n
    $game_map.need_refresh = true
    return true
  end
  def fin_del_acto
    $scene = Scene_FinActo.new(1)
    return true
  end
  def fin_del_acto2
    $scene = Scene_FinActo.new(2)
    return true
  end
end

module Vacas
  # Arranque del Acto II (al terminar el Acto I o desde la prueba del titulo)
  def self.empezar_acto2
    $game_switches[SW_HUD_OCULTO] = false
    $game_switches[SW_SIN_EFECTOS] = false
    $game_switches[SW_ACTO2] = true
    $game_switches[SW_MATADERO] = true
    $game_variables[VAR_TURNO] = 1
    $game_variables[VAR_FASE] = 0
    $game_screen.start_tone_change(Tone.new(-255, -255, -255, 0), 0)
    $game_screen.weather(0, 0, 0)
    $game_temp.player_new_map_id = 5
    $game_temp.player_new_x = 15
    $game_temp.player_new_y = 19
    $game_temp.player_new_direction = 8
    $game_temp.player_transferring = true
    $game_temp.transition_processing = false
    $game_system.menu_disabled = false
  end
  # Atajo de prueba: Mayus + Nueva partida empieza directamente en el Acto II
  def self.prueba_acto2
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 18, 19, 20]
      $game_switches[i] = true
    end
    $game_switches[9] = false
    $game_variables[VAR_VENENO] = 30
    $game_variables[2] = 7
    $game_party.gain_item(7, 1)
    $game_self_switches[[1, 1, "A"]] = true
    $game_system.save_disabled = true
    empezar_acto2
    $game_temp.player_transferring = false
    $game_map.setup(5)
    $game_player.moveto(15, 19)
    $game_player.turn_up
    $game_player.refresh
    $game_map.autoplay
    $game_map.update
  end
end
