# === VACAS: FUENTE VIGENTE ===
# Script: Vacas_Interfaz | posición en Scripts.rxdata: 100 (base 0)
# Función: Interfaz, configuración, audio, HUD, combate y guardado.
# Motor: RGSS1 / Ruby 1.8. Fuente extraída del juego instalado.
# Switches simbólicos: SW_HUD_OCULTO
# Switches con ID literal: 115
# Variables simbólicas: ninguna
# Variables con ID literal: 52
# Los índices calculados y rangos se describen en el código y en docs/sistemas/.
# Instalación: herramientas/comun/instalar_scripts.mjs (primero, vista previa).
# === FIN CABECERA ===
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
    :titulo=>[:bgm,"vacas_titulo",56,100,""],
    :combate=>[:bgm,"vacas_combate",60,100,""],
    :jefe=>[:bgm,"vacas_jefe",64,100,""],
    :persecucion=>[:bgm,"vacas_persecucion",64,100,"Pasos cada vez mas cerca"],
    :gameover=>[:bgm,"vacas_gameover",45,100,""],
    :exploracion_del_piso=>[:bgm,"bgm_piso_exploracion",42,100,""],
    :exploracion_matadero=>[:bgm,"bgm_matadero_exploracion",42,100,""],
    :camaras_frias=>[:bgm,"bgm_camaras_frias",42,100,""],
    :lucy_laboratorio=>[:bgm,"bgm_lucy_laboratorio",42,100,""],
    :alcantarillas_bgm=>[:bgm,"bgm_alcantarillas",42,100,""],
    :camara_de_la_manada=>[:bgm,"bgm_camara_manada",42,100,""],
    :tema_tranquilo_seguro_tv=>[:bgm,"bgm_tv_segura",42,100,""],
    :alterna_calle_de_noche_suspense=>[:bgm,"bgm_extra_calle_noche",42,100,""],
    :alterna_camaras_drone=>[:bgm,"bgm_extra_estacion_drone",42,100,""],
    :alterna_sotano_lab=>[:bgm,"bgm_extra_sotano",42,100,""],
    :alterna_laboratorio_tenso=>[:bgm,"bgm_extra_tension_lab",42,100,""],
    :alterna_alcantarillas_drone=>[:bgm,"bgm_extra_dark_drone",42,100,""],
    :alterna_batalla=>[:bgm,"bgm_extra_batalla_rpg",42,100,""],
    :menu=>[:bgs,"vacas_menu",26,100,"Zumbido electrico"],
    :piso=>[:bgs,"vacas_piso",26,100,"La television tras la pared"],
    :matadero=>[:bgs,"vacas_matadero",26,100,"La cadena sigue girando"],
    :camaras=>[:bgs,"vacas_camaras",26,100,"Compresor lejano"],
    :laboratorio=>[:bgs,"vacas_laboratorio",26,100,"Cristal y fluorescentes"],
    :alcantarillas=>[:bgs,"vacas_alcantarillas",26,100,"Agua bajo los pies"],
    :manada=>[:bgs,"vacas_manada",26,100,"Respiraciones en la oscuridad"],
    :estatica_de_tv_vieja=>[:bgs,"bgs_tv_estatica",26,100,"Estatica de TV vieja"],
    :tv_amortiguada_estatica_filtrada=>[:bgs,"bgs_tv_estatica_amortiguada",26,100,"TV amortiguada (estatica filtrada)"],
    :zumbido_de_nevera=>[:bgs,"bgs_nevera_zumbido",26,100,"Zumbido de nevera"],
    :reloj_tictac_piso=>[:bgs,"bgs_reloj_tictac",26,100,"Reloj tictac (piso)"],
    :lluvia_en_ventana_calle_noche=>[:bgs,"bgs_lluvia_ventana",26,100,"Lluvia en ventana / calle noche"],
    :lluvia_exterior=>[:bgs,"bgs_lluvia_calle",26,100,"Lluvia exterior"],
    :cadenas_y_transportador=>[:bgs,"bgs_matadero_cadenas",26,100,"Cadenas y transportador"],
    :fabrica_oscura=>[:bgs,"bgs_matadero_fabrica_oscura",26,100,"Fabrica oscura"],
    :compresor_de_camara_fria=>[:bgs,"bgs_camara_compresor",26,100,"Compresor de camara fria"],
    :goteo_y_eco=>[:bgs,"bgs_alcantarilla_goteo",26,100,"Goteo y eco"],
    :agua_corriendo=>[:bgs,"bgs_agua_corriente",26,100,"Agua corriendo"],
    :edificio_abandonado_ambiente=>[:bgs,"bgs_edificio_abandonado",26,100,"Edificio abandonado (ambiente)"],
    :ambiente_hueco_alcantarilla_camara=>[:bgs,"bgs_mazmorra_eco",26,100,"Ambiente hueco (alcantarilla/camara)"],
    :fluorescente_zumbido_electrico=>[:bgs,"bgs_fluorescente_zumbido",26,100,"Fluorescente / zumbido electrico"],
    :generador_maquina=>[:bgs,"bgs_generador",26,100,"Generador / maquina"],
    :latido_lento=>[:bgs,"bgs_latido_lento",26,100,"Latido lento"],
    :latido_rapido=>[:bgs,"bgs_latido_rapido",26,100,"Latido rapido"],
    :respiracion_pesada=>[:bgs,"bgs_respiracion_pesada",26,100,"Respiracion pesada"],
    :respiracion_de_horror=>[:bgs,"bgs_respiracion_horror",26,100,"Respiracion de horror"],
    :corral_de_ganado_mugidos_y_arrastre=>[:bgs,"bgs_corral_ganado",26,100,"Corral de ganado (mugidos y arrastre)"],
    :victoria=>[:me,"vacas_victoria",56,100,""],
    :derrota=>[:me,"vacas_derrota",56,100,""],
    :nivel_logro=>[:me,"me_logro",56,100,""],
    :game_over_alterno=>[:me,"me_game_over_triste",56,100,""],
    :cursor=>[:se,"ui_cursor",42,100,""],
    :confirmar=>[:se,"ui_confirmar",42,100,""],
    :cancelar=>[:se,"ui_cancelar",42,100,""],
    :error=>[:se,"ui_error",42,100,""],
    :golpe=>[:se,"mente_golpe",52,100,"Golpe seco"],
    :susto=>[:se,"mente_susto",62,100,"Golpe repentino"],
    :paso_baldosa=>[:se,"paso_baldosa",24,100,""],
    :paso_metal=>[:se,"paso_metal",24,100,""],
    :paso_agua=>[:se,"paso_agua",24,100,""],
    :puerta=>[:se,"puerta_oxido",52,100,"Una puerta chirria"],
    :paso_concreto=>[:se,"se_paso_concreto_1",24,100,""],
    :paso_concreto_2=>[:se,"se_paso_concreto_2",24,100,""],
    :paso_concreto_3=>[:se,"se_paso_concreto_3",24,100,""],
    :paso_baldosa_1=>[:se,"se_paso_baldosa_1",24,100,""],
    :paso_baldosa_2=>[:se,"se_paso_baldosa_2",24,100,""],
    :paso_baldosa_3=>[:se,"se_paso_baldosa_3",24,100,""],
    :paso_agua_1=>[:se,"se_paso_agua_1",24,100,""],
    :paso_agua_2=>[:se,"se_paso_agua_2",24,100,""],
    :paso_agua_3=>[:se,"se_paso_agua_3",24,100,""],
    :paso_rejilla_metal=>[:se,"se_paso_rejilla_metal_1",24,100,""],
    :paso_rejilla_metal_2=>[:se,"se_paso_rejilla_metal_2",24,100,""],
    :paso_rejilla_metal_3=>[:se,"se_paso_rejilla_metal_3",24,100,""],
    :paso_madera=>[:se,"se_paso_madera_1",24,100,""],
    :paso_madera_2=>[:se,"se_paso_madera_2",24,100,""],
    :paso_madera_3=>[:se,"se_paso_madera_3",24,100,""],
    :puerta_madera_abrir=>[:se,"se_puerta_madera_abrir",52,100,""],
    :puerta_madera_cerrar=>[:se,"se_puerta_madera_cerrar",52,100,""],
    :puerta_metal_pesada_abrir=>[:se,"se_puerta_metal_abrir",52,100,""],
    :puerta_metal_pesada_cerrar=>[:se,"se_puerta_metal_cerrar",52,100,""],
    :puerta_de_hierro=>[:se,"se_puerta_hierro",52,100,""],
    :crujido_de_puerta=>[:se,"se_puerta_crujido",52,100,""],
    :manija_de_puerta_trabada=>[:se,"se_puerta_manija_trabada",52,100,""],
    :destrabar_puerta=>[:se,"se_puerta_destrabar",52,100,""],
    :cuchilla_corte_de_carne=>[:se,"se_cuchillada_1",52,100,""],
    :cuchilla_corte_de_carne_2=>[:se,"se_cuchillada_2",52,100,""],
    :hueso_quebrado=>[:se,"se_corte_hueso",52,100,""],
    :hueso_crujiendo=>[:se,"se_hueso_seco",52,100,""],
    :sierra_sobre_hueso_sierra_ruido_mecanico=>[:se,"se_sierra_hueso",52,100,""],
    :chapoteo_gore=>[:se,"se_chapoteo_1",52,100,""],
    :chapoteo_gore_2=>[:se,"se_chapoteo_2",52,100,""],
    :desgarro_de_carne=>[:se,"se_desgarro_carne",52,100,""],
    :sonido_viscoso=>[:se,"se_viscoso",52,100,""],
    :cadena_gancho=>[:se,"se_gancho_cadena",52,100,""],
    :gancho_metalico=>[:se,"se_gancho_metal",52,100,""],
    :mugido_de_vaca=>[:se,"se_mugido_1",52,100,""],
    :mugido_de_vaca_2=>[:se,"se_mugido_2",52,100,""],
    :mugido_de_vaca_3=>[:se,"se_mugido_3",52,100,""],
    :mugido_angustiado=>[:se,"se_mugido_angustia",52,100,""],
    :mugido_grave_distorsionado=>[:se,"se_mugido_grave",52,100,""],
    :llave_recoger=>[:se,"se_llave_recoger",52,100,""],
    :llaves_tintineo=>[:se,"se_llaves_tintineo",52,100,""],
    :papel_nota=>[:se,"se_papel_nota_1",52,100,""],
    :papel_nota_2=>[:se,"se_papel_nota_2",52,100,""],
    :interruptor_de_luz=>[:se,"se_interruptor_luz",52,100,""],
    :linterna_clic=>[:se,"se_linterna_clic",52,100,""],
    :tv_encender_estatica_con_entrada=>[:se,"se_tv_encender",52,100,""],
    :tv_apagar_estatica_con_corte=>[:se,"se_tv_apagar",52,100,""],
    :frasco_de_vidrio=>[:se,"se_frasco_vidrio_1",52,100,""],
    :frasco_de_vidrio_2=>[:se,"se_frasco_vidrio_2",52,100,""],
    :recoger_objeto=>[:se,"se_objeto_recoger",52,100,""],
    :combate_golpe_a_carne=>[:se,"se_golpe_carne",52,100,""],
    :combate_golpe_pesado=>[:se,"se_golpe_pesado",52,100,""],
    :combate_fallo_silbido=>[:se,"se_fallo_aire",52,100,""],
    :curar=>[:se,"se_curar",52,100,""],
    :estado_veneno=>[:se,"se_estado_veneno",52,100,""],
    :cordura_baja_stinger=>[:se,"se_cordura_baja",52,100,""],
    :muerte_de_enemigo=>[:se,"se_enemigo_muere",52,100,""],
    :screamer_1=>[:se,"se_screamer_1",62,100,""],
    :screamer_2=>[:se,"se_screamer_2",62,100,""],
    :screamer_3=>[:se,"se_screamer_3",62,100,""],
    :nivel_victoria_breve=>[:se,"se_nivel_victoria",52,100,""]
  }
  LEGACY = {
    "001-Battle01"=>:combate,
    "001-System01"=>:cursor,
    "001-Victory01"=>:victoria,
    "001-Wind01"=>:piso,
    "002-System02"=>:confirmar,
    "002-Wind02"=>:corral_de_ganado_mugidos_y_arrastre,
    "003-System03"=>:cancelar,
    "004-System04"=>:error,
    "005-Defeat01"=>:derrota,
    "005-Rain01"=>:lluvia_exterior,
    "005-System05"=>:error,
    "006-System06"=>:recoger_objeto,
    "007-System07"=>:combate_fallo_silbido,
    "008-System08"=>:muerte_de_enemigo,
    "009-System09"=>:muerte_de_enemigo,
    "010-System10"=>:confirmar,
    "011-System11"=>:combate_fallo_silbido,
    "012-System12"=>:combate_fallo_silbido,
    "013-Move01"=>:crujido_de_puerta,
    "015-Jump01"=>:combate_fallo_silbido,
    "015-Mystery01"=>:derrota,
    "015-Quake01"=>:matadero,
    "016-Drips01"=>:alcantarillas,
    "016-Shock01"=>:victoria,
    "018-Darkness01"=>:estatica_de_tv_vieja,
    "024-Door01"=>:puerta_madera_abrir,
    "026-Door03"=>:puerta_metal_pesada_abrir,
    "032-Switch01"=>:interruptor_de_luz,
    "036-Dungeon02"=>:combate,
    "040-Knock01"=>:puerta,
    "041-Knock02"=>:manija_de_puerta_trabada,
    "042-Knock03"=>:crujido_de_puerta,
    "044-Chest01"=>:recoger_objeto,
    "045-Push01"=>:gancho_metalico,
    "046-Book01"=>:papel_nota,
    "050-Explosion03"=>:combate_golpe_a_carne,
    "051-Explosion04"=>:combate_golpe_a_carne,
    "052-Cannon01"=>:combate_golpe_pesado,
    "057-Wrong01"=>:error,
    "058-Slow01"=>:titulo,
    "064-Slow07"=>:titulo,
    "070-Animal05"=>:mugido_angustiado,
    "086-Action01"=>:combate_fallo_silbido,
    "087-Action02"=>:combate_fallo_silbido,
    "088-Action03"=>:combate_fallo_silbido,
    "089-Attack01"=>:combate_golpe_a_carne,
    "091-Attack03"=>:combate_golpe_a_carne,
    "092-Attack04"=>:susto,
    "093-Attack05"=>:cuchilla_corte_de_carne,
    "094-Attack06"=>:combate_golpe_a_carne,
    "098-Attack10"=>:combate_golpe_a_carne,
    "099-Attack11"=>:combate_golpe_a_carne,
    "100-Attack12"=>:combate_golpe_a_carne,
    "101-Attack13"=>:combate_golpe_a_carne,
    "102-Attack14"=>:combate_golpe_a_carne,
    "103-Attack15"=>:combate_golpe_a_carne,
    "104-Attack16"=>:combate_golpe_a_carne,
    "105-Heal01"=>:curar,
    "106-Heal02"=>:curar,
    "107-Heal03"=>:curar,
    "108-Heal04"=>:curar,
    "109-Heal05"=>:curar,
    "110-Heal06"=>:curar,
    "111-Heal07"=>:curar,
    "112-Heal08"=>:curar,
    "113-Remedy01"=>:curar,
    "114-Remedy02"=>:curar,
    "115-Raise01"=>:curar,
    "116-Raise02"=>:curar,
    "117-Fire01"=>:combate_golpe_a_carne,
    "118-Fire02"=>:combate_golpe_a_carne,
    "119-Fire03"=>:combate_golpe_a_carne,
    "120-Ice01"=>:chapoteo_gore,
    "121-Ice02"=>:chapoteo_gore,
    "122-Ice03"=>:chapoteo_gore,
    "123-Thunder01"=>:combate_golpe_pesado,
    "124-Thunder02"=>:combate_golpe_a_carne,
    "125-Thunder03"=>:combate_golpe_a_carne,
    "126-Water01"=>:chapoteo_gore,
    "127-Water02"=>:chapoteo_gore,
    "128-Water03"=>:chapoteo_gore,
    "129-Earth01"=>:combate_golpe_a_carne,
    "130-Earth02"=>:combate_golpe_a_carne,
    "131-Earth03"=>:combate_golpe_a_carne,
    "132-Wind01"=>:combate_fallo_silbido,
    "133-Wind02"=>:combate_fallo_silbido,
    "134-Wind03"=>:combate_fallo_silbido,
    "135-Light01"=>:combate_golpe_a_carne,
    "136-Light02"=>:combate_golpe_a_carne,
    "137-Light03"=>:combate_golpe_a_carne,
    "138-Darkness01"=>:cordura_baja_stinger,
    "139-Darkness02"=>:cordura_baja_stinger,
    "140-Darkness03"=>:golpe,
    "141-Burst01"=>:combate_golpe_a_carne,
    "142-Burst02"=>:combate_golpe_a_carne,
    "143-Support01"=>:curar,
    "144-Support02"=>:curar,
    "145-Support03"=>:curar,
    "146-Support04"=>:curar,
    "147-Support05"=>:curar,
    "148-Support06"=>:curar,
    "149-Support07"=>:curar,
    "150-Support08"=>:curar,
    "151-Support09"=>:curar,
    "152-Support10"=>:curar,
    "153-Support11"=>:curar,
    "154-Support12"=>:curar,
    "155-Support13"=>:curar,
    "156-Support14"=>:curar,
    "157-Skill01"=>:combate_golpe_a_carne,
    "158-Skill02"=>:combate_golpe_a_carne,
    "159-Skill03"=>:combate_golpe_a_carne,
    "160-Skill04"=>:combate_golpe_a_carne,
    "161-Skill05"=>:combate_golpe_a_carne,
    "162-Skill06"=>:combate_golpe_a_carne,
    "163-Skill07"=>:combate_golpe_a_carne,
    "164-Skill08"=>:combate_golpe_a_carne,
    "165-Skill09"=>:combate_golpe_a_carne,
    "166-Skill10"=>:combate_golpe_a_carne,
    "167-Skill11"=>:combate_golpe_a_carne,
    "168-Skill12"=>:combate_golpe_a_carne,
    "169-Skill13"=>:combate_golpe_a_carne,
    "170-Skill14"=>:combate_golpe_a_carne,
    "171-Skill15"=>:combate_golpe_a_carne,
    "172-Skill16"=>:combate_golpe_a_carne,
    "173-Skill17"=>:combate_golpe_a_carne,
    "174-Skill18"=>:combate_golpe_a_carne,
    "175-Skill19"=>:combate_golpe_a_carne,
    "176-Skill20"=>:combate_golpe_a_carne,
    "177-Skill21"=>:combate_golpe_a_carne,
    "178-Skill22"=>:combate_golpe_a_carne,
    "179-Skill23"=>:combate_golpe_a_carne,
    "180-Skill24"=>:combate_golpe_a_carne
  }
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
  MAP_AUDIO = {
    1=>[:piso,:exploracion_del_piso,:piso,:baldosa],
    2=>[:piso,:exploracion_del_piso,:piso,:baldosa],
    3=>[:piso,:exploracion_del_piso,:edificio_abandonado_ambiente,:baldosa],
    4=>[:piso,:alterna_calle_de_noche_suspense,:lluvia_exterior,:concreto],
    5=>[:matadero,:exploracion_matadero,:lluvia_exterior,:concreto],
    6=>[:matadero,:exploracion_matadero,:zumbido_de_nevera,:baldosa],
    7=>[:matadero,:exploracion_matadero,:corral_de_ganado_mugidos_y_arrastre,:concreto],
    8=>[:matadero,:exploracion_matadero,:matadero,:metal],
    9=>[:camaras,:camaras_frias,:camaras,:metal],
    10=>[:matadero,:exploracion_matadero,:reloj_tictac_piso,:madera],
    11=>[:matadero,:exploracion_matadero,:cadenas_y_transportador,:metal],
    12=>[:laboratorio,:tema_tranquilo_seguro_tv,:reloj_tictac_piso,:madera],
    13=>[:laboratorio,:lucy_laboratorio,:zumbido_de_nevera,:baldosa],
    14=>[:laboratorio,:alterna_sotano_lab,:edificio_abandonado_ambiente,:concreto],
    15=>[:laboratorio,:lucy_laboratorio,:fluorescente_zumbido_electrico,:baldosa],
    16=>[:laboratorio,:alterna_laboratorio_tenso,:laboratorio,:baldosa],
    17=>[:alcantarillas,:alcantarillas_bgm,:alcantarillas,:concreto],
    18=>[:alcantarillas,:alterna_alcantarillas_drone,:goteo_y_eco,:concreto],
    19=>[:alcantarillas,:alcantarillas_bgm,:agua_corriendo,:agua],
    20=>[:manada,:camara_de_la_manada,:manada,:concreto],
    21=>[:manada,:tema_tranquilo_seguro_tv,:ambiente_hueco_alcantarilla_camara,:concreto]
  }
  # Tags de terreno XP 1..5: agua, metal, madera, concreto, baldosa.
  TERRAIN_STEPS = {1=>:agua,2=>:metal,3=>:madera,4=>:concreto,5=>:baldosa}
  STEP_KEYS = {
    :baldosa=>[:paso_baldosa_1,:paso_baldosa_2,:paso_baldosa_3],
    :metal=>[:paso_rejilla_metal,:paso_rejilla_metal_2,:paso_rejilla_metal_3],
    :agua=>[:paso_agua_1,:paso_agua_2,:paso_agua_3],
    :madera=>[:paso_madera,:paso_madera_2,:paso_madera_3],
    :concreto=>[:paso_concreto,:paso_concreto_2,:paso_concreto_3]
  }
  def self.zone
    (MAP_AUDIO[$game_map.map_id] || MAP_AUDIO[2])[0]
  end
  def self.chasing?
    [10,90,120,122].any? { |id| $game_switches[id] }
  end
  def self.map_audio
    row=MAP_AUDIO[$game_map.map_id]; return unless row
    keys=[chasing? ? :persecucion : row[1],row[2]]
    keys.each do |key|
      audio=TABLE[key]; current=Audio.vacas_tracks[audio[0]]
      expected='Audio/'+audio[0].to_s.upcase+'/'+audio[1]
      play(key) unless current && current[0]==expected
    end
  end
  def self.footstep(player)
    surface=TERRAIN_STEPS[$game_map.terrain_tag(player.x,player.y)]
    surface ||= (MAP_AUDIO[$game_map.map_id] || MAP_AUDIO[2])[3]
    keys=STEP_KEYS[surface]; return unless keys
    @step_variant=(@step_variant || -1)+1
    play(keys[@step_variant % keys.size])
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
        base=File.basename(name.to_s).sub(/\.[^.]+$/, '')
        key=Vacas_Audio::LEGACY[base]
        key=Vacas_Audio.screamer if base=='092-Attack04' && Vacas_Audio.screamer
        if [:llave_recoger,:papel_nota,:recoger_objeto,:frasco_de_vidrio].include?(key)
          return unless Vacas_Audio.allow_pickup?
        end
        if key && kind==:bgs && $game_map && Vacas_Audio::MAP_AUDIO[$game_map.map_id]
          key=Vacas_Audio::MAP_AUDIO[$game_map.map_id][2]
        end
        if key
          row=Vacas_Audio::TABLE[key]
          name='Audio/'+kind.to_s.upcase+'/'+row[1]
          volume=[volume,row[2]].min; pitch=row[3]
        end
        vacas_tracks[kind]=[name,volume,pitch] if [:bgm,:bgs].include?(kind)
        if key==:susto || base==Vacas_Audio::TABLE[:susto][1] || base.index('se_screamer_')==0 || key.to_s.index('screamer_')==0
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
    Vacas_HD.cover(@back)
    @back.zoom_x*=1.03; @back.zoom_y*=1.03
    @veil=Plane.new
    @veil.bitmap=RPG::Cache.picture('ui_fog')
    @veil.opacity=32; @veil.z=1
    @tick=0
  end
  def update
    @tick+=1
    @back.x=(Vacas_HD.w-@back.bitmap.width*@back.zoom_x)/2-10+Math.sin(@tick/150.0)*7
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
    y=Vacas_HD.y(40)
    contents.font.size=18
    lines.each do |s|
      line=''
      s.split(' ').each do |word|
        candidate=line=='' ? word : line+' '+word
        if contents.text_size(candidate).width>contents.width && line!=''
          Vacas_UI.text(contents,0,y,contents.width,line,18);y+=Vacas_HD.y(26);line=word
        else
          line=candidate
        end
      end
      Vacas_UI.text(contents,0,y,contents.width,line,18);y+=Vacas_HD.y(30)
    end
  end
