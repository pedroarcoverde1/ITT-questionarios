# ITT — Questionários de proficiência pós-trilha

A **ITT** é uma ONG que ensina computação para adolescentes do ensino fundamental e médio
usando trilhas (formações) da Alura. Este repositório responde a uma pergunta: **ao concluir a
trilha, o estudante atingiu um nível considerável?**

Para cada trilha existem três artefatos:

| Artefato | Para quê |
|----------|----------|
| `cursos/<ID>-<slug>.json` | **Matriz de aprendizagem**: competências, objetivos por curso, rubrica de proficiência e blueprint do questionário. É o documento que a coordenação revisa e ajusta. |
| `prompts/<ID>.md` | **Texto colável + roteiro de montagem**: a seção 2 é o prompt que se cola na plataforma parceira (define o tema das questões); a seção 3 diz quantas questões por tema e qual botão de tipo selecionar. |
| `questionarios/<ID>.md` | **Questionário montado**: os 20 itens escritos por extenso, com gabarito e o motivo de cada alternativa errada. É a referência do que pedir à plataforma — e pode ser aplicado como está. |

O status de cada trilha está em [`catalogo.md`](catalogo.md). Para o fluxo de uso completo —
qual artefato serve a quem, como aplicar um questionário e como acrescentar uma trilha — veja
[`entrega.md`](entrega.md).

## Trilhas prontas

As 9 trilhas da planilha atual da ITT, cobrindo 39 cursos e 329 horas.

| ID | Escola | Trilha | Matriz | Prompt | Questionário |
|----|--------|--------|--------|--------|--------------|
| PR01 | Programação | A partir do zero: iniciante em programação | [json](cursos/PR01-iniciante-programacao.json) | [md](prompts/PR01.md) | [md](questionarios/PR01.md) |
| PR02 | Programação | Aprenda a programar em Python com Orientação a Objetos | [json](cursos/PR02-python-orientacao-objetos.json) | [md](prompts/PR02.md) | [md](questionarios/PR02.md) |
| PR03 | Programação | Django: crie aplicações em Python | [json](cursos/PR03-django-aplicacoes-python.json) | [md](prompts/PR03.md) | [md](questionarios/PR03.md) |
| PR06 | Programação | Desenvolva jogos com Unity | [json](cursos/PR06-jogos-unity.json) | [md](prompts/PR06.md) | [md](questionarios/PR06.md) |
| PR12 | Programação | Boas práticas em Python | [json](cursos/PR12-boas-praticas-python.json) | [md](prompts/PR12.md) | [md](questionarios/PR12.md) |
| FE01 | Front-end | HTML e CSS para projetos web | [json](cursos/FE01-html-css-projetos-web.json) | [md](prompts/FE01.md) | [md](questionarios/FE01.md) |
| FE03 | Front-end | Desenvolvimento Front-end com JavaScript | [json](cursos/FE03-front-end-javascript.json) | [md](prompts/FE03.md) | [md](questionarios/FE03.md) |
| UX02 | UX & Design | Game Design | [json](cursos/UX02-game-design.json) | [md](prompts/UX02.md) | [md](questionarios/UX02.md) |
| UX03 | UX & Design | Blender | [json](cursos/UX03-blender.json) | [md](prompts/UX03.md) | [md](questionarios/UX03.md) |

## Como usar

1. Abra `prompts/<ID>.md` e cole a **seção 2** no campo de prompt da plataforma — só ela.
   O prompt define o **tema** das questões; o tipo não vem dele.
2. Siga o roteiro da **seção 3**, linha por linha: em cada uma, selecione o botão de tipo
   indicado (múltipla escolha, múltipla resposta ou dissertativa) e peça a quantidade
   indicada para aquele tema.
3. Confira os totais do roteiro: 20 itens por trilha, 2 deles dissertativos, e a contagem
   de itens com trecho de código.
4. Compare o que a plataforma devolveu com `questionarios/<ID>.md`, item a item — a ordem é
   a mesma do roteiro. Onde o item gerado vier mais fraco, use o de lá. Se vários vierem
   rasos, cole dois ou três itens do arquivo no prompt como amostra e peça de novo.
5. Aplique o questionário depois da trilha concluída e reporte a faixa de proficiência de
   `cursos/<ID>-*.json` → `rubrica_proficiencia`.

O **nível mínimo esperado** em todas as trilhas é a faixa **adequado (70–84%)**. Abaixo disso,
a trilha não produziu a proficiência pretendida para aquele estudante.

