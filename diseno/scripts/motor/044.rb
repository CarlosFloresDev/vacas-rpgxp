#==============================================================================
# ** Window_Status
#------------------------------------------------------------------------------
#  This window displays full status specs on the status screen.
#==============================================================================

class Window_Status < Window_Base
  #--------------------------------------------------------------------------
  # * Object Initialization
  #     actor : actor
  #--------------------------------------------------------------------------
  def initialize(actor)
    super(Vacas_HD.x(0), Vacas_HD.x(0), Vacas_HD.w, Vacas_HD.h - Vacas_HD.x(0))
    self.contents = Bitmap.new(width - 32, height - 32)
    @actor = actor
    refresh
  end
  #--------------------------------------------------------------------------
  # * Refresh
  #--------------------------------------------------------------------------
  def status_y(n)
    (n * (self.contents.height - 32) / 416.0).round
  end
  def refresh
    self.contents.clear
    draw_actor_graphic(@actor, 40, status_y(112))
    draw_actor_name(@actor, 4, status_y(0))
    draw_actor_class(@actor, 4 + 144, status_y(0))
    draw_actor_level(@actor, 96, status_y(32))
    draw_actor_state(@actor, 96, status_y(64))
    draw_actor_hp(@actor, 96, status_y(112), 172)
    draw_actor_sp(@actor, 96, status_y(144), 172)
    draw_actor_parameter(@actor, 96, status_y(192), 0)
    draw_actor_parameter(@actor, 96, status_y(224), 1)
    draw_actor_parameter(@actor, 96, status_y(256), 2)
    draw_actor_parameter(@actor, 96, status_y(304), 3)
    draw_actor_parameter(@actor, 96, status_y(336), 4)
    draw_actor_parameter(@actor, 96, status_y(368), 5)
    draw_actor_parameter(@actor, 96, status_y(400), 6)
    self.contents.font.color = system_color
    self.contents.draw_text(Vacas_HD.w / 2, status_y(48), 80, 32, "Exp.")
    self.contents.draw_text(Vacas_HD.w / 2, status_y(80), 80, 32, "Siguiente")
    self.contents.font.color = normal_color
    self.contents.draw_text(Vacas_HD.w / 2 + 80, status_y(48), 84, 32, @actor.exp_s, 2)
    self.contents.draw_text(Vacas_HD.w / 2 + 80, status_y(80), 84, 32, @actor.next_rest_exp_s, 2)
    self.contents.font.color = system_color
    self.contents.draw_text(Vacas_HD.w / 2, status_y(160), 96, 32, "Equipo")
    draw_item_name($data_weapons[@actor.weapon_id], Vacas_HD.w / 2 + 16, status_y(208))
    draw_item_name($data_armors[@actor.armor1_id], Vacas_HD.w / 2 + 16, status_y(256))
    draw_item_name($data_armors[@actor.armor2_id], Vacas_HD.w / 2 + 16, status_y(304))
    draw_item_name($data_armors[@actor.armor3_id], Vacas_HD.w / 2 + 16, status_y(352))
    draw_item_name($data_armors[@actor.armor4_id], Vacas_HD.w / 2 + 16, status_y(400))
  end
  def dummy
    self.contents.font.color = system_color
    self.contents.draw_text(Vacas_HD.w / 2, status_y(112), 96, 32, $data_system.words.weapon)
    self.contents.draw_text(Vacas_HD.w / 2, status_y(176), 96, 32, $data_system.words.armor1)
    self.contents.draw_text(Vacas_HD.w / 2, status_y(240), 96, 32, $data_system.words.armor2)
    self.contents.draw_text(Vacas_HD.w / 2, status_y(304), 96, 32, $data_system.words.armor3)
    self.contents.draw_text(Vacas_HD.w / 2, status_y(368), 96, 32, $data_system.words.armor4)
    draw_item_name($data_weapons[@actor.weapon_id], Vacas_HD.w / 2 + 24, status_y(144))
    draw_item_name($data_armors[@actor.armor1_id], Vacas_HD.w / 2 + 24, status_y(208))
    draw_item_name($data_armors[@actor.armor2_id], Vacas_HD.w / 2 + 24, status_y(272))
    draw_item_name($data_armors[@actor.armor3_id], Vacas_HD.w / 2 + 24, status_y(336))
    draw_item_name($data_armors[@actor.armor4_id], Vacas_HD.w / 2 + 24, status_y(400))
  end
end
