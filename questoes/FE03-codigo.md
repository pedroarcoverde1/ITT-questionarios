# FE03 · Itens com trecho de código

> Trilha: **Desenvolvimento Front-end com JavaScript** — matriz em
> [`cursos/FE03-front-end-javascript.json`](../cursos/FE03-front-end-javascript.json),
> prompt em [`prompts/FE03.md`](../prompts/FE03.md).
>
> São os **8 itens da coluna "Com código"** do roteiro de montagem (os `analise_codigo` da
> matriz). Servem como referência de calibragem: ou se usam como estão, ou se colam como
> exemplo no gerador quando o item que ele devolveu veio fraco demais.
>
> Toda alternativa errada sai de um `erros_comuns` da competência — nenhuma é aleatória.
> Os trechos foram executados antes de entrar aqui; a saída descrita é a saída real.

---

## FE03-COD-01 · C1 Integrar JavaScript à página e selecionar elementos

*Análise de código · analisar · erro comum: rodar o script antes de a página carregar*

O arquivo `app.js` deveria trocar o título da lista de tarefas, mas o console do navegador
acusa `Uncaught TypeError: Cannot set properties of null`. Qual é a causa?

```html
<!-- index.html -->
<head>
  <script src="app.js"></script>
</head>
<body>
  <h1 class="titulo">Minhas tarefas</h1>
</body>
```

```js
// app.js
const titulo = document.querySelector('.titulo');
titulo.textContent = 'Tarefas de hoje';
```

- **A)** O script foi carregado no `<head>` e rodou antes de o `<h1>` existir no DOM, então
  `querySelector` devolveu `null`.
- **B)** `querySelector` não aceita seletor de classe; para classes é preciso usar
  `getElementsByClassName`.
- **C)** `textContent` não existe em um `<h1>`; o certo nesse caso é `value`.
- **D)** A alteração não pode ser feita por script: só vale o que estiver salvo no arquivo
  `index.html`.

**Gabarito: A.** Mover o `<script>` para o fim do `<body>`, ou usar `defer`, resolve.
**B** confunde a família de seletores; **C** confunde `textContent` com `value`, que é de
campo de formulário; **D** é a ideia de que mexer no DOM mexe no arquivo em disco.

---

## FE03-COD-02 · C2 Reagir a eventos da pessoa usuária

*Análise de código · analisar · erro comum: executar a função no registro do ouvinte*

Ao abrir a página do temporizador, a mensagem `contagem iniciada` aparece no console sem
ninguém ter clicado — e clicar no botão não faz mais nada. Por quê?

```js
const botao = document.querySelector('#iniciar');
let segundos = 0;

function iniciarContagem() {
  segundos = 25 * 60;
  console.log('contagem iniciada');
}

botao.addEventListener('click', iniciarContagem());
```

- **A)** Os parênteses em `iniciarContagem()` executaram a função na hora do registro, e o
  que virou ouvinte foi o `undefined` que ela devolveu.
- **B)** Falta `preventDefault()` dentro da função, então o navegador recarrega a página e
  perde o clique.
- **C)** O botão ainda não existia quando o ouvinte foi registrado, então o clique não
  encontra a função.
- **D)** O ouvinte foi registrado duas vezes, por isso a função dispara sozinha uma vez.

**Gabarito: A.** O certo é passar a referência: `addEventListener('click', iniciarContagem)`.
**B** aplica `preventDefault` fora do lugar (ele é para `submit`); **C** descreveria um erro
na linha do `querySelector`, não a mensagem observada; **D** é o erro de ouvinte duplicado,
que causaria ação em duplicidade *depois* do clique, não antes.

---

## FE03-COD-03 · C3 Criar, alterar e remover elementos no DOM

*Análise de código · aplicar · erro comum: criar o elemento e esquecer de anexá-lo*

A função roda sem nenhum erro no console, mas nada aparece na lista da página. Qual
correção faz a tarefa aparecer?