## Como a matriz foi construída

Os dados factuais — lista de cursos, carga horária, módulos da ementa, objetivos declarados —
vêm das **páginas públicas da Alura**, registradas em `metadados.fontes` de cada arquivo com a
data de extração. Nenhum vídeo foi baixado; não é preciso login para reproduzir a coleta.

O que **não** vem da Alura e é elaboração pedagógica da ITT, portanto revisável:

- o agrupamento dos objetivos em competências terminais;
- os **pesos** de cada competência e a distribuição de itens do blueprint;
- os **erros comuns** (que viram os distratores das alternativas);
- as **faixas de proficiência** e o corte do "nível considerável".

## Decisões de desenho

- **Pós-trilha apenas**, sem pré-teste. A matriz carrega faixas de corte em vez de itens
  comparáveis antes/depois.
- **Três tipos de item** na matriz: múltipla escolha, análise de código e dissertativa.
  A plataforma, porém, só oferece três botões — múltipla escolha, múltipla resposta e
  dissertativa. No roteiro de cada prompt, os itens de `analise_codigo` viram múltipla
  escolha com um trecho de código no enunciado (coluna "Com código"), e parte dos itens
  objetivos vira múltipla resposta onde o tema pede identificar um conjunto.
- **Trilhas sem programação** (UX02 Game Design e UX03 Blender) não usam `analise_codigo`:
  o blueprint tem só múltipla escolha e dissertativa, e no roteiro a coluna "Com código" dá
  lugar a **"Com estímulo"** — um trecho curto de GDD, uma cena ou uma situação de modelagem
  descrita em texto. Os prompts nunca pedem que o estudante veja uma imagem.
- **O que a trilha pressupõe entra na matriz.** Várias formações da Alura são declaradas
  para público profissional ou de nível intermediário (PR03, PR12 e UX02). Nesses casos a
  matriz cobra o conceito, calibra os contextos ao nível da ITT e empurra a prática
  profissional para o `fora_de_escopo`; o ajuste fica registrado em
  `rubrica_proficiencia.observacao` e em [`catalogo.md`](catalogo.md).
- **Dois níveis aninhados**: competências valem para a trilha inteira; cada curso tem seus
  próprios objetivos, e todo objetivo aponta para uma competência.
- Cada curso declara um `fora_de_escopo` — é a fronteira que impede o gerador de cobrar
  conteúdo que a trilha não ensinou.

## Questionários montados

O prompt diz **o que pedir** à plataforma; `questionarios/` traz os 20 itens de cada trilha
**já escritos** — enunciado, alternativas, gabarito e o motivo de cada alternativa errada.
São **180 itens**, **59** deles com trecho de código (ou, nas trilhas sem programação, com
estímulo em texto). O índice e as convenções estão em
[`questionarios/README.md`](questionarios/README.md).

Servem para comparar com o que a plataforma devolveu, para colar como amostra de calibragem
quando o gerado vier raso, ou para aplicar direto: os itens objetivos têm gabarito e as
dissertativas têm rubrica de três pontos.

A pasta [`questoes/`](questoes/) é anterior e mais estreita: só os itens com código de FE03,
PR02 e PR03, com o comentário dos distratores mais detalhado. O texto dos itens é o mesmo nos
dois lugares.

Em todos eles o gabarito é a alternativa **A**, para facilitar a revisão pela coordenação —
**embaralhe antes de aplicar**.

## Validação

```bash
python3 scripts/validar.py          # valida todos os arquivos de cursos/
python3 scripts/validar.py cursos/PR02-python-orientacao-objetos.json
```

Só usa a biblioteca padrão. Checa: campos obrigatórios, prefixos de id, soma dos pesos = 1.0,
carga dos cursos = carga da trilha, objetivos apontando para competências existentes,
competências órfãs, totais do blueprint, faixas contíguas da rubrica e existência do prompt.

Checa também o **roteiro da seção 3 de cada prompt contra o blueprint da matriz**: número
total de itens, itens objetivos, dissertativas, a contagem da coluna "Com código" e os itens
por competência, além da linha `**Totais**` conferir com a própria tabela. É a garantia de
que o questionário montado na plataforma é o questionário planejado.

E, quando `questionarios/<ID>.md` existe, confere o **questionário escrito contra esse
roteiro**: numeração sequencial de 1 a 20, itens por tipo, itens por competência, contagem de
itens com código ou estímulo, gabarito presente em cada item objetivo, rubrica em cada
dissertativa, e a tabela "Gabarito resumido" conferindo com o cabeçalho de cada item.