end

class Window_VacasCommand < Window_Selectable
  def initialize(x,y,w,commands)
    super(x,y,w,[commands.size*32+32,Vacas_HD.h-y-8].min)
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
    @logo=Sprite.new; @logo.z=5; @logo.bitmap=Bitmap.new(Vacas_HD.w,Vacas_HD.h)
    b=@logo.bitmap
    Vacas_UI.text(b,42,Vacas_HD.y(48),500,'V A C A S',64)
    Vacas_UI.text(b,46,Vacas_HD.y(132),500,'LA CARNE RECUERDA',17,Vacas_UI::MINT)
    Vacas_UI.text(b,28,Vacas_HD.bottom(28),600,'Z / Intro: elegir     Esc: volver     Flechas: mover',16)
    @command_window=Window_VacasCommand.new(350,Vacas_HD.y(145),248,
      ['Nueva partida','Continuar','Ajustes','Creditos','Salir'])
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
    when 3; Vacas_Audio.play(:confirmar); $scene=Scene_VacasCredits.new
    when 4; command_shutdown
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
    @panel=Window_VacasPanel.new(32,8,Vacas_HD.w-64,80)
    @panel.lines('AJUSTES',''.split)
    @list=Window_VacasCommand.new(32,88,Vacas_HD.w-64,LABELS)
    @list.height=Vacas_HD.h-144
    @hint=Window_VacasPanel.new(32,Vacas_HD.bottom(48),Vacas_HD.w-64,48)
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
    @command_window=Window_VacasCommand.new(24,104,208,
      ['Objetos','Estado / Cordura','Notas','Guardar','Ajustes','Salir'])
    @command_window.height=[224,Vacas_HD.h-168].min
    @command_window.index=[@menu_index || 0,5].min
    @command_window.disable_item(3) unless Vacas_UI.save_allowed?
    @top=Window_VacasPanel.new(24,8,Vacas_HD.w-48,88)
    infos=load_data('Data/MapInfos.rxdata')
    @top.lines('PAUSA / '+infos[$game_map.map_id].name,[])
    @tasks=Window_VacasPanel.new(244,104,Vacas_HD.w-268,Vacas_HD.h-160)
    @tasks.lines('Lo que queda',Vacas.tareas.collect { |t| (t[1] ? '+ ' : '> ')+t[0] })
    @foot=Window_VacasPanel.new(24,Vacas_HD.bottom(56),Vacas_HD.w-48,56)
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
    @panel=Window_VacasPanel.new(24,8,Vacas_HD.w-48,88)
    @panel.lines(@mode==:estado ? 'ESTADO / EL CUERPO RECUERDA' : 'NOTAS / LO QUE HAS GUARDADO',[])
    if @mode==:estado
      a=$game_party.actors[0]
      @body=Window_VacasPanel.new(24,104,Vacas_HD.w-48,Vacas_HD.h-112)
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
      @body=Window_VacasCommand.new(24,104,Vacas_HD.w-48,labels)
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
    @text=Window_VacasPanel.new(32,24,Vacas_HD.w-64,144)
    @text.lines('LA CARNE NO OLVIDA',['Aun puedes volver a intentarlo.'])
    @list=Window_VacasCommand.new(32,Vacas_HD.bottom(144),300,['Cargar partida','Volver al titulo','Salir'])
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
    super(8,Vacas_HD.bottom(146),160,146)
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
      self.x=86; self.y=Vacas_HD.bottom(154); self.zoom_x=0.6; self.zoom_y=0.6
    end
  end
end

class Window_Item
  alias ui_inventory_initialize initialize
  def initialize
    ui_inventory_initialize
    self.x=24;self.y=104;self.width=Vacas_HD.w-48
    self.height=Vacas_HD.h-self.y-8
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
    self.x=24; self.y=64+@file_index*((Vacas_HD.h-64)/4); self.width=Vacas_HD.w-48; self.height=(Vacas_HD.h-64)/4-4
    self.contents.dispose;self.contents=Bitmap.new(Vacas_HD.w-80,56);refresh
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
    Vacas_Audio.map_audio if $scene.is_a?(Scene_Map)
  end
end

# HUD integrado, sin duplicar la bateria del acto IV.
class Sprite_Veneno
  def initialize
    super(nil)
    self.bitmap=Bitmap.new(240,84); self.x=14; self.y=Vacas_HD.bottom(90); self.z=4000
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
    Vacas_Audio.screamer=[:screamer_1,:screamer_2,:screamer_3][(id-1)%3]
    begin
      ui_susto(id)
    ensure
      Vacas_Audio.screamer=nil
    end
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
        @ui_view=Viewport.new(0,0,Vacas_HD.w,Vacas_HD.h); @ui_view.z=99999
        @ui_overlay=Sprite.new(@ui_view); @ui_overlay.bitmap=Bitmap.new(Vacas_HD.w,Vacas_HD.h)
        @ui_caption=Sprite.new(@ui_view); @ui_caption.bitmap=Bitmap.new(Vacas_HD.w,40)
        @ui_caption.y=0; @ui_caption.z=2
      end
      value=Vacas_Config.get(:brillo)
      if @ui_brightness!=value
        @ui_brightness=value
        @ui_overlay.bitmap.fill_rect(0,0,Vacas_HD.w,Vacas_HD.h,value<100 ? Color.new(0,0,0) : Color.new(255,245,220))
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
    super(176,Vacas_HD.bottom(146),Vacas_HD.w-176,146)
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
  def initialize; super(Vacas_HD.w-224,4,216,100); @values={}; end
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
    self.x=86;self.y=Vacas_HD.bottom(154) if self.actor
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
    @actor_command_window.x=8;@actor_command_window.y=Vacas_HD.bottom(146)
    @actor_command_window.active=false;@actor_command_window.visible=false
    ui_start_phase1
  end
  alias ui_battle_main main
  def main
    @ui_enemies=Window_VacasEnemies.new
    @ui_entry=Sprite.new; @ui_entry.z=9000; @ui_entry.bitmap=Bitmap.new(Vacas_HD.w,Vacas_HD.h)
    @ui_entry.bitmap.fill_rect(0,0,Vacas_HD.w,Vacas_HD.h,Color.new(6,12,12,220))
    Vacas_UI.text(@ui_entry.bitmap,90,Vacas_HD.y(200),460,'LA IMAGEN TE ENCUENTRA',30,Vacas_UI::INK,1)
    @ui_entry_ticks=48
    zone=Vacas_Audio.zone
    zone=:manada if $game_temp.battle_troop_id==17
    zone=:laboratorio if (10..13).include?($game_temp.battle_troop_id)
    $game_map.battleback_name='ui_'+zone.to_s
    Vacas_Audio.play([9,13,17,21,35,36,37].include?($game_temp.battle_troop_id) ? :jefe : :combate)
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
      @actor_command_window.x=8; @actor_command_window.y=Vacas_HD.bottom(146)
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
    card=Window_VacasPanel.new(104,(Vacas_HD.h-156)/2,432,156); card.z=10000
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
    self.x=104; self.y=(Vacas_HD.h-156)/2; self.width=432; self.height=156
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
    @damage_sprite.bitmap=b; @damage_sprite.ox=90; @damage_sprite.oy=Vacas_HD.y(40)
    @damage_sprite.x=self.x; @damage_sprite.y=self.y-self.oy/2
    @damage_sprite.z=3000; @damage_duration=40
  end
