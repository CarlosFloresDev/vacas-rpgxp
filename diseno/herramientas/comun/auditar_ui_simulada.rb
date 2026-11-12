# Respaldo explicito: no fabrica PNG ni afirma medir la fuente del motor.
require 'json'
prefix=File.read('diseno/herramientas/comun/simular_hd.rb',:encoding=>'UTF-8').split("$hd_log=File.open")[0]
prefix=prefix.lines.reject { |line| line.start_with?('Dir.chdir') }.join
eval(prefix,TOPLEVEL_BINDING,'dobles_ui')
class Font
  alias ui_mock_initialize initialize
  def initialize
    ui_mock_initialize
    @size=Font.default_size || 22; @name=Font.default_name
  end
end
class Bitmap
  def clear; end
  def draw_text(*args); end
  def blt(*args); end
end
module Input
  def self.raw_key_states; Array.new(512,false); end
end
class Window
  def contents_opacity=(value); @contents_opacity=[[value,0].max,255].min; end
end
source=File.read('diseno/herramientas/comun/capturar_ui.rb',:encoding=>'UTF-8')
source.sub!('ui_runtime.txt','ui_simulado_'+($MKXP ? '360' : '480')+'.txt')
source.gsub!('CAPTURA ','MEDICION SIMULADA ')
source.sub!(':motor_real=>true',":motor_real=>false,:limitacion=>'PhysFS impide iniciar Ruby en mkxp-z; text_size es estimado por dobles, no valida tinta ni fuente real'")
start=source.index('    if $ui_report[:api][:snap_to_bitmap]')
stop=source.index('    rows=[]',start)
source[start...stop]="    path=nil # Sin captura: nunca crear imagenes simuladas como evidencia nativa.\n"
source.sub!("'capturas_generadas_requieren_revision_visual'","'pendiente_motor_real'")
eval(source,TOPLEVEL_BINDING,'auditoria_ui_simulada')
metric_errors=$ui_report[:pantallas].inject(0) { |sum,p| sum+(p[:ventanas]+p[:sprites]).inject(0) { |n,w| n+w[:errores].size } }
raise 'Fallos de geometria: '+metric_errors.to_s if metric_errors>0
checks=[]
def ui_pulse(window)
  $ui_keys=[Input::C]; window.update
  $ui_keys=[]; window.update
end
b=Bitmap.new(600,128); b.font.size=16
text='Una palabra extraordinariamente_larga_sin_espacios y otra frase con acentos: acción, árbol.'
wrapped=Vacas_UI.wrap(b,text,160,true)
raise 'El ajuste pierde caracteres' unless wrapped.join.delete(' ')==text.delete(' ')
raise 'El ajuste excede el ancho' unless wrapped.all? { |s| s.scan(/./m).inject(0) { |n,ch| n+b.text_size(ch).width }<=160 }
checks.push('Ajuste conserva caracteres, acentos y palabras sin espacios')
(2..4).each do |n|
  $game_temp=Game_Temp.new
  options=(0...n).collect { |i| 'Opcion '+i.to_s+' '+('una decision larga y completa '*5) }
  $game_temp.message_text=options.join("\n")+"\n"
  $game_temp.choice_start=0; $game_temp.choice_max=n
  selected=nil; $game_temp.choice_proc=Proc.new { |i| selected=i }
  w=Window_Message.new; 20.times { w.update }
  ui_pulse(w)
  raise 'Revelar confirma una decision' unless selected.nil? && w.active
  w.index=n-1; w.update
  raise 'Cursor de opcion fuera de ventana' if w.cursor_rect.y<0 || w.cursor_rect.y+w.cursor_rect.height>w.height-32
  ui_pulse(w)
  raise 'Se altera el indice de la decision' unless selected==n-1
  w.dispose
  checks.push(n.to_s+' opciones largas: revelar, desplazar y confirmar conserva el indice')
end
$game_temp=Game_Temp.new
$game_temp.message_text=('Una frase extensa con suficientes palabras para necesitar otra pagina. '*30)+"\n"
ended=false; $game_temp.message_proc=Proc.new { ended=true }
w=Window_Message.new; 20.times { w.update }; ui_pulse(w)
raise 'No hay paginacion' unless w.instance_variable_get(:@ui_pages).size>0 && !ended
100.times { break if ended; ui_pulse(w) }
raise 'Mensaje no llega al final' unless ended
w.dispose
checks.push('Mensaje largo completa todas las paginas y llama al evento solo al final')
File.open('diseno/verificaciones/ui_regresiones_'+Vacas_HD.h.to_s+'.json','w') { |f| f.write(JSON.pretty_generate({:motor_real=>false,:comprobaciones=>checks})) }
puts JSON.pretty_generate($ui_report[:errores])
puts 'Pantallas auditadas con dobles: '+$ui_report[:pantallas].size.to_s
exit($ui_report[:errores].empty? ? 0 : 1)
