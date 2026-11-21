"""Consulta dados públicos de CNPJ (BrasilAPI, com a Minha Receita de reserva).

Devolve SÓ dados da empresa. Nunca devolve sócios (QSA), CPF, e-mail ou telefone,
mesmo quando a fonte traz.

Uso:
  python scripts/cnpj.py 33.000.167/0001-01
  python scripts/cnpj.py 33000167000101 11222333000181
"""
from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from comum import baixar, cnpj_valido, imprimir_json, saida_utf8, so_digitos  # noqa: E402

saida_utf8()

FONTES = [
    "https://brasilapi.com.br/api/cnpj/v1/{cnpj}",
    "https://minhareceita.org/{cnpj}",
]


def _limpar(d: dict, cnpj: str, fonte: str) -> dict:
    data = d.get("data_inicio_atividade") or ""
    return {
        "cnpj": cnpj,
        "razao_social": d.get("razao_social") or "",
        "nome_fantasia": d.get("nome_fantasia") or "",
        "cnae_codigo": str(d.get("cnae_fiscal") or ""),
        "cnae_descricao": d.get("cnae_fiscal_descricao") or "",
        "porte_receita": d.get("porte") or d.get("descricao_porte") or "",
        "municipio": d.get("municipio") or "",
        "uf": d.get("uf") or "",
        "situacao_cadastral": d.get("descricao_situacao_cadastral") or "",
        "matriz_ou_filial": d.get("descricao_identificador_matriz_filial") or "",
        "ano_abertura": data[:4],
        "capital_social": d.get("capital_social") or "",
        "fonte": fonte.split("/")[2],
    }


def consultar(cnpj: str) -> dict:
    c = so_digitos(cnpj)
    if not cnpj_valido(c):
        return {"cnpj": c, "erro": "CNPJ inválido (dígitos verificadores não batem)"}
    ultimo = ""
    for modelo in FONTES:
        url = modelo.format(cnpj=c)
        try:
            return _limpar(json.loads(baixar(url, tentativas=2)), c, url)
        except Exception as e:
            ultimo = str(e)
            continue
    return {"cnpj": c, "erro": f"não encontrado nas fontes públicas ({ultimo})"}


def main(args: list[str]) -> int:
    if not args:
        print(__doc__)
        return 1
    resultados = []
    for i, a in enumerate(args):
        if i:
            time.sleep(1.0)  # educado com as fontes gratuitas
        resultados.append(consultar(a))
    imprimir_json(resultados if len(resultados) > 1 else resultados[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