end

# Ganchos de ambiente y pasos. La frecuencia no depende de la velocidad de FPS.
class Game_Map
  alias ui_map_autoplay autoplay
  def autoplay
    ui_map_autoplay
    Vacas_Audio.map_audio
  end
end
class Game_Player
  alias ui_player_increase_steps increase_steps
  def increase_steps
    ui_player_increase_steps
    @ui_steps=(@ui_steps || 0)+1
    now=Graphics.frame_count
    if @ui_steps%3==0 && !@move_route_forcing && !$game_temp.message_window_showing &&
        (!@ui_step_frame || now<@ui_step_frame || now-@ui_step_frame>=12)
      Vacas_Audio.footstep(self); @ui_step_frame=now
    end
  end
end

module Vacas_Audio
  CREDITS = [
    "# Creditos de audio - Vacas",
    "",
    "Todos los archivos estan convertidos a OGG Vorbis (los 10 SE requeridos tambien en WAV 16-bit mono con el mismo nombre). Solo licencias CC0 / dominio publico / CC-BY 3.0 o 4.0.",
    "Los archivos CC-BY exigen atribucion: incluir este listado (o equivalente) en los creditos del juego.",
    "",
    "Atribucion de musica (Kevin MacLeod): \"Titulo\" Kevin MacLeod (incompetech.com), licenciada bajo Creative Commons: By Attribution 4.0 https://creativecommons.org/licenses/by/4.0/",
    "",
    "Modificaciones comunes: conversion a OGG, recorte, normalizacion (BGM/BGS/ME a -16 LUFS aprox., SE a pico -1 dB), recorte de silencios en SE, fundido corto y crossfade de bucle en BGM/BGS. Las mezclas (BGS compuestos) combinan varias grabaciones.",
    "",
    "## BGM",
    "",
    "### bgm/vacas_titulo.ogg (destino: Audio/BGM/vacas_titulo.ogg)",
    "- Que es: Titulo (86.0 s, 1001 KB, bucle: si)",
    "- Fuente: Ghost Story - autor: Kevin MacLeod - https://incompetech.com/music/royalty-free/mp3-royaltyfree/Ghost%20Story.mp3 - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "### bgm/vacas_combate.ogg (destino: Audio/BGM/vacas_combate.ogg)",
    "- Que es: Combate normal (96.0 s, 1193 KB, bucle: si)",
    "- Fuente: Killing Time - autor: Kevin MacLeod - https://incompetech.com/music/royalty-free/mp3-royaltyfree/Killing%20Time.mp3 - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "### bgm/vacas_jefe.ogg (destino: Audio/BGM/vacas_jefe.ogg)",
    "- Que es: Jefe (Rey, Diagnostico, Pastor) (135.0 s, 1597 KB, bucle: si)",
    "- Fuente: Giant Wyrm - autor: Kevin MacLeod - https://incompetech.com/music/royalty-free/mp3-royaltyfree/Giant%20Wyrm.mp3 - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 5s",
    "",
    "### bgm/vacas_persecucion.ogg (destino: Audio/BGM/vacas_persecucion.ogg)",
    "- Que es: Persecucion (52.0 s, 701 KB, bucle: si)",
    "- Fuente: Chase - autor: Kevin MacLeod - https://incompetech.com/music/royalty-free/mp3-royaltyfree/Chase.mp3 - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "### bgm/vacas_gameover.ogg (destino: Audio/BGM/vacas_gameover.ogg)",
    "- Que es: Game over (46.0 s, 594 KB, bucle: si)",
    "- Fuente: Cryptic Sorrow - autor: Kevin MacLeod - https://incompetech.com/music/royalty-free/mp3-royaltyfree/Cryptic%20Sorrow.mp3 - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "### bgm/bgm_piso_exploracion.ogg",
    "- Que es: Exploracion del piso (116.0 s, 1476 KB, bucle: si)",
    "- Fuente: Ossuary 5 - Rest - autor: Kevin MacLeod - https://incompetech.com/music/royalty-free/mp3-royaltyfree/Ossuary%205%20-%20Rest.mp3 - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "### bgm/bgm_matadero_exploracion.ogg",
    "- Que es: Exploracion matadero (116.0 s, 1412 KB, bucle: si)",
    "- Fuente: Crypto - autor: Kevin MacLeod - https://incompetech.com/music/royalty-free/mp3-royaltyfree/Crypto.mp3 - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "### bgm/bgm_camaras_frias.ogg",
    "- Que es: Camaras frias (116.0 s, 1503 KB, bucle: si)",
    "- Fuente: Deep Haze - autor: Kevin MacLeod - https://incompetech.com/music/royalty-free/mp3-royaltyfree/Deep%20Haze.mp3 - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "### bgm/bgm_lucy_laboratorio.ogg",
    "- Que es: Lucy / laboratorio (116.0 s, 1688 KB, bucle: si)",
    "- Fuente: Darkling - autor: Kevin MacLeod - https://incompetech.com/music/royalty-free/mp3-royaltyfree/Darkling.mp3 - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "### bgm/bgm_alcantarillas.ogg",
    "- Que es: Alcantarillas (116.0 s, 1358 KB, bucle: si)",
    "- Fuente: Gathering Darkness - autor: Kevin MacLeod - https://incompetech.com/music/royalty-free/mp3-royaltyfree/Gathering%20Darkness.mp3 - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "### bgm/bgm_camara_manada.ogg",
    "- Que es: Camara de la manada (115.0 s, 1253 KB, bucle: si)",
    "- Fuente: Heart of the Beast - autor: Kevin MacLeod - https://incompetech.com/music/royalty-free/mp3-royaltyfree/Heart%20of%20the%20Beast.mp3 - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 5s",
    "",
    "### bgm/bgm_tv_segura.ogg",
    "- Que es: Tema tranquilo \"seguro\" (TV) (116.0 s, 1601 KB, bucle: si)",
    "- Fuente: Lullaby (pack: Lullaby) - autor: Pro Sensory - https://opengameart.org/content/lullaby-0 - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "### bgm/bgm_extra_calle_noche.ogg",
    "- Que es: Alterna: calle de noche / suspense (116.0 s, 1471 KB, bucle: si)",
    "- Fuente: (Night of the Streets [Horror/Suspense]) - autor: nene - https://opengameart.org/content/night-of-the-streets-horrorsuspense - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "### bgm/bgm_extra_estacion_drone.ogg",
    "- Que es: Alterna: camaras / drone (115.0 s, 1129 KB, bucle: si)",
    "- Fuente: (Station Drone 2) - autor: Tozan - https://opengameart.org/content/station-drone-2 - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 5s",
    "",
    "### bgm/bgm_extra_sotano.ogg",
    "- Que es: Alterna: sotano / lab (115.0 s, 1036 KB, bucle: si)",
    "- Fuente: (Telos Creepy Cage Street) - autor: Tozan - https://opengameart.org/content/telos-creepy-cage-street - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 5s",
    "",
    "### bgm/bgm_extra_tension_lab.ogg",
    "- Que es: Alterna: laboratorio tenso (116.0 s, 1097 KB, bucle: si)",
    "- Fuente: (tension and distress) - autor: allen yatsura - https://opengameart.org/content/tension-and-distress - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "### bgm/bgm_extra_dark_drone.ogg",
    "- Que es: Alterna: alcantarillas drone (115.0 s, 1119 KB, bucle: si)",
    "- Fuente: (Dark Ambient Drone) - autor: Tsorthan Grove - https://opengameart.org/content/dark-ambient-drone - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 5s",
    "",
    "### bgm/bgm_extra_batalla_rpg.ogg",
    "- Que es: Alterna: batalla (96.0 s, 1322 KB, bucle: si)",
    "- Fuente: Battle RPG Theme Var (pack: Boss Battle Theme) - autor: CleytonKauffman - https://opengameart.org/content/boss-battle-theme - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 4s",
    "",
    "## BGS",
    "",
    "### bgs/vacas_menu.ogg (destino: Audio/BGS/vacas_menu.ogg)",
    "- Que es: Pausa / menu (tenue) (28.0 s, 241 KB, bucle: si)",
    "- Fuente: Inside of refrigerator.ogg - autor: stephan - https://commons.wikimedia.org/wiki/File%3AInside_of_refrigerator.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG; filtro/tono aplicado (lowpass=f=900); crossfade de bucle 2s",
    "",
    "### bgs/vacas_piso.ogg (destino: Audio/BGS/vacas_piso.ogg)",
    "- Que es: Piso y calle: lluvia en ventana + reloj (72.0 s, 643 KB, bucle: si)",
    "- Fuente: Rain against the window.ogg - autor: cori - https://commons.wikimedia.org/wiki/File%3ARain_against_the_window.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Fuente: Clock ticking.ogg - autor: natalie - https://commons.wikimedia.org/wiki/File%3AClock_ticking.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Fuente: Inside of refrigerator.ogg - autor: stephan - https://commons.wikimedia.org/wiki/File%3AInside_of_refrigerator.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: mezcla de 3 fuentes; recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "### bgs/vacas_matadero.ogg (destino: Audio/BGS/vacas_matadero.ogg)",
    "- Que es: Matadero: cintas, cadenas, prensa (87.0 s, 849 KB, bucle: si)",
    "- Fuente: WWS Conveyorbelt.ogg - autor: Work With Sounds / Konrad Gutkowski - https://commons.wikimedia.org/wiki/File%3AWWS_Conveyorbelt.ogg - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Fuente: WWS Bucketchain.ogg - autor: Work With Sounds / Konrad Gutkowski - https://commons.wikimedia.org/wiki/File%3AWWS_Bucketchain.ogg - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Fuente: WWS Punchingpress.ogg - autor: Work With Sounds / Konrad Gutkowski - https://commons.wikimedia.org/wiki/File%3AWWS_Punchingpress.ogg - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: mezcla de 3 fuentes; recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "### bgs/vacas_camaras.ogg (destino: Audio/BGS/vacas_camaras.ogg)",
    "- Que es: Camaras frias: compresor (87.0 s, 870 KB, bucle: si)",
    "- Fuente: WWS Compressor.ogg - autor: Work With Sounds / Torsten Nilsson - https://commons.wikimedia.org/wiki/File%3AWWS_Compressor.ogg - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Fuente: Inside of refrigerator.ogg - autor: stephan - https://commons.wikimedia.org/wiki/File%3AInside_of_refrigerator.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: mezcla de 2 fuentes; recorte/normalizacion/OGG; filtro/tono aplicado (lowpass=f=500); crossfade de bucle 3s",
    "",
    "### bgs/vacas_laboratorio.ogg (destino: Audio/BGS/vacas_laboratorio.ogg)",
    "- Que es: Laboratorio: zumbido electrico + latido + reloj (58.0 s, 517 KB, bucle: si)",
    "- Fuente: Electric noise (pack: 12 Ambient Machine Sounds) - autor: bart - https://opengameart.org/content/12-ambient-machine-sounds - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Fuente: heartbeat slow (pack: Heartbeat sounds) - autor: bart - https://opengameart.org/content/heartbeat-sounds - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Clock ticking.ogg - autor: natalie - https://commons.wikimedia.org/wiki/File%3AClock_ticking.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: mezcla de 3 fuentes; recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "### bgs/vacas_alcantarillas.ogg (destino: Audio/BGS/vacas_alcantarillas.ogg)",
    "- Que es: Alcantarillas: goteo con eco + agua corriendo (58.0 s, 591 KB, bucle: si)",
    "- Fuente: atmosbasement (pack: Dripping water loop) - autor: qubodup - https://opengameart.org/content/dripping-water-loop - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: bg_water_running (pack: Running Water - background noise) - autor: HippoDevelopment - https://opengameart.org/content/running-water-background-noise - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: mezcla de 2 fuentes; recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "### bgs/vacas_manada.ogg (destino: Audio/BGS/vacas_manada.ogg)",
    "- Que es: Manada: respiracion, mugidos lejanos, corral (57.0 s, 366 KB, bucle: si)",
    "- Fuente: Ambience_MonstersBelly_00.mp3 (pack: Horror Sound Effects Library) - autor: Little Robot Sound Factory - https://opengameart.org/content/horror-sound-effects-library - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Fuente: Cow in Vezo.ogg - autor: Gasybeaugosse2020 - https://commons.wikimedia.org/wiki/File%3ACow_in_Vezo.ogg - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Cow in Antefasy.wav - autor: Gasybeaugosse2020 - https://commons.wikimedia.org/wiki/File%3ACow_in_Antefasy.wav - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Katalalan.ogg - autor: Sabak5388 - https://commons.wikimedia.org/wiki/File%3AKatalalan.ogg - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Heavy breathing 3.ogg - autor: ezwa - https://commons.wikimedia.org/wiki/File%3AHeavy_breathing_3.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: mezcla de 5 fuentes; recorte/normalizacion/OGG; filtro/tono aplicado (lowpass=f=1800, lowpass=f=2500,asetrate=33000,aresample=44100, asetrate=36000,aresample=44100, asetrate=34000,aresample=44100, lowpass=f=1200); crossfade de bucle 3s",
    "",
    "### bgs/bgs_tv_estatica.ogg",
    "- Que es: Estatica de TV vieja (28.0 s, 225 KB, bucle: si)",
    "- Fuente: ScatterNoise1 (pack: Static) - autor: xhunterko - https://opengameart.org/content/static - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "### bgs/bgs_tv_estatica_amortiguada.ogg",
    "- Que es: TV amortiguada (estatica filtrada) (28.0 s, 165 KB, bucle: si)",
    "- Fuente: ScatterNoise1 (pack: Static) - autor: xhunterko - https://opengameart.org/content/static - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; filtro/tono aplicado (lowpass=f=700); crossfade de bucle 2s",
    "",
    "### bgs/bgs_nevera_zumbido.ogg",
    "- Que es: Zumbido de nevera (28.0 s, 260 KB, bucle: si)",
    "- Fuente: Inside of refrigerator.ogg - autor: stephan - https://commons.wikimedia.org/wiki/File%3AInside_of_refrigerator.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "### bgs/bgs_reloj_tictac.ogg",
    "- Que es: Reloj tictac (piso) (28.0 s, 267 KB, bucle: si)",
    "- Fuente: Clock ticking.ogg - autor: natalie - https://commons.wikimedia.org/wiki/File%3AClock_ticking.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "### bgs/bgs_lluvia_ventana.ogg",
    "- Que es: Lluvia en ventana / calle noche (77.0 s, 643 KB, bucle: si)",
    "- Fuente: Rain against the window.ogg - autor: cori - https://commons.wikimedia.org/wiki/File%3ARain_against_the_window.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "### bgs/bgs_lluvia_calle.ogg",
    "- Que es: Lluvia exterior (57.0 s, 538 KB, bucle: si)",
    "- Fuente: amb_rain_loop_1 (pack: AMB Rain Loop 1) - autor: Kresiek The Furry - https://opengameart.org/content/amb-rain-loop-1 - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "### bgs/bgs_matadero_cadenas.ogg",
    "- Que es: Cadenas y transportador (72.0 s, 648 KB, bucle: si)",
    "- Fuente: WWS Two-chainconveyorinoperation.ogg - autor: Work With Sounds / Technical Museum of Slovenia - https://commons.wikimedia.org/wiki/File%3AWWS_Two-chainconveyorinoperation.ogg - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "### bgs/bgs_matadero_fabrica_oscura.ogg",
    "- Que es: Fabrica oscura (97.0 s, 815 KB, bucle: si)",
    "- Fuente: dark factory (pack: Dark Factory) - autor: bart - https://opengameart.org/content/dark-factory - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "### bgs/bgs_camara_compresor.ogg",
    "- Que es: Compresor de camara fria (87.0 s, 869 KB, bucle: si)",
    "- Fuente: WWS Compressor.ogg - autor: Work With Sounds / Torsten Nilsson - https://commons.wikimedia.org/wiki/File%3AWWS_Compressor.ogg - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "### bgs/bgs_alcantarilla_goteo.ogg",
    "- Que es: Goteo y eco (18.1 s, 192 KB, bucle: si)",
    "- Fuente: atmosbasement (pack: Dripping water loop) - autor: qubodup - https://opengameart.org/content/dripping-water-loop - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "### bgs/bgs_agua_corriente.ogg",
    "- Que es: Agua corriendo (38.0 s, 353 KB, bucle: si)",
    "- Fuente: bg_water_running (pack: Running Water - background noise) - autor: HippoDevelopment - https://opengameart.org/content/running-water-background-noise - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "### bgs/bgs_edificio_abandonado.ogg",
    "- Que es: Edificio abandonado (ambiente) (65.0 s, 619 KB, bucle: si)",
    "- Fuente: abandonedbuildingambience (pack: Abandoned Building Ambience) - autor: tcarisland - https://opengameart.org/content/abandoned-building-ambience - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "### bgs/bgs_mazmorra_eco.ogg",
    "- Que es: Ambiente hueco (alcantarilla/camara) (87.0 s, 809 KB, bucle: si)",
    "- Fuente: dungeon_ambient_1 (pack: Loopable Dungeon Ambience) - autor: JaggedStone - https://opengameart.org/content/loopable-dungeon-ambience - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "### bgs/bgs_fluorescente_zumbido.ogg",
    "- Que es: Fluorescente / zumbido electrico (28.0 s, 251 KB, bucle: si)",
    "- Fuente: Electric noise (pack: 12 Ambient Machine Sounds) - autor: bart - https://opengameart.org/content/12-ambient-machine-sounds - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "### bgs/bgs_generador.ogg",
    "- Que es: Generador / maquina (27.9 s, 197 KB, bucle: si)",
    "- Fuente: loop_generator_1 (pack: Generator (loop)) - autor: YCbCr - https://opengameart.org/content/generator-loop - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "### bgs/bgs_latido_lento.ogg",
    "- Que es: Latido lento (29.0 s, 103 KB, bucle: si)",
    "- Fuente: heartbeat_slow_0 (pack: Heartbeat sounds) - autor: bart - https://opengameart.org/content/heartbeat-sounds - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 1s",
    "",
    "### bgs/bgs_latido_rapido.ogg",
    "- Que es: Latido rapido (29.0 s, 138 KB, bucle: si)",
    "- Fuente: heartbeat_fast_0 (pack: Heartbeat sounds) - autor: bart - https://opengameart.org/content/heartbeat-sounds - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 1s",
    "",
    "### bgs/bgs_respiracion_pesada.ogg",
    "- Que es: Respiracion pesada (43.0 s, 350 KB, bucle: si)",
    "- Fuente: Heavy breathing 3.ogg - autor: ezwa - https://commons.wikimedia.org/wiki/File%3AHeavy_breathing_3.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "### bgs/bgs_respiracion_horror.ogg",
    "- Que es: Respiracion de horror (29.0 s, 174 KB, bucle: si)",
    "- Fuente: horrorbreathing (pack: horror breathing) - autor: primbal - https://opengameart.org/content/horror-breathing - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade de bucle 1s",
    "",
    "### bgs/bgs_corral_ganado.ogg",
    "- Que es: Corral de ganado (mugidos y arrastre) (38.0 s, 244 KB, bucle: si)",
    "- Fuente: Ambience_MonstersBelly_00.mp3 (pack: Horror Sound Effects Library) - autor: Little Robot Sound Factory - https://opengameart.org/content/horror-sound-effects-library - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Fuente: Cow in Vezo.ogg - autor: Gasybeaugosse2020 - https://commons.wikimedia.org/wiki/File%3ACow_in_Vezo.ogg - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Katalalan.ogg - autor: Sabak5388 - https://commons.wikimedia.org/wiki/File%3AKatalalan.ogg - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Cow in Antefasy.wav - autor: Gasybeaugosse2020 - https://commons.wikimedia.org/wiki/File%3ACow_in_Antefasy.wav - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: mezcla de 4 fuentes; recorte/normalizacion/OGG; filtro/tono aplicado (lowpass=f=1500); crossfade de bucle 2s",
    "",
    "## ME",
    "",
    "### me/vacas_victoria.ogg (destino: Audio/ME/vacas_victoria.ogg)",
    "- Que es: Victoria (6.0 s, 72 KB, bucle: no)",
    "- Fuente: Jingle_Win_00.mp3 (pack: Horror Sound Effects Library) - autor: Little Robot Sound Factory - https://opengameart.org/content/horror-sound-effects-library - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### me/vacas_derrota.ogg (destino: Audio/ME/vacas_derrota.ogg)",
    "- Que es: Derrota / retirada mental (4.9 s, 56 KB, bucle: no)",
    "- Fuente: Jingle_Lose_00.mp3 (pack: Horror Sound Effects Library) - autor: Little Robot Sound Factory - https://opengameart.org/content/horror-sound-effects-library - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### me/me_logro.ogg",
    "- Que es: Nivel / logro (3.1 s, 38 KB, bucle: no)",
    "- Fuente: Jingle_Achievement_00.mp3 (pack: Horror Sound Effects Library) - autor: Little Robot Sound Factory - https://opengameart.org/content/horror-sound-effects-library - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### me/me_game_over_triste.ogg",
    "- Que es: Game over alterno (6.0 s, 74 KB, bucle: no)",
    "- Fuente: (Sad game over) - autor: Emma_MA - https://opengameart.org/content/sad-game-over - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "## SE",
    "",
    "### se/ui_cursor.ogg (destino: Audio/SE/ui_cursor.wav)",
    "- Que es: Cursor (0.1 s, 5 KB, bucle: no)",
    "- Fuente: menu tick (pack: Menu select tick) - autor: mikeask - https://opengameart.org/content/menu-select-tick - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/ui_confirmar.ogg (destino: Audio/SE/ui_confirmar.wav)",
    "- Que es: Confirmar (0.2 s, 5 KB, bucle: no)",
    "- Fuente: Menu Choice (pack: Menu Choice) - autor: Sudocolon - https://opengameart.org/content/menu-choice - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/ui_cancelar.ogg (destino: Audio/SE/ui_cancelar.wav)",
    "- Que es: Cancelar (clic analogico) (0.2 s, 5 KB, bucle: no)",
    "- Fuente: light_switch_turn_off (pack: Light Switch Turn On And Off SFX) - autor: FunnyDude - https://opengameart.org/content/light-switch-turn-on-and-off-sfx-0 - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/ui_error.ogg (destino: Audio/SE/ui_error.wav)",
    "- Que es: Error (golpe de madera apagado) (0.2 s, 4 KB, bucle: no)",
    "- Fuente: wood_hit_03 (pack: 100 CC0 metal and wood SFX) - autor: rubberduck - https://opengameart.org/content/100-cc0-metal-and-wood-sfx - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; filtro/tono aplicado (lowpass=f=900)",
    "",
    "### se/mente_golpe.ogg (destino: Audio/SE/mente_golpe.wav)",
    "- Que es: Golpe mental / impacto (0.1 s, 4 KB, bucle: no)",
    "- Fuente: squishsplat_impact (pack: Squish Sounds Effects) - autor: EZduzziteh - https://opengameart.org/content/squish-sounds-effects - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; filtro/tono aplicado (lowpass=f=3000)",
    "",
    "### se/mente_susto.ogg (destino: Audio/SE/mente_susto.wav)",
    "- Que es: Susto (1.1 s, 13 KB, bucle: no)",
    "- Fuente: horrorghostscream (pack: Phantom Scream) - autor: VishwaJai - https://opengameart.org/content/phantom-scream - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/paso_baldosa.ogg (destino: Audio/SE/paso_baldosa.wav)",
    "- Que es: Paso baldosa (0.1 s, 4 KB, bucle: no)",
    "- Fuente: tile 1 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/paso_metal.ogg (destino: Audio/SE/paso_metal.wav)",
    "- Que es: Paso metal (0.3 s, 6 KB, bucle: no)",
    "- Fuente: metal 1 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/paso_agua.ogg (destino: Audio/SE/paso_agua.wav)",
    "- Que es: Paso agua (0.2 s, 6 KB, bucle: no)",
    "- Fuente: water 1 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/puerta_oxido.ogg (destino: Audio/SE/puerta_oxido.wav)",
    "- Que es: Puerta oxidada (1.4 s, 16 KB, bucle: no)",
    "- Fuente: creaky-door-hinge (pack: Creaky Door Hinge Spooky) - autor: w.forster.1@gmail.com - https://opengameart.org/content/creaky-door-hinge-spooky - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_concreto_1.ogg",
    "- Que es: Paso concreto (0.1 s, 4 KB, bucle: no)",
    "- Fuente: boots 0 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_concreto_2.ogg",
    "- Que es: Paso concreto (0.1 s, 4 KB, bucle: no)",
    "- Fuente: boots 2 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_concreto_3.ogg",
    "- Que es: Paso concreto (0.1 s, 4 KB, bucle: no)",
    "- Fuente: boots 4 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_baldosa_1.ogg",
    "- Que es: Paso baldosa (0.1 s, 4 KB, bucle: no)",
    "- Fuente: tile 0 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_baldosa_2.ogg",
    "- Que es: Paso baldosa (0.1 s, 4 KB, bucle: no)",
    "- Fuente: tile 2 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_baldosa_3.ogg",
    "- Que es: Paso baldosa (0.1 s, 4 KB, bucle: no)",
    "- Fuente: tile 4 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_agua_1.ogg",
    "- Que es: Paso agua (0.2 s, 5 KB, bucle: no)",
    "- Fuente: water 0 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_agua_2.ogg",
    "- Que es: Paso agua (0.2 s, 6 KB, bucle: no)",
    "- Fuente: water 2 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_agua_3.ogg",
    "- Que es: Paso agua (0.2 s, 5 KB, bucle: no)",
    "- Fuente: water 4 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_rejilla_metal_1.ogg",
    "- Que es: Paso rejilla_metal (0.2 s, 5 KB, bucle: no)",
    "- Fuente: metal 0 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_rejilla_metal_2.ogg",
    "- Que es: Paso rejilla_metal (0.3 s, 5 KB, bucle: no)",
    "- Fuente: metal 2 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_rejilla_metal_3.ogg",
    "- Que es: Paso rejilla_metal (0.1 s, 4 KB, bucle: no)",
    "- Fuente: metal 4 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_madera_1.ogg",
    "- Que es: Paso madera (0.3 s, 5 KB, bucle: no)",
    "- Fuente: wood 0 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_madera_2.ogg",
    "- Que es: Paso madera (0.3 s, 5 KB, bucle: no)",
    "- Fuente: wood 2 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_paso_madera_3.ogg",
    "- Que es: Paso madera (0.3 s, 5 KB, bucle: no)",
    "- Fuente: wood 4 (pack: Footsteps on different surfaces) - autor: congusbongus (masterizado; originales swuing, ceberation, Eelke, EminYILDIRIM via freesound, ver license.txt del pack) - https://opengameart.org/content/footsteps-on-different-surfaces - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_puerta_madera_abrir.ogg",
    "- Que es: Puerta madera abrir (0.9 s, 12 KB, bucle: no)",
    "- Fuente: DoorOpen03 (pack: Door Open, Door Close Set) - autor: qubodup - https://opengameart.org/content/door-open-door-close-set - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_puerta_madera_cerrar.ogg",
    "- Que es: Puerta madera cerrar (0.7 s, 10 KB, bucle: no)",
    "- Fuente: DoorClose05 (pack: Door Open, Door Close Set) - autor: qubodup - https://opengameart.org/content/door-open-door-close-set - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_puerta_metal_abrir.ogg",
    "- Que es: Puerta metal pesada abrir (0.4 s, 7 KB, bucle: no)",
    "- Fuente: metal_open_01 (pack: 100 CC0 metal and wood SFX) - autor: rubberduck - https://opengameart.org/content/100-cc0-metal-and-wood-sfx - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_puerta_metal_cerrar.ogg",
    "- Que es: Puerta metal pesada cerrar (0.3 s, 6 KB, bucle: no)",
    "- Fuente: metal_slam_01 (pack: 100 CC0 metal and wood SFX) - autor: rubberduck - https://opengameart.org/content/100-cc0-metal-and-wood-sfx - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_puerta_hierro.ogg",
    "- Que es: Puerta de hierro (0.8 s, 11 KB, bucle: no)",
    "- Fuente: iron_door (pack: Iron Door) - autor: themightyglider - https://opengameart.org/content/iron-door - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_puerta_crujido.ogg",
    "- Que es: Crujido de puerta (6.8 s, 62 KB, bucle: no)",
    "- Fuente: creakylightwoodendoor (pack: Creaky light wooden door) - autor: fractilegames - https://opengameart.org/content/creaky-light-wooden-door - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_puerta_manija_trabada.ogg",
    "- Que es: Manija de puerta trabada (0.6 s, 9 KB, bucle: no)",
    "- Fuente: LockedDoorHandleJiggle (pack: Door Lock Sounds) - autor: Cough-E - https://opengameart.org/content/door-lock-sounds - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_puerta_destrabar.ogg",
    "- Que es: Destrabar puerta (0.4 s, 7 KB, bucle: no)",
    "- Fuente: UnlockDoor (pack: Door Lock Sounds) - autor: Cough-E - https://opengameart.org/content/door-lock-sounds - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_cuchillada_1.ogg",
    "- Que es: Cuchilla / corte de carne (0.2 s, 6 KB, bucle: no)",
    "- Fuente: Stab_Knife_00.mp3 (pack: Horror Sound Effects Library) - autor: Little Robot Sound Factory - https://opengameart.org/content/horror-sound-effects-library - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_cuchillada_2.ogg",
    "- Que es: Cuchilla / corte de carne (0.3 s, 6 KB, bucle: no)",
    "- Fuente: Stab_Knife_02.mp3 (pack: Horror Sound Effects Library) - autor: Little Robot Sound Factory - https://opengameart.org/content/horror-sound-effects-library - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_corte_hueso.ogg",
    "- Que es: Hueso quebrado (0.6 s, 10 KB, bucle: no)",
    "- Fuente: Wet Break 3 (pack: Fleshy Bone Break/Snap SFX) - autor: Zane Little Music - https://opengameart.org/content/fleshy-bone-breaksnap-sfx - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_hueso_seco.ogg",
    "- Que es: Hueso crujiendo (0.3 s, 8 KB, bucle: no)",
    "- Fuente: Bonecrack_00.mp3 (pack: Horror Sound Effects Library) - autor: Little Robot Sound Factory - https://opengameart.org/content/horror-sound-effects-library - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_sierra_hueso.ogg",
    "- Que es: Sierra sobre hueso (sierra/ruido mecanico) (2.3 s, 31 KB, bucle: no)",
    "- Fuente: Sawing or winding something.ogg - autor: stephan - https://commons.wikimedia.org/wiki/File%3ASawing_or_winding_something.ogg - licencia: Public domain (dominio publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_chapoteo_1.ogg",
    "- Que es: Chapoteo / gore (0.2 s, 5 KB, bucle: no)",
    "- Fuente: squish_01 (pack: Squish Sounds Effects) - autor: EZduzziteh - https://opengameart.org/content/squish-sounds-effects - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_chapoteo_2.ogg",
    "- Que es: Chapoteo / gore (0.2 s, 5 KB, bucle: no)",
    "- Fuente: squish_03 (pack: Squish Sounds Effects) - autor: EZduzziteh - https://opengameart.org/content/squish-sounds-effects - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_desgarro_carne.ogg",
    "- Que es: Desgarro de carne (2.5 s, 26 KB, bucle: no)",
    "- Fuente: fresh_meat_004 (pack: Fresh Meat) - autor: Paul Wortmann - https://opengameart.org/content/fresh-meat - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_viscoso.ogg",
    "- Que es: Sonido viscoso (1.4 s, 9 KB, bucle: no)",
    "- Fuente: squelch noise (pack: Lo Fi Squelching noise) - autor: Some Weirdo - https://opengameart.org/content/lo-fi-squelching-noise - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_gancho_cadena.ogg",
    "- Que es: Cadena / gancho (0.9 s, 12 KB, bucle: no)",
    "- Fuente: winch Marker #2 (pack: Chain winch sounds) - autor: bart - https://opengameart.org/content/chain-winch-sounds - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_gancho_metal.ogg",
    "- Que es: Gancho metalico (0.2 s, 5 KB, bucle: no)",
    "- Fuente: metal_hit_02 (pack: 100 CC0 metal and wood SFX) - autor: rubberduck - https://opengameart.org/content/100-cc0-metal-and-wood-sfx - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_mugido_1.ogg",
    "- Que es: Mugido de vaca (0.8 s, 11 KB, bucle: no)",
    "- Fuente: Cow in Vezo.ogg - autor: Gasybeaugosse2020 - https://commons.wikimedia.org/wiki/File%3ACow_in_Vezo.ogg - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_mugido_2.ogg",
    "- Que es: Mugido de vaca (0.6 s, 8 KB, bucle: no)",
    "- Fuente: Cow in Antefasy.wav - autor: Gasybeaugosse2020 - https://commons.wikimedia.org/wiki/File%3ACow_in_Antefasy.wav - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_mugido_3.ogg",
    "- Que es: Mugido de vaca (2.0 s, 20 KB, bucle: no)",
    "- Fuente: Katalalan.ogg - autor: Sabak5388 - https://commons.wikimedia.org/wiki/File%3AKatalalan.ogg - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_mugido_angustia.ogg",
    "- Que es: Mugido angustiado (1.2 s, 15 KB, bucle: no)",
    "- Fuente: moo-death (pack: Sci-Fi Aliens and Cows Pack) - autor: qubodup - https://opengameart.org/content/sci-fi-aliens-and-cows-pack - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_mugido_grave.ogg",
    "- Que es: Mugido grave distorsionado (0.9 s, 9 KB, bucle: no)",
    "- Fuente: Cow in Antefasy.wav - autor: Gasybeaugosse2020 - https://commons.wikimedia.org/wiki/File%3ACow_in_Antefasy.wav - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; filtro/tono aplicado (asetrate=30000,aresample=44100,lowpass=f=3500)",
    "",
    "### se/se_llave_recoger.ogg",
    "- Que es: Llave: recoger (0.4 s, 6 KB, bucle: no)",
    "- Fuente: key_pickup (pack: Key pickup) - autor: Vinrax - https://opengameart.org/content/key-pickup - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_llaves_tintineo.ogg",
    "- Que es: Llaves tintineo (0.4 s, 7 KB, bucle: no)",
    "- Fuente: keys_03 (pack: 100 CC0 metal and wood SFX) - autor: rubberduck - https://opengameart.org/content/100-cc0-metal-and-wood-sfx - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_papel_nota_1.ogg",
    "- Que es: Papel / nota (0.5 s, 8 KB, bucle: no)",
    "- Fuente: Paper Sound - 1 (pack: Various Paper Sound Effects) - autor: Luckius - https://opengameart.org/content/various-paper-sound-effects - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_papel_nota_2.ogg",
    "- Que es: Papel / nota (2.6 s, 29 KB, bucle: no)",
    "- Fuente: Paper Sound - 4 (pack: Various Paper Sound Effects) - autor: Luckius - https://opengameart.org/content/various-paper-sound-effects - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_interruptor_luz.ogg",
    "- Que es: Interruptor de luz (0.1 s, 4 KB, bucle: no)",
    "- Fuente: light_switch_turn_on (pack: Light Switch Turn On And Off SFX) - autor: FunnyDude - https://opengameart.org/content/light-switch-turn-on-and-off-sfx-0 - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_linterna_clic.ogg",
    "- Que es: Linterna: clic (0.1 s, 4 KB, bucle: no)",
    "- Fuente: light_switch_turn_off (pack: Light Switch Turn On And Off SFX) - autor: FunnyDude - https://opengameart.org/content/light-switch-turn-on-and-off-sfx-0 - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; filtro/tono aplicado (highpass=f=400)",
    "",
    "### se/se_tv_encender.ogg",
    "- Que es: TV: encender (estatica con entrada) (1.1 s, 13 KB, bucle: no)",
    "- Fuente: ScatterNoise1 (pack: Static) - autor: xhunterko - https://opengameart.org/content/static - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; filtro/tono aplicado (highpass=f=1500,afade=t=in:d=0.15)",
    "",
    "### se/se_tv_apagar.ogg",
    "- Que es: TV: apagar (estatica con corte) (0.3 s, 6 KB, bucle: no)",
    "- Fuente: ScatterNoise1 (pack: Static) - autor: xhunterko - https://opengameart.org/content/static - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; filtro/tono aplicado (lowpass=f=3000,afade=t=out:d=0.4)",
    "",
    "### se/se_frasco_vidrio_1.ogg",
    "- Que es: Frasco de vidrio (0.2 s, 6 KB, bucle: no)",
    "- Fuente: glass_bottle_close (pack: glass bottle (open & close)) - autor: sinny - https://opengameart.org/content/glass-bottle-open-close - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_frasco_vidrio_2.ogg",
    "- Que es: Frasco de vidrio (0.2 s, 5 KB, bucle: no)",
    "- Fuente: glass_bottle_open (pack: glass bottle (open & close)) - autor: sinny - https://opengameart.org/content/glass-bottle-open-close - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_objeto_recoger.ogg",
    "- Que es: Recoger objeto (0.5 s, 8 KB, bucle: no)",
    "- Fuente: key-176034 (pack: Item Pickup / Key) - autor: Musheran - https://opengameart.org/content/item-pickup-key - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_golpe_carne.ogg",
    "- Que es: Combate: golpe a carne (0.2 s, 5 KB, bucle: no)",
    "- Fuente: squish_05 (pack: Squish Sounds Effects) - autor: EZduzziteh - https://opengameart.org/content/squish-sounds-effects - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_golpe_pesado.ogg",
    "- Que es: Combate: golpe pesado (0.5 s, 8 KB, bucle: no)",
    "- Fuente: Deep Break 2 (pack: Deep Bone Crack/Break SFX) - autor: Zane Little Music - https://opengameart.org/content/deep-bone-crackbreak-sfx - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_fallo_aire.ogg",
    "- Que es: Combate: fallo / silbido (0.1 s, 4 KB, bucle: no)",
    "- Fuente: swish-7 (pack: Swishes Sound Pack) - autor: artisticdude - https://opengameart.org/content/swishes-sound-pack - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_curar.ogg",
    "- Que es: Curar (1.0 s, 13 KB, bucle: no)",
    "- Fuente: 02_heal_02 (pack: 8 Heals and Buffs SFX) - autor: leohpaz - https://opengameart.org/content/8-heals-and-buffs-sfx - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_estado_veneno.ogg",
    "- Que es: Estado / veneno (1.3 s, 9 KB, bucle: no)",
    "- Fuente: 46_poison_01 (pack: 8 Magic Attacks) - autor: leohpaz - https://opengameart.org/content/8-magic-attacks - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_cordura_baja.ogg",
    "- Que es: Cordura baja (stinger) (2.0 s, 21 KB, bucle: no)",
    "- Fuente: Monster_03.mp3 (pack: Horror Sound Effects Library) - autor: Little Robot Sound Factory - https://opengameart.org/content/horror-sound-effects-library - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_enemigo_muere.ogg",
    "- Que es: Muerte de enemigo (1.3 s, 13 KB, bucle: no)",
    "- Fuente: moo-notification (pack: Sci-Fi Aliens and Cows Pack) - autor: qubodup - https://opengameart.org/content/sci-fi-aliens-and-cows-pack - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; filtro/tono aplicado (asetrate=26000,aresample=44100,lowpass=f=3000)",
    "",
    "### se/se_screamer_1.ogg",
    "- Que es: Screamer 1 (3.0 s, 28 KB, bucle: no)",
    "- Fuente: horrorghostscream (pack: Phantom Scream) - autor: VishwaJai - https://opengameart.org/content/phantom-scream - licencia: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_screamer_2.ogg",
    "- Que es: Screamer 2 (0.9 s, 11 KB, bucle: no)",
    "- Fuente: female_scream_1 (pack: Female Scream 1) - autor: Nocturnal_Vanguard - https://opengameart.org/content/female-scream-1 - licencia: CC0 (https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_screamer_3.ogg",
    "- Que es: Screamer 3 (2.9 s, 30 KB, bucle: no)",
    "- Fuente: monster_scream (pack: Monster Scream) - autor: SneidXK - https://opengameart.org/content/monster-scream - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "### se/se_nivel_victoria.ogg",
    "- Que es: Nivel / victoria (breve) (2.9 s, 23 KB, bucle: no)",
    "- Fuente: Jingle_Achievement_00.mp3 (pack: Horror Sound Effects Library) - autor: Little Robot Sound Factory - https://opengameart.org/content/horror-sound-effects-library - licencia: CC-BY 3.0 (https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG"
  ]
  def self.screamer; @screamer; end
  def self.screamer=(key); @screamer=key; end
