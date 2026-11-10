begin
  $hd_log=File.open('diseno/verificaciones/hd_runtime.txt','w')
  require 'zlib'
  rows=load_data('Data/Scripts.rxdata')
  rows.each do |row|
    next if row[1]=='Main'
    $hd_log.puts('CARGA '+row[1]); $hd_log.flush
    source=Zlib::Inflate.inflate(row[2])
    source.force_encoding('UTF-8') if source.respond_to?(:force_encoding)
    eval(source,TOPLEVEL_BINDING,row[1])
  end
  load 'diseno/herramientas/comun/comprobar_limites_hd.rb'
  module Input
    class << self
      alias hd_native_update update
      def update
        hd_native_update
        $hd_tick=($hd_tick || 0)+1
        if $hd_name && $hd_tick==70
          hd_capture($hd_name)
        end
        $scene=nil if $hd_name && $hd_tick>=74
      end
      def trigger?(key); ($hd_keys || []).include?(key); end
      def repeat?(key); trigger?(key); end
      def press?(key); ($hd_held || []).include?(key); end
    end
  end
  # Prohibicion expresa: el arnes no debe escribir Vacas.cfg.
  module Vacas_Config
    def self.save; raise 'El arnes no puede guardar Vacas.cfg'; end
  end
  load 'diseno/herramientas/comun/prueba_hd_runtime.rb'
  # Permite correcciones y repeticion dentro del MISMO proceso, sin otro arranque.
  deadline=Time.now+480
  while Time.now<deadline
    Graphics.update
    break if File.exist?('diseno/verificaciones/hd_terminar')
    patch='diseno/verificaciones/hd_repetir.rb'
    if File.exist?(patch)
      source=File.read(patch); File.delete(patch)
      eval(source,TOPLEVEL_BINDING,patch)
      load 'diseno/herramientas/comun/prueba_hd_runtime.rb'
    end
  end
rescue Exception => e
  $hd_log.puts('FATAL '+e.class.to_s+': '+e.message) if $hd_log
  $hd_log.puts(e.backtrace) if $hd_log
ensure
  $hd_log.close if $hd_log
end
