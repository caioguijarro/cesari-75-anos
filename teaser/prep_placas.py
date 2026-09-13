"""Prepara os cinco planos do teaser a partir do acervo REAL do Grupo Cesari.

Cada imagem e recortada para 16:9 de modo a (a) eliminar marca d'agua e legenda
queimada do institucional e (b) melhorar o enquadramento. Nada e gerado: o pixel
e o da propria empresa.
"""
from PIL import Image
import glob

A = '/home/user/cesari-75-anos/teaser/acervo/site'
OUT = '/home/user/cesari-75-anos/teaser/placas'

# id -> (nome, topo_cortado, base_cortada, esquerda, direita)  fracoes da altura/largura
PLACAS = [
    ('59332c198fae', '1-aerea-complexo-serra', 0.135, 0.00, 0.00, 0.00),   # tira watermark do topo
    ('d712b1d32ec4', '2-ferrovia-containers',  0.02,  0.02, 0.00, 0.00),
    ('24d82b5e21d4', '3-ceparking-carretas',   0.00,  0.02, 0.00, 0.00),
    ('70fdc55dfc6a', '4-armazem-tambores',     0.00,  0.04, 0.00, 0.00),
    ('5f129b5ddb27', '5-containers-contraluz', 0.00,  0.00, 0.00, 0.00),
]

def prep(mid, nome, ct, cb, cl, cr):
    src = [f for f in glob.glob(f'{A}/*') if mid in f][0]
    im = Image.open(src).convert('RGB')
    w, h = im.size
    im = im.crop((int(w*cl), int(h*ct), w-int(w*cr), h-int(h*cb)))
    w, h = im.size
    # recorte central para 16:9
    alvo = 16/9
    if w/h > alvo:
        nw = int(h*alvo); im = im.crop(((w-nw)//2, 0, (w-nw)//2+nw, h))
    else:
        nh = int(w/alvo); im = im.crop((0, (h-nh)//2, w, (h-nh)//2+nh))
    # sobe para 1920x1080 quando a origem e menor
    if im.width < 1920:
        im = im.resize((1920, 1080), Image.LANCZOS)
    elif im.width > 1920:
        im = im.resize((1920, 1080), Image.LANCZOS)
    im.save(f'{OUT}/{nome}.png')
    print(f'{nome:28} <- {mid}  origem {Image.open(src).size}')

if __name__ == '__main__':
    for p in PLACAS: prep(*p)
