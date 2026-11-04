---
name: gerar-questionario
description: Recebe a ementa de um curso ou trilha (texto colado, arquivo ou URL da Alura) e gera, no padrão da ITT, a matriz de aprendizagem em cursos/<ID>-<slug>.json, o prompt em prompts/<ID>.md — o texto que se cola na plataforma parceira e o roteiro de montagem — e o questionário escrito em questionarios/<ID>.md, os 20 itens pós-trilha com gabarito e rubrica. Use quando pedirem para gerar o questionário, os prompts, a matriz ou os itens de uma trilha ou curso novo, para "transformar esta ementa em questionário", para adicionar uma trilha ao repositório, para escrever os itens de uma trilha que já tem matriz e prompt, ou para refazer o prompt de uma trilha existente a partir de uma ementa atualizada.
---

# Gerar questionário a partir de uma ementa

Transforma uma ementa em três artefatos do repositório ITT-questionarios:

| Artefato | Papel |
|----------|-------|
| `cursos/<ID>-<slug>.json` | Matriz de aprendizagem: competências, objetivos por curso, rubrica e blueprint de 20 itens. É o que a coordenação revisa. |
| `prompts/<ID>.md` | Prompt em 3 seções: como montar, **texto para colar** na plataforma e **roteiro de montagem** (quantas questões por tema e qual botão). |
| `questionarios/<ID>.md` | Questionário escrito: os 20 itens por extenso, com gabarito, motivo de cada distrator e rubrica nas dissertativas. Referência de aplicação e de comparação com o que a plataforma devolver. |

Cada um é **derivado** do anterior: o prompt sai da matriz, o questionário sai do roteiro do
prompt. Nunca escreva um prompt sem a matriz, nem itens sem o roteiro. O validador cruza os
três; as regras de distribuição que ele não checa estão na conferência do passo 6.

O questionário é opcional para o validador, mas é o que o outro time usa — só pule quando a
pessoa pedir "só a matriz e o prompt". Veja [entrega.md](../../../entrega.md) para o fluxo de
uso dos três artefatos.

Antes de escrever, leia:

- [references/matriz.md](references/matriz.md) — como montar cada campo do JSON e os números de calibragem.
- [references/prompt.md](references/prompt.md) — o modelo exato do `.md` e as regras de redação do texto colável.
- [references/questionario.md](references/questionario.md) — o formato de cada item, as convenções de gabarito e rubrica.
- Um exemplo real do mesmo tipo de trilha: `cursos/PR06-jogos-unity.json` + `prompts/PR06.md`
  + `questionarios/PR06.md` (programação), ou os três de UX02 (sem programação).
  `cursos/PR02-python-orientacao-objetos.json` é a matriz mais completa.

## Por que a plataforma pede este formato

A plataforma parceira não recebe um arquivo que devolve itens prontos. O campo de prompt
define só o **tema** das questões; o **tipo** vem de um botão selecionado a cada pedido —
múltipla escolha, múltipla resposta ou dissertativa. Por isso o prompt tem um texto colável
(o tema) e um roteiro linha a linha (o botão e a quantidade). A matriz tem um tipo a mais,
`analise_codigo`, que no roteiro vira múltipla escolha com trecho de código no enunciado.

E, porque a plataforma às vezes devolve item raso ou fora do escopo da trilha, o
questionário escrito existe como **referência**: a coordenação compara item a item, troca o
que vier fraco, cola dois ou três dos nossos no prompt como amostra de calibragem, ou aplica
os nossos direto. Sem ele não há como saber se o que a plataforma gerou é a avaliação que a
matriz planejou.

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

- `n_atividades` e `atualizado_em` ficam `null`, como em PR06 (o schema aceita o nulo
  nesses dois campos justamente por isso);
- carga por curso ausente → divida o total; tecnologia não nomeada (dialeto de SQL, versão
  de engine, framework) → escolha a mais comum para iniciantes; registre cada suposição em
  `metadados.derivado_de` e em "Pontos para a equipe ITT confirmar" do `catalogo.md`.

Tudo o que é elaboração pedagógica — competências, pesos, erros comuns, faixas — é da ITT e
pode ser proposto por você.

**Ementa colada ou em arquivo, sem página pública**: `trilha.url` e `cursos[].url` são
obrigatórios. Crie a pasta `ementas/` se ainda não existir, salve o texto da ementa em
`ementas/<ID>-<slug>.md` e use esse caminho relativo nos campos `url` e em
`metadados.fontes` — o schema aceita URL pública ou caminho relativo dentro do repositório.
Quando a fonte não é a Alura, `titulo_alura` guarda o nome do curso na fonte, e o texto
"Alura" da matriz e do prompt (observação da rubrica, regra de redação 7) vira o nome da
plataforma de origem ou "plataforma do curso".

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

