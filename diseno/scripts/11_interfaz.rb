# Vacas: interfaz completa. RGSS1 / Ruby 1.8. Instalar despues de BajoCiudad.
module Vacas_Config
  FILE = 'Vacas.cfg'
  DEFAULTS = {:bgm=>80, :bgs=>70, :se=>80, :me=>80, :texto=>2,
    :brillo=>100, :intensidad=>70, :subtitulos=>true}
  def self.values
    return @values if @values
    @values = DEFAULTS.clone
    begin
      data = File.open(FILE, 'rb') { |f| Marshal.load(f) }
      DEFAULTS.each do |k,v|
        n = data[k] if data.is_a?(Hash)
        if v == true
          @values[k] = n if n == true || n == false
        elsif n.is_a?(Numeric)
          limits = k == :texto ? [1,4] : (k == :brillo ? [50,150] : [0,100])
          @values[k] = [[n.to_i,limits[0]].max,limits[1]].min
        end
      end
    rescue StandardError
      # Config ausente/corrupta: valores seguros, no afecta a las partidas.
    end
    @values
  end
  def self.get(k); values[k]; end
  def self.set(k,v); values[k]=v; end
  def self.save
    begin
      File.open(FILE+'.tmp','wb') { |f| Marshal.dump(values,f) }
      File.delete(FILE+'.bak') if FileTest.exist?(FILE+'.bak')
      File.rename(FILE,FILE+'.bak') if FileTest.exist?(FILE)
      File.rename(FILE+'.tmp',FILE)
      true
    rescue StandardError
      File.rename(FILE+'.bak',FILE) if !FileTest.exist?(FILE) && FileTest.exist?(FILE+'.bak')
      false
    end
  end
end

module Vacas_Audio
  # clave => [tipo, nombre SIN extension, volumen base, tono, subtitulo]
  TABLE = {
    :titulo=>[:bgm,'vacas_titulo',80,100,''],
    :menu=>[:bgs,'vacas_menu',45,100,'Zumbido electrico'],
    :piso=>[:bgs,'vacas_piso',65,100,'La television tras la pared'],
    :matadero=>[:bgs,'vacas_matadero',65,100,'La cadena sigue girando'],
    :camaras=>[:bgs,'vacas_camaras',60,100,'Compresor lejano'],
    :laboratorio=>[:bgs,'vacas_laboratorio',55,100,'Cristal y fluorescentes'],
    :alcantarillas=>[:bgs,'vacas_alcantarillas',60,100,'Agua bajo los pies'],
    :manada=>[:bgs,'vacas_manada',60,100,'Respiraciones en la oscuridad'],
    :combate=>[:bgm,'vacas_combate',75,100,''],
    :jefe=>[:bgm,'vacas_jefe',80,100,''],
    :persecucion=>[:bgm,'vacas_persecucion',80,100,'Pasos cada vez mas cerca'],
    :victoria=>[:me,'vacas_victoria',70,100,''],
    :derrota=>[:me,'vacas_derrota',65,100,''],
    :gameover=>[:bgm,'vacas_gameover',65,100,''],
    :cursor=>[:se,'ui_cursor',55,100,''],
    :confirmar=>[:se,'ui_confirmar',65,100,''],
    :cancelar=>[:se,'ui_cancelar',60,100,''],
    :error=>[:se,'ui_error',60,100,''],
    :golpe=>[:se,'mente_golpe',75,100,'Golpe seco'],
    :susto=>[:se,'mente_susto',85,100,'Golpe repentino'],
    :paso_baldosa=>[:se,'paso_baldosa',40,100,''],
    :paso_metal=>[:se,'paso_metal',40,100,''],
    :paso_agua=>[:se,'paso_agua',40,100,''],
    :puerta=>[:se,'puerta_oxido',60,100,'Una puerta chirria']
  }
  LEGACY = {'058-Slow01'=>:titulo, '036-Dungeon02'=>:combate,
    '016-Shock01'=>:victoria, '092-Attack04'=>:susto,
    '140-Darkness03'=>:golpe, '040-Knock01'=>:puerta}
  def self.path?(name)
    return true if FileTest.exist?(name)
    ['.ogg','.wav','.mp3','.mid','.wma'].any? { |ext| FileTest.exist?(name+ext) }
  end
  def self.play(key)
    row=TABLE[key]; return unless row
    type,name,vol,pitch,caption=row
    Audio.send(type.to_s+'_play','Audio/'+type.to_s.upcase+'/'+name,vol,pitch)
    subtitle(caption) if path?('Audio/'+type.to_s.upcase+'/'+name)
  end
  def self.subtitle(s)
    return if s.nil? || s=='' || !Vacas_Config.get(:subtitulos)
    @caption=s; @until=Graphics.frame_count+100
  end
  def self.caption
    return '' unless Vacas_Config.get(:subtitulos) && @until && Graphics.frame_count<@until
    @caption || ''
  end
  def self.zone
    id=$game_map.map_id
    return :manada if [20,21].include?(id)
    return :alcantarillas if id>=17
    return :laboratorio if id>=12
    return :camaras if id==9
    return :matadero if id>=5
    :piso
  end
  def self.refresh
    [:bgm,:bgs].each do |type|
      args=Audio.vacas_tracks[type]
      Audio.send(type.to_s+'_play',*args) if args
    end
  end
end