end

# Creditos completos del pack, incluidos autores secundarios, obras y enlaces.
# Se pagina texto ya ajustado al ancho real de la fuente, incluidas URL largas.
class Scene_VacasCredits
  def main
    @background=Vacas_UI.background('titulo')
    @panel=Window_VacasPanel.new(24,24,Vacas_HD.w-48,Vacas_HD.h-96)
    @footer=Window_VacasPanel.new(24,Vacas_HD.bottom(64),Vacas_HD.w-48,64)
    @page=0; @lines=Vacas_Audio::CREDITS_LINES
    @per_page=[(@panel.height-32)/25,1].max
    @pages=[(@lines.size+@per_page-1)/@per_page,1].max
    draw
    Vacas_UI.loop_scene(self)
    @panel.dispose; @footer.dispose; @background.dispose
  end
  def draw
    @panel.contents.clear
    @per_page.times do |i|
      line=@lines[@page*@per_page+i]
      b=@panel.contents; b.font.name='Courier New'; b.font.size=16; b.font.color=Vacas_UI::INK
      b.draw_text(4,i*25,548,25,line) if line
    end
    @footer.contents.clear
    Vacas_UI.text(@footer.contents,0,0,552,
      'Creditos '+(@page+1).to_s+'/'+@pages.to_s+'  Flechas: pagina  Esc: titulo',16)
  end
  def update
    @background.update
    if Input.trigger?(Input::B)
      Vacas_Audio.play(:cancelar); $scene=Scene_Title.new; return
    end
    delta=0
    delta=1 if Input.repeat?(Input::RIGHT) || Input.repeat?(Input::DOWN) || Input.trigger?(Input::C)
    delta=-1 if Input.repeat?(Input::LEFT) || Input.repeat?(Input::UP)
    next_page=[[@page+delta,0].max,@pages-1].min
    if next_page!=@page
      @page=next_page; Vacas_Audio.play(:cursor); draw
    end
  end
