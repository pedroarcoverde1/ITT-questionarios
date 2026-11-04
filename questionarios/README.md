# Questionários montados

Os 20 itens de cada trilha, escritos por extenso: enunciado, alternativas, gabarito e o
motivo de cada alternativa errada. **180 itens** no total, **59** deles com trecho de código
(ou, nas trilhas sem programação, com estímulo em texto).

São a referência do que pedir à plataforma. Três usos:

1. **Comparar.** Monte o questionário na plataforma seguindo `prompts/<ID>.md` e compare item
   a item com o daqui. Onde o gerado estiver mais fraco, troque.
2. **Colar como exemplo.** Se a plataforma devolver itens rasos, cole dois ou três itens
   daqui no prompt como amostra de calibragem e peça de novo.
3. **Aplicar como está.** Os itens são completos e corrigíveis — gabarito nos objetivos,
   rubrica de três pontos nas dissertativas.

| ID | Trilha | Itens | Com código / estímulo | Arquivo |
|----|--------|:-----:|:---------------------:|---------|
| PR01 | A partir do zero: iniciante em programação | 20 | 6 | [PR01.md](PR01.md) |
| PR02 | Python com Orientação a Objetos | 20 | 7 | [PR02.md](PR02.md) |
| PR03 | Django: crie aplicações em Python | 20 | 7 | [PR03.md](PR03.md) |
| PR06 | Desenvolva jogos com Unity | 20 | 5 | [PR06.md](PR06.md) |
| PR12 | Boas práticas em Python | 20 | 8 | [PR12.md](PR12.md) |
| FE01 | HTML e CSS para projetos web | 20 | 6 | [FE01.md](FE01.md) |
| FE03 | Front-end com JavaScript | 20 | 8 | [FE03.md](FE03.md) |
| UX02 | Game Design | 20 | 6 *(estímulo)* | [UX02.md](UX02.md) |
| UX03 | Blender | 20 | 6 *(estímulo)* | [UX03.md](UX03.md) |

## Como cada item foi construído

- **A ordem dos itens é a ordem das linhas do roteiro** da seção 3 do prompt. O item 1 do
  arquivo corresponde à primeira linha da tabela, e assim por diante.
- **Toda alternativa errada sai de um `erros_comuns`** da competência na matriz — nenhuma é
  aleatória. Cada item traz, abaixo do gabarito, o motivo de cada distrator.
- **Quatro alternativas** nos itens de múltipla escolha, **cinco** nos de múltipla resposta.
- **O gabarito é sempre a alternativa A**, para a coordenação revisar rápido. **Embaralhe
  antes de aplicar.**
- **As dissertativas trazem rubrica** de três pontos, com as faixas integral / parcial / nulo.
- **Os trechos de código Python e JavaScript foram executados** antes de entrar aqui: a saída
  afirmada no gabarito é a saída real. Os de C# (PR06) e os de template Django não são
  executáveis fora do seu ambiente e foram conferidos à mão.
- **Trilhas sem programação** (UX02 e UX03) não têm itens com código: no lugar deles vêm
  itens com **estímulo** — um trecho de GDD, uma cena, uma lista de funcionalidades, uma
  situação de modelagem. Nenhum item depende de o estudante ver uma imagem.

## Correção

Cada item objetivo vale 1 ponto; múltipla resposta só pontua com o conjunto exato.
Dissertativa vale 1 (integral), 0,5 (parcial) ou 0, pela rubrica do próprio item.
Converta os 20 pontos em porcentagem e compare com `rubrica_proficiencia` da matriz da
trilha. O mínimo esperado em todas elas é a faixa **adequado (70–84%)** — 14 pontos.

## Validação

```bash
python3 ../scripts/validar.py
```

Além do que já checava, o validador confere cada arquivo daqui contra o roteiro do prompt
correspondente: numeração sequencial de 1 a 20, itens por tipo, itens por competência,
contagem de itens com código ou estímulo, presença de gabarito em cada item objetivo e de
rubrica em cada dissertativa, e a tabela "Gabarito resumido" conferindo com o cabeçalho de
cada item.

> Os itens com código de FE03, PR02 e PR03 também estão em
> [`../questoes/`](../questoes/), com o comentário dos distratores mais detalhado. O texto
> dos itens é o mesmo nos dois lugares.
