# Questionário escrito — modelo do `questionarios/<ID>.md`

O terceiro artefato: os 20 itens por extenso, com gabarito e o motivo de cada alternativa
errada. É o que a coordenação compara com o que a plataforma devolveu — ou aplica direto.

`scripts/validar.py` confere este arquivo contra o roteiro da seção 3 do prompt sempre que
ele existe (`valida_questionario`). Os trechos que ele lê por expressão regular são o
**cabeçalho de cada item** e a tabela **`## Gabarito resumido`**: mantenha os dois no
formato exato abaixo.

## Ordem e correspondência

**A ordem dos itens é a ordem das linhas do roteiro.** A primeira linha da tabela da seção 3
gera os primeiros itens, e assim por diante. Uma linha que pede 3 questões gera 3 itens
consecutivos. Numere de 1 a 20 sem buraco.

Disso decorre o que o validador cobra: itens por tipo, itens por competência e contagem de
itens com código/estímulo têm de bater com o roteiro, item a item.

## Cabeçalho de cada item

```
## <n> · <Tipo> · C<k> <título curto da competência>[ · com código]
```

- `<n>`: 1 a 20, sequencial.
- `<Tipo>`: exatamente `Múltipla escolha`, `Múltipla resposta` ou `Dissertativa` — os mesmos
  rótulos da coluna "Botão a selecionar" do roteiro.
- `C<k> <título curto>`: o mesmo texto da coluna Tema do roteiro. O validador lê o `C<k>`
  para somar os itens por competência.
- `· com código` (ou `· com estímulo`, em trilha sem programação) **só** nos itens que
  trazem o trecho no enunciado. A soma tem de dar o `blueprint.por_tipo.analise_codigo` da
  matriz — ou, sem programação, a contagem de estímulos do roteiro.

Separe os itens com `---` numa linha só.

## Item de múltipla escolha

````markdown
## 1 · Múltipla escolha · C1 Cena, GameObject e componente

Você arrastou o sprite de uma caixa de madeira para a cena. Ela aparece na tela, mas não cai
nem bloqueia o personagem. Quais componentes ela precisa?

- **A)** Um `Collider2D`, para que ela bloqueie a passagem, e — se ela deve cair — um
  `Rigidbody2D`, para que a física passe a agir sobre ela.
- **B)** Nenhum: um GameObject já vem com comportamento de física por estar na cena.
- **C)** Apenas um script, porque colisão e gravidade são escritas em código.
- **D)** Um `Animator`, que é o componente responsável por informar o motor de física.

**Gabarito: A.** Um GameObject é um recipiente vazio; todo comportamento vem dos componentes.
**B** é o erro de esperar comportamento sem componente; **C** reescreve à mão o que o motor
de física já faz; **D** confunde animação com física.
````

- **Quatro alternativas** (A–D). O enunciado tem no máximo 3 linhas antes das alternativas.
- **Toda alternativa errada sai de um `erros_comuns`** da competência na matriz. Nenhuma
  aleatória: cada distrator é o que pensa quem entendeu em parte.
- A linha `**Gabarito: <letra>.**` é obrigatória — o validador procura por `**Gabarito:`.
  Depois dela, uma frase justificando a correta e **o motivo de cada distrator**, nomeando a
  letra em negrito.

### Item com código

O trecho vai entre o enunciado e as alternativas, em bloco cercado com a linguagem
(```` ```csharp ````, ```` ```python ````, ```` ```js ````, ```` ```html ````). No máximo
12–15 linhas, só com o que a trilha ensinou. Descreva em texto o efeito esperado — nunca
dependa de o estudante ver a tela, a página ou a cena rodando.

**Execute o código antes de escrever o gabarito.** Python e JavaScript rodam aqui: a saída
afirmada tem de ser a saída real. C#, template Django e HTML/CSS não são executáveis fora do
ambiente do estudante — confira à mão e diga isso na entrega.

## Item de múltipla resposta

Igual ao de múltipla escolha, com três diferenças:

- **Cinco alternativas** (A–E), das quais três corretas.
- O enunciado termina com `(marque todas)`.
- O gabarito é `**Gabarito: A, B e C.**` — o conjunto exato.

Cabe onde o tema pede identificar um conjunto: "quais afirmações estão corretas", "o que
entra no MVP", "quais itens são necessários".

## Item dissertativo

````markdown
## 10 · Dissertativa · C4 Física 2D e colisões

Explique por que mover o personagem **pela física** (alterando a velocidade do `Rigidbody2D`)
é diferente de mover **alterando a posição** (`transform.position`) a cada quadro. Diga o que
costuma dar errado na segunda forma.

**O que a resposta precisa conter:**

1. Que alterar a posição direto **teleporta** o objeto, sem o motor de física participar do
   deslocamento (ponto principal).
