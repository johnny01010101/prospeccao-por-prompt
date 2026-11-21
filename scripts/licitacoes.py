"""Contratos públicos ganhos (PNCP, Portal Nacional de Contratações Públicas).

Empresa que acabou de ganhar contrato público tem dinheiro novo e costuma contratar
e comprar. Fonte pública e gratuita, sem login.

Uso:
  python scripts/licitacoes.py checar 00.000.000/0001-00 [--dias 120]
      Contratos que essa empresa ganhou nos últimos N dias: quantos, valor somado,
      o maior (órgão, objeto, data e link).

  python scripts/licitacoes.py descobrir "termo do setor" [--dias 30] [--valor-minimo 100000] [--uf SP] [--paginas 2]
      Empresas que ganharam contratos com esse termo no objeto, agrupadas por CNPJ.
      Bom pra achar contas novas num setor (ex.: "software", "manutenção predial").

Saída: JSON. Só dados de empresa (fornecedores pessoa física são ignorados).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from comum import baixar, cnpj_valido, imprimir_json, saida_utf8, so_digitos  # noqa: E402

saida_utf8()

BUSCA = ("https://pncp.gov.br/api/search/?q={q}&tipos_documento=contrato&ordenacao=-data"
         "&pagina={p}&tam_pagina=50&status=todos")
LINK = "https://pncp.gov.br/app{item}"


def _data(item: dict) -> str:
    return (item.get("data_assinatura") or item.get("data_publicacao_pncp") or "")[:10]


def _pagina(q: str, p: int) -> list[dict]:
    url = BUSCA.format(q=urllib.parse.quote(q), p=p)
    return json.loads(baixar(url, navegador=True)).get("items", []) or []


def _contrato(i: dict) -> dict:
    return {
        "data": _data(i),
        "valor": float(i.get("valor_global") or 0),
        "orgao": i.get("orgao_nome") or "",
        "uf": i.get("uf") or "",
        "objeto": (i.get("description") or "")[:200],
        "link": LINK.format(item=i.get("item_url") or ""),
    }


def checar(cnpj: str, dias: int) -> dict:
    c = so_digitos(cnpj)
    if not cnpj_valido(c):
        return {"cnpj": c, "erro": "CNPJ inválido"}
    limite = (date.today() - timedelta(days=dias)).isoformat()
    achados = []
    paginas_lidas = 0
    for p in (1, 2, 3):
        try:
            itens = _pagina(c, p)
        except Exception as e:
            return {"cnpj": c, "erro": f"PNCP indisponível agora ({e})"}
        if not itens:
            break
        paginas_lidas = p
        novos = [i for i in itens if so_digitos(i.get("fornecedor_ni") or "") == c]
        achados += [_contrato(i) for i in novos if _data(i) >= limite and not i.get("cancelado")]
        if itens and _data(itens[-1]) < limite:
            break
        time.sleep(1.0)
    achados.sort(key=lambda x: x["valor"], reverse=True)
    return {
        "cnpj": c,
        "dias": dias,
        "qtd_contratos": len(achados),
        "pode_ter_mais": paginas_lidas == 3 and len(achados) >= 100,
        "valor_total": round(sum(x["valor"] for x in achados), 2),
        "maior": achados[0] if achados else None,
        "mais_recente": max(achados, key=lambda x: x["data"]) if achados else None,
    }


def descobrir(termo: str, dias: int, minimo: float, uf: str | None, paginas: int) -> list[dict]:
    limite = (date.today() - timedelta(days=dias)).isoformat()
    empresas: dict[str, dict] = {}
    for p in range(1, max(1, min(paginas, 5)) + 1):
        try:
            itens = _pagina(termo, p)
        except Exception as e:
            print(f"[aviso] PNCP falhou na página {p}: {e}", file=sys.stderr)
            break
        if not itens:
            break
        for i in itens:
            ni = so_digitos(i.get("fornecedor_ni") or "")
            if len(ni) != 14 or i.get("cancelado") or _data(i) < limite:
                continue
            if uf and (i.get("uf") or "").upper() != uf.upper():
                continue
            e = empresas.setdefault(ni, {"cnpj": ni, "empresa": i.get("fornecedor_nome") or "",
                                         "qtd_contratos": 0, "valor_total": 0.0, "contratos": []})
            ct = _contrato(i)
            e["qtd_contratos"] += 1
            e["valor_total"] += ct["valor"]
            e["contratos"].append(ct)
        if _data(itens[-1]) < limite:
            break
        time.sleep(1.0)
    lista = [e for e in empresas.values() if e["valor_total"] >= minimo]
    for e in lista:
        e["valor_total"] = round(e["valor_total"], 2)
        e["contratos"].sort(key=lambda x: x["valor"], reverse=True)
        e["contratos"] = e["contratos"][:3]
    return sorted(lista, key=lambda e: -e["valor_total"])


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    a = sub.add_parser("checar"); a.add_argument("cnpjs", nargs="+"); a.add_argument("--dias", type=int, default=120)
    b = sub.add_parser("descobrir"); b.add_argument("termo"); b.add_argument("--dias", type=int, default=30)
    b.add_argument("--valor-minimo", type=float, default=100000); b.add_argument("--uf"); b.add_argument("--paginas", type=int, default=2)
    args = ap.parse_args()
    if args.cmd == "checar":
        res = []
        for n, c in enumerate(args.cnpjs):
            if n:
                time.sleep(1.0)
            res.append(checar(c, args.dias))
        imprimir_json(res if len(res) > 1 else res[0])
    elif args.cmd == "descobrir":
        res = descobrir(args.termo, args.dias, args.valor_minimo, args.uf, args.paginas)
        imprimir_json({"empresas": len(res), "resultado": res})
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
