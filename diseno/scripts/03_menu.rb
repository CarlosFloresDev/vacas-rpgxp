# === VACAS: FUENTE VIGENTE ===
# Script: Vacas_Menu | posición en Scripts.rxdata: 91 (base 0)
# Función: Menú, estado y objetos del jugador.
# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.
# Switches simbólicos: ninguno
# Switches con ID literal: ninguno
# Variables simbólicas: ninguna
# Variables con ID literal: 7, 8, 13
# Los índices calculados y rangos se describen en el código y en docs/sistemas/.
# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).
# === FIN CABECERA ===
#==============================================================================
# ** Vacas - Menu de terror
#------------------------------------------------------------------------------
#  Menu reducido: Objetos / Guardar (solo con la tele) / Salir, con una
#  lista de tareas pendientes. Sin estado, equipo ni habilidades.
#==============================================================================

module Vacas
  # Devuelve [[texto, hecho], ...] segun los interruptores de la historia
  def self.tareas
    s = $game_switches
    lista = []
    return tareas_acto2 if s[22]
    if s[14]
      lista.push(["Ya tienes trabajo.", true])
    elsif s[13]
      lista.push(["Bajar a la calle: el camión del matadero.", false])
    elsif s[10]
      lista.push(["Esconderte. Ya viene.", false])
    elsif s[9]
      lista.push(["Ir a dormir.", false])
    elsif s[2]
      lista.push(["Dar de comer a Perro.", s[3]])
      lista.push(["Llevarle el jarabe a madre.", s[4]])
      lista.push(["Comprar carne en la carnicería.", s[5]])
      lista.push(["Darle la carne a madre.", s[6]])
      lista.push(["Leer los anuncios del portal.", s[7]])
      if s[3] and s[4] and s[6] and s[7]
        lista.push(["Volver con madre.", false])
      end
    else
      lista.push(["Ir a ver qué quiere madre.", false])
    end
    return lista
  end
  # Acto II: segun turno (variable 7) y fase (variable 8)
  def self.tareas_acto2
    s = $game_switches
    t = $game_variables[7]
    f = $game_variables[8]
    lista = []
    if s[27]
      lista.push(["Volver a casa: el 3ºB.", false]) if $game_map.map_id == 3 and !s[28]
      lista.push(["Darle el sueldo a madre.", s[28]])
      lista.push(["Acostarte. Mañana hay turno.", false]) if s[28]
      return lista
    end
    lista.push(["Fichar a la entrada.", s[24]])
    lista.push(["Ponerte el mono en el vestuario.", s[25]]) if s[24]
    return lista unless s[25]
    case t
    when 1
      lista.push(["La cadena: el puesto de la cinta.", f > 3])
      lista.push(["Traer la manguera del pasillo de mantenimiento.", f > 4]) if f >= 4
      lista.push(["Devolverle la manguera a Cripps.", f > 5]) if f >= 5
    when 2
      lista.push(["La cadena: el puesto de corte.", f > 3])
      lista.push(["Llevar piezas a las cámaras (" + $game_variables[13].to_s + "/3).", f > 4]) if f >= 4
      lista.push(["La rejilla del pasillo de mantenimiento.", f > 5]) if f >= 5
      lista.push(["El libro de Cripps, en su oficina.", f > 6]) if f >= 6
      lista.push(["Volver a la rejilla.", f > 7]) if f >= 7
    when 3
      lista.push(["Hablar con Cripps en la cadena.", f > 3])
      lista.push(["Traer la vaca del corral del fondo.", f > 4]) if f >= 4
      lista.push(["El cajón.", f > 5]) if f >= 5
    end
    lista.push(["Fichar la salida.", false]) if f >= 9
    return lista
  end
end

class Window_Tareas < Window_Base
  def initialize
    super(200, Vacas_HD.y(64), 420, Vacas_HD.y(288))
    self.contents = Bitmap.new(width - 32, height - 32)
    refresh
  end
  def refresh
    self.contents.clear
    self.contents.font.color = system_color
    self.contents.draw_text(4, 0, 380, 32, "Pendiente")
    y = 40
    for t in Vacas.tareas
      if t[1]
        self.contents.font.color = disabled_color
        marca = "x "
      else
        self.contents.font.color = normal_color
        marca = "- "
      end
      self.contents.draw_text(4, y, 380, 28, marca + t[0])
      y += 30
    end
  end
end

