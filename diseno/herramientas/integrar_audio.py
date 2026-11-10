"""Instala fuentes sin borrarlas y genera el catalogo RGSS1 y atribuciones.
Ejecutar una vez sobre 11_interfaz.rb; conserva respaldo antes de escribir.
"""
from pathlib import Path
import collections, datetime, hashlib, json, re, shutil, unicodedata

ROOT = Path(__file__).resolve().parents[2]
FUENTES = ROOT / 'diseno/audio_fuentes'
manifest = json.loads((FUENTES / 'manifest.json').read_text(encoding='utf-8-sig'))
script = ROOT / 'diseno/scripts/11_interfaz.rb'
source = script.read_text(encoding='utf-8')
if 'MAP_AUDIO =' in source:
    raise SystemExit('Ya integrado: editar la tabla existente, no volver a generar.')
backup = ROOT / ('diseno/respaldos/antes_audio_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
backup.mkdir(parents=True)
for file in [script, ROOT/'Data/Scripts.rxdata', ROOT/'diseno/AUDIO.md', ROOT/'diseno/INTERFAZ.md']:
    dest = backup / file.relative_to(ROOT)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file, dest)
(ROOT/'diseno/herramientas/respaldo_audio.txt').write_text(str(backup), encoding='utf8')

original = re.findall(r":(\w+)=>\[:(\w+),'([^']+)',\d+,\d+,'([^']*)'\]", source)
old = {name:(key,caption) for key,kind,name,caption in original}
counts = collections.Counter()
used_keys = {key for key,caption in old.values()}
catalog = []
def slug(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii','ignore').decode().lower()
    return re.sub('[^a-z0-9]+','_',text).strip('_')
def ruby(text):
    return json.dumps(text, ensure_ascii=False)
for entry in manifest:
    src = FUENTES/entry['file']
    assert src.is_file(), src
    dest = ROOT/(entry['destino'] or ('Audio/'+entry['type'].upper()+'/'+src.name))
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.suffix.lower() != src.suffix.lower():
        # El pack incluye WAV reales; nunca renombrar bytes OGG como WAV.
        wav = src.with_suffix(dest.suffix)
        assert wav.is_file() and wav.read_bytes()[:4] == b'RIFF', wav
        shutil.copy2(wav, dest)
        shutil.copy2(src, dest.with_suffix(src.suffix))
    else:
        shutil.copy2(src, dest)
    if dest.stem in old:
        key, caption = old[dest.stem]
    else:
        base = slug(entry['use'])
        counts[base] += 1
        key = base + ('_'+str(counts[base]) if counts[base]>1 else '')
        if key in used_keys: key += '_'+entry['type']
        while key in used_keys: key += '_extra'
        used_keys.add(key)
        caption = entry['use'] if entry['type']=='bgs' else ''
    kind = entry['type']
    volume = {'bgm':42,'bgs':26,'me':56,'se':52}[kind]
    if key in ['titulo','combate','jefe','persecucion','gameover']:
        volume = {'titulo':56,'combate':60,'jefe':64,'persecucion':64,'gameover':45}[key]
    if 'paso' in key: volume = 24
    if key in ['cursor','confirmar','cancelar','error']: volume = 42
    if 'susto' in key or 'screamer' in key: volume = 62
    catalog.append(dict(entry, key=key, destino=str(dest.relative_to(ROOT)).replace('\\','/'),
                        volume=volume, caption=caption))
by_file = {Path(r['file']).stem:r['key'] for r in catalog}
rows = ['    :%s=>[:%s,%s,%d,100,%s]' % (r['key'],r['type'],ruby(Path(r['destino']).stem),r['volume'],ruby(r['caption'])) for r in catalog]
source = re.sub(r'  TABLE = \{.*?\n  \}', lambda m: '  TABLE = {\n'+',\n'.join(rows)+'\n  }',source,count=1,flags=re.S)

# Todas las referencias de los datos actuales se resuelven localmente por LEGACY.
snapshot = json.loads((ROOT/'diseno/herramientas/snapshot.json').read_text(encoding='utf8'))
refs = set()
def walk(obj):
    if isinstance(obj,dict):
        if obj.get('_class')=='RPG::AudioFile' and obj.get('name'): refs.add(obj['name'])
        for val in obj.values(): walk(val)
    elif isinstance(obj,list):
        for val in obj: walk(val)
walk(snapshot)
for p in (ROOT/'diseno/scripts').glob('*.rb'):
    refs.update(re.findall(r'AudioFile.new\([\'\"]([^\'\"]+)',p.read_text(encoding='utf8')))
refs.update(['093-Attack05','057-Wrong01','045-Push01'])
explicit = {'058-Slow01':'titulo','036-Dungeon02':'combate','016-Shock01':'victoria',
 '015-Mystery01':'derrota','092-Attack04':'susto','140-Darkness03':'golpe',
 '040-Knock01':'puerta','024-Door01':by_file['se_puerta_madera_abrir'],
 '026-Door03':by_file['se_puerta_metal_abrir'],'032-Switch01':by_file['se_interruptor_luz'],
 '041-Knock02':by_file['se_puerta_manija_trabada'],'042-Knock03':by_file['se_puerta_crujido'],
 '044-Chest01':by_file['se_objeto_recoger'],'045-Push01':by_file['se_gancho_metal'],
 '046-Book01':by_file['se_papel_nota_1'],'052-Cannon01':by_file['se_golpe_pesado'],
 '057-Wrong01':'error','093-Attack05':by_file['se_cuchillada_1'],
 '070-Animal05':by_file['se_mugido_angustia'],'123-Thunder01':by_file['se_golpe_pesado'],
 '001-Battle01':'combate','001-Victory01':'victoria','005-Defeat01':'derrota','064-Slow07':'titulo',
 '001-System01':'cursor','002-System02':'confirmar','003-System03':'cancelar','004-System04':'error',
 '005-System05':'error','006-System06':by_file['se_objeto_recoger'],
 '007-System07':by_file['se_fallo_aire'],'008-System08':by_file['se_enemigo_muere'],
 '009-System09':by_file['se_enemigo_muere'],'010-System10':'confirmar',
 '011-System11':by_file['se_fallo_aire'],'012-System12':by_file['se_fallo_aire'],
 '001-Wind01':'piso','002-Wind02':by_file['bgs_corral_ganado'],
 '005-Rain01':by_file['bgs_lluvia_calle'],'016-Drips01':'alcantarillas',
 '015-Quake01':'matadero','018-Darkness01':by_file['bgs_tv_estatica'],
 '013-Move01':by_file['se_puerta_crujido']}
legacy = {}
real_names = {Path(r['destino']).stem for r in catalog}
for name in sorted(refs):
    if name in real_names: continue
    key = explicit.get(name)
    if key is None:
        if re.search(r'Heal|Remedy|Raise|Support',name): key=by_file['se_curar']
        elif re.search(r'Water|Ice',name): key=by_file['se_chapoteo_1']
        elif re.search(r'Wind|Action|Move|Jump',name): key=by_file['se_fallo_aire']
        elif re.search(r'Darkness',name): key=by_file['se_cordura_baja']
        else: key=by_file['se_golpe_carne']
    legacy[name]=key
source = re.sub(r'  LEGACY = \{.*?\}\n', '  LEGACY = {\n'+',\n'.join('    '+ruby(n)+'=>:'+k for n,k in legacy.items())+'\n  }\n',source,count=1,flags=re.S)

# Zona visual, musica, ambiente, superficie. Los 21 mapas se asignan explicitamente.
settings = [
 (1,'piso','bgm_piso_exploracion','vacas_piso','baldosa'),
 (2,'piso','bgm_piso_exploracion','vacas_piso','baldosa'),
 (3,'piso','bgm_piso_exploracion','bgs_edificio_abandonado','baldosa'),
 (4,'piso','bgm_extra_calle_noche','bgs_lluvia_calle','concreto'),
 (5,'matadero','bgm_matadero_exploracion','bgs_lluvia_calle','concreto'),
 (6,'matadero','bgm_matadero_exploracion','bgs_nevera_zumbido','baldosa'),
 (7,'matadero','bgm_matadero_exploracion','bgs_corral_ganado','concreto'),
 (8,'matadero','bgm_matadero_exploracion','vacas_matadero','metal'),
 (9,'camaras','bgm_camaras_frias','vacas_camaras','metal'),
 (10,'matadero','bgm_matadero_exploracion','bgs_reloj_tictac','madera'),
 (11,'matadero','bgm_matadero_exploracion','bgs_matadero_cadenas','metal'),
 (12,'laboratorio','bgm_tv_segura','bgs_reloj_tictac','madera'),
 (13,'laboratorio','bgm_lucy_laboratorio','bgs_nevera_zumbido','baldosa'),
 (14,'laboratorio','bgm_extra_sotano','bgs_edificio_abandonado','concreto'),
 (15,'laboratorio','bgm_lucy_laboratorio','bgs_fluorescente_zumbido','baldosa'),
 (16,'laboratorio','bgm_extra_tension_lab','vacas_laboratorio','baldosa'),
 (17,'alcantarillas','bgm_alcantarillas','vacas_alcantarillas','concreto'),
 (18,'alcantarillas','bgm_extra_dark_drone','bgs_alcantarilla_goteo','concreto'),
 (19,'alcantarillas','bgm_alcantarillas','bgs_agua_corriente','agua'),
 (20,'manada','bgm_camara_manada','vacas_manada','concreto'),
 (21,'manada','bgm_tv_segura','bgs_mazmorra_eco','concreto')]
maps = []
lines = []
for id,zone,bgm,bgs,surface in settings:
    lines.append('    %d=>[:%s,:%s,:%s,:%s]' % (id,zone,by_file[bgm],by_file[bgs],surface))
    maps.append(dict(id=id,name=snapshot['MapInfos'][str(id)]['name'],zone=zone,bgm=by_file[bgm],bgs=by_file[bgs],surface=surface))
zone_code = '''  MAP_AUDIO = {
%s
  }
  # Tags de terreno XP 1..5: agua, metal, madera, concreto, baldosa.
  TERRAIN_STEPS = {1=>:agua,2=>:metal,3=>:madera,4=>:concreto,5=>:baldosa}
  STEP_KEYS = {
%s
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
    play(keys[@step_variant %% keys.size])
  end
''' % (',\n'.join(lines),',\n'.join('    :'+s+'=>['+','.join(':'+by_file['se_paso_'+base+'_'+str(i)] for i in range(1,4))+']' for s,base in [('baldosa','baldosa'),('metal','rejilla_metal'),('agua','agua'),('madera','madera'),('concreto','concreto')]))
source = re.sub(r'  def self.zone\n.*?\n  end\n',zone_code,source,count=1,flags=re.S)
source = source.replace("key=Vacas_Audio::LEGACY[File.basename(name.to_s)]", "base=File.basename(name.to_s).sub(/\\.[^.]+$/, '')\n        key=Vacas_Audio::LEGACY[base]\n        key=Vacas_Audio.screamer if base=='092-Attack04' && Vacas_Audio.screamer")
source = source.replace("name='Audio/'+kind.to_s.upcase+'/'+row[1]", "name='Audio/'+kind.to_s.upcase+'/'+row[1]\n          volume=[volume,row[2]].min; pitch=row[3]")
source = source.replace("if key==:susto || File.basename(name.to_s)==Vacas_Audio::TABLE[:susto][1]", "if key==:susto || base==Vacas_Audio::TABLE[:susto][1] || base.index('se_screamer_')==0 || key.to_s.index('screamer_')==0")
# Los eventos paralelos conservan tono/niebla; su BGS RTP usa la seleccion del mapa.
source = source.replace('if key\n          row=Vacas_Audio::TABLE[key]', 'if key && kind==:bgs && $game_map && Vacas_Audio::MAP_AUDIO[$game_map.map_id]\n          key=Vacas_Audio::MAP_AUDIO[$game_map.map_id][2]\n        end\n        if key\n          row=Vacas_Audio::TABLE[key]')
source = source.replace("['Nueva partida','Continuar','Ajustes','Salir']", "['Nueva partida','Continuar','Ajustes','Creditos','Salir']")
source = source.replace('when 3; command_shutdown', 'when 3; Vacas_Audio.play(:confirmar); $scene=Scene_VacasCredits.new\n    when 4; command_shutdown')
source = re.sub(r'    chasing=\[10,90,120,122\].*?      @ui_chasing=chasing\n    end', '    Vacas_Audio.map_audio if $scene.is_a?(Scene_Map)', source,count=1,flags=re.S)
source = source.replace('    Vacas_Audio.play(Vacas_Audio.zone)','    Vacas_Audio.map_audio')
source = source.replace('    ui_map_autoplay\n', '    ui_map_autoplay\n')
source = re.sub(r'    if @ui_steps%2==0.*?\n    end\n  end\nend\s*$', '''    now=Graphics.frame_count
    if @ui_steps%3==0 && !@move_route_forcing && !$game_temp.message_window_showing &&
        (!@ui_step_frame || now<@ui_step_frame || now-@ui_step_frame>=12)
      Vacas_Audio.footstep(self); @ui_step_frame=now
    end
  end
end
''',source,count=1,flags=re.S)
# Atribuciones completas incorporadas: no dependen de Markdown externo al distribuir.
credits=(FUENTES/'CREDITOS.md').read_text(encoding='utf-8-sig').splitlines()
credit_code='\nmodule Vacas_Audio\n  CREDITS = [\n'+',\n'.join('    '+ruby(l.replace('`','')) for l in credits)+'\n  ]\n'
credit_code+='  def self.screamer; @screamer; end\n  def self.screamer=(key); @screamer=key; end\nend\n'
source += credit_code
script.write_text(source,encoding='utf8')
(ROOT/'CREDITOS_AUDIO.md').write_text((FUENTES/'CREDITOS.md').read_text(encoding='utf-8-sig'),encoding='utf8')
(ROOT/'diseno/audio_catalogo.json').write_text(json.dumps(dict(entries=catalog,maps=maps,legacy=legacy,backup=str(backup)),ensure_ascii=False,indent=2),encoding='utf8')
print('Instaladas',len(catalog),'entradas;',len(legacy),'traducciones RTP. Respaldo:',backup)
