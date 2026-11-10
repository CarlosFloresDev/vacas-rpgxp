# === VACAS: FUENTE VIGENTE ===
# Script: Vacas_Pantallas | posición en Scripts.rxdata: 92 (base 0)
# Función: Título, derrota, pantallas y entradas de prueba.
# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.
# Switches simbólicos: ninguno
# Switches con ID literal: ninguno
# Variables simbólicas: ninguna
# Variables con ID literal: ninguna
# Los índices calculados y rangos se describen en el código y en docs/sistemas/.
# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).
# === FIN CABECERA ===
#==============================================================================
# ** Vacas - Pantallas
#------------------------------------------------------------------------------
#  Aviso de contenido al arrancar, titulo en castellano, fin del acto y
#  game over propio.
#==============================================================================

#------------------------------------------------------------------------------
# Utilidad: texto centrado sobre negro
#------------------------------------------------------------------------------
module Vacas
  def self.sprite_texto(lineas, y0, alto = 30, tam = 22, color = nil)
    s = Sprite.new
    s.bitmap = Bitmap.new(640, 480)
    s.bitmap.font.size = tam
    c = color
    if c.nil?
      c = Color.new(210, 200, 180)
    end
    s.bitmap.font.color = c
    y = y0
    for l in lineas
      s.bitmap.draw_text(0, y, 640, alto, l, 1)
      y += alto
    end
    return s
  end
end

#==============================================================================
# ** Scene_Aviso - aviso de contenido (solo al arrancar el juego)
#==============================================================================
class Scene_Aviso
  def main
    @fondo = Sprite.new
    @fondo.bitmap = Bitmap.new(640, 480)
    @fondo.bitmap.fill_rect(0, 0, 640, 480, Color.new(0, 0, 0))
    @titulo = Vacas.sprite_texto(["AVISO DE CONTENIDO"], 70, 36, 28,
      Color.new(190, 40, 34))
    lineas = [
      "Vacas es un juego de terror psicológico para adultos.",
      "",
      "Contiene maltrato familiar y psicológico, violencia,",
      "sangre, imágenes perturbadoras sobre la carne y los",
      "animales de matadero, y temas de salud mental.",
      "",
      "No contiene escenas sexuales.",
      "",
      "Si en algún momento te hace daño, para. El juego espera."
    ]
    @texto = Vacas.sprite_texto(lineas, 140, 28, 20)
    @pie = Vacas.sprite_texto(["Pulsa Intro para continuar"], 420, 28, 16,
      Color.new(140, 130, 115))
    @pie.opacity = 0
    @espera = 0
    Graphics.transition(40)
    loop do
      Graphics.update
      Input.update
      @espera += 1
      if @espera > 60
        @pie.opacity = 120 + (Graphics.frame_count % 60) * 2
      else
        @pie.opacity = 0
      end
      if @espera > 60 and Input.trigger?(Input::C)
        $scene = Scene_Title.new
      end
      break if $scene != self
    end
    Graphics.freeze
    for s in [@fondo, @titulo, @texto, @pie]
      s.bitmap.dispose
      s.dispose
    end
    Graphics.transition(30)
    Graphics.freeze
  end
end

#==============================================================================
# ** Scene_Title - en castellano y con los graficos propios
#==============================================================================
class Scene_Title
  def main
    if $BTEST
      battle_test
      return
    end
    $data_actors        = load_data("Data/Actors.rxdata")
    $data_classes       = load_data("Data/Classes.rxdata")
    $data_skills        = load_data("Data/Skills.rxdata")
    $data_items         = load_data("Data/Items.rxdata")
    $data_weapons       = load_data("Data/Weapons.rxdata")
    $data_armors        = load_data("Data/Armors.rxdata")
    $data_enemies       = load_data("Data/Enemies.rxdata")
    $data_troops        = load_data("Data/Troops.rxdata")
    $data_states        = load_data("Data/States.rxdata")
    $data_animations    = load_data("Data/Animations.rxdata")
    $data_tilesets      = load_data("Data/Tilesets.rxdata")
    $data_common_events = load_data("Data/CommonEvents.rxdata")
    $data_system        = load_data("Data/System.rxdata")
    Vacas.ajustar_sistema
    $game_system = Game_System.new
    @sprite = Sprite.new
    @sprite.bitmap = RPG::Cache.title($data_system.title_name)
    @command_window = Window_Command.new(200, ["Nueva partida", "Continuar", "Salir"])
    @command_window.back_opacity = 140
    @command_window.x = 320 - @command_window.width / 2
    @command_window.y = 350
    @continue_enabled = false
    for i in 0..3
      if FileTest.exist?("Save#{i+1}.rxdata")
        @continue_enabled = true
      end
    end
    if @continue_enabled
      @command_window.index = 1
    else
      @command_window.disable_item(1)
    end
    $game_system.bgm_play($data_system.title_bgm)
    Audio.me_stop
    Audio.bgs_stop
    Graphics.transition(40)
    loop do
      Graphics.update
      Input.update
      update
      break if $scene != self
    end
    Graphics.freeze
    @command_window.dispose
    @sprite.bitmap.dispose
    @sprite.dispose
  end
