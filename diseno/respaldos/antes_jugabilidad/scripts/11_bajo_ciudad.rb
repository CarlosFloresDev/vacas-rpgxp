# === VACAS: FUENTE VIGENTE ===
# Script: Vacas_BajoCiudad | posición en Scripts.rxdata: 99 (base 0)
# Función: Progreso, combate y pruebas del Acto IV (BajoCiudad).
# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.
# Switches simbólicos: SW_HUD_OCULTO
# Switches con ID literal: 96, 97, 98, 113, 115
# Variables simbólicas: ninguna
# Variables con ID literal: 23, 51, 52, 53, 55, 56
# Los índices calculados y rangos se describen en el código y en docs/sistemas/.
# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).
# === FIN CABECERA ===
# Acto IV: Bajo la ciudad. RGSS1 / Ruby 1.8.
module Vacas
  def self.bajo_ciudad?
    return $game_switches[113] && (17..21).include?($game_map.map_id)
  end
  def self.empezar_acto4
    return unless $game_switches[98]
    unless $game_switches[113]
      $game_switches[113] = true
      $game_switches[115] = true
      $game_variables[51] = $game_switches[96] ? 0 : 1
      $game_variables[52] = 100
      $game_variables[55] = 1
      $game_party.gain_item(30,1)
      $game_party.gain_item(31,2)
    end
    for id in [9,10,11,15,16,23,24,25,26,27,29,30,31,40,90,101]
      $game_switches[id] = false
    end
    $game_system.timer_working = false
    $game_system.menu_disabled = false
    $game_system.save_disabled = true
    $game_player.transparent = false
    $game_temp.player_new_map_id = 17
    $game_temp.player_new_x = 4
    $game_temp.player_new_y = 11
    $game_temp.player_new_direction = 8
    $game_temp.player_transferring = true
    $game_temp.transition_processing = false
  end
  def self.prueba_acto4(pruebas = false)
    prueba_acto3(pruebas)
    for id in [82,83,84,85,86,88,91,95,98,104,105,106]
      $game_switches[id] = true
    end
    $game_switches[96] = !pruebas
    $game_switches[97] = pruebas
    $game_variables[23] = pruebas ? 2 : 1
    $game_party.gain_item(28,1)
    $game_party.gain_item(29,1)
    empezar_acto4
    $game_temp.player_transferring = false
    $game_map.setup(17)
    $game_player.moveto(4,11)
    $game_player.turn_up
    $game_map.autoplay
    $game_map.update
  end
  def self.reputacion(n)
    $game_variables[51] = [[-3,$game_variables[51]+n].max,5].min
  end
  def self.recargar
    return false unless $game_party.item_number(31)>0 && $game_variables[52]<100
    $game_party.lose_item(31,1)
    $game_variables[52] = [$game_variables[52]+60,100].min
    $game_switches[115] = true
    return true
  end
  def self.detener_caza
    for id in [120,122,123,125]
      $game_switches[id] = false
    end
    $game_system.timer_working = false
    $game_system.menu_disabled = false
    $game_player.transparent = false
  end
  # Solo avanza en exploracion libre; menus, mensajes y combate no gastan pila.
  def self.actualizar_linterna
    return unless bajo_ciudad?
    return if $game_temp.message_window_showing || $game_system.map_interpreter.running?
    if Input.trigger?(Input::X)
      $game_switches[115] = !$game_switches[115] if $game_variables[52]>0
    end
    recargar if Input.trigger?(Input::Y)
    return if [20,21].include?($game_map.map_id)
    n = $game_variables[56]+1
    $game_variables[56] = n
    if $game_switches[115] && $game_variables[52]>0
      $game_variables[52] -= 1 if n%120==0
      $game_switches[115] = false if $game_variables[52]<=0
    elsif n%240==0
      self.veneno = [96,self.veneno+1].min
    end
  end
  class << self
    alias bajo_tareas_antes tareas
    def tareas
      return bajo_tareas_antes unless $game_switches[113]
      s=$game_switches
      return [["Pacto sellado. Acto V: matadero nocturno.",false]] if s[132]
      return [["Hablar con la Guernsey. Elegir el pacto.",false]] if s[131]
      return [["Camara: escuchar a la Guernsey.",false]] if s[118]
      return [["Valvulas: cerrar retorno, abrir descarga.",false]] if s[119]
      return [["Buscar rueda en los tuneles. Altar al este.",false]]
    end
  end
end
class Scene_Title
  alias bajo_nueva_partida command_new_game
  def command_new_game
    salto = Vacas_HD.key?(:alt)
    pruebas = Vacas_HD.key?(:shift)
    bajo_nueva_partida
    Vacas.prueba_acto4(pruebas) if salto
  end
end
class Scene_Map
  alias bajo_update_antes update
  def update
    bajo_update_antes
    Vacas.actualizar_linterna if $scene.is_a?(Scene_Map)
  end
