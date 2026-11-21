"""Filtro anti-repetição e manutenção do histórico.

Comandos:
  python scripts/filtrar.py importar ARQUIVO.csv
      Lê a lista atual ou a exportação do CRM (qualquer CSV com uma coluna de site,
      domínio, e-mail corporativo ou nome de empresa) e grava kit/nao-abordar.csv.
      Só guarda nome da empresa e domínio. Nunca guarda dados de pessoa.

  python scripts/filtrar.py checar
      Lê kit/contas.csv e tira as contas que já estão em kit/nao-abordar.csv,
      em kit/historico.csv (rodadas anteriores) ou repetidas no próprio arquivo.
      As retiradas vão pra kit/descartadas.csv com o motivo.

  python scripts/filtrar.py arquivar
      Depois de gerar a planilha: copia as contas da rodada pra kit/historico.csv,
      pra que o /atualizar mostre só o que é novo.
"""
from __future__ import annotations

import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from comum import (COLUNAS_DESCARTADAS, IDS_CONTAS, KIT, dominio, gravar_csv,  # noqa: E402
                   ler_csv, saida_utf8)

saida_utf8()

NAO_ABORDAR = KIT / "nao-abordar.csv"
HISTORICO = KIT / "historico.csv"
CONTAS = KIT / "contas.csv"
DESCARTADAS = KIT / "descartadas.csv"

PISTAS_SITE = ("site", "website", "domain", "dominio", "domínio", "url", "web")
PISTAS_EMAIL = ("email", "e-mail", "mail")
PISTAS_NOME = ("empresa", "company", "conta", "account", "organiza", "razao", "razão", "nome fantasia", "name")
EMAIL_PESSOAL = {"gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "yahoo.com.br", "icloud.com",
                 "live.com", "bol.com.br", "uol.com.br", "terra.com.br", "msn.com"}


def _nome_normal(n: str) -> str:
    n = (n or "").lower()
    n = re.sub(r"\b(ltda|s\.?a\.?|me|epp|eireli|holding|grupo|do brasil|brasil)\b", " ", n)
    return re.sub(r"[^a-z0-9à-ú]+", "", n)


def _coluna(cabecalho, pistas):
    for c in cabecalho:
        if any(p in c.lower() for p in pistas):
            return c
    return None


def importar(arquivo: str) -> int:
    linhas = ler_csv(__import__("pathlib").Path(arquivo))
    if not linhas:
        print("Arquivo vazio ou não encontrado.")
        return 1
    cab = list(linhas[0].keys())
    c_site, c_email, c_nome = _coluna(cab, PISTAS_SITE), _coluna(cab, PISTAS_EMAIL), _coluna(cab, PISTAS_NOME)
    existentes = {(l.get("dominio") or l.get("nome_normal")) for l in ler_csv(NAO_ABORDAR)}
    novos = ler_csv(NAO_ABORDAR)
    for l in linhas:
        d = dominio(l.get(c_site, "")) if c_site else ""
        if not d and c_email:
            d = dominio(l.get(c_email, ""))
            if d in EMAIL_PESSOAL:
                d = ""
        nome = (l.get(c_nome, "") if c_nome else "").strip()
        chave = d or _nome_normal(nome)
        if not chave or chave in existentes:
            continue
        existentes.add(chave)
        novos.append({"nome_empresa": nome, "dominio": d, "nome_normal": _nome_normal(nome), "origem": "lista do usuário"})
    gravar_csv(NAO_ABORDAR, novos, ["nome_empresa", "dominio", "nome_normal", "origem"])
    print(f"{len(novos)} empresas na lista de não abordar (colunas usadas: site={c_site}, e-mail={c_email}, nome={c_nome}).")
    return 0


def checar() -> int:
    contas = ler_csv(CONTAS)
    bloqueio_dom, bloqueio_nome = set(), set()
    for origem, motivo in ((NAO_ABORDAR, "já está na sua lista ou no seu CRM"), (HISTORICO, "já entregue numa rodada anterior")):
        for l in ler_csv(origem):
            d = l.get("dominio") or dominio(l.get("site", ""))
            n = l.get("nome_normal") or _nome_normal(l.get("nome_empresa", ""))
            if d:
                bloqueio_dom.add((d, motivo))
            if n:
                bloqueio_nome.add((n, motivo))
    doms = {d: m for d, m in bloqueio_dom}
    nomes = {n: m for n, m in bloqueio_nome}
    vistos, ficam, saem = set(), [], ler_csv(DESCARTADAS)
    for c in contas:
        d, n = dominio(c.get("site", "")), _nome_normal(c.get("nome_empresa", ""))
        motivo = doms.get(d) if d else None
        motivo = motivo or (nomes.get(n) if n else None)
        if not motivo and ((d and d in vistos) or (n and n in vistos)):
            motivo = "repetida nesta rodada"
        if not c.get("nome_empresa") or not c.get("site"):
            motivo = motivo or "sem nome ou sem site (obrigatórios)"
        if motivo:
            saem.append({"nome_empresa": c.get("nome_empresa", ""), "site": c.get("site", ""), "motivo": motivo})
            continue
        vistos.update(x for x in (d, n) if x)
        ficam.append(c)
    gravar_csv(CONTAS, ficam, IDS_CONTAS)
    gravar_csv(DESCARTADAS, saem, COLUNAS_DESCARTADAS)
    print(f"Ficaram {len(ficam)} contas. Saíram {len(contas) - len(ficam)} nesta checagem.")
    return 0


def arquivar() -> int:
    hist = ler_csv(HISTORICO)
    hoje = date.today().isoformat()
    for c in ler_csv(CONTAS):
        hist.append({"nome_empresa": c.get("nome_empresa", ""), "site": c.get("site", ""),
                     "dominio": dominio(c.get("site", "")), "nome_normal": _nome_normal(c.get("nome_empresa", "")),
                     "rodada": hoje})
    gravar_csv(HISTORICO, hist, ["nome_empresa", "site", "dominio", "nome_normal", "rodada"])
    print(f"Histórico com {len(hist)} contas.")
    return 0


def main(args):
    if not args or args[0] not in ("importar", "checar", "arquivar"):
        print(__doc__)
        return 1
    if args[0] == "importar":
        if len(args) < 2:
            print("Falta o caminho do arquivo.")
            return 1
        return importar(args[1])
    return checar() if args[0] == "checar" else arquivar()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
