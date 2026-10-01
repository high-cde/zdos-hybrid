#!/usr/bin/env python3
"""zdos-zk — avvio della ZDOS Hybrid Security Workstation (Parrot Edition).

Punto d'ingresso unico dell'interfaccia ibrida:
  1. risolve la radice del progetto (ZDOS_ROOT → ~/zdos-organism → directory dello script);
  2. avvia opzionalmente il Node Pulse ZComm (porta 8787) del microcosmo;
  3. apre il Glass Engine Tkinter con l'identità visiva Parrot OS.

Esempi:
    python3 zdos_zk_launch.py
    ZDOS_ROOT=~/zdos-organism python3 zdos_zk_launch.py --no-node
    python3 zdos_zk_launch.py --check
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ACCENT = "\033[38;2;21;224;237m"
NEON = "\033[38;2;0;255;240m"
MUTED = "\033[38;2;135;153;181m"
OK = "\033[38;2;61;220;151m"
WARN = "\033[38;2;255;200;87m"
BAD = "\033[38;2;255;92;122m"
RESET = "\033[0m"
BOLD = "\033[1m"

WIDTH = 62
INNER = WIDTH - 2
ANSI = re.compile(r"\033\[[0-9;]*m")


def line(text: str = "", color: str = ACCENT) -> None:
    """Riga del banner: il padding ignora i codici ANSI."""
    visible = ANSI.sub("", text)
    padding = " " * max(0, INNER - 2 - len(visible))
    print(f"  {color}║{RESET} {text}{padding} {color}║{RESET}")


def banner() -> None:
    rule = "═" * INNER
    top = f"  {ACCENT}╔{rule}╗{RESET}"
    bottom = f"  {ACCENT}╚{rule}╝{RESET}"
    print()
    print(top)
    line(f"{BOLD}{NEON}ZDOS HYBRID · PARROT EDITION{RESET}", ACCENT)
    line(f"{MUTED}Security Workstation · ZComm · Evidence Chain{RESET}", ACCENT)
    line(f"{MUTED}identità visiva: Parrot OS 7 «Echo»{RESET}", ACCENT)
    print(bottom)
    print()


def resolve_root(explicit: str | None) -> Path:
    """Radice del progetto: nessun percorso assoluto hard-coded."""
    candidates = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    if os.environ.get("ZDOS_ROOT"):
        candidates.append(Path(os.environ["ZDOS_ROOT"]).expanduser())
    candidates.append(Path.home() / "zdos-organism")
    candidates.append(Path(__file__).resolve().parent)
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    return (Path.home() / "zdos-organism").resolve()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Avvio della ZDOS Hybrid Security Workstation (Parrot Edition).",
    )
    parser.add_argument("--root", help="radice dell'ecosistema (default: ~/zdos-organism)")
    parser.add_argument("--no-node", action="store_true", help="non avviare il Node Pulse in background")
    parser.add_argument("--check", action="store_true", help="verifica i prerequisiti ed esci")
    args = parser.parse_args()

    banner()
    root = resolve_root(args.root)
    ui_path = root / "zdos_omni_os.py"
    node_script = root / "zdos-microcosm-beta" / "node" / "zdos-node.ts"

    print(f"  {MUTED}root       {RESET} {root}")
    print(f"  {MUTED}glass      {RESET} {'✓' if ui_path.exists() else '✗'} {ui_path}")
    print(f"  {MUTED}node pulse {RESET} {'✓' if node_script.exists() else '·'} {node_script}")

    if not ui_path.exists():
        print(f"\n  {BAD}✗ Glass Engine non trovato.{RESET}")
        print(f"  {MUTED}Esegui prima: {RESET}bash zdos-autobuild.sh  {MUTED}oppure imposta ZDOS_ROOT.{RESET}\n")
        return 2

    if args.check:
        print(f"\n  {OK}Prerequisiti verificati.{RESET}\n")
        return 0

    server_process = None
    if not args.no_node and node_script.exists():
        print(f"\n  {ACCENT}▸{RESET} Node Pulse ZComm in background (porta 8787)…")
        try:
            server_process = subprocess.Popen(
                ["npx", "tsx", "node/zdos-node.ts"],
                cwd=str(node_script.parent.parent),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as exc:  # pragma: no cover - dipende dall'ambiente
            print(f"  {WARN}! Node Pulse non avviato: {exc}{RESET}")
        time.sleep(1)

    try:
        print(f"  {ACCENT}▸{RESET} Apertura Glass Engine (interfaccia Parrot Edition)…\n")
        subprocess.run([sys.executable, str(ui_path)], cwd=str(root), check=False)
    except KeyboardInterrupt:
        print(f"\n  {WARN}! Interruzione utente.{RESET}")
    finally:
        if server_process:
            print(f"  {MUTED}▸ chiusura servizi in background…{RESET}")
            server_process.terminate()
            server_process.wait()
        print(f"  {OK}✓ Sessione ZDOS conclusa in sicurezza.{RESET}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