### 5. Escrever o questionário — `questionarios/<ID>.md`

Siga [references/questionario.md](references/questionario.md). Os 20 itens por extenso, **na
ordem das linhas do roteiro**: uma linha que pede 3 questões gera 3 itens consecutivos.

O que não se negocia, porque é o que dá valor ao arquivo:

- toda alternativa errada sai de um `erros_comuns` da competência na matriz, e o motivo de
  cada distrator fica escrito abaixo do gabarito;
- 4 alternativas na múltipla escolha, 5 na múltipla resposta (3 corretas);
- o gabarito é sempre a alternativa **A** — e o cabeçalho avisa para embaralhar;
- as dissertativas trazem rubrica de 3 pontos com faixas integral / parcial / nulo;
- **código Python e JavaScript tem de ser executado antes** de o gabarito afirmar a saída.
  C#, template Django e HTML/CSS não rodam aqui: confira à mão e diga isso na entrega.

Mantenha exatos o cabeçalho de cada item (`## <n> · <Tipo> · C<k> <título>[ · com código]`) e
a tabela `## Gabarito resumido` — o validador lê os dois por expressão regular.

Se a pessoa pediu só a matriz e o prompt, pule este passo e diga que a trilha ficou sem o
questionário de referência.

### 6. Validar

```bash
PYTHONIOENCODING=utf-8 python scripts/validar.py cursos/<ID>-<slug>.json
```

Corrija até sair `✓`. Um comando só valida os três artefatos: a matriz, o roteiro do prompt
contra o blueprint e — quando `questionarios/<ID>.md` existe — o questionário contra o
roteiro. Os erros mais comuns: pesos que somam 0.99, `itens_alvo` que somam 21 depois do
arredondamento, roteiro com contagem por competência errada, linha `**Totais**` fora do
formato exato, competência sem nenhum objetivo apontando para ela, item do questionário sem
a linha `**Gabarito:` ou fora da tabela de gabarito resumido.

O validador só confere totais e presença. Confira você mesmo, nos três artefatos:

- [ ] as 2 dissertativas estão em competências diferentes, ambas com `dissertativa` em
      `tipos_de_item`;
- [ ] as 2 múltiplas respostas estão em competências diferentes;
- [ ] "Com código" só é diferente de 0 em linhas de múltipla escolha de competências com
      `analise_codigo` em `tipos_de_item`;
- [ ] a calibragem da regra 8 do texto colável repete `blueprint.por_bloom`;
- [ ] as linhas do bloco colável têm até ~92 caracteres;
- [ ] nada no texto colável nem nos itens cobra algo que esteja no `fora_de_escopo`;
- [ ] cada distrator dos itens é rastreável a um `erros_comuns` da competência;
- [ ] a saída afirmada nos itens com código é a saída real do código.

### 7. Registrar a trilha no repositório

- `catalogo.md`: linha na tabela de trilhas (na coluna "Página Alura", o link da fonte que
  houver), a frase de totais logo abaixo dela ("Todas as N trilhas… X cursos, Y horas") e,
  se a ementa teve furo de fonte, suposição, público acima do nível da ITT ou ID fora da
  planilha, uma linha em "Pontos para a equipe ITT confirmar". Não mexa na tabela de Times
  sem a pessoa pedir.
- `README.md`: linha na tabela "Trilhas prontas" (as três colunas de artefato), a frase de
  totais acima dela, a contagem de itens da seção "Questionários montados" e a contagem de
  trilhas na seção "Relatório em PDF".
- `questionarios/README.md`, se você escreveu o questionário: linha na tabela do índice, o
  total de itens e de itens com código do parágrafo de abertura.
- `scripts/gerar_relatorio.py`: acrescente o ID à lista `ORDEM` — o script falha de
  propósito se achar uma matriz fora dela.
- Se `pdflatex` estiver no PATH, regenere o PDF com
  `PYTHONIOENCODING=utf-8 python scripts/gerar_relatorio.py`. Se não estiver, avise que o
  PDF ficou desatualizado.

Não faça commit sem a pessoa pedir.

### 8. Entregar

Responda com:

- os caminhos dos arquivos gerados e o resultado do validador;
- o **texto para colar** (seção 2) e o **roteiro** (seção 3), para a pessoa já usar;
- o que é suposição ou elaboração sua e merece revisão da coordenação: dados que faltaram
  na ementa, público declarado acima do nível da ITT, pesos que você decidiu, itens com
  código que você não conseguiu executar.