module Audio
  class << self
    def vacas_tracks; @vacas_tracks ||= {}; end
    alias vacas_original_bgm_play bgm_play
    alias vacas_original_bgs_play bgs_play
    alias vacas_original_se_play se_play
    alias vacas_original_me_play me_play
    def vacas_dispatch(kind,original,args)
        name=args[0]; volume=args[1] || 100; pitch=args[2] || 100
        key=Vacas_Audio::LEGACY[File.basename(name.to_s)]
        if key
          row=Vacas_Audio::TABLE[key]
          name='Audio/'+kind.to_s.upcase+'/'+row[1]
        end
        vacas_tracks[kind]=[name,volume,pitch] if [:bgm,:bgs].include?(kind)
        if key==:susto || File.basename(name.to_s)==Vacas_Audio::TABLE[:susto][1]
          volume=volume*Vacas_Config.get(:intensidad)/100
        end
        if Vacas_Audio.path?(name.to_s)
          Vacas_Audio.subtitle(row[4]) if key
          send(original,name,volume*Vacas_Config.get(kind)/100,pitch)
        elsif [:bgm,:bgs].include?(kind)
          send(kind.to_s+'_stop')
        end
    end
    def bgm_play(*args); vacas_dispatch(:bgm,:vacas_original_bgm_play,args); end
    def bgs_play(*args); vacas_dispatch(:bgs,:vacas_original_bgs_play,args); end
    def se_play(*args); vacas_dispatch(:se,:vacas_original_se_play,args); end
    def me_play(*args); vacas_dispatch(:me,:vacas_original_me_play,args); end
    alias vacas_original_bgm_stop bgm_stop
    alias vacas_original_bgs_stop bgs_stop
    def bgm_stop; vacas_tracks.delete(:bgm); vacas_original_bgm_stop; end
    def bgs_stop; vacas_tracks.delete(:bgs); vacas_original_bgs_stop; end
  end
end

module Vacas_UI
  INK=Color.new(226,216,187)
  MINT=Color.new(142,187,153)
  RUST=Color.new(154,69,54)
  DARK=Color.new(12,17,17,240)
  def self.text(b,x,y,w,s,size=20,color=INK,align=0)
    b.font.name='Arial'; b.font.size=size; b.font.color=color
    b.draw_text(x,y,w,[size+8,28].max,s.to_s,align)
  end
  def self.bar(b,x,y,w,value,max,kind)
    ratio=[[value.to_f/[max,1].max,0].max,1].min
    b.fill_rect(x,y,w,7,Color.new(5,8,8,240))
    texture=RPG::Cache.picture('ui_bar_'+kind)
    n=((w-2)*ratio).to_i
    b.stretch_blt(Rect.new(x+1,y+1,n,5),texture,texture.rect) if n>0
  end
  def self.background(name='menu'); Vacas_UI_Background.new(name); end
  def self.loop_scene(scene)
    Graphics.transition(16)
    loop do
      Graphics.update; Input.update; scene.update
      break if $scene != scene
    end
    Graphics.freeze
  end
  def self.save_allowed?
    return false if $game_system.menu_disabled
    return false if [10,90,120,122].any? { |id| $game_switches[id] }
    return true if $game_map.map_id==21
    return false unless $game_map.map_id==2
    # La television del salon: misma restriccion fisica del punto de guardado.
    ($game_player.x-8).abs+($game_player.y-17).abs<=1
  end
  def self.heading(b,title,sub)
    text(b,24,24,560,title,30)
    text(b,26,57,560,sub,16,MINT)
  end
end

# Fondo propio animado: desplazamiento subpixel, niebla y fluorescente.
class Vacas_UI_Background
  def initialize(name)
    @back=Sprite.new
    @back.bitmap=RPG::Cache.picture('ui_'+name)
    @back.zoom_x=1.03; @back.zoom_y=1.03
    @veil=Plane.new
    @veil.bitmap=RPG::Cache.picture('ui_fog')
    @veil.opacity=32; @veil.z=1
    @tick=0
  end
  def update
    @tick+=1
    @back.x=-10+Math.sin(@tick/150.0)*7
    @veil.ox+=0.25; @veil.oy-=0.1
    n=(@tick%193<3) ? -22*Vacas_Config.get(:intensidad)/100 : 0
    @back.tone=Tone.new(n,n,n,0)
  end
  def dispose; @veil.dispose; @back.dispose; end
end

# Skin y color propios para TODAS las ventanas (incluye inventario y archivos).
Font.default_name='Arial'
Font.default_size=20
class Window_Base
  alias ui_base_initialize initialize
  def initialize(*args)
    ui_base_initialize(*args)
    self.windowskin=RPG::Cache.windowskin('ui_windowskin')
    self.back_opacity=235
  end
  alias ui_base_update update
  def update
    ui_base_update
    self.windowskin=RPG::Cache.windowskin('ui_windowskin')
  end
  def normal_color; Vacas_UI::INK; end
  def system_color; Vacas_UI::MINT; end
  def disabled_color; Color.new(131,128,112,150); end
  def crisis_color; Color.new(216,151,92); end
  def knockout_color; Color.new(218,91,72); end
end

