# Formula de dano/estados y seleccion de acciones nativas, 20 semillas por caso.
$game_temp.in_battle=true
a=$game_actors[1];resultados=[]
cases=(1..21).collect { |id| [id,nil] }+(33..37).collect { |id| [id,nil] }
cases += [[21,860],[21,1070],[35,650],[35,990],[36,650],[36,990],[37,650],[37,990]]
for tid,hp in cases
  original=$data_enemies[tid].maxhp
  $data_enemies[tid].maxhp=hp if hp
  turns=[];wins=0
  20.times do |seed|
    srand(seed);a.recover_all;Vacas.veneno=50;$game_troop.setup(tid)
    enemy=$game_troop.enemies[0];turn=0
    while enemy.hp>0 && a.hp>0 && turn<100
      turn+=1;$game_temp.battle_turn=turn
      if a.hp<200 || a.sp<8 || [2,3,4].any? { |id| a.state?(id) }
        a.skill_effect(a,$data_skills[61])
      else
        a.sp-=$data_skills[62].sp_cost
        enemy.skill_effect(a,$data_skills[62])
      end
      if enemy.hp>0
        enemy.make_action
        action=enemy.current_action
        if action.kind==0 && action.basic==0
          a.attack_effect(enemy)
        elsif action.kind==1
          skill=$data_skills[action.skill_id]
          enemy.sp-=skill.sp_cost
          a.skill_effect(enemy,skill)
        end
      end
      a.remove_states_auto;enemy.remove_states_auto
      Graphics.frame_reset if turn%10==0
    end
    wins+=1 if a.hp>0 && enemy.hp==0
    turns.push(turn)
    Graphics.update
  end
  line=[tid,$data_enemies[tid].maxhp,wins,turns.min,turns.sort[10],turns.max]
  resultados.push(line)
  verificar(wins==20 && turns.max<100,'Balance global tropa/HP/victorias/min/med/max '+line.join('/'))
  $data_enemies[tid].maxhp=original
end
File.open('diseno/verificaciones/balance_fase45.tsv','w') do |f|
  f.puts("tropa\thp\tvictorias_de_20\tturnos_min\tturnos_mediana\tturnos_max")
  resultados.each { |r| f.puts(r.join("\t")) }
end
$game_temp.in_battle=false

# Ejecutar los minijuegos reales con entradas perfectas y tambien sin entradas.
# En el recorrido solo se sustituyo su resultado para aislar los contratos.
module Input
  class << self
    alias mini_test_trigger trigger?
    alias mini_test_dir4 dir4
    def dir4
      if $mini_cinta && !$mini_fallar
        p=$mini_cinta.instance_variable_get(:@piezas).find { |row| !row[2] }
        return p[1] if p && (90..160).include?(p[0].x+24)
        return 0
      end
      return mini_test_dir4
    end
    def trigger?(key)
      if $mini_corte && key==Input::C
        return false if $mini_fallar
        x=$mini_corte.instance_variable_get(:@cuchilla).x-120+3
        left=$mini_corte.instance_variable_get(:@zona_x)
        width=$mini_corte.instance_variable_get(:@zona_w)
        return x>=left+3 && x<=left+width-3
      end
      return key==dir4 && dir4!=0 if $mini_cinta
      return mini_test_trigger(key)
    end
  end
end
for fallar in [false,true]
  $mini_fallar=fallar
  $mini_corte=Vacas_Corte.new(6)
  r=$mini_corte.run;$mini_corte.dispose;$mini_corte=nil
  verificar(r==(fallar ? 0 : 6),'Corte: seis rondas '+(fallar ? 'sin entradas' : 'perfectas'))
  for tipo,n in [[Vacas_Cinta,12],[Vacas_Noria,16]]
    $mini_cinta=tipo.new(n)
    r=$mini_cinta.run;$mini_cinta.dispose;$mini_cinta=nil
    verificar(r==(fallar ? 0 : n),'Cinta/noria '+tipo.to_s+' '+(fallar ? 'sin entradas' : 'perfectas'))
  end
end
$mini_fallar=false