end
class Interpreter
  alias bajo_susto_antes susto
  def susto(id)
    return bajo_susto_antes(id) unless [10,11].include?(id)
    flag = id==10 ? 136 : 137
    return true if $game_switches[flag]
    $game_switches[flag] = true
    $game_screen.vacas_susto(id)
    @wait_count=24
    return true
  end
  def bajo_captura
    $game_variables[53] += 1
    subir_veneno_tope(8,96)
    # Nada unico se pierde. La caza queda resuelta para evitar bucles frustrantes.
    $game_switches[$game_map.map_id==19 ? 124 : 121] = true
    Vacas.detener_caza
    return true
  end
  def bajo_tension(n)
    subir_veneno_tope(n,96)
    return true
  end
end
# Mascara con radio cercano y cono orientado; no ocupa Pictures 98 ni toca tono.
# Solo cinco bitmaps compartidos por spriteset, se liberan al transferir.
class Sprite_Linterna < Sprite
  def initialize(viewport = nil)
    super(viewport)
    self.z=2900
    @mascaras={}
    @direccion=nil
  end
  def mascara(d)
    return @mascaras[d] if @mascaras[d]
    b=Bitmap.new(Vacas_HD.w*2,Vacas_HD.h*2)
    b.fill_rect(0,0,Vacas_HD.w*2,Vacas_HD.h*2,Color.new(1,8,7,218))
    # Crear agujero por franjas horizontales; no hay get_pixel por fotograma.
    for y in -190..190
      (-190).step(190,4) do |x|
        dist=Math.sqrt(x*x+y*y)
        near=d==0 ? 35 : 57
        forward = d==2 ? y : d==8 ? -y : d==6 ? x : -x
        cross = (d==2 || d==8) ? x.abs : y.abs
        beam=d!=0 && forward>0 && forward<182 && cross<forward*0.52+12
        next unless dist<near || beam
        edge=dist<near ? dist/near : [forward/182.0,cross/(forward*0.52+12)].max
        a=[0,((edge-0.45)*330).to_i].max
        a=[218,a].min
        b.fill_rect(Vacas_HD.w+x,Vacas_HD.h+y,4,1,Color.new(1,8,7,a))
      end
    end
    @mascaras[d]=b
    return b
  end
  def update
    super
    on=Vacas.bajo_ciudad? && ![20,21].include?($game_map.map_id)
    self.visible=on
    return unless on
    d=$game_switches[115] && $game_variables[52]>0 ? $game_player.direction : 0
    if @direccion!=d
      self.bitmap=mascara(d)
      @direccion=d
    end
    self.x=$game_player.screen_x-Vacas_HD.w
    self.y=$game_player.screen_y-18-Vacas_HD.h
  end
  def dispose
    for b in @mascaras.values
      b.dispose
    end
    super
  end
end
class Sprite_Bateria < Sprite
  def initialize
    super(nil)
    self.bitmap=Bitmap.new(330,42)
    self.x=124; self.y=Vacas_HD.bottom(42); self.z=4000
    @estado=nil
  end
  def update
    super
    self.visible=Vacas.bajo_ciudad? && !$game_switches[Vacas::SW_HUD_OCULTO]
    return unless self.visible
    a=[$game_variables[52],$game_variables[51],$game_switches[115],$game_party.item_number(31)]
    return if a==@estado
    @estado=a
    b=self.bitmap;b.clear;b.font.size=13
    b.font.color=Color.new(196,209,172)
    b.draw_text(0,0,330,15,"pila #{a[0]}% | manada #{a[1]} | repuestos #{a[3]}")
    b.fill_rect(0,17,96,5,Color.new(22,35,29,220))
    b.fill_rect(1,18,a[0]*94/100,3,Color.new(148,175,108))
    b.draw_text(104,13,226,18,"A: luz / S: recargar")
  end
  def dispose
    self.bitmap.dispose
    super
  end
end
class Spriteset_Map
  alias bajo_ss_update update
  alias bajo_ss_dispose dispose
  def update
    bajo_ss_update
    if Vacas.bajo_ciudad?
      @bajo_luz=Sprite_Linterna.new(@viewport1) unless @bajo_luz
      @bajo_pila=Sprite_Bateria.new unless @bajo_pila
    end
    @bajo_luz.update if @bajo_luz
    @bajo_pila.update if @bajo_pila
  end
  def dispose
    @bajo_luz.dispose if @bajo_luz
    @bajo_pila.dispose if @bajo_pila
    bajo_ss_dispose
  end
end
class Scene_Load
  alias bajo_read_save read_save_data
  def read_save_data(file)
    bajo_read_save(file)
    unless $game_system.instance_variable_get(:@bajo_mapas_v1)
      x,y=$game_player.x,$game_player.y
      $game_map.setup($game_map.map_id)
      $game_player.moveto(x,y)
      $game_player.refresh
      $game_system.instance_variable_set(:@bajo_mapas_v1,true)
    end
  end
end
