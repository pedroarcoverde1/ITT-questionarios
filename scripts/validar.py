#!/usr/bin/env python3
"""Valida a consistência interna das matrizes de aprendizagem.

Uso: python3 scripts/validar.py cursos/*.json
Sem argumentos, valida todos os arquivos de cursos/.
Só usa a biblioteca padrão (jsonschema não é dependência deste projeto).
"""
import json
import os
import re
import sys
from glob import glob

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOOM = {"lembrar", "entender", "aplicar", "analisar", "avaliar", "criar"}
TIPOS = {"multipla_escolha", "analise_codigo", "dissertativa"}
GRUPOS_BLOOM = {
    "lembrar_entender": {"lembrar", "entender"},
    "aplicar": {"aplicar"},
    "analisar_avaliar": {"analisar", "avaliar", "criar"},
}


def le_roteiro(d, caminho_prompt):
    """Lê a tabela da seção 3 do prompt.

    Devolve (secao, por_botao, por_comp, com_estimulo, erros). É a fonte que tanto o
    prompt quanto o questionário de `questionarios/` são comparados contra.
    """
    erros = []
    with open(caminho_prompt, encoding="utf-8") as f:
        md = f.read()
    if "## 3. Roteiro de montagem" not in md:
        return None, {}, {}, 0, ["prompt sem a seção '## 3. Roteiro de montagem'"]
    sec = md.split("## 3. Roteiro de montagem", 1)[1]

    por_botao, por_comp, com_estimulo = {}, {}, 0
    for linha in sec.splitlines():
        if not linha.startswith("|") or "Botão a selecionar" in linha:
            continue
        if re.match(r"^\|[\s:|-]+\|$", linha):
            continue
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        if len(celulas) < 4:
            erros.append(f"linha do roteiro com menos de 4 colunas: {linha.strip()}")
            continue
        try:
            qtd, estimulo = int(celulas[1]), int(celulas[3])
        except ValueError:
            erros.append(f"quantidade ou coluna de estímulo não numérica: {linha.strip()}")
            continue
        por_botao[celulas[2]] = por_botao.get(celulas[2], 0) + qtd
        com_estimulo += estimulo
        comp = f"{d['id_itt']}.{celulas[0].split()[0]}"
        por_comp[comp] = por_comp.get(comp, 0) + qtd

    return sec, por_botao, por_comp, com_estimulo, erros


def valida_roteiro(d, caminho_prompt):
    """Confere a seção 3 do prompt contra o blueprint da matriz.

    O prompt é o artefato que a coordenação usa na plataforma; se ele divergir do
    blueprint, o questionário montado não é o questionário planejado.
    """
    bp = d["blueprint_questionario"]
    sec, por_botao, por_comp, com_estimulo, erros = le_roteiro(d, caminho_prompt)
    if sec is None:
        return erros

    n = sum(por_botao.values())
    if n != bp["n_itens_total"]:
        erros.append(f"roteiro soma {n} itens, blueprint.n_itens_total = {bp['n_itens_total']}")

    objetivos_bp = sum(v for k, v in bp["por_tipo"].items() if k != "dissertativa")
    objetivos_rot = por_botao.get("Múltipla escolha", 0) + por_botao.get("Múltipla resposta", 0)
    if objetivos_rot != objetivos_bp:
        erros.append(f"roteiro tem {objetivos_rot} itens objetivos, blueprint tem {objetivos_bp}")

    diss_bp = bp["por_tipo"].get("dissertativa", 0)
    if por_botao.get("Dissertativa", 0) != diss_bp:
        erros.append(f"roteiro tem {por_botao.get('Dissertativa', 0)} dissertativas, blueprint tem {diss_bp}")

    cod_bp = bp["por_tipo"].get("analise_codigo", 0)
    if cod_bp and com_estimulo != cod_bp:
        erros.append(f"coluna 'Com código' soma {com_estimulo}, blueprint.analise_codigo = {cod_bp}")

    for cid, alvo in bp["por_competencia"].items():
        if por_comp.get(cid, 0) != alvo:
            erros.append(f"roteiro dá {por_comp.get(cid, 0)} itens a {cid}, blueprint pede {alvo}")
    for cid in set(por_comp) - set(bp["por_competencia"]):
        erros.append(f"roteiro cita tema '{cid}' que não é competência da matriz")

    m = re.search(
        r"\*\*Totais\*\*: (\d+) múltipla escolha · (\d+) múltipla resposta · "
        r"(\d+) dissertativa = \*\*(\d+) itens\*\*;\s*\n\*\*(\d+)\*\*",
        sec,
    )
    if not m:
        erros.append("linha '**Totais**' ausente ou fora do formato esperado")
    else:
        declarado = tuple(int(x) for x in m.groups())
        real = (
            por_botao.get("Múltipla escolha", 0),
            por_botao.get("Múltipla resposta", 0),
            por_botao.get("Dissertativa", 0),
            n,
            com_estimulo,
        )
        if declarado != real:
            erros.append(f"linha '**Totais**' declara {declarado}, mas a tabela soma {real}")

    return erros


