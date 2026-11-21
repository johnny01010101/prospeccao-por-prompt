"""Busca vagas abertas em portais públicos (Gupy e Vagas.com) e agrupa por empresa.

Lê só as páginas públicas de busca (as mesmas que qualquer candidato vê). Não usa login.

Uso:
  python scripts/vagas.py "SDR" "gerente comercial" --paginas 2 --dias 30
  python scripts/vagas.py "analista de RH" --uf "São Paulo" --descricao

Opções:
  --paginas N   páginas por termo e por portal (padrão 1, máximo 5)
  --dias N      só vagas publicadas nos últimos N dias (padrão 45)
  --uf NOME     filtra pelo estado (por extenso, "Minas Gerais", ou sigla, "MG")
  --fontes X    gupy,vagas (padrão: as duas)
  --descricao   inclui os primeiros 1.200 caracteres da descrição
  --saida ARQ   grava também um CSV com uma linha por empresa (ex.: dados/vagas.csv)
  --sem-historico  não grava a foto desta rodada em dados/historico-vagas.csv

Sinais que saem prontos por empresa:
  qtd_vagas, vaga_mais_recente
  estruturar_do_zero  a descrição fala em primeiro vendedor, montar o time ou criar a área do zero
  vagas_rodada_anterior / crescimento_vagas  comparação com a última rodada com os mesmos termos

Saída: JSON com uma entrada por empresa.
"""
from __future__ import annotations

import argparse
import csv
import html as htmllib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from comum import DADOS, baixar, gravar_csv, imprimir_json, saida_utf8  # noqa: E402

saida_utf8()

GUPY = "https://portal.gupy.io/job-search/term={termo}&page={pagina}"
VAGAS = "https://www.vagas.com.br/vagas-de-{slug}?ordenar_por=mais_recentes&pagina={pagina}"
PADRAO_DADOS = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)
HISTORICO = DADOS / "historico-vagas.csv"
OCULTA = re.compile(r"^(confidencial|empresa confidencial|sigilos[oa]|n[ãa]o informad[oa])$", re.I)

UFS = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia", "CE": "Ceará",
    "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul", "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
    "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina",
    "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins",
}

# Sinal "estruturar do zero": a empresa está montando a área comercial agora.
DO_ZERO = re.compile(
    r"primeir[oa]s? (vendedor|sdr|bdr|executiv|closer|contrata[çc][ãa]o comercial|pessoa (de|do) (vendas|comercial))"
    r"|estrutura[rç][ãa]?o? (d?[oa] )?(time|[áa]rea|setor|equipe|processo|opera[çc][ãa]o) (de vendas|comercial)"
    r"|(montar|construir|criar|implantar|implementar) (o |a |um |uma |nosso |nossa )?(time|[áa]rea|setor|equipe|processo) (de vendas|comercial)"
    r"|(time|[áa]rea|setor|equipe|opera[çc][ãa]o|processo) (de vendas|comercial)[^.]{0,40}(do|desde o) zero",
    re.I,
)


