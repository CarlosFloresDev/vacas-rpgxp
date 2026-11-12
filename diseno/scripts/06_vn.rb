# === VACAS: FUENTE VIGENTE ===
# Script: Vacas_VN | posición en Scripts.rxdata: 94 (base 0)
# Función: Diálogos, retratos y presentación de novela visual.
# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.
# Switches simbólicos: ninguno
# Switches con ID literal: ninguno
# Variables simbólicas: ninguna
# Variables con ID literal: ninguna
# Los índices calculados y rangos se describen en el código y en docs/sistemas/.
# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).
# === FIN CABECERA ===
#==============================================================================
# Vacas_VN -- RGSS1 / Ruby 1.8. Mensajes compatibles con opciones y variables.
# \P[steven_miedo] \L / \R \D[1] \NOMBRE[Steven]
# C revela el texto; una segunda pulsacion avanza. No consume decisiones.
#==============================================================================
$KCODE = 'u'
# Una sola normalizacion para dialogos normales y VN, antes de medir/paginar.
module Vacas_MessageText
  def self.normalize(value)
    text=value.to_s.clone
    text.gsub!(/\\\\/) { "\003" } # barra literal, protegida de los controles
    16.times do
      previous=text.clone
      text.gsub!(/\\V\[(\d+)\]/i) { $game_variables[$1.to_i].to_s }
      break if previous==text
    end
    text.gsub!(/\\V\[[^\]]*\]/i, '') # tambien corta referencias ciclicas
    text.gsub!(/\\N\[(\d+)\]/i) do
      actor=$game_actors[$1.to_i]
      actor ? actor.name : ''
    end
    # XP no implementa las pausas/velocidades de VX. Se descartan sin tinta.
    text.gsub!(/\\[.\|!><\^\$\{\}]/, '')
    text.gsub!(/\\(?:P\[[^\]]*\]|NOMBRE\[[^\]]*\]|D\[[01]\]|C\[\d+\]|[GLR]|[A-Za-z]+(?:\[[^\]]*\])?)/i) do |code|
      code =~ /\A\\(?:P\[[^\]]*\]|NOMBRE\[[^\]]*\]|D\[[01]\]|C\[\d+\]|[GLR])\z/i ? code : ''
    end
    text
  end
  def self.visible(value)
    value.gsub(/\\C\[\d+\]|\\G/i, '').gsub(/\003/) { '\\' }
  end
end
class Window_Message
  # Fila superior visible de cada retrato (los demas empiezan arriba).
  VN_TOP = {'junco_neutral'=>61, 'madre_envejecida_neutral'=>93, 'madre_ira'=>93, 'madre_neutral'=>93, 'muesca_neutral'=>121}
  alias vacas_vn_initialize initialize
  def initialize
    vacas_vn_initialize
    self.x = 16
    self.width = Vacas_HD.w - 32
    self.contents.dispose
    self.contents = Bitmap.new(Vacas_HD.w - 64, 128)
    self.contents.font.name = 'Arial'
    self.contents.font.size = 16
    @vn_bust = Sprite.new
    @vn_bust.z = 9995
    @vn_plate = Sprite.new
    @vn_plate.z = 9999
    @vn_plate.bitmap = Bitmap.new(300, 36)
    @vn_dim = Sprite.new
    @vn_dim.z = 9993
    @vn_dim.bitmap = Bitmap.new(Vacas_HD.w, Vacas_HD.h)
    @vn_dim.bitmap.fill_rect(0, 0, Vacas_HD.w, Vacas_HD.h, Color.new(0, 0, 0, 125))
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
    self.y = $game_temp.in_battle ? 8 : Vacas_HD.bottom(self.height + 8)
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
    text.gsub!(/\\R/i) { right = true; '' }
    text.gsub!(/\\L/i) { right = false; '' }
    $game_temp.message_text = text.clone
    vacas_vn_refresh
    # Bustos por encima del mapa, debajo de la caja. Cache posee su bitmap.
    if portrait != nil
      @vn_bust.bitmap = RPG::Cache.picture('retrato_' + portrait)
      # En combate el busto termina antes del estado inferior.
      bottom=$game_temp.in_battle ? Vacas_HD.bottom(154) : Vacas_HD.h
      @vn_bust.zoom_x = @vn_bust.zoom_y = [1.0, (bottom-24).to_f/@vn_bust.bitmap.height].min
      @vn_bust.x = right ? Vacas_HD.w - (@vn_bust.bitmap.width * @vn_bust.zoom_x).to_i : 0
      # La cabeza siempre arriba: los retratos con aire encima suben.
      top=(VN_TOP[portrait] || 0)
      @vn_bust.y = [bottom - (@vn_bust.bitmap.height * @vn_bust.zoom_y).to_i, 8 - (top * @vn_bust.zoom_y).to_i].min
      @vn_bust.visible = true
    end
    @vn_dim.visible = dim
    self.back_opacity = (portrait != nil) ? 255 : 235
    unless name == ''
      b = @vn_plate.bitmap
      b.clear
      b.fill_rect(0, 0, 300, 36, Color.new(17, 22, 22, 235))
      b.fill_rect(0, 32, 300, 3, Color.new(139, 111, 72))
      b.font.name = 'Arial'
      b.font.size = 18
      b.font.color = Color.new(222, 207, 165)
      b.draw_text(12, 0, 276, 32, Vacas_UI.fit(b,name,276))
      # Placa del nombre al lado contrario del busto: nunca tapa la cara.
      @vn_plate.x = (portrait != nil) ? (right ? 16 : Vacas_HD.w - 316) : (right ? Vacas_HD.w - 316 : 16)
      @vn_plate.y = $game_temp.in_battle ? self.y + self.height : self.y - 36
      @vn_plate.visible = true
    end
    # El mensaje original ya expandio variables y colores. Copiamos el resultado
    # y revelamos cada glifo UTF-8, sin alterar la logica nativa de opciones.
    return if $game_temp.num_input_variable_id > 0
    @vn_choice_active = self.active
    self.active = false
    plain = Vacas_MessageText.visible(text)
    begin
      last = plain.clone
      plain.gsub!(/\\[Vv]\[([0-9]+)\]/) { $game_variables[$1.to_i].to_s }
    end until last == plain
    plain.gsub!(/\\[Nn]\[([0-9]+)\]/) { $game_actors[$1.to_i].name }
    plain.gsub!(/\\[Cc]\[[0-9]+\]/, '')
    plain.gsub!(/\\[Gg]/, '')
    plain.gsub!(/\\\\/) { '\\' }
    # El render base indenta las elecciones ocho pixeles y empieza en x=4.
    @vn_full = Bitmap.new(self.contents.width, self.contents.height)
    @vn_full.blt(0, 0, self.contents, self.contents.rect)
    self.contents.clear
    @vn_units = []
    x = $game_temp.choice_start==0 ? 8 : 0
    y = 0
    plain.scan(/./m).each do |ch|
      if ch == "\n"
        y += 32
        x = y/32 >= $game_temp.choice_start ? 8 : 0
      else
        w = self.contents.text_size(ch).width
        @vn_units.push(Rect.new(x+4, y, w + 4, 32)) if y < 128
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
      elsif @vn_tick % (defined?(Vacas_Config) ? Vacas_Config.get(:texto) : 2) == 0
        r = @vn_units.shift
        self.contents.blt(r.x, r.y, @vn_full, r)
      end
      if @vn_units.empty?
        self.contents.blt(0,0,@vn_full,@vn_full.rect)
        self.active = @vn_choice_active
      end
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

