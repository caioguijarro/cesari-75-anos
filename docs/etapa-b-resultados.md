# Etapa B — Still frames e teste de travessia

**Executada em 13/09/2026 · aguardando aprovação para seguir ao vídeo**

Arquivos em `teaser/stills/` e `teaser/galgo/`. Script reprodutível em
`teaser/build_galgo.py`, `build_galgo2.py`, `build_galgo3.py`.

---

## 1. Os cinco ambientes

Gerados com **Soul Location** (Higgsfield), 2048 × 1152, 16:9, a partir de um
prompt-base único para garantir consistência entre planos.

| # | Arquivo | Ambiente | Status |
|---|---|---|---|
| 1 | `01-porto-santos.png` | Porto de Santos, amanhecer — navio atracado, grab suspenso, moega com filtro no cais, trilhos do ramal | ✅ 1ª tentativa |
| 2 | `02-armazem-graneis.png` | Armazém de granéis, manhã — montanha ocre, feixes de luz clerestório, pá carregadeira dando escala | ✅ 1ª tentativa |
| 3 | `03-serra-do-mar.png` | Serra do Mar, meio-dia encoberto — carreta inox, névoa entre ridges, viaduto em pilares | ⚠️ refeito |
| 4 | `04-patio-containers.png` | Pátio de containers e isotanks, tarde — grid saturado, reach stacker, fileiras de isotanks | ✅ 1ª tentativa |
| 5 | `05-rio-tapajos.png` | Rio Tapajós, entardecer — comboio de barcaças carregadas de granel, empurrador, mata | ⚠️ refeito |

### Por que 3 e 5 foram refeitos

**Plano 3, 1ª versão:** dominante ciano-esverdeada forte, que destoava dos outros
planos e violava o "cor natural, sem filtro" do design system. Além disso a carreta
aparecia de traseira, e havia artefatos de geração — um vulto humano deformado no
acostamento e uma figura sobre o tanque.
**Correção:** `natural neutral colour balance, no teal tint`, ângulo de três quartos,
`absolutely no people anywhere in frame`.

**Plano 5, 1ª versão:** contraluz total contra o sol, transformando as barcaças em
silhueta ilegível. Metade superior do quadro era céu vazio. Lia como "rio amazônico
genérico", não como operação de granel.
**Correção:** câmera baixa e próxima da água, luz lateral em vez de contraluz, barcaças
carregadas ocupando a faixa central, horizonte alto com pouca faixa de céu.

Ambos os refeitos resolveram os dois problemas.

---

## 2. ⚠️ O teste de travessia derrubou a ideia original

A decupagem aprovada especificava o galgo como **borda do corte** — a silhueta
atravessando e revelando o ambiente seguinte *dentro da própria forma*. O teste mostrou
que **isso não funciona.**

### O que falhou

| Variante | Mecânica | Resultado |
|---|---|---|
| **A** — faixa + galgo preenchido | A silhueta do galgo é preenchida com a imagem seguinte | ❌ A forma vira uma mancha orgânica amorfa. Lê como nuvem ou onda, nunca como galgo |
| **B** — perfil puro | A frente do wipe assume o contorno do galgo linha a linha | ❌ Pior. A 0,5 s lê como retângulos irregulares. Nenhuma leitura de animal |

**A causa:** o galgo do logotipo tem proporção de **4,5 : 1** — extremamente alongado,
com pernas finas. A forma só é reconhecível por **contraste chapado**. Preenchida com
fotografia texturizada, as pernas somem e o corpo se dissolve no fundo.

O design system já sabia disso e estava escrito lá: *"pode sair da marca e virar
elemento isolado **em azul chapado**"*. Eu tentei elevar a especificação e a
especificação estava certa.

### O que funciona

| Variante | Mecânica | Resultado |
|---|---|---|
| **C** — galgo azul chapado | Galgo em `#1C3C7D` sólido com filete creme de contorno; o corte vem colado na traseira | ✅ Lê perfeitamente sobre o porto azul-escuro e sobre o armazém ocre. Resta a borda reta e nua do corte |
| **D** — faixa creme pura | A especificação literal do design system, sem galgo | ✅ Limpa e legível, mas fria. Perde o galgo por completo |
| **E** — C + filete vertical | Galgo chapado, e a borda do corte selada por um filete creme vertical | ✅ **Recomendada** |

### ✅ Recomendação: variante E

O filete creme que sela o corte não é um remendo — é o **"filete padrão"** que o design
system já define como elemento gráfico. A linha do corte deixa de ser um acidente
técnico e vira um elemento deliberado da marca, da mesma família da faixa.

Resultado: o galgo permanece inconfundível em qualquer fundo, o corte fica limpo, e a
gramática continua sendo a do design system — faixa e filete creme atravessando na
velocidade do galgo.

**Consequência para a decupagem:** o texto do item 2 de `storyboard-teaser-b.md` — "o
galgo é a borda do corte" — precisa ser corrigido para "o galgo é a **ponta** do corte,
em azul chapado, e o corte é selado por um filete creme". O conceito narrativo (o galgo
como constante, o mundo como variável) permanece intacto; muda só a mecânica visual.

---

## 3. O que ainda não foi testado

- A **vinheta de abertura** (faixa creme revelando o "75" em Instrument Serif)
- As **cartelas tipográficas** dos Blocos III e IV
- O **galgo sólido em repouso** aos 21 s
- O movimento interno de cada plano (ainda são imagens estáticas)

---

## 4. Custo e ambiente

- **7 gerações de imagem** consumidas (5 + 2 refeitos), modelo `soul_location`
- Saldo no início da etapa: **200 créditos**, plano starter
- O teste de travessia **não consumiu crédito** — é composição local em Pillow a partir
  do PNG da marca, sem IA. O galgo nunca é gerado: é sempre a forma exata do logotipo
- `ffmpeg` segue ausente no ambiente. Os testes saíram como GIF via Pillow, o que
  bastou para validar a travessia. Para o corte final com áudio será preciso instalar

---

## 5. Próximo passo

Aprovada a variante E e os cinco ambientes, seguem em paralelo:

1. Corrigir o item 2 da decupagem para a mecânica E
2. Gerar os 5 clipes de vídeo de 3 s a partir dos stills aprovados
3. Construir vinheta e cartelas em HTML/CSS a 1920 × 1080
4. Instalar `ffmpeg` e montar
