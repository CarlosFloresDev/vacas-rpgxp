# Carga y guardado Marshal fiel de datos RGSS1 fuera del motor.
# Table, Color y Tone reproducen su formato binario _dump/_load exacto; las
# clases RPG::* se crean vacías y Marshal conserva sus variables de instancia.
# Uso: require_relative 'rgss_datos'; RGSSDatos.cargar('Data/Map002.rxdata')
class Table
  attr_reader :xsize, :ysize, :zsize, :data
  def initialize(x, y = 1, z = 1)
    @dim = z > 1 ? 3 : (y > 1 ? 2 : 1)
    @xsize, @ysize, @zsize = x, y, z
    @data = Array.new(x * y * z, 0)
  end
  def self._load(s)
    dim, x, y, z, n = s.unpack('l5')
    t = allocate
    t.instance_variable_set(:@dim, dim)
    t.instance_variable_set(:@xsize, x)
    t.instance_variable_set(:@ysize, y)
    t.instance_variable_set(:@zsize, z)
    t.instance_variable_set(:@data, s[20, n * 2].unpack('s*'))
    t
  end
  def _dump(_l = -1)
    [@dim, @xsize, @ysize, @zsize, @data.size].pack('l5') + @data.pack('s*')
  end
  def [](x, y = 0, z = 0)
    return nil if x < 0 || y < 0 || z < 0 || x >= @xsize || y >= @ysize || z >= @zsize
    @data[x + y * @xsize + z * @xsize * @ysize]
  end
  def []=(*a)
    v = a.pop
    x, y, z = a[0], a[1] || 0, a[2] || 0
    @data[x + y * @xsize + z * @xsize * @ysize] = v
  end
end
class Color
  attr_accessor :red, :green, :blue, :alpha
  def initialize(r = 0, g = 0, b = 0, a = 255); @red, @green, @blue, @alpha = r, g, b, a; end
  def self._load(s); new(*s.unpack('E4')); end
  def _dump(_l = -1); [@red, @green, @blue, @alpha].pack('E4'); end
end
class Tone
  attr_accessor :red, :green, :blue, :gray
  def initialize(r = 0, g = 0, b = 0, a = 0); @red, @green, @blue, @gray = r, g, b, a; end
  def self._load(s); new(*s.unpack('E4')); end
  def _dump(_l = -1); [@red, @green, @blue, @gray].pack('E4'); end
end
class Module
  # Cualquier clase RGSS/RPG/Game_* desconocida se crea como objeto de datos.
  def const_missing(name)
    k = Class.new do
      def method_missing(m, *a)
        n = m.to_s
        if n.end_with?('=') then instance_variable_set('@' + n.chomp('='), a[0])
        elsif instance_variable_defined?('@' + n) then instance_variable_get('@' + n)
        else super
        end
      end
    end
    const_set(name, k)
  end
end
module RPG; end
module RGSSDatos
  module_function
  def resolver(e)
    return false unless e.message =~ /undefined class\/module ([A-Za-z_][A-Za-z_0-9:]*)/
    $1.split('::').reject(&:empty?).inject(Object) do |s, n|
      s.const_defined?(n, false) ? s.const_get(n, false) : s.const_missing(n.to_sym)
    end
    true
  end
  def cargar(path)
    begin
      File.open(path, 'rb') { |f| Marshal.load(f) }
    rescue ArgumentError, NameError => e
      retry if resolver(e)
      raise
    end
  end
  # Partidas: varios objetos Marshal concatenados.
  def cargar_todos(path)
    begin
      objs = []
      File.open(path, 'rb') { |f| objs << Marshal.load(f) until f.eof? }
      objs
    rescue ArgumentError, NameError => e
      retry if resolver(e)
      raise
    end
  end
  def guardar(path, obj)
    File.binwrite(path, Marshal.dump(obj))
  end
end
