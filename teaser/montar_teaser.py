"""Montagem do teaser de 30 s — Grupo Cesari 75 anos, variante B "So o galgo".

Fidelidade: os cinco planos sao FOTOGRAFIA REAL do Grupo Cesari, retirada do
proprio site. O movimento de camera e feito aqui (Ken Burns), nao por IA, para
que nenhum pixel do conteudo seja inventado. O galgo e a marca vem do PNG
oficial. Tipografia em Archivo e Instrument Serif, as fontes do design system.

Saida: 1920x1080, 24 fps, 30,0 s exatos.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import subprocess, sys, os

W, H, FPS = 1920, 1080, 24
DUR = 30.0
NF = int(DUR * FPS)                     # 720 frames

CREME       = (253, 251, 239)
CREME_SOMBRA= (242, 236, 216)
AZUL        = (28, 60, 125)
AZUL_FUNDO  = (17, 42, 87)

D = os.path.dirname(os.path.abspath(__file__))
FT = f'{D}/fontes'

PLANOS = [
    ('1-aerea-complexo-serra',  'in',    (0.50, 0.55)),
    ('2-ferrovia-containers',   'left',  (0.50, 0.50)),
    ('3-ceparking-carretas',    'right', (0.50, 0.50)),
    ('4-armazem-tambores',      'in',    (0.55, 0.50)),
    ('5-containers-contraluz',  'in',    (0.50, 0.50)),
]

# ---------------------------------------------------------------- recursos
def carregar_placas():
    out = []
    for nome, _, _ in PLANOS:
        im = Image.open(f'{D}/placas/{nome}.png').convert('RGB')
        if im.size != (W, H): im = im.resize((W, H), Image.LANCZOS)
        out.append(im)
    return out

def silhueta_galgo(altura):
    g = Image.open(f'{D}/../brand/marca/galgo.png').convert('RGB')
    g = g.resize((int(g.width * altura / g.height), altura), Image.LANCZOS)
    m = Image.new('L', g.size, 0)
    px, mp = g.load(), m.load()
    for y in range(g.height):
        for x in range(g.width):
            r, v, b = px[x, y]
            mp[x, y] = 255 if abs(r-253)+abs(v-251)+abs(b-239) > 120 else 0
    return m

def fonte(nome, tam):
    return ImageFont.truetype(f'{FT}/{nome}', tam)

F_SERIF   = lambda t: fonte('InstrumentSerif-0.ttf', t)
F_ARCHIVO = lambda t: fonte('Archivo-1.ttf', t)      # peso medio/600

# ---------------------------------------------------------------- utilidades
def ken_burns(im, t, modo, foco):
    """t em [0,1]. Movimento de camera sobre a foto real — nada e inventado."""
    z0, z1 = 1.0, 1.055
    z = z0 + (z1 - z0) * t
    if modo == 'left':  z, dx, dy = 1.055, -0.022 + 0.044*t, 0.0
    elif modo == 'right': z, dx, dy = 1.055, 0.022 - 0.044*t, 0.0
    else: dx, dy = 0.0, 0.0
    nw, nh = int(W*z), int(H*z)
    big = im.resize((nw, nh), Image.LANCZOS)
    cx = (nw - W) * (foco[0] + dx)
    cy = (nh - H) * (foco[1] + dy)
    cx = max(0, min(nw-W, int(cx))); cy = max(0, min(nh-H, int(cy)))
    return big.crop((cx, cy, cx+W, cy+H))

def linhas_de_rota(base):
    """Textura do design system: filetes horizontais paralelos a 1 px."""
    d = ImageDraw.Draw(base, 'RGBA')
    for y in range(0, H, 14):
        d.line([(0, y), (W, y)], fill=(253, 251, 239, 12), width=1)
    return base

def fade_preto(im, k):
    if k >= 1.0: return im
    return ImageEnhance.Brightness(im).enhance(max(0.0, k))

# ---------------------------------------------------------------- blocos
def bloco_vinheta(f, galgo):
    """0,0 -> 5,0 s. Faixa creme atravessa e revela o 75."""
    im = Image.new('RGB', (W, H), AZUL_FUNDO)
    linhas_de_rota(im)
    t = f / FPS
    if t >= 2.4:                                    # o 75 ja revelado
        d = ImageDraw.Draw(im)
        fnt = F_SERIF(int(H*0.55))
        d.text((int(W*0.085), int(H*0.50)), '75', font=fnt, fill=CREME, anchor='lm')
        if t > 4.55:                                 # escurece para o corte
            im = fade_preto(im, max(0.0, 1 - (t-4.55)/0.45))
    elif t >= 1.2:                                   # a faixa atravessando
        p = (t - 1.2) / 1.2
        fw = int(W*0.26)
        pos = int(-fw + p*(W + 2*fw))
        d = ImageDraw.Draw(im)
        if pos - fw > 0:                             # o 75 vai surgindo atras
            rev = Image.new('RGB', (W, H), AZUL_FUNDO); linhas_de_rota(rev)
            dr = ImageDraw.Draw(rev)
            dr.text((int(W*0.085), int(H*0.50)), '75', font=F_SERIF(int(H*0.55)),
                    fill=CREME, anchor='lm')
            im.paste(rev.crop((0, 0, min(W, pos-fw), H)), (0, 0))
        x0, x1 = max(0, pos-fw), max(0, min(W, pos))
        if x1 > x0: im.paste(Image.new('RGB', (x1-x0, H), CREME), (x0, 0))
    return im

def travessia(a, b, p, galgo, filete=12):
    """Variante E: galgo azul chapado com contorno creme puxa o corte."""
    gw, gh = galgo.size
    contorno = galgo.filter(ImageFilter.MaxFilter(9))
    ponta = int(-gw + p*(W + 2*gw))
    corte = ponta - int(gw*0.55)
    m = Image.new('L', (W, H), 0)
    atras = max(0, min(W, corte))
    if atras: m.paste(255, (0, 0, atras, H))
    f = a.copy(); f.paste(b, (0, 0), m)
    if 0 < corte < W + filete:
        f.paste(Image.new('RGB', (filete, H), CREME), (corte - filete//2, 0))
    y = (H-gh)//2
    f.paste(Image.new('RGB', galgo.size, CREME), (ponta-gw, y), contorno)
    f.paste(Image.new('RGB', galgo.size, AZUL),  (ponta-gw, y), galgo)
    return f

def bloco_cartela(f0, placas, galgo_g):
    """20,0 -> 25,0 s. O batimento que nao vem."""
    t = f0 / FPS                                   # 0..5 dentro do bloco
    base = ken_burns(placas[4], 1.0, PLANOS[4][1], PLANOS[4][2])
    if t < 1.0:                                    # dessatura e escurece
        k = t / 1.0
        im = ImageEnhance.Color(base).enhance(1 - 0.95*k)
        im = ImageEnhance.Brightness(im).enhance(1 - 0.78*k)
        azul = Image.new('RGB', (W, H), AZUL_FUNDO)
        im = Image.blend(im, azul, 0.55*k)
    else:
        im = Image.new('RGB', (W, H), AZUL_FUNDO); linhas_de_rota(im)
    if t >= 1.0:                                   # o galgo resolve, imovel
        k = min(1.0, (t-1.0)/0.8)
        gw, gh = galgo_g.size
        # cortado pela margem ESQUERDA, no quadril — a cabeca fica inteira na tela,
        # como manda o design system ("cortado pela margem no maximo ate o quadril")
        x = -int(gw*0.14)
        y = int(H*0.20)                            # terco superior, longe do texto
        contorno = galgo_g.filter(ImageFilter.MaxFilter(11))
        # filete creme de contorno: sem ele o azul chapado nao le sobre o azul profundo
        im.paste(Image.new('RGB', (gw, gh), CREME), (x, y),
                 contorno.point(lambda v: int(v*k)))
        im.paste(Image.new('RGB', (gw, gh), AZUL), (x, y),
                 galgo_g.point(lambda v: int(v*k)))
    if t >= 2.0:                                   # a frase, no terco inferior
        k = min(1.0, (t-2.0)/0.35)
        txt = Image.new('L', (W, H), 0)
        dt = ImageDraw.Draw(txt)
        dt.text((int(W*0.085), int(H*0.72)), 'Há coisas que o tempo não muda.',
                font=F_ARCHIVO(int(H*0.062)), fill=int(255*k), anchor='lm')
        im.paste(Image.new('RGB', (W, H), CREME), (0, 0), txt)
    return im

def bloco_marca(f0, marca):
    im = Image.new('RGB', (W, H), CREME)
    mw = int(W*0.46)
    m = marca.resize((mw, int(marca.height*mw/marca.width)), Image.LANCZOS)
    im.paste(m, ((W-m.width)//2, (H-m.height)//2), m if m.mode=='RGBA' else None)
    t = f0 / FPS
    if t < 0.18: im = fade_preto(im, t/0.18)
    return im

# ---------------------------------------------------------------- principal
def main():
    placas = carregar_placas()
    galgo   = silhueta_galgo(int(H*0.30))          # travessias
    galgo_g = silhueta_galgo(int(H*0.26))          # o galgo em repouso
    marca   = Image.open(f'{D}/../brand/marca/marca-75-tagline.png').convert('RGBA')

    ff = ['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}',
          '-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','slow',
          '-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',
          f'{D}/teaser-cesari-75.mp4']
    p = subprocess.Popen(ff, stdin=subprocess.PIPE,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    F_VIN, F_PL, F_CART = 120, 72, 120             # vinheta, cada plano, cartela
    TRAV = 12                                      # 0,5 s de travessia

    for f in range(NF):
        if f < F_VIN:
            im = bloco_vinheta(f, galgo)
        elif f < F_VIN + 5*F_PL:                   # 120..479
            k = f - F_VIN
            i, loc = k // F_PL, k % F_PL
            t = loc / F_PL
            cur = ken_burns(placas[i], t, PLANOS[i][1], PLANOS[i][2])
            if loc < TRAV:                         # travessia entrando neste plano
                ant = (ken_burns(placas[i-1], 1.0, PLANOS[i-1][1], PLANOS[i-1][2])
                       if i > 0 else Image.new('RGB', (W, H), AZUL_FUNDO))
                im = travessia(ant, cur, (loc+1)/TRAV, galgo)
            else:
                im = cur
        elif f < F_VIN + 5*F_PL + F_CART:          # 480..599
            im = bloco_cartela(f - (F_VIN + 5*F_PL), placas, galgo_g)
        else:                                      # 600..719
            im = bloco_marca(f - (F_VIN + 5*F_PL + F_CART), marca)
        p.stdin.write(im.tobytes())
        if f % 120 == 0: print(f'  frame {f}/{NF}', flush=True)

    p.stdin.close(); p.wait()
    print('pronto:', f'{D}/teaser-cesari-75.mp4')

if __name__ == '__main__':
    main()
