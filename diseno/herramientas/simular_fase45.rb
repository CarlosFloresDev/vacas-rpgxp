# Complemento sin Game.exe: clases de logica originales; primitivas RGSS dobles.
# No verifica renderer, audio nativo, ni compatibilidad binaria Ruby 1.8.
require 'json'
require 'digest'
Dir.chdir(File.expand_path('../..',File.dirname(__FILE__)))
$sim_snapshot=JSON.parse(File.read('diseno/herramientas/snapshot.json',encoding:'UTF-8'))
class DataXP
  def initialize(*args);end
end
module RPG;end
class Table
  attr_accessor :xsize,:ysize,:zsize,:data
  def initialize(x=1,y=1,z=1);@xsize=x;@ysize=y;@zsize=z;@data=Array.new(x*y*z,0);end
  def [](*a);@data[(a[0]||0)+(a[1]||0)*@xsize+(a[2]||0)*@xsize*@ysize] || 0;end
  def []=(*a);v=a.pop;@data[(a[0]||0)+(a[1]||0)*@xsize+(a[2]||0)*@xsize*@ysize]=v;end
end
class Color
  attr_accessor :red,:green,:blue,:alpha
  def initialize(r=0,g=0,b=0,a=255);set(r,g,b,a);end
  def set(r,g,b,a=255);@red=r;@green=g;@blue=b;@alpha=a;end
end
class Tone < Color
  def gray;@alpha;end
  def gray=(v);@alpha=v;end
end
class Rect
  attr_accessor :x,:y,:width,:height
  def initialize(*a);set(*(a.empty? ? [0,0,0,0] : a));end
  def set(x,y,w,h);@x=x;@y=y;@width=w;@height=h;end
  def empty;set(0,0,0,0);end
end
def convertir(v,key=nil)
  if v.is_a?(Array);return v.collect { |x| convertir(x) };end
  return v unless v.is_a?(Hash)
  if v['_class']
    name=v['_class'];parts=name.split('::');parent=Object
    parts.each do |part|
      parent.const_set(part,Class.new(DataXP)) unless parent.const_defined?(part,false)
      parent=parent.const_get(part,false)
    end
    obj=parent.allocate
    v.each do |k,val|
      next if k=='_class'
      parent.class_eval { attr_accessor k.to_sym } unless parent.method_defined?(k)
      obj.instance_variable_set('@'+k,convertir(val,k))
    end
    return obj
  end
  h={};v.each { |k,val| h[k.to_s.match?(/^\d+$/) ? k.to_i : k]=convertir(val,k) };h
end
$sim_data={};$sim_snapshot.each { |k,v| $sim_data[k]=convertir(v) unless k=='Scripts' }
class RPG::AudioFile
  def initialize(name='',volume=100,pitch=100);@name=name;@volume=volume;@pitch=pitch;end
end
class Font
  class << self;attr_accessor :default_name,:default_size;end
  attr_accessor :name,:size,:bold,:italic,:color
  def initialize;@size=22;@color=Color.new;end
end
class Bitmap
  attr_reader :width,:height,:font
  def initialize(w,h=nil)
    if w.is_a?(String)
      p=File.file?(w) ? w : w+'.png'
      @width,@height=File.binread(p)[16,8].unpack('NN')
    else;@width=w;@height=h;end
    @font=Font.new
  end
  def rect;Rect.new(0,0,@width,@height);end
  def text_size(s);Rect.new(0,0,s.to_s.size*@font.size/2,@font.size);end
  def dispose;@disposed=true;end
  def disposed?;!!@disposed;end
  def method_missing(n,*args);return nil if [:fill_rect,:clear,:clear_rect,:draw_text,:blt,:stretch_blt,:hue_change].include?(n);super;end
end
class VisualXP
  attr_accessor :x,:y,:z,:ox,:oy,:zoom_x,:zoom_y,:bitmap,:visible,:tone,:color,:blend_type,:viewport,:src_rect,:rect,:active,:pause,:contents,:back_opacity,:contents_opacity,:cursor_rect,:width,:height,:windowskin,:openness,:stretch,:autotiles,:tileset,:map_data,:priorities,:ox,:oy,:bush_depth,:mirror,:type,:max
  def initialize(*a)
    @x=@y=@z=@ox=@oy=0;@zoom_x=@zoom_y=1;@opacity=255;@visible=true
    @width=@height=480;@cursor_rect=Rect.new;@src_rect=Rect.new;@rect=Rect.new(0,0,640,480)
    @tone=Tone.new;@color=Color.new;@autotiles=[];@viewport=a[0]
  end
  def opacity;@opacity;end
  def opacity=(n);@opacity=[[n,0].max,255].min;end
  def update;end
  def flash(*a);end
  def dispose;@disposed=true;end
  def disposed?;!!@disposed;end
