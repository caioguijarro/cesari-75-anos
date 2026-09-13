"""Variante E — a sintese.

C provou que o galgo azul chapado com filete creme le em qualquer fundo.
O que sobrou de feio na C foi a borda reta e nua do corte atras dele.
E) sela essa borda com um filete creme vertical — o "filete padrao" do design
   system — de modo que a linha do corte vire um elemento deliberado da marca.
"""
from PIL import Image, ImageFilter
from build_galgo2 import silhueta, carrega, CREME, AZUL, W, H, FPS, DUR, NF, D

def frames_e(a, b, masc, filete_px=10):
    gw, gh = masc.size
    contorno = masc.filter(ImageFilter.MaxFilter(9))
    galgo = Image.new('RGB', masc.size, AZUL)
    creme = Image.new('RGB', masc.size, CREME)
    barra = Image.new('RGB', (filete_px, H), CREME)
    out = []
    for i in range(NF):
        t = (i+1)/NF
        ponta = int(-gw + t*(W + 2*gw))
        corte = ponta - int(gw*0.55)
        m = Image.new('L', (W, H), 0)
        atras = max(0, min(W, corte))
        if atras: m.paste(255, (0, 0, atras, H))
        f = a.copy(); f.paste(b, (0, 0), m)
        if 0 < corte < W + filete_px:            # filete creme selando o corte
            f.paste(barra, (corte - filete_px//2, 0))
        y = (H-gh)//2
        f.paste(creme, (ponta-gw, y), contorno)
        f.paste(galgo, (ponta-gw, y), masc)
        out.append(f)
    return out

if __name__ == '__main__':
    a, b = carrega(f'{D}/stills/01-porto-santos.png'), carrega(f'{D}/stills/02-armazem-graneis.png')
    fr = frames_e(a, b, silhueta(int(H*0.30)))
    fr[0].save(f'{D}/galgo/travessia-e-galgo-filete.gif', save_all=True,
               append_images=fr[1:]+[fr[-1]]*12, duration=int(1000/FPS), loop=0, optimize=True)
    cs = Image.new('RGB', (W, H//2*4), CREME)
    for k, idx in enumerate([2, 5, 8, 11]):
        cs.paste(fr[idx].resize((W, H//2), Image.LANCZOS), (0, k*(H//2)))
    cs.save(f'{D}/galgo/contatos-e-galgo-filete.png')
    print('e ok')
