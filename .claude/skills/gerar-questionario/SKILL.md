---
name: gerar-questionario
description: Recebe a ementa de um curso ou trilha (texto colado, arquivo ou URL da Alura) e gera, no padrão da ITT, a matriz de aprendizagem em cursos/<ID>-<slug>.json e o prompt em prompts/<ID>.md — o texto que se cola na plataforma parceira e o roteiro de montagem que resulta no questionário pós-trilha de 20 itens. Use quando pedirem para gerar o questionário, os prompts ou a matriz de uma trilha ou curso novo, para "transformar esta ementa em questionário", para adicionar uma trilha ao repositório ou para refazer o prompt de uma trilha existente a partir de uma ementa atualizada.
---

# Gerar questionário a partir de uma ementa

Transforma uma ementa em dois artefatos do repositório ITT-questionarios:

| Artefato | Papel |
|----------|-------|
| `cursos/<ID>-<slug>.json` | Matriz de aprendizagem: competências, objetivos por curso, rubrica e blueprint de 20 itens. É o que a coordenação revisa. |
| `prompts/<ID>.md` | Prompt em 3 seções: como montar, **texto para colar** na plataforma e **roteiro de montagem** (quantas questões por tema e qual botão). |

O prompt é **derivado** da matriz — nunca escreva um sem o outro. O validador cruza os
totais dos dois; as regras de distribuição que ele não checa estão na conferência do passo 5.

Antes de escrever, leia:

- [references/matriz.md](references/matriz.md) — como montar cada campo do JSON e os números de calibragem.
- [references/prompt.md](references/prompt.md) — o modelo exato do `.md` e as regras de redação do texto colável.
- Um exemplo real do mesmo tipo de trilha: `prompts/PR06.md` + `cursos/PR06-jogos-unity.json`
  (programação), `prompts/UX02.md` + `cursos/UX02-game-design.json` (sem programação) ou
  `cursos/PR02-python-orientacao-objetos.json` (a matriz mais completa).

## Por que a plataforma pede este formato

A plataforma parceira não recebe um arquivo que devolve itens prontos. O campo de prompt
define só o **tema** das questões; o **tipo** vem de um botão selecionado a cada pedido —
múltipla escolha, múltipla resposta ou dissertativa. Por isso o prompt tem um texto colável
(o tema) e um roteiro linha a linha (o botão e a quantidade). A matriz tem um tipo a mais,
`analise_codigo`, que no roteiro vira múltipla escolha com trecho de código no enunciado.

## Passo a passo

### 1. Ler a ementa e completar os dados factuais

A ementa pode vir colada, como arquivo (PDF, DOCX, texto) ou como URL. Extraia:

- título da trilha ou do curso, carga horária, público-alvo declarado, pré-requisitos;
- lista de cursos (uma ementa de **um curso só** vira uma trilha com `n_cursos: 1`);
- por curso: módulos/aulas, bullets de "o que você vai aprender", conceitos citados;
- o projeto prático que atravessa o curso, se houver (vira `projeto_fio_condutor`).

**URL da Alura**: a página de formação é renderizada por JavaScript. Os dados estão no
payload embutido no HTML — estrutura de etapas, lista ordenada de cursos e, por curso, um
JSON-LD com carga, público e data, além da ementa e dos bullets. Busque também cada
`alura.com.br/curso-online-<slug>` para a ementa do curso. Se uma página não estiver
publicada, derive os módulos da descrição da etapa e registre o furo em
`metadados.derivado_de` (veja como PR06 fez).

**Não invente fato.** Carga, módulos e objetivos declarados vêm da ementa. Quando faltar:

- `n_atividades` e `atualizado_em` ficam `null`, como em PR06 (o schema declara o tipo, mas
  o validador aceita o nulo);
- carga por curso ausente → divida o total; tecnologia não nomeada (dialeto de SQL, versão
  de engine, framework) → escolha a mais comum para iniciantes; registre cada suposição em
  `metadados.derivado_de` e em "Pontos para a equipe ITT confirmar" do `catalogo.md`.

Tudo o que é elaboração pedagógica — competências, pesos, erros comuns, faixas — é da ITT e
pode ser proposto por você.

**Ementa colada ou em arquivo, sem página pública**: `trilha.url` e `cursos[].url` são
obrigatórios. Salve o texto da ementa em `ementas/<ID>-<slug>.md` e use esse caminho
relativo nos campos `url` e em `metadados.fontes`. Quando a fonte não é a Alura, `titulo_alura`
guarda o nome do curso na fonte, e o texto "Alura" da matriz e do prompt (observação da
rubrica, regra de redação 7) vira o nome da plataforma de origem ou "plataforma do curso".

### 2. Definir identificação