end
class Sprite < VisualXP;end
class Plane < VisualXP;end
class Viewport < VisualXP;end
class Tilemap < VisualXP;end
class Window < VisualXP
  def initialize(*a)
    super;@x=a[0]||0;@y=a[1]||0;@width=a[2]||640;@height=a[3]||480
    @active=true;@contents_opacity=255
  end
end
class RPG::Sprite < Sprite
  def damage(*a);end
  def dispose_damage;end
  def effect?;false;end
  def animation(*a);end
  def loop_animation(*a);end
  def whiten;end
  def appear;end
  def escape;end
  def collapse;end
  def blink_on;end
  def blink_off;end
end
class RPG::Weather < VisualXP;end
module RPG::Cache
  def self.method_missing(n,*a)
    dirs={:picture=>'Pictures',:character=>'Characters',:battler=>'Battlers',:battleback=>'Battlebacks',:title=>'Titles',:gameover=>'Gameovers',:windowskin=>'Windowskins',:tileset=>'Tilesets',:autotile=>'Autotiles',:panorama=>'Panoramas',:fog=>'Fogs',:icon=>'Icons',:animation=>'Animations',:transition=>'Transitions'}
    return if n==:clear
    p='Graphics/'+dirs.fetch(n)+'/'+a[0].to_s+'.png'
    return Bitmap.new(p) if File.file?(p)
    Bitmap.new(640,480)
  end
end
module Graphics
  class << self;attr_accessor :frame_count,:frame_rate;end
  self.frame_count=0;self.frame_rate=40
  def self.update;self.frame_count+=1;end
  def self.frame_reset;end
  def self.freeze;end
  def self.transition(*a);end
end
module Input
  DOWN=2;LEFT=4;RIGHT=6;UP=8;A=11;B=12;C=13;X=14;Y=15;Z=16;L=17;R=18;SHIFT=21;CTRL=22;ALT=23;F5=25;F6=26;F7=27;F8=28;F9=29
  def self.update;end
  def self.press?(*a);false;end
  def self.trigger?(*a);false;end
  def self.repeat?(*a);false;end
  def self.dir4;0;end
  def self.dir8;0;end
end
module Audio
  [:bgm,:bgs,:me,:se].each do |kind|
    [:play,:stop,:fade].each { |action| define_singleton_method(kind.to_s+'_'+action.to_s) { |*a| } }
  end
end
class Win32API
  def initialize(*a);end
  def call(*a);0;end
end
def load_data(path)
  key=File.basename(path,'.rxdata')
  return File.open(path,'rb') { |f| Marshal.load(f) } if key=='Scripts'
  raise 'Data no disponible '+path unless $sim_data[key]
  Marshal.load(Marshal.dump($sim_data[key]))
end
$sim_snapshot['Scripts'].each do |s|
  next if s['name']=='Main'
  eval(s['code'],TOPLEVEL_BINDING,s['name'])
end
retained=['Vacas_finales.dat','Vacas_finales.tmp'].collect { |p| [p,File.file?(p) ? File.binread(p) : nil] }
cfg=File.binread('Vacas.cfg')
begin
  source=File.read('diseno/herramientas/prueba_fase45.rb',encoding:'UTF-8')
  source=source.gsub('verificacion_rgss_fase45.txt','verificacion_simulada_fase45.txt')
  source=source.gsub('RGSS real','logica simulada Ruby 3, primitivas RGSS dobles')
  source=source.gsub('f.read }',"f.read.force_encoding('UTF-8') }")
  eval(source,TOPLEVEL_BINDING,'prueba_fase45.rb')
ensure
  retained.each { |p,b| b ? File.binwrite(p,b) : (File.delete(p) if File.file?(p)) }
  raise 'Config modificada' unless cfg==File.binread('Vacas.cfg')
end
log=File.read('diseno/verificacion_simulada_fase45.txt',encoding:'UTF-8')
puts log.lines.last(8)
raise 'Fallo simulado' if log.include?('FALLO ') || !log.include?('OK FIN:')
