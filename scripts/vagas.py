"""Busca vagas abertas no portal público da Gupy e agrupa por empresa.

Lê só a página pública de busca (a mesma que qualquer candidato vê). Não usa login.

Uso:
  python scripts/vagas.py "SDR" "gerente comercial" --paginas 2 --dias 30
  python scripts/vagas.py "analista de RH" --uf "São Paulo" --descricao

Opções:
  --paginas N   páginas por termo (12 vagas por página; padrão 1, máximo 5)
  --dias N      só vagas publicadas nos últimos N dias (padrão 45)
  --uf NOME     filtra pelo estado escrito por extenso, ex.: "Minas Gerais"
  --descricao   inclui os primeiros 1.200 caracteres da descrição (pra achar ferramentas citadas)
  --saida ARQ   grava também um CSV com uma linha por empresa (ex.: kit/vagas.csv)

Saída: JSON com uma entrada por empresa (nome, página de carreira, vagas, datas, cidades).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(__file__))
from comum import baixar, gravar_csv, imprimir_json, saida_utf8  # noqa: E402

saida_utf8()

BUSCA = "https://portal.gupy.io/job-search/term={termo}&page={pagina}"
PADRAO_DADOS = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)


def _pagina(termo: str, pagina: int) -> list[dict]:
    url = BUSCA.format(termo=urllib.parse.quote(termo), pagina=pagina)
    html = baixar(url, navegador=True)
    m = PADRAO_DADOS.search(html)
    if not m:
        return []
    props = json.loads(m.group(1)).get("props", {}).get("pageProps", {})
    return props.get("initialJobList", {}).get("data", []) or []


def _carreira(job_url: str) -> str:
    host = urllib.parse.urlparse(job_url or "").netloc
    return f"https://{host}" if host else ""


def buscar(termos, paginas=1, dias=45, uf=None, descricao=False) -> list[dict]:
    limite = datetime.now(timezone.utc) - timedelta(days=dias)
    empresas: dict[str, dict] = {}
    vistos = set()
    for termo in termos:
        for p in range(1, max(1, min(paginas, 5)) + 1):
            try:
                vagas = _pagina(termo, p)
            except Exception as e:
                print(f"[aviso] falhou '{termo}' página {p}: {e}", file=sys.stderr)
                break
            if not vagas:
                break
            for v in vagas:
                if v.get("id") in vistos:
                    continue
                vistos.add(v.get("id"))
                data_txt = v.get("publishedDate") or ""
                try:
                    data = datetime.fromisoformat(data_txt.replace("Z", "+00:00"))
                except ValueError:
                    data = None
                if data and data < limite:
                    continue
                if uf and (v.get("state") or "").lower() != uf.lower():
                    continue
                nome = (v.get("careerPageName") or "").strip()
                if not nome:
                    continue
                e = empresas.setdefault(nome.lower(), {
                    "empresa": nome,
                    "pagina_carreira": _carreira(v.get("jobUrl")),
                    "qtd_vagas": 0,
                    "vagas": [],
                })
                e["qtd_vagas"] += 1
                item = {
                    "cargo": (v.get("name") or "").strip(),
                    "data": data_txt[:10],
                    "cidade": v.get("city") or "",
                    "estado": v.get("state") or "",
                    "modelo": v.get("workplaceType") or "",
                    "link": v.get("jobUrl") or "",
                    "termo": termo,
                }
                if descricao:
                    item["descricao"] = re.sub(r"\s+", " ", v.get("description") or "")[:1200]
                e["vagas"].append(item)
            time.sleep(1.0)
    lista = sorted(empresas.values(), key=lambda x: (-x["qtd_vagas"], x["empresa"]))
    for e in lista:
        e["vagas"].sort(key=lambda x: x["data"], reverse=True)
        e["vaga_mais_recente"] = e["vagas"][0]["data"] if e["vagas"] else ""
    return lista


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("termos", nargs="+")
    ap.add_argument("--paginas", type=int, default=1)
    ap.add_argument("--dias", type=int, default=45)
    ap.add_argument("--uf")
    ap.add_argument("--descricao", action="store_true")
    ap.add_argument("--saida")
    a = ap.parse_args()
    res = buscar(a.termos, a.paginas, a.dias, a.uf, a.descricao)
    if a.saida:
        linhas = [{
            "empresa": e["empresa"],
            "pagina_carreira": e["pagina_carreira"],
            "qtd_vagas": e["qtd_vagas"],
            "vaga_mais_recente": e["vaga_mais_recente"],
            "cargos": " | ".join(sorted({v["cargo"] for v in e["vagas"]}))[:500],
            "cidades": " | ".join(sorted({f'{v["cidade"]}/{v["estado"]}'.strip("/") for v in e["vagas"]}))[:300],
            "link_exemplo": e["vagas"][0]["link"] if e["vagas"] else "",
        } for e in res]
        from pathlib import Path
        gravar_csv(Path(a.saida), linhas, list(linhas[0].keys()) if linhas else ["empresa"])
    imprimir_json({"empresas": len(res), "resultado": res})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
