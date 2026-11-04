# PR03 · Itens com trecho de código

> Trilha: **Django: crie aplicações em Python** — matriz em
> [`cursos/PR03-django-aplicacoes-python.json`](../cursos/PR03-django-aplicacoes-python.json),
> prompt em [`prompts/PR03.md`](../prompts/PR03.md).
>
> São os **7 itens da coluna "Com código"** do roteiro de montagem (os `analise_codigo` da
> matriz). Servem como referência de calibragem: ou se usam como estão, ou se colam como
> exemplo no gerador quando o item que ele devolveu veio fraco demais.
>
> Toda alternativa errada sai de um `erros_comuns` da competência — nenhuma é aleatória.
> O contexto é o projeto fio condutor da trilha: a galeria de fotografias.

---

## PR03-COD-01 · C1 Projeto, app, rotas e configuração

*Análise de código · aplicar · evidência: dizer qual rota e qual view atendem a URL*

Com essas rotas, o que acontece quando o navegador pede `/imagem/7/`?

```python
# setup/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('galeria.urls')),
]
```

```python
# galeria/urls.py
from django.urls import path
from galeria.views import index, imagem

urlpatterns = [
    path('', index, name='index'),
    path('imagem/<int:foto_id>/', imagem, name='imagem'),
]
```

- **A)** A view `imagem` responde, recebendo `request` e `foto_id` com o valor inteiro `7`.
- **B)** A view `index` responde, porque o `path('')` casa com qualquer URL que chegue na
  app.
- **C)** Nenhuma view responde: a rota `imagem/<int:foto_id>/` também precisaria ser
  declarada em `setup/urls.py`.
- **D)** A view `imagem` responde, mas recebe `foto_id` como o texto `'7'`: `<int:...>`
  apenas verifica se o trecho é numérico.

**Gabarito: A.** O `include` repassa o resto do caminho para `galeria/urls.py`, e o
conversor `<int:...>` entrega o valor já convertido para `int`.
**B** confunde rota vazia com rota coringa; **C** é a ideia de deixar todas as URLs no
arquivo do projeto, sem isolar por app; **D** reduz o conversor a uma validação.

---

## PR03-COD-02 · C2 Templates sem duplicação

*Análise de código · analisar · erro comum: confundir o nome no contexto com o nome no template*

A página `/` carrega sem erro nenhum, mas nenhuma fotografia aparece, mesmo havendo
registros no banco. Por quê?

```python
# galeria/views.py
def index(request):
    fotografias = Fotografia.objects.all()
    return render(request, 'galeria/index.html', {'cards': fotografias})
```

```django
{# galeria/index.html #}
{% for foto in fotografias %}
  <h2>{{ foto.nome }}</h2>
{% endfor %}
```

- **A)** O contexto publicou a lista sob o nome `cards`, e o template percorre
  `fotografias`, que não existe no contexto — o `for` não roda nenhuma vez.
- **B)** Falta `{% load static %}` no topo do template.
- **C)** `objects.all()` só funciona dentro do Admin; em uma view é preciso usar `filter()`.
- **D)** O contexto precisa receber uma lista, não um QuerySet: sem `list(fotografias)` o
  `for` do template não percorre nada.

**Gabarito: A.** No template vale o nome da **chave** do contexto, não o da variável da
view: ou se percorre `cards`, ou se publica a chave como `fotografias`.
**B** trata de arquivos estáticos, não do contexto; **C** inventa uma restrição do ORM;
**D** supõe que o template não itera QuerySet — ele itera.

---

## PR03-COD-03 · C3 Models e migrações

*Análise de código · avaliar · erro comum: usar `CharField` para tudo*

Neste model, dois campos estão com o tipo errado para o dado que guardam. Quais são, e o
que deveria ser usado?

```python
class Fotografia(models.Model):
    nome = models.CharField(max_length=100)
    legenda = models.CharField(max_length=150)
    data_registro = models.CharField(max_length=20)
    foto = models.CharField(max_length=200)
```

- **A)** `data_registro`, que deveria ser `DateField`, e `foto`, que deveria ser
  `ImageField`.
- **B)** `nome`, que deveria ser `TextField`, e `legenda`, que deveria ser `CharField` sem
  `max_length`.
- **C)** Nenhum: `CharField` guarda qualquer dado, e o tipo só muda a aparência do campo na
  tela do Admin.
- **D)** `foto`, que deveria ser `URLField`, e `data_registro`, que deveria ser
  `IntegerField` com o número de segundos.

**Gabarito: A.** O tipo do campo define o que o banco aceita, como o Django valida o
formulário e, no caso de `ImageField`, o upload do arquivo para a pasta de mídia.
**B** troca campos que já estão corretos; **C** é exatamente o erro de usar `CharField` para
tudo; **D** guarda o endereço em vez do arquivo e joga a data para número.

---

## PR03-COD-04 · C3 Models e migrações

*Análise de código · aplicar · evidência: escrever o `filter()` que casa com o termo buscado*

A busca por `nebu` não encontra a fotografia chamada "Nebulosa de Órion", embora ela esteja
cadastrada. Qual correção resolve?

```python
def buscar(request):
    termo = request.GET.get('buscar')
    fotografias = Fotografia.objects.filter(nome=termo)
    return render(request, 'galeria/buscar.html', {'cards': fotografias})
```

- **A)** Usar `filter(nome__icontains=termo)`: `nome=termo` exige que o nome seja
  exatamente igual ao termo digitado.
- **B)** Percorrer `Fotografia.objects.all()` com um `for` e comparar `foto.nome == termo`
  dentro do laço.
