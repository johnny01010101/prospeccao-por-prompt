"""Gera a planilha final (.xlsx) com 4 abas, sem instalar nada.

Abas: "Comece aqui", "Contas", "Descartadas", "Sinais e critérios".
A aba "Contas" já serve pra importar na fulgurite: as duas primeiras colunas
(Nome da empresa e Site) são as únicas obrigatórias.

Uso:
  python scripts/planilha.py                 lê kit/contas.csv e kit/descartadas.csv
  python scripts/planilha.py --exemplo       usa exemplos/ (dados fictícios) pra testar
  python scripts/planilha.py --saida ARQ.xlsx
"""
from __future__ import annotations

import argparse
import os
import sys
import zipfile
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(__file__))
from comum import (COLUNAS_CONTAS, KIT, RAIZ, SAIDA, ler_csv, link_fulgurite,  # noqa: E402
                   saida_utf8)

saida_utf8()

# estilos (índices em cellXfs)
NORMAL, CABECALHO, QUEBRA, FAIXA_A, FAIXA_B, FAIXA_C, TITULO, LINK, SUBTITULO = range(9)
LARGURAS = {
    "nome_empresa": 28, "site": 26, "faixa": 7, "nota": 10, "por_que_agora": 48,
    "o_que_vende": 40, "encaixe_icp": 36, "alertas": 30, "vagas_comerciais": 36,
    "ferramentas_citadas": 30, "cargo_decisor": 30, "area_decisora": 20, "proximo_passo": 24,
}
COLUNAS_LINK = {"site", "sinal1_link", "sinal2_link", "sinal3_link", "noticia_link"}


def _col(n: int) -> str:
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _limpo(v) -> str:
    texto = "" if v is None else str(v)
    return "".join(ch for ch in texto if ch in "\t\n\r" or ord(ch) >= 32)


def _celula(ref: str, valor, estilo: int = NORMAL, link: bool = False) -> str:
    v = _limpo(valor)
    if v == "":
        return f'<c r="{ref}" s="{estilo}"/>'
    if link and v.lower().startswith(("http://", "https://", "www.")):
        url = v if v.lower().startswith("http") else "https://" + v
        formula = escape(f'HYPERLINK("{url.replace(chr(34), "")}","{v.replace(chr(34), "")[:250]}")')
        return f'<c r="{ref}" s="{LINK}" t="str"><f>{formula}</f><v>{escape(v)}</v></c>'
    try:
        if v.replace(",", ".").replace(".", "", 1).isdigit() and len(v) < 12 and not v.startswith("0"):
            return f'<c r="{ref}" s="{estilo}"><v>{float(v.replace(",", "."))}</v></c>'
    except ValueError:
        pass
    return f'<c r="{ref}" s="{estilo}" t="inlineStr"><is><t xml:space="preserve">{escape(v)}</t></is></c>'