end

module Vacas_Audio
  def self.allow_pickup?
    now=Graphics.frame_count
    return false if @pickup_frame && now>=@pickup_frame && now-@pickup_frame<10
    @pickup_frame=now; true
  end
  def self.pickup(key)
    play(key) if allow_pickup?
  end
end
class Game_Party
  alias audio_gain_item gain_item
  def gain_item(id,n)
    before=item_number(id)
    audio_gain_item(id,n)
    if n>0 && item_number(id)>before && $scene.is_a?(Scene_Map)
      name=$data_items[id] ? $data_items[id].name.downcase : ''
      key=name.include?('llave') ? :llave_recoger : :recoger_objeto
      key=:papel_nota if [4,6,8,9,10,11,13,15,23,24,28,33,34].include?(id)
      key=:frasco_de_vidrio if name.include?('tarro') || name.include?('frasco')
      Vacas_Audio.pickup(key)
    end
  end
end
module Vacas
  class << self
    alias audio_actualizar_linterna actualizar_linterna
    def actualizar_linterna
      before=$game_switches[115]
      audio_actualizar_linterna
      if before!=$game_switches[115] && @audio_recharge_frame!=Graphics.frame_count
        Vacas_Audio.play(:linterna_clic)
      end
    end
    alias audio_recargar recargar
    def recargar
      result=audio_recargar
      if result
        @audio_recharge_frame=Graphics.frame_count
        Vacas_Audio.play(:linterna_clic)
      end
      result
    end
  end
end
# El acierto ya tiene un SE original por pieza: se sustituye sin duplicarlo.
class Vacas_Minijuego
  def se(nombre,vol=80,tono=100)
    if nombre=='093-Attack05'
      Vacas_Audio.play(is_a?(Vacas_Corte) ? :cuchilla_corte_de_carne : :gancho_metalico)
    else
      $game_system.se_play(RPG::AudioFile.new(nombre,vol,tono))
    end
  end
end

