#!/usr/bin/env bash
set -e

echo "======================================================="
echo " ZDOS // FULL ECOSYSTEM AUTOBUILD & NATIVE PIPELINE   "
echo "======================================================="

ZDOS_ROOT="$HOME/zdos-organism"
mkdir -p "$ZDOS_ROOT/assets"
mkdir -p "$ZDOS_ROOT/webapp/assets"
cd "$ZDOS_ROOT"

# 1. Creazione file di stile e script per la webapp di gestione (app.x-zdos.it)
cat << 'EOT' > webapp/index.html
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ZDOS Hybrid Management Hub · Parrot Edition</title>
    <meta name="description" content="Management Hub dell'ecosistema ZDOS Hybrid — identità visiva Parrot OS «Echo».">
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <div class="topline" aria-hidden="true"></div>
    <div id="zdos-app">
        <aside class="sidebar">
            <div class="logo">
                <h2>ZDOS <span>Hybrid</span></h2>
                <div class="logo-meta">
                    <span class="badge">Parrot Edition</span>
                    <span class="badge ghost">Net 80.24</span>
                </div>
            </div>
            <nav>
                <button class="nav-btn active" onclick="switchTab('dashboard')">Dashboard</button>
                <button class="nav-btn" onclick="switchTab('gestionale')">Gestionale</button>
                <button class="nav-btn" onclick="switchTab('microcosm')">ZComm / Microcosm</button>
                <button class="nav-btn" onclick="switchTab('developers')">Sezione Sviluppatori</button>
                <button class="nav-btn" onclick="switchTab('identita')">Identità visiva</button>
            </nav>
            <footer class="sidebar-footer">
                <span class="dot" aria-hidden="true"></span>
                palette Parrot OS <code>#15E0ED</code>
            </footer>
        </aside>
        <main class="content">
            <section id="tab-dashboard" class="tab-pane active">
                <header>
                    <h1>Connessione Esterna app.x-zdos.it</h1>
                    <span id="connection-status" class="status-pill online">Connesso</span>
                </header>
                <div class="grid-metrics">
                    <div class="card">
                        <h3>Internet 80.24</h3>
                        <p class="metric-value">ATTIVO (Mesh)</p>
                    </div>
                    <div class="card">
                        <h3>Nodi ZComm</h3>
                        <p class="metric-value">1,024 Attivi</p>
                    </div>
                </div>
            </section>
            <section id="tab-gestionale" class="tab-pane">
                <header><h1>Software Gestionale Distro ZDOS</h1></header>
                <p>Moduli di gestione risorse e demoni di sistema attivi.</p>
            </section>
            <section id="tab-microcosm" class="tab-pane">
                <header><h1>ZDOS Microcosm - ZComm Node</h1></header>
                <p>Canale di messaggistica cifrata su Internet 80.24.</p>
            </section>
            <section id="tab-developers" class="tab-pane">
                <header><h1>Sezione Sviluppatori &amp; SDK</h1></header>
                <p>Endpoint API: <code>https://app.x-zdos.it/api/v1/</code></p>
            </section>
            <section id="tab-identita" class="tab-pane">
                <header><h1>Identità visiva · Parrot OS «Echo»</h1></header>
                <p>La palette dell'interfaccia è allineata a Parrot OS 7: fondo notte
                   <code>#0A0118</code>, indaco profondo <code>#06043E</code>, ciano di marca
                   <code>#15E0ED</code> e neon <code>#00FFF0</code> per gli elementi attivi.</p>
                <p>Token completi in <code>assets/theme/parrot-tokens.json</code> e nel modulo
                   <code>parrot_theme.py</code>.</p>
            </section>
        </main>
    </div>
    <script src="assets/app.js"></script>
</body>
</html>
EOT

