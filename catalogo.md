# Catálogo de trilhas ITT

Fonte: planilha de trilhas da ONG (`imagens/planilha-trilhas-atual.jpeg`, aba **Times**).
A planilha anterior (`imagens/planilha-trilhas-antiga.jpeg`) está registrada aqui só para
rastrear as divergências — ela **não** é fonte de verdade.

## Trilhas da planilha atual

| ID | Escola | Formação (nome na planilha) | Página Alura | Carga | Cursos | Matriz |
|----|--------|------------------------------|--------------|-------|:------:|:------:|
| PR01 | Programação | A partir do zero: iniciante em programação | [formacao-programacao](https://www.alura.com.br/formacao-programacao) | 29h | 5 | ✅ [`cursos/PR01-iniciante-programacao.json`](cursos/PR01-iniciante-programacao.json) |
| PR02 | Programação | Aprenda a programar em Python com Orientação a Objetos | [formacao-linguagem-python](https://www.alura.com.br/formacao-linguagem-python) | 22h | 3 | ✅ [`cursos/PR02-python-orientacao-objetos.json`](cursos/PR02-python-orientacao-objetos.json) |
| PR03 | Programação | Django: crie aplicações em Python | [formacao-django](https://www.alura.com.br/formacao-django) | 44h | 5 | ✅ [`cursos/PR03-django-aplicacoes-python.json`](cursos/PR03-django-aplicacoes-python.json) |
| PR06 | Programação | Desenvolva jogos com Unity | [formacao-desenvolvendo-jogos-2d-unity](https://www.alura.com.br/formacao-desenvolvendo-jogos-2d-unity) | 24h | 2 | ✅ [`cursos/PR06-jogos-unity.json`](cursos/PR06-jogos-unity.json) |
| PR12 | Programação | Boas práticas em Python | [formacao-boas-praticas-python](https://www.alura.com.br/formacao-boas-praticas-python) | 24h | 3 | ✅ [`cursos/PR12-boas-praticas-python.json`](cursos/PR12-boas-praticas-python.json) |
| FE01 | Front-end | HTML e CSS para projetos web | [formacao-html-css](https://www.alura.com.br/formacao-html-css) | 54h | 4 | ✅ [`cursos/FE01-html-css-projetos-web.json`](cursos/FE01-html-css-projetos-web.json) |
| FE03 | Front-end | Desenvolvimento Front-end: criar aplicações web com HTML, CSS e JavaScript | [formacao-front-end](https://www.alura.com.br/formacao-front-end) | 60h | 8 | ✅ [`cursos/FE03-front-end-javascript.json`](cursos/FE03-front-end-javascript.json) |
| UX02 | UX & Design | Game Design | [formacao-game-design](https://www.alura.com.br/formacao-game-design) | 32h | 4 | ✅ [`cursos/UX02-game-design.json`](cursos/UX02-game-design.json) |
| UX03 | UX & Design | Blender | [formacao-blender](https://www.alura.com.br/formacao-blender) | 40h | 5 | ✅ [`cursos/UX03-blender.json`](cursos/UX03-blender.json) |

✅ = matriz de aprendizagem e prompt prontos · ⬜ = pendente

Todas as 9 trilhas da planilha atual têm matriz e prompt — **39 cursos, 329 horas** no total.

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
| PR03 | Django: crie aplicações em Python | Django: crie aplicações em Python |
| PR06 | Desenvolva jogos com Unity | Desenvolva jogos com Unity (URL: `formacao-desenvolvendo-jogos-2d-unity`) |
| PR12 | Boas práticas em Python | Boas práticas em Python |
| FE01 | (A partir do zero:) HTML e CSS para projetos web | HTML e CSS: do zero ao layout responsivo |
| FE03 | Desenvolvimento Front-end: criar aplicações web com HTML, CSS e JavaScript | Desenvolvimento Front-end: **cursos para** criar aplicações web com HTML, CSS e JavaScript |
| UX02 | Game Design | Game Design |
| UX03 | Blender | Blender |

## Pontos para a equipe ITT confirmar

Levantados na coleta de 2026-10-21, ao montar as seis matrizes restantes:

| ID | Ponto | Por que importa |
|----|-------|-----------------|
| PR03 | A Alura classifica a formação Django na escola **Back-end**; a planilha ITT a põe em **Programação**. Mantivemos a escola da planilha. | Só afeta a organização interna, não o conteúdo da matriz. |
| PR03 | Os cursos 4 e 5 (OAuth 2.0 e CRUD no S3) são declarados pela Alura para público **profissional** e tratam de infraestrutura AWS. | A matriz cobra só o conceito desses dois (peso somado 0.22) e deixa a operação da AWS fora de escopo. Confirmar se a ITT aplica a trilha inteira. |
| PR06 | As páginas individuais dos dois cursos de Unity **não estão publicadas** — redirecionam para a home da Alura. | Sem ementa publicada, os módulos vieram da descrição das etapas na página da formação e a carga de 12h por curso é a divisão do total de 24h. Reconferir quando publicarem. |
| PR12 | Os três cursos são declarados para nível **intermediário**, e o de PEP 8 pressupõe familiaridade com FastAPI. | A matriz cobra boas práticas, SOLID, padrões e testes em contextos do nível de PR02, e mantém FastAPI fora de escopo. |
| UX02 | Os cursos 2, 3 e 4 são declarados para **profissionais da área** com projeto em andamento; o 4 trata de monetização e captação. | A matriz cobra raciocínio de design e de produto, não prática de mercado. |
| UX02 / UX03 | Trilhas **sem programação**: o tipo de item `analise_codigo` não se aplica. | Os blueprints usam só `multipla_escolha` e `dissertativa`, e o roteiro do prompt troca a coluna "Com código" por "Com estímulo". |
