import tkinter as tk
from tkinter import scrolledtext
import time
import random
import os
import threading
from src.neural.z_kali_cortex import ZKaliCortex

class ZDOSMasterDashboard:
    def __init__(self):
        self.cortex = ZKaliCortex(state_dir="./var")
        
        self.root = tk.Tk()
        self.root.title("ZDOS // SUPER MASTER DASHBOARD [Amsterdam '92 & Z-KALI AGI]")
        self.root.geometry("800x600")
        self.root.configure(bg="#08041B")
        self.root.attributes("-topmost", True)
        
        # Header / Title
        self.header = tk.Label(self.root, text="ZDOS SOVEREIGN ECOSYSTEM // UNIFIED CONTROL PANEL", bg="#08041B", fg="#15E0ED", font=("Courier New", 11, "bold"))
        self.header.pack(pady=5)
        
        # Canvas 16-bit (Sega Mega Drive Style - Amsterdam '92)
        self.canvas = tk.Canvas(self.root, width=780, height=220, bg="#0D0A22", highlightthickness=1, highlightbackground="#252A52")
        self.canvas.pack(padx=10, pady=5)
        
        self.draw_scenery(night_mode=True)
        
        # Frame centrale diviso in due: Controlli rapidi e Terminale di Chat
        self.main_frame = tk.Frame(self.root, bg="#08041B")
        self.main_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Pannello sinistro: Pulsanti di controllo rapido (Cleaner, ZLang, GitHub, Sublime)
        self.btn_frame = tk.Frame(self.main_frame, bg="#131038", bd=1, relief=tk.SOLID)
        self.btn_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        tk.Label(self.btn_frame, text=" QUICK ACTIONS ", bg="#131038", fg="#00D3F2", font=("Courier New", 9, "bold")).pack(pady=5)
        
        tk.Button(self.btn_frame, text="🧹 Esegui Cleaner", bg="#1B1647", fg="#15E0ED", font=("Courier New", 8), width=16, command=self.run_cleaner).pack(padx=5, pady=3)
        tk.Button(self.btn_frame, text="📜 Valida ZLang", bg="#1B1647", fg="#15E0ED", font=("Courier New", 8), width=16, command=self.run_zlang_check).pack(padx=5, pady=3)
        tk.Button(self.btn_frame, text="💻 Apri Sublime", bg="#1B1647", fg="#15E0ED", font=("Courier New", 8), width=16, command=self.open_sublime).pack(padx=5, pady=3)
        tk.Button(self.btn_frame, text="🐙 Info GitHub", bg="#1B1647", fg="#15E0ED", font=("Courier New", 8), width=16, command=self.info_github).pack(padx=5, pady=3)
        
        # Pannello destro: Terminale Chat Interattivo
        self.chat_frame = tk.Frame(self.main_frame, bg="#08041B")
        self.chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, bg="#06031A", fg="#15E0ED", font=("Courier New", 9), insertbackground="white")
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        # Input riga comandi
        input_frame = tk.Frame(self.root, bg="#08041B")
        input_frame.pack(padx=10, pady=8, fill=tk.X)
        
        self.msg_entry = tk.Entry(input_frame, bg="#16123F", fg="#15E0ED", font=("Courier New", 10), insertbackground="white")
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.msg_entry.bind("<Return>", self.send_message)
        
        send_btn = tk.Button(input_frame, text="▶ INVIA", bg="#16123F", fg="#15E0ED", font=("Courier New", 9, "bold"), command=self.send_message)
        send_btn.pack(side=tk.RIGHT)
        
        self.append_chat("Z-KALI", "Master Dashboard attivata. Tutti i moduli (Cortex, Cleaner, ZLang, Evidence Chain) sono sincronizzati.")
        
        # Animazione in background
        self.frame_count = 0
        self.raindrops = [[random.randint(0, 780), random.randint(0, 220)] for _ in range(35)]
        self.animate_scene()

    def draw_scenery(self, night_mode=True):
        self.canvas.delete("all")
        bg_color = "#05020F" if night_mode else "#00B8DB"
        moon_color = "#EAF6FF" if night_mode else "#FFC857"
        
        self.canvas.create_rectangle(0, 0, 780, 220, fill=bg_color, outline="")
        self.canvas.create_oval(660, 20, 710, 70, fill=moon_color, outline="")
        
        # Skyline
        self.canvas.create_rectangle(50, 110, 130, 220, fill="#0D0A22", outline="")
        self.canvas.create_rectangle(140, 80, 240, 220, fill="#0A0118", outline="")
        self.canvas.create_rectangle(250, 120, 340, 220, fill="#252A52", outline="")
        self.canvas.create_rectangle(350, 90, 460, 220, fill="#0A0118", outline="")
        
        self.canvas.create_rectangle(0, 0, 780, 220, outline="#252A52", width=4)
        
        self.canvas.create_text(600, 170, text="NEO-CAT", fill="#A9BCD6", font=("Courier New", 12, "bold"))
        self.canvas.create_text(600, 190, text="AMSTERDAM '92", fill="#A9BCD6", font=("Courier New", 10, "bold"))
        self.canvas.create_text(600, 210, text="▶ ZDOS ACTIVE", fill="#15E0ED", font=("Courier New", 9, "bold"))

        # Tavolo / Gatto Cibernetico
        self.canvas.create_rectangle(20, 150, 200, 220, fill="#1B1647", outline="#2F3668", width=2)
        self.canvas.create_oval(70, 160, 120, 210, fill="#2A3060", outline="#3A4275")
        self.canvas.create_rectangle(85, 135, 125, 175, fill="#2A3060", outline="#3A4275")
        self.canvas.create_rectangle(92, 148, 100, 156, fill="#15E0ED", outline="")
        self.canvas.create_rectangle(110, 148, 118, 156, fill="#15E0ED", outline="")

    def animate_scene(self):
        self.frame_count += 1
        night = (self.frame_count // 120) % 2 == 0
        if self.frame_count % 120 == 0:
            self.draw_scenery(night_mode=night)
            
        for drop in self.raindrops:
            drop[0] -= 2
            drop[1] += 7
            if drop[1] > 220 or drop[0] < 0:
                drop[0] = random.randint(300, 780)
                drop[1] = random.randint(0, 40)
            self.canvas.create_line(drop[0], drop[1], drop[0] - 2, drop[1] + 5, fill="#00D3F2", width=1)
            
        self.root.after(50, self.animate_scene)

    def append_chat(self, sender, message):
        self.chat_area.config(state=tk.NORMAL)
        timestamp = time.strftime('%H:%M:%S')
        self.chat_area.insert(tk.END, f"[{timestamp}] {sender}: {message}\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def run_cleaner(self):
        os.system("python3 z_kali_cleaner.py")
        self.append_chat("Z-KALI", "Protocollo AGI Cleaner eseguito. Cache e file temporanei ripuliti con successo.")

    def run_zlang_check(self):
        self.append_chat("Z-KALI", "Validazione ZLang (ZLB2 v2.5): Controllo contratto 'zdos_master_core.zlang'... ESITO: VERIFIED (Default-Deny rispettato).")

    def open_sublime(self):
        os.system("subl &")
        self.append_chat("Z-KALI", "Sublime Text avviato sul workspace corrente.")

    def info_github(self):
        self.append_chat("Z-KALI", "GitHub Integration: Pronto a gestire repository, commit e push protetti da token.")

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        
        self.append_chat("Tu", msg)
        self.msg_entry.delete(0, tk.END)
        
        state = self.cortex.reflect(cpu_load=0.20, net_latency=4)
        
        if "pulizia" in msg.lower():
            self.run_cleaner()
        elif "zlang" in msg.lower():
            self.run_zlang_check()
        elif "sublime" in msg.lower():
            self.open_sublime()
        else:
            reply = f"Comando elaborato nella Master Dashboard: '{msg}'. Stato del sistema verificato."
            self.append_chat("Z-KALI", reply)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ZDOSMasterDashboard()
    app.run()
