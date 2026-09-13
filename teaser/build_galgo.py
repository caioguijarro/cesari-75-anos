"""Teste de travessia do galgo — o galgo como borda do corte.

Gera dois GIFs comparando as duas gramáticas possíveis de transição:
  A) faixa + galgo na ponta — frente reta, o galgo puxa a cortina
  B) perfil puro — a frente do wipe tem o contorno do galgo linha a linha
"""
from PIL import Image
import os

CREME = (253, 251, 239)
AZUL = (28, 60, 125)          # --cesari-azul #1C3C7D
W, H = 1280, 720              # proxy de 1920x1080 para o teste
FPS = 24
DUR = 0.5                     # travessia de 0,5 s conforme a decupagem
NFRAMES = int(FPS * DUR)

def silhueta(altura_alvo):
    """Extrai a silhueta do galgo do PNG (fundo creme opaco, sem alpha util)."""
    g = Image.open('/home/user/cesari-75-anos/brand/marca/galgo.png').convert('RGB')
    esc = altura_alvo / g.height
    g = g.resize((int(g.width * esc), altura_alvo), Image.LANCZOS)
    # mascara: 255 onde o pixel se afasta do creme
    masc = Image.new('L', g.size, 0)
    px, mp = g.load(), masc.load()
    for y in range(g.height):
        for x in range(g.width):
            r, vd, b = px[x, y]
            d = abs(r - CREME[0]) + abs(vd - CREME[1]) + abs(b - CREME[2])
            mp[x, y] = 255 if d > 120 else 0
    return masc

def carrega(p):
    im = Image.open(p).convert('RGB')
    esc = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * esc), int(im.height * esc)), Image.LANCZOS)
    l = (im.width - W) // 2
    t = (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))

def frames_faixa(a, b, masc):
    """A) A frente do wipe e uma faixa vertical reta; o galgo vai na ponta, solido."""
    gw, gh = masc.size
    out = []
    for i in range(NFRAMES):
        t = (i + 1) / NFRAMES
        # a ponta do galgo percorre de -gw ate W+gw
        ponta = int(-gw + t * (W + 2 * gw))
        m = Image.new('L', (W, H), 0)
        # tudo atras da ponta ja foi revelado
        atras = max(0, min(W, ponta - gw))
        if atras > 0:
            m.paste(255, (0, 0, atras, H))
        # o galgo solido na ponta
        m.paste(masc, (ponta - gw, (H - gh) // 2), masc)
        f = a.copy()
        f.paste(b, (0, 0), m)
        out.append(f)
    return out

def frames_perfil(a, b, masc):
    """B) A frente do wipe tem o contorno do galgo, linha a linha."""
    gw, gh = masc.size
    mp = masc.load()
    topo = (H - gh) // 2
    # para cada linha do galgo, o x mais a direita onde ha silhueta
    borda = []
    for y in range(gh):
        d = -1
        for x in range(gw - 1, -1, -1):
            if mp[x, y]:
                d = x
                break
        borda.append(d)
    corpo = int(gw * 0.45)     # linha base onde o galgo nao alcanca
    out = []
    for i in range(NFRAMES):
        t = (i + 1) / NFRAMES
        pos = int(-gw + t * (W + 2 * gw))
        m = Image.new('L', (W, H), 0)
        px = m.load()
        for y in range(H):
            gy = y - topo
            d = borda[gy] if (0 <= gy < gh and borda[gy] >= 0) else corpo
            lim = max(0, min(W, pos + d))
            for x in range(lim):
                px[x, y] = 255
        f = a.copy()
        f.paste(b, (0, 0), m)
        out.append(f)
    return out

if __name__ == '__main__':
    d = '/home/user/cesari-75-anos/teaser'
    a = carrega(f'{d}/stills/01-porto-santos.png')
    b = carrega(f'{d}/stills/02-armazem-graneis.png')
    masc = silhueta(int(H * 0.42))     # galgo ocupa 42% da altura da tela
    ms = int(1000 / FPS)

    for nome, fn in (('a-faixa', frames_faixa), ('b-perfil', frames_perfil)):
        fr = fn(a, b, masc)
        # segura o ultimo frame para o loop respirar
        fr[0].save(f'{d}/galgo/travessia-{nome}.gif', save_all=True,
                   append_images=fr[1:] + [fr[-1]] * 12, duration=ms, loop=0, optimize=True)
        # tira de contatos: 4 momentos da travessia
        cs = Image.new('RGB', (W, H // 2 * 4), CREME)
        for k, idx in enumerate([2, 5, 8, 11]):
            cs.paste(fr[idx].resize((W, H // 2), Image.LANCZOS), (0, k * (H // 2)))
        cs.save(f'{d}/galgo/contatos-{nome}.png')
        print(nome, 'ok', len(fr), 'frames')