- **ID ITT** (`PR`, `FE`, `UX` ou `DO` + 2 dígitos) e, se não houver URL, a **URL da página
  do curso**: são as únicas informações que valem bloquear para perguntar, e numa pergunta
  só. Se a pessoa deu o ID, use-o; se ele não está na planilha atual
  (`imagens/planilha-trilhas-atual.jpeg`, listada em `catalogo.md`), siga em frente e
  registre isso em "Pontos para a equipe ITT confirmar". Escola segue o prefixo:
  PR Programação, FE Front-end, UX UX & Design, DO DevOps.
- **Pré-requisitos**: `trilha.pre_requisitos` lista IDs de trilhas ITT. Traduza o
  conhecimento que a ementa pressupõe para a trilha ITT que o ensina, com a cadeia inteira
  (Python básico → `["PR01", "PR02"]`, como PR03 e PR12). Se nenhuma trilha ITT ensina,
  deixe `[]` e diga no Contexto do prompt o que o estudante já precisa saber.
- Confira se `cursos/<ID>-*.json` já existe. Se existe, a tarefa é **atualizar** a trilha:
  leia a matriz atual, preserve o que é elaboração da ITT que continua válida e suba
  `metadados.versao`.
- **Programação ou não?** Se a trilha tem código que o estudante escreve ou lê (Python, JS,
  C#, HTML/CSS…), é de programação: usa `analise_codigo` e a coluna "Com código". Se não
  (design, arte, modelagem 3D, game design), não usa `analise_codigo` e a coluna vira
  "Com estímulo".

### 3. Escrever a matriz — `cursos/<ID>-<slug>.json`

Siga [references/matriz.md](references/matriz.md). Ordem que funciona:

1. objetivos de aprendizagem por curso, a partir dos módulos e bullets da ementa;
2. agrupe os objetivos em 7–8 competências terminais da trilha inteira;
3. para cada competência: 3 evidências observáveis e 4 erros comuns concretos;
4. pesos (soma 1.0) → `itens_alvo` → blueprint;
5. rubrica com descritores específicos da trilha;
6. `fora_de_escopo` de cada curso: o que é vizinho do assunto e a trilha não ensina.

### 4. Escrever o prompt — `prompts/<ID>.md`

Siga o modelo de [references/prompt.md](references/prompt.md) **à risca nos cabeçalhos, na
tabela e na linha de Totais** — o validador e o gerador de relatório leem esses trechos por
expressão regular. O texto colável é a matriz reescrita para quem gera questões: cada
competência vira um bloco "Cobrar" (das evidências) + "Erros típicos" (dos erros comuns).

### 5. Validar

```bash
PYTHONIOENCODING=utf-8 python scripts/validar.py cursos/<ID>-<slug>.json
```

Corrija até sair `✓`. Os erros mais comuns: pesos que somam 0.99, `itens_alvo` que somam
21 depois do arredondamento, roteiro com contagem por competência errada, linha
`**Totais**` fora do formato exato, competência sem nenhum objetivo apontando para ela.

O validador só confere totais. Confira você mesmo, no roteiro e na matriz:

- [ ] as 2 dissertativas estão em competências diferentes, ambas com `dissertativa` em
      `tipos_de_item`;
- [ ] as 2 múltiplas respostas estão em competências diferentes;
- [ ] "Com código" só é diferente de 0 em linhas de múltipla escolha de competências com
      `analise_codigo` em `tipos_de_item`;
- [ ] a calibragem da regra 8 do texto colável repete `blueprint.por_bloom`;
- [ ] as linhas do bloco colável têm até ~92 caracteres;
- [ ] nada no texto colável cobra algo que esteja no `fora_de_escopo`.

### 6. Registrar a trilha no repositório

- `catalogo.md`: linha na tabela de trilhas (na coluna "Página Alura", o link da fonte que
  houver), a frase de totais logo abaixo dela ("Todas as N trilhas… X cursos, Y horas") e,
  se a ementa teve furo de fonte, suposição, público acima do nível da ITT ou ID fora da
  planilha, uma linha em "Pontos para a equipe ITT confirmar". Não mexa na tabela de Times
  sem a pessoa pedir.
- `README.md`: linha na tabela "Trilhas prontas", a frase de totais acima dela e a contagem
  de trilhas na seção "Relatório em PDF".
- `scripts/gerar_relatorio.py`: acrescente o ID à lista `ORDEM` — o script falha de
  propósito se achar uma matriz fora dela.
- Se `pdflatex` estiver no PATH, regenere o PDF com
  `PYTHONIOENCODING=utf-8 python scripts/gerar_relatorio.py`. Se não estiver, avise que o
  PDF ficou desatualizado.

Não faça commit sem a pessoa pedir.

### 7. Entregar

Responda com:

- os caminhos dos dois arquivos e o resultado do validador;
- o **texto para colar** (seção 2) e o **roteiro** (seção 3), para a pessoa já usar;
- o que é suposição ou elaboração sua e merece revisão da coordenação: dados que faltaram
  na ementa, público declarado acima do nível da ITT, pesos que você decidiu.
