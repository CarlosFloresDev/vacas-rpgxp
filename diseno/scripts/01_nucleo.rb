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
  def self.veneno=(v)
    v = 0 if v < 0
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
  def fin_del_acto
    $scene = Scene_FinActo.new
    return true
  end
end
