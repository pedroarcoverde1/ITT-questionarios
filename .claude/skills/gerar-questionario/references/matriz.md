# Matriz de aprendizagem — como montar cada campo

O formato completo está em `esquema/matriz.schema.json`; as regras de consistência que o
schema não expressa estão em `scripts/validar.py`. Este guia diz **como decidir** o conteúdo.

## O que vem da ementa e o que é da ITT

| Vem da ementa (fato, não inventar) | É elaboração pedagógica da ITT (você propõe) |
|------------------------------------|----------------------------------------------|
| títulos, URLs, carga horária, nº de cursos | competências e seu agrupamento |
| módulos de cada curso | pesos e itens por competência |
| bullets "o que você vai aprender" | evidências observáveis |
| conceitos citados | erros comuns (viram distratores) |
| público e pré-requisitos declarados | rubrica e faixas de proficiência |
| | `fora_de_escopo` de cada curso |

## Esqueleto

```json
{
  "id_itt": "PR06",
  "escola": "Programação",
  "trilha": {
    "titulo_itt": "<nome na planilha da ITT>",
    "titulo_alura": "<nome atual na fonte; igual ao anterior se não houver divergência>",
    "url": "<URL da ementa>",
    "carga_horaria_h": 24,
    "n_cursos": 2,
    "publico_alvo": "Adolescentes do ensino fundamental II e médio atendidos pela ITT, ...",
    "pre_requisitos": [],
    "projeto_fio_condutor": "<o projeto que atravessa a trilha>"
  },
  "competencias": [ ... ],
  "cursos": [ ... ],
  "rubrica_proficiencia": { ... },
  "blueprint_questionario": { ... },
  "prompt": "prompts/PR06.md",
  "metadados": {
    "versao": "1.0",
    "data_extracao": "<AAAA-MM-DD de hoje>",
    "fontes": ["<URLs ou arquivos da ementa>"],
    "derivado_de": "<de onde saiu cada dado factual e o que foi suposto>"
  }
}
```

- `pre_requisitos` lista **IDs de outras trilhas ITT** (ex.: PR02 exige `["PR01"]`), não
  conhecimentos.
- `publico_alvo` descreve o público **da ITT**, não o da fonte. Se a fonte declara público
  profissional ou intermediário, diga isso no `publico_alvo`, calibre os contextos ao nível
  da ITT e registre o ajuste em `rubrica_proficiencia.observacao`.
- Slug do arquivo: kebab-case curto sem acento, ex. `PR06-jogos-unity.json`.

## Cursos

```json
{
  "id": "PR06.01",
  "titulo": "...",
  "url": "...",
  "carga_horaria_h": 12,
  "n_atividades": null,
  "atualizado_em": null,
  "etapa_da_trilha": "<nome do passo da trilha, se houver>",
  "modulos": ["<um por módulo da ementa>"],
  "conceitos_chave": ["<10 a 16 termos que a trilha ensina>"],
  "objetivos_de_aprendizagem": [
    { "id": "PR06.01.O1", "enunciado": "<verbo no infinitivo + objeto>", "nivel_bloom": "aplicar", "competencia": "PR06.C1" }
  ],
  "fora_de_escopo": ["<5 itens>"]
}
```

- A soma de `carga_horaria_h` dos cursos tem de fechar com a da trilha. Sem carga por
  curso na ementa, divida o total e diga isso em `derivado_de`.
- **Objetivos**: 5 a 10 por curso — numa trilha de um curso só, 7 a 10, para que cada
  competência receba pelo menos um —, cada um com um verbo observável ("Escrever", "Configurar",
  "Distinguir", "Diagnosticar"), não "Conhecer" ou "Entender sobre". Cada objetivo aponta
  para exatamente uma competência.
- **fora_de_escopo**: o que é vizinho e plausível de cair numa prova genérica do assunto,
  mas a trilha não ensina (ex.: Unity → jogos 3D, multiplayer, shaders). É a cerca que impede
  a plataforma de cobrar o que não foi ensinado — seja específico. Cerca de 5 por curso;
  numa trilha de um curso só, 6 a 10, porque essa lista é a cerca da trilha inteira.

## Competências

```json
{
  "id": "PR06.C4",
  "titulo": "<verbo no infinitivo: o que o estudante faz>",
  "descricao": "<1–2 frases>",
  "nivel_bloom": "aplicar",
  "peso": 0.15,
  "itens_alvo": 3,
  "cursos_origem": ["PR06.01"],
  "evidencias_observaveis": ["<3 itens>"],
  "erros_comuns": ["<4 itens>"],
  "tipos_de_item": ["multipla_escolha", "analise_codigo", "dissertativa"]
}
```

