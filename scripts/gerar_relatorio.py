#!/usr/bin/env python3
"""Gera relatorios/relatorio-trilhas-itt.pdf a partir das matrizes e dos prompts.

Uso: python3 scripts/gerar_relatorio.py [--tex-only]

Lê cursos/*.json e prompts/*.md, monta um LaTeX e compila com pdflatex.
Só usa a biblioteca padrão; precisa de pdflatex no PATH (TeX Live).
O .tex é intermediário: vai para um diretório temporário, e só o PDF fica no repositório.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "relatorios", "relatorio-trilhas-itt.pdf")

# Ordem pedagógica das trilhas, igual à de catalogo.md.
ORDEM = ["PR01", "PR02", "PR03", "PR06", "PR12", "FE01", "FE03", "UX02", "UX03"]

BLOOM_ROTULO = {
    "lembrar": "lembrar", "entender": "entender", "aplicar": "aplicar",
    "analisar": "analisar", "avaliar": "avaliar", "criar": "criar",
}


def esc(s):
    """Escapa texto comum para LaTeX."""
    if s is None:
        return "---"
    s = str(s)
    for a, b in (
        ("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
        ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
        ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
    ):
        s = s.replace(a, b)
    return s


def mono(s):
    """Texto em monoespaçado.

    Permite quebra de linha depois de "/" (caminhos de arquivo), mas nunca depois de "."
    — senão identificadores como PR01.02 se partem ao fim da linha.
    """
    return r"\texttt{" + esc(s).replace("/", r"/\allowbreak{}") + "}"


def carrega():
    matrizes = {}
    for nome in os.listdir(os.path.join(RAIZ, "cursos")):
        if not nome.endswith(".json"):
            continue
        with open(os.path.join(RAIZ, "cursos", nome), encoding="utf-8") as f:
            d = json.load(f)
        d["_arquivo"] = f"cursos/{nome}"
        matrizes[d["id_itt"]] = d
    faltando = [i for i in ORDEM if i not in matrizes]
    if faltando:
        sys.exit(f"matriz ausente para: {', '.join(faltando)}")
    extra = [i for i in matrizes if i not in ORDEM]
    if extra:
        sys.exit(f"trilha fora da lista ORDEM de scripts/gerar_relatorio.py: {', '.join(extra)}")
    return matrizes


def le_prompt(d):
    """Devolve (texto_colavel, linhas_do_roteiro, nota_de_equivalencia, rotulo_col_estimulo)."""
    caminho = os.path.join(RAIZ, d["prompt"])
    with open(caminho, encoding="utf-8") as f:
        md = f.read()

    bloco = re.search(r"## 2\. Texto para colar\s*\n+```\n(.*?)\n```", md, re.S)
    if not bloco:
        sys.exit(f"{d['prompt']}: seção 2 (texto para colar) não encontrada")
    colavel = bloco.group(1)

    sec3 = md.split("## 3. Roteiro de montagem", 1)[1]
    linhas, rotulo = [], "Com código"
    for linha in sec3.splitlines():
        if not linha.startswith("|"):
            continue
        if re.match(r"^\|[\s:|-]+\|$", linha):
            continue
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        if "Botão a selecionar" in linha:
            rotulo = celulas[3]
            continue
        linhas.append(celulas)
    nota = re.findall(r"^> (.*)$", sec3, re.M)
    return colavel, linhas, " ".join(nota), rotulo


def tabela_panorama(matrizes):
    out = [
        r"\begin{longtable}{@{}l l >{\raggedright\arraybackslash}p{6.4cm} r r r@{}}",
        r"\toprule",
        r"\textbf{ID} & \textbf{Escola} & \textbf{Trilha} & \textbf{Carga} & "
        r"\textbf{Cursos} & \textbf{Itens} \\",
        r"\midrule \endhead",
    ]
    ch = ncur = nit = 0
    for i in ORDEM:
        d = matrizes[i]
        t, bp = d["trilha"], d["blueprint_questionario"]
        ch += t["carga_horaria_h"]
        ncur += t["n_cursos"]
        nit += bp["n_itens_total"]
        out.append(
            f"\\textbf{{{esc(i)}}} & {esc(d['escola'])} & {esc(t['titulo_itt'])} & "
            f"{t['carga_horaria_h']}h & {t['n_cursos']} & {bp['n_itens_total']} \\\\"
        )
    out += [
        r"\midrule",
        f"\\multicolumn{{3}}{{@{{}}l}}{{\\textbf{{Total}}}} & \\textbf{{{ch}h}} & "
        f"\\textbf{{{ncur}}} & \\textbf{{{nit}}} \\\\",
        r"\bottomrule",
        r"\end{longtable}",
    ]
    return "\n".join(out)


def bloco_identificacao(d):
    t = d["trilha"]
    pre = ", ".join(t.get("pre_requisitos") or []) or "nenhum"
    linhas = [
        ("Escola (ITT)", esc(d["escola"])),
        ("Nome na planilha ITT", esc(t["titulo_itt"])),
        ("Nome atual na Alura", esc(t["titulo_alura"])),
        ("Página da formação", r"\url{" + t["url"] + "}"),
        ("Carga horária", f"{t['carga_horaria_h']}h em {t['n_cursos']} cursos"),
        ("Pré-requisitos", esc(pre)),
        ("Público-alvo", esc(t["publico_alvo"])),
    ]
    if t.get("projeto_fio_condutor"):
        linhas.append(("Projeto fio condutor", esc(t["projeto_fio_condutor"])))
    linhas += [
        ("Matriz", mono(d["_arquivo"])),
        ("Prompt", mono(d["prompt"])),
    ]
    out = [r"\begin{longtable}{@{}>{\bfseries\raggedright\arraybackslash}p{3.6cm} "
           r">{\raggedright\arraybackslash}p{12.4cm}@{}}",
           r"\toprule \endhead"]
    for rot, val in linhas:
        out.append(f"{rot} & {val} \\\\[2pt]")
    out += [r"\bottomrule", r"\end{longtable}"]
    return "\n".join(out)


def bloco_competencias(d):
    comps = d["competencias"]
    out = [r"\subsection*{Competências avaliadas}",
           r"\addcontentsline{toc}{subsection}{Competências avaliadas}",
           r"\begin{longtable}{@{}l >{\raggedright\arraybackslash}p{8.5cm} r r l@{}}",
           r"\toprule",
           r"\textbf{Código} & \textbf{Competência} & \textbf{Peso} & \textbf{Itens} & "
           r"\textbf{Bloom} \\",
           r"\midrule \endhead"]
    for c in comps:
        out.append(
            f"{mono(c['id'])} & {esc(c['titulo'])} & {c['peso']:.2f} & {c['itens_alvo']} & "
            f"{esc(BLOOM_ROTULO.get(c['nivel_bloom'], c['nivel_bloom']))} \\\\[2pt]"
        )
    soma = sum(c["peso"] for c in comps)
    total = sum(c["itens_alvo"] for c in comps)
    out += [r"\midrule",
            f"\\multicolumn{{2}}{{@{{}}l}}{{\\textbf{{Total}}}} & \\textbf{{{soma:.2f}}} & "
            f"\\textbf{{{total}}} & \\\\",
            r"\bottomrule", r"\end{longtable}"]

    out.append(r"\noindent\textit{Detalhe de cada competência: o que ela significa e as "
               r"evidências que a demonstram. Os erros comuns que viram distratores não se "
               r"repetem aqui porque aparecem na íntegra no texto colável do prompt, "
               r"adiante.}\par\medskip")
    for c in comps:
        out.append(r"\begin{compbox}{" + mono(c["id"]) + " --- " + esc(c["titulo"]) + "}")
        out.append(esc(c["descricao"]) + r"\par\smallskip")
        out.append(r"\textbf{Evidências observáveis}")
        out.append(r"\begin{itemize}[leftmargin=1.2em,itemsep=1pt,topsep=2pt]")
        for e in c["evidencias_observaveis"]:
            out.append(r"\item " + esc(e))
        out.append(r"\end{itemize}")
        out.append(r"\smallskip\textbf{Tipos de item:} " +
                   ", ".join(mono(t) for t in c["tipos_de_item"]) +
                   r" \quad\textbf{Cursos de origem:} " +
                   ", ".join(mono(x) for x in c["cursos_origem"]))
        out.append(r"\end{compbox}")
    return "\n".join(out)


def bloco_cursos(d):
    idx = {c["id"]: c for c in d["competencias"]}
    out = [r"\subsection*{Cursos da trilha}",
           r"\addcontentsline{toc}{subsection}{Cursos da trilha}"]
    for cur in d["cursos"]:
        meta = [f"{cur['carga_horaria_h']}h"]
        if cur.get("n_atividades"):
            meta.append(f"{cur['n_atividades']} atividades")
        if cur.get("atualizado_em"):
            meta.append(f"atualizado em {cur['atualizado_em']}")
        out.append(r"\subsubsection*{" + mono(cur["id"]) + " --- " + esc(cur["titulo"]) + "}")
        out.append(r"\addcontentsline{toc}{subsubsection}{" + esc(cur["id"]) + " "
                   + esc(cur["titulo"]) + "}")
        out.append(r"\noindent\small " + esc(" · ".join(meta)))
        if cur.get("etapa_da_trilha"):
            out.append(r" \,|\, Etapa: \textit{" + esc(cur["etapa_da_trilha"]) + "}")
        out.append(r"\\ \footnotesize\url{" + cur["url"] + r"}\par\normalsize\smallskip")

        out.append(r"\noindent\textbf{Módulos da ementa.} " +
                   esc("; ".join(cur["modulos"])) + r".\par\smallskip")
        out.append(r"\noindent\textbf{Conceitos-chave.} " +
                   ", ".join(mono(k) for k in cur["conceitos_chave"]) + r".\par\smallskip")

        out.append(r"\noindent\textbf{Objetivos de aprendizagem}\par\nopagebreak")
        out.append(r"\begin{longtable}{@{}l >{\raggedright\arraybackslash}p{10.1cm} l l@{}}")
        out.append(r"\toprule \textbf{Objetivo} & \textbf{Enunciado} & \textbf{Bloom} & "
                   r"\textbf{Competência} \\ \midrule \endhead")
        for o in cur["objetivos_de_aprendizagem"]:
            out.append(
                f"{mono(o['id'])} & {esc(o['enunciado'])} & "
                f"{esc(BLOOM_ROTULO.get(o['nivel_bloom'], o['nivel_bloom']))} & "
                f"{mono(o['competencia'])} \\\\[2pt]"
            )
        out.append(r"\bottomrule \end{longtable}")
        alvos = sorted({o["competencia"] for o in cur["objetivos_de_aprendizagem"]})
        out.append(r"\noindent\small\textbf{Competências alimentadas por este curso:} " +
                   "; ".join(f"{mono(a)} {esc(idx[a]['titulo'])}" for a in alvos) +
                   r".\par\normalsize\smallskip")
        out.append(r"\noindent\textbf{Fora de escopo (o questionário não cobra).} " +
                   esc("; ".join(cur["fora_de_escopo"])) + r".\par\medskip")
    return "\n".join(out)


def bloco_rubrica(d):
    r = d["rubrica_proficiencia"]
    out = [r"\subsection*{Rubrica de proficiência}",
           r"\addcontentsline{toc}{subsection}{Rubrica de proficiência}",
           r"\begin{longtable}{@{}l l >{\raggedright\arraybackslash}p{11.6cm}@{}}",
           r"\toprule \textbf{Faixa} & \textbf{\%} & \textbf{Descritor} \\ \midrule \endhead"]
    for f in sorted(r["faixas"], key=lambda x: x["min_pct"]):
        destaque = f["nivel"] == r["nivel_minimo_esperado"]
        nome = esc(f["nivel"])
        if destaque:
            nome = r"\textbf{" + nome + r"}"
        out.append(f"{nome} & {f['min_pct']}--{f['max_pct']} & {esc(f['descritor'])} \\\\[2pt]")
    out += [r"\bottomrule", r"\end{longtable}"]
    out.append(r"\noindent\textbf{Nível mínimo esperado:} " +
               esc(r["nivel_minimo_esperado"]) + r".\par")
    if r.get("observacao"):
        out.append(r"\begin{notabox}\textbf{Observação da coordenação.} " +
                   esc(r["observacao"]) + r"\end{notabox}")
    return "\n".join(out)


def bloco_prompt(d, colavel, roteiro, nota, rotulo):
    bp = d["blueprint_questionario"]
    out = [r"\subsection*{Prompt do questionário}",
           r"\addcontentsline{toc}{subsection}{Prompt do questionário}"]
    por_tipo = " · ".join(f"{esc(k)} {v}" for k, v in bp["por_tipo"].items())
    por_bloom = " · ".join(f"{esc(k.replace('_', '/'))} {v}" for k, v in bp["por_bloom"].items())
    out.append(r"\noindent\textbf{Blueprint.} " +
               f"{bp['n_itens_total']} itens, {bp['tempo_estimado_min']} minutos estimados. "
               r"Por tipo na matriz: " + por_tipo + ". Por nível cognitivo: " + por_bloom +
               r".\par\medskip")

    out.append(r"\noindent\textbf{Roteiro de montagem.} Percorra as linhas de cima para baixo: "
               r"em cada uma, selecione o botão indicado na plataforma e peça a quantidade "
               r"daquele tema.\par\nopagebreak")
    out.append(r"\begin{longtable}{@{}>{\raggedright\arraybackslash}p{3.3cm} c "
               r">{\raggedright\arraybackslash}p{2.1cm} c "
               r">{\raggedright\arraybackslash}p{6.4cm}@{}}")
    out.append(r"\toprule \textbf{Tema} & \textbf{Qtd.} & \textbf{Botão} & "
               r"\textbf{" + esc(rotulo) + r"} & \textbf{Foco da linha} \\ \midrule \endhead")
    somas = {}
    estim = 0
    for c in roteiro:
        somas[c[2]] = somas.get(c[2], 0) + int(c[1])
        estim += int(c[3])
        out.append(f"{esc(c[0])} & {esc(c[1])} & {esc(c[2])} & {esc(c[3])} & {esc(c[4])} \\\\[2pt]")
    out += [r"\bottomrule", r"\end{longtable}"]
    # ordem fixa na linha de totais, independente da ordem em que os botões aparecem
    ordem_botao = ["Múltipla escolha", "Múltipla resposta", "Dissertativa"]
    chaves = [b for b in ordem_botao if b in somas] + [b for b in somas if b not in ordem_botao]
    tot = " · ".join(f"{esc(b)} {somas[b]}" for b in chaves)
    out.append(r"\noindent\textbf{Totais:} " + tot +
               f" = \\textbf{{{sum(somas.values())} itens}}; {estim} com "
               f"{esc(rotulo.lower().replace('com ', ''))} no enunciado.\\par")
    if nota:
        out.append(r"\begin{notabox}" + esc(nota) + r"\end{notabox}")

    out.append(r"\medskip\noindent\textbf{Texto para colar na plataforma.} Cole o bloco "
               r"abaixo inteiro no campo de prompt, uma vez só. Ele define o "
               r"\emph{tema} das questões; o \emph{tipo} vem do botão que você seleciona a "
               r"cada linha do roteiro acima.\par\smallskip")
    out.append(r"\begin{Verbatim}")
    out.append(colavel)
    out.append(r"\end{Verbatim}")
    return "\n".join(out)


def bloco_fontes(matrizes):
    out = [r"\section*{Apêndice --- fontes e reprodutibilidade}",
           r"\addcontentsline{toc}{section}{Apêndice --- fontes e reprodutibilidade}",
           r"\markboth{Apêndice}{Apêndice}",
           r"Os dados factuais de cada trilha --- lista de cursos, carga horária, módulos da "
           r"ementa, público-alvo e objetivos declarados --- vêm das páginas públicas da Alura, "
           r"sem login e sem baixar vídeo. Competências, pesos, erros comuns, faixas de "
           r"proficiência e os roteiros de montagem são elaboração pedagógica da ITT e são, "
           r"portanto, revisáveis.\par\medskip",
           r"\begin{longtable}{@{}l l >{\footnotesize\raggedright\arraybackslash}"
           r"p{11.6cm}@{}}",
           r"\toprule \textbf{Trilha} & \textbf{Extração} & \textbf{Fontes} \\ "
           r"\midrule \endhead"]
    for i in ORDEM:
        m = matrizes[i]["metadados"]
        fontes = r" \newline ".join(
            (r"\url{" + f + "}") if f.startswith("http") else mono(f) for f in m["fontes"]
        )
        out.append(f"\\textbf{{{esc(i)}}} & {esc(m['data_extracao'])} & {fontes} \\\\[3pt]")
    out += [r"\bottomrule", r"\end{longtable}"]
    ressalvas = [(i, matrizes[i]["metadados"]["derivado_de"]) for i in ORDEM
                 if "ATENÇÃO" in matrizes[i]["metadados"].get("derivado_de", "")]
    for i, texto in ressalvas:
        out.append(r"\begin{notabox}\textbf{Ressalva de fonte --- " + esc(i) + r".} " +
                   esc(texto) + r"\end{notabox}")
    out.append(r"\medskip\noindent A consistência de todos os arquivos é verificável com "
               r"\texttt{python3 scripts/validar.py}, que confere, entre outras regras, se o "
               r"roteiro de cada prompt fecha com o blueprint da sua matriz. Este relatório é "
               r"gerado por \texttt{python3 scripts/gerar\_relatorio.py} e não deve ser "
               r"editado à mão.\par")
    return "\n".join(out)


PREAMBULO = r"""\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage[margin=2cm,includeheadfoot,headheight=14pt]{geometry}
\usepackage{booktabs,longtable,array,enumitem,xcolor,fancyhdr,titlesec}
\usepackage{fvextra}
\usepackage[hyphens]{url}
\usepackage[hidelinks]{hyperref}
% URLs de curso da Alura são longas; deixe o TeX quebrá-las em -, /, . e _
\makeatletter
\g@addto@macro\UrlBreaks{\do\-\do\/\do\.\do\_\do\?\do\=\do\&}
\makeatother
\Urlmuskip=0mu plus 1mu\relax
\usepackage{tcolorbox}
\tcbuselibrary{breakable,skins}

