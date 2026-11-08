#==============================================================================
# Vacas_VN -- RGSS1 / Ruby 1.8. Mensajes compatibles con opciones y variables.
# \P[steven_miedo] \L / \R \D[1] \NOMBRE[Steven]
# C revela el texto; una segunda pulsacion avanza. No consume decisiones.
#==============================================================================
$KCODE = 'u'
class Window_Message
  alias vacas_vn_initialize initialize
  def initialize
    vacas_vn_initialize
    self.x = 16
    self.width = 608
    self.contents.dispose
    self.contents = Bitmap.new(576, 128)
    self.contents.font.name = 'Arial'
    self.contents.font.size = 22
    @vn_bust = Sprite.new
    @vn_bust.z = 9995
    @vn_plate = Sprite.new
    @vn_plate.z = 9999
    @vn_plate.bitmap = Bitmap.new(300, 36)
    @vn_dim = Sprite.new
    @vn_dim.z = 9993
    @vn_dim.bitmap = Bitmap.new(640, 480)
    @vn_dim.bitmap.fill_rect(0, 0, 640, 480, Color.new(0, 0, 0, 125))
    vn_hide
  end
  def vn_hide
    return if @vn_bust == nil
    @vn_bust.visible = false
    @vn_plate.visible = false
    @vn_dim.visible = false
    if @vn_full != nil
      @vn_full.dispose
      @vn_full = nil
    end
    @vn_units = nil
  end
  alias vacas_vn_reset reset_window
  def reset_window
    vacas_vn_reset
    self.x = 16
    self.y = $game_temp.in_battle ? 16 : 312
    self.opacity = 235
    self.back_opacity = 200
  end
  alias vacas_vn_refresh refresh
  def refresh
    vn_hide
    text = ($game_temp.message_text || '').clone
    portrait = nil
    right = false
    dim = false
    name = ''
    text.gsub!(/\\P\[([a-z0-9_]+)\]/i) { portrait = $1; '' }
    text.gsub!(/\\NOMBRE\[([^\]]+)\]/i) { name = $1; '' }
    text.gsub!(/\\D\[([01])\]/i) { dim = ($1 == '1'); '' }
    text.gsub!(/\\R\b/i) { right = true; '' }
    text.gsub!(/\\L\b/i) { right = false; '' }
    $game_temp.message_text = text.clone
    vacas_vn_refresh
    # Bustos por encima del mapa, debajo de la caja. Cache posee su bitmap.
    if portrait != nil
      @vn_bust.bitmap = RPG::Cache.picture('retrato_' + portrait)
      @vn_bust.x = right ? 400 : 0
      @vn_bust.y = 20
      @vn_bust.visible = true
    end
    @vn_dim.visible = dim
    unless name == ''
      b = @vn_plate.bitmap
      b.clear
      b.fill_rect(0, 0, 300, 36, Color.new(17, 22, 22, 235))
      b.fill_rect(0, 32, 300, 3, Color.new(139, 111, 72))
      b.font.name = 'Arial'
      b.font.size = 22
      b.font.color = Color.new(222, 207, 165)
      b.draw_text(12, 0, 280, 32, name)
      @vn_plate.x = right ? 324 : 16
      @vn_plate.y = $game_temp.in_battle ? 176 : self.y - 36
      @vn_plate.visible = true
    end
    # El mensaje original ya expandio variables y colores. Copiamos el resultado
    # y revelamos cada glifo UTF-8, sin alterar la logica nativa de opciones.
    return if $game_temp.num_input_variable_id > 0
    @vn_choice_active = self.active
    self.active = false
    plain = text.clone
    begin
      last = plain.clone
      plain.gsub!(/\\[Vv]\[([0-9]+)\]/) { $game_variables[$1.to_i].to_s }
    end until last == plain
    plain.gsub!(/\\[Nn]\[([0-9]+)\]/) { $game_actors[$1.to_i].name }
    plain.gsub!(/\\[Cc]\[[0-9]+\]/, '')
    plain.gsub!(/\\[Gg]/, '')
    plain.gsub!(/\\\\/) { '\\' }
    @vn_full = Bitmap.new(self.contents.width, self.contents.height)
    @vn_full.blt(0, 0, self.contents, self.contents.rect)
    self.contents.clear
    @vn_units = []
    x = 0
    y = 0
    plain.scan(/./m).each do |ch|
      if ch == "\n"
        x = 0
        y += 32
      else
        w = self.contents.text_size(ch).width
        @vn_units.push(Rect.new(x, y, w + 4, 32)) if y < 128
        x += w
      end
    end
    @vn_tick = 0
  end
  alias vacas_vn_update update
  def update
    if @vn_units != nil and @vn_units.size > 0 and !@fade_in
      # Actualiza la seleccion base sin dejar que C cierre un mensaje a medias.
      super
      self.pause = false
      @vn_tick += 1
      if Input.trigger?(Input::C) or Input.press?(Input::A)
        self.contents.blt(0, 0, @vn_full, @vn_full.rect)
        @vn_units.clear
      elsif @vn_tick % 2 == 0
        r = @vn_units.shift
        self.contents.blt(r.x, r.y, @vn_full, r)
      end
      self.active = @vn_choice_active if @vn_units.empty?
      return
    end
    vacas_vn_update
  end
  alias vacas_vn_terminate terminate_message
  def terminate_message
    vn_hide
    vacas_vn_terminate
  end
  alias vacas_vn_dispose dispose
  def dispose
    vacas_vn_dispose
    @vn_plate.bitmap.dispose
    @vn_dim.bitmap.dispose
    @vn_bust.dispose
    @vn_plate.dispose
    @vn_dim.dispose
  end
end
