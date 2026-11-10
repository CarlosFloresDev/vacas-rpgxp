# Máscaras ancladas al mundo, afectadas por tonos/fundidos nativos y sin slots
# de imagen de evento. No se cambia el estado narrativo ni se guarda en Save.
class Spriteset_Map
  alias revision_update_original update
  alias revision_dispose_original dispose
  def update
    revision_update_original
    mid = $game_map.map_id
    if mid >= 1 && mid <= 16
      if @revision_mid != mid
        @revision_luz.dispose if @revision_luz
        @revision_luz = Sprite.new(@viewport1)
        @revision_luz.bitmap = RPG::Cache.picture(sprintf('revision_luz%02d',mid))
        @revision_luz.z = 2500
        @revision_mid = mid
      end
      @revision_luz.x = -$game_map.display_x / 4
      @revision_luz.y = -$game_map.display_y / 4
    elsif @revision_luz
      @revision_luz.dispose
      @revision_luz = nil
      @revision_mid = nil
    end
  end
  def dispose
    @revision_luz.dispose if @revision_luz
    revision_dispose_original
  end
end