module Vacas_Audio
  CREDITS_LINES = [
    "FEKA STUDIOS - VACAS",
    "Carlos - dirección, arte, diseño",
    "Alexandre - historia",
    'Ithalo "Ander" - sonido',
    "",
    "Creditos de audio - Vacas",
    "",
    "Todos los archivos estan convertidos a OGG Vorbis (los",
    "10 SE requeridos tambien en WAV 16-bit mono con el",
    "mismo nombre). Solo licencias CC0 / dominio publico /",
    "CC-BY 3.0 o 4.0.",
    "Los archivos CC-BY exigen atribucion: incluir este",
    "listado (o equivalente) en los creditos del juego.",
    "",
    "Atribucion de musica (Kevin MacLeod): \"Titulo\" Kevin",
    "MacLeod (incompetech.com), licenciada bajo Creative",
    "Commons: By Attribution 4.0",
    "https://creativecommons.org/licenses/by/4.0/",
    "",
    "Modificaciones comunes: conversion a OGG, recorte,",
    "normalizacion (BGM/BGS/ME a -16 LUFS aprox., SE a pico",
    "-1 dB), recorte de silencios en SE, fundido corto y",
    "crossfade de bucle en BGM/BGS. Las mezclas (BGS",
    "compuestos) combinan varias grabaciones.",
    "",
    "BGM",
    "",
    "bgm/vacas_titulo.ogg (destino:",
    "Audio/BGM/vacas_titulo.ogg)",
    "- Que es: Titulo (86.0 s, 1001 KB, bucle: si)",
    "- Fuente: Ghost Story - autor: Kevin MacLeod - https:/",
    "/incompetech.com/music/royalty-free/mp3-royaltyfree/Gh",
    "ost%20Story.mp3 - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "bgm/vacas_combate.ogg (destino:",
    "Audio/BGM/vacas_combate.ogg)",
    "- Que es: Combate normal (96.0 s, 1193 KB, bucle: si)",
    "- Fuente: Killing Time - autor: Kevin MacLeod - https:",
    "//incompetech.com/music/royalty-free/mp3-royaltyfree/K",
    "illing%20Time.mp3 - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "bgm/vacas_jefe.ogg (destino: Audio/BGM/vacas_jefe.ogg)",
    "- Que es: Jefe (Rey, Diagnostico, Pastor) (135.0 s,",
    "1597 KB, bucle: si)",
    "- Fuente: Giant Wyrm - autor: Kevin MacLeod - https://",
    "incompetech.com/music/royalty-free/mp3-royaltyfree/Gia",
    "nt%20Wyrm.mp3 - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 5s",
    "",
    "bgm/vacas_persecucion.ogg (destino:",
    "Audio/BGM/vacas_persecucion.ogg)",
    "- Que es: Persecucion (52.0 s, 701 KB, bucle: si)",
    "- Fuente: Chase - autor: Kevin MacLeod - https://incom",
    "petech.com/music/royalty-free/mp3-royaltyfree/Chase.mp",
    "3 - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 3s",
    "",
    "bgm/vacas_gameover.ogg (destino:",
    "Audio/BGM/vacas_gameover.ogg)",
    "- Que es: Game over (46.0 s, 594 KB, bucle: si)",
    "- Fuente: Cryptic Sorrow - autor: Kevin MacLeod - http",
    "s://incompetech.com/music/royalty-free/mp3-royaltyfree",
    "/Cryptic%20Sorrow.mp3 - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "bgm/bgm_piso_exploracion.ogg",
    "- Que es: Exploracion del piso (116.0 s, 1476 KB,",
    "bucle: si)",
    "- Fuente: Ossuary 5 - Rest - autor: Kevin MacLeod - ht",
    "tps://incompetech.com/music/royalty-free/mp3-royaltyfr",
    "ee/Ossuary%205%20-%20Rest.mp3 - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "bgm/bgm_matadero_exploracion.ogg",
    "- Que es: Exploracion matadero (116.0 s, 1412 KB,",
    "bucle: si)",
    "- Fuente: Crypto - autor: Kevin MacLeod - https://inco",
    "mpetech.com/music/royalty-free/mp3-royaltyfree/Crypto.",
    "mp3 - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "bgm/bgm_camaras_frias.ogg",
    "- Que es: Camaras frias (116.0 s, 1503 KB, bucle: si)",
    "- Fuente: Deep Haze - autor: Kevin MacLeod - https://i",
    "ncompetech.com/music/royalty-free/mp3-royaltyfree/Deep",
    "%20Haze.mp3 - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "bgm/bgm_lucy_laboratorio.ogg",
    "- Que es: Lucy / laboratorio (116.0 s, 1688 KB, bucle:",
    "si)",
    "- Fuente: Darkling - autor: Kevin MacLeod - https://in",
    "competech.com/music/royalty-free/mp3-royaltyfree/Darkl",
    "ing.mp3 - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "bgm/bgm_alcantarillas.ogg",
    "- Que es: Alcantarillas (116.0 s, 1358 KB, bucle: si)",
    "- Fuente: Gathering Darkness - autor: Kevin MacLeod -",
    "https://incompetech.com/music/royalty-free/mp3-royalty",
    "free/Gathering%20Darkness.mp3 - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "bgm/bgm_camara_manada.ogg",
    "- Que es: Camara de la manada (115.0 s, 1253 KB,",
    "bucle: si)",
    "- Fuente: Heart of the Beast - autor: Kevin MacLeod -",
    "https://incompetech.com/music/royalty-free/mp3-royalty",
    "free/Heart%20of%20the%20Beast.mp3 - licencia: CC-BY",
    "4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 5s",
    "",
    "bgm/bgm_tv_segura.ogg",
    "- Que es: Tema tranquilo \"seguro\" (TV) (116.0 s, 1601",
    "KB, bucle: si)",
    "- Fuente: Lullaby (pack: Lullaby) - autor: Pro Sensory",
    "- https://opengameart.org/content/lullaby-0 -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "bgm/bgm_extra_calle_noche.ogg",
    "- Que es: Alterna: calle de noche / suspense (116.0 s,",
    "1471 KB, bucle: si)",
    "- Fuente: (Night of the Streets [Horror/Suspense]) -",
    "autor: nene - https://opengameart.org/content/night-of",
    "-the-streets-horrorsuspense - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "bgm/bgm_extra_estacion_drone.ogg",
    "- Que es: Alterna: camaras / drone (115.0 s, 1129 KB,",
    "bucle: si)",
    "- Fuente: (Station Drone 2) - autor: Tozan -",
    "https://opengameart.org/content/station-drone-2 -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 5s",
    "",
    "bgm/bgm_extra_sotano.ogg",
    "- Que es: Alterna: sotano / lab (115.0 s, 1036 KB,",
    "bucle: si)",
    "- Fuente: (Telos Creepy Cage Street) - autor: Tozan -",
    "https://opengameart.org/content/telos-creepy-cage-stre",
    "et - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 5s",
    "",
    "bgm/bgm_extra_tension_lab.ogg",
    "- Que es: Alterna: laboratorio tenso (116.0 s, 1097",
    "KB, bucle: si)",
    "- Fuente: (tension and distress) - autor: allen",
    "yatsura -",
    "https://opengameart.org/content/tension-and-distress -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "bgm/bgm_extra_dark_drone.ogg",
    "- Que es: Alterna: alcantarillas drone (115.0 s, 1119",
    "KB, bucle: si)",
    "- Fuente: (Dark Ambient Drone) - autor: Tsorthan Grove",
    "- https://opengameart.org/content/dark-ambient-drone -",
    "licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 5s",
    "",
    "bgm/bgm_extra_batalla_rpg.ogg",
    "- Que es: Alterna: batalla (96.0 s, 1322 KB, bucle:",
    "si)",
    "- Fuente: Battle RPG Theme Var (pack: Boss Battle",
    "Theme) - autor: CleytonKauffman -",
    "https://opengameart.org/content/boss-battle-theme -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 4s",
    "",
    "BGS",
    "",
    "bgs/vacas_menu.ogg (destino: Audio/BGS/vacas_menu.ogg)",
    "- Que es: Pausa / menu (tenue) (28.0 s, 241 KB, bucle:",
    "si)",
    "- Fuente: Inside of refrigerator.ogg - autor: stephan",
    "- https://commons.wikimedia.org/wiki/File%3AInside_of_",
    "refrigerator.ogg - licencia: Public domain (dominio",
    "publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG;",
    "filtro/tono aplicado (lowpass=f=900); crossfade de",
    "bucle 2s",
    "",
    "bgs/vacas_piso.ogg (destino: Audio/BGS/vacas_piso.ogg)",
    "- Que es: Piso y calle: lluvia en ventana + reloj",
    "(72.0 s, 643 KB, bucle: si)",
    "- Fuente: Rain against the window.ogg - autor: cori -",
    "https://commons.wikimedia.org/wiki/File%3ARain_against",
    "_the_window.ogg - licencia: Public domain (dominio",
    "publico (ver pagina del archivo en Wikimedia Commons))",
    "- Fuente: Clock ticking.ogg - autor: natalie - https:/",
    "/commons.wikimedia.org/wiki/File%3AClock_ticking.ogg -",
    "licencia: Public domain (dominio publico (ver pagina",
    "del archivo en Wikimedia Commons))",
    "- Fuente: Inside of refrigerator.ogg - autor: stephan",
    "- https://commons.wikimedia.org/wiki/File%3AInside_of_",
    "refrigerator.ogg - licencia: Public domain (dominio",
    "publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: mezcla de 3 fuentes;",
    "recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "bgs/vacas_matadero.ogg (destino:",
    "Audio/BGS/vacas_matadero.ogg)",
    "- Que es: Matadero: cintas, cadenas, prensa (87.0 s,",
    "849 KB, bucle: si)",
    "- Fuente: WWS Conveyorbelt.ogg - autor: Work With",
    "Sounds / Konrad Gutkowski - https://commons.wikimedia.",
    "org/wiki/File%3AWWS_Conveyorbelt.ogg - licencia: CC-BY",
    "4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Fuente: WWS Bucketchain.ogg - autor: Work With",
    "Sounds / Konrad Gutkowski - https://commons.wikimedia.",
    "org/wiki/File%3AWWS_Bucketchain.ogg - licencia: CC-BY",
    "4.0 (https://creativecommons.org/licenses/by/4.0/)",
    "- Fuente: WWS Punchingpress.ogg - autor: Work With",
    "Sounds / Konrad Gutkowski - https://commons.wikimedia.",
    "org/wiki/File%3AWWS_Punchingpress.ogg - licencia:",
    "CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: mezcla de 3 fuentes;",
    "recorte/normalizacion/OGG; crossfade de bucle 3s",
    "",
    "bgs/vacas_camaras.ogg (destino:",
    "Audio/BGS/vacas_camaras.ogg)",
    "- Que es: Camaras frias: compresor (87.0 s, 870 KB,",
    "bucle: si)",
    "- Fuente: WWS Compressor.ogg - autor: Work With Sounds",
    "/ Torsten Nilsson - https://commons.wikimedia.org/wiki",
    "/File%3AWWS_Compressor.ogg - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Fuente: Inside of refrigerator.ogg - autor: stephan",
    "- https://commons.wikimedia.org/wiki/File%3AInside_of_",
    "refrigerator.ogg - licencia: Public domain (dominio",
    "publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: mezcla de 2 fuentes;",
    "recorte/normalizacion/OGG; filtro/tono aplicado",
    "(lowpass=f=500); crossfade de bucle 3s",
    "",
    "bgs/vacas_laboratorio.ogg (destino:",
    "Audio/BGS/vacas_laboratorio.ogg)",
    "- Que es: Laboratorio: zumbido electrico + latido +",
    "reloj (58.0 s, 517 KB, bucle: si)",
    "- Fuente: Electric noise (pack: 12 Ambient Machine",
    "Sounds) - autor: bart - https://opengameart.org/conten",
    "t/12-ambient-machine-sounds - licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Fuente: heartbeat slow (pack: Heartbeat sounds) -",
    "autor: bart -",
    "https://opengameart.org/content/heartbeat-sounds -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Clock ticking.ogg - autor: natalie - https:/",
    "/commons.wikimedia.org/wiki/File%3AClock_ticking.ogg -",
    "licencia: Public domain (dominio publico (ver pagina",
    "del archivo en Wikimedia Commons))",
    "- Modificaciones: mezcla de 3 fuentes;",
    "recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "bgs/vacas_alcantarillas.ogg (destino:",
    "Audio/BGS/vacas_alcantarillas.ogg)",
    "- Que es: Alcantarillas: goteo con eco + agua",
    "corriendo (58.0 s, 591 KB, bucle: si)",
    "- Fuente: atmosbasement (pack: Dripping water loop) -",
    "autor: qubodup -",
    "https://opengameart.org/content/dripping-water-loop -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: bg_water_running (pack: Running Water -",
    "background noise) - autor: HippoDevelopment - https://",
    "opengameart.org/content/running-water-background-noise",
    "- licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: mezcla de 2 fuentes;",
    "recorte/normalizacion/OGG; crossfade de bucle 2s",
    "",
    "bgs/vacas_manada.ogg (destino:",
    "Audio/BGS/vacas_manada.ogg)",
    "- Que es: Manada: respiracion, mugidos lejanos, corral",
    "(57.0 s, 366 KB, bucle: si)",
    "- Fuente: Ambience_MonstersBelly_00.mp3 (pack: Horror",
    "Sound Effects Library) - autor: Little Robot Sound",
    "Factory - https://opengameart.org/content/horror-sound",
    "-effects-library - licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Fuente: Cow in Vezo.ogg - autor: Gasybeaugosse2020 -",
    "https://commons.wikimedia.org/wiki/File%3ACow_in_Vezo.",
    "ogg - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Cow in Antefasy.wav - autor:",
    "Gasybeaugosse2020 - https://commons.wikimedia.org/wiki",
    "/File%3ACow_in_Antefasy.wav - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Katalalan.ogg - autor: Sabak5388 - https://c",
    "ommons.wikimedia.org/wiki/File%3AKatalalan.ogg -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Heavy breathing 3.ogg - autor: ezwa - https:",
    "//commons.wikimedia.org/wiki/File%3AHeavy_breathing_3.",
    "ogg - licencia: Public domain (dominio publico (ver",
    "pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: mezcla de 5 fuentes;",
    "recorte/normalizacion/OGG; filtro/tono aplicado",
    "(lowpass=f=1800,",
    "lowpass=f=2500,asetrate=33000,aresample=44100,",
    "asetrate=36000,aresample=44100,",
    "asetrate=34000,aresample=44100, lowpass=f=1200);",
    "crossfade de bucle 3s",
    "",
    "bgs/bgs_tv_estatica.ogg",
    "- Que es: Estatica de TV vieja (28.0 s, 225 KB, bucle:",
    "si)",
    "- Fuente: ScatterNoise1 (pack: Static) - autor:",
    "xhunterko - https://opengameart.org/content/static -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 2s",
    "",
    "bgs/bgs_tv_estatica_amortiguada.ogg",
    "- Que es: TV amortiguada (estatica filtrada) (28.0 s,",
    "165 KB, bucle: si)",
    "- Fuente: ScatterNoise1 (pack: Static) - autor:",
    "xhunterko - https://opengameart.org/content/static -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG;",
    "filtro/tono aplicado (lowpass=f=700); crossfade de",
    "bucle 2s",
    "",
    "bgs/bgs_nevera_zumbido.ogg",
    "- Que es: Zumbido de nevera (28.0 s, 260 KB, bucle:",
    "si)",
    "- Fuente: Inside of refrigerator.ogg - autor: stephan",
    "- https://commons.wikimedia.org/wiki/File%3AInside_of_",
    "refrigerator.ogg - licencia: Public domain (dominio",
    "publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 2s",
    "",
    "bgs/bgs_reloj_tictac.ogg",
    "- Que es: Reloj tictac (piso) (28.0 s, 267 KB, bucle:",
    "si)",
    "- Fuente: Clock ticking.ogg - autor: natalie - https:/",
    "/commons.wikimedia.org/wiki/File%3AClock_ticking.ogg -",
    "licencia: Public domain (dominio publico (ver pagina",
    "del archivo en Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 2s",
    "",
    "bgs/bgs_lluvia_ventana.ogg",
    "- Que es: Lluvia en ventana / calle noche (77.0 s, 643",
    "KB, bucle: si)",
    "- Fuente: Rain against the window.ogg - autor: cori -",
    "https://commons.wikimedia.org/wiki/File%3ARain_against",
    "_the_window.ogg - licencia: Public domain (dominio",
    "publico (ver pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 3s",
    "",
    "bgs/bgs_lluvia_calle.ogg",
    "- Que es: Lluvia exterior (57.0 s, 538 KB, bucle: si)",
    "- Fuente: amb_rain_loop_1 (pack: AMB Rain Loop 1) -",
    "autor: Kresiek The Furry -",
    "https://opengameart.org/content/amb-rain-loop-1 -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 3s",
    "",
    "bgs/bgs_matadero_cadenas.ogg",
    "- Que es: Cadenas y transportador (72.0 s, 648 KB,",
    "bucle: si)",
    "- Fuente: WWS Two-chainconveyorinoperation.ogg -",
    "autor: Work With Sounds / Technical Museum of Slovenia",
    "- https://commons.wikimedia.org/wiki/File%3AWWS_Two-ch",
    "ainconveyorinoperation.ogg - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 3s",
    "",
    "bgs/bgs_matadero_fabrica_oscura.ogg",
    "- Que es: Fabrica oscura (97.0 s, 815 KB, bucle: si)",
    "- Fuente: dark factory (pack: Dark Factory) - autor:",
    "bart - https://opengameart.org/content/dark-factory -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 3s",
    "",
    "bgs/bgs_camara_compresor.ogg",
    "- Que es: Compresor de camara fria (87.0 s, 869 KB,",
    "bucle: si)",
    "- Fuente: WWS Compressor.ogg - autor: Work With Sounds",
    "/ Torsten Nilsson - https://commons.wikimedia.org/wiki",
    "/File%3AWWS_Compressor.ogg - licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 3s",
    "",
    "bgs/bgs_alcantarilla_goteo.ogg",
    "- Que es: Goteo y eco (18.1 s, 192 KB, bucle: si)",
    "- Fuente: atmosbasement (pack: Dripping water loop) -",
    "autor: qubodup -",
    "https://opengameart.org/content/dripping-water-loop -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 2s",
    "",
    "bgs/bgs_agua_corriente.ogg",
    "- Que es: Agua corriendo (38.0 s, 353 KB, bucle: si)",
    "- Fuente: bg_water_running (pack: Running Water -",
    "background noise) - autor: HippoDevelopment - https://",
    "opengameart.org/content/running-water-background-noise",
    "- licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 2s",
    "",
    "bgs/bgs_edificio_abandonado.ogg",
    "- Que es: Edificio abandonado (ambiente) (65.0 s, 619",
    "KB, bucle: si)",
    "- Fuente: abandonedbuildingambience (pack: Abandoned",
    "Building Ambience) - autor: tcarisland - https://openg",
    "ameart.org/content/abandoned-building-ambience -",
    "licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 3s",
    "",
    "bgs/bgs_mazmorra_eco.ogg",
    "- Que es: Ambiente hueco (alcantarilla/camara) (87.0",
    "s, 809 KB, bucle: si)",
    "- Fuente: dungeon_ambient_1 (pack: Loopable Dungeon",
    "Ambience) - autor: JaggedStone - https://opengameart.o",
    "rg/content/loopable-dungeon-ambience - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 3s",
    "",
    "bgs/bgs_fluorescente_zumbido.ogg",
    "- Que es: Fluorescente / zumbido electrico (28.0 s,",
    "251 KB, bucle: si)",
    "- Fuente: Electric noise (pack: 12 Ambient Machine",
    "Sounds) - autor: bart - https://opengameart.org/conten",
    "t/12-ambient-machine-sounds - licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 2s",
    "",
    "bgs/bgs_generador.ogg",
    "- Que es: Generador / maquina (27.9 s, 197 KB, bucle:",
    "si)",
    "- Fuente: loop_generator_1 (pack: Generator (loop)) -",
    "autor: YCbCr -",
    "https://opengameart.org/content/generator-loop -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 2s",
    "",
    "bgs/bgs_latido_lento.ogg",
    "- Que es: Latido lento (29.0 s, 103 KB, bucle: si)",
    "- Fuente: heartbeat_slow_0 (pack: Heartbeat sounds) -",
    "autor: bart -",
    "https://opengameart.org/content/heartbeat-sounds -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 1s",
    "",
    "bgs/bgs_latido_rapido.ogg",
    "- Que es: Latido rapido (29.0 s, 138 KB, bucle: si)",
    "- Fuente: heartbeat_fast_0 (pack: Heartbeat sounds) -",
    "autor: bart -",
    "https://opengameart.org/content/heartbeat-sounds -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 1s",
    "",
    "bgs/bgs_respiracion_pesada.ogg",
    "- Que es: Respiracion pesada (43.0 s, 350 KB, bucle:",
    "si)",
    "- Fuente: Heavy breathing 3.ogg - autor: ezwa - https:",
    "//commons.wikimedia.org/wiki/File%3AHeavy_breathing_3.",
    "ogg - licencia: Public domain (dominio publico (ver",
    "pagina del archivo en Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 2s",
    "",
    "bgs/bgs_respiracion_horror.ogg",
    "- Que es: Respiracion de horror (29.0 s, 174 KB,",
    "bucle: si)",
    "- Fuente: horrorbreathing (pack: horror breathing) -",
    "autor: primbal -",
    "https://opengameart.org/content/horror-breathing -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG; crossfade",
    "de bucle 1s",
    "",
    "bgs/bgs_corral_ganado.ogg",
    "- Que es: Corral de ganado (mugidos y arrastre) (38.0",
    "s, 244 KB, bucle: si)",
    "- Fuente: Ambience_MonstersBelly_00.mp3 (pack: Horror",
    "Sound Effects Library) - autor: Little Robot Sound",
    "Factory - https://opengameart.org/content/horror-sound",
    "-effects-library - licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Fuente: Cow in Vezo.ogg - autor: Gasybeaugosse2020 -",
    "https://commons.wikimedia.org/wiki/File%3ACow_in_Vezo.",
    "ogg - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Katalalan.ogg - autor: Sabak5388 - https://c",
    "ommons.wikimedia.org/wiki/File%3AKatalalan.ogg -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Fuente: Cow in Antefasy.wav - autor:",
    "Gasybeaugosse2020 - https://commons.wikimedia.org/wiki",
    "/File%3ACow_in_Antefasy.wav - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: mezcla de 4 fuentes;",
    "recorte/normalizacion/OGG; filtro/tono aplicado",
    "(lowpass=f=1500); crossfade de bucle 2s",
    "",
    "ME",
    "",
    "me/vacas_victoria.ogg (destino:",
    "Audio/ME/vacas_victoria.ogg)",
    "- Que es: Victoria (6.0 s, 72 KB, bucle: no)",
    "- Fuente: Jingle_Win_00.mp3 (pack: Horror Sound",
    "Effects Library) - autor: Little Robot Sound Factory -",
    "https://opengameart.org/content/horror-sound-effects-l",
    "ibrary - licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "me/vacas_derrota.ogg (destino:",
    "Audio/ME/vacas_derrota.ogg)",
    "- Que es: Derrota / retirada mental (4.9 s, 56 KB,",
    "bucle: no)",
    "- Fuente: Jingle_Lose_00.mp3 (pack: Horror Sound",
    "Effects Library) - autor: Little Robot Sound Factory -",
    "https://opengameart.org/content/horror-sound-effects-l",
    "ibrary - licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "me/me_logro.ogg",
    "- Que es: Nivel / logro (3.1 s, 38 KB, bucle: no)",
    "- Fuente: Jingle_Achievement_00.mp3 (pack: Horror",
    "Sound Effects Library) - autor: Little Robot Sound",
    "Factory - https://opengameart.org/content/horror-sound",
    "-effects-library - licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "me/me_game_over_triste.ogg",
    "- Que es: Game over alterno (6.0 s, 74 KB, bucle: no)",
    "- Fuente: (Sad game over) - autor: Emma_MA -",
    "https://opengameart.org/content/sad-game-over -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "SE",
    "",
    "se/ui_cursor.ogg (destino: Audio/SE/ui_cursor.wav)",
    "- Que es: Cursor (0.1 s, 5 KB, bucle: no)",
    "- Fuente: menu tick (pack: Menu select tick) - autor:",
    "mikeask -",
    "https://opengameart.org/content/menu-select-tick -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/ui_confirmar.ogg (destino:",
    "Audio/SE/ui_confirmar.wav)",
    "- Que es: Confirmar (0.2 s, 5 KB, bucle: no)",
    "- Fuente: Menu Choice (pack: Menu Choice) - autor:",
    "Sudocolon -",
    "https://opengameart.org/content/menu-choice -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/ui_cancelar.ogg (destino: Audio/SE/ui_cancelar.wav)",
    "- Que es: Cancelar (clic analogico) (0.2 s, 5 KB,",
    "bucle: no)",
    "- Fuente: light_switch_turn_off (pack: Light Switch",
    "Turn On And Off SFX) - autor: FunnyDude - https://open",
    "gameart.org/content/light-switch-turn-on-and-off-sfx-0",
    "- licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/ui_error.ogg (destino: Audio/SE/ui_error.wav)",
    "- Que es: Error (golpe de madera apagado) (0.2 s, 4",
    "KB, bucle: no)",
    "- Fuente: wood_hit_03 (pack: 100 CC0 metal and wood",
    "SFX) - autor: rubberduck - https://opengameart.org/con",
    "tent/100-cc0-metal-and-wood-sfx - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG;",
    "filtro/tono aplicado (lowpass=f=900)",
    "",
    "se/mente_golpe.ogg (destino: Audio/SE/mente_golpe.wav)",
    "- Que es: Golpe mental / impacto (0.1 s, 4 KB, bucle:",
    "no)",
    "- Fuente: squishsplat_impact (pack: Squish Sounds",
    "Effects) - autor: EZduzziteh -",
    "https://opengameart.org/content/squish-sounds-effects",
    "- licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG;",
    "filtro/tono aplicado (lowpass=f=3000)",
    "",
    "se/mente_susto.ogg (destino: Audio/SE/mente_susto.wav)",
    "- Que es: Susto (1.1 s, 13 KB, bucle: no)",
    "- Fuente: horrorghostscream (pack: Phantom Scream) -",
    "autor: VishwaJai -",
    "https://opengameart.org/content/phantom-scream -",
    "licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/paso_baldosa.ogg (destino:",
    "Audio/SE/paso_baldosa.wav)",
    "- Que es: Paso baldosa (0.1 s, 4 KB, bucle: no)",
    "- Fuente: tile 1 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/paso_metal.ogg (destino: Audio/SE/paso_metal.wav)",
    "- Que es: Paso metal (0.3 s, 6 KB, bucle: no)",
    "- Fuente: metal 1 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/paso_agua.ogg (destino: Audio/SE/paso_agua.wav)",
    "- Que es: Paso agua (0.2 s, 6 KB, bucle: no)",
    "- Fuente: water 1 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/puerta_oxido.ogg (destino:",
    "Audio/SE/puerta_oxido.wav)",
    "- Que es: Puerta oxidada (1.4 s, 16 KB, bucle: no)",
    "- Fuente: creaky-door-hinge (pack: Creaky Door Hinge",
    "Spooky) - autor: w.forster.1@gmail.com - https://openg",
    "ameart.org/content/creaky-door-hinge-spooky -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_concreto_1.ogg",
    "- Que es: Paso concreto (0.1 s, 4 KB, bucle: no)",
    "- Fuente: boots 0 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_concreto_2.ogg",
    "- Que es: Paso concreto (0.1 s, 4 KB, bucle: no)",
    "- Fuente: boots 2 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_concreto_3.ogg",
    "- Que es: Paso concreto (0.1 s, 4 KB, bucle: no)",
    "- Fuente: boots 4 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_baldosa_1.ogg",
    "- Que es: Paso baldosa (0.1 s, 4 KB, bucle: no)",
    "- Fuente: tile 0 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_baldosa_2.ogg",
    "- Que es: Paso baldosa (0.1 s, 4 KB, bucle: no)",
    "- Fuente: tile 2 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_baldosa_3.ogg",
    "- Que es: Paso baldosa (0.1 s, 4 KB, bucle: no)",
    "- Fuente: tile 4 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_agua_1.ogg",
    "- Que es: Paso agua (0.2 s, 5 KB, bucle: no)",
    "- Fuente: water 0 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_agua_2.ogg",
    "- Que es: Paso agua (0.2 s, 6 KB, bucle: no)",
    "- Fuente: water 2 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_agua_3.ogg",
    "- Que es: Paso agua (0.2 s, 5 KB, bucle: no)",
    "- Fuente: water 4 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_rejilla_metal_1.ogg",
    "- Que es: Paso rejilla_metal (0.2 s, 5 KB, bucle: no)",
    "- Fuente: metal 0 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_rejilla_metal_2.ogg",
    "- Que es: Paso rejilla_metal (0.3 s, 5 KB, bucle: no)",
    "- Fuente: metal 2 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_rejilla_metal_3.ogg",
    "- Que es: Paso rejilla_metal (0.1 s, 4 KB, bucle: no)",
    "- Fuente: metal 4 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_madera_1.ogg",
    "- Que es: Paso madera (0.3 s, 5 KB, bucle: no)",
    "- Fuente: wood 0 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_madera_2.ogg",
    "- Que es: Paso madera (0.3 s, 5 KB, bucle: no)",
    "- Fuente: wood 2 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_paso_madera_3.ogg",
    "- Que es: Paso madera (0.3 s, 5 KB, bucle: no)",
    "- Fuente: wood 4 (pack: Footsteps on different",
    "surfaces) - autor: congusbongus (masterizado;",
    "originales swuing, ceberation, Eelke, EminYILDIRIM via",
    "freesound, ver license.txt del pack) - https://opengam",
    "eart.org/content/footsteps-on-different-surfaces -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_puerta_madera_abrir.ogg",
    "- Que es: Puerta madera abrir (0.9 s, 12 KB, bucle:",
    "no)",
    "- Fuente: DoorOpen03 (pack: Door Open, Door Close Set)",
    "- autor: qubodup - https://opengameart.org/content/doo",
    "r-open-door-close-set - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_puerta_madera_cerrar.ogg",
    "- Que es: Puerta madera cerrar (0.7 s, 10 KB, bucle:",
    "no)",
    "- Fuente: DoorClose05 (pack: Door Open, Door Close",
    "Set) - autor: qubodup - https://opengameart.org/conten",
    "t/door-open-door-close-set - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_puerta_metal_abrir.ogg",
    "- Que es: Puerta metal pesada abrir (0.4 s, 7 KB,",
    "bucle: no)",
    "- Fuente: metal_open_01 (pack: 100 CC0 metal and wood",
    "SFX) - autor: rubberduck - https://opengameart.org/con",
    "tent/100-cc0-metal-and-wood-sfx - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_puerta_metal_cerrar.ogg",
    "- Que es: Puerta metal pesada cerrar (0.3 s, 6 KB,",
    "bucle: no)",
    "- Fuente: metal_slam_01 (pack: 100 CC0 metal and wood",
    "SFX) - autor: rubberduck - https://opengameart.org/con",
    "tent/100-cc0-metal-and-wood-sfx - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_puerta_hierro.ogg",
    "- Que es: Puerta de hierro (0.8 s, 11 KB, bucle: no)",
    "- Fuente: iron_door (pack: Iron Door) - autor:",
    "themightyglider -",
    "https://opengameart.org/content/iron-door - licencia:",
    "CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_puerta_crujido.ogg",
    "- Que es: Crujido de puerta (6.8 s, 62 KB, bucle: no)",
    "- Fuente: creakylightwoodendoor (pack: Creaky light",
    "wooden door) - autor: fractilegames - https://opengame",
    "art.org/content/creaky-light-wooden-door - licencia:",
    "CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_puerta_manija_trabada.ogg",
    "- Que es: Manija de puerta trabada (0.6 s, 9 KB,",
    "bucle: no)",
    "- Fuente: LockedDoorHandleJiggle (pack: Door Lock",
    "Sounds) - autor: Cough-E -",
    "https://opengameart.org/content/door-lock-sounds -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_puerta_destrabar.ogg",
    "- Que es: Destrabar puerta (0.4 s, 7 KB, bucle: no)",
    "- Fuente: UnlockDoor (pack: Door Lock Sounds) - autor:",
    "Cough-E -",
    "https://opengameart.org/content/door-lock-sounds -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_cuchillada_1.ogg",
    "- Que es: Cuchilla / corte de carne (0.2 s, 6 KB,",
    "bucle: no)",
    "- Fuente: Stab_Knife_00.mp3 (pack: Horror Sound",
    "Effects Library) - autor: Little Robot Sound Factory -",
    "https://opengameart.org/content/horror-sound-effects-l",
    "ibrary - licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_cuchillada_2.ogg",
    "- Que es: Cuchilla / corte de carne (0.3 s, 6 KB,",
    "bucle: no)",
    "- Fuente: Stab_Knife_02.mp3 (pack: Horror Sound",
    "Effects Library) - autor: Little Robot Sound Factory -",
    "https://opengameart.org/content/horror-sound-effects-l",
    "ibrary - licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_corte_hueso.ogg",
    "- Que es: Hueso quebrado (0.6 s, 10 KB, bucle: no)",
    "- Fuente: Wet Break 3 (pack: Fleshy Bone Break/Snap",
    "SFX) - autor: Zane Little Music - https://opengameart.",
    "org/content/fleshy-bone-breaksnap-sfx - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_hueso_seco.ogg",
    "- Que es: Hueso crujiendo (0.3 s, 8 KB, bucle: no)",
    "- Fuente: Bonecrack_00.mp3 (pack: Horror Sound Effects",
    "Library) - autor: Little Robot Sound Factory - https:/",
    "/opengameart.org/content/horror-sound-effects-library",
    "- licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_sierra_hueso.ogg",
    "- Que es: Sierra sobre hueso (sierra/ruido mecanico)",
    "(2.3 s, 31 KB, bucle: no)",
    "- Fuente: Sawing or winding something.ogg - autor:",
    "stephan - https://commons.wikimedia.org/wiki/File%3ASa",
    "wing_or_winding_something.ogg - licencia: Public",
    "domain (dominio publico (ver pagina del archivo en",
    "Wikimedia Commons))",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_chapoteo_1.ogg",
    "- Que es: Chapoteo / gore (0.2 s, 5 KB, bucle: no)",
    "- Fuente: squish_01 (pack: Squish Sounds Effects) -",
    "autor: EZduzziteh -",
    "https://opengameart.org/content/squish-sounds-effects",
    "- licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_chapoteo_2.ogg",
    "- Que es: Chapoteo / gore (0.2 s, 5 KB, bucle: no)",
    "- Fuente: squish_03 (pack: Squish Sounds Effects) -",
    "autor: EZduzziteh -",
    "https://opengameart.org/content/squish-sounds-effects",
    "- licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_desgarro_carne.ogg",
    "- Que es: Desgarro de carne (2.5 s, 26 KB, bucle: no)",
    "- Fuente: fresh_meat_004 (pack: Fresh Meat) - autor:",
    "Paul Wortmann -",
    "https://opengameart.org/content/fresh-meat - licencia:",
    "CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_viscoso.ogg",
    "- Que es: Sonido viscoso (1.4 s, 9 KB, bucle: no)",
    "- Fuente: squelch noise (pack: Lo Fi Squelching noise)",
    "- autor: Some Weirdo -",
    "https://opengameart.org/content/lo-fi-squelching-noise",
    "- licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_gancho_cadena.ogg",
    "- Que es: Cadena / gancho (0.9 s, 12 KB, bucle: no)",
    "- Fuente: winch Marker #2 (pack: Chain winch sounds) -",
    "autor: bart -",
    "https://opengameart.org/content/chain-winch-sounds -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_gancho_metal.ogg",
    "- Que es: Gancho metalico (0.2 s, 5 KB, bucle: no)",
    "- Fuente: metal_hit_02 (pack: 100 CC0 metal and wood",
    "SFX) - autor: rubberduck - https://opengameart.org/con",
    "tent/100-cc0-metal-and-wood-sfx - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_mugido_1.ogg",
    "- Que es: Mugido de vaca (0.8 s, 11 KB, bucle: no)",
    "- Fuente: Cow in Vezo.ogg - autor: Gasybeaugosse2020 -",
    "https://commons.wikimedia.org/wiki/File%3ACow_in_Vezo.",
    "ogg - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_mugido_2.ogg",
    "- Que es: Mugido de vaca (0.6 s, 8 KB, bucle: no)",
    "- Fuente: Cow in Antefasy.wav - autor:",
    "Gasybeaugosse2020 - https://commons.wikimedia.org/wiki",
    "/File%3ACow_in_Antefasy.wav - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_mugido_3.ogg",
    "- Que es: Mugido de vaca (2.0 s, 20 KB, bucle: no)",
    "- Fuente: Katalalan.ogg - autor: Sabak5388 - https://c",
    "ommons.wikimedia.org/wiki/File%3AKatalalan.ogg -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_mugido_angustia.ogg",
    "- Que es: Mugido angustiado (1.2 s, 15 KB, bucle: no)",
    "- Fuente: moo-death (pack: Sci-Fi Aliens and Cows",
    "Pack) - autor: qubodup - https://opengameart.org/conte",
    "nt/sci-fi-aliens-and-cows-pack - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_mugido_grave.ogg",
    "- Que es: Mugido grave distorsionado (0.9 s, 9 KB,",
    "bucle: no)",
    "- Fuente: Cow in Antefasy.wav - autor:",
    "Gasybeaugosse2020 - https://commons.wikimedia.org/wiki",
    "/File%3ACow_in_Antefasy.wav - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG;",
    "filtro/tono aplicado",
    "(asetrate=30000,aresample=44100,lowpass=f=3500)",
    "",
    "se/se_llave_recoger.ogg",
    "- Que es: Llave: recoger (0.4 s, 6 KB, bucle: no)",
    "- Fuente: key_pickup (pack: Key pickup) - autor:",
    "Vinrax - https://opengameart.org/content/key-pickup -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_llaves_tintineo.ogg",
    "- Que es: Llaves tintineo (0.4 s, 7 KB, bucle: no)",
    "- Fuente: keys_03 (pack: 100 CC0 metal and wood SFX) -",
    "autor: rubberduck - https://opengameart.org/content/10",
    "0-cc0-metal-and-wood-sfx - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_papel_nota_1.ogg",
    "- Que es: Papel / nota (0.5 s, 8 KB, bucle: no)",
    "- Fuente: Paper Sound - 1 (pack: Various Paper Sound",
    "Effects) - autor: Luckius - https://opengameart.org/co",
    "ntent/various-paper-sound-effects - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_papel_nota_2.ogg",
    "- Que es: Papel / nota (2.6 s, 29 KB, bucle: no)",
    "- Fuente: Paper Sound - 4 (pack: Various Paper Sound",
    "Effects) - autor: Luckius - https://opengameart.org/co",
    "ntent/various-paper-sound-effects - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_interruptor_luz.ogg",
    "- Que es: Interruptor de luz (0.1 s, 4 KB, bucle: no)",
    "- Fuente: light_switch_turn_on (pack: Light Switch",
    "Turn On And Off SFX) - autor: FunnyDude - https://open",
    "gameart.org/content/light-switch-turn-on-and-off-sfx-0",
    "- licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_linterna_clic.ogg",
    "- Que es: Linterna: clic (0.1 s, 4 KB, bucle: no)",
    "- Fuente: light_switch_turn_off (pack: Light Switch",
    "Turn On And Off SFX) - autor: FunnyDude - https://open",
    "gameart.org/content/light-switch-turn-on-and-off-sfx-0",
    "- licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG;",
    "filtro/tono aplicado (highpass=f=400)",
    "",
    "se/se_tv_encender.ogg",
    "- Que es: TV: encender (estatica con entrada) (1.1 s,",
    "13 KB, bucle: no)",
    "- Fuente: ScatterNoise1 (pack: Static) - autor:",
    "xhunterko - https://opengameart.org/content/static -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG;",
    "filtro/tono aplicado",
    "(highpass=f=1500,afade=t=in:d=0.15)",
    "",
    "se/se_tv_apagar.ogg",
    "- Que es: TV: apagar (estatica con corte) (0.3 s, 6",
    "KB, bucle: no)",
    "- Fuente: ScatterNoise1 (pack: Static) - autor:",
    "xhunterko - https://opengameart.org/content/static -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG;",
    "filtro/tono aplicado",
    "(lowpass=f=3000,afade=t=out:d=0.4)",
    "",
    "se/se_frasco_vidrio_1.ogg",
    "- Que es: Frasco de vidrio (0.2 s, 6 KB, bucle: no)",
    "- Fuente: glass_bottle_close (pack: glass bottle (open",
    "& close)) - autor: sinny - https://opengameart.org/con",
    "tent/glass-bottle-open-close - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_frasco_vidrio_2.ogg",
    "- Que es: Frasco de vidrio (0.2 s, 5 KB, bucle: no)",
    "- Fuente: glass_bottle_open (pack: glass bottle (open",
    "& close)) - autor: sinny - https://opengameart.org/con",
    "tent/glass-bottle-open-close - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_objeto_recoger.ogg",
    "- Que es: Recoger objeto (0.5 s, 8 KB, bucle: no)",
    "- Fuente: key-176034 (pack: Item Pickup / Key) -",
    "autor: Musheran -",
    "https://opengameart.org/content/item-pickup-key -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_golpe_carne.ogg",
    "- Que es: Combate: golpe a carne (0.2 s, 5 KB, bucle:",
    "no)",
    "- Fuente: squish_05 (pack: Squish Sounds Effects) -",
    "autor: EZduzziteh -",
    "https://opengameart.org/content/squish-sounds-effects",
    "- licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_golpe_pesado.ogg",
    "- Que es: Combate: golpe pesado (0.5 s, 8 KB, bucle:",
    "no)",
    "- Fuente: Deep Break 2 (pack: Deep Bone Crack/Break",
    "SFX) - autor: Zane Little Music - https://opengameart.",
    "org/content/deep-bone-crackbreak-sfx - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_fallo_aire.ogg",
    "- Que es: Combate: fallo / silbido (0.1 s, 4 KB,",
    "bucle: no)",
    "- Fuente: swish-7 (pack: Swishes Sound Pack) - autor:",
    "artisticdude -",
    "https://opengameart.org/content/swishes-sound-pack -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_curar.ogg",
    "- Que es: Curar (1.0 s, 13 KB, bucle: no)",
    "- Fuente: 02_heal_02 (pack: 8 Heals and Buffs SFX) -",
    "autor: leohpaz -",
    "https://opengameart.org/content/8-heals-and-buffs-sfx",
    "- licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_estado_veneno.ogg",
    "- Que es: Estado / veneno (1.3 s, 9 KB, bucle: no)",
    "- Fuente: 46_poison_01 (pack: 8 Magic Attacks) -",
    "autor: leohpaz -",
    "https://opengameart.org/content/8-magic-attacks -",
    "licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_cordura_baja.ogg",
    "- Que es: Cordura baja (stinger) (2.0 s, 21 KB, bucle:",
    "no)",
    "- Fuente: Monster_03.mp3 (pack: Horror Sound Effects",
    "Library) - autor: Little Robot Sound Factory - https:/",
    "/opengameart.org/content/horror-sound-effects-library",
    "- licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_enemigo_muere.ogg",
    "- Que es: Muerte de enemigo (1.3 s, 13 KB, bucle: no)",
    "- Fuente: moo-notification (pack: Sci-Fi Aliens and",
    "Cows Pack) - autor: qubodup - https://opengameart.org/",
    "content/sci-fi-aliens-and-cows-pack - licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG;",
    "filtro/tono aplicado",
    "(asetrate=26000,aresample=44100,lowpass=f=3000)",
    "",
    "se/se_screamer_1.ogg",
    "- Que es: Screamer 1 (3.0 s, 28 KB, bucle: no)",
    "- Fuente: horrorghostscream (pack: Phantom Scream) -",
    "autor: VishwaJai -",
    "https://opengameart.org/content/phantom-scream -",
    "licencia: CC-BY 4.0",
    "(https://creativecommons.org/licenses/by/4.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_screamer_2.ogg",
    "- Que es: Screamer 2 (0.9 s, 11 KB, bucle: no)",
    "- Fuente: female_scream_1 (pack: Female Scream 1) -",
    "autor: Nocturnal_Vanguard -",
    "https://opengameart.org/content/female-scream-1 -",
    "licencia: CC0",
    "(https://creativecommons.org/publicdomain/zero/1.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_screamer_3.ogg",
    "- Que es: Screamer 3 (2.9 s, 30 KB, bucle: no)",
    "- Fuente: monster_scream (pack: Monster Scream) -",
    "autor: SneidXK -",
    "https://opengameart.org/content/monster-scream -",
    "licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG",
    "",
    "se/se_nivel_victoria.ogg",
    "- Que es: Nivel / victoria (breve) (2.9 s, 23 KB,",
    "bucle: no)",
    "- Fuente: Jingle_Achievement_00.mp3 (pack: Horror",
    "Sound Effects Library) - autor: Little Robot Sound",
    "Factory - https://opengameart.org/content/horror-sound",
    "-effects-library - licencia: CC-BY 3.0",
    "(https://creativecommons.org/licenses/by/3.0/)",
    "- Modificaciones: recorte/normalizacion/OGG"
  ]
end
