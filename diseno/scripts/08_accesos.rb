#==============================================================================
# Vacas_Accesos -- Actualiza el mapa almacenado en partidas anteriores.
# Solo cambia la copia en memoria. El archivo de guardado no se escribe.
#==============================================================================
class Game_System
  def vacas_version_sistemas
    return @vacas_version_sistemas || 0
  end
  def vacas_marcar_version
    @vacas_version_sistemas = 1
  end
end
class Scene_Load
  alias vacas_accesos_read_save_data read_save_data
  def read_save_data(file)
    vacas_accesos_read_save_data(file)
    if $game_system.vacas_version_sistemas < 1
      x, y = $game_player.x, $game_player.y
      $game_map.setup($game_map.map_id)
      $game_player.moveto(x, y)
      $game_player.refresh
      for actor in $game_party.actors
        for id in actor.skills.clone
          actor.forget_skill(id) if id < 61
        end
        for id in [61, 62, 63, 64]
          actor.learn_skill(id)
        end
      end
      $game_system.vacas_marcar_version
    end
  end
end
