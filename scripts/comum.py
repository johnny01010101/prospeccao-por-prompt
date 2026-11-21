"""Funções comuns do agente de Prospecção por Prompt. Só biblioteca padrão do Python (3.9+).

Funciona igual no Windows e no Mac.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
SAIDA = RAIZ / "saida"

# Link do próximo passo dentro do agente e da planilha: cadastro direto do trial
# (50 créditos, 7 dias, sem cartão). Quem chega aqui já usou o agente.
# Fora do agente (PDF, e-mail, README, LP) o link é https://fulgurite.io.
FULGURITE_URL = "https://app.fulgurite.io/signup"
UTM = "utm_source=prospeccao-por-prompt&utm_medium=agente&utm_campaign=prospeccao-por-prompt"

AGENTE = "Mozilla/5.0 (compatible; prospeccao-por-prompt/1.0)"
NAVEGADOR = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130 Safari/537.36"
)

# Colunas da aba "contas". As duas primeiras são as únicas obrigatórias
# pra importar na fulgurite.
COLUNAS_CONTAS = [
    ("nome_empresa", "Nome da empresa"),
    ("site", "Site"),
    ("faixa", "Faixa"),
    ("nota", "Nota (0-100)"),
    ("por_que_agora", "Por que agora"),
    ("sinal1_tipo", "Sinal 1: tipo"),
    ("sinal1_resumo", "Sinal 1: resumo"),
    ("sinal1_data", "Sinal 1: data"),
    ("sinal1_link", "Sinal 1: link"),
    ("sinal2_tipo", "Sinal 2: tipo"),
    ("sinal2_resumo", "Sinal 2: resumo"),
    ("sinal2_data", "Sinal 2: data"),
    ("sinal2_link", "Sinal 2: link"),
    ("sinal3_tipo", "Sinal 3: tipo"),
    ("sinal3_resumo", "Sinal 3: resumo"),
    ("sinal3_data", "Sinal 3: data"),
    ("sinal3_link", "Sinal 3: link"),
    ("qtd_sinais", "Qtd. de sinais"),
    ("vagas_comerciais", "Vagas comerciais abertas"),
    ("ferramentas_citadas", "Ferramentas ou concorrentes citados"),
    ("noticia_titulo", "Notícia recente"),
    ("noticia_data", "Notícia: data"),
    ("noticia_link", "Notícia: link"),
    ("o_que_vende", "O que a empresa vende"),
    ("setor_cnae", "Setor / CNAE"),
    ("porte", "Porte (estimado)"),
    ("cidade_uf", "Cidade / UF"),
    ("cnpj", "CNPJ"),
    ("razao_social", "Razão social"),
    ("situacao_cadastral", "Situação cadastral"),
    ("ano_abertura", "Ano de abertura"),
    ("area_decisora", "Área que decide"),
    ("cargo_decisor", "Cargo provável de quem decide"),
    ("fulgurite", "Quem decide e o contato"),
    ("encaixe_icp", "Encaixe com o ICP"),
    ("alertas", "Alertas"),
    ("observado_inferido", "Observado ou inferido"),
    ("verificado_em", "Verificado em"),
    ("proximo_passo", "Próximo passo sugerido"),
]
IDS_CONTAS = [c for c, _ in COLUNAS_CONTAS]
COLUNAS_DESCARTADAS = ["nome_empresa", "site", "motivo"]


def saida_utf8() -> None:
    """Evita erro de acento no terminal do Windows."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8")
        except Exception:
            pass


def baixar(url: str, navegador: bool = False, tentativas: int = 3, espera: float = 2.0) -> str:
    cabecalho = {"User-Agent": NAVEGADOR if navegador else AGENTE, "Accept-Language": "pt-BR,pt;q=0.9"}
    erro = None
    for n in range(tentativas):
        try:
            req = urllib.request.Request(url, headers=cabecalho)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            erro = e
            if e.code in (404, 400):
                raise
            time.sleep(espera * (n + 1))
        except Exception as e:  # rede instável
            erro = e
            time.sleep(espera * (n + 1))
    raise RuntimeError(f"não consegui baixar {url}: {erro}")


def dominio(valor: str) -> str:
    """Normaliza site ou e-mail corporativo em domínio: 'https://www.Acme.com.br/x' -> 'acme.com.br'."""
    if not valor:
        return ""
    v = valor.strip().lower()
    if "@" in v and "/" not in v:
        v = v.split("@", 1)[1]
    if "://" not in v:
        v = "http://" + v
    host = urllib.parse.urlparse(v).netloc.split(":")[0]
    return host[4:] if host.startswith("www.") else host


def so_digitos(texto: str) -> str:
    return re.sub(r"\D", "", texto or "")


def cnpj_valido(cnpj: str) -> bool:
    c = so_digitos(cnpj)
    if len(c) != 14 or c == c[0] * 14:
        return False
    def dv(base: str, pesos: list[int]) -> str:
        s = sum(int(d) * p for d, p in zip(base, pesos)) % 11
        return "0" if s < 2 else str(11 - s)
    p1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    p2 = [6] + p1
    return c[12] == dv(c[:12], p1) and c[13] == dv(c[:12] + c[12], p2)


def ler_csv(caminho: Path) -> list[dict]:
    if not caminho.exists():
        return []
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        amostra = f.read(4096)
        f.seek(0)
        try:
            dialeto = csv.Sniffer().sniff(amostra, delimiters=",;\t")
        except csv.Error:
            dialeto = csv.excel
        return [dict(l) for l in csv.DictReader(f, dialect=dialeto)]


def gravar_csv(caminho: Path, linhas: list[dict], colunas: list[str]) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=colunas, extrasaction="ignore")
        w.writeheader()
        for l in linhas:
            w.writerow({c: l.get(c, "") for c in colunas})


def imprimir_json(dado) -> None:
    print(json.dumps(dado, ensure_ascii=False, indent=2))


def link_fulgurite(conteudo: str = "planilha") -> str:
    return f"{FULGURITE_URL}?{UTM}&utm_content={urllib.parse.quote(conteudo)}"


os.environ.setdefault("PYTHONIOENCODING", "utf-8")
