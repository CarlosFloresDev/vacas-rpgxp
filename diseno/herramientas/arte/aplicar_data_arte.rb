# Integración incremental; conserva clases RPG, tablas, páginas y comandos.
require_relative '../comun/rgss_datos'
require 'fileutils'
require 'json'
require 'digest'
ROOT = File.expand_path('../../..', __dir__)
Dir.chdir(ROOT)
BACK = 'diseno/respaldos/antes_cambios_data_arte'
FileUtils.mkdir_p(BACK)
Dir['Data/*'].each do |p|
  target = File.join(BACK, File.basename(p))
  FileUtils.cp(p, target) unless File.exist?(target)
end
datos = {}
cambios = []
get = lambda { |name| datos[name] ||= RGSSDatos.cargar("Data/#{name}.rxdata") }
set = lambda do |obj, field, value, ruta|
  old = obj.instance_variable_get("@#{field}")
  next if old == value
  # Ruby moderno no debe introducir metadatos de encoding en RGSS1.
  value = value.b if value.is_a?(String)
  cambios << {ruta: ruta + '.' + field.to_s, antes: old, despues: value}
  obj.instance_variable_set("@#{field}", value)
end
asset = lambda do |cat, name|
  raise "Falta #{cat}/#{name}" unless File.file?("Graphics/#{cat}/#{name}.png")
  name
end
(2..8).each do |id|
  a = get.call('Actors')[id]
  %w[character battler].each do |kind|
    n = asset.call(kind == 'character' ? 'Characters' : 'Battlers', format('vacas_reserva_actor%02d', id))
    set.call(a, kind + '_name', n, "Actors[#{id}]")
    set.call(a, kind + '_hue', 0, "Actors[#{id}]")
  end
end
# La apertura ya retira estos actores antes de jugar. Evitar su exposición inicial.
set.call(get.call('System'), 'party_members', [1], 'System')
maps = Dir['Data/Map[0-9]*.rxdata'].map { |p| File.basename(p, '.rxdata') }
used_tilesets = []
maps.each do |name|
  m = get.call(name)
  used_tilesets << m.tileset_id
  m.events.each do |id, event|
    event.pages.each_with_index do |page, pi|
      old = page.graphic.character_name
      next unless %w[vacas_guernsey4 vacas_junco vacas_muesca].include?(old)
      set.call(page.graphic, 'character_name', asset.call('Characters', old + '_80'), "#{name}.events[#{id}].pages[#{pi}].graphic")
    end
  end
end
{ '016-Ice01' => [30,31,32], '024-Support01' => [53,54,55] }.each do |old, ids|
  ids.each { |id| set.call(get.call('Animations')[id], 'animation_name', asset.call('Animations', 'vacas_rejilla_' + old), "Animations[#{id}]") }
end
# Retirar SOLO referencias gráficas de reservas no utilizadas, sin borrar IDs.
get.call('Tilesets').each_with_index do |ts, id|
  next unless ts && id.between?(1,50)
  raise "Tileset RTP utilizado #{id}" if used_tilesets.include?(id)
  %w[tileset_name panorama_name fog_name battleback_name].each { |f| set.call(ts, f, '', "Tilesets[#{id}]") }
  set.call(ts, 'autotile_names', Array.new(7) { ''.b }, "Tilesets[#{id}]")
end
used_enemies = get.call('Troops').compact.flat_map { |t| t.members.map(&:enemy_id) }.uniq
(22..32).each do |id|
  raise "Enemigo RTP utilizado #{id}" if used_enemies.include?(id)
  set.call(get.call('Enemies')[id], 'battler_name', '', "Enemies[#{id}]")
end
%w[Weapons Armors Skills].each do |name|
  get.call(name).each_with_index do |obj,id|
    next unless obj && obj.icon_name =~ /^\d{3}-/
    # Solo tubo y ropa son equipo del protagonista; reservas sin icono.
    icon = name == 'Weapons' && id == 1 ? 'vacas_tubo_oxidado' : name == 'Armors' && id == 25 ? 'vacas_ropa_trabajo' : ''
    asset.call('Icons',icon) unless icon.empty?
    set.call(obj,'icon_name',icon,"#{name}[#{id}]")
  end
end
# Verificación semántica completa por serialización: revertir en memoria cada
# cambio autorizado debe reconstruir exactamente el Marshal previo normalizado.
datos.each do |name,obj|
  old = RGSSDatos.cargar("Data/#{name}.rxdata")
  next if Marshal.dump(old) == Marshal.dump(obj)
  if name =~ /^Map\d+$/
    copy = Marshal.load(Marshal.dump(obj))
    copy.events.each do |id,event|
      event.pages.each_with_index { |p,i| p.graphic.character_name = old.events[id].pages[i].graphic.character_name }
    end
    raise "Cambio de jugabilidad no autorizado: #{name}" unless Marshal.dump(copy) == Marshal.dump(old)
  end
  RGSSDatos.guardar("Data/#{name}.rxdata",obj)
  raise "Marshal no fiel #{name}" unless Marshal.dump(RGSSDatos.cargar("Data/#{name}.rxdata")) == Marshal.dump(obj)
end
report = {cambios: cambios, mapas: cambios.map { |c| c[:ruta][/^Map\d+/] }.compact.uniq,
  respaldo: BACK, mapas_solo_nombre_grafico: true,
  hashes_respaldo: Dir[BACK+'/*.rxdata'].to_h { |p| [File.basename(p),Digest::SHA256.file(p).hexdigest] }}
out = 'diseno/verificaciones/data_arte_aplicado.json'
File.write(out, JSON.pretty_generate(report)) unless cambios.empty?
puts "Aplicados #{cambios.size} campos; mapas conservan posición, páginas, comandos, through y tablas."
