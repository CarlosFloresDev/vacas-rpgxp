#==============================================================================
# ** Window_Gold
#------------------------------------------------------------------------------
#  This window displays amount of gold.
#==============================================================================

class Window_Gold < Window_Base
  #--------------------------------------------------------------------------
  # * Object Initialization
  #--------------------------------------------------------------------------
  def initialize
    super(Vacas_HD.x(0), Vacas_HD.y(0), Vacas_HD.x(160), 64)
    self.contents = Bitmap.new(width - 32, height - 32)
    refresh
  end
  #--------------------------------------------------------------------------
  # * Refresh
  #--------------------------------------------------------------------------
  def refresh
    self.contents.clear
    Vacas_UI.text(contents,4,0,contents.width-8,
      $game_party.gold.to_s+' '+$data_system.words.gold,14,Vacas_UI::INK,2)
  end
end