def _sem_acento(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def _chave(nome: str) -> str:
    t = _sem_acento(nome.lower())
    t = re.sub(r"\b(ltda|s\.?a\.?|eireli|me|epp|grupo)\b", " ", t)
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def _uf_ok(filtro: str | None, estado: str) -> bool:
    if not filtro:
        return True
    alvo = UFS.get(filtro.upper(), filtro)
    e = estado.strip()
    return _sem_acento(e.lower()) in {_sem_acento(alvo.lower()), _sem_acento(filtro.lower())} or \
        _sem_acento(UFS.get(e.upper(), e).lower()) == _sem_acento(alvo.lower())


# ---------- Gupy ----------
def _gupy(termo: str, pagina: int) -> list[dict]:
    url = GUPY.format(termo=urllib.parse.quote(termo), pagina=pagina)
    m = PADRAO_DADOS.search(baixar(url, navegador=True))
    if not m:
        return []
    props = json.loads(m.group(1)).get("props", {}).get("pageProps", {})
    out = []
    for v in props.get("initialJobList", {}).get("data", []) or []:
        host = urllib.parse.urlparse(v.get("jobUrl") or "").netloc
        out.append({
            "id": f"gupy-{v.get('id')}",
            "empresa": (v.get("careerPageName") or "").strip(),
            "pagina_carreira": f"https://{host}" if host else "",
            "cargo": (v.get("name") or "").strip(),
            "data": (v.get("publishedDate") or "")[:10],
            "cidade": v.get("city") or "",
            "estado": v.get("state") or "",
            "modelo": v.get("workplaceType") or "",
            "link": v.get("jobUrl") or "",
            "descricao": re.sub(r"\s+", " ", v.get("description") or ""),
            "portal": "Gupy",
        })
    return out


# ---------- Vagas.com ----------
def _data_vagas(txt: str) -> str:
    t = txt.strip().lower()
    hoje = date.today()
    if "hoje" in t:
        return hoje.isoformat()
    if "ontem" in t:
        return (hoje - timedelta(days=1)).isoformat()
    m = re.search(r"há (\d+) dias?", t)
    if m:
        return (hoje - timedelta(days=int(m.group(1)))).isoformat()
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", t)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else ""


def _limpo(t: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", t))).strip()


def _vagas(termo: str, pagina: int) -> list[dict]:
    slug = re.sub(r"[^a-z0-9]+", "-", _sem_acento(termo.lower())).strip("-")
    pagina_html = baixar(VAGAS.format(slug=slug, pagina=pagina), navegador=True)
    out = []
    for bloco in re.findall(r'<li class="vaga[^"]*">(.*?)</li>\s*(?=<li class="vaga|</ul>)', pagina_html, re.S):
        a = re.search(r'<a class="link-detalhes-vaga" data-id-vaga="(\d+)"[^>]*title="([^"]*)"[^>]*href="([^"]+)"', bloco)
        emp = re.search(r'<span class="emprVaga">(.*?)</span>', bloco, re.S)
        if not a or not emp:
            continue
        local = re.search(r'<div class="vaga-local">(.*?)<div', bloco, re.S)
        local_txt = _limpo(local.group(1)) if local else ""
        cidade, _, uf = local_txt.partition(" / ")
        data = re.search(r'data-publicacao">(.*?)</span>', bloco, re.S)
        desc = re.search(r'<div class="detalhes">(.*?)</div>', bloco, re.S)
        out.append({
            "id": f"vagas-{a.group(1)}",
            "empresa": _limpo(emp.group(1)),
            "pagina_carreira": "",
            "cargo": htmllib.unescape(a.group(2)).strip(),
            "data": _data_vagas(_limpo(data.group(1))) if data else "",
            "cidade": cidade.strip(),
            "estado": UFS.get(uf.strip().upper(), uf.strip()),
            "modelo": "",
            "link": "https://www.vagas.com.br" + a.group(3),
            "descricao": _limpo(desc.group(1)).removeprefix("Descrição:").strip() if desc else "",
            "portal": "Vagas.com",
        })
    return out


PORTAIS = {"gupy": _gupy, "vagas": _vagas}


# ---------- histórico (crescimento entre rodadas) ----------
def _historico_anterior(termos_chave: str) -> tuple[str, dict[str, int]]:
    if not HISTORICO.exists():
        return "", {}
    with HISTORICO.open(encoding="utf-8", newline="") as f:
        linhas = [r for r in csv.DictReader(f) if r.get("termos") == termos_chave]
    hoje = date.today().isoformat()
    datas = sorted({r["data"] for r in linhas if r["data"] < hoje})
    if not datas:
        return "", {}
    ultima = datas[-1]
    return ultima, {r["chave"]: int(r["qtd_vagas"] or 0) for r in linhas if r["data"] == ultima}


def _gravar_historico(termos_chave: str, lista: list[dict]) -> None:
    hoje = date.today().isoformat()
    antigas = []
    if HISTORICO.exists():
        with HISTORICO.open(encoding="utf-8", newline="") as f:
            antigas = [r for r in csv.DictReader(f) if not (r["data"] == hoje and r["termos"] == termos_chave)]
    novas = [{"data": hoje, "termos": termos_chave, "chave": _chave(e["empresa"]),
              "empresa": e["empresa"], "qtd_vagas": e["qtd_vagas"]} for e in lista]
    gravar_csv(HISTORICO, antigas + novas, ["data", "termos", "chave", "empresa", "qtd_vagas"])


def buscar(termos, paginas=1, dias=45, uf=None, descricao=False, fontes=("gupy", "vagas"), historico=True) -> list[dict]:
    limite = (datetime.now(timezone.utc) - timedelta(days=dias)).date().isoformat()
    empresas: dict[str, dict] = {}
    vistos = set()
    for fonte in fontes:
        coletar = PORTAIS[fonte]
        for termo in termos:
            for p in range(1, max(1, min(paginas, 5)) + 1):
                try:
                    vagas = coletar(termo, p)
                except Exception as e:
                    print(f"[aviso] {fonte} falhou em '{termo}' página {p}: {e}", file=sys.stderr)
                    break
                if not vagas:
                    break
                for v in vagas:
                    if v["id"] in vistos or not v["empresa"] or OCULTA.search(v["empresa"]):
                        continue
                    vistos.add(v["id"])
                    if v["data"] and v["data"] < limite:
                        continue
                    if not _uf_ok(uf, v["estado"]):
                        continue
                    e = empresas.setdefault(_chave(v["empresa"]), {
                        "empresa": v["empresa"], "pagina_carreira": v["pagina_carreira"],
                        "qtd_vagas": 0, "portais": set(), "estruturar_do_zero": False,
                        "trecho_do_zero": "", "vagas": [],
                    })
                    e["pagina_carreira"] = e["pagina_carreira"] or v["pagina_carreira"]
                    e["qtd_vagas"] += 1
                    e["portais"].add(v["portal"])
                    m = DO_ZERO.search(v["descricao"]) or DO_ZERO.search(v["cargo"])
                    if m and not e["estruturar_do_zero"]:
                        e["estruturar_do_zero"] = True
                        txt = v["descricao"] or v["cargo"]
                        ini = max(0, m.start() - 80)
                        e["trecho_do_zero"] = "…" + txt[ini:m.end() + 80].strip() + "…"
                    item = {k: v[k] for k in ("cargo", "data", "cidade", "estado", "modelo", "link", "portal")}
                    item["termo"] = termo
                    if descricao:
                        item["descricao"] = v["descricao"][:1200]
                    e["vagas"].append(item)
                time.sleep(1.0)

    termos_chave = " | ".join(sorted(t.lower().strip() for t in termos))
    data_anterior, anterior = _historico_anterior(termos_chave) if historico else ("", {})
    lista = sorted(empresas.values(), key=lambda x: (-x["qtd_vagas"], x["empresa"]))
    for e in lista:
        e["portais"] = sorted(e["portais"])
        e["vagas"].sort(key=lambda x: x["data"], reverse=True)
        e["vaga_mais_recente"] = e["vagas"][0]["data"] if e["vagas"] else ""
        if data_anterior:
            antes = anterior.get(_chave(e["empresa"]), 0)
            e["vagas_rodada_anterior"] = antes
            e["data_rodada_anterior"] = data_anterior
            e["crescimento_vagas"] = e["qtd_vagas"] - antes
    if historico and lista:
        _gravar_historico(termos_chave, lista)
    return lista


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("termos", nargs="+")
    ap.add_argument("--paginas", type=int, default=1)
    ap.add_argument("--dias", type=int, default=45)
    ap.add_argument("--uf")
    ap.add_argument("--fontes", default="gupy,vagas")
    ap.add_argument("--descricao", action="store_true")
    ap.add_argument("--saida")
    ap.add_argument("--sem-historico", action="store_true")
    a = ap.parse_args()
    fontes = [f.strip() for f in a.fontes.split(",") if f.strip() in PORTAIS] or list(PORTAIS)
    res = buscar(a.termos, a.paginas, a.dias, a.uf, a.descricao, fontes, not a.sem_historico)
    if a.saida:
        linhas = [{
            "empresa": e["empresa"],
            "pagina_carreira": e["pagina_carreira"],
            "qtd_vagas": e["qtd_vagas"],
            "crescimento_vagas": e.get("crescimento_vagas", ""),
            "estruturar_do_zero": "sim" if e["estruturar_do_zero"] else "",
            "vaga_mais_recente": e["vaga_mais_recente"],
            "portais": " | ".join(e["portais"]),
            "cargos": " | ".join(sorted({v["cargo"] for v in e["vagas"]}))[:500],
            "cidades": " | ".join(sorted({f'{v["cidade"]}/{v["estado"]}'.strip("/") for v in e["vagas"]}))[:300],
            "link_exemplo": e["vagas"][0]["link"] if e["vagas"] else "",
        } for e in res]
        gravar_csv(Path(a.saida), linhas, list(linhas[0].keys()) if linhas else ["empresa"])
    imprimir_json({"empresas": len(res), "resultado": res})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
