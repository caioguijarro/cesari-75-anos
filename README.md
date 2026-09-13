# Grupo Cesari — 75 anos

Campanha comemorativa dos 75 anos do Grupo Cesari. Este repositório concentra pesquisa,
identidade, roteiro e produção audiovisual do projeto.

**Assinatura da campanha:** *História, valores e legado.*

---

## Estado atual

| Frente | Situação |
|---|---|
| Design system | ✅ Construído — `brand/` |
| Pesquisa sobre a empresa | ✅ Concluída — `docs/pesquisa-grupo-cesari.md` |
| Análise do roteiro | ✅ Concluída — `docs/analise-roteiro.md` |
| Teaser 30 s | 🎬 Variante B · decupagem aprovada · **5 stills e teste de travessia prontos** — `docs/etapa-b-resultados.md` |
| Filme completo (3'30") | ⏸ Aguarda acervo histórico |
| Peças da festa | ⏸ Aguarda data do evento e ano de fundação |

---

## Índice

### `docs/`

- **[`pesquisa-grupo-cesari.md`](docs/pesquisa-grupo-cesari.md)** — levantamento completo
  do site oficial e do canal no YouTube: as 10 empresas, os números de operação, as 20
  bases, a UCC, os programas sociais e o acervo audiovisual existente.
- **[`analise-roteiro.md`](docs/analise-roteiro.md)** — comparação entre a proposta de
  roteiro e o que a empresa efetivamente comunica. Contém o conflito de datas e o
  checklist de pendências.
- **[`plano-teaser-30s.md`](docs/plano-teaser-30s.md)** — plano de produção do teaser:
  direção de arte ancorada na operação real, as duas variantes apresentadas, pipeline
  técnico e pontos de aprovação.
- **[`storyboard-teaser-b.md`](docs/storyboard-teaser-b.md)** — 🎬 decupagem cravada da
  **Variante B "Só o galgo"**, escolhida: 30 s quadro a quadro, os cinco ambientes, o
  desenho de som e os prompts de geração.
- **[`etapa-b-resultados.md`](docs/etapa-b-resultados.md)** — resultados dos still
  frames e do teste de travessia, incluindo a mecânica que falhou e a correção adotada.

### `teaser/`

- **`stills/`** — os cinco ambientes aprovados, 2048 × 1152.
- **`galgo/`** — testes de travessia: GIFs em velocidade real e tiras de contatos.
- **`build_galgo*.py`** — composição da travessia a partir do PNG da marca, sem IA.

### `brand/`

- **[`tokens.md`](brand/tokens.md)** — referência rápida de cores, tipografia, elementos
  gráficos e a especificação oficial de vinheta de vídeo.
- **`Design System 75 Anos Cesari.dc.html`** — canvas completo do design system.
- **`marca/`** — marca comemorativa, selo e galgo em PNG.

### Raiz

- **`Proposta de roteiro.docx`** — roteiro original do filme de 3'30".

---

## ⚠️ Bloqueador aberto: ano de fundação

Quatro fontes discordam:

| Fonte | Afirma |
|---|---|
| Proposta de roteiro | 1952 → 75 anos em **2027** |
| Design system | 1951 — 2026 → 75 anos em **2026** |
| Site oficial (© 2026) | "Com 75 anos de experiência" → **já agora** |
| Briefing do cliente | aniversário "ano que vem" → **2027** |

Isso bloqueia convite impresso, adesivo de frota, backdrop e credenciais — peças que não
se corrigem depois de produzidas. É preciso a fonte primária: contrato social ou data de
abertura do CNPJ mais antigo do grupo.

Detalhes em [`docs/analise-roteiro.md`](docs/analise-roteiro.md).

---

## Próximos passos

1. Resolver o ano de fundação
2. Aprovar a decupagem da Variante B (`docs/storyboard-teaser-b.md`)
3. ~~Gerar os 5 still frames e o teste de travessia~~ ✅ feito
4. Gerar os 5 clipes de vídeo, a vinheta e as cartelas; instalar `ffmpeg` e montar
5. Em paralelo e com urgência: iniciar o garimpo do acervo histórico 1952–1994 e a
   gravação de depoimentos de colaboradores antigos
