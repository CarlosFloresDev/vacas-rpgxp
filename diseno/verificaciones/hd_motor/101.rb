# Vacas: intro animada de Feka Studios. RGSS1 / Ruby 1.8.
# Seccion Vacas_IntroFeka, despues de Vacas_Interfaz y antes de Main.
# Solo la lanza Main al arrancar el programa; despues cede el paso a la
# cadena de arranque de siempre (aviso de contenido -> titulo).
# Graficos: Graphics/Pictures/feka_*.png (herramientas/arte_intro_feka.py).
class Scene_FekaIntro
  FONDO   = Color.new(8, 7, 11)        # #08070b
  NEON    = [255, 61, 87]              # #ff3d57
  LOGO_X  = 136                        # logo 368x146 centrado en 640
  LOGO_Y  = 150
  GOTA_X  = LOGO_X + 107               # centro de la gota dentro del logo
  GOTA_Y  = LOGO_Y + 85
  SUELO_Y = 322                        # donde salpica (eje de la linea)
  # Fotogramas a 40 fps: 250 = 6,25 s.
  T_LOGO  = 20                         # enciende el neon
  T_FIJO  = 64                         # logo estable
  T_CAE   = 100                        # la gota se suelta
  T_SALPI = 126                        # toca el suelo
  T_TEXTO = 150                        # aparece PRESENTA
  T_FUERA = 222                        # fundido a negro
  T_FIN   = 250
  # Opacidad del tubo de neon al encender (un valor cada 2 fotogramas).
  PARPADEO = [170, 40, 215, 0, 0, 0, 255, 95, 255, 255, 255, 130, 255, 255,
              70, 255, 255, 255, 190, 255, 255, 255]
  SE_NEON   = ['Audio/SE/se_interruptor_luz', 80, 100]
  SE_SALPI  = ['Audio/SE/se_chapoteo_1', 70, 110]

  def self.siguiente
    defined?(Scene_Aviso) ? Scene_Aviso.new : Scene_Title.new
  end

  def main
    begin
      crear
    rescue StandardError, Errno::ENOENT
      # Falta algun grafico: la intro se omite, el juego arranca igual.
      liberar
      $scene = Scene_FekaIntro.siguiente
      return
    end
    @t = 0
    @salida = nil
    @intensidad = Vacas_Config.get(:intensidad)
    Graphics.transition(2)
    loop do
      Graphics.update
      Input.update
      update
      break if $scene != self
    end
    Graphics.freeze
    liberar
  end

  def sprite(nombre, x, y, z)
    s = Sprite.new
    @sprites.push(s)
    @propios.push(s) unless nombre
    s.bitmap = nombre ? RPG::Cache.picture(nombre) : Bitmap.new(640, 480)
    s.x = x; s.y = y; s.z = z; s.opacity = 0
    s
  end

  def crear
    @sprites = []; @propios = []; @gotas = []
    @fondo = sprite(nil, 0, 0, 0)
    @fondo.bitmap.fill_rect(0, 0, 640, 480, FONDO); @fondo.opacity = 255
    @halo = sprite('feka_halo', 64, 95, 1); @halo.blend_type = 1
    @fantasma = sprite('feka_logo', LOGO_X, LOGO_Y, 2)
    @fantasma.blend_type = 1
    @fantasma.color = Color.new(NEON[0], NEON[1], NEON[2], 255)
    @logo = sprite('feka_logo', LOGO_X, LOGO_Y, 3)
    @franjas = [sprite('feka_logo', LOGO_X, LOGO_Y, 4),
                sprite('feka_logo', LOGO_X, LOGO_Y, 4)]
    @linea = sprite('feka_linea', LOGO_X, SUELO_Y - 6, 3)
    @texto = sprite('feka_presenta', 0, 344, 3)
    @texto.x = (640 - @texto.bitmap.width) / 2
    @destello = sprite('feka_halo', GOTA_X, SUELO_Y, 4)
    @destello.blend_type = 1; @destello.ox = 256; @destello.oy = 128
    @destello.zoom_x = 0.3; @destello.zoom_y = 0.3
    @gota = sprite('feka_gota', GOTA_X, GOTA_Y, 5)
    @gota.ox = 8; @gota.oy = 8
    9.times do |i|
      g = sprite('feka_gota', GOTA_X, SUELO_Y, 5)
      g.ox = 8; g.oy = 8
      g.color = Color.new(NEON[0], NEON[1], NEON[2], 255)
      z = 0.28 + rand(30) / 100.0
      g.zoom_x = z; g.zoom_y = z
      vx = (i - 4) * 0.75 + (rand(9) - 4) / 10.0
      @gotas.push([g, GOTA_X.to_f, SUELO_Y.to_f, vx, -2.2 - rand(30) / 10.0])
    end
    @velo = sprite(nil, 0, 0, 20)
    @velo.bitmap.fill_rect(0, 0, 640, 480, Color.new(0, 0, 0)); @velo.opacity = 255
  end

  def liberar
    return unless @sprites
    @sprites.each do |s|
      next if s.disposed?
      s.bitmap.dispose if @propios.include?(s) && s.bitmap && !s.bitmap.disposed?
      s.dispose
    end
    @sprites = nil
  end

  def se(datos)
    Audio.se_play(datos[0], datos[1], datos[2])   # pasa por los ajustes de volumen
  end

  def rampa(desde, hasta)
    return 0.0 if @t <= desde
    return 1.0 if @t >= hasta
    (@t - desde).to_f / (hasta - desde)
  end

  def update
    @t += 1
    if @salida.nil? && (Input.trigger?(Input::C) || Input.trigger?(Input::B))
      @salida = [@t, 10]                      # saltar: fundido rapido
      Audio.se_stop
    end
    @salida = [@t, T_FIN - T_FUERA] if @salida.nil? && @t >= T_FUERA
    se(SE_NEON) if @t == T_LOGO && @salida.nil?
    se(SE_SALPI) if @t == T_SALPI && @salida.nil?
    update_logo
    update_gota
    update_salpicadura
    # Velo negro: entrada, salida y salto.
    if @salida
      k = (@t - @salida[0]).to_f / @salida[1]
      @velo.opacity = [255 * k, 255].min
      $scene = Scene_FekaIntro.siguiente if k >= 1.0
    else
      @velo.opacity = 255 * (1.0 - rampa(0, 18))
    end
  end

  def update_logo
    f = @t - T_LOGO
    if f < 0
      nivel = 0
    elsif f < PARPADEO.size * 2 && @intensidad > 0
      crudo = PARPADEO[f / 2]
      nivel = 255 - (255 - crudo) * [@intensidad + 30, 100].min / 100
      nivel = nivel * [f / 10.0, 1.0].min if @intensidad < 30
    else
      nivel = 255 * [f / 24.0, 1.0].min
    end
    @logo.opacity = nivel
    # Aberracion roja: fuerte al encender, residual despues.
    vivo = (@t >= T_LOGO && @t < T_FIJO && @intensidad > 0)
    @fantasma.x = LOGO_X + (vivo ? (rand(2) == 0 ? -3 : 3) : 1)
    @fantasma.y = LOGO_Y + (vivo ? 0 : 1)
    @fantasma.opacity = vivo ? nivel * 0.55 : nivel * 0.22
    # Franjas desplazadas (glitch) solo mientras enciende.
    @franjas.each do |s|
      if vivo && rand(5) == 0
        alto = 6 + rand(22)
        y = rand(146 - alto)
        s.src_rect.set(0, y, 368, alto)
        s.y = LOGO_Y + y
        s.x = LOGO_X + (rand(2) == 0 ? -1 : 1) * (4 + rand(9))
        s.opacity = [nivel, 200].min
      elsif !vivo || rand(3) == 0
        s.opacity = 0
      end
    end
    # Halo: respira con el tubo y da un golpe con la salpicadura.
    base = nivel * 0.42 + Math.sin(@t / 14.0) * 14
    golpe = @t >= T_SALPI ? 110 * (1.0 - rampa(T_SALPI, T_SALPI + 34)) : 0
    @halo.opacity = [[base + golpe, 0].max, 255].min
  end

  def update_gota
    if @t < T_CAE
      @gota.opacity = @logo.opacity
      # La gota engorda y se estira antes de soltarse.
      k = rampa(T_FIJO + 10, T_CAE)
      @gota.zoom_y = 1.0 + 0.22 * k
      @gota.y = GOTA_Y + (2 * k).to_i
      @gota.color = Color.new(NEON[0], NEON[1], NEON[2], 120 * k)
    elsif @t < T_SALPI
      k = rampa(T_CAE, T_SALPI)
      @gota.opacity = 255
      @gota.y = GOTA_Y + 2 + ((SUELO_Y - GOTA_Y - 2) * k * k).to_i
      @gota.zoom_y = 1.22 + 0.7 * k
      @gota.zoom_x = 1.0 - 0.2 * k
      @gota.color = Color.new(NEON[0], NEON[1], NEON[2], 120 + 135 * k)
    else
      @gota.opacity = 0
    end
  end

  def update_salpicadura
    return if @t < T_SALPI
    vida = @t - T_SALPI
    @gotas.each do |d|
      g = d[0]
      d[1] += d[3]; d[2] += d[4]; d[4] += 0.32
      g.x = d[1].to_i; g.y = d[2].to_i
      g.opacity = d[2] > SUELO_Y + 4 ? 0 : [255 - vida * 9, 0].max
    end
    @destello.opacity = [230 - vida * 11, 0].max
    @destello.zoom_x = 0.3 + vida * 0.02
    # La linea de neon nace en el punto de impacto y corre a los dos lados.
    k = rampa(T_SALPI, T_SALPI + 30)
    k = 1.0 - (1.0 - k) * (1.0 - k)
    izq = (107 * k).to_i; der = (261 * k).to_i
    @linea.src_rect.set(107 - izq, 0, izq + der, 13)
    @linea.x = LOGO_X + 107 - izq
    @linea.opacity = [vida * 40, 255].min
    # PRESENTA sube un poco mientras aparece.
    k = rampa(T_TEXTO, T_TEXTO + 34)
    @texto.opacity = 205 * k
    @texto.y = 344 - (4 * k).to_i
  end
end
