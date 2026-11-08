#==============================================================================
# Vacas_Mente -- Combate frontal XP. Enemigos mentales; veneno nunca mata aqui.
#==============================================================================
module Vacas
  def self.preparar_mente(completo = false)
    for a in $game_party.actors
      # Tambien migra partidas anteriores sin reiniciar sus estadisticas.
      for id in [61, 62, 63, 64]
        a.learn_skill(id)
      end
      a.set_graphic(a.character_name, a.character_hue, 'steven_mente', 0)
      if completo
        a.recover_all
      else
        a.hp = [a.hp, a.maxhp * 3 / 4].max
        a.sp = [a.sp, a.maxsp * 3 / 4].max
      end
    end
  end
end
class Interpreter
  def preparar_mente
    Vacas.preparar_mente(true)
    return true
  end
end
class Scene_Map
  alias vacas_mente_call_battle call_battle
  def call_battle
    # Los encuentros aleatorios se limitan a estos mapas y fuera de patrullas.
    if $game_temp.battle_proc == nil
      unless Vacas.veneno >= 35 and [8, 9, 11].include?($game_map.map_id) and
          !$game_switches[26] and !$game_switches[29] and !$game_switches[30]
        $game_temp.battle_calling = false
        $game_player.make_encounter_count
        return
      end
      $game_temp.battle_can_lose = true
      $game_system.vacas_gastar_encuentro
    end
    Vacas.preparar_mente(false)
    $vacas_tone_antes = $game_screen.tone.clone
    $vacas_fondo_antes = $game_map.battleback_name
    troop = $game_temp.battle_troop_id
    fondo = [2, 8].include?(troop) ? 'piso' : ([3, 6].include?(troop) ? 'tunel' : 'matadero')
    $game_map.battleback_name = 'mente_' + fondo
    $game_screen.start_tone_change(Tone.new(-15, -20, -12, 45), 0)
    vacas_mente_call_battle
  end
end
class Game_Battler
  alias vacas_mente_skill_effect skill_effect
  def skill_effect(user, skill)
    effective = vacas_mente_skill_effect(user, skill)
    if $game_temp.in_battle and self.is_a?(Game_Actor)
      if user.is_a?(Game_Enemy) and effective
        extra = {65=>4, 66=>5, 67=>6, 68=>4, 69=>3, 70=>7}[skill.id]
        Vacas.veneno = [96, Vacas.veneno + extra].min if extra != nil
      elsif skill.id == 61
        self.sp += 18
        for id in [2, 3, 4]
          remove_state(id)
        end
        Vacas.veneno = Vacas.veneno - 6
        effective = true
      end
    end
    return effective
  end
end
class Scene_Battle
  alias vacas_mente_start_phase2 start_phase2
  def start_phase2
    # Solo un pequeño aumento por ronda, sin alcanzar el game over de historia.
    if $game_temp.battle_turn > 0
      burden = $game_party.actors.any? { |a| a.state?(4) } ? 2 : 1
      Vacas.veneno = [96, Vacas.veneno + burden].min
    end
    vacas_mente_start_phase2
  end
  alias vacas_mente_end battle_end
  def battle_end(result)
    $game_variables[18] = result
    Vacas.veneno = result == 0 ? Vacas.veneno - 5 : [96, Vacas.veneno + 8].min
    # No se mantienen muerte ni estados mentales fuera de estas visiones.
    for a in $game_party.actors
      a.recover_all
    end
    $game_player.make_encounter_count
    vacas_mente_end(result)
    if $vacas_tone_antes != nil
      $game_screen.start_tone_change($vacas_tone_antes, 0)
      $game_map.battleback_name = $vacas_fondo_antes
      $vacas_tone_antes = nil
    end
  end
end
class Spriteset_Battle
  alias vacas_mente_ss_initialize initialize
  def initialize
    vacas_mente_ss_initialize
    @vacas_hud = Sprite_Veneno.new
    @vacas_hud.y = 278
  end
  alias vacas_mente_ss_update update
  def update
    vacas_mente_ss_update
    @vacas_hud.update if @vacas_hud != nil
  end
  alias vacas_mente_ss_dispose dispose
  def dispose
    @vacas_hud.dispose if @vacas_hud != nil
    vacas_mente_ss_dispose
  end
