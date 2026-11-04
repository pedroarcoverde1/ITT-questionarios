# Guia de entrega — fluxo de uso e artefatos

Documento de handoff deste repositório. Responde a três perguntas: **o que tem aqui**,
**o que de fato se usa** e **como usar**, do primeiro questionário aplicado até a inclusão
de uma trilha nova.

Contexto em uma frase: a ITT é uma ONG que ensina computação para adolescentes usando
trilhas da Alura, e este repositório existe para responder se, ao concluir a trilha, o
estudante atingiu um nível considerável. A resposta é um questionário pós-trilha de 20 itens
por trilha, ancorado numa matriz de competências.

## Os quatro artefatos, e quais importam para você

Cada trilha tem três artefatos versionados, derivados em cadeia. O quarto é o relatório.

```
ementa da Alura  →  cursos/<ID>.json  →  prompts/<ID>.md  →  questionarios/<ID>.md
                    (matriz)             (texto colável       (os 20 itens
                                          + roteiro)           escritos)
                            ↓
                    relatorios/relatorio-trilhas-itt.pdf
```

| Artefato | O que é | Quem usa, e para quê |
|----------|---------|----------------------|
| `cursos/<ID>-<slug>.json` | **Matriz de aprendizagem.** Competências da trilha, objetivos por curso, pesos, rubrica de proficiência e blueprint dos 20 itens. | **Coordenação pedagógica**, para revisar e ajustar o que a avaliação cobra. É a fonte de tudo o mais — mexer aqui obriga a refazer os dois seguintes. |
| `prompts/<ID>.md` | **Texto colável + roteiro.** A seção 2 é o prompt que vai no campo da plataforma; a seção 3 diz, linha a linha, quantas questões de cada tema e qual botão de tipo apertar. | **Quem opera a plataforma.** É o artefato de trabalho do dia a dia. |
| `questionarios/<ID>.md` | **Questionário escrito.** Os 20 itens por extenso: enunciado, alternativas, gabarito, motivo de cada alternativa errada e rubrica nas dissertativas. | **Quem aplica e quem corrige.** Serve para comparar com o que a plataforma devolveu, para substituir item fraco, ou para aplicar direto. |
| `relatorios/relatorio-trilhas-itt.pdf` | As 9 trilhas num documento só, ~90 páginas com sumário. Gerado, nunca editado à mão. | **Reunião e revisão offline.** Nada aqui é fonte: tudo vem de `cursos/` e `prompts/`. |

**Se você só vai aplicar questionários:** `prompts/<ID>.md` e `questionarios/<ID>.md`
bastam. A matriz você consulta no fim, para converter a nota em faixa de proficiência.