- **C)** Trocar `filter` por `get`, que é o método que faz busca por parte do texto.
- **D)** Rodar `makemigrations` e `migrate`, porque o índice de busca do campo `nome` ainda
  não foi criado no banco.

**Gabarito: A.** `__icontains` busca por conteúdo parcial e sem diferenciar maiúsculas de
minúsculas.
**B** é o erro de comparar com `==` em vez de usar os filtros do ORM (e traria o banco todo
para a memória); **C** inverte o papel de `get`, que devolve um único registro e dá erro se
não achar; **D** confunde busca com estrutura de banco.

---

## PR03-COD-05 · C5 Formulários e validação

*Análise de código · analisar · erro comum: usar `cleaned_data` antes de `is_valid()`*

Ao enviar o formulário, a aplicação quebra com
`AttributeError: 'FotografiaForms' object has no attribute 'cleaned_data'`. Qual é a causa?

```python
def nova_foto(request):
    form = FotografiaForms(request.POST, request.FILES)
    nome = form.cleaned_data['nome']
    if form.is_valid():
        form.save()
    return redirect('index')
```

- **A)** `cleaned_data` só passa a existir depois de `is_valid()` rodar; a leitura precisa
  ir para dentro do `if`.
- **B)** Falta o `{% csrf_token %}` no template do formulário.
- **C)** O formulário não guarda os dados enviados: o nome tem de ser lido direto de
  `request.POST['nome']`.
- **D)** A validação do campo precisa estar em um método chamado `validar_nome()`; fora
  desse nome, o Django não preenche `cleaned_data`.

**Gabarito: A.** É `is_valid()` que roda as validações e monta `cleaned_data`.
**B** causaria erro 403 no envio, não esse `AttributeError`; **C** é o erro de ler
`request.POST` direto e salvar sem validar; **D** erra o padrão, que é `clean_<campo>`.

---

## PR03-COD-06 · C6 Autenticação e autorização

*Análise de código · avaliar · erro comum: proteger o link e deixar a URL acessível*

No template do menu, o link "Nova foto" aparece só para quem está logado. Mesmo assim,
qualquer visitante que digite `/nova-foto/` na barra de endereços abre a página. Qual
correção protege de verdade?

```python
# galeria/views.py
from django.shortcuts import render

def nova_foto(request):
    return render(request, 'galeria/nova_foto.html')
```

- **A)** Decorar a view com `@login_required`: esconder o link no template é aparência, não
  proteção — a URL continua respondendo a qualquer um.
- **B)** Remover o link do menu para todos os visitantes, inclusive os logados.
- **C)** Trocar a rota por um endereço difícil de adivinhar, como `/nova-foto-x9k2/`.
- **D)** Envolver o formulário em `{% if user.is_authenticated %}` dentro do template
  `nova_foto.html`.

**Gabarito: A.** A autorização tem de estar na view, que é quem decide se responde.
**B** piora a navegação sem proteger nada; **C** é segurança por obscuridade; **D** esconde
o formulário, mas a view segue aberta e um envio direto continuaria passando.

---

## PR03-COD-07 · C7 CRUD no fluxo MTV

*Análise de código · avaliar · erro comum: confundir a view de criar com a de editar*

Ao salvar a edição de uma fotografia, aparece uma fotografia **nova** na galeria e a
original continua igual; além disso, atualizar a página reenvia o formulário. Qual correção
resolve os dois problemas?

```python
def editar_foto(request, foto_id):
    fotografia = Fotografia.objects.get(pk=foto_id)
    form = FotografiaForms(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    return render(request, 'galeria/editar_foto.html', {'form': form})
```

- **A)** Passar o registro ao formulário com
  `FotografiaForms(request.POST, request.FILES, instance=fotografia)` e, depois de salvar,
  devolver `redirect('index')` em vez de `render`.
- **B)** Chamar `fotografia.save()` antes de `form.save()`, para que o Django saiba qual
  registro atualizar.
- **C)** Apagar o registro antigo com `fotografia.delete()` e deixar o `form.save()` criar
  o substituto.
- **D)** Trocar `get(pk=foto_id)` por `filter(pk=foto_id)`, porque `get` devolve uma cópia
  do registro, e não ele mesmo.

**Gabarito: A.** Sem `instance`, o formulário cria um registro novo; e responder a um POST
com `render` deixa a pessoa em uma página cujo recarregamento repete o envio — o padrão é
redirecionar.
**B** salva o registro inalterado e não muda o destino do `form.save()`; **C** perde o
histórico e o `pk` original; **D** confunde o retorno de `get` com o de `filter`, que é um
QuerySet.

---

## Resumo

| Item | Competência | Foco | Gabarito |
|------|-------------|------|:--------:|
| PR03-COD-01 | C1 | qual view atende a URL e o que recebe | A |
| PR03-COD-02 | C2 | nome da chave do contexto vs nome no template | A |
| PR03-COD-03 | C3 | tipo de campo adequado ao dado | A |
| PR03-COD-04 | C3 | `filter` com `__icontains` em vez de igualdade exata | A |
| PR03-COD-05 | C5 | `is_valid()` antes de `cleaned_data` | A |
| PR03-COD-06 | C6 | `@login_required` protege a URL, o template não | A |
| PR03-COD-07 | C7 | `instance=` na edição e `redirect` depois do POST | A |

Fecha com a coluna "Com código" do roteiro de `prompts/PR03.md`: **7 itens**, distribuídos
C1 ×1, C2 ×1, C3 ×2, C5 ×1, C6 ×1, C7 ×1.

> **Antes de aplicar**: embaralhe a posição da alternativa correta. Aqui o gabarito é sempre
> **A** só para facilitar a revisão pela coordenação.
