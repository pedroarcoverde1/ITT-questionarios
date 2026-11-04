# PR02 · Itens com trecho de código

> Trilha: **Aprenda a programar em Python com Orientação a Objetos** — matriz em
> [`cursos/PR02-python-orientacao-objetos.json`](../cursos/PR02-python-orientacao-objetos.json),
> prompt em [`prompts/PR02.md`](../prompts/PR02.md).
>
> São os **7 itens da coluna "Com código"** do roteiro de montagem (os `analise_codigo` da
> matriz). Servem como referência de calibragem: ou se usam como estão, ou se colam como
> exemplo no gerador quando o item que ele devolveu veio fraco demais.
>
> Toda alternativa errada sai de um `erros_comuns` da competência — nenhuma é aleatória.
> Os trechos foram executados em Python 3 antes de entrar aqui; a saída descrita é a real.

---

## PR02-COD-01 · C2 Condicionais, laços e tratamento de exceções

*Análise de código · aplicar · erro comum: erro de 1 na contagem do `range()`*

Qual é a saída do programa?

```python
notas = [8, 6, 10, 7]
soma = 0

for i in range(1, len(notas)):
    soma += notas[i]

print(soma)
```

- **A)** `23`
- **B)** `31`
- **C)** `21`
- **D)** `IndexError`, porque `range(1, len(notas))` chega ao índice 4.

**Gabarito: A.** O laço vai de 1 a 3, pulando a primeira nota: 6 + 10 + 7 = 23.
**B** soma as quatro notas, supondo que o laço começa em 0; **C** supõe que o `range` pula o
último índice em vez do primeiro; **D** acha que o fim do `range` é inclusivo.

---

## PR02-COD-02 · C3 Listas e dicionários

*Análise de código · aplicar · erro comum: achar que a lista começa no índice 1*

Qual é a saída do programa?

```python
restaurantes = [
    {'nome': 'Pizza da Esquina', 'categoria': 'Italiana', 'ativo': True},
    {'nome': 'Sushi do Bairro', 'categoria': 'Japonesa', 'ativo': False},
]

print(restaurantes[1]['categoria'])
```

- **A)** `Japonesa`
- **B)** `Italiana`
- **C)** `KeyError: 'categoria'`, porque o acesso correto seria `restaurantes[1].categoria`.
- **D)** Um erro: é preciso percorrer a lista com `for` antes de acessar qualquer
  dicionário dela.

**Gabarito: A.** O índice 1 é o segundo dicionário da lista, e a chave `'categoria'` dele
vale `'Japonesa'`.
**B** conta a lista a partir de 1; **C** usa sintaxe de atributo onde o dicionário pede
chave entre colchetes; **D** supõe que não se pode indexar direto.

---

## PR02-COD-03 · C4 Funções e módulos

*Análise de código · analisar · erro comum: usar `print()` no lugar de `return`*

Qual é a saída completa do programa?

```python
def calcular_media(notas):
    media = sum(notas) / len(notas)
    print(media)

resultado = calcular_media([8, 6, 10])
print(f'A média é {resultado}')
```

- **A)** `8.0` e, na linha seguinte, `A média é None`.
- **B)** `8.0` e, na linha seguinte, `A média é 8.0`.
- **C)** Apenas `A média é 8.0`.
- **D)** Um erro: uma função que usa `print()` não pode ter o retorno atribuído a uma
  variável.

**Gabarito: A.** A função mostra o valor na tela, mas não o devolve; sem `return media`, a
variável `resultado` recebe `None`.
**B** confunde imprimir com devolver; **C** ignora o `print` de dentro da função;
**D** inventa uma restrição da linguagem.

---

## PR02-COD-04 · C5 Classes, atributos de instância e construtor

*Análise de código · analisar · erro comum: esquecer o `self` na atribuição do construtor*

Qual é a saída do programa?

```python
class Jogo:
    def __init__(self, nome, nota):
        nome = nome
        self.nota = nota

jogo = Jogo('Celeste', 9.5)
print(jogo.nome)
```

- **A)** `AttributeError: 'Jogo' object has no attribute 'nome'`, porque `nome = nome`
  criou uma variável local em vez de um atributo do objeto.
- **B)** `Celeste`
- **C)** `None`
- **D)** Um erro, porque o construtor precisa ser chamado explicitamente:
  `jogo.__init__('Celeste', 9.5)`.

**Gabarito: A.** O certo é `self.nome = nome`: sem o `self`, o valor morre no fim do
`__init__`.
**B** supõe que o parâmetro vira atributo sozinho; **C** supõe que o atributo existe vazio;
**D** é o erro de chamar `__init__` na mão — `Jogo(...)` já o chama.

---

## PR02-COD-05 · C5 Classes, atributos de instância e construtor

