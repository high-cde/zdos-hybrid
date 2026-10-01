"""parrot_theme.py — Design system "Parrot OS" per l'interfaccia ZDOS Hybrid.

Identità visiva allineata a **Parrot OS 7 «Echo»** (KDE Plasma 6, temi Flat Remix
+ Sweet Mars): fondo notte viola-ink, ciano di marca, neon per gli stati attivi.

Fonti dei codici colore (verificabili):
  * simple-icons, voce "Parrot Security" — colore ufficiale di marca `#15E0ED`.
  * palette pubblica di parrotsec.org — `#00FFF0`, `#00D3F2`, `#00B8DB`,
    `#02ABB5`, `#0A0118`, `#06043E`, `#0F0A1E`, `#0A0A1F`, `#8799B5`.

Il modulo è volutamente senza dipendenze: viene importato dalle interfacce
Tkinter (`zdos_omni_os.py`, `z_kali_*.py`, `zdos_master_dashboard.py`) e usato
dai generatori di script. Se il file non è presente, le interfacce ricadono
sulla palette inline di fallback.
"""

from __future__ import annotations

# --- Palette --------------------------------------------------------------

P = {
    # Fondi (notte Parrot)
    "bg_deep": "#04010F",   # sfondo applicazione, livello 0
    "bg": "#0A0118",        # sfondo base di marca
    "panel": "#0F0A1E",     # pannelli e finestre
    "panel_alt": "#131038",  # pannelli sollevati
    "surface": "#06043E",   # barre, sidebar, header (indaco profondo)
    "surface_alt": "#16123F",
    "raised": "#1B1647",    # hover / bottoni neutri
    "canvas_sky": "#06043E",
    "night_alt": "#0A0A1F",   # grigio-notte della palette pubblica parrotsec.org
    # Bordi
    "border": "#1D2B4B",
    "border_hi": "#252A52",
    "border_soft": "#2A3060",
    # Testo
    "text": "#EAF6FF",
    "text_soft": "#D6E6F5",
    "text_muted": "#8799B5",  # grigio-azzurro Parrot
    "text_dim": "#6F7F9E",
    # Ciano di marca e derivati
    "cyan": "#15E0ED",        # colore ufficiale Parrot Security
    "cyan_hi": "#00FFF0",     # neon, elemento attivo
    "cyan_mid": "#00D3F2",
    "cyan_dim": "#00B8DB",
    "teal": "#02ABB5",
    "teal_deep": "#0B3B4A",
    # Secondari
    "violet": "#7C3AED",      # Sweet Mars
    "violet_soft": "#9B6BFF",
    # Stati
    "ok": "#3DDC97",
    "warn": "#FFC857",
    "alert": "#FF5C7A",
    "gold": "#FEBE2D",
    # Contrasto su ciano
    "on_cyan": "#000000",
}

# Alias brevi usati nei file Tkinter.
BG = P["bg"]
BG_DEEP = P["bg_deep"]
PANEL = P["panel"]
SURFACE = P["surface"]
BORDER = P["border"]
TEXT = P["text"]
MUTED = P["text_muted"]
CYAN = P["cyan"]
CYAN_HI = P["cyan_hi"]

# --- Tipografia -----------------------------------------------------------

FONTS = {
    "ui": ("Ubuntu", 10),
    "ui_bold": ("Ubuntu", 10, "bold"),
    "ui_small": ("Ubuntu", 9),
    "brand": ("Ubuntu", 11, "bold"),
    "mono": ("JetBrains Mono", 9),
    "mono_small": ("Consolas", 9),
    "mono_bold": ("Consolas", 9, "bold"),
}
# Nota: se il font non è installato Tkinter ripiega automaticamente sul default;
# l'ordine consigliato su Ubuntu è Ubuntu → JetBrains Mono → Consolas.

# --- Componenti testuali --------------------------------------------------

BRAND = "ZDOS HYBRID"
EDITION = "Parrot Edition"
TAGLINE = "Security Workstation · ZComm · Evidence Chain · Node Pulse"

RULES = {
    "top": "╔" + "═" * 58 + "╗",
    "mid": "╟" + "─" * 58 + "╢",
    "bottom": "╚" + "═" * 58 + "╝",
}


def banner(subtitle: str = TAGLINE, width: int = 58) -> str:
    """Banner ASCII coerente con l'identità Parrot, per la CLI."""
    lines = [
        "╔" + "═" * width + "╗",
        "║" + f"  ▸ {BRAND} · {EDITION}".ljust(width) + "║",
        "║" + f"    {subtitle}".ljust(width) + "║",
        "╚" + "═" * width + "╝",
    ]
    return "\n".join(lines)


def ansi(text: str, color: str = "cyan", bold: bool = False) -> str:
    """Colora una stringa per il terminale usando la palette Parrot."""
    codes = {
        "cyan": "38;2;21;224;237",
        "cyan_hi": "38;2;0;255;240",
        "muted": "38;2;135;153;181",
        "ok": "38;2;61;220;151",
        "warn": "38;2;255;200;87",
        "alert": "38;2;255;92;122",
        "violet": "38;2;124;58;237",
    }
    prefix = "\033[1m" if bold else ""
    return f"{prefix}\033[{codes.get(color, codes['cyan'])}m{text}\033[0m"


def export_tokens() -> dict:
    """Token esportabili (usati anche da `assets/theme/parrot-tokens.json`)."""
    return {
        "name": "Parrot OS 7 Echo — ZDOS Hybrid identity",
        "palette": P,
        "fonts": {k: list(v) for k, v in FONTS.items()},
        "css": {
            "--parrot-bg-deep": P["bg_deep"],
            "--parrot-bg": P["bg"],
            "--parrot-panel": P["panel"],
            "--parrot-panel-alt": P["panel_alt"],
            "--parrot-surface": P["surface"],
            "--parrot-raised": P["raised"],
            "--parrot-border": P["border"],
            "--parrot-border-hi": P["border_hi"],
            "--parrot-text": P["text"],
            "--parrot-text-muted": P["text_muted"],
            "--parrot-cyan": P["cyan"],
            "--parrot-cyan-hi": P["cyan_hi"],
            "--parrot-cyan-dim": P["cyan_dim"],
            "--parrot-teal": P["teal"],
            "--parrot-violet": P["violet"],
            "--parrot-ok": P["ok"],
            "--parrot-warn": P["warn"],
            "--parrot-alert": P["alert"],
        },
    }


if __name__ == "__main__":  # pragma: no cover - diagnostica manuale
    print(banner())
    print(ansi("  identità: Parrot OS 7 «Echo»", "cyan_hi", bold=True))
    for name, value in P.items():
        print(f"  {name:<12}{value}")