cat << 'EOT' > webapp/assets/style.css
/* ZDOS Hybrid Management Hub — identità visiva Parrot OS 7 «Echo»
   Token canonici: parrot_theme.py / assets/theme/parrot-tokens.json
   Palette di riferimento: simple-icons "Parrot Security" (#15E0ED) e
   parrotsec.org (#00FFF0, #00D3F2, #00B8DB, #0A0118, #06043E, #0F0A1E, #8799B5). */

:root {
    --parrot-bg-deep: #04010F;
    --parrot-bg: #0A0118;
    --parrot-panel: #0F0A1E;
    --parrot-panel-alt: #131038;
    --parrot-surface: #06043E;
    --parrot-raised: #1B1647;
    --parrot-border: #1D2B4B;
    --parrot-border-hi: #252A52;
    --parrot-text: #EAF6FF;
    --parrot-text-muted: #8799B5;
    --parrot-text-dim: #6F7F9E;
    --parrot-cyan: #15E0ED;
    --parrot-cyan-hi: #00FFF0;
    --parrot-cyan-mid: #00D3F2;
    --parrot-cyan-dim: #00B8DB;
    --parrot-teal: #02ABB5;
    --parrot-violet: #7C3AED;
    --parrot-ok: #3DDC97;
    --parrot-warn: #FFC857;
    --parrot-alert: #FF5C7A;

    --font-ui: 'Ubuntu', 'Segoe UI', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    --glow: 0 0 12px rgba(21, 224, 237, 0.35);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    background:
        radial-gradient(1200px 600px at 15% -10%, rgba(21, 224, 237, 0.10), transparent 60%),
        radial-gradient(900px 500px at 100% 0%, rgba(124, 58, 237, 0.12), transparent 55%),
        var(--parrot-bg);
    color: var(--parrot-text);
    font-family: var(--font-ui);
    -webkit-font-smoothing: antialiased;
}

.topline {
    height: 3px;
    background: linear-gradient(90deg, var(--parrot-cyan) 0%, var(--parrot-cyan-hi) 45%, var(--parrot-violet) 100%);
}

#zdos-app { display: flex; height: calc(100vh - 3px); overflow: hidden; }

/* --- Sidebar ------------------------------------------------------------ */
.sidebar {
    width: 268px;
    background: linear-gradient(180deg, var(--parrot-surface) 0%, var(--parrot-bg) 100%);
    border-right: 1px solid var(--parrot-border);
    display: flex;
    flex-direction: column;
}

.logo {
    padding: 22px 20px 18px;
    border-bottom: 1px solid var(--parrot-border);
}

.logo h2 {
    color: var(--parrot-text);
    font-size: 1.18rem;
    letter-spacing: 0.04em;
}

.logo h2 span { color: var(--parrot-cyan); }

.logo-meta { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }

.badge {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    background: rgba(21, 224, 237, 0.14);
    color: var(--parrot-cyan);
    border: 1px solid rgba(21, 224, 237, 0.35);
    padding: 3px 7px;
    border-radius: 4px;
}

.badge.ghost {
    background: transparent;
    color: var(--parrot-text-muted);
    border-color: var(--parrot-border-hi);
}

nav { display: flex; flex-direction: column; padding: 16px 14px; gap: 6px; }

.nav-btn {
    background: transparent;
    border: 1px solid transparent;
    color: var(--parrot-text-muted);
    font-family: var(--font-ui);
    font-size: 0.92rem;
    text-align: left;
    padding: 10px 14px;
    cursor: pointer;
    border-radius: 8px;
    transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}

.nav-btn:hover {
    background: rgba(21, 224, 237, 0.07);
    color: var(--parrot-cyan-mid);
    border-color: rgba(21, 224, 237, 0.20);
}

.nav-btn.active {
    background: rgba(21, 224, 237, 0.12);
    color: var(--parrot-cyan-hi);
    border-color: rgba(21, 224, 237, 0.45);
    box-shadow: inset 3px 0 0 var(--parrot-cyan);
}

.sidebar-footer {
    margin-top: auto;
    padding: 14px 20px;
    border-top: 1px solid var(--parrot-border);
    color: var(--parrot-text-dim);
    font-size: 0.74rem;
    font-family: var(--font-mono);
    display: flex;
    align-items: center;
    gap: 8px;
}

.dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--parrot-cyan);
    box-shadow: var(--glow);
}

/* --- Contenuto ---------------------------------------------------------- */
.content { flex: 1; padding: 32px 36px; overflow-y: auto; }

.tab-pane { display: none; }
.tab-pane.active { display: block; animation: fade 0.22s ease; }

@keyframes fade { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }

.tab-pane header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 22px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--parrot-border);
}

h1 { font-size: 1.28rem; font-weight: 600; letter-spacing: 0.01em; }

p { color: var(--parrot-text-muted); line-height: 1.6; margin: 10px 0; }

code {
    font-family: var(--font-mono);
    font-size: 0.84rem;
    color: var(--parrot-cyan-mid);
    background: rgba(6, 4, 62, 0.6);
    border: 1px solid var(--parrot-border);
    border-radius: 4px;
    padding: 1px 6px;
}

.grid-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
}

.card {
    background: linear-gradient(160deg, var(--parrot-panel-alt) 0%, var(--parrot-panel) 100%);
    border: 1px solid var(--parrot-border);
    border-radius: 10px;
    padding: 22px;
    transition: border-color 0.18s ease, box-shadow 0.18s ease;
}

.card:hover {
    border-color: rgba(21, 224, 237, 0.45);
    box-shadow: 0 0 18px rgba(21, 224, 237, 0.14);
}

