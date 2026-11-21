"""Rotina diária: todo dia, no horário escolhido, o agente busca as empresas mais frescas
e grava uma planilha nova em saida/diario-AAAA-MM-DD.xlsx.

Usa o agendador do próprio sistema (launchd no Mac, Agendador de Tarefas no Windows).
O computador precisa estar ligado no horário. Cada rodada usa o seu plano do Claude
(ou do ChatGPT), como uma conversa normal.

Uso:
  python scripts/agendar.py criar --hora 08:00 --qtd 10 [--motor claude|codex] [--simular]
  python scripts/agendar.py status
  python scripts/agendar.py remover

--simular mostra o que seria criado, sem instalar nada.
"""
from __future__ import annotations

import argparse
import os
import platform
import plistlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from comum import DADOS, RAIZ, saida_utf8  # noqa: E402

saida_utf8()

NOME = "prospeccao-por-prompt.diario"
NOME_WIN = "Prospeccao por Prompt - diario"
PLIST = Path.home() / "Library" / "LaunchAgents" / f"com.{NOME}.plist"
LOG = DADOS / "rotina.log"
CONFIG = DADOS / "rotina.txt"


def _pedido(qtd: int) -> str:
    return (f"Rotina diária: rode o comando atualizar no modo diário com {qtd} empresas. "
            "Não faça perguntas. No fim, grave a planilha e arquive a rodada.")


def _comando_motor(motor: str, qtd: int) -> list[str]:
    if motor == "codex":
        return ["codex", "exec", "--skip-git-repo-check", "--sandbox", "workspace-write", _pedido(qtd)]
    return ["claude", "-p", _pedido(qtd)]


def _achar(motor: str) -> str | None:
    exe = "codex" if motor == "codex" else "claude"
    return shutil.which(exe)


def _script_mac(motor: str, qtd: int) -> str:
    cmd = " ".join(f"'{c}'" if " " in c else c for c in _comando_motor(motor, qtd))
    return f"""#!/bin/zsh -l
# Rotina diária do Prospecção por Prompt (criada por scripts/agendar.py).
cd "{RAIZ}" || exit 1
echo "=== $(date '+%Y-%m-%d %H:%M') ===" >> "{LOG}"
{cmd} >> "{LOG}" 2>&1
status=$?
if ls saida/diario-$(date +%Y-%m-%d).xlsx >/dev/null 2>&1; then
  osascript -e 'display notification "As empresas de hoje estão na pasta saida." with title "Prospecção por Prompt"'
else
  osascript -e 'display notification "A rodada de hoje não gerou planilha. Veja dados/rotina.log." with title "Prospecção por Prompt"'
fi
exit $status
"""


def _script_win(motor: str, qtd: int) -> str:
    exe, *resto = _comando_motor(motor, qtd)
    args = " ".join(f'"{a}"' if " " in a else a for a in resto)
    return f"""@echo off
chcp 65001 >nul
rem Rotina diária do Prospecção por Prompt (criada por scripts/agendar.py).
cd /d "{RAIZ}"
echo === %date% %time% === >> "{LOG}"
call {exe} {args} >> "{LOG}" 2>&1
"""


def _hora(txt: str) -> tuple[int, int]:
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", txt.strip())
    if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
        raise SystemExit("Hora inválida. Use o formato 08:00.")
    return int(m.group(1)), int(m.group(2))


def criar(hora: str, qtd: int, motor: str, simular: bool) -> int:
    h, m = _hora(hora)
    qtd = max(1, min(qtd, 30))
    sistema = platform.system()
    if not simular and not _achar(motor):
        print(f"Não achei o comando '{'codex' if motor == 'codex' else 'claude'}' neste computador. "
              "A rotina precisa dele instalado no terminal.")
        return 1
    DADOS.mkdir(exist_ok=True)

    if sistema == "Darwin":
        script = DADOS / "rotina.sh"
        conteudo = _script_mac(motor, qtd)
        plist = {
            "Label": f"com.{NOME}",
            "ProgramArguments": ["/bin/zsh", "-l", str(script)],
            "StartCalendarInterval": {"Hour": h, "Minute": m},
            "StandardOutPath": str(LOG),
            "StandardErrorPath": str(LOG),
        }
        if simular:
            print(f"[simulação] gravaria {script}:\n{conteudo}")
            print(f"[simulação] gravaria {PLIST}:\n{plistlib.dumps(plist).decode()}")
            return 0
        script.write_text(conteudo, encoding="utf-8")
        script.chmod(0o755)
        PLIST.parent.mkdir(parents=True, exist_ok=True)
        uid = os.getuid()
        subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(PLIST)], capture_output=True)
        PLIST.write_bytes(plistlib.dumps(plist))
        r = subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(PLIST)], capture_output=True, text=True)
        if r.returncode != 0:
            print("Não consegui ligar a rotina:", r.stderr.strip())
            return 1

    elif sistema == "Windows":
        script = DADOS / "rotina.cmd"
        conteudo = _script_win(motor, qtd)
        cmd = ["schtasks", "/Create", "/SC", "DAILY", "/ST", f"{h:02d}:{m:02d}",
               "/TN", NOME_WIN, "/TR", f'"{script}"', "/F"]
        if simular:
            print(f"[simulação] gravaria {script}:\n{conteudo}")
            print("[simulação] rodaria:", " ".join(cmd))
            return 0
        script.write_text(conteudo, encoding="utf-8")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print("Não consegui ligar a rotina:", (r.stderr or r.stdout).strip())
            return 1
    else:
        print("Neste sistema, crie a rotina pelo cron: todo dia, na pasta do agente, rode:")
        print("  " + " ".join(_comando_motor(motor, qtd)))
        return 1

    CONFIG.write_text(f"hora={h:02d}:{m:02d}\nqtd={qtd}\nmotor={motor}\n", encoding="utf-8")
    print(f"PRONTO: todo dia às {h:02d}:{m:02d}, {qtd} empresas novas em saida/diario-AAAA-MM-DD.xlsx.")
    return 0


def status() -> int:
    if CONFIG.exists():
        print("Rotina ligada:", CONFIG.read_text(encoding="utf-8").replace("\n", " ").strip())
    else:
        print("Nenhuma rotina ligada.")
    if LOG.exists():
        linhas = LOG.read_text(encoding="utf-8", errors="replace").splitlines()
        print("Últimas linhas do registro:")
        print("\n".join(linhas[-8:]))
    return 0


def remover() -> int:
    sistema = platform.system()
    if sistema == "Darwin":
        subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}", str(PLIST)], capture_output=True)
        PLIST.unlink(missing_ok=True)
        (DADOS / "rotina.sh").unlink(missing_ok=True)
    elif sistema == "Windows":
        subprocess.run(["schtasks", "/Delete", "/TN", NOME_WIN, "/F"], capture_output=True)
        (DADOS / "rotina.cmd").unlink(missing_ok=True)
    CONFIG.unlink(missing_ok=True)
    print("PRONTO: rotina desligada.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("criar")
    c.add_argument("--hora", default="08:00")
    c.add_argument("--qtd", type=int, default=10)
    c.add_argument("--motor", choices=["claude", "codex"], default="claude")
    c.add_argument("--simular", action="store_true")
    sub.add_parser("status")
    sub.add_parser("remover")
    a = ap.parse_args()
    if a.cmd == "criar":
        return criar(a.hora, a.qtd, a.motor, a.simular)
    if a.cmd == "status":
        return status()
    if a.cmd == "remover":
        return remover()
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