class Window_Lugar < Window_Base
  def initialize
    super(200, Vacas_HD.y(352), 420, Vacas_HD.y(64))
    self.contents = Bitmap.new(width - 32, height - 32)
    self.contents.font.color = normal_color
    nombre = ""
    infos = load_data("Data/MapInfos.rxdata")
    if infos[$game_map.map_id] != nil
      nombre = infos[$game_map.map_id].name
    end
    self.contents.draw_text(4, 0, 380, 32, nombre)
  end
end

class Scene_Menu
  def initialize(menu_index = 0)
    @menu_index = menu_index
  end
  def main
    @spriteset = Spriteset_Map.new
    @command_window = Window_Command.new(160, ["Objetos", "Guardar", "Salir"])
    @command_window.x = 20
    @command_window.y = 64
    @command_window.index = @menu_index
    @command_window.disable_item(1)
    @tareas_window = Window_Tareas.new
    @lugar_window = Window_Lugar.new
    @gold_window = Window_Gold.new
    @gold_window.x = 20
    @gold_window.y = Vacas_HD.y(352)
    @aviso_window = Window_Help.new
    @aviso_window.visible = false
    Graphics.transition
    loop do
      Graphics.update
      Input.update
      update
      break if $scene != self
    end
    Graphics.freeze
    @command_window.dispose
    @tareas_window.dispose
    @lugar_window.dispose
    @gold_window.dispose
    @aviso_window.dispose
    @spriteset.dispose
  end
  def update
    @command_window.update
    @aviso_window.update
    if Input.trigger?(Input::B)
      $game_system.se_play($data_system.cancel_se)
      $scene = Scene_Map.new
      return
    end
    if Input.trigger?(Input::C)
      case @command_window.index
      when 0
        $game_system.se_play($data_system.decision_se)
        $scene = Scene_Item.new
      when 1
        $game_system.se_play($data_system.buzzer_se)
        @aviso_window.set_text("Solo puedes guardar delante de la tele.", 1)
        @aviso_window.visible = true
      when 2
        $game_system.se_play($data_system.decision_se)
        $scene = Scene_End.new
      end
    end
  end
end

class Scene_End
  def main
    @command_window = Window_Command.new(220, ["Volver al título", "Cerrar el juego", "Cancelar"])
    @command_window.x = Vacas_HD.w / 2 - @command_window.width / 2
    @command_window.y = Vacas_HD.h / 2 - @command_window.height / 2
    Graphics.transition
    loop do
      Graphics.update
      Input.update
      update
      break if $scene != self
    end
    Graphics.freeze
    @command_window.dispose
    if $scene.is_a?(Scene_Title)
      Graphics.transition
      Graphics.freeze
    end
  end
  def command_cancel
    $game_system.se_play($data_system.decision_se)
    $scene = Scene_Menu.new(2)
  end
  def update
    @command_window.update
    if Input.trigger?(Input::B)
      $game_system.se_play($data_system.cancel_se)
      $scene = Scene_Menu.new(2)
      return
    end
    if Input.trigger?(Input::C)
      case @command_window.index
      when 0
        command_to_title
      when 1
        command_shutdown
      when 2
        command_cancel
      end
    end
  end
end

# Textos de guardar / cargar en castellano
class Scene_Save < Scene_File
  def initialize
    super("¿En qué hueco quieres guardar? La tele zumba.")
  end
end
class Scene_Load < Scene_File
  alias vacas_load_initialize initialize
  def initialize
    vacas_load_initialize
    @help_text = "¿Qué partida quieres cargar?"
  end
  alias vacas_read_save_data read_save_data
  def read_save_data(file)
    vacas_read_save_data(file)
    $game_system.windowskin_name = Vacas::WINDOWSKIN
  end
end
class Window_SaveFile < Window_Base
  alias vacas_wsf_refresh refresh
  def refresh
    vacas_wsf_refresh
    self.contents.fill_rect(4, 0, 160, 32, Color.new(0, 0, 0, 0))
    self.contents.font.color = normal_color
    self.contents.draw_text(4, 0, 160, 32, "Partida #{@file_index + 1}")
  end
end

# Recuerda que objeto se ha usado: el evento comun 1 lee las notas segun
# $vacas_ultimo_objeto (el MCP no permite crear mas eventos comunes).
$vacas_ultimo_objeto = 0
class Scene_Item
  alias vacas_item_update_item update_item
  def update_item
    if Input.trigger?(Input::C) and @item_window.item != nil
      $vacas_ultimo_objeto = @item_window.item.id
    end
    vacas_item_update_item
  end
end
