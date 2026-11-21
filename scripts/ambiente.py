"""Confere se a máquina está pronta pra rodar o Radar de Contas.

Uso:  python scripts/ambiente.py
Imprime PRONTO no fim quando estiver tudo certo.
"""
from __future__ import annotations

import platform
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
from comum import KIT, SAIDA, baixar, saida_utf8  # noqa: E402

saida_utf8()


def main() -> int:
    ok = True
    print(f"Sistema: {platform.system()} {platform.release()}")

    v = sys.version_info
    if v < (3, 9):
        print(f"[falta] Python 3.9 ou mais novo (encontrado {v.major}.{v.minor}).")
        ok = False
    else:
        print(f"[ok] Python {v.major}.{v.minor}.{v.micro}")

    for pasta in (KIT, SAIDA):
        pasta.mkdir(exist_ok=True)
    print("[ok] Pastas kit/ e saida/ prontas")

    testes = {
        "consulta pública de CNPJ": "https://brasilapi.com.br/api/cnpj/v1/33000167000101",
        "portal de vagas": "https://portal.gupy.io/job-search/term=vendas",
    }
    for nome, url in testes.items():
        try:
            baixar(url, navegador="gupy" in url, tentativas=2)
            print(f"[ok] Acesso: {nome}")
        except Exception as e:
            print(f"[aviso] Sem acesso: {nome} ({e})")
            print("        O kit continua funcionando pela busca na web do Claude, só fica mais lento.")

    if ok:
        print("\nPRONTO")
        return 0
    print("\nAinda falta instalar o Python. Veja INSTALAR.md.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