class Window_VacasPanel < Window_Base
  def initialize(x,y,w,h)
    super(x,y,w,h)
    self.contents=Bitmap.new(w-32,h-32)
  end
  def lines(title,lines)
    contents.clear
    Vacas_UI.text(contents,0,0,contents.width,title,23,Vacas_UI::MINT)
    y=40
    contents.font.size=18
    lines.each do |s|
      line=''
      s.split(' ').each do |word|
        candidate=line=='' ? word : line+' '+word
        if contents.text_size(candidate).width>contents.width && line!=''
          Vacas_UI.text(contents,0,y,contents.width,line,18);y+=26;line=word
        else
          line=candidate
        end
      end
      Vacas_UI.text(contents,0,y,contents.width,line,18);y+=30
    end
  end
end

class Window_VacasCommand < Window_Selectable
  def initialize(x,y,w,commands)
    super(x,y,w,[commands.size*32+32,480-y-8].min)
    @commands=commands; @item_max=commands.size; @column_max=1
    self.contents=Bitmap.new(w-32,@item_max*32)
    @disabled=[]; self.index=0; refresh
  end
  def disable_item(n); @disabled.push(n); refresh; end
  def refresh
    contents.clear
    @commands.each_with_index do |s,i|
      Vacas_UI.text(contents,12,i*32,contents.width-16,s,21,
        @disabled.include?(i) ? disabled_color : normal_color)
    end
  end
end

# Un cursor animado propio en cualquier lista. El rectangulo usa la skin propia.
class Window_Selectable
  alias ui_select_update update
  def update
    old=@index
    ui_select_update
    if !@ui_cursor
      @ui_cursor=Sprite.new
      @ui_cursor.bitmap=RPG::Cache.picture('ui_cursor')
    end
    r=self.cursor_rect
    @ui_cursor.visible=self.visible && self.active && @index>=0 && r.width>0
    @ui_cursor.x=self.x+8+r.x+Math.sin(Graphics.frame_count/7.0)*2
    @ui_cursor.y=self.y+22+r.y
    @ui_cursor.z=self.z+2; @ui_cursor.opacity=self.contents_opacity
    Vacas_Audio.play(:cursor) if old!=@index && self.active
  end
  alias ui_select_dispose dispose
  def dispose
    @ui_cursor.dispose if @ui_cursor
    ui_select_dispose
  end
end

class Scene_Title
  # Conserva command_new_game y toda su cadena Mayus/Ctrl/Alt.
  def main
    if $BTEST; battle_test; return; end
    names={'Actors'=>'actors','Classes'=>'classes','Skills'=>'skills','Items'=>'items',
      'Weapons'=>'weapons','Armors'=>'armors','Enemies'=>'enemies','Troops'=>'troops',
      'States'=>'states','Animations'=>'animations','Tilesets'=>'tilesets',
      'CommonEvents'=>'common_events','System'=>'system'}
    names.each { |file,key| eval('$data_'+key+' = load_data("Data/'+file+'.rxdata")') }
    Vacas.ajustar_sistema; $game_system=Game_System.new
    @background=Vacas_UI.background('titulo')
    @logo=Sprite.new; @logo.z=5; @logo.bitmap=Bitmap.new(640,480)
    b=@logo.bitmap
    Vacas_UI.text(b,42,72,500,'V A C A S',64)
    Vacas_UI.text(b,46,141,500,'LA CARNE RECUERDA',17,Vacas_UI::MINT)
    Vacas_UI.text(b,28,441,600,'Z / Intro: elegir     Esc: volver     Flechas: mover',16)
    @command_window=Window_VacasCommand.new(36,230,248,
      ['Nueva partida','Continuar','Ajustes','Salir'])
    @continue_enabled=(1..4).any? { |i| FileTest.exist?('Save'+i.to_s+'.rxdata') }
    @command_window.disable_item(1) unless @continue_enabled
    Vacas_Audio.play(:titulo)
    Vacas_UI.loop_scene(self)
    @command_window.dispose; @logo.bitmap.dispose; @logo.dispose; @background.dispose
  end
  def update
    @background.update; @command_window.update
    return unless Input.trigger?(Input::C)
    case @command_window.index
    when 0; Vacas_Audio.play(:confirmar); command_new_game
    when 1; command_continue
    when 2; Vacas_Audio.play(:confirmar); $scene=Scene_VacasSettings.new(:titulo)
    when 3; command_shutdown
    end
  end
end

