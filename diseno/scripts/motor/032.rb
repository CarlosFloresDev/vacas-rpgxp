#==============================================================================
# ** Window_Help
#------------------------------------------------------------------------------
#  This window shows skill and item explanations along with actor status.
#==============================================================================

class Window_Help < Window_Base
  #--------------------------------------------------------------------------
  # * Object Initialization
  #--------------------------------------------------------------------------
  def initialize
    super(0, 0, Vacas_HD.w, $scene.is_a?(Scene_Item) ? 96 : 64)
    self.contents = Bitmap.new(width - 32, height - 32)
  end
  #--------------------------------------------------------------------------
  # * Set Text
  #  text  : text string displayed in window
  #  align : alignment (0..flush left, 1..center, 2..flush right)
  #--------------------------------------------------------------------------
  def set_text(text, align = 0)
    # If at least one part of text and alignment differ from last time
    if text != @text or align != @align
      # Redraw text
      self.contents.clear
      self.contents.font.color = normal_color
      self.contents.font.size=14
      # Reservar una columna para el contador, sin tapar la ultima palabra.
      @ui_help_lines=Vacas_UI.wrap(contents,text,self.width-104)
      @ui_help_page=0; @ui_help_ticks=0
      @text = text
      @align = align
      draw_help_page
      @actor = nil
    end
    self.visible = true
  end
  def draw_help_page
    contents.clear
    count=[contents.height/24,1].max
    @ui_help_lines[@ui_help_page*count,count].to_a.each_with_index do |line,i|
      Vacas_UI.text(contents,4,i*24,self.width-104,line,14,Vacas_UI::INK,@align || 0)
    end
    pages=[(@ui_help_lines.size+count-1)/count,1].max
    if pages>1
      Vacas_UI.text(contents,contents.width-60,0,56,
        (@ui_help_page+1).to_s+'/'+pages.to_s,14,Vacas_UI::MINT,2)
    end
  end
  def update
    super
    return unless @ui_help_lines && @text
    count=[contents.height/24,1].max
    @ui_help_ticks+=1
    if @ui_help_lines.size>count && @ui_help_ticks%180==0
      @ui_help_page=(@ui_help_page+1)%((@ui_help_lines.size+count-1)/count)
      draw_help_page
    end
  end
  #--------------------------------------------------------------------------
  # * Set Actor
  #     actor : status displaying actor
  #--------------------------------------------------------------------------
  def set_actor(actor)
    if actor != @actor
      self.contents.clear
      draw_actor_name(actor, 4, 0)
      draw_actor_state(actor, 140, 0)
      draw_actor_hp(actor, 284, 0)
      draw_actor_sp(actor, 460, 0)
      @actor = actor
      @text = nil
      self.visible = true
    end
  end
  #--------------------------------------------------------------------------
  # * Set Enemy
  #     enemy : name and status displaying enemy
  #--------------------------------------------------------------------------
  def set_enemy(enemy)
    text = enemy.name
    state_text = make_battler_state_text(enemy, 112, false)
    if state_text != ""
      text += "  " + state_text
    end
    set_text(text, 1)
  end
end
