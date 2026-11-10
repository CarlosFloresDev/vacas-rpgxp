# Instala la intro de Feka Studios con Ruby/Marshal (editor RPGXP cerrado).
# - Inserta/actualiza la seccion Vacas_IntroFeka justo antes de Main.
# - Hace que Main arranque en Scene_FekaIntro (solo al iniciar el programa).
# Idempotente. Uso: ruby diseno/herramientas/instalar_intro_feka.rb
require 'zlib'
require 'fileutils'
root=File.expand_path('../..',File.dirname(__FILE__))
Dir.chdir(root)
path='Data/Scripts.rxdata'
backup='diseno/respaldos/antes_intro_feka/Data/Scripts.rxdata'
unless File.file?(backup)
  FileUtils.mkdir_p(File.dirname(backup))
  FileUtils.cp(path,backup)
  puts "Respaldo creado: #{backup}"
end
rows=File.open(path,'rb') { |f| Marshal.load(f) }
nombre='Vacas_IntroFeka'.b
codigo=Zlib::Deflate.deflate(File.binread('diseno/scripts/12_intro_feka.rb'))
main=rows.index { |r| r[1]=='Main' }
raise 'No existe Main' unless main
row=rows.find { |r| r[1]==nombre }
if row
  row[2]=codigo
else
  id=rows.map { |r| r[0] }.select { |n| n.between?(99823000,99823999) }.max+1
  rows.insert(main,[id,nombre.dup.force_encoding(rows[main][1].encoding),codigo])
  main+=1
end
fuente=Zlib::Inflate.inflate(rows[main][2])
unless fuente.include?('Scene_FekaIntro.new')
  raise 'Main no arranca en Scene_Aviso' unless fuente.include?('$scene = Scene_Aviso.new')
  fuente=fuente.sub('$scene = Scene_Aviso.new','$scene = Scene_FekaIntro.new')
  rows[main][2]=Zlib::Deflate.deflate(fuente)
end
raise 'Vacas_IntroFeka debe ir justo antes de Main' unless rows[main-1][1]==nombre
temp=path+'.intro.tmp'
File.open(temp,'wb') { |f| Marshal.dump(rows,f) }
test=File.open(temp,'rb') { |f| Marshal.load(f) }
raise 'Diferencia de scripts' unless test==rows
FileUtils.mv(temp,path,:force=>true)
puts "Instalado Vacas_IntroFeka; #{test.size} scripts cargan por Marshal."
