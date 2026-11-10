# Suite nativa. No guarda partidas ni configuracion; todas las entradas son simuladas.
def hd_step(label)
  $hd_log.puts('INICIO '+label); $hd_log.flush
  yield
  $hd_log.puts('OK '+label)
rescue Exception => e
  $hd_log.puts('FALLO '+label+': '+e.class.to_s+': '+e.message)
  $hd_log.puts(e.backtrace)
ensure
  $hd_log.flush
end
def hd_capture(name)
  Graphics.transition(0)
  3.times { Graphics.update }
  b=Graphics.snap_to_bitmap
  b.to_file('diseno/capturas/interfaz/hd_'+name+'.png')
  b.dispose
  Vacas_HD_Check.inspect_windows(name,$hd_log)
end
def hd_scene(scene,name)
  $hd_tick=0; $hd_name=name; $scene=scene
  scene.main
ensure
  $hd_name=nil; $hd_keys=[]
end
hd_step('resolucion') do
  raise 'Motor no detectado' unless Vacas_HD.mkxp?
  raise 'Lienzo incorrecto' unless [Graphics.width,Graphics.height]==[640,360]
  $hd_log.puts('Ruby '+RUBY_VERSION+' System='+System.methods.sort.inspect)
end
hd_step('titulo') { hd_scene(Scene_Title.new,'titulo') }
# Inicializacion de partida original; se omite la reproduccion de la cinematica.
hd_step('partida') { Scene_Title.new.command_new_game; $scene=Scene_Map.new }
hd_step('guardado_existente') do
  File.open('Save1.rxdata','rb') { |f| Marshal.load(f) until f.eof? }
end
[
 [Scene_Menu.new,'pausa'],[Scene_VacasSettings.new(:titulo),'ajustes'],
 [Scene_VacasJournal.new(:estado),'estado'],[Scene_VacasJournal.new(:notas),'notas'],
 [Scene_VacasCredits.new,'creditos'],[Scene_CreditosJuego.new,'creditos_juego'],
 [Scene_Item.new,'objetos'],[Scene_Load.new,'cargar'],[Scene_Gameover.new,'gameover'],
 [Scene_Aviso.new,'aviso'],[Scene_FekaIntro.new,'feka'],
 [Scene_VacasCine.new(Vacas_Cine::APERTURA),'cine']
].each { |row| hd_step(row[1]) { hd_scene(row[0],row[1]) } }
hd_step('escenas_estandar') do
  $game_temp.name_actor_id=1; $game_temp.name_max_char=8
  $game_temp.shop_goods=[]
  [Scene_Skill.new(0),Scene_Equip.new(0),Scene_Status.new(0),
    Scene_Shop.new,Scene_Name.new,Scene_Debug.new,Scene_End.new,
    Scene_PruebaActo6.new(false),Scene_FinalVacas.new(1)].each do |scene|
    hd_scene(scene,'estandar_'+scene.class.to_s)
  end
end
hd_step('mapa_dialogo') do
  $hd_name=nil; $game_map.setup(1); $game_player.moveto(10,10)
  $game_switches[Vacas::SW_HUD_OCULTO]=false; $scene=Scene_Map.new
  ss=Spriteset_Map.new; ss.update; hd_capture('mapa')
  $game_temp.message_text='\\P[steven_miedo]\\NOMBRE[Steven]La luz sigue encendida.'+"\n"+'Y el pasillo no termina.'
  $game_temp.message_window_showing=true
  w=Window_Message.new
  20.times { w.update; Graphics.update }
  $hd_keys=[Input::C]; w.update; $hd_keys=[]; w.update
  hd_capture('dialogo')
ensure
  w.dispose if w && !w.disposed?
  ss.dispose if ss
  $game_temp.message_text=nil; $game_temp.message_window_showing=false
end
hd_step('minijuegos') do
  [Vacas_Corte,Vacas_Cinta,Vacas_Noria].each do |klass|
    m=klass.new(3); hd_capture(klass.to_s.downcase); m.dispose
  end
end
hd_step('combate') do
  $game_temp.battle_troop_id=8; $game_temp.battle_can_lose=true
  $game_temp.battle_can_escape=true; $game_temp.battle_proc=Proc.new { |n| }
  $game_temp.map_bgm=$game_system.playing_bgm
  $scene=Scene_Battle.new
  hd_scene($scene,'combate')
end
hd_step('camara_todos_mapas') do
  Dir.glob('Data/Map[0-9]*.rxdata').sort.each do |path|
    mid=File.basename(path)[/\d+/].to_i; $game_map.setup(mid)
    [[0,0],[$game_map.width-1,$game_map.height-1]].each do |xy|
      $game_player.moveto(xy[0],xy[1])
      max=[$game_map.height*128-Vacas_HD.h*4,0].max
      raise 'scroll '+mid.to_s unless $game_map.display_y.between?(0,max)
      hud=Sprite_Veneno.new; hud.update
      if hud.visible && $game_player.screen_x.between?(hud.x,hud.x+hud.bitmap.width) &&
          $game_player.screen_y.between?(hud.y,hud.y+hud.bitmap.height)
        raise 'HUD tapa al jugador en '+mid.to_s
      end
      hud.bitmap.dispose; hud.dispose
    end
  end
end
hd_step('ventanas_todas_clases') do
  $game_temp.in_battle=false
  actor=$game_party.actors[0]
  args={
    'Window_Base'=>[0,0,Vacas_HD.w,Vacas_HD.h],
    'Window_Selectable'=>[0,0,200,100], 'Window_Command'=>[200,['Uno','Dos']],
    'Window_VacasCommand'=>[24,24,200,['Uno','Dos']],
    'Window_VacasPanel'=>[24,24,200,100],
    'Window_VacasBattleCommand'=>[['Uno','Dos']],
    'Window_BattleResult'=>[0,0,[]], 'Window_Skill'=>[actor],
    'Window_SkillStatus'=>[actor], 'Window_Status'=>[actor],
    'Window_EquipLeft'=>[actor], 'Window_EquipRight'=>[actor],
    'Window_EquipItem'=>[actor,0], 'Window_SaveFile'=>[0,'Save1.rxdata'],
    'Window_ShopBuy'=>[[]], 'Window_NameEdit'=>[actor,8], 'Window_InputNumber'=>[2]
  }
  classes=[]
  ObjectSpace.each_object(Class) { |c| classes.push(c) if c.to_s =~ /^Window_/ }
  classes.sort { |a,b| a.to_s <=> b.to_s }.each do |klass|
    window=nil
    begin
      window=klass.new(*(args[klass.to_s] || [])); window.visible=true
      Vacas_HD_Check.inspect_windows(klass.to_s,$hd_log)
      $hd_log.puts('VENTANA OK '+klass.to_s)
    ensure
      window.dispose if window && !window.disposed?
    end
  end
end
$hd_log.puts('FIN SUITE'); $hd_log.flush
