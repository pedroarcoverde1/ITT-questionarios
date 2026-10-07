# ITT — Questionários de proficiência pós-trilha

A **ITT** é uma ONG que ensina computação para adolescentes do ensino fundamental e médio
usando trilhas (formações) da Alura. Este repositório responde a uma pergunta: **ao concluir a
trilha, o estudante atingiu um nível considerável?**

Para cada trilha existem dois artefatos:

| Artefato | Para quê |
|----------|----------|
| `cursos/<ID>-<slug>.json` | **Matriz de aprendizagem**: competências, objetivos por curso, rubrica de proficiência e blueprint do questionário. É o documento que a coordenação revisa e ajusta. |
| `prompts/<ID>.md` | **Descrição compacta** da trilha em forma de prompt. É o arquivo que se cola na plataforma parceira para gerar o questionário. Autossuficiente: funciona sozinho, sem o JSON junto. |

O status de cada trilha está em [`catalogo.md`](catalogo.md).

## Trilhas prontas

| ID | Trilha | Matriz | Prompt |
|----|--------|--------|--------|
| PR01 | A partir do zero: iniciante em programação | [json](cursos/PR01-iniciante-programacao.json) | [md](prompts/PR01.md) |
| PR02 | Aprenda a programar em Python com Orientação a Objetos | [json](cursos/PR02-python-orientacao-objetos.json) | [md](prompts/PR02.md) |
| FE01 | HTML e CSS para projetos web | [json](cursos/FE01-html-css-projetos-web.json) | [md](prompts/FE01.md) |

## Como usar

1. Abra `prompts/<ID>.md` e cole o conteúdo inteiro na plataforma de questionários.
2. A plataforma devolve um JSON de itens no formato descrito na seção 7 do prompt.
3. Confira contra o blueprint: nº de itens por competência, por tipo e por nível cognitivo.
4. Aplique o questionário depois da trilha concluída e reporte a faixa da rubrica (seção 8).

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
- **Três tipos de item**: múltipla escolha, análise de código e dissertativa.
- **Dois níveis aninhados**: competências valem para a trilha inteira; cada curso tem seus
  próprios objetivos, e todo objetivo aponta para uma competência.
- Cada curso declara um `fora_de_escopo` — é a fronteira que impede o gerador de cobrar
  conteúdo que a trilha não ensinou.

## Validação

```bash
python3 scripts/validar.py          # valida todos os arquivos de cursos/
python3 scripts/validar.py cursos/PR02-python-orientacao-objetos.json
```

Só usa a biblioteca padrão. Checa: campos obrigatórios, prefixos de id, soma dos pesos = 1.0,
carga dos cursos = carga da trilha, objetivos apontando para competências existentes,
competências órfãs, totais do blueprint, faixas contíguas da rubrica e existência do prompt.

O formato está documentado em [`esquema/matriz.schema.json`](esquema/matriz.schema.json)
(JSON Schema draft 2020-12), útil para autocompletar no editor. A validação executável do
projeto é o script, que cobre também as regras que o schema não expressa.

## Adicionando uma trilha nova

1. Localize a formação em `alura.com.br` e anote a URL.
2. Para cada curso dela, abra `alura.com.br/curso-online-<slug>` e colete carga horária,
   ementa, público-alvo e os bullets de "O que você vai aprender".
3. Crie `cursos/<ID>-<slug>.json` seguindo PR02 como modelo (é o mais completo).
4. Escreva `prompts/<ID>.md` com as mesmas 8 seções dos prompts existentes.
5. Rode `python3 scripts/validar.py` e corrija o que aparecer.
6. Atualize a linha da trilha em `catalogo.md` e a tabela deste README.

## Estrutura

```
catalogo.md                  trilhas da ONG, times e divergências entre planilhas
cursos/                      matrizes de aprendizagem (JSON)
prompts/                     descrições compactas coláveis (Markdown)
esquema/matriz.schema.json   formato das matrizes
scripts/validar.py           validação de consistência
imagens/                     planilhas de trilhas da ITT (fonte original)
```