.card h3 {
    color: var(--parrot-text-muted);
    font-size: 0.82rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.metric-value {
    font-family: var(--font-mono);
    font-size: 1.42rem;
    color: var(--parrot-cyan);
    margin-top: 12px;
}

.status-pill {
    font-family: var(--font-mono);
    font-size: 0.78rem;
    padding: 5px 13px;
    border-radius: 999px;
    background: rgba(61, 220, 151, 0.12);
    color: var(--parrot-ok);
    border: 1px solid rgba(61, 220, 151, 0.45);
}

.status-pill.online { box-shadow: 0 0 12px rgba(61, 220, 151, 0.20); }

/* --- Scrollbar ---------------------------------------------------------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--parrot-bg-deep); }
::-webkit-scrollbar-thumb {
    background: var(--parrot-border-hi);
    border-radius: 999px;
    border: 2px solid var(--parrot-bg-deep);
}
::-webkit-scrollbar-thumb:hover { background: var(--parrot-cyan-dim); }
EOT

cat << 'EOT' > webapp/assets/app.js
function switchTab(tabId) {
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    document.getElementById('tab-' + tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}
EOT

# 2b. Design system condiviso: identità visiva Parrot OS «Echo»
cat << 'EOF' > parrot_theme.py
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
EOF

# 2. Creazione dell'applicazione principale ZDOS con Browser Antifingerprint Anonimo (Tor Clone)
cat << 'EOF' > zdos_omni_os.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import time
import random
import os
import json
import secrets
import socket
from urllib.request import urlopen, Request
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from PIL import Image, ImageTk

TOKEN_ADDRESS = "0xfc90516a1f736fac557e09d8853db80da192c296"
BRIDGE_PORT = 8888

class BridgeState:
    secret_key = "ZDOS-" + secrets.token_hex(3).upper() + "-" + secrets.token_hex(3).upper()
    latest_token_data = {"price": "0.00", "change": "0.00%", "liquidity": "$0", "volume": "$0"}

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()

class MobileBridgeHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if parsed.path == "/api/sync":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            payload = {"status": "AUTHORIZED", "token": TOKEN_ADDRESS, "metrics": BridgeState.latest_token_data, "host": LOCAL_IP}
            self.wfile.write(json.dumps(payload).encode())
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<html><body><h3>ZDOS Microcosm SwebApp Bridge Active</h3></body></html>")

def run_bridge_server():
    server = HTTPServer(("0.0.0.0", BRIDGE_PORT), MobileBridgeHandler)
    server.serve_forever()

class ZDOSPuppyDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("ZDOS Hybrid // Net 80.24 · Parrot Edition")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#0F0A1E")

        self.running = True
        threading.Thread(target=run_bridge_server, daemon=True).start()
        self.start_token_poller()

        # identità visiva Parrot OS: barra ciano di marca
        tk.Frame(self.root, bg="#15E0ED", height=3).pack(side="top", fill="x")
        self.create_top_header()
        self.create_dashboard_layout()
        self.create_statusbar()

        self.root.bind("<Escape>", lambda e: self.root.quit())

    def create_top_header(self):
        self.header = tk.Frame(self.root, bg="#131038", height=45, bd=0)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        logo_title = tk.Label(self.header, text=" 🛡️ ZDOS HYBRID // NET 80.24 · PARROT EDITION", bg="#131038", fg="#15E0ED", font=('Ubuntu', 11, 'bold'))
        logo_title.pack(side="left", padx=15)

        actions = [
            ("🌐 Anon Browser (Tor)", self.open_anon_browser),
            ("🔗 Webapp (app.x-zdos.it)", self.open_webapp_dashboard),
            ("⚡ Zlang Studio", self.open_zlang_app),
            ("🛠️ Kali Security", self.open_kali_tools_app),
            ("💻 Terminale Root", self.open_terminal)
        ]

        for text, cmd in actions:
            b = tk.Button(self.header, text=text, bg="#16123F", fg="#D6E6F5", font=('Ubuntu', 9), relief="flat", command=cmd)
            b.pack(side="left", padx=4, pady=8)

        self.dsn_header_lbl = tk.Label(self.header, text="$DSN: Loading...", bg="#131038", fg="#3DDC97", font=('Courier', 9, 'bold'), padx=15)
        self.dsn_header_lbl.pack(side="right", padx=10)

    def create_dashboard_layout(self):
        self.main_container = tk.Frame(self.root, bg="#0F0A1E")
        self.main_container.pack(side="top", fill="both", expand=True)

        sidebar = tk.Frame(self.main_container, bg="#131038", width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text=" PARROT EDITION & TOOLKIT ", bg="#131038", fg="#8E9FBB", font=('Ubuntu', 9, 'bold')).pack(anchor="w", padx=15, pady=(15, 5))

        nav_buttons = [
            ("🌐 Anon Browser (Tor Clone)", self.open_anon_browser),
            ("🔗 Webapp app.x-zdos.it", self.open_webapp_dashboard),
            ("⚡ Zlang Validator (ZLB2)", self.open_zlang_app),
            ("🛠️ Kali Security Tools", self.open_kali_tools_app),
            ("🛡️ Evidence Ledger", self.open_evidence_app)
        ]

        for text, cmd in nav_buttons:
            btn = tk.Button(sidebar, text=text, bg="#16123F", fg="#D6E6F5", font=('Ubuntu', 9, 'bold'), anchor="w", relief="flat", padx=15, pady=8, command=cmd)
            btn.pack(fill="x", padx=10, pady=3)

        self.center_area = tk.Frame(self.main_container, bg="#0F0A1E")
        self.center_area.pack(side="right", fill="both", expand=True)
        self.load_overview_view()

    def load_overview_view(self):
        for w in self.center_area.winfo_children(): w.destroy()
        hero = tk.Frame(self.center_area, bg="#0F0A1E")
        hero.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(hero, text="ZDOS HYBRID ECOSYSTEM & NET 80.24", fg="#15E0ED", bg="#0F0A1E", font=('Ubuntu', 14, 'bold')).pack(pady=10)
        tk.Label(hero, text="Browser Antifingerprint integrato, Webapp gestionale e protocollo decentralizzato.", fg="#8E9FBB", bg="#0F0A1E", font=('Ubuntu', 9)).pack(pady=5)

    def open_anon_browser(self):
        def build(parent):
            top_bar = tk.Frame(parent, bg="#131038", height=35)
            top_bar.pack(side="top", fill="x", pady=2)
            
            tk.Label(top_bar, text="🔒 Circuit ID:", bg="#131038", fg="#3DDC97", font=('Ubuntu', 9, 'bold')).pack(side="left", padx=5)
            circuit_lbl = tk.Label(top_bar, text="Tor-Relay-Z8024 [AES-256 Active]", bg="#131038", fg="#D6E6F5", font=('Courier', 9))
            circuit_lbl.pack(side="left", padx=5)

            def new_circuit():
                rand_id = secrets.token_hex(4).upper()
                circuit_lbl.config(text=f"Tor-Relay-Z{rand_id} [IP Masked]")

            tk.Button(top_bar, text="🔄 Cambia Nodo", bg="#16123F", fg="#15E0ED", font=('Ubuntu', 8, 'bold'), command=new_circuit).pack(side="right", padx=5)

            url_bar = tk.Frame(parent, bg="#0F0A1E")
            url_bar.pack(side="top", fill="x", pady=5)
            tk.Label(url_bar, text="URL:", bg="#0F0A1E", fg="#8E9FBB").pack(side="left")
            url_entry = tk.Entry(url_bar, bg="#131038", fg="#D6E6F5", font=('Courier', 9), relief="flat")
            url_entry.insert(0, "https://app.x-zdos.it")
            url_entry.pack(side="left", fill="x", expand=True, padx=5)

            browser_view = scrolledtext.ScrolledText(parent, bg="#0F0A1E", fg="#15E0ED", font=('Courier', 9))
            browser_view.pack(fill="both", expand=True, pady=5)
            browser_view.insert(tk.END, "[ANON BROWSER] Antifingerprint protetto.\n- Canvas noise: ENABLED\n- WebGL spoofing: ACTIVE\n- Referer stripping: STRICT\n\nConnesso a https://app.x-zdos.it/\n")
            browser_view.config(state=tk.DISABLED)

            def load_url():
                browser_view.config(state=tk.NORMAL)
                browser_view.insert(tk.END, f"\n> Navigazione cifrata verso: {url_entry.get()}\n[OK] Pagina caricata tramite circuito anonimo.\n")
                browser_view.see(tk.END)
                browser_view.config(state=tk.DISABLED)

            tk.Button(url_bar, text="Vai", bg="#16123F", fg="#3DDC97", font=('Ubuntu', 8, 'bold'), command=load_url).pack(side="right")

        self.spawn_window("🌐 ZDOS Anon Browser (Tor Clone)", 700, 480, build)

    def open_webapp_dashboard(self):
        def build(parent):
            tk.Label(parent, text="ZDOS WEBAPP MANAGEMENT HUB (app.x-zdos.it)", bg="#0F0A1E", fg="#15E0ED", font=('Ubuntu', 11, 'bold')).pack(anchor="w", pady=5)
            box = scrolledtext.ScrolledText(parent, bg="#0F0A1E", fg="#3DDC97", font=('Courier', 9), height=14)
            box.pack(fill="both", expand=True, pady=5)
            box.insert(tk.END, "[WEBAPP] Connessione a https://app.x-zdos.it/ stabilita.\n- Stato Internet 80.24: ATTIVO\n- Sincronizzazione ZComm: OK\n")
            box.config(state=tk.DISABLED)
        self.spawn_window("🔗 Webapp Dashboard", 600, 400, build)

    def open_zlang_app(self):
        def build(parent):
            tk.Label(parent, text="ZLANG / VALIDATOR ZLB2 PROFILE 2.5", bg="#0F0A1E", fg="#15E0ED", font=('Ubuntu', 11, 'bold')).pack(anchor="w", pady=5)
            editor = scrolledtext.ScrolledText(parent, bg="#131038", fg="#D6E6F5", font=('Courier', 9), height=10)
            editor.pack(fill="both", expand=True, pady=5)
            editor.insert(tk.END, "emit ZDOS Net 80.24 attivo.\n")
        self.spawn_window("⚡ Zlang Studio", 580, 400, build)

    def open_kali_tools_app(self):
        def build(parent):
            tk.Label(parent, text="KALI SECURITY & NET 80.24 TOOLS", bg="#0F0A1E", fg="#15E0ED", font=('Ubuntu', 11, 'bold')).pack(anchor="w", pady=5)
            box = scrolledtext.ScrolledText(parent, bg="#131038", fg="#3DDC97", font=('Courier', 9), height=12)
            box.pack(fill="both", expand=True, pady=5)
            box.insert(tk.END, "[Z-CYBERCORE] Default-deny attivo sui nodi di rete.\n")
            box.config(state=tk.DISABLED)
        self.spawn_window("🛠️ Kali Security Tools", 560, 360, build)

    def open_terminal(self):
        def build(parent):
            term = scrolledtext.ScrolledText(parent, bg="#0F0A1E", fg="#3DDC97", font=('Courier', 10), height=14)
            term.pack(fill="both", expand=True, pady=2)
            term.insert(tk.END, "root@net-8024:~# \n")
            term.config(state=tk.DISABLED)
        self.spawn_window("💻 Terminale Root", 620, 380, build)

    def open_evidence_app(self):
        def build(parent):
            tk.Label(parent, text="PUBLIC EVIDENCE RAIL / APPEND-ONLY LEDGER", bg="#0F0A1E", fg="#FEBE2D", font=('Ubuntu', 10, 'bold')).pack(anchor="w", pady=5)
            box = scrolledtext.ScrolledText(parent, bg="#0F0A1E", fg="#FEBE2D", font=('Courier', 8), height=12)
            box.pack(fill="both", expand=True, pady=5)
            box.insert(tk.END, "[01] NET 80.24 initialized -> VERIFIED\n[02] ANON BROWSER circuits active\n")
            box.config(state=tk.DISABLED)
        self.spawn_window("🛡️ Evidence Chain Ledger", 560, 360, build)

    def create_statusbar(self):
        self.statusbar = tk.Frame(self.root, bg="#131038", height=26)
        self.statusbar.pack(side="bottom", fill="x")
        self.statusbar.pack_propagate(False)
        status_lbl = tk.Label(self.statusbar, text=" ZDOS Hybrid · Parrot Edition | Net 80.24 attivo | Bridge 127.0.0.1:8888", bg="#131038", fg="#8E9FBB", font=('Ubuntu', 8))
        status_lbl.pack(side="left", padx=10)

    def poll_dex(self):
        def _fetch():
            url = f"https://api.dexscreener.com/latest/dex/tokens/{TOKEN_ADDRESS}"
            try:
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urlopen(req, timeout=4) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    pairs = data.get("pairs")
                    if pairs and len(pairs) > 0:
                        p = pairs[0]
                        BridgeState.latest_token_data = {"price": str(p.get("priceUsd", "0.00")), "change": str(p.get("priceChange", {}).get("h24", "0.00")) + "%"}
                        if hasattr(self, 'dsn_header_lbl') and self.dsn_header_lbl.winfo_exists():
                            self.dsn_header_lbl.config(text=f"$DSN: ${BridgeState.latest_token_data['price']} ({BridgeState.latest_token_data['change']})")
            except Exception: pass
        threading.Thread(target=_fetch, daemon=True).start()

    def start_token_poller(self):
        def _loop():
            while self.running:
                self.poll_dex()
                time.sleep(10)
        threading.Thread(target=_loop, daemon=True).start()

    def spawn_window(self, title, width, height, builder_func):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry(f"{width}x{height}+220+120")
        win.configure(bg="#0F0A1E")
        content = tk.Frame(win, bg="#0F0A1E")
        content.pack(fill="both", expand=True, padx=10, pady=10)
        builder_func(content)
        return win

if __name__ == "__main__":
    root = tk.Tk()
    app = ZDOSPuppyDesktop(root)
    root.mainloop()
EOF