\definecolor{tinta}{HTML}{1C1A17}
\definecolor{acento}{HTML}{3A5A8C}
\definecolor{suave}{HTML}{F4F2ED}
\definecolor{traco}{HTML}{C3BCAC}

\hypersetup{colorlinks=false,pdftitle={Relatorio de trilhas e questionarios -- ITT},
  pdfauthor={ITT},pdfsubject={Matrizes de aprendizagem e prompts de questionario}}

% sem babel-português instalado, as poucas cadeias automáticas ficam em inglês
\renewcommand{\contentsname}{Sumário}

\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.12}
\setlength{\LTpre}{4pt}\setlength{\LTpost}{6pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\sloppy
% Esta instalação do TeX Live só traz padrões de hifenização do inglês, que partem
% palavras em português nos lugares errados ("esper-ado"). Proibimos a hifenização
% automática e deixamos apenas as quebras em hífens já existentes — inclusive as
% que o pacote url insere nas URLs longas da Alura.
\hyphenpenalty=10000
\exhyphenpenalty=100

\fvset{fontsize=\footnotesize,breaklines=true,breakanywhere=true,frame=leftline,
  framerule=1.4pt,rulecolor=\color{traco},framesep=9pt,xleftmargin=4pt}

\titleformat{\section}{\color{acento}\Large\bfseries}{}{0pt}{}
\titlespacing*{\section}{0pt}{16pt}{8pt}
\titleformat{\subsection}{\color{tinta}\large\bfseries}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{12pt}{5pt}
\titleformat{\subsubsection}{\color{tinta}\normalsize\bfseries}{}{0pt}{}
\titlespacing*{\subsubsection}{0pt}{10pt}{4pt}

\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\fancyhead[L]{\footnotesize\color{tinta}ITT --- Questionários de proficiência pós-trilha}
\fancyhead[R]{\footnotesize\color{tinta}\nouppercase{\leftmark}}
\fancyfoot[C]{\footnotesize\thepage}

\newtcolorbox{compbox}[1]{breakable,enhanced,colback=suave,colframe=traco,
  boxrule=0.4pt,left=7pt,right=7pt,top=5pt,bottom=5pt,
  fonttitle=\bfseries\small,title={#1},coltitle=tinta,
  colbacktitle=suave,borderline north={0.4pt}{0pt}{traco},
  before skip=5pt,after skip=7pt}

\newtcolorbox{notabox}{breakable,enhanced,colback=white,colframe=acento,
  boxrule=0pt,leftrule=1.6pt,left=7pt,right=5pt,top=4pt,bottom=4pt,
  sharp corners,before skip=6pt,after skip=8pt,fontupper=\small}
"""


def monta(matrizes):
    hoje = date.today().isoformat()
    ch = sum(matrizes[i]["trilha"]["carga_horaria_h"] for i in ORDEM)
    ncur = sum(matrizes[i]["trilha"]["n_cursos"] for i in ORDEM)

    p = [PREAMBULO, r"\begin{document}"]

    # --- capa
    p.append(r"""
\thispagestyle{empty}
\vspace*{2.2cm}
{\color{acento}\rule{\textwidth}{2pt}}\par\vspace{10pt}
{\Huge\bfseries Trilhas, competências e questionários\par}
\vspace{6pt}
{\LARGE ITT --- avaliação de proficiência pós-trilha\par}
\vspace{10pt}
{\color{acento}\rule{\textwidth}{0.6pt}}
\vspace{1.4cm}

\begin{minipage}{\textwidth}
\large
Relatório de referência para a coordenação: o que cada trilha da ITT se propõe a ensinar,
quais competências o questionário pós-trilha cobra, o que cada curso da trilha contribui, e
o prompt pronto para gerar o questionário na plataforma parceira.
\end{minipage}

\vspace{1.2cm}
\begin{longtable}{@{}>{\bfseries\raggedright\arraybackslash}p{4.2cm} >{\raggedright\arraybackslash}p{11.8cm}@{}}
\toprule \endhead
Trilhas cobertas & """ + str(len(ORDEM)) + r""" (todas as da planilha atual da ITT) \\[2pt]
Cursos & """ + str(ncur) + r""" \\[2pt]
Carga total & """ + str(ch) + r"""h \\[2pt]
Itens por questionário & 20, sendo 2 dissertativos \\[2pt]
Nível mínimo esperado & adequado (70--84\%) \\[2pt]
Gerado em & """ + hoje + r""" \\[2pt]
Gerado por & \texttt{scripts/gerar\_relatorio.py} \\
\bottomrule
\end{longtable}

\vfill
\begin{notabox}
\textbf{Como ler este relatório.} O questionário é \textbf{um por trilha}, não um por curso:
a avaliação acontece depois de a trilha inteira ser concluída e mede competências que
atravessam vários cursos. Por isso cada trilha tem \emph{um} prompt, e a contribuição de cada
curso aparece nos seus objetivos de aprendizagem, que apontam para as competências cobradas.
\end{notabox}
\clearpage
""")

    # --- sumário
    p.append(r"\pagenumbering{roman}")
    p.append(r"\tableofcontents")
    p.append(r"\clearpage\pagenumbering{arabic}")

    # --- panorama
    p.append(r"\section*{Panorama das trilhas}")
    p.append(r"\addcontentsline{toc}{section}{Panorama das trilhas}")
    p.append(r"\markboth{Panorama}{Panorama}")
    p.append(tabela_panorama(matrizes))
    p.append(r"""
\subsection*{Como aplicar}
\addcontentsline{toc}{subsection}{Como aplicar}
\begin{enumerate}[leftmargin=1.4em,itemsep=2pt]
\item Abra a seção \textbf{Prompt do questionário} da trilha e cole o \textbf{texto para
colar} no campo de prompt da plataforma, uma vez só.
\item Percorra o \textbf{roteiro de montagem} linha por linha. Em cada linha, selecione na
plataforma o botão de tipo indicado --- múltipla escolha, múltipla resposta ou dissertativa
--- e peça a quantidade daquele tema.
\item Confira os totais ao fim do roteiro antes de fechar o questionário.
\item Aplique depois de a trilha estar concluída e reporte a faixa da
\textbf{rubrica de proficiência} da trilha.
\end{enumerate}

\subsection*{Por que três botões e três tipos}
\addcontentsline{toc}{subsection}{Por que três botões e três tipos}
A matriz de cada trilha classifica os itens em múltipla escolha, análise de código e
dissertativa. A plataforma parceira, porém, oferece outros três botões: múltipla escolha,
múltipla resposta e dissertativa. O roteiro faz a tradução: os itens de análise de código
viram múltipla escolha com um trecho de código no enunciado (coluna \textbf{Com código}), e
parte dos itens objetivos vira múltipla resposta onde o tema pede identificar um conjunto.

Nas duas trilhas sem programação --- UX02 Game Design e UX03 Blender --- o tipo análise de
código não se aplica, e a coluna passa a ser \textbf{Com estímulo}: um trecho curto de Game
Design Document, uma cena ou uma situação de modelagem descrita em texto. Nenhum prompt pede
que o estudante veja uma imagem.
\clearpage
""")

    # --- uma seção por trilha
    for i in ORDEM:
        d = matrizes[i]
        colavel, roteiro, nota, rotulo = le_prompt(d)
        titulo = f"{i} --- {esc(d['trilha']['titulo_itt'])}"
        p.append(r"\section*{" + titulo + "}")
        p.append(r"\addcontentsline{toc}{section}{" + titulo + "}")
        p.append(r"\markboth{" + esc(i) + "}{" + esc(i) + "}")
        p.append(bloco_identificacao(d))
        p.append(bloco_competencias(d))
        p.append(bloco_cursos(d))
        p.append(bloco_rubrica(d))
        p.append(bloco_prompt(d, colavel, roteiro, nota, rotulo))
        p.append(r"\clearpage")

    p.append(bloco_fontes(matrizes))
    p.append(r"\end{document}")
    return "\n".join(p)


def main():
    matrizes = carrega()
    tex = monta(matrizes)
    if "--tex-only" in sys.argv:
        destino = os.path.join(RAIZ, "relatorios", "relatorio-trilhas-itt.tex")
        with open(destino, "w", encoding="utf-8") as f:
            f.write(tex)
        print(f"tex escrito em {os.path.relpath(destino, RAIZ)}")
        return 0

    if not shutil.which("pdflatex"):
        sys.exit("pdflatex não encontrado no PATH (instale o TeX Live)")

    with tempfile.TemporaryDirectory(prefix="relatorio-itt-") as tmp:
        base = os.path.join(tmp, "relatorio")
        with open(base + ".tex", "w", encoding="utf-8") as f:
            f.write(tex)
        # duas passadas: a primeira resolve o sumário, a segunda acerta a paginação
        for passada in (1, 2):
            r = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                 "-output-directory", tmp, base + ".tex"],
                capture_output=True, text=True, errors="replace", timeout=300,
            )
            if r.returncode != 0:
                log = ""
                if os.path.exists(base + ".log"):
                    with open(base + ".log", encoding="utf-8", errors="replace") as f:
                        log = f.read()
                erros = re.findall(r"^! .*(?:\n.*){0,4}", log, re.M)
                sys.exit("pdflatex falhou na passada "
                         f"{passada}:\n{''.join(erros[:5]) or r.stdout[-2500:]}")
        os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
        shutil.copy(base + ".pdf", SAIDA)
        with open(base + ".log", encoding="utf-8", errors="replace") as f:
            log = f.read()

    over = len(re.findall(r"Overfull \\hbox", log))
    paginas = re.search(r"Output written on .*\((\d+) pages", log)
    print(f"✓ {os.path.relpath(SAIDA, RAIZ)} "
          f"({paginas.group(1) if paginas else '?'} páginas, "
          f"{os.path.getsize(SAIDA) // 1024} KB)")
    if over:
        print(f"  aviso: {over} linha(s) transbordando a margem (Overfull hbox)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