2. Que mover pela física faz o motor resolver colisão, gravidade e empurrões.
3. Um sintoma concreto do segundo caminho: o personagem atravessa paredes e chão, ou trepida
   porque o motor tenta corrigir a posição que o script forçou.

**Faixas:** os três pontos = integral · pontos 1 e 2, sem um sintoma concreto = parcial · só
"é melhor usar a física" sem explicar a diferença = nulo.
````

- A linha `**O que a resposta precisa conter:**` é obrigatória — é o que o validador procura
  nos itens dissertativos.
- **Três pontos numerados**, o primeiro marcado como `(ponto principal)`.
- **Faixas** na ordem integral · parcial · nulo, cada uma dizendo que combinação de pontos a
  caracteriza. Sem isso a dissertativa não é corrigível por outra pessoa.

## Convenção de gabarito

**O gabarito é sempre a alternativa A** (ou `A, B e C` na múltipla resposta), para a
coordenação revisar rápido. O cabeçalho do arquivo avisa para **embaralhar antes de aplicar**
— não omita esse aviso.

## Cabeçalho do arquivo

```markdown
# Questionário <ID> — <titulo_itt>

> **Referência de aplicação.** Questionário montado por extenso a partir de
> [`prompts/<ID>.md`](../prompts/<ID>.md): serve para comparar com o que a plataforma
> devolver, para substituir um item que vier fraco, ou para aplicar direto.
>
> | | |
> |---|---|
> | Trilha | <nome e recorte> |
> | Matriz | [`cursos/<ID>-<slug>.json`](../cursos/<ID>-<slug>.json) |
> | Itens | 20 — 16 múltipla escolha · 2 múltipla resposta · 2 dissertativa |
> | Com código | <N> (itens <lista>) |
> | Tempo estimado | <blueprint.tempo_estimado_min> min |
> | Nível mínimo esperado | adequado (70–84%) |
>
> <uma a duas frases sobre o que o questionário deliberadamente não cobra — a regra 5 do
> texto colável, quando a trilha usa ferramenta com interface — e como os itens com código
> descrevem o efeito esperado.>
>
> A ordem segue as linhas do roteiro. **O gabarito é sempre a primeira alternativa** para
> facilitar a revisão — embaralhe antes de aplicar.

---
```

Em trilha sem programação, a linha da tabela é `| Com estímulo | <N> (itens <lista>) |` e o
parágrafo diz que a trilha é **sem programação** e que tipo de estímulo os itens trazem —
trecho de GDD, cena descrita, lista de funcionalidades — e que nenhum depende de ver imagem.

## Fechamento do arquivo

### Tabela `## Gabarito resumido`

Duas metades por linha, 4 células cada (itens 1–10 à esquerda, 11–20 à direita):

```markdown
## Gabarito resumido

| # | Tipo | Comp. | Gabarito | # | Tipo | Comp. | Gabarito |
|:-:|------|:-----:|:--------:|:-:|------|:-----:|:--------:|
| 1 | MC | C1 | A | 11 | MC | C5 | A |
| 5 | MR | C2 | A, B, C | 15 | MR | C6 | A, B, C |
| 10 | Dissertativa | C4 | rubrica | 20 | Dissertativa | C8 | rubrica |

**Conferência com o roteiro de `prompts/<ID>.md`:** C1 ×2, C2 ×3, … = 20 itens ·
16 MC + 2 MR + 2 dissertativas · <N> com código.
```

O rótulo de tipo aqui é abreviado: `MC`, `MR` ou `Dissertativa` — o validador cruza cada
linha com o cabeçalho do item correspondente e reclama de item ausente ou a mais.

### Seção `## Correção`

Repete a regra de pontuação e o corte, com o link da matriz: 1 ponto por item objetivo
(múltipla resposta só pontua com o conjunto exato), dissertativa 1 / 0,5 / 0 pela rubrica do
próprio item, converter em porcentagem e comparar com `rubrica_proficiencia`. O mínimo
esperado é **adequado (70–84%)** — 14 pontos.

## Calibragem

Números dos 9 questionários existentes — 180 itens, 59 com código ou estímulo:

| | Programação | Sem programação |
|---|---|---|
| Itens | 20 | 20 |
| Com código / estímulo | 5–8, igual ao `analise_codigo` do blueprint | 6 estímulos |
| Alternativas | 4 na MC, 5 na MR | 4 na MC, 5 na MR |
| Linhas de código por item | 12–15 no máximo | — |

## Não crie `questoes/`

A pasta `questoes/` é anterior a `questionarios/` e cobre só os itens com código de FE03,
PR02 e PR03. Está mantida por histórico; **não gere arquivos novos lá**.