```js
const lista = document.querySelector('#lista-tarefas');

function adicionarTarefa(texto) {
  const item = document.createElement('li');
  item.textContent = texto;
  item.classList.add('tarefa');
}

adicionarTarefa('Estudar JavaScript');
```

- **A)** Acrescentar `lista.append(item)` no fim da função: o `<li>` foi criado em memória,
  mas nunca anexado ao DOM.
- **B)** Trocar `textContent` por `innerHTML`, porque `textContent` não escreve dentro do
  `<li>`.
- **C)** Trocar `classList.add('tarefa')` por `item.style.display = 'block'`, porque a
  classe está escondendo o elemento.
- **D)** Declarar `const item` fora da função: variáveis criadas dentro dela são descartadas
  no fim da execução e o `<li>` não chega à página.

**Gabarito: A.** `createElement` cria; só `append` (ou `appendChild`) insere.
**B** confunde o papel de `textContent`; **C** troca classe por estilo inline sem motivo;
**D** é a confusão entre escopo da variável e presença do elemento no DOM.

---

## FE03-COD-04 · C3 Criar, alterar e remover elementos no DOM

*Análise de código · analisar · erro comum: confundir `textContent` com `value`*

A pessoa digita "Ler um livro" e clica em **Salvar**. O parágrafo de aviso continua vazio na
tela. O que está errado?

```html
<input id="nome-tarefa" type="text">
<button id="salvar">Salvar</button>
<p id="aviso"></p>
```

```js
const campo = document.querySelector('#nome-tarefa');
const aviso = document.querySelector('#aviso');

document.querySelector('#salvar').addEventListener('click', () => {
  aviso.value = 'Tarefa salva: ' + campo.textContent;
});
```

- **A)** As duas propriedades estão trocadas: o texto digitado está em `campo.value`, e o
  parágrafo recebe texto por `aviso.textContent`.
- **B)** O `<input>` precisa estar dentro de um `<form>`; fora dele o valor digitado não é
  guardado.
- **C)** Falta `preventDefault()` no clique: sem ele a página recarrega e limpa o parágrafo.
- **D)** A alteração acontece só no DOM; para aparecer na tela o arquivo HTML precisaria ser
  salvo com o novo texto.

**Gabarito: A.** `value` é de campo de formulário; `textContent` é do conteúdo de texto de
um elemento comum.
**B** inventa uma exigência; **C** usa `preventDefault` onde não há envio de formulário;
**D** é a ideia de que o DOM é o arquivo.

---

## FE03-COD-05 · C4 Processar coleções com os métodos de array

*Análise de código · aplicar · erro comum: esperar que `forEach` devolva um novo array*

O objetivo é obter um array só com os livros disponíveis. O que aparece no console e qual é
a correção?

```js
const livros = [
  { titulo: 'Duna', preco: 60, disponivel: true },
  { titulo: 'Fundação', preco: 45, disponivel: false },
  { titulo: 'Neuromancer', preco: 52, disponivel: true },
];

const resultado = livros.forEach((livro) => livro.disponivel);
console.log(resultado);
```

- **A)** `undefined` — `forEach` percorre mas não devolve nada; o método para selecionar
  itens é `filter`.
- **B)** `[true, false, true]` — `forEach` devolve o resultado do callback; para obter os
  objetos bastaria trocar por `map`.
- **C)** Os dois livros disponíveis — o código já faz o que se pretende.
- **D)** Um erro, porque o callback de `forEach` precisa de `return` explícito.

**Gabarito: A.**
**B** é a confusão entre `forEach` e `map` (e `map` também não filtraria); **C** supõe que
devolver `true` no callback seleciona o item; **D** confunde ausência de retorno com erro.

---

## FE03-COD-06 · C4 Processar coleções com os métodos de array

*Análise de código · aplicar · evidência: prever o valor devolvido por um `reduce`*

Qual valor o `console.log` imprime?