TIPO_CURTO = {"Múltipla escolha": "MC", "Múltipla resposta": "MR", "Dissertativa": "Dissertativa"}


def valida_questionario(d, caminho_prompt, caminho_q):
    """Confere o questionário escrito de `questionarios/` contra o roteiro do prompt.

    O questionário é o artefato que a coordenação aplica ou usa como referência do que
    pedir à plataforma; se ele divergir do roteiro, deixa de ser a mesma avaliação.
    Checa: numeração sequencial dos itens, itens por tipo, itens por competência, itens
    com código/estímulo, presença de gabarito ou rubrica em cada item, e a tabela
    'Gabarito resumido' conferindo com os cabeçalhos.
    """
    _, por_botao_rot, por_comp_rot, com_estimulo_rot, erros = le_roteiro(d, caminho_prompt)
    if erros:
        return []  # o roteiro já é inválido; valida_roteiro reporta
    with open(caminho_q, encoding="utf-8") as f:
        md = f.read()

    erros = []
    itens = []  # (numero, tipo, competencia, tem_estimulo)
    cabecalho = re.compile(
        r"^## (\d+) · ([^·\n]+?) · (C\d+)[^·\n]*(?: · com (código|estímulo))?\s*$", re.M
    )
    blocos = list(cabecalho.finditer(md))
    for i, m in enumerate(blocos):
        num, tipo, comp, estimulo = int(m.group(1)), m.group(2).strip(), m.group(3), m.group(4)
        itens.append((num, tipo, f"{d['id_itt']}.{comp}", bool(estimulo)))
        if tipo not in TIPO_CURTO:
            erros.append(f"item {num}: tipo desconhecido '{tipo}'")
        corpo = md[m.end(): blocos[i + 1].start() if i + 1 < len(blocos) else len(md)]
        if tipo == "Dissertativa":
            if "**O que a resposta precisa conter:**" not in corpo:
                erros.append(f"item {num}: dissertativa sem rubrica de correção")
        elif "**Gabarito:" not in corpo:
            erros.append(f"item {num}: sem linha '**Gabarito:'")

    esperado = sum(por_botao_rot.values())
    if len(itens) != esperado:
        erros.append(f"questionário tem {len(itens)} itens, o roteiro pede {esperado}")
    if [n for n, _, _, _ in itens] != list(range(1, len(itens) + 1)):
        erros.append("itens não numerados de 1 a N em sequência")

    por_tipo = {}
    por_comp = {}
    com_estimulo = 0
    for _, tipo, comp, est in itens:
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
        por_comp[comp] = por_comp.get(comp, 0) + 1
        com_estimulo += est
    for tipo in set(por_tipo) | set(por_botao_rot):
        if por_tipo.get(tipo, 0) != por_botao_rot.get(tipo, 0):
            erros.append(
                f"questionário tem {por_tipo.get(tipo, 0)} itens de '{tipo}', "
                f"o roteiro pede {por_botao_rot.get(tipo, 0)}"
            )
    for comp in sorted(set(por_comp) | set(por_comp_rot)):
        if por_comp.get(comp, 0) != por_comp_rot.get(comp, 0):
            erros.append(
                f"questionário dá {por_comp.get(comp, 0)} itens a {comp}, "
                f"o roteiro pede {por_comp_rot.get(comp, 0)}"
            )
    if com_estimulo != com_estimulo_rot:
        erros.append(
            f"questionário tem {com_estimulo} itens com código/estímulo, "
            f"o roteiro pede {com_estimulo_rot}"
        )

    # --- tabela 'Gabarito resumido': duas metades por linha, 4 células cada
    if "## Gabarito resumido" not in md:
        erros.append("sem a seção '## Gabarito resumido'")
        return erros
    tab = md.split("## Gabarito resumido", 1)[1]
    resumo = {}
    for linha in tab.splitlines():
        if not linha.startswith("|") or "Gabarito |" in linha:
            continue
        if re.match(r"^\|[\s:|-]+\|$", linha):
            continue
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        for inicio in range(0, len(celulas) - 3, 4):
            num, tipo, comp = celulas[inicio: inicio + 3]
            if not num.isdigit():
                continue
            resumo[int(num)] = (tipo, comp)
    for num, tipo, comp, _ in itens:
        if num not in resumo:
            erros.append(f"item {num} ausente da tabela 'Gabarito resumido'")
            continue
        esperado_linha = (TIPO_CURTO.get(tipo, tipo), comp.split(".", 1)[1])
        if resumo[num] != esperado_linha:
            erros.append(
                f"item {num}: 'Gabarito resumido' diz {resumo[num]}, "
                f"o cabeçalho do item diz {esperado_linha}"
            )
    for num in sorted(set(resumo) - {n for n, _, _, _ in itens}):
        erros.append(f"'Gabarito resumido' lista o item {num}, que não existe no questionário")
    return erros