**Se você vai integrar isso num serviço de geração de questionários:** o que transfere é a
matriz (`esquema/matriz.schema.json`), o validador e as regras de redação de
`.claude/skills/gerar-questionario/references/`. A seção 3 dos prompts existe só porque a
UI da plataforma parceira pede o tipo por botão; um serviço que gera item a item não precisa
dela. Veja [Limites conhecidos](#limites-conhecidos).

### O que *não* usar

- `questoes/` — pasta anterior, com só os itens de código de FE03, PR02 e PR03. O texto é o
  mesmo que está em `questionarios/`, com comentário de distrator mais longo. Mantida por
  histórico; **não é mais alimentada**.
- `imagens/` — fotos das planilhas originais da ITT. Fonte de conferência de ID e nome de
  trilha, nada além.

## Fluxo 1 — aplicar o questionário de uma trilha que já existe

Exemplo real, trilha **PR06 · Desenvolva jogos com Unity**.

**1. Abra `prompts/PR06.md` e cole a seção 2 no campo de prompt da plataforma.** Só ela, uma
vez. É um bloco que começa assim:

```
AVALIAÇÃO PÓS-TRILHA — DESENVOLVIMENTO DE JOGOS 2D COM UNITY

Contexto: questionário aplicado depois de a trilha ser concluída, em uma ONG que ensina
computação para adolescentes do ensino fundamental II e médio. A trilha é a primeira
experiência do estudante com uma engine de jogos e com a linguagem C#. (...)

ASSUNTOS

C1 - Cena, GameObject e componente
  Cobrar: dada uma necessidade do jogo, dizer qual componente precisa ser adicionado (...)
  Erros típicos, para virar alternativa errada: (...)
```

Esse texto define **o tema** das questões — não o tipo, não a quantidade.

**2. Percorra a seção 3, linha por linha.** Cada linha é um pedido na plataforma: selecione o
botão da coluna "Botão a selecionar", peça a quantidade da coluna "Questões" e informe como
tema o que está em "Foco da linha".

| Tema | Questões | Botão a selecionar | Com código | Foco da linha |
|------|:--------:|--------------------|:----------:|---------------|
| C1 Cena, GameObject e componente | 2 | Múltipla escolha | 0 | qual componente falta, asset vs instância na cena |
| C2 Scripts em C# e ciclo de vida | 2 | Múltipla escolha | 2 | Start vs Update, efeito do trecho sobre o GameObject |
| C2 Scripts em C# e ciclo de vida | 1 | Múltipla resposta | 0 | quais afirmações sobre Start, Update e Time.deltaTime estão corretas |

A coluna "Com código" diz quantas daquelas questões devem trazer um trecho de código no
enunciado — a plataforma não tem botão para isso, então entra no texto do pedido.

**3. Confira os totais** no fim da seção 3: 20 itens, sendo 16 múltipla escolha, 2 múltipla
resposta e 2 dissertativas, e a contagem de itens com código.

**4. Compare com `questionarios/PR06.md`, item a item.** A ordem é a mesma do roteiro: o item
1 do arquivo corresponde à primeira linha da tabela. Onde o item gerado vier mais fraco,
use o nosso. Se vários vierem rasos, cole dois ou três dos nossos no prompt como amostra de
calibragem e peça de novo.

Cada item de lá está completo e revisável:

```markdown
## 1 · Múltipla escolha · C1 Cena, GameObject e componente

Você arrastou o sprite de uma caixa de madeira para a cena. Ela aparece na tela, mas não cai
nem bloqueia o personagem. Quais componentes ela precisa?

- **A)** Um `Collider2D`, para que ela bloqueie a passagem, e — se ela deve cair — um
  `Rigidbody2D`, para que a física passe a agir sobre ela.
- **B)** Nenhum: um GameObject já vem com comportamento de física por estar na cena.
(...)

**Gabarito: A.** Um GameObject é um recipiente vazio; todo comportamento vem dos componentes.
**B** é o erro de esperar comportamento sem componente; (...)
```

> **O gabarito é sempre a alternativa A** em todos os arquivos, para a coordenação revisar
> rápido. **Embaralhe antes de aplicar.**

**5. Aplique e corrija.** 1 ponto por item objetivo (múltipla resposta só pontua com o
conjunto exato); dissertativa vale 1, 0,5 ou 0 pela rubrica do próprio item. Converta os 20
pontos em porcentagem e leia a faixa em `cursos/PR06-jogos-unity.json` →
`rubrica_proficiencia`:

| Faixa | % | O que a faixa significa |
|-------|---|-------------------------|
| iniciante | 0–49 | reconhece termos, não relaciona nem aplica |
| básico | 50–69 | segue um modelo pronto; comete os erros típicos da trilha |
| **adequado** | **70–84** | **faz sozinho o núcleo da trilha — mínimo esperado** |
| avançado | 85–100 | diagnostica, justifica escolhas, fecha o projeto |

As faixas e o corte são os mesmos nas 9 trilhas — **adequado (70–84%)**, isto é, 14 dos 20
pontos. O **descritor** de cada faixa, porém, é específico da trilha: o "adequado" de PR06
é "programa comportamento em C# no método certo do ciclo de vida, liga input a movimento,
configura colisão…". Leia o descritor da trilha antes de reportar a faixa — é ele que diz o
que o estudante sabe fazer, e a porcentagem sozinha não diz.

Abaixo de adequado, a trilha não produziu a proficiência pretendida para aquele estudante.

## Fluxo 2 — acrescentar uma trilha nova

A partir de uma ementa (URL da Alura, PDF, DOCX ou texto colado).

### Com a skill do Claude Code (caminho recomendado)

O repositório traz a skill
[`gerar-questionario`](.claude/skills/gerar-questionario/SKILL.md), que percorre os 8 passos
do método: lê a ementa, define identificação, escreve a matriz, deriva o prompt, escreve os
20 itens, valida, registra a trilha no catálogo e no README e entrega o que precisa de
revisão humana. Com o Claude Code aberto nesta pasta:

```
/gerar-questionario https://www.alura.com.br/formacao-<slug> — ID PR07
```

ou, sem a URL:

```
/gerar-questionario a ementa está em ~/Downloads/ementa-sql.pdf — ID PR09
```

Ela só interrompe para perguntar duas coisas, e numa pergunta só: o **ID ITT** e, se não
houver página pública, **onde está a ementa**. O resto segue com suposição registrada em
`metadados.derivado_de` e em "Pontos para a equipe ITT confirmar" do `catalogo.md`.

O método está em três arquivos de referência, que são a documentação do padrão e valem a
leitura mesmo sem usar a skill:

| Referência | Conteúdo |
|------------|----------|
| [`references/matriz.md`](.claude/skills/gerar-questionario/references/matriz.md) | como decidir cada campo do JSON, e os números de calibragem das 9 trilhas |
| [`references/prompt.md`](.claude/skills/gerar-questionario/references/prompt.md) | o modelo do `.md` e as 8 regras de redação do texto colável |
| [`references/questionario.md`](.claude/skills/gerar-questionario/references/questionario.md) | o formato de cada item, gabarito, rubrica e as convenções de escrita |

**Ao mudar uma convenção do repositório, atualize esses arquivos no mesmo commit** — são eles
que mantêm a próxima trilha igual às 9 existentes.

### À mão

O passo a passo está no [README](README.md#adicionando-uma-trilha-nova). Em resumo: colete a
ementa de cada curso, escreva a matriz usando PR02 como modelo, derive o prompt, escreva os
itens na ordem do roteiro, rode o validador, atualize `catalogo.md`, o `README.md`, o
`questionarios/README.md` e a lista `ORDEM` de `scripts/gerar_relatorio.py`.

## Validação

Um comando confere os três artefatos de todas as trilhas:

```bash
python3 scripts/validar.py                    # tudo
python3 scripts/validar.py cursos/PR06-jogos-unity.json   # uma trilha
```

Só biblioteca padrão, sem instalar nada. O que ele garante:

| Nível | Checagens |
|-------|-----------|
| Matriz | campos obrigatórios, prefixos de id, soma dos pesos = 1.0, carga dos cursos = carga da trilha, objetivo apontando para competência existente, competência órfã, totais do blueprint, faixas contíguas da rubrica |
| Prompt × matriz | total de itens, itens objetivos, dissertativas, coluna "Com código", itens por competência, e a linha `**Totais**` conferindo com a própria tabela |
| Questionário × prompt | numeração de 1 a 20, itens por tipo, itens por competência, contagem com código/estímulo, gabarito em cada item objetivo, rubrica em cada dissertativa, tabela "Gabarito resumido" conferindo com o cabeçalho de cada item |

É o que impede os três artefatos de divergirem: se o roteiro não bate com o blueprint, o
questionário montado não é o questionário planejado.

**O validador não checa semântica.** Essas conferências são humanas, e estão listadas no
passo 6 da skill: se os distratores saíram de fato dos `erros_comuns`, se nada cobra o que
está no `fora_de_escopo`, se a saída afirmada num item com código é a saída real.

Para regerar o PDF (precisa de `pdflatex` no PATH):

```bash
python3 scripts/gerar_relatorio.py            # relatorios/relatorio-trilhas-itt.pdf
python3 scripts/gerar_relatorio.py --tex-only # só o .tex, para inspecionar
```

## O que é fato e o que é decisão nossa

A distinção mais importante para quem recebe o material, porque separa o que não se discute
do que está aberto a revisão.

| Vem da ementa — fato, não se inventa | É elaboração pedagógica da ITT — revisável |
|---|---|
| títulos, URLs, carga horária, número de cursos | o agrupamento dos objetivos em 7–8 competências |
| módulos de cada curso | os pesos de cada competência e a distribuição do blueprint |
| bullets de "o que você vai aprender" | as evidências observáveis |
| conceitos citados | os **erros comuns**, que viram os distratores |
| público-alvo e pré-requisitos declarados | as faixas de proficiência e o corte do "nível considerável" |
| | o `fora_de_escopo` de cada curso |

Toda suposição feita por falta de dado na ementa está registrada em `metadados.derivado_de`
da matriz, e o que precisa de decisão da ITT está em "Pontos para a equipe ITT confirmar"
no [`catalogo.md`](catalogo.md). **Comece por essa lista.**

Um caso recorrente: três trilhas (PR03, PR12 e UX02) são declaradas na Alura para público
profissional ou intermediário. Nesses casos a matriz cobra o conceito, calibra os contextos
ao nível da ITT e empurra a prática profissional para o `fora_de_escopo`; o ajuste está em
`rubrica_proficiencia.observacao`.

## Limites conhecidos

- **Pós-trilha apenas, sem pré-teste.** Não há itens comparáveis antes/depois: a conclusão
  vem das faixas de corte, não de ganho medido.
- **As faixas de proficiência nunca foram aplicadas.** 70% como corte de "adequado" é
  decisão da coordenação, não resultado empírico. `rubrica_proficiencia.observacao` pede
  revisão depois do primeiro ciclo de aplicação.
- **O roteiro de montagem é específico da plataforma parceira.** Ele existe porque o campo de
  prompt define só o tema e o tipo vem de um botão por pedido. Numa integração em que o
  serviço gera item a item, a seção 3 perde sentido e o que fica é a matriz, o texto colável
  e as regras de redação.
- **Nenhum item depende de imagem.** Nas trilhas sem programação (UX02, UX03) o estímulo é
  sempre texto — trecho de GDD, cena descrita, lista de funcionalidades. Isso limita o que
  dá para avaliar em Blender e em direção de arte.
- **Código não executável conferido à mão.** Python e JavaScript dos itens foram executados;
  C# (PR06) e templates Django não rodam fora do ambiente do estudante.
- **`questoes/` está congelada** e duplica texto de `questionarios/`. Se incomodar, o caminho
  é apagá-la, não atualizá-la.
