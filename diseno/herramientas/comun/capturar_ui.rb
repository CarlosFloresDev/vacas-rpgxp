# Capturador nativo aislado. No instalar en Scripts.rxdata.
require 'zlib'
require 'json'
$ui_report={:motor_real=>true,:pantallas=>[],:errores=>[]}
$ui_report[:hallazgos_corregidos]=[
  {:pantalla=>'Guardar / Continuar',:antes=>'70 - 32 = 38 px visibles; segunda linea termina en 56: corte de 18 px',:despues=>'Dos tarjetas de 108 px; contenido de 76 px; filas en 0 y 32; cuatro ranuras en dos paginas'},
  {:pantalla=>'Paneles',:antes=>'Interlineado reducido a 20/23 px con rectangulos de texto de 28 px',:despues=>'Titulo de 28 px, cuerpo de 24 px y paginacion con contador'},
  {:pantalla=>'Tienda',:antes=>'Dinero en y=48 invade ayuda de 64 px',:despues=>'Dinero en y=64; listas con filas completas'},
  {:pantalla=>'VN',:antes=>'Sin ajuste ni paginas; glifos fuera de las cuatro filas',:despues=>'Medicion por glifo, cuatro filas por pagina; decisiones completas con desplazamiento y cursor por opcion'},
  {:pantalla=>'Aviso',:antes=>'Rectangulos de 28 px cada 21 px',:despues=>'Interlineado igual al rectangulo, fuente limitada por text_size'},
  {:pantalla=>'Combate',:antes=>'Tres enemigos ocupaban 236 px y alcanzaban el estado inferior',:despues=>'Filas calculadas hasta el borde del estado; objetivos ocultos mientras se muestra ayuda'},
  {:pantalla=>'Listas y teclado',:antes=>'Filas parciales, nombres largos comprimidos y teclado mas alto que sus celdas',:despues=>'Filas completas, nombres con elipsis y teclado ajustado por altura efectiva'}]