O formato está documentado em [`esquema/matriz.schema.json`](esquema/matriz.schema.json)
(JSON Schema draft 2020-12), útil para autocompletar no editor. A validação executável do
projeto é o script, que cobre também as regras que o schema não expressa.

## Relatório em PDF

```bash
python3 scripts/gerar_relatorio.py            # gera relatorios/relatorio-trilhas-itt.pdf
python3 scripts/gerar_relatorio.py --tex-only # só o .tex, para inspecionar
```

Reúne num documento só o que a coordenação precisa consultar fora do editor: panorama das
9 trilhas, e para cada uma a identificação, as competências com suas evidências observáveis,
cada curso com módulos, objetivos e fora de escopo, a rubrica de proficiência e o prompt
completo — roteiro de montagem e texto colável na íntegra. Cerca de 90 páginas, com sumário
navegável.

O conteúdo vem inteiro de `cursos/*.json` e `prompts/*.md`; **não edite o PDF à mão**, altere
a fonte e gere de novo. Precisa de `pdflatex` (TeX Live) no PATH. Ao acrescentar uma trilha,
inclua o ID na lista `ORDEM` do script — ele falha de propósito se encontrar uma matriz que
não esteja nessa lista.

## Adicionando uma trilha nova

### Com a skill do Claude Code

O repositório traz a skill [`gerar-questionario`](.claude/skills/gerar-questionario/SKILL.md),
que recebe a ementa de um curso ou trilha — texto colado, arquivo ou URL da Alura — e gera
os três artefatos: a matriz em `cursos/`, o prompt em `prompts/` e os 20 itens escritos em
`questionarios/`. Ela roda o validador e registra a trilha no catálogo, no README e no
relatório. Com o Claude Code aberto nesta pasta:

```
/gerar-questionario <cole a ementa, o caminho do arquivo ou a URL> — ID PR07
```

ou só peça "gere o questionário desta ementa". O método que a skill segue está em
[`references/matriz.md`](.claude/skills/gerar-questionario/references/matriz.md),
[`references/prompt.md`](.claude/skills/gerar-questionario/references/prompt.md) e
[`references/questionario.md`](.claude/skills/gerar-questionario/references/questionario.md);
ao mudar uma convenção do repositório, atualize esses arquivos junto.

### À mão

1. Localize a formação em `alura.com.br` e anote a URL.
2. Para cada curso dela, abra `alura.com.br/curso-online-<slug>` e colete carga horária,
   ementa, público-alvo e os bullets de "O que você vai aprender".
3. Crie `cursos/<ID>-<slug>.json` seguindo PR02 como modelo (é o mais completo).
4. Escreva `prompts/<ID>.md` com as 3 seções dos prompts existentes: como montar, texto
   para colar e roteiro de montagem. O roteiro precisa fechar com o blueprint da matriz —
   o validador compara os dois.
5. Se quiser a referência aplicável, escreva `questionarios/<ID>.md` com os 20 itens na
   ordem das linhas do roteiro (veja as convenções em `questionarios/README.md`). É opcional:
   o validador só checa o arquivo quando ele existe.
6. Rode `python3 scripts/validar.py` e corrija o que aparecer.
7. Atualize a linha da trilha em `catalogo.md` e a tabela deste README.
8. Acrescente o ID à lista `ORDEM` de `scripts/gerar_relatorio.py` e regenere o PDF.

## Estrutura

```
.claude/skills/              skill gerar-questionario: ementa → matriz + prompt + itens
catalogo.md                  trilhas da ONG, times e divergências entre planilhas
entrega.md                   guia de handoff: fluxo de uso e para que serve cada artefato
cursos/                      matrizes de aprendizagem (JSON)
ementas/                     ementas recebidas sem página pública (criada quando preciso)
prompts/                     descrições compactas coláveis (Markdown)
questionarios/               os 20 itens de cada trilha, escritos (referência de aplicação)
questoes/                    só os itens com código de FE03, PR02 e PR03, comentados
esquema/matriz.schema.json   formato das matrizes
relatorios/                  relatório em PDF, gerado (não editar à mão)
scripts/validar.py           validação de consistência
scripts/gerar_relatorio.py   monta o relatório em PDF a partir de cursos/ e prompts/
imagens/                     planilhas de trilhas da ITT (fonte original)
```