class Scene_VacasSettings
  KEYS=[:bgm,:bgs,:se,:me,:texto,:brillo,:intensidad,:subtitulos,:fullscreen,:volver]
  LABELS=['Musica / BGM','Ambiente / BGS','Efectos / SE','Melodias / ME',
    'Velocidad de texto','Brillo','Sustos y temblores','Subtitulos de sonido',
    'Pantalla completa','Guardar y volver']
  def initialize(origin=:menu); @origin=origin; end
  def main
    @background=Vacas_UI.background
    @panel=Window_VacasPanel.new(32,8,576,80)
    @panel.lines('AJUSTES',''.split)
    @list=Window_VacasCommand.new(32,88,576,LABELS)
    @hint=Window_VacasPanel.new(32,432,576,48)
    draw
    Vacas_UI.loop_scene(self)
    @background.dispose; @panel.dispose; @list.dispose; @hint.dispose
  end
  def draw
    @list.contents.clear
    KEYS.each_with_index do |k,i|
      value=Vacas_Config.get(k)
      s=case k
      when :subtitulos; value ? 'Si' : 'No'
      when :texto; {1=>'Rapida',2=>'Normal',3=>'Lenta',4=>'Muy lenta'}[value]
      when :fullscreen; 'Alt + Enter'
      when :volver; ''
      else; value.to_s+' %'
      end
      Vacas_UI.text(@list.contents,16,i*32,350,LABELS[i],20)
      Vacas_UI.text(@list.contents,366,i*32,170,s,20,Vacas_UI::MINT,2)
    end
    @hint.contents.clear
    Vacas_UI.text(@hint.contents,0,-5,540,'Izq / Der: ajustar    Esc: guardar y volver',15)
  end
  def update
    @background.update; @list.update
    key=KEYS[@list.index]
    delta=Input.repeat?(Input::RIGHT) ? 1 : (Input.repeat?(Input::LEFT) ? -1 : 0)
    if key==:volver && Input.trigger?(Input::C) || Input.trigger?(Input::B)
      if Vacas_Config.save
        Vacas_Audio.play(:cancelar)
        $scene= @origin==:titulo ? Scene_Title.new : Scene_Menu.new(4)
      else
        @hint.lines('No se pudo escribir Vacas.cfg. Reintenta.',[])
        Vacas_Audio.play(:error)
      end
      return
    end
    if key==:subtitulos && (delta!=0 || Input.trigger?(Input::C))
      Vacas_Config.set(key,!Vacas_Config.get(key)); draw
    elsif delta!=0 && ![:fullscreen,:volver,:subtitulos].include?(key)
      low=key==:texto ? 1 : (key==:brillo ? 50 : 0)
      high=key==:texto ? 4 : (key==:brillo ? 150 : 100)
      step=key==:texto ? 1 : 5
      Vacas_Config.set(key,[[Vacas_Config.get(key)+delta*step,low].max,high].min)
      Vacas_Audio.refresh if [:bgm,:bgs,:se,:me].include?(key)
      Vacas_Audio.play(:cursor); draw
    end
  end
end

class Scene_Menu
  def main
    Vacas_Audio.play(:menu)
    @background=Vacas_UI.background
    @command_window=Window_VacasCommand.new(24,112,208,
      ['Objetos','Estado / Cordura','Notas','Guardar','Ajustes','Salir'])
    @command_window.index=[@menu_index || 0,5].min
    @command_window.disable_item(3) unless Vacas_UI.save_allowed?
    @top=Window_VacasPanel.new(24,16,592,88)
    infos=load_data('Data/MapInfos.rxdata')
    @top.lines('PAUSA / '+infos[$game_map.map_id].name,[])
    @tasks=Window_VacasPanel.new(244,112,372,304)
    @tasks.lines('Lo que queda',Vacas.tareas.collect { |t| (t[1] ? '+ ' : '> ')+t[0] })
    @foot=Window_VacasPanel.new(24,424,592,56)
    @foot.lines('Z: elegir   Esc: regresar    '+$game_party.gold.to_s+' monedas',[])
    Vacas_UI.loop_scene(self)
    [@command_window,@top,@tasks,@foot].each { |w| w.dispose }; @background.dispose
  end
  def update
    @background.update; @command_window.update
    if Input.trigger?(Input::B); Vacas_Audio.play(:cancelar); $scene=Scene_Map.new; return; end
    return unless Input.trigger?(Input::C)
    Vacas_Audio.play(:confirmar)
    case @command_window.index
    when 0; $scene=Scene_Item.new
    when 1; $scene=Scene_VacasJournal.new(:estado)
    when 2; $scene=Scene_VacasJournal.new(:notas)
    when 3
      if Vacas_UI.save_allowed?; $scene=Scene_Save.new
      else; Vacas_Audio.play(:error); @foot.lines('Guarda ante la tele o en el altar.',[]); end
    when 4; $scene=Scene_VacasSettings.new
    when 5; $scene=Scene_End.new
    end
  end
end

class Scene_VacasJournal
  def initialize(mode); @mode=mode; end
  def main
    @background=Vacas_UI.background
    @panel=Window_VacasPanel.new(24,16,592,88)
    @panel.lines(@mode==:estado ? 'ESTADO / EL CUERPO RECUERDA' : 'NOTAS / LO QUE HAS GUARDADO',[])
    if @mode==:estado
      a=$game_party.actors[0]
      @body=Window_VacasPanel.new(24,112,592,328)
      @body.lines(a.name,['Salud: '+a.hp.to_s+' / '+a.maxhp.to_s,
        'Aliento: '+a.sp.to_s+' / '+a.maxsp.to_s,
        'Cordura: '+(100-Vacas.veneno).to_s+' / 100',
        'Veneno: '+Vacas.veneno.to_s+' / 100',
        'Huella permanente: '+Vacas.huella.to_s,
        'La cordura es el inverso del veneno.'])
      a.states.each_with_index do |id,i|
        next unless [2,3,4].include?(id)
        b=RPG::Cache.icon('ui_estado_'+id.to_s)
        @body.contents.blt(360+i*28,12,b,b.rect)
      end
    else
      ids=[4,6,8,9,10,11,13,15,23,24,28,33,34]
      @notes=ids.select { |id| $data_items[id] && $game_party.item_number(id)>0 }
      labels=@notes.collect { |id| $data_items[id].name }
      labels=['Aun no has guardado notas.'] if labels.empty?
      @body=Window_VacasCommand.new(24,112,592,labels)
    end
    Vacas_UI.loop_scene(self)
    @panel.dispose; @body.dispose; @background.dispose
  end
  def update
    @background.update; @body.update
    if Input.trigger?(Input::B); $scene=Scene_Menu.new(@mode==:estado ? 1 : 2); return; end
    return unless @mode==:notas && Input.trigger?(Input::C) && !@notes.empty?
    # CE1 conserva los textos originales y sus ramas narrativas.
    $vacas_ultimo_objeto=@notes[@body.index]
    $game_temp.common_event_id=1
    $scene=Scene_Map.new
  end
