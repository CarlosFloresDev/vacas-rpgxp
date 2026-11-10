# Cargar dentro de RGSS/mkxp despues de los scripts del juego.
# Recorre clases de escena/ventana y comprueba las instancias visibles vivas.
# Las listas pueden tener contents mayor que la ventana: eso es scroll, no fuga.
module Vacas_HD_Check
  def self.inspect_windows(label, log)
    classes = []
    ObjectSpace.each_object(Class) do |c|
      classes.push(c.to_s) if c.to_s =~ /^(Scene_|Window_)/
    end
    failures = []
    ObjectSpace.each_object(Window) do |w|
      next if w.disposed? || !w.visible
      r = [w.x,w.y,w.width,w.height]
      if r[0] < 0 || r[1] < 0 || r[0]+r[2] > Vacas_HD.w || r[1]+r[3] > Vacas_HD.h
        failures.push(w.class.to_s+' '+r.inspect)
      end
    end
    log.puts('LIMITES '+label+' clases='+classes.sort.join(','))
    failures.each { |s| log.puts('FUERA '+s) }
    log.flush
    raise failures.join('; ') unless failures.empty?
  end
end
