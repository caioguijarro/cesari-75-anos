# Etapa C — Teaser montado

**13/09/2026 · `teaser/teaser-cesari-75.mp4` · 1920×1080 · 24 fps · 30,00 s · sem áudio**

---

## 1. O que é real e o que é gerado

| Elemento | Origem |
|---|---|
| Os cinco planos | **Fotografia real do Grupo Cesari**, publicada no próprio site |
| Movimento de câmera | Ken Burns local (Pillow + ffmpeg) — **não é IA** |
| Galgo, marca, selo | PNG oficial do design system — **nunca gerado** |
| Tipografia | Archivo e Instrument Serif, as fontes do design system |
| Paleta | Tokens exatos do design system |

**Nenhum pixel de conteúdo foi inventado.** A peça inteira é imagem da própria
empresa mais grafismo da própria marca.

---

## 2. ⚠️ Por que a IA saiu do movimento

O plano era animar as fotos com image-to-video (FLUX 3 Video). Foram gerados dois
clipes de teste, com prompts explicitamente restritivos ("preserve the source
photograph exactly", "no added objects", "no new people").

**Resultado misto:**

- **Ceparking** — preservou bem. A placa da empresa continua legível, a frota
  permanece, o dolly lateral é suave. Clipe guardado em `teaser/clipes/`.
- **Armazém de tambores** — **alucinou**. Ao longo dos 5 s a câmera desliza muito
  além do pedido, os tambores se reorganizam e o operador muda de posição e de
  pose. A cena deixa de ser a cena real da Cesari.

O padrão: planos amplos e estáticos sobrevivem; planos com muitos objetos
próximos e pessoas são reconstruídos.

**Decisão:** como o pedido é conteúdo fiel, o movimento de câmera passou a ser
feito localmente. Ken Burns sobre a foto real tem fidelidade de 100% por
construção — é a fotografia da empresa, com a câmera se movendo sobre ela. A IA
não é necessária para isso, e aqui era ativamente prejudicial.

O clipe do Ceparking fica disponível caso se queira movimento interno de cena
naquele plano específico.

---

## 3. Os cinco planos

| # | Plano | Movimento | Origem |
|---|---|---|---|
| 1 | Aérea do complexo no vale da Serra do Mar | push-in lento | frame do institucional |
| 2 | Ramal ferroviário, vagões e reach stacker | pan à esquerda | site |
| 3 | Pátio Ceparking, frota de carretas-tanque | pan à direita | site |
| 4 | Armazém de tambores, operador e empilhadeira | push-in lento | site |
| 5 | Containers em contraluz de pôr do sol | push-in lento | foto 4096 px |

Cada placa foi recortada para 16:9 eliminando a marca d'água
"#INSTITUCIONALCESARI", o galgo de canto e as legendas queimadas em inglês.

---

## 4. Correções feitas durante a montagem

**A cartela dos 22 s não lia.** O galgo em azul Cesari `#1C3C7D` sobre o azul
profundo `#112A57` praticamente desaparecia, e a frase estava sobreposta a ele.
Corrigido com filete creme de contorno — o mesmo recurso adotado nas travessias —
e separando galgo (terço superior) e texto (terço inferior).

**O galgo estava cortado pelo lado errado.** Estava saindo pela margem direita,
cortando o focinho. O design system diz "cortado pela margem no máximo até o
quadril" — ou seja, corta-se a traseira, nunca a cabeça. Invertido: agora sai
pela margem esquerda, com a cabeça inteira em quadro.

---

## 5. ⚠️ O que falta

**Áudio.** A peça está muda. Pela decupagem, o som não é acompanhamento: as cinco
travessias são a percussão, feita de som real de operação (grab, moega, freio a
ar, container assentando, motor fluvial), e o Bloco III existe porque essa batida
para. Sem isso o teaser entrega talvez 60% do efeito.

Não há biblioteca de som licenciada neste ambiente. Dois caminhos:

1. Som de operação gerado por IA — coerente com "IA só no que for necessário",
   já que não altera nenhuma imagem
2. Biblioteca licenciada, escolhida por você

**Conferir direitos.** As imagens são do site público da Cesari. Sendo a peça
para a própria empresa, o uso é natural — mas vale a confirmação formal de que o
grupo detém os direitos das fotos e dos frames do institucional, sobretudo se
houver produtora terceirizada envolvida.

**Pendências herdadas:** ano de fundação (1951 × 1952) e logo em vetor.

---

## 6. Ambiente

`ffmpeg` **resolvido** — 7.0.2 via `imageio-ffmpeg`, sem depender de apt. O
bloqueador registrado desde o primeiro plano está encerrado.

`yt-dlp` instalado, mas o YouTube recusa download de vídeo a partir deste
ambiente (403 / verificação de bot); só entrega storyboards de 160 × 90. As 30
capas do canal foram baixadas em 1280 × 720, mas são artes com overlay de título,
não frames limpos. O material real aproveitável veio todo do site.