end

class Scene_Gameover
  def main
    Audio.bgs_stop; Audio.me_stop; Vacas_Audio.play(:gameover)
    @background=Vacas_UI.background('gameover')
    @text=Window_VacasPanel.new(32,68,576,144)
    @text.lines('LA CARNE NO OLVIDA',['Aun puedes volver a intentarlo.'])
    @list=Window_VacasCommand.new(32,282,300,['Cargar partida','Volver al titulo','Salir'])
    Vacas_UI.loop_scene(self)
    @list.dispose; @text.dispose; @background.dispose
  end
  def update
    @background.update; @list.update
    return unless Input.trigger?(Input::C)
    case @list.index
    when 0; $scene=Scene_Load.new
    when 1; $scene=Scene_Title.new
    when 2; $scene=nil
    end
  end
end

class Scene_End
  alias ui_end_main main
  def main
    @ui_background=Vacas_UI.background
    ui_end_main
    @ui_background.dispose
  end
  def command_cancel; $scene=Scene_Menu.new(5); end
  alias ui_end_update update
  def update
    @ui_background.update if @ui_background
    ui_end_update
  end
end

# Inventario y archivos reciben el mismo fondo, marco, cursor y tipografia.
class Scene_Item
  alias ui_item_main main
  def main
    @ui_background=Vacas_UI.background
    ui_item_main
    @ui_background.dispose
  end
  alias ui_item_update update
  def update
    @ui_background.update if @ui_background
    ui_item_update
  end
end
class Scene_File
  alias ui_file_main main
  def main
    @ui_background=Vacas_UI.background
    ui_file_main
    @ui_background.dispose
  end
  alias ui_file_update update
  def update
    @ui_background.update if @ui_background
    ui_file_update
  end
end

module Vacas
  class << self
    alias ui_ajustar_sistema ajustar_sistema
    def ajustar_sistema
      ui_ajustar_sistema
      $data_system.windowskin_name='ui_windowskin'
      {:cursor_se=>:cursor,:decision_se=>:confirmar,:cancel_se=>:cancelar,
        :buzzer_se=>:error}.each do |setter,key|
        row=Vacas_Audio::TABLE[key]
        $data_system.send(setter.to_s+'=',RPG::AudioFile.new(row[1],row[2],row[3]))
      end
      if $data_items
        $data_items.compact.each do |item|
          item.icon_name=[4,6,8,9,10,11,13,15,23,24,28,33,34].include?(item.id) ? 'ui_nota' : 'ui_objeto'
          item.icon_name='ui_bateria' if [30,31].include?(item.id)
        end
      end
      $data_skills.compact.each { |s| s.icon_name='ui_estado_2' } if $data_skills
    end
  end
end

class Window_PartyCommand
  def initialize
    super(8,334,160,146)
    self.contents=Bitmap.new(128,114)
    @commands=['Afrontar','Apartarse']; @item_max=2; @column_max=1
    draw_item(0,normal_color)
    draw_item(1,$game_temp.battle_can_escape ? normal_color : disabled_color)
    self.active=false; self.visible=false; self.index=0
  end
  def draw_item(i,color)
    contents.fill_rect(0,i*32,128,32,Color.new(0,0,0,0))
    Vacas_UI.text(contents,10,i*32,118,@commands[i],20,color)
  end
  def update_cursor_rect
    self.cursor_rect.set(0,@index*32,128,32)
  end
end

class Sprite_Battler
  alias ui_battler_update update
  def update
    ui_battler_update
    if @battler && @battler.is_a?(Game_Actor)
      self.x=86; self.y=326; self.zoom_x=0.6; self.zoom_y=0.6
    end
  end
end

class Window_Item
  alias ui_inventory_initialize initialize
  def initialize
    ui_inventory_initialize
    self.x=24;self.y=104;self.width=592
    self.height=$game_temp.in_battle ? 224 : 360
    @column_max=1
    refresh; self.index=0
  end
  def draw_item(index)
    item=@data[index]
    count=item.is_a?(RPG::Item) ? $game_party.item_number(item.id) :
      (item.is_a?(RPG::Weapon) ? $game_party.weapon_number(item.id) : $game_party.armor_number(item.id))
    b=contents;y=index*32
    icon=RPG::Cache.icon(item.is_a?(RPG::Item) ? item.icon_name : 'ui_objeto')
    b.blt(12,y+4,icon,icon.rect)
    Vacas_UI.text(b,48,y,430,item.name,20,normal_color)
    Vacas_UI.text(b,486,y,60,count.to_s,19,Vacas_UI::MINT,2)
  end
end