end
# Vocabulario del sistema nativo. Conserva su seleccion, turnos y resultados.
module Vacas
  class << self
    alias mente_ajustar_sistema ajustar_sistema
    def ajustar_sistema
      mente_ajustar_sistema
      w = $data_system.words
      w.attack = 'Golpear'
      w.skill = 'Recursos'
      w.guard = 'Resguardarse'
      w.item = 'Objetos'
      w.str = 'Fuerza'
      w.dex = 'Pulso'
      w.agi = 'Reflejos'
      w.int = 'Voluntad'
      w.atk = 'Impacto'
      w.pdef = 'Resistencia'
      w.mdef = 'Templanza'
      w.weapon = 'Herramienta'
      w.armor1 = 'Proteccion'
      w.armor2 = 'Cabeza'
      w.armor3 = 'Ropa'
      w.armor4 = 'Recuerdo'
      $data_system.battle_bgm = RPG::AudioFile.new('036-Dungeon02', 65, 65)
      $data_system.battle_end_me = RPG::AudioFile.new('016-Shock01', 45, 65)
    end
  end
end
class Window_PartyCommand
  alias vacas_mente_party_initialize initialize
  def initialize
    vacas_mente_party_initialize
    @commands = ['Afrontar', 'Apartarse']
    draw_item(0, normal_color)
    draw_item(1, $game_temp.battle_can_escape ? normal_color : disabled_color)
  end
end
class Window_BattleResult
  def refresh
    self.contents.clear
    self.contents.font.size = 21
    self.contents.font.color = normal_color
    self.contents.draw_text(4, 0, 280, 32, 'Sigues aquí. Respira.')
    self.contents.draw_text(4, 32, 280, 32, 'La imagen pierde fuerza.') if self.contents.height >= 64
  end
end
#==============================================================================
# Susto reutilizable: Llamar script: susto(1). Switches 61..67, imagen 98.
#==============================================================================
class Game_Screen
  def vacas_susto(id)
    @pictures[98].show('screamer_' + id.to_s, 0, 0, 0, 100, 100, 255, 0)
    start_shake(9, 9, 24)
    start_flash(Color.new(255, 240, 210, 210), 5)
    $game_system.se_play(RPG::AudioFile.new('092-Attack04', 100, 65))
    @vacas_susto_restante = 24
  end
  alias vacas_susto_update update
  def update
    vacas_susto_update
    if @vacas_susto_restante != nil and @vacas_susto_restante > 0
      @vacas_susto_restante -= 1
      @pictures[98].erase if @vacas_susto_restante == 0
    end
  end
end
class Interpreter
  def susto(id)
    return true unless (1..7).include?(id)
    return true if $game_switches[60 + id]
    $game_switches[60 + id] = true
    $game_screen.vacas_susto(id)
    @wait_count = 24
    return true
  end
end
# Encuentros escasos: como maximo dos por turno, solo con mono y veneno >=35.
class Game_System
  def vacas_cupo_mental
    key = $game_variables[7]
    if @vacas_cupo_turno != key
      @vacas_cupo_turno = key
      @vacas_cupo_usado = 0
    end
    return @vacas_cupo_usado || 0
  end
  def vacas_gastar_encuentro
    @vacas_cupo_usado = vacas_cupo_mental + 1
  end
end
class Game_Map
  alias vacas_mente_encounter_list encounter_list
  def encounter_list
    return vacas_mente_encounter_list unless [8, 9, 11].include?(@map_id)
    return [] unless $game_switches[25] and Vacas.veneno >= 35
    return [] if $game_switches[26] or $game_switches[29] or $game_switches[30]
    return [] if $game_system.vacas_cupo_mental >= 2
    return {8=>[5,7], 9=>[7,4], 11=>[3,6]}[@map_id]
  end
end
class Game_Player
  alias vacas_mente_encounter_count make_encounter_count
  def make_encounter_count
    vacas_mente_encounter_count
    @encounter_count = 45 + rand(65) + rand(65) if [8, 9, 11].include?($game_map.map_id)
  end
end
# Traduce las etiquetas internas de daño del motor.
class Game_Battler
  alias vacas_mente_damage_set damage=
  def damage=(value)
    vacas_mente_damage_set(value == 'Miss' ? 'Fallo' : value)
  end
end
class RPG::Sprite
  alias vacas_mente_damage damage
  def damage(value, critical)
    # RGSS dibuja 'Critical' dentro de su biblioteca. Se conserva el daño
    # multiplicado y se evita esa etiqueta inglesa en la presentación.
    vacas_mente_damage(value, false)
  end
end