# Paginacion antes de dibujar: no se pierde texto al superar cuatro filas.
# Las opciones permanecen juntas en la ultima pagina y conservan sus indices.
class Window_Message
  alias ui_pages_refresh refresh
  def refresh
    unless @ui_advancing
      text=Vacas_MessageText.normalize($game_temp.message_text)
      tags=''
      text.gsub!(/\\(?:P|NOMBRE|D)\[[^\]]*\]|\\[LR]/i) { tags+=$&; '' }
      text.gsub!(/\\[Vv]\[(\d+)\]/) { $game_variables[$1.to_i].to_s }
      text.gsub!(/\\[Nn]\[(\d+)\]/) { $game_actors[$1.to_i].name }
      @ui_choice_max=$game_temp.choice_max
      @ui_number_id=$game_temp.num_input_variable_id
      rows=text.split("\n")
      choices=@ui_choice_max>0 ? rows.slice!($game_temp.choice_start,@ui_choice_max) : []
      choices ||= []
      lines=Vacas_UI.wrap(contents,rows.join("\n"),contents.width-20,true)
      pages=[]
      reserved=@ui_choice_max>0 ? @ui_choice_max : (@ui_number_id>0 ? 1 : 0)
      while lines.size>4-reserved
        pages.push(lines.slice!(0,[4,lines.size].min))
      end
      @ui_choice_rows=[]
      final=lines.clone
      choices.each do |s|
        wrapped=Vacas_UI.wrap(contents,s,contents.width-24,true)
        @ui_choice_rows.push([final.size,wrapped.size])
        final.concat(wrapped)
      end
      pages.push(final) unless final.empty? && reserved==0 && !pages.empty?
      color=''
      @ui_pages=pages.collect do |p|
        body=p.join("\n")+"\n"
        page=tags+color+body
        body.scan(/\\C\[\d+\]/i) { |code| color=code }
        page
      end
      @ui_last_start=lines.size
    end
    $game_temp.message_text=@ui_pages.shift
    last=@ui_pages.empty?
    $game_temp.choice_max=last ? @ui_choice_max : 0
    $game_temp.choice_start=last && @ui_choice_max>0 ? @ui_last_start : 99
    $game_temp.num_input_variable_id=last ? @ui_number_id : 0
    $game_temp.num_input_start=@ui_last_start if last && @ui_number_id>0
    rows=[$game_temp.message_text.count("\n"),4].max
    contents.dispose
    self.contents=Bitmap.new(self.width-32,rows*32)
    self.contents.font.name='Arial'; self.contents.font.size=16
    self.oy=0
    ui_pages_refresh
  end
  alias ui_pages_cursor update_cursor_rect
  def update_cursor_rect
    if self.index>=0 && @ui_choice_rows && $game_temp.choice_max>0
      row,count=@ui_choice_rows[self.index]
      top=row*32; span=count*32
      self.oy=top if top<self.oy || top+span>self.oy+self.height-32
      self.cursor_rect.set(8,top-self.oy,self.width-56,[span,self.height-32].min)
    else
      ui_pages_cursor
    end
  end
  alias ui_pages_update update
  def update
    if @ui_pages && !@ui_pages.empty? && @contents_showing && !@fade_in &&
        (!@vn_units || @vn_units.empty?) && Input.trigger?(Input::C)
      @ui_advancing=true
      refresh
      @ui_advancing=false
      return
    end
    ui_pages_update
  end
end
