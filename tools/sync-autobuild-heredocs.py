#!/usr/bin/env python3
"""sync-autobuild-heredocs.py — mantiene allineati i file generati e i blocchi
heredoc di `zdos-autobuild.sh`.

`zdos-autobuild.sh` ricrea `webapp/index.html`, `webapp/assets/style.css`,
`webapp/assets/app.js` e `parrot_theme.py`: senza sincronizzazione i due lati
divergono e l'avvio via autobuild produce un'interfaccia diversa da quella del
repository (drift già osservato per `zdos_omni_os.py`).

Uso:
    python3 tools/sync-autobuild-heredocs.py            # riscrive i blocchi
    python3 tools/sync-autobuild-heredocs.py --check    # verifica senza scrivere
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "zdos-autobuild.sh"

# (file sorgente, destinazione nel generatore)
PAIRS = [
    ("webapp/index.html", "webapp/index.html"),
    ("webapp/assets/style.css", "webapp/assets/style.css"),
    ("webapp/assets/app.js", "webapp/assets/app.js"),
    ("parrot_theme.py", "parrot_theme.py"),
]


def block_pattern(target: str) -> re.Pattern[str]:
    return re.compile(
        r"^(cat << '(?:EOT|EOF)' > " + re.escape(target) + r"\n)(.*?)^((?:EOT|EOF))$",
        re.DOTALL | re.MULTILINE,
    )


def main() -> int:
    check_only = "--check" in sys.argv
    script = SCRIPT.read_text(encoding="utf-8")
    original = script
    status = 0

    for source, target in PAIRS:
        src = ROOT / source
        if not src.exists():
            print(f"  ·  {source}: assente")
            continue
        body = src.read_text(encoding="utf-8").rstrip("\n")
        pattern = block_pattern(target)
        match = pattern.search(script)
        if not match:
            print(f"  ·  {target}: nessun blocco heredoc (aggiunta non necessaria)")
            continue
        current = match.group(2).rstrip("\n")
        if current == body:
            print(f"  ✓  {target}: già allineato")
            continue
        status = 1 if check_only else status
        if check_only:
            print(f"  !  {target}: disallineato rispetto a {source}")
            continue
        script = pattern.sub(
            lambda m: m.group(1) + (body + "\n" if body else "") + m.group(3),
            script,
            count=1,
        )
        print(f"  ✓  {target}: riscritto da {source}")

    if not check_only and script != original:
        SCRIPT.write_text(script, encoding="utf-8")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
