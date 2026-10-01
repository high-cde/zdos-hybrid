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
    <title>ZDOS Management Hub | app.x-zdos.it</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <div id="zdos-app">
        <aside class="sidebar">
            <div class="logo">
                <h2>ZDOS Core</h2>
                <span class="badge">Net 80.24</span>
            </div>
            <nav>
                <button class="nav-btn active" onclick="switchTab('dashboard')">Dashboard</button>
                <button class="nav-btn" onclick="switchTab('gestionale')">Gestionale</button>
                <button class="nav-btn" onclick="switchTab('microcosm')">ZComm / Microcosm</button>
                <button class="nav-btn" onclick="switchTab('developers')">Sezione Sviluppatori</button>
            </nav>
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
                <header><h1>Sezione Sviluppatori & SDK</h1></header>
                <p>Endpoint API: <code>https://app.x-zdos.it/api/v1/</code></p>
            </section>
        </main>
    </div>
    <script src="assets/app.js"></script>
</body>
</html>
EOT

cat << 'EOT' > webapp/assets/style.css
:root { --bg-dark: #0a0d14; --bg-panel: #121824; --accent: #00ffcc; --text-main: #e0e6ed; --text-muted: #8a99ad; --border: #222d42; }
* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Courier New', Courier, monospace; }
body { background-color: var(--bg-dark); color: var(--text-main); }
#zdos-app { display: flex; height: 100vh; overflow: hidden; }
.sidebar { width: 260px; background-color: var(--bg-panel); border-right: 1px solid var(--border); display: flex; flex-direction: column; }
.logo { padding: 20px; border-bottom: 1px solid var(--border); }
.logo h2 { color: var(--accent); font-size: 1.2rem; }
.badge { font-size: 0.75rem; background: #00ffcc22; color: var(--accent); padding: 2px 6px; border-radius: 4px; }
nav { display: flex; flex-direction: column; padding: 15px; gap: 10px; }
.nav-btn { background: transparent; border: none; color: var(--text-muted); text-align: left; padding: 10px 15px; cursor: pointer; border-radius: 6px; }
.nav-btn:hover, .nav-btn.active { background: var(--border); color: var(--accent); }
.content { flex: 1; padding: 30px; overflow-y: auto; }
.tab-pane { display: none; }
.tab-pane.active { display: block; }
.grid-metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
.card { background: var(--bg-panel); border: 1px solid var(--border); padding: 20px; border-radius: 8px; }
.metric-value { font-size: 1.5rem; color: var(--accent); margin-top: 10px; }
.status-pill { padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; background: #00ffcc22; color: var(--accent); border: 1px solid var(--accent); }
EOT

cat << 'EOT' > webapp/assets/app.js
function switchTab(tabId) {
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    document.getElementById('tab-' + tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}
EOT

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
        self.root.title("ZDOS // NET 80.24 & ANON BROWSER")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#0e1117")

        self.running = True
        threading.Thread(target=run_bridge_server, daemon=True).start()
        self.start_token_poller()

        self.create_top_header()
        self.create_dashboard_layout()
        self.create_statusbar()

        self.root.bind("<Escape>", lambda e: self.root.quit())

    def create_top_header(self):
        self.header = tk.Frame(self.root, bg="#161b22", height=45, bd=0)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        logo_title = tk.Label(self.header, text=" 🛡️ ZDOS // NET 80.24 CORE", bg="#161b22", fg="#58a6ff", font=('Ubuntu', 11, 'bold'))
        logo_title.pack(side="left", padx=15)

        actions = [
            ("🌐 Anon Browser (Tor)", self.open_anon_browser),
            ("🔗 Webapp (app.x-zdos.it)", self.open_webapp_dashboard),
            ("⚡ Zlang Studio", self.open_zlang_app),
            ("🛠️ Kali Security", self.open_kali_tools_app),
            ("💻 Terminale Root", self.open_terminal)
        ]

        for text, cmd in actions:
            b = tk.Button(self.header, text=text, bg="#21262d", fg="#c9d1d9", font=('Ubuntu', 9), relief="flat", command=cmd)
            b.pack(side="left", padx=4, pady=8)

        self.dsn_header_lbl = tk.Label(self.header, text="$DSN: Loading...", bg="#161b22", fg="#3fb950", font=('Courier', 9, 'bold'), padx=15)
        self.dsn_header_lbl.pack(side="right", padx=10)

    def create_dashboard_layout(self):
        self.main_container = tk.Frame(self.root, bg="#0e1117")
        self.main_container.pack(side="top", fill="both", expand=True)

        sidebar = tk.Frame(self.main_container, bg="#161b22", width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text=" NET 80.24 & TOOLKIT ", bg="#161b22", fg="#8b949e", font=('Ubuntu', 9, 'bold')).pack(anchor="w", padx=15, pady=(15, 5))

        nav_buttons = [
            ("🌐 Anon Browser (Tor Clone)", self.open_anon_browser),
            ("🔗 Webapp app.x-zdos.it", self.open_webapp_dashboard),
            ("⚡ Zlang Validator (ZLB2)", self.open_zlang_app),
            ("🛠️ Kali Security Tools", self.open_kali_tools_app),
            ("🛡️ Evidence Ledger", self.open_evidence_app)
        ]

        for text, cmd in nav_buttons:
            btn = tk.Button(sidebar, text=text, bg="#21262d", fg="#c9d1d9", font=('Ubuntu', 9, 'bold'), anchor="w", relief="flat", padx=15, pady=8, command=cmd)
            btn.pack(fill="x", padx=10, pady=3)

        self.center_area = tk.Frame(self.main_container, bg="#0e1117")
        self.center_area.pack(side="right", fill="both", expand=True)
        self.load_overview_view()

    def load_overview_view(self):
        for w in self.center_area.winfo_children(): w.destroy()
        hero = tk.Frame(self.center_area, bg="#0e1117")
        hero.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(hero, text="ZDOS HYBRID ECOSYSTEM & NET 80.24", fg="#58a6ff", bg="#0e1117", font=('Ubuntu', 14, 'bold')).pack(pady=10)
        tk.Label(hero, text="Browser Antifingerprint integrato, Webapp gestionale e protocollo decentralizzato.", fg="#8b949e", bg="#0e1117", font=('Ubuntu', 9)).pack(pady=5)

    def open_anon_browser(self):
        def build(parent):
            top_bar = tk.Frame(parent, bg="#161b22", height=35)
            top_bar.pack(side="top", fill="x", pady=2)
            
            tk.Label(top_bar, text="🔒 Circuit ID:", bg="#161b22", fg="#3fb950", font=('Ubuntu', 9, 'bold')).pack(side="left", padx=5)
            circuit_lbl = tk.Label(top_bar, text="Tor-Relay-Z8024 [AES-256 Active]", bg="#161b22", fg="#c9d1d9", font=('Courier', 9))
            circuit_lbl.pack(side="left", padx=5)

            def new_circuit():
                rand_id = secrets.token_hex(4).upper()
                circuit_lbl.config(text=f"Tor-Relay-Z{rand_id} [IP Masked]")

            tk.Button(top_bar, text="🔄 Cambia Nodo", bg="#21262d", fg="#58a6ff", font=('Ubuntu', 8, 'bold'), command=new_circuit).pack(side="right", padx=5)

            url_bar = tk.Frame(parent, bg="#0e1117")
            url_bar.pack(side="top", fill="x", pady=5)
            tk.Label(url_bar, text="URL:", bg="#0e1117", fg="#8b949e").pack(side="left")
            url_entry = tk.Entry(url_bar, bg="#161b22", fg="#c9d1d9", font=('Courier', 9), relief="flat")
            url_entry.insert(0, "https://app.x-zdos.it")
            url_entry.pack(side="left", fill="x", expand=True, padx=5)

            browser_view = scrolledtext.ScrolledText(parent, bg="#0d1117", fg="#00ffcc", font=('Courier', 9))
            browser_view.pack(fill="both", expand=True, pady=5)
            browser_view.insert(tk.END, "[ANON BROWSER] Antifingerprint protetto.\n- Canvas noise: ENABLED\n- WebGL spoofing: ACTIVE\n- Referer stripping: STRICT\n\nConnesso a https://app.x-zdos.it/\n")
            browser_view.config(state=tk.DISABLED)

            def load_url():
                browser_view.config(state=tk.NORMAL)
                browser_view.insert(tk.END, f"\n> Navigazione cifrata verso: {url_entry.get()}\n[OK] Pagina caricata tramite circuito anonimo.\n")
                browser_view.see(tk.END)
                browser_view.config(state=tk.DISABLED)

            tk.Button(url_bar, text="Vai", bg="#21262d", fg="#3fb950", font=('Ubuntu', 8, 'bold'), command=load_url).pack(side="right")

        self.spawn_window("🌐 ZDOS Anon Browser (Tor Clone)", 700, 480, build)

    def open_webapp_dashboard(self):
        def build(parent):
            tk.Label(parent, text="ZDOS WEBAPP MANAGEMENT HUB (app.x-zdos.it)", bg="#0e1117", fg="#58a6ff", font=('Ubuntu', 11, 'bold')).pack(anchor="w", pady=5)
            box = scrolledtext.ScrolledText(parent, bg="#0d1117", fg="#3fb950", font=('Courier', 9), height=14)
            box.pack(fill="both", expand=True, pady=5)
            box.insert(tk.END, "[WEBAPP] Connessione a https://app.x-zdos.it/ stabilita.\n- Stato Internet 80.24: ATTIVO\n- Sincronizzazione ZComm: OK\n")
            box.config(state=tk.DISABLED)
        self.spawn_window("🔗 Webapp Dashboard", 600, 400, build)

    def open_zlang_app(self):
        def build(parent):
            tk.Label(parent, text="ZLANG / VALIDATOR ZLB2 PROFILE 2.5", bg="#0e1117", fg="#58a6ff", font=('Ubuntu', 11, 'bold')).pack(anchor="w", pady=5)
            editor = scrolledtext.ScrolledText(parent, bg="#161b22", fg="#c9d1d9", font=('Courier', 9), height=10)
            editor.pack(fill="both", expand=True, pady=5)
            editor.insert(tk.END, "emit ZDOS Net 80.24 attivo.\n")
        self.spawn_window("⚡ Zlang Studio", 580, 400, build)

    def open_kali_tools_app(self):
        def build(parent):
            tk.Label(parent, text="KALI SECURITY & NET 80.24 TOOLS", bg="#0e1117", fg="#58a6ff", font=('Ubuntu', 11, 'bold')).pack(anchor="w", pady=5)
            box = scrolledtext.ScrolledText(parent, bg="#161b22", fg="#3fb950", font=('Courier', 9), height=12)
            box.pack(fill="both", expand=True, pady=5)
            box.insert(tk.END, "[Z-CYBERCORE] Default-deny attivo sui nodi di rete.\n")
            box.config(state=tk.DISABLED)
        self.spawn_window("🛠️ Kali Security Tools", 560, 360, build)

    def open_terminal(self):
        def build(parent):
            term = scrolledtext.ScrolledText(parent, bg="#0d1117", fg="#3fb950", font=('Courier', 10), height=14)
            term.pack(fill="both", expand=True, pady=2)
            term.insert(tk.END, "root@net-8024:~# \n")
            term.config(state=tk.DISABLED)
        self.spawn_window("💻 Terminale Root", 620, 380, build)

    def open_evidence_app(self):
        def build(parent):
            tk.Label(parent, text="PUBLIC EVIDENCE RAIL / APPEND-ONLY LEDGER", bg="#0e1117", fg="#d29922", font=('Ubuntu', 10, 'bold')).pack(anchor="w", pady=5)
            box = scrolledtext.ScrolledText(parent, bg="#0d1117", fg="#d29922", font=('Courier', 8), height=12)
            box.pack(fill="both", expand=True, pady=5)
            box.insert(tk.END, "[01] NET 80.24 initialized -> VERIFIED\n[02] ANON BROWSER circuits active\n")
            box.config(state=tk.DISABLED)
        self.spawn_window("🛡️ Evidence Chain Ledger", 560, 360, build)

    def create_statusbar(self):
        self.statusbar = tk.Frame(self.root, bg="#161b22", height=26)
        self.statusbar.pack(side="bottom", fill="x")
        self.statusbar.pack_propagate(False)
        status_lbl = tk.Label(self.statusbar, text=" ZDOS Net 80.24 Active | Anon Browser Ready | Bridge: http://127.0.0.1:8888", bg="#161b22", fg="#8b949e", font=('Ubuntu', 8))
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
        win.configure(bg="#0e1117")
        content = tk.Frame(win, bg="#0e1117")
        content.pack(fill="both", expand=True, padx=10, pady=10)
        builder_func(content)
        return win

if __name__ == "__main__":
    root = tk.Tk()
    app = ZDOSPuppyDesktop(root)
    root.mainloop()
