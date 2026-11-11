require 'json'
class Module
 def const_missing(name)
  const_set(name,Class.new do
   def self._load(bytes);o=allocate;o.instance_variable_set(:@bytes,bytes);o;end
  end)
 end
end
begin
 objects=[]
 File.open('Save1.rxdata','rb') { |f| objects << Marshal.load(f) until f.eof? }
rescue ArgumentError => e
 if e.message =~ /undefined class\/module ([A-Za-z_][A-Za-z_0-9:]*)/
  $1.split('::').reject(&:empty?).inject(Object) { |scope,name| scope.const_defined?(name,false) ? scope.const_get(name,false) : scope.const_missing(name.to_sym) };retry
 end
 raise
end
r={}
objects.each do |o|
 case o.class.to_s
 when 'Game_Switches'; a=o.instance_variable_get(:@data);r['switches']=[2,4,8,22,81,113,140,176].map { |id| [id,a[id]] }.to_h
 when 'Game_SelfSwitches';r['lavabo_A']=o.instance_variable_get(:@data)[[2,11,'A']]
 when 'Game_Party';r['jarabe']=o.instance_variable_get(:@items)[3]
 when 'Game_System';r['migraciones']=[o.instance_variable_get(:@vacas_version_sistemas),o.instance_variable_get(:@lucy_mapas_v1)]
 when 'Game_Map'
  r['mapa']=o.instance_variable_get(:@map_id)
  m=o.instance_variable_get(:@map)
  if m
   r['tileset_guardado']=m.instance_variable_get(:@tileset_id)
   e=m.instance_variable_get(:@events)[11]
   r['lavabo_guardado']=[e.instance_variable_get(:@x),e.instance_variable_get(:@y)] if e
  end
 when 'Game_Player';r['jugador']=[o.instance_variable_get(:@x),o.instance_variable_get(:@y)]
 end
end
File.write('diseno/verificaciones/diagnostico_guardado_jarabe.json',JSON.pretty_generate(r))
puts JSON.generate(r)
