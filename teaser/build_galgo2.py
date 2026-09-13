"""Correcao do teste de travessia.

O teste 1 mostrou que preencher a silhueta do galgo com a imagem destroi a forma:
o galgo e muito alongado (4,5:1) e as pernas finas somem sem contraste chapado.
O design system ja dizia a resposta: o galgo isolado e SEMPRE azul chapado.

C) galgo azul chapado com filete creme puxa o corte
D) faixa creme pura atravessa e revela (spec literal do design system)
"""
from PIL import Image, ImageFilter

CREME = (253, 251, 239)
AZUL = (28, 60, 125)
W, H = 1280, 720
FPS, DUR = 24, 0.5
NF = int(FPS * DUR)
D = '/home/user/cesari-75-anos/teaser'

def silhueta(alt):
    g = Image.open('/home/user/cesari-75-anos/brand/marca/galgo.png').convert('RGB')
    g = g.resize((int(g.width * alt / g.height), alt), Image.LANCZOS)
    m = Image.new('L', g.size, 0)
    px, mp = g.load(), m.load()
    for y in range(g.height):
        for x in range(g.width):
            r, v, b = px[x, y]
            mp[x, y] = 255 if abs(r-CREME[0])+abs(v-CREME[1])+abs(b-CREME[2]) > 120 else 0
    return m

def carrega(p):
    im = Image.open(p).convert('RGB')
    e = max(W/im.width, H/im.height)
    im = im.resize((int(im.width*e), int(im.height*e)), Image.LANCZOS)
    l, t = (im.width-W)//2, (im.height-H)//2
    return im.crop((l, t, l+W, t+H))

def frames_c(a, b, masc):
    """Galgo AZUL CHAPADO com filete creme; o corte vem colado na sua traseira."""
    gw, gh = masc.size
    filete = masc.filter(ImageFilter.MaxFilter(9))          # contorno creme de ~4px
    galgo = Image.new('RGB', masc.size, AZUL)
    cor_filete = Image.new('RGB', masc.size, CREME)
    out = []
    for i in range(NF):
        t = (i+1)/NF
        ponta = int(-gw + t*(W + 2*gw))
        m = Image.new('L', (W, H), 0)
        atras = max(0, min(W, ponta - int(gw*0.55)))        # corte sob o corpo do galgo
        if atras: m.paste(255, (0, 0, atras, H))
        f = a.copy(); f.paste(b, (0, 0), m)
        y = (H-gh)//2
        f.paste(cor_filete, (ponta-gw, y), filete)          # filete creme por baixo
        f.paste(galgo, (ponta-gw, y), masc)                 # galgo azul chapado
        out.append(f)
    return out

def frames_d(a, b):
    """Faixa creme atravessa e revela — a especificacao literal do design system."""
    fw = int(W*0.22)
    out = []
    for i in range(NF):
        t = (i+1)/NF
        pos = int(-fw + t*(W + 2*fw))
        m = Image.new('L', (W, H), 0)
        atras = max(0, min(W, pos-fw))
        if atras: m.paste(255, (0, 0, atras, H))
        f = a.copy(); f.paste(b, (0, 0), m)
        x0, x1 = max(0, pos-fw), max(0, min(W, pos))
        if x1 > x0: f.paste(Image.new('RGB', (x1-x0, H), CREME), (x0, 0))
        out.append(f)
    return out

if __name__ == '__main__':
    a, b = carrega(f'{D}/stills/01-porto-santos.png'), carrega(f'{D}/stills/02-armazem-graneis.png')
    masc = silhueta(int(H*0.30))
    ms = int(1000/FPS)
    for nome, fr in (('c-galgo-chapado', frames_c(a, b, masc)), ('d-faixa-creme', frames_d(a, b))):
        fr[0].save(f'{D}/galgo/travessia-{nome}.gif', save_all=True,
                   append_images=fr[1:]+[fr[-1]]*12, duration=ms, loop=0, optimize=True)
        cs = Image.new('RGB', (W, H//2*4), CREME)
        for k, idx in enumerate([2, 5, 8, 11]):
            cs.paste(fr[idx].resize((W, H//2), Image.LANCZOS), (0, k*(H//2)))
        cs.save(f'{D}/galgo/contatos-{nome}.png')
        print(nome, 'ok')
