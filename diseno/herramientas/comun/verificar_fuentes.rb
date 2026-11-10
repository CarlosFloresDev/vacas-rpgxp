# Compara tokens de Ruby: omite únicamente los comentarios de las cabeceras.
require 'json'
require 'zlib'
require 'ripper'
root=File.expand_path('../../..',__dir__)
rows=Marshal.load(File.binread(File.join(root,'Data/Scripts.rxdata')))
manifest=JSON.parse(File.read(File.join(root,'diseno/scripts/manifest.json'),encoding:'UTF-8'))
def tokens(source)
  Ripper.lex(source.force_encoding('UTF-8')).reject { |t| [:on_comment,:on_sp,:on_ignored_nl,:on_nl].include?(t[1]) }.map { |t| t[1,2] }
end
errors=[]
manifest.each do |entry|
  row=rows[entry['index']]
  errors << entry['file'] unless row[1]==entry['name'] && tokens(Zlib::Inflate.inflate(row[2]))==tokens(File.binread(File.join(root,entry['file'])))
end
puts JSON.generate(scripts:manifest.size,errors:errors)
exit(errors.empty? ? 0 : 1)