$ui_log=File.open('diseno/verificaciones/ui_runtime.txt','w')
begin
  load_data('Data/Scripts.rxdata').each do |row|
    next if row[1]=='Main'
    source=Zlib::Inflate.inflate(row[2])
    source.force_encoding('UTF-8') if source.respond_to?(:force_encoding)
    eval(source,TOPLEVEL_BINDING,row[1])
  end
  Graphics.resize_screen(640,480) if ENV['VACAS_UI_ALTO']=='480'
  $ui_report[:lienzo]=[Vacas_HD.w,Vacas_HD.h]
  $ui_report[:fuente]={:nombre=>Font.default_name,:tamano=>Font.default_size}
  $ui_report[:fuente][:arial_disponible]=Font.exist?('Arial') if Font.respond_to?(:exist?)
  sample=Bitmap.new(640,64)
  $ui_report[:fuente][:muestras]=[14,16,20].collect do |size|
    sample.font.size=size; m=sample.text_size('Ágj ¿Dónde está la salida?')
    {:tamano=>size,:ancho=>m.width,:alto=>m.height}
  end
  sample.dispose
  $ui_report[:api]={:snap_to_bitmap=>Graphics.respond_to?(:snap_to_bitmap),
    :screenshot=>Graphics.respond_to?(:screenshot),:to_file=>Bitmap.instance_methods.collect { |m| m.to_s }.include?('to_file')}
  module Vacas_Config
    def self.save; raise 'Prohibido escribir Vacas.cfg'; end
  end
  class Scene_Save
    def on_decision(*args); raise 'Prohibido guardar partidas'; end
  end
  class Bitmap
    attr_reader :ui_draws
    alias ui_native_clear clear
    def clear
      @ui_draws=[]; ui_native_clear
    end
    alias ui_native_draw_text draw_text
    def draw_text(*args)
      if args[0].is_a?(Rect)
        r=args[0]; s=args[1].to_s
      else
        r=Rect.new(*args[0,4]); s=args[4].to_s
      end
      m=text_size(s); @ui_draws ||= []
      @ui_draws.push({:texto=>s,:rect=>[r.x,r.y,r.width,r.height],
        :medida=>[m.width,m.height],:fuente=>font.name,:tamano=>font.size}) unless s.strip==''
      ui_native_draw_text(*args)
    end
    alias ui_native_blt blt
    def blt(x,y,source,rect,*args)
      # VN copia el texto a un bitmap auxiliar antes de revelarlo por glifos.
      if x==0 && y==0 && rect.x==0 && rect.y==0 && rect.width==width && rect.height==height
        @ui_draws=(source.ui_draws || []).clone
      end
      ui_native_blt(x,y,source,rect,*args)
    end
  end
  module Input
    class << self
      alias ui_native_update update
      def update
        ui_native_update
        return unless $ui_scene_name
        $ui_tick+=1
        if $ui_tick==80
          ui_capture($ui_scene_name)
          ui_windows.each do |w|
            next unless w.is_a?(Window_Selectable) && w.visible && w.active
            total=w.instance_variable_get(:@item_max) || 0
            if total>w.page_row_max && total>0
              w.index=total-1; w.update
              ui_capture($ui_scene_name+'_ultima_fila')
            end
          end
        end
        if $ui_tick>=82
          if $ui_current_cine
            $ui_current_cine.instance_variable_set(:@terminada,true)
            $scene=nil if $scene.equal?($ui_current_cine)
          else
            $scene=nil
          end
        end
      end
      def trigger?(key); ($ui_keys || []).include?(key); end
      def repeat?(key); trigger?(key); end
      def press?(key); false; end
    end
  end
  # Las cinematica de un final se ejecutan dentro de otra escena: fotografiar
  # tanto el plano como la tarjeta final, sin confundir sus ciclos de vida.
  class Scene_VacasCine
    alias ui_capture_cine_main main
    def main
      nested=!$scene.equal?(self)
      old_name=$ui_scene_name
      if nested
        $ui_scene_name=old_name+'_cinematica'; $ui_tick=0
      end
      $ui_current_cine=self
      ui_capture_cine_main
    ensure
      $ui_current_cine=nil
      if nested
        $ui_scene_name=old_name; $ui_tick=0
      end
    end
  end
  # Fixtures exclusivamente en memoria; no crear ni reemplazar Save*.rxdata.
  class Window_SaveFile
    alias ui_fixture_initialize initialize
    def initialize(index,filename)
      ui_fixture_initialize(index,filename)
      if $ui_slots
        @file_exist=index<$ui_slots
        @game_variables=Game_Variables.new; @game_variables[1]=87
        @total_sec=999999*3600+59*60; @time_stamp=Time.local(2026,11,11,23,59)
        refresh
      end
    end
  end
  def ui_windows
    result=[]
    ObjectSpace.each_object(Window_Base) { |w| result.push(w) unless w.disposed? }
    result
  end
  def ui_capture(name)
    Graphics.transition(0); 3.times { Graphics.update }
    path='diseno/capturas/interfaz/ui_'+Vacas_HD.h.to_s+'_'+name+'.png'
    if $ui_report[:api][:snap_to_bitmap] && $ui_report[:api][:to_file]
      b=Graphics.snap_to_bitmap; b.to_file(path); b.dispose
    elsif $ui_report[:api][:screenshot]
      Graphics.screenshot(path)
    else
      raise 'No existe una API PNG compatible'
    end
    rows=[]
    ui_windows.each do |w|
      next unless w.visible && w.contents
      b=w.instance_variable_get(:@vn_full) || w.contents; errors=[]
      errors.push('ventana_fuera_del_lienzo') if w.x<0 || w.y<0 || w.x+w.width>Vacas_HD.w || w.y+w.height>Vacas_HD.h
      visible=(b.ui_draws || []).select { |d| r=d[:rect]; r[1]+r[3]>w.oy && r[1]<w.oy+w.height-32 }
      visible.each do |d|
        r=d[:rect]; m=d[:medida]
        errors.push('texto_mas_alto_que_fila: '+d[:texto]) if m[1]>r[3]
        errors.push('texto_mas_ancho_que_rectangulo: '+d[:texto]) if m[0]>r[2]
        errors.push('texto_fuera_del_bitmap: '+d[:texto]) if r[0]<0 || r[0]+[m[0],r[2]].min>b.width || r[1]<0 || r[1]+r[3]>b.height
        top=r[1]+(r[3]-m[1])/2
        errors.push('texto_recortado_por_ventana: '+d[:texto]) if top<w.oy || top+m[1]>w.oy+w.height-32
      end
      rect=w.cursor_rect
      heights={}
      visible.each { |d| heights[d[:rect][1]]=[heights[d[:rect][1]] || 0,d[:rect][3]].max }
      if rect.width>0 && (rect.x<0 || rect.y<0 || rect.x+rect.width>w.width-32 || rect.y+rect.height>w.height-32)
        errors.push('cursor_fuera_de_filas_visibles')
      end
      rows.push({:clase=>w.class.to_s,:ventana=>[w.x,w.y,w.width,w.height],
        :contenido=>[b.width,b.height],:alto_disponible=>w.height-32,:scroll_y=>w.oy,
        :altos_de_linea=>heights.values,:alto_de_lineas_total=>heights.values.inject(0) { |sum,h| sum+h },
        :lineas_visibles=>visible.collect { |d| d[:rect][1] }.uniq.size,
        :cursor=>[rect.x,rect.y,rect.width,rect.height],:textos=>visible,:errores=>errors.uniq})
    end
    overlaps=[]
    rows.each_with_index do |a,i|
      rows[(i+1)..-1].to_a.each do |b|
        x,y,w,h=a[:ventana]; xx,yy,ww,hh=b[:ventana]
        overlaps.push([a[:clase],b[:clase]]) if x<xx+ww && xx<x+w && y<yy+hh && yy<y+h
      end
    end
    sprites=[]
    ObjectSpace.each_object(Sprite) do |s|
      next if s.disposed? || !s.visible || !s.bitmap || s.bitmap.disposed?
      draws=s.bitmap.ui_draws || []
      next if draws.empty?
      errors=[]
      observations=[]
      draws.each do |d|
        r=d[:rect]; m=d[:medida]
        errors.push('texto_fuera_de_fila: '+d[:texto]) if m[1]>r[3] || m[0]>r[2]
        if r[1]<0 || r[1]+r[3]>s.bitmap.height
          if $scene.is_a?(Scene_CreditosJuego)
            observations.push('Entrada/salida intencional del texto durante el desplazamiento de creditos')
          else
            errors.push('texto_fuera_de_bitmap: '+d[:texto])
          end
        end
      end
      sprites.push({:clase=>s.class.to_s,:posicion=>[s.x,s.y],:textos=>draws,:errores=>errors.uniq,:observaciones=>observations.uniq})
    end
    $ui_report[:pantallas].push({:nombre=>name,:png=>path,:ventanas=>rows,:sprites=>sprites,:solapes_para_revision=>overlaps})
    $ui_log.puts('CAPTURA '+name); $ui_log.flush
  end
  def ui_case(name)
    $ui_log.puts('INICIO '+name); $ui_log.flush
    yield
  rescue Exception => e
    $ui_report[:errores].push(name+': '+e.message); $ui_log.puts(e.backtrace)
  ensure
    $ui_scene_name=nil; $ui_keys=[]
    ui_windows.each { |w| w.dispose }
  end
  def ui_scene(name,scene)
    ui_case(name) { $ui_tick=0; $ui_scene_name=name; $scene=scene; scene.main }
  end
  ui_scene('titulo',Scene_Title.new)
  Scene_Title.new.command_new_game; $scene=Scene_Map.new
  $game_actors[1].name='Steven del pasillo interminable y la puerta cerrada'
  (1...$data_items.size).each { |id| $game_party.gain_item(id,12) if $data_items[id] }
  $data_items[1].name='Objeto de nombre extraordinariamente largo para revisar el inventario'
  $data_items[1].description=('Una descripcion extensa que debe continuar en otra linea sin desaparecer. '*6)
  [1,4].each do |count|
    $ui_slots=count
    [0,3].each do |selected|
      $game_temp.last_file_index=selected
      ui_scene('cargar_'+count.to_s+'_ranuras_pagina_'+(selected/2+1).to_s,Scene_Load.new)
    end
  end
  $ui_slots=4; $game_temp.last_file_index=0; ui_scene('guardar',Scene_Save.new); $ui_slots=nil
  [[Scene_Menu.new,'pausa'],[Scene_Item.new,'objetos'],
   [Scene_VacasJournal.new(:notas),'notas'],[Scene_VacasJournal.new(:estado),'estado'],
   [Scene_VacasSettings.new,'ajustes'],[Scene_End.new,'salir'],
   [Scene_Aviso.new,'aviso'],[Scene_FekaIntro.new,'intro'],
   [Scene_VacasCine.new(Vacas_Cine::APERTURA),'nueva_partida'],
   [Scene_FinActo.new(1),'tarjeta_acto'],[Scene_Gameover.new,'gameover'],
   [Scene_VacasCredits.new,'creditos'],[Scene_CreditosJuego.new,'creditos_juego'],
   [Scene_FinalVacas.new(1),'fin']].each { |scene,name| ui_scene(name,scene) }
  (3..6).each { |acto| ui_scene('tarjeta_acto_'+acto.to_s,Scene_VacasCine.new(Vacas_Cine.tarjeta(acto))) }
  $game_temp.shop_goods=[[0,1],[0,2],[1,1],[2,1]]; ui_scene('tienda',Scene_Shop.new)
  ui_case('hud') do
    $scene=Scene_Map.new; $game_map.setup(1); $game_player.moveto(10,10)
    $game_switches[Vacas::SW_HUD_OCULTO]=false
    sprites=Spriteset_Map.new; sprites.update; ui_capture('hud_cordura_bateria'); sprites.dispose
  end
  long=('El pasillo sigue abierto y las voces no dejan de llamar desde la oscuridad. '*3)
  cases=[['mensaje','Texto normal. '+long,0],['mensaje_nombre','\\NOMBRE[Nombre de prueba muy largo]'+long,0],
    ['vn_izquierda','\\P[steven_miedo]\\L\\NOMBRE[Steven]'+([long]*4).join("\n"),0],
    ['vn_derecha','\\P[steven_miedo]\\R\\NOMBRE[Steven]'+([long]*4).join("\n"),0]]
  (2..4).each { |n| cases.push(['elecciones_'+n.to_s,([long]*n).join("\n"),n]) }
  cases.each do |name,text,count|
    ui_case(name) do
      $game_temp.message_text=text+"\n"; $game_temp.choice_start=count>0 ? 0 : 99
      $game_temp.choice_max=count; $game_temp.choice_proc=Proc.new { |n| }
      w=Window_Message.new; 20.times { w.update; Graphics.update }
      $ui_keys=[Input::C]; w.update; $ui_keys=[]; w.update; ui_capture(name)
      (1...count).each do |i|
        w.index=i; w.update; ui_capture(name+'_opcion_'+(i+1).to_s)
      end
      page=1
      while w.instance_variable_get(:@ui_pages).to_a.size>0
        raise 'Paginacion no progresa' if page>64
        $ui_keys=[Input::C]; w.update; $ui_keys=[]; w.update
        $ui_keys=[Input::C]; w.update; $ui_keys=[]; w.update
        page+=1; ui_capture(name+'_pagina_'+page.to_s)
      end
      w.dispose
    end
  end
  ui_case('numeros') do
    $game_temp.message_text="Introduce el numero.\n"
    $game_temp.num_input_start=1; $game_temp.num_input_variable_id=99; $game_temp.num_input_digits_max=8
    w=Window_Message.new; 20.times { w.update; Graphics.update }; ui_capture('numeros'); w.dispose
  end
  $game_temp.battle_troop_id=8; $game_temp.battle_can_lose=true; $game_temp.battle_can_escape=true
  $game_temp.battle_proc=Proc.new { |n| }; $game_temp.map_bgm=$game_system.playing_bgm
  ui_scene('batalla',Scene_Battle.new)
  ui_case('batalla_ventanas') do
    $game_troop.setup(8)
    c=Window_VacasBattleCommand.new(['Afrontar','Poner nombre','Respirar','Objetos'])
    c.x=8; c.y=Vacas_HD.bottom(146)
    s=Window_BattleStatus.new; e=Window_VacasEnemies.new; e.update
    ui_capture('batalla_comandos_objetivos_estado'); e.visible=false
    h=Window_Help.new; h.set_text(long); ui_capture('batalla_ayuda')
    [c,s,e,h].each { |w| w.dispose }
    r=Window_BattleResult.new(99999,99999,[$data_items[1]])
    ui_capture('batalla_resultado'); r.dispose
  end
  # Todas las clases estandar, incluidas las que no abre la pausa personalizada.
  $game_temp.in_battle=false
  actor=$game_party.actors[0]
  args={'Window_Base'=>[0,0,640,360],'Window_Selectable'=>[0,0,200,128],
    'Window_Command'=>[240,['Primera opcion','Segunda opcion']],
    'Window_VacasCommand'=>[24,24,240,['Primera opcion','Segunda opcion']],
    'Window_VacasPanel'=>[24,24,240,128],'Window_VacasBattleCommand'=>[['Uno','Dos']],
    'Window_BattleResult'=>[99999,99999,[]],'Window_Skill'=>[actor],
    'Window_SkillStatus'=>[actor],'Window_Status'=>[actor],'Window_EquipLeft'=>[actor],
    'Window_EquipRight'=>[actor],'Window_EquipItem'=>[actor,0],
    'Window_SaveFile'=>[0,'Save1.rxdata'],'Window_ShopBuy'=>[$game_temp.shop_goods],
    'Window_NameEdit'=>[actor,8],'Window_InputNumber'=>[8]}
  classes=[]
  ObjectSpace.each_object(Class) { |c| classes.push(c) if c.to_s =~ /^Window_/ }
  classes.sort { |a,b| a.to_s<=>b.to_s }.each do |klass|
    ui_case('ventana_'+klass.to_s) do
      w=klass.new(*(args[klass.to_s] || [])); w.visible=true
      if w.is_a?(Window_ShopNumber); w.set($data_items[1],99,999999); end
      if w.is_a?(Window_ShopStatus); w.item=$data_weapons[1]; end
      ui_capture('ventana_'+klass.to_s); w.dispose
    end
  end
rescue Exception => e
  $ui_report[:errores].push(e.class.to_s+': '+e.message); $ui_log.puts(e.backtrace)
ensure
  $ui_report[:estado]='capturas_generadas_requieren_revision_visual'
  File.open('diseno/verificaciones/auditoria_ui.json','w') { |f| f.write(JSON.pretty_generate($ui_report)) }
  $ui_log.close
end
