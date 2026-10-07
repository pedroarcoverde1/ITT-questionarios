# Catálogo de trilhas ITT

Fonte: planilha de trilhas da ONG (`imagens/planilha-trilhas-atual.jpeg`, aba **Times**).
A planilha anterior (`imagens/planilha-trilhas-antiga.jpeg`) está registrada aqui só para
rastrear as divergências — ela **não** é fonte de verdade.

## Trilhas da planilha atual

| ID | Escola | Formação (nome na planilha) | Página Alura | Carga | Cursos | Matriz |
|----|--------|------------------------------|--------------|-------|:------:|:------:|
| PR01 | Programação | A partir do zero: iniciante em programação | [formacao-programacao](https://www.alura.com.br/formacao-programacao) | 29h | 5 | ✅ [`cursos/PR01-iniciante-programacao.json`](cursos/PR01-iniciante-programacao.json) |
| PR02 | Programação | Aprenda a programar em Python com Orientação a Objetos | [formacao-linguagem-python](https://www.alura.com.br/formacao-linguagem-python) | 22h | 3 | ✅ [`cursos/PR02-python-orientacao-objetos.json`](cursos/PR02-python-orientacao-objetos.json) |
| PR03 | Programação | Django: crie aplicações em Python | — | — | — | ⬜ |
| PR06 | Programação | Desenvolva jogos com Unity | — | — | — | ⬜ |
| PR12 | Programação | Boas práticas em Python | — | — | — | ⬜ |
| FE01 | Front-end | HTML e CSS para projetos web | [formacao-html-css](https://www.alura.com.br/formacao-html-css) | 54h | 4 | ✅ [`cursos/FE01-html-css-projetos-web.json`](cursos/FE01-html-css-projetos-web.json) |
| FE03 | Front-end | Desenvolvimento Front-end: criar aplicações web com HTML, CSS e JavaScript | — | — | — | ⬜ |
| UX02 | UX & Design | Game Design | — | — | — | ⬜ |
| UX03 | UX & Design | Blender | — | — | — | ⬜ |

✅ = matriz de aprendizagem e prompt prontos · ⬜ = pendente

## Times (agrupamentos de trilhas)

Da aba **Times**, cada time percorre uma combinação de formações:

| Time | Trilhas |
|------|---------|
| Iniciante Python | PR01, PR02, PR03, PR12 |
| Iniciante Front-End | FE01, FE03 |
| Front-End 2 e Games 1 | FE03, UX02, UX03 |
| Games 1 + Front End 1 | UX02, UX03, FE01 |
| Python Reduzido | PR01, PR02 |
| Games 1 | UX02, UX03 |
| Unity + Games 1 + Front-End 1 | PR06, UX02, UX03, FE01 |
| Unity + Front-End 1 | PR06, FE01 |
| Front-End 1 | FE01 |
| Iniciante Python Reduzido | PR01, PR02, PR12 |

## Divergências entre as duas planilhas

Resolvidas sempre a favor da planilha atual, mas listadas para a equipe ITT confirmar:

| Item | Planilha antiga | Planilha atual | Tratamento |
|------|-----------------|----------------|-----------|
| Django | `PR05` | `PR03` | usamos **PR03** |
| Prefixo de Front-end | `FR01`, `FR02` | `FE01`, `FE03` | usamos **FE\*** |
| UX03 | Formação Game art: construindo um mundo isométrico | Formação Blender | usamos **Blender** |
| Começando com Linux | `DO05` (DevOps) | ausente | **fora do escopo** até a ITT confirmar se ainda é oferecida |
| WordPress: crie sites do zero | `FR02` (Front-end) | ausente | **fora do escopo**, idem |

## Divergências entre planilha e Alura

A Alura renomeia formações com frequência. O nome da planilha e o nome atual na Alura são
guardados separadamente em cada JSON (`trilha.titulo_itt` vs `trilha.titulo_alura`):

| ID | Nome na planilha ITT | Nome atual na Alura |
|----|----------------------|---------------------|
| PR01 | A partir do zero: iniciante em programação | A partir do zero: iniciante em programação |
| PR02 | Aprenda a programar em Python com Orientação a Objetos | Aprenda a programar em Python com Orientação a Objetos |
| FE01 | (A partir do zero:) HTML e CSS para projetos web | HTML e CSS: do zero ao layout responsivo |
