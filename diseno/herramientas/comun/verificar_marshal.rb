# Comprueba Marshal real de Ruby sin ejecutar scripts ni escribir archivos.
# Las clases RGSS ausentes se representan por objetos de datos opacos.
require 'json'
class Module
  def const_missing(name)
    klass = Class.new do
      def self._load(bytes)
        object = allocate
        object.instance_variable_set(:@marshal_bytes, bytes)
        object
      end
    end
    const_set(name, klass)
  end
end
root = File.expand_path('../../..', __dir__)
files = Dir.glob(File.join(root, '**', '*.rxdata'), File::FNM_DOTMATCH)
errors = []
files.each do |file|
  begin
    # Save*.rxdata contiene varios objetos Marshal concatenados.
    File.open(file, 'rb') { |f| Marshal.load(f) until f.eof? }
  rescue StandardError => e
    if e.message =~ /undefined class\/module ([A-Za-z_][A-Za-z_0-9:]*)/
      $1.split('::').reject(&:empty?).inject(Object) { |scope, name| scope.const_defined?(name, false) ? scope.const_get(name, false) : scope.const_missing(name.to_sym) }
      retry
    else
      errors << {file: file, error: e.message}
    end
  end
end
puts JSON.pretty_generate(files: files.size, errors: errors)
exit(errors.empty? ? 0 : 1)