*Análise de código · avaliar · erro comum: confundir atributo de classe com atributo de instância*

O que o programa imprime, e por quê?

```python
class Playlist:
    musicas = []

    def __init__(self, nome):
        self.nome = nome

    def adicionar(self, musica):
        self.musicas.append(musica)

rock = Playlist('Rock')
mpb = Playlist('MPB')
rock.adicionar('Smells Like Teen Spirit')

print(len(mpb.musicas))
```

- **A)** `1`, porque `musicas` foi declarada no corpo da classe e as duas playlists
  compartilham a mesma lista; para cada objeto ter a sua, ela precisa ser criada dentro do
  `__init__`.
- **B)** `0`, porque cada objeto criado recebe a sua própria lista vazia.
- **C)** `AttributeError`, porque `mpb` nunca chamou `adicionar` e por isso não tem o
  atributo `musicas`.
- **D)** `1`, porque `append()` sempre grava na classe, mesmo quando a lista é criada
  dentro do `__init__`.

**Gabarito: A.**
**B** é a suposição de que o atributo de classe é copiado para cada instância; **C** confunde
chamar o método com criar o atributo; **D** acerta o número por um motivo falso — se a lista
nascesse no `__init__`, cada objeto teria a sua e a saída seria `0`.

---

## PR02-COD-06 · C6 Encapsulamento com property e métodos de classe e estáticos

*Análise de código · analisar · erro comum: chamar a property com parênteses*

Qual é a saída do programa?

```python
class Restaurante:
    def __init__(self, nome, nota):
        self.nome = nome
        self._nota = nota

    @property
    def nota(self):
        return f'{self._nota:.1f}'

bistro = Restaurante('Bistrô', 9)
print(bistro.nota())
```

- **A)** `TypeError: 'str' object is not callable` — `nota` é uma property, lida como
  atributo: o certo é `bistro.nota`, sem parênteses.
- **B)** `9.0`
- **C)** O endereço do método em memória, algo como `<bound method Restaurante.nota>`.
- **D)** `AttributeError`, porque o underscore em `_nota` impede a leitura do valor fora da
  classe.

**Gabarito: A.** A property devolve a string `'9.0'`; os parênteses tentam chamar essa
string como se fosse função.
**B** ignora os parênteses; **C** trata a property como método não chamado; **D** supõe que o
underscore é uma trava da linguagem — ele é só convenção de uso interno.

---

## PR02-COD-07 · C7 Herança, polimorfismo e classes abstratas

*Análise de código · analisar · erro comum: esquecer `super().__init__()` na subclasse*

Qual é a saída do programa?

```python
class Midia:
    def __init__(self, titulo, ano):
        self.titulo = titulo
        self.ano = ano

class Filme(Midia):
    def __init__(self, titulo, ano, duracao):
        self.duracao = duracao

interestelar = Filme('Interestelar', 2014, 169)
print(interestelar.titulo)
```

- **A)** `AttributeError: 'Filme' object has no attribute 'titulo'`, porque `Filme`
  sobrescreveu o construtor e não chamou `super().__init__(titulo, ano)`.
- **B)** `Interestelar`, porque a herança copia os atributos da superclasse
  automaticamente.
- **C)** `None`, porque o atributo herdado existe, mas chega sem valor.
- **D)** Um erro de sintaxe: uma subclasse não pode ter `__init__` próprio, só métodos
  novos.

**Gabarito: A.** Herdar dá acesso ao construtor da superclasse, mas não o executa: quem
sobrescreve `__init__` precisa chamá-lo.
**B** e **C** supõem atributos herdados automaticamente (com e sem valor); **D** nega que se
possa sobrescrever o construtor.

---

## Resumo

| Item | Competência | Foco | Gabarito |
|------|-------------|------|:--------:|
| PR02-COD-01 | C2 | `range()` com fim exclusivo e início em 1 | A |
| PR02-COD-02 | C3 | valor aninhado em lista de dicionários | A |
| PR02-COD-03 | C4 | `print()` não substitui `return` | A |
| PR02-COD-04 | C5 | `self` na atribuição do construtor | A |
| PR02-COD-05 | C5 | atributo de classe compartilhado entre instâncias | A |
| PR02-COD-06 | C6 | property lida como atributo, sem parênteses | A |
| PR02-COD-07 | C7 | `super().__init__()` na subclasse | A |

Fecha com a coluna "Com código" do roteiro de `prompts/PR02.md`: **7 itens**, distribuídos
C2 ×1, C3 ×1, C4 ×1, C5 ×2, C6 ×1, C7 ×1.

> **Antes de aplicar**: embaralhe a posição da alternativa correta. Aqui o gabarito é sempre
> **A** só para facilitar a revisão pela coordenação.
