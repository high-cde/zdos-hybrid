#!/usr/bin/env python3
"""apply-parrot-theme.py — riallinea la palette delle interfacce ZDOS Hybrid
all'identità visiva di **Parrot OS 7 «Echo»**.

Perché uno script e non una modifica a mano: la palette Kali-teal (`#00ffcc`) e
le tinte GitHub-dark erano duplicate in nove file, più i blocchi heredoc di
`zdos-autobuild.sh` che li rigenerano. Una mappatura esplicita rende la modifica
ripetibile, verificabile e reversibile.

Fonti dei colori di destinazione:
  * simple-icons, "Parrot Security" — colore di marca `#15E0ED`.
  * parrotsec.org — `#00FFF0`, `#00D3F2`, `#00B8DB`, `#02ABB5`, `#0A0118`,
    `#06043E`, `#0F0A1E`, `#8799B5`.

Uso:
    python3 tools/apply-parrot-theme.py            # applica
    python3 tools/apply-parrot-theme.py --check    # mostra solo i colori residui
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TARGETS = [
    "zdos_omni_os.py",
    "z_kali_ui.py",
    "z_kali_sovereign.py",
    "z_kali_megadrive.py",
    "z_kali_ruby_city.py",
    "zdos_master_dashboard.py",
    "interface/glass/core_ui.py",
    "webapp/assets/style.css",
    "zdos-autobuild.sh",
]

# vecchio colore -> nuovo colore (Parrot OS 7 «Echo»)
MAP = {
    # --- fondi ---------------------------------------------------------
    "#020408": "#030109",
    "#030509": "#04010F",
    "#03060f": "#04010F",
    "#05070b": "#04010F",
    "#07090e": "#04010F",
    "#080b10": "#06031A",
    "#090d16": "#05020F",
    "#0a0d14": "#06031A",
    "#0a101d": "#080522",
    "#080c16": "#090624",
    "#080e1c": "#090624",
    "#0c1424": "#0B0626",
    "#0c0c14": "#08041B",
    "#0d1117": "#0F0A1E",
    "#0d111a": "#0D0A22",
    "#0e1117": "#0F0A1E",
    "#111827": "#0D0A22",
    "#121212": "#0A0118",
    "#121824": "#131038",
    "#161b22": "#131038",
    "#0f172a": "#0A0118",
    # --- superfici e bordi ---------------------------------------------
    "#161f30": "#16123F",
    "#1a2234": "#1B1647",
    "#1e293b": "#252A52",
    "#1e1e1e": "#0F0A1E",
    "#21262d": "#16123F",
    "#222d42": "#222A55",
    "#273447": "#2A3060",
    "#2d2d2d": "#131038",
    "#334155": "#2F3668",
    "#3d3d3d": "#1B1647",
    "#475569": "#3A4275",
    "#1e1b4b": "#1A1650",
    "#1e3a8a": "#06304F",
    "#1f4037": "#0B3B4A",
    # --- accenti --------------------------------------------------------
    "#00ffcc": "#15E0ED",   # teal Kali -> ciano Parrot
    "#34d399": "#3DDC97",
    "#3fb950": "#3DDC97",
    "#6ee7b7": "#5CF2C0",
    "#38bdf8": "#00D3F2",
    "#60a5fa": "#4FE9FF",
    "#58a6ff": "#15E0ED",
    "#3b82f6": "#00B8DB",
    "#a855f7": "#7C3AED",
    "#c084fc": "#9B6BFF",
    "#d29922": "#FEBE2D",
    "#fbbf24": "#FFC857",
    # --- testo ----------------------------------------------------------
    "#8a99ad": "#8799B5",
    "#8b949e": "#8E9FBB",
    "#94a3b8": "#A9BCD6",
    "#64748b": "#6F7F9E",
    "#c9d1d9": "#D6E6F5",
    "#cbd5e1": "#C3D4E6",
    "#e0e6ed": "#EAF6FF",
    "#e2e8f0": "#EAF6FF",
}

HEX = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")

# Colori considerati validi in uscita: bianco/nero puri usati per il contrasto
# sui fondi ciano, i valori della palette Parrot e le relative varianti alpha.
def allowed_colors() -> set[str]:
    allowed = {"#ffffff", "#000000"}
    try:
        import sys

        sys.path.insert(0, str(ROOT))
        from parrot_theme import P

        allowed |= {value.lower() for value in P.values()}
    except Exception:  # pragma: no cover - il check resta utile anche senza il modulo
        pass
    allowed |= {value.lower() for value in MAP.values()}
    allowed |= {color + alpha for color in list(allowed) for alpha in ("22", "33", "55")}
    return allowed


# Righe di documentazione che citano i colori *sorgente*: restano intatte.
DOC_MARKERS = ("parrotsec.org", "simple-icons", "palette di riferimento", "fonti dei codici")


def _convert_line(text: str) -> tuple[str, int]:
    hits = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal hits
        raw = match.group(0)
        low = raw.lower()
        if low in MAP:
            hits += 1
            return MAP[low]
        if len(raw) == 7 and low[:7] + "22" in MAP:  # es. #00ffcc22 (alpha)
            base = MAP[low]
            hits += 1
            return base + raw[7:]
        if len(raw) == 9 and low[:7] in MAP:
            hits += 1
            return MAP[low[:7]] + raw[7:]
        return raw

    return HEX.sub(repl, text), hits


def convert(text: str) -> tuple[str, int]:
    hits = 0
    lines = []
    for line in text.splitlines(keepends=True):
        low = line.lower()
        if any(marker in low for marker in DOC_MARKERS):
            lines.append(line)
            continue
        converted, found = _convert_line(line)
        hits += found
        lines.append(converted)
    return "".join(lines), hits


def main() -> int:
    check_only = "--check" in sys.argv
    allowed = allowed_colors()
    total = 0
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            print(f"  ·  {rel} (assente, saltato)")
            continue
        original = path.read_text(encoding="utf-8")
        updated, hits = convert(original)
        total += hits
        if check_only:
            leftovers = {
                c.lower()
                for c in HEX.findall(updated)
                if c.lower() not in allowed
            }
            print(f"  {'!' if leftovers else '✓'}  {rel}: {hits} sostituzioni, "
                  f"{len(leftovers)} colori fuori palette")
            continue
        if updated != original:
            path.write_text(updated, encoding="utf-8")
        print(f"  ✓  {rel}: {hits} colori riallineati")
    print(f"\n  Totale: {total} occorrenze")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
