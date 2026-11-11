# === VACAS: FUENTE VIGENTE ===
# Script: Vacas_Veneno | posición en Scripts.rxdata: 90 (base 0)
# Función: Efectos y presentación del veneno y la cordura.
# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.
# Switches simbólicos: SW_HUD_OCULTO, SW_SIN_EFECTOS
# Switches con ID literal: ninguno
# Variables simbólicas: ninguna
# Variables con ID literal: ninguna
# Los índices calculados y rangos se describen en el código y en docs/sistemas/.
# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).
# === FIN CABECERA ===
#==============================================================================
# ** Vacas - Veneno (cordura)
#------------------------------------------------------------------------------
#  Indicador discreto en pantalla y efectos (tono, temblor, destellos)
#  que crecen con la variable 1 "Veneno" (0..100).
#==============================================================================

$vacas_hud_pulso = 0

class Sprite_Veneno < Sprite
  ANCHO = 96
  def initialize
    super(nil)
    self.bitmap = Bitmap.new(ANCHO + 8, 22)
    self.x = 14
    self.y = Vacas_HD.h - 34
    self.z = 4000
    @valor = -1
    @contador = 0
    refrescar
  end
  def dispose
    self.bitmap.dispose if self.bitmap != nil
    super
  end
  def refrescar
    v = Vacas.veneno
    @valor = v
    b = self.bitmap
    b.clear
    b.font.size = 13
    b.font.color = Color.new(190, 170, 140, 255)
    b.draw_text(0, 0, ANCHO, 12, "veneno")
    # marco
    b.fill_rect(0, 14, ANCHO, 6, Color.new(0, 0, 0, 200))
    b.fill_rect(1, 15, ANCHO - 2, 4, Color.new(40, 32, 26, 220))
    largo = (ANCHO - 2) * v / Vacas::VENENO_MAX
    if largo > 0
      r = 150 + v
      r = 255 if r > 255
      g = 120 - v
      g = 10 if g < 10
      b.fill_rect(1, 15, largo, 4, Color.new(r, g, 20, 255))
    end
  end
  def update
    super
    refrescar if @valor != Vacas.veneno
    oculto = ($game_switches != nil and $game_switches[Vacas::SW_HUD_OCULTO])
    @contador += 1
    base = 110 + Vacas.veneno
    if Vacas.veneno >= 50
      # latido: mas rapido cuanto mas veneno
      periodo = 70 - Vacas.veneno / 2
      periodo = 20 if periodo < 20
      base += 50 if (@contador % periodo) < 6
    end
    if $vacas_hud_pulso > 0
      $vacas_hud_pulso -= 1
      base = 255 if ($vacas_hud_pulso / 4) % 2 == 0
    end
    base = 255 if base > 255
    if oculto
      self.opacity = 0
    else
      self.opacity = base
    end
  end
end

#==============================================================================
# ** Spriteset_Map - tono extra y efectos aleatorios segun el veneno
#==============================================================================
class Spriteset_Map
  alias vacas_ssm_initialize initialize
  def initialize
    @vacas_hud = Sprite_Veneno.new
    vacas_ssm_initialize
  end
  alias vacas_ssm_dispose dispose
  def dispose
    @vacas_hud.dispose
    vacas_ssm_dispose
  end
  alias vacas_ssm_update update
  def update
    vacas_ssm_update
    return if @vacas_hud == nil
    @vacas_hud.update
    v = Vacas.veneno
    t = $game_screen.tone
    # el veneno amarillea, apaga el azul y quita color
    rr = t.red + v * 0.30
    gg = t.green - v * 0.15
    bb = t.blue - v * 0.45
    gr = t.gray + v * 1.4
    gr = 255 if gr > 255
    @viewport1.tone = Tone.new(rr, gg, bb, gr)
    vacas_efectos(v)
  end
  def vacas_efectos(v)
    return if $game_switches[Vacas::SW_SIN_EFECTOS]
    return if $game_temp.message_window_showing
    if v >= 35 and rand(900 - v * 6) == 0
      $game_screen.start_shake(1 + v / 35, 5, 6 + v / 10)
    end
    if v >= 55 and rand(1100 - v * 8) == 0
      $game_screen.start_flash(Color.new(120, 0, 0, 30 + v), 4 + v / 12)
    end
    if v >= 75 and rand(1600 - v * 10) == 0
      $game_system.se_play(RPG::AudioFile.new("040-Knock01", 60, 70))
      $game_screen.start_flash(Color.new(0, 0, 0, 160), 10)
    end
  end
end