```js
const carrinho = [
  { nome: 'camiseta', preco: 50, qtd: 2 },
  { nome: 'boné', preco: 30, qtd: 1 },
  { nome: 'meia', preco: 10, qtd: 3 },
];

const total = carrinho.reduce((soma, item) => soma + item.preco * item.qtd, 0);
console.log(total);
```

- **A)** `160`
- **B)** `90`
- **C)** `3`
- **D)** `undefined`, porque falta `return` dentro do callback do `reduce`.

**Gabarito: A.** 50×2 + 30×1 + 10×3 = 160.
**B** soma só os preços, ignorando `qtd`; **C** conta os itens da coleção em vez de acumular;
**D** é o erro do `return` esquecido — aqui a arrow de uma linha já devolve o valor.

---

## FE03-COD-07 · C5 Lidar com código assíncrono

*Análise de código · analisar · erro comum: achar que `setTimeout` de 0 ms executa na hora*

Em que ordem as três mensagens aparecem no console?

```js
console.log('1 - começou o Pomodoro');

setTimeout(() => {
  console.log('2 - fim do bloco de estudo');
}, 0);

console.log('3 - cronômetro na tela');
```

- **A)** 1, 3, 2
- **B)** 1, 2, 3
- **C)** Só 1 e 3: com 0 ms o navegador descarta o `setTimeout`.
- **D)** 2, 1, 3

**Gabarito: A.** Mesmo com 0 ms, o callback só é chamado depois que o código síncrono termina.
**B** é a ideia de execução imediata; **C** supõe que o atraso zero cancela o agendamento;
**D** supõe que o que é agendado roda primeiro.

---

## FE03-COD-08 · C6 Consumir uma API com fetch e implementar o CRUD

*Análise de código · analisar · erro comum: esquecer o `.json()` da resposta*

A função deveria listar os pensamentos do mural, mas o console acusa
`pensamentos.forEach is not a function`. Qual é a correção?

```js
async function carregarPensamentos() {
  const resposta = await fetch('http://localhost:3000/pensamentos');
  const pensamentos = resposta;
  pensamentos.forEach((p) => console.log(p.conteudo));
}
```

- **A)** Converter o corpo da resposta: `const pensamentos = await resposta.json();`.
- **B)** Acrescentar `await` antes do `forEach`, porque a lista ainda é uma promise pendente.
- **C)** Trocar `await fetch(...)` por `fetch(...).then(...)`: `fetch` não funciona com
  `await`.
- **D)** Trocar o método da requisição para `POST`, porque é ela que vai buscar os dados no
  servidor.

**Gabarito: A.** `fetch` devolve um objeto `Response`; os dados saem de `.json()`.
**B** confunde o objeto `Response` com uma promise não resolvida; **C** nega que `fetch`
devolva promise; **D** troca `GET` por `POST`.

---

## Resumo

| Item | Competência | Foco | Gabarito |
|------|-------------|------|:--------:|
| FE03-COD-01 | C1 | script no `<head>` e seletor devolvendo `null` | A |
| FE03-COD-02 | C2 | referência da função vs chamada no registro | A |
| FE03-COD-03 | C3 | `createElement` sem `append` | A |
| FE03-COD-04 | C3 | `textContent` vs `value` | A |
| FE03-COD-05 | C4 | `forEach` não devolve array; usar `filter` | A |
| FE03-COD-06 | C4 | saída de um `reduce` que acumula preço × quantidade | A |
| FE03-COD-07 | C5 | ordem de execução com `setTimeout` de 0 ms | A |
| FE03-COD-08 | C6 | `.json()` entre a resposta e os dados | A |

Fecha com a coluna "Com código" do roteiro de `prompts/FE03.md`: **8 itens**, distribuídos
C1 ×1, C2 ×1, C3 ×2, C4 ×2, C5 ×1, C6 ×1.

> **Antes de aplicar**: embaralhe a posição da alternativa correta. Aqui o gabarito é sempre
> **A** só para facilitar a revisão pela coordenação.
