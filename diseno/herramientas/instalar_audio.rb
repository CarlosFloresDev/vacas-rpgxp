# Instalacion con Ruby/Marshal: sustituye solo Vacas_Interfaz, preserva IDs/Main.
require 'zlib'
require 'fileutils'
root=File.expand_path('../..',File.dirname(__FILE__))
Dir.chdir(root)
path='Data/Scripts.rxdata'
backup=File.read('diseno/herramientas/respaldo_audio.txt',:encoding=>'UTF-8').strip
raise 'Falta respaldo de Scripts' unless File.file?(backup+'/Data/Scripts.rxdata')
rows=File.open(path,'rb') { |f| Marshal.load(f) }
row=rows.find { |r| r[1]=='Vacas_Interfaz' }
raise 'No existe Vacas_Interfaz' unless row
row[2]=Zlib::Deflate.deflate(File.binread('diseno/scripts/11_interfaz.rb'))
temp=path+'.audio.tmp'
File.open(temp,'wb') { |f| Marshal.dump(rows,f) }
test=File.open(temp,'rb') { |f| Marshal.load(f) }
raise 'Diferencia de scripts' unless test==rows
FileUtils.mv(temp,path,:force=>true)
puts "Instalado Vacas_Interfaz; #{test.size} scripts cargan por Marshal."
