# Prueba SIMULADA (sin Game.exe): ejecuta el codigo real de Scene_FekaIntro extraido de
# Data/Scripts.rxdata contra dobles minimos de RGSS. Valida logica, no el render del motor.
# Uso: ruby diseno/herramientas/prueba_intro_feka_simulada.rb
require 'zlib'
Dir.chdir(File.expand_path('../..',File.dirname(__FILE__)))
rows=File.open('Data/Scripts.rxdata','rb') { |f| Marshal.load(f) }
i=rows.index { |r| r[1]=='Vacas_IntroFeka' }
def ok(c,t); puts((c ? 'OK ' : 'FALLO ')+t); raise t unless c; end
ok(i && rows[i+1][1]=='Main' && rows[i-1][1]=='Vacas_Interfaz','Seccion Vacas_IntroFeka entre Vacas_Interfaz y Main')
main=Zlib::Inflate.inflate(rows[i+1][2])
ok(main.scan(/\$scene = (\w+)\.new/).flatten==['Scene_FekaIntro'],'Main arranca en Scene_FekaIntro')
todo=rows.map { |r| Zlib::Inflate.inflate(r[2]).force_encoding('UTF-8') }
ok(todo.join.scan('Scene_FekaIntro.new').size==1,'Solo Main crea la intro (titulo, game over y salir al titulo no pasan por ella)')
class Color; attr_accessor :alpha; def initialize(r,g,b,a=255); raise 'color' unless [r,g,b,a].all? { |v| v.is_a?(Numeric) }; @alpha=a; end; end
class Rect; attr_reader :v; def set(*a); raise 'rect' unless a.size==4 && a.all? { |n| n.is_a?(Integer) && n>=0 }; @v=a; end; end
class Bitmap
  attr_reader :width,:height
  def initialize(w,h); @width=w; @height=h; end
  def fill_rect(*a); end
  def dispose; @d=true; end
  def disposed?; @d; end
end
class Sprite
  VIVOS=[]
  attr_accessor :bitmap,:z,:blend_type,:color,:ox,:oy,:zoom_x,:zoom_y,:opacity
  attr_reader :x,:y,:src_rect
  def initialize; @src_rect=Rect.new; VIVOS.push(self); end
  def x=(v); raise 'x no entero' unless v.is_a?(Integer); @x=v; end
  def y=(v); raise 'y no entero' unless v.is_a?(Integer); @y=v; end
  def dispose; @d=true; VIVOS.delete(self); end
  def disposed?; @d; end
end
module RPG; module Cache
  def self.picture(n)
    raise Errno::ENOENT,n if $faltan
    w,h=File.binread("Graphics/Pictures/#{n}.png")[16,8].unpack('NN'); Bitmap.new(w,h)
  end
end; end
module Graphics; def self.update; $frames+=1; end; def self.transition(*a); end; def self.freeze; end; end
module Input
  C=13; B=12
  def self.update; $tick+=1; raise 'no termina' if $tick>2000; end
  def self.trigger?(k); $teclas[$tick]==k; end
end
module Audio
  def self.se_play(n,v,p); ok(File.file?(n+'.ogg'),'Existe '+n+'.ogg') unless $se.include?(n); $se.push(n); end
  def self.se_stop; end
end
module Vacas_Config; def self.get(k); $cfg[k]; end; end
class Scene_Aviso; end
class Scene_Title; end
eval(todo[i],TOPLEVEL_BINDING,'Vacas_IntroFeka')
def correr(teclas={},cfg={:intensidad=>70})
  $tick=0; $frames=0; $teclas=teclas; $cfg=cfg; $se=[]
  $scene=Scene_FekaIntro.new; $scene.main
  ok($scene.is_a?(Scene_Aviso),'  -> pasa a Scene_Aviso (aviso de contenido -> titulo)')
  ok(Sprite::VIVOS.empty?,'  -> todos los sprites liberados')
  $tick
end
n=correr; ok(n==250 && $se.size==2,"Completa: #{n} fotogramas = #{n/40.0} s, efectos: #{$se.map { |s| File.basename(s) }.join(', ')}")
n=correr({60=>Input::C}); ok(n==70 && $se.size==1,"C/Intro en el fotograma 60 salta: fin en #{n}")
n=correr({5=>Input::B}); ok(n==15 && $se.empty?,"Esc en el fotograma 5 salta: fin en #{n}, sin efectos")
n=correr({},{:intensidad=>0}); ok(n==250,'Intensidad 0: sin parpadeo ni glitch, misma duracion')
$faltan=true; n=correr; ok(n==0,'Graficos ausentes: la intro se omite sin error')
puts 'OK FIN INTRO FEKA (simulada)'