def valida(caminho):
    erros = []

    def erro(msg):
        erros.append(msg)

    with open(caminho, encoding="utf-8") as f:
        d = json.load(f)

    for campo in ("id_itt", "escola", "trilha", "competencias", "cursos",
                  "rubrica_proficiencia", "blueprint_questionario", "prompt", "metadados"):
        if campo not in d:
            erro(f"campo obrigatório ausente: {campo}")
    if erros:
        return erros

    idt = d["id_itt"]

    # --- trilha
    for campo in ("titulo_itt", "titulo_alura", "url", "carga_horaria_h", "n_cursos", "publico_alvo"):
        if campo not in d["trilha"]:
            erro(f"trilha.{campo} ausente")

    # --- competências
    comps = d["competencias"]
    ids_comp = [c["id"] for c in comps]
    if len(set(ids_comp)) != len(ids_comp):
        erro("ids de competência duplicados")
    for c in comps:
        if not c["id"].startswith(idt + "."):
            erro(f"competência {c['id']} não usa o prefixo {idt}.")
        if c["nivel_bloom"] not in BLOOM:
            erro(f"{c['id']}: nivel_bloom inválido '{c['nivel_bloom']}'")
        for t in c["tipos_de_item"]:
            if t not in TIPOS:
                erro(f"{c['id']}: tipo de item inválido '{t}'")
        for campo in ("evidencias_observaveis", "erros_comuns"):
            if not c.get(campo):
                erro(f"{c['id']}: {campo} vazio")

    soma = sum(c["peso"] for c in comps)
    if abs(soma - 1.0) > 0.001:
        erro(f"soma dos pesos das competências = {soma:.3f}, esperado 1.000")

    # --- cursos e objetivos
    ids_curso = [cur["id"] for cur in d["cursos"]]
    if len(set(ids_curso)) != len(ids_curso):
        erro("ids de curso duplicados")
    if len(ids_curso) != d["trilha"]["n_cursos"]:
        erro(f"trilha.n_cursos = {d['trilha']['n_cursos']} mas há {len(ids_curso)} cursos")

    carga = sum(cur["carga_horaria_h"] for cur in d["cursos"])
    if carga != d["trilha"]["carga_horaria_h"]:
        erro(f"soma da carga dos cursos = {carga}h, mas trilha.carga_horaria_h = {d['trilha']['carga_horaria_h']}h")

    usadas = set()
    ids_obj = []
    for cur in d["cursos"]:
        if not cur["id"].startswith(idt + "."):
            erro(f"curso {cur['id']} não usa o prefixo {idt}.")
        if not cur.get("fora_de_escopo"):
            erro(f"{cur['id']}: fora_de_escopo vazio (o gerador precisa dessa fronteira)")
        if not cur.get("objetivos_de_aprendizagem"):
            erro(f"{cur['id']}: sem objetivos de aprendizagem")
        for o in cur.get("objetivos_de_aprendizagem", []):
            ids_obj.append(o["id"])
            if not o["id"].startswith(cur["id"] + "."):
                erro(f"objetivo {o['id']} não usa o prefixo do curso {cur['id']}.")
            if o["nivel_bloom"] not in BLOOM:
                erro(f"{o['id']}: nivel_bloom inválido '{o['nivel_bloom']}'")
            if o["competencia"] not in ids_comp:
                erro(f"{o['id']} aponta para competência inexistente '{o['competencia']}'")
            else:
                usadas.add(o["competencia"])
    if len(set(ids_obj)) != len(ids_obj):
        erro("ids de objetivo duplicados")

    for c in comps:
        if c["id"] not in usadas:
            erro(f"competência órfã (nenhum objetivo aponta para ela): {c['id']}")
        for cid in c["cursos_origem"]:
            if cid not in ids_curso:
                erro(f"{c['id']}.cursos_origem cita curso inexistente '{cid}'")

    # --- rubrica
    faixas = sorted(d["rubrica_proficiencia"]["faixas"], key=lambda f: f["min_pct"])
    if faixas[0]["min_pct"] != 0 or faixas[-1]["max_pct"] != 100:
        erro("faixas da rubrica não cobrem de 0 a 100")
    for a, b in zip(faixas, faixas[1:]):
        if b["min_pct"] != a["max_pct"] + 1:
            erro(f"faixas não contíguas entre '{a['nivel']}' e '{b['nivel']}'")
    niveis = [f["nivel"] for f in faixas]
    if d["rubrica_proficiencia"]["nivel_minimo_esperado"] not in niveis:
        erro("nivel_minimo_esperado não corresponde a nenhuma faixa")

    # --- blueprint
    bp = d["blueprint_questionario"]
    n = bp["n_itens_total"]
    for chave in ("por_competencia", "por_tipo", "por_bloom"):
        total = sum(bp[chave].values())
        if total != n:
            erro(f"blueprint.{chave} soma {total}, esperado n_itens_total = {n}")
    faltando = set(ids_comp) - set(bp["por_competencia"])
    if faltando:
        erro(f"blueprint.por_competencia não cobre: {', '.join(sorted(faltando))}")
    sobrando = set(bp["por_competencia"]) - set(ids_comp)
    if sobrando:
        erro(f"blueprint.por_competencia cita competência inexistente: {', '.join(sorted(sobrando))}")
    for t in bp["por_tipo"]:
        if t not in TIPOS:
            erro(f"blueprint.por_tipo: tipo inválido '{t}'")
    for g in bp["por_bloom"]:
        if g not in GRUPOS_BLOOM:
            erro(f"blueprint.por_bloom: grupo inválido '{g}'")
    for c in comps:
        alvo = bp["por_competencia"].get(c["id"])
        if alvo is not None and c.get("itens_alvo") != alvo:
            erro(f"{c['id']}.itens_alvo = {c.get('itens_alvo')} diverge do blueprint ({alvo})")

    # --- prompt
    caminho_prompt = os.path.join(RAIZ, d["prompt"])
    if not os.path.exists(caminho_prompt):
        erro(f"arquivo de prompt não encontrado: {d['prompt']}")
    else:
        for e in valida_roteiro(d, caminho_prompt):
            erro(f"{d['prompt']}: {e}")

        # --- questionário escrito (opcional: só é checado quando existe)
        rel_q = os.path.join("questionarios", f"{idt}.md")
        caminho_q = os.path.join(RAIZ, rel_q)
        if os.path.exists(caminho_q):
            for e in valida_questionario(d, caminho_prompt, caminho_q):
                erro(f"{rel_q}: {e}")

    return erros


def main():
    alvos = sys.argv[1:] or sorted(glob(os.path.join(RAIZ, "cursos", "*.json")))
    if not alvos:
        print("nenhum arquivo para validar")
        return 1
    falhou = False
    for caminho in alvos:
        try:
            erros = valida(caminho)
        except Exception as e:  # JSON inválido, chave ausente em campo obrigatório etc.
            erros = [f"{type(e).__name__}: {e}"]
        nome = os.path.basename(caminho)
        if erros:
            falhou = True
            print(f"✗ {nome}")
            for e in erros:
                print(f"    {e}")
        else:
            print(f"✓ {nome}")
    return 1 if falhou else 0


if __name__ == "__main__":
    sys.exit(main())
