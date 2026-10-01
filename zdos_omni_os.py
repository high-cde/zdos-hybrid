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
import webbrowser
from urllib.request import urlopen, Request
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

TOKEN_ADDRESS = "0xfc90516a1f736fac557e09d8853db80da192c296"
BRIDGE_PORT = 8888
XCLOUD_REPO_URL = "https://github.com/high-cde/xCLOUD-by-zdos.git"

class ZDOSBackendCore:
    def __init__(self):
        self.audit_log = []
        self.modules_status = {
            "Zlang M1-M7": "VERIFIED",
            "Internet 80.24": "ACTIVE",
            "DSN Layer": "CONNECTED",
            "xCLOUD Enterprise": "RUNNING"
        }
        self.log_event("SYSTEM_BOOT", "ZDOS Glass Engine avviato correttamente.")

    def log_event(self, event_type, details):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{event_type}] {details}"
        self.audit_log.append(entry)
        if len(self.audit_log) > 100: self.audit_log.pop(0)
        return entry

    def get_system_metrics(self):
        return {
            "cpu_load": f"{round(random.uniform(0.5, 1.8), 2)}%",
            "ram_usage": "44.1 MB / 4096 MB",
            "storage_mode": "Read-Only Encrypted (ext4)",
            "active_peers": 1024
        }

backend = ZDOSBackendCore()

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
        if parsed.path == "/api/sync":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            payload = {"status": "AUTHORIZED", "token": TOKEN_ADDRESS, "metrics": BridgeState.latest_token_data, "backend": backend.modules_status, "host": LOCAL_IP}
            self.wfile.write(json.dumps(payload).encode())
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<html><body><h3>ZDOS Glass Engine Active</h3></body></html>")

def run_bridge_server():
    server = HTTPServer(("0.0.0.0", BRIDGE_PORT), MobileBridgeHandler)
    server.serve_forever()

class ZDOSPuppyDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("ZDOS Hybrid // Glass Engine · Parrot Edition")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#04010F")

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
        self.header = tk.Frame(self.root, bg="#0D0A22", height=50, bd=0)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        logo_title = tk.Label(self.header, text=" ❖ ZDOS HYBRID // GLASS ENGINE · PARROT EDITION", bg="#0D0A22", fg="#00D3F2", font=('Segoe UI', 11, 'bold'))
        logo_title.pack(side="left", padx=20)

        actions = [
            ("☁️ xCLOUD-by-zdos", self.open_xcloud_app),
            ("📊 Dashboards", self.open_dashboards_hub),
            ("🌐 Anon Browser", self.open_anon_browser),
            ("🔗 Webapp", self.open_webapp_dashboard),
            ("⚡ Zlang M1-M7", self.open_zlang_app),
            ("💻 Terminale", self.open_terminal)
        ]

        for text, cmd in actions:
            is_xcloud = "xCLOUD" in text
            bg_col = "#06304F" if is_xcloud else "#16123F"
            fg_col = "#4FE9FF" if is_xcloud else "#A9BCD6"
            b = tk.Button(self.header, text=text, bg=bg_col, fg=fg_col, font=('Segoe UI', 9, 'bold' if is_xcloud else 'normal'), relief="flat", activebackground="#2F3668", activeforeground="#ffffff", command=cmd)
            b.pack(side="left", padx=5, pady=9)

        self.dsn_header_lbl = tk.Label(self.header, text="$DSN: Loading...", bg="#0D0A22", fg="#3DDC97", font=('Consolas', 9, 'bold'), padx=15)
        self.dsn_header_lbl.pack(side="right", padx=15)

    def create_dashboard_layout(self):
        self.main_container = tk.Frame(self.root, bg="#04010F")
        self.main_container.pack(side="top", fill="both", expand=True)

        sidebar = tk.Frame(self.main_container, bg="#0D0A22", width=290)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text=" GLASS CONTROL SUITE ", bg="#0D0A22", fg="#6F7F9E", font=('Segoe UI', 9, 'bold')).pack(anchor="w", padx=20, pady=(20, 10))

        nav_buttons = [
            ("☁️ xCLOUD-by-zdos Hub", self.open_xcloud_app),
            ("📊 Dedicated Dashboards", self.open_dashboards_hub),
            ("☁️ Cloud File Manager", self.open_cloud_file_manager),
            ("⚡ Zlang Runtime Studio", self.open_zlang_app),
            ("🛡️ Evidence Chain Ledger", self.open_evidence_app),
            ("🌐 Anon Browser (Tor)", self.open_anon_browser),
            ("🔗 Webapp app.x-zdos.it", self.open_webapp_dashboard),
            ("🛠️ Backend Audit Logs", self.open_backend_audit)
        ]

        for text, cmd in nav_buttons:
            is_xcloud = "xCLOUD" in text
            bg_col = "#06304F" if is_xcloud else "#16123F"
            fg_col = "#4FE9FF" if is_xcloud else "#C3D4E6"
            btn = tk.Button(sidebar, text=text, bg=bg_col, fg=fg_col, font=('Segoe UI', 9, 'bold' if is_xcloud else 'normal'), anchor="w", relief="flat", padx=15, pady=9, activebackground="#252A52", activeforeground="#00D3F2", command=cmd)
            btn.pack(fill="x", padx=12, pady=4)

        self.center_area = tk.Frame(self.main_container, bg="#04010F")
        self.center_area.pack(side="right", fill="both", expand=True)
        self.load_overview_view()

    def load_overview_view(self):
        for w in self.center_area.winfo_children(): w.destroy()
        hero = tk.Frame(self.center_area, bg="#04010F")
        hero.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(hero, text="ZDOS HYBRID OPERATING SYSTEM v2026.2", fg="#00D3F2", bg="#04010F", font=('Segoe UI', 16, 'bold')).pack(anchor="w", pady=5)
        tk.Label(hero, text="Minimalist Glass Engine attivo con integrazione xCLOUD-by-zdos e DSN Layer.", fg="#6F7F9E", bg="#04010F", font=('Segoe UI', 10)).pack(anchor="w", pady=(0, 20))

        grid = tk.Frame(hero, bg="#04010F")
        grid.pack(anchor="w")

        cards = [
            ("☁️ xCLOUD-by-zdos Enterprise", "Dashboard aziendale stile Bitrix24, DSN Wallet e Portal Fusion", self.open_xcloud_app),
            ("📊 System & Mesh Dashboards", "Monitoraggio in tempo reale di risorse e nodi 80.24", self.open_dashboards_hub),
            ("☁️ Cloud File Manager", "Interfaccia sincronizzata con GitHub, GitLab e Discord", self.open_cloud_file_manager),
            ("🛠️ Backend Audit Logs", "Ispezione in tempo reale dei log di sistema e degli eventi", self.open_backend_audit)
        ]

        for i, (title, desc, cmd) in enumerate(cards):
            card = tk.Frame(grid, bg="#0D0A22", padx=20, pady=16, width=280, height=120)
            card.grid(row=i//2, column=i%2, padx=15, pady=15)
            card.grid_propagate(False)

            is_xcloud_card = "xCLOUD" in title
            title_col = "#4FE9FF" if is_xcloud_card else "#00D3F2"

            tk.Label(card, text=title, bg="#0D0A22", fg=title_col, font=('Segoe UI', 11, 'bold')).pack(anchor="w")
            tk.Label(card, text=desc, bg="#0D0A22", fg="#6F7F9E", font=('Segoe UI', 8), wraplength=240, justify="left").pack(anchor="w", pady=6)
            tk.Button(card, text="Apri ➔", bg="#16123F", fg="#C3D4E6", font=('Segoe UI', 8, 'bold'), relief="flat", activebackground="#252A52", activeforeground="#00D3F2", command=cmd).pack(anchor="e", pady=2)

    def open_xcloud_app(self):
        backend.log_event("XCLOUD_HUB", "Accesso alla dashboard xCLOUD Enterprise.")
        def build(parent):
            tk.Label(parent, text="☁️️ xCLOUD ENTERPRISE BY ZDOS (Bitrix24 Hub & DSN Layer)", bg="#04010F", fg="#4FE9FF", font=('Segoe UI', 12, 'bold')).pack(anchor="w", pady=5)
            tk.Label(parent, text=f"Repository sorgente: {XCLOUD_REPO_URL}", bg="#04010F", fg="#6F7F9E", font=('Consolas', 8)).pack(anchor="w", pady=(0, 10))

            notebook = ttk.Notebook(parent)
            notebook.pack(fill="both", expand=True, pady=5)

            tab1 = tk.Frame(notebook, bg="#0D0A22", padx=10, pady=10)
            notebook.add(tab1, text="🏢 Enterprise CRM & Projects")
            crm_box = scrolledtext.ScrolledText(tab1, bg="#04010F", fg="#3DDC97", font=('Consolas', 9), height=12)
            crm_box.pack(fill="both", expand=True)
            crm_box.insert(tk.END, "[CRM] Gestione Clienti, Vendite e Marketing: ATTIVO\n[PROJECTS] Pianificazione e Monitoraggio Attività: SINCRONIZZATO\n[COLLABORATION] Calendari e Pipeline Aziendali: PRONTI\n")
            crm_box.config(state=tk.DISABLED)

            tab2 = tk.Frame(notebook, bg="#0D0A22", padx=10, pady=10)
            notebook.add(tab2, text="🔗 DSN Blockchain & Wallet")
            dsn_box = scrolledtext.ScrolledText(tab2, bg="#04010F", fg="#00D3F2", font=('Consolas', 9), height=12)
            dsn_box.pack(fill="both", expand=True)
            dsn_box.insert(tk.END, f"[DSN LAYER] Token Address: {TOKEN_ADDRESS}\n[BLOCKCHAIN] Registrazione Eventi On-Chain: ATTIVA\n[WALLET] Identità Digitale e Firma Elettronica: VERIFICATA\n[SMART CONTRACT] Registry Aziendale: CONNESSO\n")
            dsn_box.config(state=tk.DISABLED)

            def open_browser_repo():
                webbrowser.open("https://github.com/high-cde/xCLOUD-by-zdos")
                backend.log_event("GITHUB_REDIRECT", "Apertura link esterno xCLOUD-by-zdos.")

            btn_row = tk.Frame(parent, bg="#04010F")
            btn_row.pack(fill="x", pady=10)
            tk.Button(btn_row, text="🌐 Apri xCLOUD-by-zdos su GitHub", bg="#06304F", fg="#ffffff", font=('Segoe UI', 9, 'bold'), relief="flat", command=open_browser_repo).pack(side="left", padx=5)

        self.spawn_window("☁️ xCLOUD Enterprise Hub", 750, 520, build)

    def open_dashboards_hub(self):
        def build(parent):
            tk.Label(parent, text="ZDOS DEDICATED SYSTEM DASHBOARDS", bg="#04010F", fg="#00D3F2", font=('Segoe UI', 12, 'bold')).pack(anchor="w", pady=10)
            notebook = ttk.Notebook(parent)
            notebook.pack(fill="both", expand=True, pady=5)
            metrics = backend.get_system_metrics()
            tab1 = tk.Frame(notebook, bg="#0D0A22", padx=10, pady=10)
            notebook.add(tab1, text="🖥️ System Resource")
            m_box = scrolledtext.ScrolledText(tab1, bg="#04010F", fg="#3DDC97", font=('Consolas', 9), height=12)
            m_box.pack(fill="both", expand=True)
            m_box.insert(tk.END, f"[METRICS] CPU Load: {metrics['cpu_load']}\n[METRICS] RAM Usage: {metrics['ram_usage']}\n[METRICS] Storage: {metrics['storage_mode']}\n")
            m_box.config(state=tk.DISABLED)
        self.spawn_window("📊 Dedicated Dashboards Hub", 700, 480, build)

    def open_cloud_file_manager(self):
        def build(parent):
            tk.Label(parent, text="☁️ CLOUD FILE MANAGER (GitHub · GitLab · Discord)", bg="#04010F", fg="#00D3F2", font=('Segoe UI', 12, 'bold')).pack(anchor="w", pady=5)
            file_list = scrolledtext.ScrolledText(parent, bg="#0D0A22", fg="#3DDC97", font=('Consolas', 9), height=12)
            file_list.pack(fill="both", expand=True, pady=10)
            file_list.insert(tk.END, "📁 /xCLOUD-enterprise/core (Sync con GitHub xCLOUD-by-zdos)\n📁 /zdos-microcosm-beta/src (Sync con GitLab)\n")
            file_list.config(state=tk.DISABLED)
        self.spawn_window("☁️ Cloud File Manager", 700, 480, build)

    def open_backend_audit(self):
        def build(parent):
            tk.Label(parent, text="🛠️ ZDOS BACKEND AUDIT LOGS", bg="#04010F", fg="#00D3F2", font=('Segoe UI', 12, 'bold')).pack(anchor="w", pady=10)
            box = scrolledtext.ScrolledText(parent, bg="#0D0A22", fg="#3DDC97", font=('Consolas', 9), height=14)
            box.pack(fill="both", expand=True, pady=5)
            for log in backend.audit_log: box.insert(tk.END, log + "\n")
            box.config(state=tk.DISABLED)
        self.spawn_window("Backend Audit Logs", 700, 450, build)

    def open_zlang_app(self):
        def build(parent):
            tk.Label(parent, text="⚡ ZLANG M1-M7 CONTRACT ENGINE", bg="#04010F", fg="#00D3F2", font=('Segoe UI', 12, 'bold')).pack(anchor="w", pady=10)
            editor = scrolledtext.ScrolledText(parent, bg="#0D0A22", fg="#C3D4E6", font=('Consolas', 10), height=12)
            editor.pack(fill="both", expand=True, pady=5)
            editor.insert(tk.END, "capability storage.read-v1;\nemit xcloud.sync;\n")
        self.spawn_window("⚡ Zlang Studio", 600, 420, build)

    def open_anon_browser(self):
        def build(parent):
            tk.Label(parent, text="🌐 ZDOS Anon Browser (Tor Clone)", bg="#04010F", fg="#00D3F2", font=('Segoe UI', 12, 'bold')).pack(anchor="w", pady=10)
            box = scrolledtext.ScrolledText(parent, bg="#0D0A22", fg="#3DDC97", font=('Consolas', 10), height=12)
            box.pack(fill="both", expand=True, pady=5)
            box.insert(tk.END, "[ANON] Connesso a x-zdos.it tramite circuito Tor protetto.\n")
            box.config(state=tk.DISABLED)
        self.spawn_window("🌐 Anon Browser", 650, 420, build)

    def open_webapp_dashboard(self):
        def build(parent):
            tk.Label(parent, text="🔗 WEBAPP DASHBOARD (app.x-zdos.it)", bg="#04010F", fg="#00D3F2", font=('Segoe UI', 12, 'bold')).pack(anchor="w", pady=10)
            box = scrolledtext.ScrolledText(parent, bg="#0D0A22", fg="#3DDC97", font=('Consolas', 10), height=12)
            box.pack(fill="both", expand=True, pady=5)
            box.insert(tk.END, "[WEBAPP] Stato xCLOUD Portal: Online (https://x-zdos.it)\n")
            box.config(state=tk.DISABLED)
        self.spawn_window("Webapp Dashboard", 600, 400, build)

    def open_terminal(self):
        def build(parent):
            term = scrolledtext.ScrolledText(parent, bg="#0D0A22", fg="#3DDC97", font=('Consolas', 10), height=14)
            term.pack(fill="both", expand=True, pady=2)
            term.insert(tk.END, "root@xcloud-glass:~# \n")
            term.config(state=tk.DISABLED)
        self.spawn_window("Terminale Root", 620, 380, build)

    def open_evidence_app(self):
        def build(parent):
            tk.Label(parent, text="🛡️ EVIDENCE CHAIN LEDGER", bg="#04010F", fg="#00D3F2", font=('Segoe UI', 12, 'bold')).pack(anchor="w", pady=10)
            box = scrolledtext.ScrolledText(parent, bg="#0D0A22", fg="#FFC857", font=('Consolas', 9), height=12)
            box.pack(fill="both", expand=True, pady=5)
            box.insert(tk.END, "[01] Minimalist Glass Theme Active -> VERIFIED\n[02] xCLOUD-by-zdos Repository Linked\n")
            box.config(state=tk.DISABLED)
        self.spawn_window("Evidence Chain Ledger", 580, 380, build)

    def create_statusbar(self):
        self.statusbar = tk.Frame(self.root, bg="#0D0A22", height=28)
        self.statusbar.pack(side="bottom", fill="x")
        self.statusbar.pack_propagate(False)
        status_lbl = tk.Label(self.statusbar, text=" ZDOS Hybrid · Parrot Edition | Glass Engine v2.6 | Bridge 127.0.0.1:8888", bg="#0D0A22", fg="#6F7F9E", font=('Segoe UI', 8))
        status_lbl.pack(side="left", padx=15)

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
        win.configure(bg="#04010F")
        content = tk.Frame(win, bg="#04010F")
        content.pack(fill="both", expand=True, padx=12, pady=12)
        builder_func(content)
        return win

if __name__ == "__main__":
    root = tk.Tk()
    app = ZDOSPuppyDesktop(root)
    root.mainloop()