- **7 ou 8 competências** por trilha. Toda competência precisa de pelo menos um objetivo
  apontando para ela (senão é "órfã").
- **Evidências observáveis** são situações-tarefa que viram enunciado: "Dado X, aponta Y",
  "Distingue A de B", "Prevê o efeito de um trecho que…", "Explica por que…". Três por
  competência, de níveis diferentes.
- **Erros comuns** são concepções equivocadas concretas de quem entendeu em parte — viram as
  alternativas erradas. Bom: "Esperar gravidade sem adicionar Rigidbody2D". Ruim: "Não
  entender física". Quatro por competência.
- `tipos_de_item`: inclua `analise_codigo` só em trilha de programação e onde a competência
  se avalia lendo código; inclua `dissertativa` nas competências que vão receber as 2
  dissertativas do blueprint.
- `nivel_bloom` da competência: o nível mais alto que a avaliação cobra dela
  (`entender`, `aplicar`, `analisar`, `avaliar`). Normalmente uma a duas em `entender`, a
  maioria em `aplicar`, uma a duas em `analisar`/`avaliar`.

## Pesos e itens

- Pesos entre 0.07 e 0.20, soma **exatamente 1.0** (o validador tolera 0.001).
- `itens_alvo` ≈ `peso × 20`, arredondado, ajustado para a soma dar 20. Referência:
  0.07–0.09 → 1 ou 2; 0.10–0.12 → 2; 0.13–0.17 → 3; 0.18–0.20 → 4.
- Peso maior para o núcleo da trilha (o que a rubrica "adequado" descreve), menor para
  ambientação de ferramenta e para tópicos de fim de trilha vistos de passagem.

## Blueprint

Números das 9 trilhas existentes — fique dentro dessas faixas salvo motivo explícito:

| Campo | Programação | Sem programação |
|-------|-------------|-----------------|
| `n_itens_total` | 20 | 20 |
| `tempo_estimado_min` | 40–45 | 40 |
| `por_tipo.dissertativa` | 2 | 2 |
| `por_tipo.analise_codigo` | 5–8 | não usar a chave |
| `por_tipo.multipla_escolha` | o resto (10–13) | 18 |
| `por_bloom.lembrar_entender` | 4–7 | 6–7 |
| `por_bloom.aplicar` | 10–11 | 9 |
| `por_bloom.analisar_avaliar` | 3–6 | 4–5 |

`por_competencia`, `por_tipo` e `por_bloom` somam 20 cada; `por_competencia` repete os
`itens_alvo` de cada competência.

**Como chegar ao `por_bloom`**: classifique mentalmente os 20 itens que o roteiro vai
pedir. Itens de "distinguir", "reconhecer" e "o que é" contam como `lembrar_entender`;
"dado X, escrever/escolher/prever" conta como `aplicar`; as 2 dissertativas, os
diagnósticos ("por que o código não funciona") e as escolhas justificadas contam como
`analisar_avaliar`. Uma competência em `entender` contribui quase só com compreensão; uma em
`analisar` contribui com pelo menos um item de análise.

## Rubrica

Faixas fixas da ITT; os descritores são específicos da trilha e crescem em autonomia:

```json
"rubrica_proficiencia": {
  "faixas": [
    { "nivel": "iniciante", "min_pct": 0,  "max_pct": 49,  "descritor": "<reconhece termos, não aplica>" },
    { "nivel": "basico",    "min_pct": 50, "max_pct": 69,  "descritor": "<segue modelo pronto; erros típicos X e Y>" },
    { "nivel": "adequado",  "min_pct": 70, "max_pct": 84,  "descritor": "<faz sozinho o núcleo da trilha>" },
    { "nivel": "avancado",  "min_pct": 85, "max_pct": 100, "descritor": "<diagnostica, justifica escolhas, fecha o projeto>" }
  ],
  "nivel_minimo_esperado": "adequado",
  "observacao": "Faixas definidas pela coordenação ITT, não extraídas da Alura. Revisar após o primeiro ciclo de aplicação."
}
```

Acrescente à `observacao` qualquer ajuste de público (fonte para profissionais, etc.).
Se a fonte não é a Alura, troque "da Alura" pelo nome dela ou por "da plataforma do curso".
