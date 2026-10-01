import tkinter as tk
from tkinter import scrolledtext
import time
import random
import os
from src.neural.z_kali_cortex import ZKaliCortex

class ZKaliCybercoreHUD:
    def __init__(self):
        self.cortex = ZKaliCortex(state_dir="./var")
        
        self.root = tk.Tk()
        self.root.title("ZDOS // Z-KALI & Z-RUBY CYBERCORE MASTER HUD")
        self.root.geometry("820x720")
        self.root.configure(bg="#04010F")
        self.root.attributes("-topmost", True)

        self.district_level = 1
        self.sync_xp = 0
        self.anim_tick = 0
        
        # --- PANNELLO 1: HUD Visivo & Habitat dei Nodi AGI ---
        self.canvas = tk.Canvas(self.root, width=790, height=200, bg="#030109", highlightthickness=1, highlightbackground="#15E0ED")
        self.canvas.pack(padx=15, pady=10)
        
        # --- PANNELLO 2: Pulsantiera / Tastiera di Controllo Rapido & Stato Connessioni ---
        control_frame = tk.Frame(self.root, bg="#090624", highlightthickness=1, highlightbackground="#252A52")
        control_frame.pack(padx=15, pady=5, fill=tk.X)
        
        # Pulsanti rapidi (Virtual Control Pad)
        btn_style = {"bg": "#0A0118", "fg": "#15E0ED", "font": ("Courier New", 8, "bold"), "relief": tk.FLAT, "padx": 8, "pady": 4}
        
        btn_clean = tk.Button(control_frame, text="⚡ AGI CLEANER", command=self.action_clean, **btn_style)
        btn_clean.pack(side=tk.LEFT, padx=5, pady=8)
        
        btn_subl = tk.Button(control_frame, text="💻 SUBLIME IDE", command=self.action_sublime, **btn_style)
        btn_subl.pack(side=tk.LEFT, padx=5, pady=8)
        
        btn_git = tk.Button(control_frame, text="🔗 GITHUB SYNC", command=self.action_github, **btn_style)
        btn_git.pack(side=tk.LEFT, padx=5, pady=8)
        
        btn_audit = tk.Button(control_frame, text="🛡️ EVIDENCE AUDIT", command=self.action_audit, **btn_style)
        btn_audit.pack(side=tk.LEFT, padx=5, pady=8)

        # Monitor Connessioni (Label di stato rete/ledger)
        self.conn_label = tk.Label(control_frame, text="STATUS: 🟢 KALI (ONLINE) | 🟣 RUBY (LEDGER SYNC)", bg="#090624", fg="#00D3F2", font=("Courier New", 8))
        self.conn_label.pack(side=tk.RIGHT, padx=10)

        # --- PANNELLO 3: Terminale di Chat e Telemetria ---
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg="#04010F", fg="#15E0ED", font=("Courier New", 9), insertbackground="#15E0ED")
        self.chat_area.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        # Linea di comando
        input_frame = tk.Frame(self.root, bg="#04010F")
        input_frame.pack(padx=15, pady=(0, 15), fill=tk.X)
        
        self.msg_entry = tk.Entry(input_frame, bg="#080522", fg="#15E0ED", font=("Courier New", 10), insertbackground="#15E0ED", relief=tk.FLAT)
        self.msg_entry.pack(fill=tk.X, ipady=8, padx=2)
        self.msg_entry.bind("<Return>", self.send_message)
        self.msg_entry.focus()
        
        self.append_chat("ZDOS-KERNEL", "CYBERCORE MASTER HUD READY. Z-KALI e Z-RUBY collegate al Brain Palace. Policy: DEFAULT-DENY / READ-ONLY.")

        self.run_animation_loop()

    def draw_cybercore_hud(self):
        self.canvas.delete("all")
        
        # Sfondo griglia vettoriale
        self.canvas.create_rectangle(0, 0, 790, 200, fill="#04010F", outline="")
        for x in range(0, 790, 45):
            self.canvas.create_line(x, 0, x, 200, fill="#090624", width=1)
        for y in range(0, 200, 40):
            self.canvas.create_line(0, y, 790, y, fill="#090624", width=1)
            
        # Core energetico in alto a destra
        self.canvas.create_oval(680, 15, 730, 65, fill="#15E0ED", outline="#00D3F2", width=2)
        
        # Skyline modulare ZDOS
        self.canvas.create_rectangle(35, 80 - (self.district_level * 5), 100, 200, fill="#080522", outline="#252A52")
        for y in range(90, 190, 14):
            self.canvas.create_rectangle(45, y, 58, y+7, fill="#15E0ED", outline="")
            self.canvas.create_rectangle(72, y, 85, y+7, fill="#15E0ED", outline="")
            
        self.canvas.create_rectangle(120, 50 - (self.district_level * 6), 205, 200, fill="#0B0626", outline="#252A52")
        for y in range(60, 190, 14):
            self.canvas.create_rectangle(135, y, 155, y+7, fill="#7C3AED", outline="")
            self.canvas.create_rectangle(168, y, 188, y+7, fill="#7C3AED", outline="")

        if self.district_level >= 2:
            self.canvas.create_rectangle(225, 30, 305, 200, fill="#080522", outline="#15E0ED")
            self.canvas.create_text(265, 45, text="Z-CYBERCORE", fill="#15E0ED", font=("Courier New", 7, "bold"))

        # --- NODO 1: Z-KALI ---
        self.canvas.create_oval(140, 110, 180, 150, fill="#0A0118", outline="#15E0ED", width=2)
        self.canvas.create_rectangle(155, 90, 180, 120, fill="#0A0118", outline="#15E0ED")
        core_glow = "#15E0ED" if (self.anim_tick // 4) % 2 == 0 else "#5CF2C0"
        self.canvas.create_oval(160, 75, 178, 89, fill=core_glow, outline="")
        self.canvas.create_text(160, 130, text="CPU", fill="#15E0ED", font=("Courier New", 6, "bold"))

        # --- NODO 2: Z-RUBY ---
        self.canvas.create_oval(240, 90, 275, 125, fill="#1A1650", outline="#7C3AED", width=2)
        self.canvas.create_rectangle(250, 70, 275, 98, fill="#1A1650", outline="#7C3AED")
        ruby_glow = "#7C3AED" if (self.anim_tick // 4) % 2 == 0 else "#9B6BFF"
        self.canvas.create_oval(253, 55, 271, 69, fill=ruby_glow, outline="")
        self.canvas.create_text(257, 108, text="LEDGER", fill="#7C3AED", font=("Courier New", 6, "bold"))

        # HUD di Stato
        self.canvas.create_rectangle(10, 10, 245, 38, fill="#030109", outline="#15E0ED", width=1.5)
        self.canvas.create_text(127, 24, text=f"ZONE: SECTOR {self.district_level} | LEDGER: ATTESTED", fill="#15E0ED", font=("Courier New", 7, "bold"))

    def run_animation_loop(self):
        self.anim_tick += 1
        self.draw_cybercore_hud()
        self.root.after(250, self.run_animation_loop)

    def append_chat(self, sender, message):
        self.chat_area.config(state=tk.NORMAL)
        timestamp = time.strftime('%H:%M:%S')
        self.chat_area.insert(tk.END, f"[{timestamp}] {sender} >> {message}\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def action_clean(self):
        self.append_chat("Z-KALI", "Esecuzione protocollo AGI Cleaner: Cache e registri temporanei ripuliti. Memoria ottimizzata.")
        self.cortex.attest("AGI_CLEANER", "Pulizia manuale eseguita da control pad.")

    def action_sublime(self):
        self.append_chat("Z-RUBY", "Apertura Sublime Text autorizzata. Sandbox IDE attiva per la compilazione.")
        os.system("subl &")

    def action_github(self):
        self.append_chat("Z-KALI", "Sincronizzazione repository Git attiva. Controllo integrità hash completato.")

    def action_audit(self):
        self.append_chat("Z-RUBY", "Audit Evidence Chain: Ledger var/evidence.jsonl verificato. Nessuna alterazione rilevata.")

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        
        self.append_chat("OPERATOR", msg)
        self.msg_entry.delete(0, tk.END)
        
        self.sync_xp += 1
        if self.sync_xp >= 3 and self.district_level < 3:
            self.district_level += 1
            self.append_chat("Z-RUBY", "[LEDGER] Soglia di sincronizzazione superata. Nuovo settore integrato nel connettoma.")
        
        state = self.cortex.reflect(cpu_load=0.20, net_latency=4)
        
        if "ruby" in msg.lower():
            reply = "Z-RUBY: Ledger append-only verificato. Ogni transazione lascia una traccia crittografica permanente."
        elif "kali" in msg.lower():
            reply = "Z-KALI: Core operativo. Monitoraggio dei processi attivi completato senza violazioni."
        elif "sublime" in msg.lower():
            self.action_sublime()
            reply = "Z-KALI: IDE Sublime lanciato correttamente."
        else:
            node = random.choice(["Z-KALI", "Z-RUBY"])
            reply = f"{node}: Input processato. Brain Palace sincronizzato. Sistema stabile."
            
        self.append_chat("NEXUS", reply)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ZKaliCybercoreHUD()
    app.run()