def _aba(linhas: list[list[tuple]], larguras: list[int], congelar=False, filtro=False) -> str:
    xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
           '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">']
    if congelar:
        xml.append('<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" xSplit="2" topLeftCell="C2" '
                   'activePane="bottomRight" state="frozen"/></sheetView></sheetViews>')
    xml.append("<cols>" + "".join(
        f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>' for i, w in enumerate(larguras)) + "</cols>")
    xml.append("<sheetData>")
    for r, linha in enumerate(linhas, start=1):
        celulas = "".join(_celula(f"{_col(c)}{r}", v, s, l) for c, (v, s, l) in enumerate(linha))
        xml.append(f'<row r="{r}">{celulas}</row>')
    xml.append("</sheetData>")
    if filtro and linhas:
        xml.append(f'<autoFilter ref="A1:{_col(len(linhas[0]) - 1)}{len(linhas)}"/>')
    xml.append("</worksheet>")
    return "".join(xml)


ESTILOS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="5">
<font><sz val="11"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
<font><b/><sz val="16"/><name val="Calibri"/></font>
<font><u/><sz val="11"/><color rgb="FF1155CC"/><name val="Calibri"/></font>
<font><b/><sz val="12"/><name val="Calibri"/></font>
</fonts>
<fills count="6">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FF1F2937"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFC6EFCE"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFFFEB9C"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFFCE4D6"/></patternFill></fill>
</fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="9">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top"/></xf>
<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="4" fillId="3" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf>
<xf numFmtId="0" fontId="4" fillId="4" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf>
<xf numFmtId="0" fontId="4" fillId="5" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf>
<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment vertical="top"/></xf>
<xf numFmtId="0" fontId="4" fillId="0" borderId="0" xfId="0" applyFont="1"/>
</cellXfs>
</styleSheet>"""


def _nota(c: dict) -> float:
    try:
        return float(str(c.get("nota", "0")).replace(",", "."))
    except ValueError:
        return 0.0


def montar(contas: list[dict], descartadas: list[dict], criterios: list[str], destino: Path) -> Path:
    contas = sorted(contas, key=_nota, reverse=True)
    faixas = {f: sum(1 for c in contas if (c.get("faixa") or "").upper() == f) for f in "ABC"}
    hoje = date.today().strftime("%d/%m/%Y")

    comece = [
        [(f"Sua lista de contas, {hoje}", TITULO, False)],
        [("", NORMAL, False)],
        [(f"{len(contas)} contas com motivo pra abordar agora: {faixas['A']} na faixa A, "
          f"{faixas['B']} na B e {faixas['C']} na C. {len(descartadas)} ficaram de fora (veja a aba Descartadas).", QUEBRA, False)],
        [("", NORMAL, False)],
        [("Como usar na segunda-feira", SUBTITULO, False)],
        [("1. Abra a aba Contas. Ela já vem em ordem de nota: comece pelas linhas verdes (faixa A).", QUEBRA, False)],
        [("2. Leia a coluna \"Por que agora\". É o motivo, em uma linha, pra essa empresa estar na lista esta semana.", QUEBRA, False)],
        [("3. Antes de abordar, clique no link do sinal e confira. Tudo aqui vem de fontes públicas e pode mudar.", QUEBRA, False)],
        [("4. Distribua as contas A e B entre o time. As C ficam pra monitorar.", QUEBRA, False)],
        [("", NORMAL, False)],
        [("O que falta", SUBTITULO, False)],
        [("Quem decide em cada empresa e como falar com essa pessoa. O kit para aqui de propósito: ele só usa dados "
          "públicos de empresa e mostra o cargo provável de quem decide, não o nome nem o contato.", QUEBRA, False)],
        [("", NORMAL, False)],
        [("Próximo passo", SUBTITULO, False)],
        [("Suba a aba Contas na fulgurite (só precisa das colunas Nome da empresa e Site) e use os 50 créditos "
          "grátis do trial de 7 dias pra encontrar quem decide e o contato de cada conta.", QUEBRA, False)],
        [(link_fulgurite("comece-aqui"), NORMAL, True)],
        [("", NORMAL, False)],
        [("Lista viva", SUBTITULO, False)],
        [("Na semana que vem, abra o Claude nesta pasta e digite /atualizar. Ele busca só os sinais novos e não "
          "repete as contas desta lista.", QUEBRA, False)],
        [("", NORMAL, False)],
        [("Potenciais contas com base em sinais públicos. Nenhuma empresa daqui demonstrou interesse no seu produto; "
          "confira antes de abordar.", QUEBRA, False)],
    ]

    cab = [(rotulo, CABECALHO, False) for _, rotulo in COLUNAS_CONTAS]
    linhas_contas = [cab]
    estilo_faixa = {"A": FAIXA_A, "B": FAIXA_B, "C": FAIXA_C}
    for c in contas:
        linha = []
        for cid, _ in COLUNAS_CONTAS:
            v = c.get(cid, "")
            if cid == "faixa":
                linha.append((v, estilo_faixa.get(str(v).upper(), NORMAL), False))
            else:
                linha.append((v, QUEBRA if cid in LARGURAS and LARGURAS[cid] >= 30 else NORMAL, cid in COLUNAS_LINK))
        linhas_contas.append(linha)

    linhas_desc = [[("Nome da empresa", CABECALHO, False), ("Site", CABECALHO, False), ("Motivo", CABECALHO, False)]]
    linhas_desc += [[(d.get("nome_empresa", ""), NORMAL, False), (d.get("site", ""), NORMAL, True),
                     (d.get("motivo", ""), QUEBRA, False)] for d in descartadas]

    linhas_crit = [[("ICP, sinais e buscas usados nesta rodada", TITULO, False)], [("", NORMAL, False)]]
    linhas_crit += [[(l, QUEBRA, False)] for l in criterios] or [[("(sem critérios gravados)", NORMAL, False)]]

    abas = [
        ("Comece aqui", _aba(comece, [110])),
        ("Contas", _aba(linhas_contas, [LARGURAS.get(c, 16) for c, _ in COLUNAS_CONTAS], congelar=True, filtro=True)),
        ("Descartadas", _aba(linhas_desc, [30, 30, 60], congelar=False, filtro=True)),
        ("Sinais e critérios", _aba(linhas_crit, [120])),
    ]

    destino.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                   '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                   + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                             for i in range(1, len(abas) + 1))
                   + "</Types>")
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                   "</Relationships>")
        z.writestr("xl/workbook.xml",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                   'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
                   + "".join(f'<sheet name="{escape(n)}" sheetId="{i}" r:id="rId{i}"/>' for i, (n, _) in enumerate(abas, 1))
                   + "</sheets>"
                   + (f'<definedNames><definedName name="_xlnm._FilterDatabase" localSheetId="1" hidden="1">'
                      f"'Contas'!$A$1:${_col(len(COLUNAS_CONTAS) - 1)}${len(linhas_contas)}</definedName></definedNames>")
                   + "</workbook>")
        z.writestr("xl/_rels/workbook.xml.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
                             for i in range(1, len(abas) + 1))
                   + f'<Relationship Id="rId{len(abas) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                   "</Relationships>")
        z.writestr("xl/styles.xml", ESTILOS)
        for i, (_, xml) in enumerate(abas, 1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", xml)
    return destino


def _criterios(pasta: Path) -> list[str]:
    linhas = []
    for nome in ("icp.md", "sinais.md"):
        arq = pasta / nome
        if arq.exists():
            linhas.append(f"== {nome} ==")
            linhas += [l.rstrip() for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()]
            linhas.append("")
    return linhas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exemplo", action="store_true")
    ap.add_argument("--saida")
    a = ap.parse_args()
    pasta = RAIZ / "exemplos" if a.exemplo else KIT
    contas = ler_csv(pasta / "contas.csv")
    if not contas:
        print(f"Não achei contas em {pasta / 'contas.csv'}. Rode /lista primeiro.")
        return 1
    sem_obrigatorio = [c for c in contas if not c.get("nome_empresa") or not c.get("site")]
    contas = [c for c in contas if c.get("nome_empresa") and c.get("site")]
    descartadas = ler_csv(pasta / "descartadas.csv") + [
        {"nome_empresa": c.get("nome_empresa", ""), "site": c.get("site", ""), "motivo": "sem nome ou sem site"}
        for c in sem_obrigatorio]
    nome = f"lista-{'exemplo-' if a.exemplo else ''}{date.today().isoformat()}.xlsx"
    destino = Path(a.saida) if a.saida else SAIDA / nome
    montar(contas, descartadas, _criterios(pasta), destino)
    print(f"Planilha pronta: {destino.resolve()}")
    print(f"{len(contas)} contas, {len(descartadas)} descartadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