end

#==============================================================================
# ** Scene_FinActo - "Fin del Acto I / II"
#   Acto 1: al pulsar Intro sigue en el Acto II (misma partida).
#   Acto 2: vuelve al titulo.
#==============================================================================
class Scene_FinActo
  TEXTOS = {
    1 => ["Fin del Acto I", "El piso", "Acto II: La cadena", "Pulsa Intro para seguir"],
    2 => ["Fin del Acto II", "La cadena", "Acto III: Lucy", "Pulsa Intro para seguir"],
    3 => ["Fin del Acto III", "Lucy", "Acto IV: Bajo la ciudad", "Pulsa Intro para seguir"],
    4 => ["Fin del Acto IV", "Bajo la ciudad", "Acto V: La matanza", "Pulsa Intro para seguir"],
    5 => ["Fin del Acto V", "La matanza", "Acto VI: Rey-dios", "Pulsa Intro para seguir"]
  }
  def initialize(acto = 1)
    @acto = acto
  end
  def main
    Audio.bgm_fade(2000)
    Audio.bgs_fade(2000)
    t = TEXTOS[@acto]
    @fondo = Sprite.new
    @fondo.bitmap = Bitmap.new(640, 480)
    @fondo.bitmap.fill_rect(0, 0, 640, 480, Color.new(0, 0, 0))
    @fin = Vacas.sprite_texto([t[0]], 170, 50, 40, Color.new(170, 30, 26))
    @sub = Vacas.sprite_texto([t[1]], 224, 32, 22)
    @sig = Vacas.sprite_texto([t[2]], 330, 28, 18, Color.new(140, 130, 115))
    @pie = Vacas.sprite_texto([t[3]], 420, 24, 14, Color.new(110, 100, 90))
    for s in [@fin, @sub, @sig, @pie]
      s.opacity = 0
    end
    Graphics.transition(60)
    $game_system.me_play(RPG::AudioFile.new("015-Mystery01", 80, 70))
    @t = 0
    loop do
      Graphics.update
      Input.update
      @t += 1
      @fin.opacity = (@t - 20) * 3 if @t > 20
      @sub.opacity = (@t - 100) * 3 if @t > 100
      @sig.opacity = (@t - 200) * 2 if @t > 200
      @pie.opacity = 60 + (@t % 80) * 2 if @t > 260
      if @t > 260 and Input.trigger?(Input::C)
        if @acto == 1
          Vacas.empezar_acto2
          $scene = Scene_Map.new
        elsif @acto == 2
          Vacas.empezar_acto3
          $scene = Scene_Map.new
        elsif @acto == 3
          Vacas.empezar_acto4
          $scene = Scene_Map.new
        elsif @acto == 4
          Vacas.empezar_acto5
          $scene = Scene_Map.new
        elsif @acto == 5
          Vacas.empezar_acto6
          $scene = Scene_Map.new
        else
          $scene = Scene_Title.new
        end
      end
      break if $scene != self
    end
    Graphics.freeze
    for s in [@fondo, @fin, @sub, @sig, @pie]
      s.bitmap.dispose
      s.dispose
    end
    Graphics.transition(60)
    Graphics.freeze
  end
end

#==============================================================================
# ** Scene_Gameover - usa el grafico propio aunque el sistema no se recargue
#==============================================================================
class Scene_Gameover
  alias vacas_go_main main
  def main
    Vacas.ajustar_sistema
    vacas_go_main
  end
end

#==============================================================================
# ** Scene_Title - atajo de prueba: Mayus + "Nueva partida" = Acto II
#==============================================================================
class Scene_Title
  alias vacas_cng command_new_game
  def command_new_game
    atajo = Input.press?(Input::A)
    vacas_cng
    Vacas.prueba_acto2 if atajo
  end
end
