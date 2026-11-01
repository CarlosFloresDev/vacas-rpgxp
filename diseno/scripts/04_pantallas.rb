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
    s.bitmap.font.color = (color == nil ? Color.new(210, 200, 180) : color)
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
      @pie.opacity = (@espera > 60 ? 120 + (Graphics.frame_count % 60) * 2 : 0)
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
# ** Scene_FinActo - "Fin del Acto I"
#==============================================================================
class Scene_FinActo
  def main
    Audio.bgm_fade(2000)
    Audio.bgs_fade(2000)
    @fondo = Sprite.new
    @fondo.bitmap = Bitmap.new(640, 480)
    @fondo.bitmap.fill_rect(0, 0, 640, 480, Color.new(0, 0, 0))
    @fin = Vacas.sprite_texto(["Fin del Acto I"], 170, 50, 40,
      Color.new(170, 30, 26))
    @sub = Vacas.sprite_texto(["El piso"], 224, 32, 22)
    @sig = Vacas.sprite_texto(["Continuará en el Acto II: La cadena"], 330, 28, 18,
      Color.new(140, 130, 115))
    @fin.opacity = 0
    @sub.opacity = 0
    @sig.opacity = 0
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
      if @t > 260 and Input.trigger?(Input::C)
        $scene = Scene_Title.new
      end
      break if $scene != self
    end
    Graphics.freeze
    for s in [@fondo, @fin, @sub, @sig]
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