class Window_SaveFile
  alias ui_savefile_initialize initialize
  def initialize(*args)
    ui_savefile_initialize(*args)
    self.x=24; self.y=80+@file_index*96; self.width=592; self.height=88
    self.contents.dispose;self.contents=Bitmap.new(560,56);refresh
  end
  def refresh
    contents.clear
    name='RECUERDO 0'+(@file_index+1).to_s
    @name_width=contents.text_size(name).width
    Vacas_UI.text(contents,12,0,300,name,23,Vacas_UI::MINT)
    if @file_exist
      v=@game_variables[1]
      Vacas_UI.text(contents,12,28,330,'Veneno '+v.to_s+' / Cordura '+(100-v).to_s,17)
      Vacas_UI.text(contents,330,0,220,@time_stamp.strftime('%d / %m / %Y'),17,normal_color,2)
      Vacas_UI.text(contents,330,28,220,sprintf('%02d h %02d min',@total_sec/3600,@total_sec/60%60),17,normal_color,2)
    else
      Vacas_UI.text(contents,12,28,520,'Un espacio que aun no recuerda.',17)
    end
  end
end

# Persecucion enlazada a las marcas existentes; no modifica sus interpretes.
class Scene_Map
  alias ui_map_update update
  def update
    ui_map_update
    chasing=[10,90,120,122].any? { |id| $game_switches[id] }
    if @ui_chasing!=chasing
      Vacas_Audio.play(:persecucion) if chasing
      Vacas_Audio.play(Vacas_Audio.zone) unless chasing
      @ui_chasing=chasing
    end
  end
end

# HUD integrado, sin duplicar la bateria del acto IV.
class Sprite_Veneno
  def initialize
    super(nil)
    self.bitmap=Bitmap.new(240,84); self.x=14; self.y=390; self.z=4000
    @display=Vacas.veneno.to_f; @last=-1; @pulse=0
  end
  def update
    super
    v=Vacas.veneno
    @pulse=24 if @last!=v
    @last=v; @pulse-=1 if @pulse>0
    @display+=(v-@display)*0.16
    b=bitmap; b.clear
    b.fill_rect(0,0,232,80,Color.new(7,13,12,170))
    Vacas_UI.text(b,8,0,220,'CORDURA '+(100-v).to_s+' / VENENO '+v.to_s,14)
    Vacas_UI.bar(b,8,29,214,100-@display,100,'cordura')
    Vacas_UI.bar(b,8,40,214,@display,100,'vida')
    if Vacas.bajo_ciudad? && $game_party.item_number(30)>0
      Vacas_UI.text(b,8,48,210,'LINTERNA '+$game_variables[52].to_s+'%'+($game_switches[115] ? '' : ' / apagada'),14)
      Vacas_UI.bar(b,8,73,214,$game_variables[52],100,'cordura')
    end
    self.visible=!$game_temp.in_battle && !$game_temp.message_window_showing &&
      !$game_switches[Vacas::SW_HUD_OCULTO] && $scene.is_a?(Scene_Map)
    self.opacity=@pulse>0 ? 255 : 185
  end
end
class Sprite_Bateria
  def update; self.visible=false; end
end

# Intensidad global: tambien cubre eventos y las animaciones de combate.
class Game_Screen
  alias ui_start_shake start_shake
  def start_shake(power,speed,duration)
    ui_start_shake(power*Vacas_Config.get(:intensidad)/100.0,speed,duration)
  end
  alias ui_start_flash start_flash
  def start_flash(color,duration)
    c=color.clone; c.alpha=c.alpha*Vacas_Config.get(:intensidad)/100
    ui_start_flash(c,duration)
  end
  alias ui_susto vacas_susto
  def vacas_susto(id)
    ui_susto(id)
    p=@pictures[98]
    # Cero elimina imagen/flash/temblor; conserva marca y espera del evento.
    p.erase if Vacas_Config.get(:intensidad)==0
    unless Vacas_Config.get(:intensidad)==0
      p.move(1,0,0,0,100,100,255*Vacas_Config.get(:intensidad)/100,0)
    end
  end
end

# Brillo uniforme y subtitulos en todo el juego, sin tocar tonos narrativos.
module Graphics
  class << self
    alias ui_original_update update
    def update
      unless @ui_overlay
        @ui_view=Viewport.new(0,0,640,480); @ui_view.z=99999
        @ui_overlay=Sprite.new(@ui_view); @ui_overlay.bitmap=Bitmap.new(640,480)
        @ui_caption=Sprite.new(@ui_view); @ui_caption.bitmap=Bitmap.new(640,40)
        @ui_caption.y=0; @ui_caption.z=2
      end
      value=Vacas_Config.get(:brillo)
      if @ui_brightness!=value
        @ui_brightness=value
        @ui_overlay.bitmap.fill_rect(0,0,640,480,value<100 ? Color.new(0,0,0) : Color.new(255,245,220))
        @ui_overlay.opacity=(value-100).abs*2
      end
      caption=Vacas_Audio.caption
      if @ui_last_caption!=caption
        @ui_last_caption=caption; b=@ui_caption.bitmap; b.clear
        if caption!=''
          b.fill_rect(96,4,448,30,Color.new(5,10,10,210))
          Vacas_UI.text(b,100,4,440,'[ '+caption+' ]',17,Vacas_UI::INK,1)
        end
      end
      ui_original_update
    end
  end
end

