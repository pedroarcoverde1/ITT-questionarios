# Prompt — modelo do `prompts/<ID>.md`

O arquivo tem um cabeçalho e três seções. `scripts/validar.py` e `scripts/gerar_relatorio.py`
leem por expressão regular os títulos `## 2. Texto para colar` (seguido de um bloco ```` ``` ````
sem linguagem) e `## 3. Roteiro de montagem`, a tabela do roteiro e a linha `**Totais**`.
Mantenha esses trechos **exatamente** como abaixo.

## Modelo — trilha de programação

````markdown
# Questionário <ID> · <titulo_itt>

> Gerado a partir de `cursos/<ID>-<slug>.json`.
> A **seção 2** é o texto que se cola no campo de prompt da plataforma — e só ele.
> A **seção 3** é o roteiro de montagem: quantas questões por tema e qual botão selecionar.

## 1. Como montar

1. Cole o texto da seção 2 no campo de prompt, uma vez.
2. Percorra as linhas da seção 3 de cima para baixo. Em cada linha, selecione o botão
   indicado, peça a quantidade indicada e informe o tema daquela linha.
3. Confira os totais no fim da seção 3: 20 itens, sendo 2 dissertativas.

## 2. Texto para colar

```
AVALIAÇÃO PÓS-TRILHA — <TEMA DA TRILHA EM MAIÚSCULAS>

Contexto: ...

ASSUNTOS

C1 - <título curto>
  Cobrar: ...
  Erros típicos, para virar alternativa errada: ...

C2 - <título curto>
  Cobrar: ...
  Erros típicos: ...

FORA DE ESCOPO - não cobre nada disso: ...

REDAÇÃO E CALIBRAGEM

- ...
```

## 3. Roteiro de montagem

| Tema | Questões | Botão a selecionar | Com código | Foco da linha |
|------|:--------:|--------------------|:----------:|---------------|
| C1 <título curto> | 2 | Múltipla escolha | 0 | <o que essas questões focam> |
| ... | | | | |

**Totais**: 16 múltipla escolha · 2 múltipla resposta · 2 dissertativa = **20 itens**;
**<N>** deles com trecho de código no enunciado.

> Equivalência com a matriz: os 18 itens objetivos de `cursos/<ID>-<slug>.json`
> (`multipla_escolha` <a> + `analise_codigo` <b>) aparecem aqui como 16 múltipla escolha +
> 2 múltipla resposta, e a coluna "Com código" reproduz os <b> de `analise_codigo` — a
> plataforma não tem botão para esse tipo.
````

## Variação — trilha sem programação

- No cabeçalho, acrescente depois das duas linhas `> A **seção …**`:
  ```
  > Trilha sem programação: no lugar da coluna "Com código" dos prompts de programação, esta
  > tem **"Com estímulo"** — <que tipo de estímulo: trecho de GDD, cena descrita, situação…>
  > no enunciado.
  ```
- Na tabela, o cabeçalho da 4ª coluna é `Com estímulo` (o separador continua `:----------:`
  ou `:------------:`).
- A segunda linha dos Totais é `**<N>** deles com estímulo no enunciado.`
- A nota final diz `(`multipla_escolha` 18)` e explica que a matriz não usa
  `analise_codigo` por a trilha não ter programação.

## Texto para colar (seção 2)

É a matriz reescrita para quem gera as questões. Linhas com no máximo ~92 caracteres,
continuação indentada com 2 espaços, sem Markdown dentro do bloco.

**Título**: `AVALIAÇÃO PÓS-TRILHA — <TEMA>` (o tema, não o nome comercial do curso).

**Contexto** (um parágrafo): questionário aplicado depois de a trilha ser concluída, em uma
ONG que ensina computação para adolescentes do ensino fundamental II e médio; o que o
estudante já sabia antes (pré-requisitos) ou que é a primeira experiência com a ferramenta;
e o projeto fio condutor. Se é trilha sem programação, diga isso aqui.

**ASSUNTOS**: um bloco por competência, na ordem C1…Cn.
- `C<n> - <título curto>`: versão enxuta do título da competência (substantivos, 3–6
  palavras), a mesma usada na coluna Tema do roteiro.
- `Cobrar:` as 3 evidências observáveis, reescritas no infinitivo e separadas por `;`
  ("dado X, apontar Y; distinguir A de B; reconhecer que …").
- `Erros típicos, para virar alternativa errada:` só no **primeiro** bloco; nos demais,
  `Erros típicos:`. Os 4 erros comuns, separados por `;`.

**FORA DE ESCOPO**: a união dos `fora_de_escopo` de todos os cursos, numa frase só.

**REDAÇÃO E CALIBRAGEM**: estas regras, adaptadas à trilha:

1. `Português brasileiro, linguagem direta, sem jargão corporativo. Enunciado de no máximo 3 linhas.`
2. `Contextos concretos e próximos do público: <5–6 cenários do universo de um adolescente que
   combinem com o assunto — jogo, loja de lanches, biblioteca da escola, playlist…>.`
3. Programação: `Quando o item trouxer código, use <linguagem/framework> com no máximo
   <12–15> linhas, só com <o que a trilha usa>. Descreva em texto o efeito esperado — não
   dependa de o estudante ver <a tela/a página/a cena> rodando.` Cite exceções de biblioteca
   por competência, se houver (ex.: "requests, nos itens de C8").
   Sem programação: `Quando o item trouxer estímulo, use <tipos de estímulo> — no máximo 8
   linhas. Nunca dependa de o estudante ver uma imagem.`
4. Programação: `Nada de pegadinha de sintaxe fora do que a trilha ensinou. Se o erro a ser
   detectado for de digitação e não de conceito, o item não serve.`
5. Se a trilha usa ferramenta com interface (engine, editor, software 3D): `Não cobre nome de
   menu, posição de painel ou atalho da interface <da ferramenta>: avalie o raciocínio, não
   a memória da tela.`
6. `As alternativas erradas devem sair dos erros típicos listados em cada assunto, nunca ser
   aleatórias: toda alternativa errada precisa ser plausível para quem entendeu em parte.`
7. `Não pergunte nada sobre a plataforma Alura, nomes de instrutores, duração de curso ou
   ordem dos módulos.` (troque "Alura" pela fonte real, se for outra).
8. `Calibragem cognitiva do conjunto: cerca de <lembrar_entender> itens de compreensão,
   <aplicar> de aplicação e <analisar_avaliar> de análise ou avaliação.` — números do
   `blueprint.por_bloom`.

## Roteiro de montagem (seção 3)

Cada linha é um pedido na plataforma: um tema + um botão + uma quantidade.

- **Coluna Tema**: `C<n> <título curto>`. O validador lê o primeiro token (`C<n>`) para
  somar os itens por competência — ele tem de bater com `blueprint.por_competencia`.
- **Botão a selecionar**: exatamente `Múltipla escolha`, `Múltipla resposta` ou
  `Dissertativa`.
- Uma competência pode ter várias linhas (uma por botão). Ordene por competência e, dentro
  dela, Múltipla escolha → Múltipla resposta → Dissertativa.
- **Distribuição fixa**: 16 múltipla escolha · 2 múltipla resposta · 2 dissertativa.
  - As 2 **dissertativas** vão para competências diferentes, de preferência as de
    `analisar`/`avaliar` ou as que têm uma evidência "explica por que…". Cada uma precisa
    ter `dissertativa` em `tipos_de_item` da competência.
  - As 2 **múltiplas respostas** vão para competências diferentes, onde o assunto pede
    identificar um conjunto ("quais afirmações … estão corretas", "quais passos…", "quais
    itens são necessários…").
  - Múltipla escolha + múltipla resposta de cada competência + dissertativa = `itens_alvo`.
- **Com código / Com estímulo**: quantas das questões daquela linha trazem trecho de código
  (ou estímulo) no enunciado. Só em linhas de múltipla escolha; nas demais, 0. Em trilha de
  programação, a soma tem de ser igual a `blueprint.por_tipo.analise_codigo`, e só em
  competências com `analise_codigo` em `tipos_de_item`. Em trilha sem programação, use 5–7
  estímulos espalhados.
- **Foco da linha**: o recorte das evidências que aquelas questões cobram, em fragmentos
  curtos separados por vírgula. É o que a pessoa digita como tema ao pedir as questões;
  numa linha de múltipla resposta, comece por "quais …"; numa dissertativa, descreva a
  pergunta.
