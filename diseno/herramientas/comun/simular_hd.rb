# Ejecuta todas las secciones instaladas con dobles RGSS del arnes existente.
# No genera capturas: comprueba carga, geometria y logica, no render ni audio.
require 'zlib'
require 'digest'
Dir.chdir(File.expand_path('../../..',File.dirname(__FILE__)))
prefix=File.read('diseno/herramientas/comun/simular_fase45.rb',encoding:'UTF-8').split("$sim_snapshot['Scripts'].each do |s|")[0]
prefix=prefix.lines.reject { |line| line.start_with?('Dir.chdir') }.join
eval(prefix,TOPLEVEL_BINDING,'dobles_rgss')
$MKXP=ARGV[0]!='clasico'
module Graphics
  def self.width; @hd_width || 640; end
  def self.height; @hd_height || 480; end
  def self.resize_screen(w,h); @hd_width=w; @hd_height=h; end
end
module System; VERSION='SIMULADO'; end
class RPG::Weather
  def initialize(*a); super; end
end
class Table
  def _dump(depth); [3,@xsize,@ysize,@zsize,@data.size].pack('L5')+@data.pack('S*'); end
  def self._load(bytes)
    dim,x,y,z,n=bytes.unpack('L5'); t=new(x,y,z)
    t.data=bytes[20,n*2].unpack('S*'); t
  end
end
class Color
  def self._load(bytes); new(*bytes.unpack('d4')); end
  def _dump(depth); [@red,@green,@blue,@alpha].pack('d4'); end
end
def load_data(path)
  File.open(path,'rb') { |f| Marshal.load(f) }
end
$hd_log=File.open('diseno/verificaciones/hd_simulado_'+($MKXP ? '360' : '480')+'.txt','w')
before=Digest::SHA256.file('Vacas.cfg').hexdigest
rows=Marshal.load(File.binread('Data/Scripts.rxdata'))
rows.each do |row|
  next if row[1]=='Main'
  source=Zlib::Inflate.inflate(row[2]).force_encoding('UTF-8')
  eval(source,TOPLEVEL_BINDING,row[1])
  $hd_log.puts('CARGA '+row[1])
end
load 'diseno/herramientas/comun/comprobar_limites_hd.rb'
module Input
  def self.raw_key_states; Array.new(512,false); end
  def self.update
    $hd_tick=($hd_tick || 0)+1
    if $hd_name && $hd_tick==70; hd_capture($hd_name); end
    if $hd_name && $hd_tick>=74
      $scene.instance_variable_set(:@terminada,true) if $scene.is_a?(Scene_VacasCine)
      $scene=nil
    end
  end
  def self.trigger?(key); ($hd_keys || []).include?(key); end
  def self.repeat?(key); trigger?(key); end
  def self.press?(key); ($hd_held || []).include?(key); end
end
module Vacas_Config
  def self.save; raise 'No se puede escribir Vacas.cfg'; end
end
suite=File.read('diseno/herramientas/comun/prueba_hd_runtime.rb',encoding:'UTF-8')
suite=suite.sub("  Graphics.transition(0)\n  3.times { Graphics.update }\n  b=Graphics.snap_to_bitmap\n  b.to_file('diseno/capturas/interfaz/hd_'+name+'.png')\n  b.dispose",'')
suite=suite.sub("unless Vacas_HD.mkxp?","unless Vacas_HD.mkxp? == $MKXP")
suite=suite.sub('[640,360]','[640,($MKXP ? 360 : 480)]')
suite=suite.sub("  $hd_log.puts('Ruby '+RUBY_VERSION+' System='+System.methods.sort.inspect)","  $hd_log.puts('SIMULACION Ruby '+RUBY_VERSION)")
eval(suite,TOPLEVEL_BINDING,'suite_hd_simulada')
raise 'Vacas.cfg cambiado' unless before==Digest::SHA256.file('Vacas.cfg').hexdigest
$hd_log.close
report=File.read('diseno/verificaciones/hd_simulado_'+($MKXP ? '360' : '480')+'.txt')
puts report.lines.grep(/^(OK|FALLO|FUERA|FIN)/)
exit(report.include?('FALLO ') ? 1 : 0)