# VN conserva retratos, nombre, decisiones y los codigos originales.
class Window_Message
  alias ui_message_update update
  def update
    ui_message_update
    unless @ui_advance
      @ui_advance=Sprite.new
      @ui_advance.bitmap=RPG::Cache.picture('ui_avance'); @ui_advance.z=10001
    end
    @ui_advance.x=self.x+self.width-38
    @ui_advance.y=self.y+self.height-23+Math.sin(Graphics.frame_count/6.0)*2
    @ui_advance.visible=self.visible && self.pause && self.contents_opacity>0
    self.pause=false if @ui_advance.visible
  end
  alias ui_message_dispose dispose
  def dispose
    @ui_advance.dispose if @ui_advance
    ui_message_dispose
  end
end

# Ventanas de combate: actores, enemigos, estados y barras interpoladas.
class Window_BattleStatus
  def initialize
    super(176,334,464,146)
    self.contents=Bitmap.new(432,114)
    @level_up_flags=[false,false,false,false]; @ui_values={}; refresh
  end
  def refresh
    return unless self.contents
    a=$game_party.actors[0]; return unless a
    @ui_values ||= {}
    signature=[a.hp,a.sp,Vacas.veneno,a.states.clone]
    settled=[:hp,:sp,:veneno].all? do |k|
      target=k==:veneno ? Vacas.veneno : a.send(k)
      @ui_values[k] && (@ui_values[k]-target).abs<0.2
    end
    return if @ui_signature==signature && settled
    @ui_signature=signature
    self.contents.clear
    {:hp=>a.hp,:sp=>a.sp,:veneno=>Vacas.veneno}.each do |key,value|
      @ui_values[key]=value.to_f unless @ui_values[key]
      @ui_values[key]+=(value-@ui_values[key])*0.2
    end
    b=contents
    Vacas_UI.text(b,0,0,240,a.name+' / MANTENTE AQUI',19,Vacas_UI::MINT)
    Vacas_UI.text(b,0,28,204,'Salud '+a.hp.to_s+'/'+a.maxhp.to_s,17)
    Vacas_UI.bar(b,0,55,200,@ui_values[:hp],a.maxhp,'vida')
    Vacas_UI.text(b,220,28,200,'Aliento '+a.sp.to_s+'/'+a.maxsp.to_s,17)
    Vacas_UI.bar(b,220,55,204,@ui_values[:sp],a.maxsp,'cordura')
    Vacas_UI.text(b,0,64,210,'Cordura '+(100-Vacas.veneno).to_s,17)
    Vacas_UI.bar(b,0,94,200,100-@ui_values[:veneno],100,'cordura')
    Vacas_UI.text(b,220,64,200,'Veneno '+Vacas.veneno.to_s,17)
    Vacas_UI.bar(b,220,94,204,@ui_values[:veneno],100,'vida')
    a.states.each_with_index do |id,i|
      next unless [2,3,4].include?(id)
      icon=RPG::Cache.icon('ui_estado_'+id.to_s)
      b.blt(300+i*26,0,icon,icon.rect)
    end
  end
  def update; super; refresh; end
end

class Window_VacasEnemies < Window_VacasPanel
  def initialize; super(8,4,216,100); @values={}; end
  def update
    super; contents.clear
    enemies=$game_troop.enemies.select { |e| !e.hidden }
    rows=[[enemies.size,1].max,3].min
    if self.height!=32+rows*68
      self.height=32+rows*68
      self.contents.dispose;self.contents=Bitmap.new(184,rows*68)
    end
    enemies.each_with_index do |e,i|
      break if i>=3
      @values[e.index]=e.hp.to_f unless @values[e.index]
      @values[e.index]+=(e.hp-@values[e.index])*0.18
      y=i*68
      Vacas_UI.text(contents,0,y,184,e.name,16)
      Vacas_UI.bar(contents,0,y+30,182,@values[e.index],e.maxhp,'vida')
      e.states.each_with_index do |id,n|
        next unless [2,3,4].include?(id)
        icon=RPG::Cache.icon('ui_estado_'+id.to_s)
        contents.blt(n*24,y+42,icon,icon.rect)
      end
    end
  end
end

class Arrow_Base
  alias ui_arrow_update update
  def update
    ui_arrow_update
    self.bitmap=RPG::Cache.picture('ui_target')
    self.src_rect.set(0,0,32,32)
    self.ox=16; self.oy=44
    self.opacity=170+(@blink_count*10)
  end
end
class Arrow_Actor
  alias ui_actor_arrow_update update
  def update
    ui_actor_arrow_update
    self.x=86;self.y=326 if self.actor
  end
end

class Window_VacasBattleCommand < Window_Command
  def initialize(commands)
    super(160,commands)
    self.height=146
    self.contents.dispose;self.contents=Bitmap.new(128,114)
    @commands.each_index { |i| draw_item(i,normal_color) }
  end
  def draw_item(i,color)
    contents.fill_rect(0,i*28,128,28,Color.new(0,0,0,0))
    Vacas_UI.text(contents,8,i*28,120,@commands[i],18,color)
  end
  def page_row_max; 4; end
  def update_cursor_rect
    self.cursor_rect.set(0,@index*28,128,28)
  end
end

class Scene_Battle
  alias ui_start_phase1 start_phase1
  def start_phase1
    @actor_command_window.dispose
    w=$data_system.words
    @actor_command_window=Window_VacasBattleCommand.new([w.attack,w.skill,w.guard,w.item])
    @actor_command_window.x=8;@actor_command_window.y=334
    @actor_command_window.active=false;@actor_command_window.visible=false
    ui_start_phase1
  end
  alias ui_battle_main main
  def main
    @ui_enemies=Window_VacasEnemies.new
    @ui_entry=Sprite.new; @ui_entry.z=9000; @ui_entry.bitmap=Bitmap.new(640,480)
    @ui_entry.bitmap.fill_rect(0,0,640,480,Color.new(6,12,12,220))
    Vacas_UI.text(@ui_entry.bitmap,90,200,460,'LA IMAGEN TE ENCUENTRA',30,Vacas_UI::INK,1)
    @ui_entry_ticks=48
    zone=Vacas_Audio.zone
    zone=:manada if $game_temp.battle_troop_id==17
    zone=:laboratorio if (10..13).include?($game_temp.battle_troop_id)
    $game_map.battleback_name='ui_'+zone.to_s
    Vacas_Audio.play([9,13,17].include?($game_temp.battle_troop_id) ? :jefe : :combate)
    begin
      ui_battle_main
    ensure
      @ui_enemies.dispose; @ui_entry.bitmap.dispose; @ui_entry.dispose
    end
  end
  alias ui_battle_update update
  def update
    @ui_entry_ticks-=1 if @ui_entry_ticks && @ui_entry_ticks>0
    @ui_entry.opacity=[@ui_entry_ticks*7,255].min if @ui_entry
    if @ui_entry_ticks && @ui_entry_ticks>0
      @spriteset.update; @ui_enemies.update; return
    end
    if @actor_command_window
      @actor_command_window.x=8; @actor_command_window.y=334
      @actor_command_window.back_opacity=245
    end
    @ui_enemies.update if @ui_enemies
    @ui_enemies.visible=!@message_window.visible if @ui_enemies && @message_window
    ui_battle_update
  end
  alias ui_phase4_hit update_phase4_step5
  def update_phase4_step5
    hit=@target_battlers.any? { |t| t.damage.is_a?(Numeric) && t.damage>0 }
    if hit
      $game_screen.start_shake(4,7,10)
      $game_screen.start_flash(Color.new(163,66,49,65),7)
      Vacas_Audio.play(:golpe)
    end
    ui_phase4_hit
  end
  alias ui_battle_end battle_end
  def battle_end(result)
    if result!=0
      ui_result_card(result)
    end
    ui_battle_end(result)
  end
  def ui_result_card(result)
    card=Window_VacasPanel.new(104,162,432,156); card.z=10000
    card.lines(result==2 ? 'LA IMAGEN TE SUPERA' : 'APARTAS LA MIRADA',
      ['Respira. Todavia puedes seguir.','Pulsa Z / Intro.'])
    Vacas_Audio.play(:derrota)
    16.times { Graphics.update; Input.update }
    loop do
      Graphics.update; Input.update
      break if Input.trigger?(Input::C) || Input.trigger?(Input::B)
    end
    card.dispose
  end
end

class Window_BattleResult
  alias ui_result_initialize initialize
  def initialize(*args)
    ui_result_initialize(*args)
    self.x=104; self.y=164; self.width=432; self.height=156
    self.contents.dispose; self.contents=Bitmap.new(400,124)
    refresh; Vacas_Audio.play(:victoria)
  end
  def refresh
    return unless self.contents
    contents.clear
    Vacas_UI.text(contents,8,0,380,'SIGUES AQUI. RESPIRA.',27,Vacas_UI::MINT)
    Vacas_UI.text(contents,8,40,380,'La imagen pierde fuerza.',20)
    Vacas_UI.text(contents,8,78,380,'Z / Intro: volver',17)
  end
end

# Numeros emergentes propios: mantiene duracion y liberacion nativas de XP.
class RPG::Sprite
  def damage(value,critical)
    dispose_damage
    label=value.is_a?(Numeric) ? value.abs.to_s : (value=='Miss' ? 'FALLO' : value.to_s)
    b=Bitmap.new(180,56)
    b.font.name='Arial'; b.font.size=30; b.font.bold=true
    b.font.color=Color.new(4,8,8)
    b.draw_text(2,2,176,48,label,1)
    b.font.color=value.is_a?(Numeric) && value<0 ? Vacas_UI::MINT : Vacas_UI::INK
    b.draw_text(0,0,176,48,label,1)
    @damage_sprite=::Sprite.new(self.viewport)
    @damage_sprite.bitmap=b; @damage_sprite.ox=90; @damage_sprite.oy=40
    @damage_sprite.x=self.x; @damage_sprite.y=self.y-self.oy/2
    @damage_sprite.z=3000; @damage_duration=40
  end
end

# Ganchos de ambiente y pasos. La frecuencia no depende de la velocidad de FPS.
class Game_Map
  alias ui_map_autoplay autoplay
  def autoplay
    ui_map_autoplay
    Vacas_Audio.play(Vacas_Audio.zone)
  end
end
class Game_Player
  alias ui_player_increase_steps increase_steps
  def increase_steps
    ui_player_increase_steps
    @ui_steps=(@ui_steps || 0)+1
    if @ui_steps%2==0 && !$game_temp.message_window_showing
      zone=Vacas_Audio.zone
      key=[:alcantarillas,:manada].include?(zone) ? :paso_agua :
        ([:matadero,:camaras].include?(zone) ? :paso_metal : :paso_baldosa)
      Vacas_Audio.play(key)
    end
  end
end
